"""Scratch-only alpha inspection, registration and review assets."""
import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFont


def load_toolkit(root):
    spec = importlib.util.spec_from_file_location(
        "rei_atlas_tools", root / "06_共用工具/rei_atlas_tools.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def solid(alpha):
    return alpha.point(lambda value: 255 if value >= 128 else 0)


def runs(mask):
    projection = mask.getprojection()[0]
    boundaries = [i for i, (a, b) in enumerate(zip([0] + projection, projection + [0])) if bool(a) != bool(b)]
    return list(zip(boundaries[::2], boundaries[1::2]))


def inspect(path, expected):
    with Image.open(path) as source:
        info = {"format": source.format, "mode": source.mode, "size": list(source.size)}
        if source.format != "PNG" or source.mode != "RGBA":
            return info, [], ["Raw output is not an RGBA PNG"]
        image = source.copy()
    raw_alpha = image.getchannel("A")
    hist = raw_alpha.histogram()
    # Drop only alpha 1/255 observed in blank gutters. Keep original file bytes.
    alpha = raw_alpha.point(lambda value: 0 if value == 1 else value)
    mask = solid(alpha)
    groups = runs(mask)
    w, h = image.size
    border_boxes = ((0, 0, w, 1), (0, h-1, w, h), (0, 0, 1, h), (w-1, 0, w, h))
    raw_border_max = max(raw_alpha.crop(box).getextrema()[1] for box in border_boxes)
    info.update(
        alpha_extrema=raw_alpha.getextrema(), alpha_zero=hist[0],
        alpha_partial=sum(hist[1:255]), alpha_opaque=hist[255], alpha_bbox=raw_alpha.getbbox(),
        solid_x_spans=groups, raw_border_alpha_max=raw_border_max,
        raw_border_transparent=raw_border_max == 0,
        registration_alpha_floor=1, raw_alpha_one_pixels=hist[1],
        effective_alpha_bbox=alpha.getbbox(),
    )
    errors = []
    if not hist[0] or not sum(hist[128:]):
        errors.append("Expected transparent background and visible figures")
    if raw_border_max > 1:
        errors.append("Alpha above the noise floor touches a raw canvas border")
    before_pixel_sha256 = sha256(image.tobytes()).hexdigest()
    image.putalpha(alpha)
    info["alpha_cleanup"] = {
        "rule": "alpha == 1 becomes 0; all RGB bytes and other alpha values are unchanged",
        "threshold_u8": 1,
        "changed_pixels": hist[1],
        "source_png_sha256": sha256(path.read_bytes()).hexdigest(),
        "pre_cleanup_rgba_pixel_sha256": before_pixel_sha256,
        "post_cleanup_rgba_pixel_sha256": sha256(image.tobytes()).hexdigest(),
    }
    if len(groups) != expected:
        return info, [], [*errors, f"Expected {expected} separated silhouettes, found {len(groups)}"]
    edges = [0, *[(a[1] + b[0]) // 2 for a, b in zip(groups, groups[1:])], image.width]
    info["raw_internal_split_alpha_max"] = [raw_alpha.crop((x, 0, x+1, h)).getextrema()[1] for x in edges[1:-1]]
    poses = []
    for index, (left, right) in enumerate(zip(edges, edges[1:])):
        crop = image.crop((left, 0, right, image.height))
        crop_alpha = crop.getchannel("A")
        box = crop_alpha.getbbox()
        solid_box = solid(crop_alpha).getbbox()
        if not box or not solid_box:
            errors.append(f"Pose {index+1} is empty")
            continue
        if box[0] == 0 or box[2] == crop.width:
            errors.append(f"Pose {index+1} alpha touches a split edge")
        foot_band = max(3, round((solid_box[3] - solid_box[1]) * 0.045))
        feet = solid(crop_alpha).crop((0, solid_box[3]-foot_band, crop.width, solid_box[3])).getbbox()
        foot_x = (feet[0] + feet[2]) / 2
        poses.append((crop.crop(box), box, solid_box, foot_x))
    info["split_edges"] = edges
    return info, poses, errors


def register(poses, ids, folder, toolkit, lock_ground):
    heights = [bounds[3] - bounds[1] for _, _, bounds, _ in poses]
    baseline = heights[0] if lock_ground else median(heights)
    scale = 188 / baseline
    shared_ground = poses[0][2][3]
    images = []
    entries = []
    for name, (crop, box, bounds, foot_x) in zip(ids, poses):
        size = tuple(round(axis * scale) for axis in crop.size)
        resized = crop.resize(size, Image.Resampling.LANCZOS)
        ground = shared_ground if lock_ground else bounds[3]
        xy = (96 - round((foot_x-box[0])*scale), 195 - round((ground-box[1])*scale))
        frame = Image.new("RGBA", (192, 208))
        frame.paste(resized, xy)
        frame = toolkit.clear_transparent_rgb(frame)
        frame.save(folder / f"{name}.png")
        check = toolkit.analyze_cell(frame, name)
        solid_mask = solid(frame.getchannel("A"))
        bbox = solid_mask.getbbox()
        if (min(xy) < 0 or xy[0]+size[0] > 192 or xy[1]+size[1] > 208):
            check["errors"].append("Registered crop exceeds frame")
        if bbox:
            foot_band = max(3, round((bbox[3]-bbox[1])*0.045))
            feet = solid_mask.crop((0, bbox[3]-foot_band, 192, bbox[3])).getbbox()
            registered_x = (feet[0]+feet[2])/2
            if abs(registered_x-96) > 2 or abs(bbox[3]-195) > 4:
                check["errors"].append(f"Foot registration outside tolerance: {(registered_x, bbox[3])}")
        else:
            registered_x = None
        entries.append({
            "id": name, "source_solid_bbox_in_strip_slot": bounds, "offset": xy,
            "registered_solid_bbox": bbox, "solid_height": bbox[3]-bbox[1] if bbox else None,
            "foot_anchor_measured": [registered_x, bbox[3] if bbox else None], **check,
        })
        images.append(frame)
    return images, {"row_isotropic_scale": scale, "source_height_baseline": baseline,
                    "shared_source_ground": shared_ground if lock_ground else None, "frames": entries}


def compose(frames, labels, bg, scale=1):
    margin, caption = 12, 24
    step = 192*scale + margin
    canvas = Image.new("RGB", (len(frames)*step + margin, 208*scale + 2*margin + caption), bg)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=14)
    dark = bg == "#252932"
    color = "#e8eaf0" if dark else "#20242b"
    for i, (image, name) in enumerate(zip(frames, labels)):
        x = margin + i*step
        enlarged = image.resize((192*scale, 208*scale), Image.Resampling.NEAREST)
        canvas.paste(enlarged, (x, margin+caption), enlarged)
        draw.text((x+96*scale, margin), name, font=font, fill=color, anchor="mt")
    return canvas


def stack(rows):
    result = Image.new("RGB", (max(im.width for im in rows), sum(im.height for im in rows)), "#81858c")
    y = 0
    for row in rows:
        result.paste(row, (0, y))
        y += row.height
    return result


def baseline_frames(root, outfit, state):
    prefixes = {"school": "03_校服绫波丽", "black": "05_黑色战斗服"}
    count = 6
    if state == "idle":
        path = root / prefixes[outfit] / "P4-B/delivery/spritesheet-standard.png"
        with Image.open(path) as atlas:
            return [atlas.crop((i*192, 0, (i+1)*192, 208)) for i in range(count)]
    folder = root / prefixes[outfit] / f"P4-B/candidates/attempt-01/{state}/frames"
    return [Image.open(folder / f"{i:02}.png").convert("RGBA") for i in range(count)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("group", choices=["waiting", "directions"])
    parser.add_argument("input", type=Path)
    parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    evidence = out / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    toolkit = load_toolkit(args.root)
    waiting = args.group == "waiting"
    ids = [f"{i:02}" for i in range(1, 7)] if waiting else ["000", "090", "180", "270"]
    raw, poses, errors = inspect(args.input, len(ids))
    w, h = raw["size"]
    if waiting and w != 3*h:
        errors.append(f"Waiting raw ratio is {w}:{h}, expected exactly 3:1")
    result = {"source": args.input.name, "raw": raw, "errors": errors}
    tech_ok = False
    if len(poses) == len(ids):
        folder = out / "frames" / args.group / args.attempt
        folder.mkdir(parents=True, exist_ok=True)
        frames, registration = register(poses, ids, folder, toolkit, waiting)
        result["registration"] = registration
        baseline = baseline_frames(args.root, "school" if waiting else "black", "waiting" if waiting else "idle")
        result["existing_solid_bounds"] = [solid(im.getchannel("A")).getbbox() for im in baseline]
        if len({f["pixel_sha256"] for f in registration["frames"]}) != len(ids):
            errors.append("Any two registered frames must have different pixels")
        if waiting and registration["frames"][0]["solid_height"] not in (187, 188, 189):
            errors.append("Neutral standing height outside 188 px baseline tolerance")
        tech_ok = not errors and all(not f["errors"] for f in registration["frames"])
        label = "Pilot" if tech_ok else "Failed sample"
        stem = f"{args.group}-{args.attempt}"
        backgrounds = ("#eef0f4", "#252932")
        if waiting:
            for bg, suffix in zip(backgrounds, ("light", "dark")):
                comparisons = [compose([old, new], ["Existing", label], bg, 2) for old, new in zip(baseline, frames)]
                comparisons[0].save(evidence / f"{stem}-comparison-{suffix}.gif",
                                    save_all=True, append_images=comparisons[1:],
                                    duration=toolkit.ROW_DURATIONS["waiting"], loop=0, disposal=2, optimize=False)
            rows = []
            for bg in backgrounds:
                rows += [compose(baseline, [f"Existing {i}" for i in ids], bg),
                         compose(frames, [f"{label} {i}" for i in ids], bg)]
            stack(rows).save(evidence / f"{stem}-edges.png")
        else:
            rows = [compose(frames, [f"{i} deg" for i in ids], bg, 2) for bg in backgrounds]
            stack(rows).save(evidence / f"{stem}-contact.png")
    result["structure"] = "STRUCTURE_PASS" if tech_ok else "FAILED"
    target = evidence / f"{args.group}-{args.attempt}-qa.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"structure": result["structure"], "raw": raw, "errors": errors,
                      "frames": [{"id": f["id"], "height": f["solid_height"],
                                  "anchor": f["foot_anchor_measured"], "errors": f["errors"]}
                                 for f in result.get("registration", {}).get("frames", [])]}, indent=2))
    return 0 if tech_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
