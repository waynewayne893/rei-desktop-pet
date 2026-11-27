#!/usr/bin/env python3
"""Verify and gather P4-C direction candidates without assembling an atlas."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from shutil import copyfile

from PIL import Image, ImageChops, ImageOps

from p4c_register_batch import ANGLES, FORMS, detached_alpha, fingerprint, load_pilot, save_json

CARDINALS = ("000", "090", "180", "270")
MASTERS = {
    "rei-school": "02_标准化母版/rei-school/master-rgba.png",
    "rei-white": "02_标准化母版/P3-FIX/rei-white-master-rgba-p3-fix.png",
    "rei-black": "02_标准化母版/rei-black/master-rgba.png",
}
STAGE = Path("07_QA验收/P4-C")
PILOT = Path("07_QA验收/CODEX-CLOUD-ART-PILOT")
ARCHIVE = Path("07_QA验收/P4-B/human-acceptance")
BASELINE = "6b4229f76d44caf234c3120d65a71bd59989e647"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def register_reuse(root: Path) -> dict:
    ledger = read(root / ARCHIVE / "ACCEPTANCE_LEDGER.json")
    export = ledger["archives"]["pilot"]
    decision_path = ARCHIVE / export["path"]
    require(fingerprint(root / decision_path) == export["sha256"], "Pilot acceptance export hash differs.")
    review = {decision["id"]: decision for decision in read(root / decision_path)["decisions"]}
    stage = root / STAGE / "rei-black"
    (stage / "frames").mkdir(parents=True, exist_ok=True)
    raw = PILOT / "raw/directions-attempt-02.png"
    raw_sha = fingerprint(root / raw)
    master_sha = fingerprint(root / MASTERS["rei-black"])
    qa_path = PILOT / "evidence/directions-attempt-02-qa.json"
    qa = read(root / qa_path)
    require(qa["source"] == raw.name and qa["structure"] == "STRUCTURE_PASS", "Original pilot technical gate failed.")
    require(qa["raw"]["alpha_cleanup"]["source_png_sha256"] == raw_sha, "Pilot source hash differs from QA.")
    prior = {frame["id"]: frame for frame in qa["registration"]["frames"]}
    bindings = {str(entry["angle_degrees"]).zfill(3): entry for entry in ledger["p4c_reuse_verified"]}
    require(set(bindings) == set(CARDINALS), "Closeout ledger lacks the exact four black cardinal bindings.")
    result = {}
    for angle in CARDINALS:
        decision = review[angle]
        entry = bindings[angle]
        source = PILOT / f"frames/directions/attempt-02/{angle}.png"
        frame_sha = fingerprint(root / source)
        require(entry["frame_path"] == source.as_posix() and entry["frame_sha256"] == frame_sha
                and entry["native_source_path"] == raw.as_posix() and entry["native_source_sha256"] == raw_sha,
                f"Closeout ledger asset mismatch at {angle}.")
        expected = {
            "candidate": {"version": "codex-cloud-pilot/attempt-02", "source": raw_sha, "frames": [frame_sha]},
            "reference": {"version": "P3 派生 RGBA 母版", "source": master_sha, "frames": []},
        }
        require(decision["status"] == "ACCEPTED" and decision["binding"] == expected,
                f"Pilot user acceptance mismatch at {angle}.")
        require(not prior[angle]["errors"], f"Reused frame failed archived registration QA at {angle}.")
        with Image.open(root / source) as image:
            alpha = detached_alpha(image)
        dst = stage / "frames" / f"{angle}.png"
        copyfile(root / source, dst)
        require(fingerprint(dst) == frame_sha, f"Reused PNG bytes mismatch at {angle}.")
        result[angle] = {
            "form": "rei-black", "angle": angle, "path": dst.relative_to(root).as_posix(),
            "sha256": frame_sha, "source_path": raw.as_posix(), "source_sha256": raw_sha,
            "origin": "REUSED_PILOT", "human_status": "ACCEPTED", "version": "codex-cloud-pilot/attempt-02",
            "pilot_path": source.as_posix(), "qa_path": qa_path.as_posix(),
            "acceptance_path": decision_path.as_posix(), "acceptance_sha256": export["sha256"],
            "solid_height": prior[angle]["solid_height"], "foot_anchor": prior[angle]["foot_anchor_measured"],
            "detached_alpha_components": alpha,
        }
    save_json(stage / "reuse.json", result)
    return result


def choose_form(root: Path, form: str, reuse: dict) -> list[dict]:
    base = root / STAGE / form
    selected = read(base / "selection.json")
    reused = reuse if form == "rei-black" else {}
    require(set(selected) == set(ANGLES) - set(reused), f"Incomplete or noncanonical selection for {form}.")
    (base / "frames").mkdir(parents=True, exist_ok=True)
    entries = []
    for i, angle in enumerate(ANGLES):
        if angle in reused:
            entry = reused[angle]
        else:
            batch = selected[angle]
            qa_path = base / "batches" / f"{batch}.json"
            qa = read(qa_path)
            require(qa["form"] == form and qa["batch"] == batch and qa["structure"] == "STRUCTURE_PASS",
                    f"Invalid selected batch for {form}/{angle}.")
            frame = next(f for f in qa["registration"]["frames"] if f["id"] == angle)
            raw_path = root / qa["source_path"]
            require(fingerprint(raw_path) == qa["source_sha256"], f"Selected source hash changed: {raw_path}.")
            attempt = root / frame["path"]
            dst = base / "frames" / f"{angle}.png"
            require(not frame["errors"] and frame["sha256"] == fingerprint(attempt), f"Selected frame hash changed: {attempt}.")
            copyfile(attempt, dst)
            entry = {
                "form": form, "angle": angle, "path": dst.relative_to(root).as_posix(), "sha256": frame["sha256"],
                "source_path": qa["source_path"], "source_sha256": qa["source_sha256"],
                "origin": "GENERATED", "human_status": "PENDING_HUMAN_REVIEW", "version": f"p4c/{batch}",
                "qa_path": qa_path.relative_to(root).as_posix(), "attempt_path": frame["path"],
                "solid_height": frame["solid_height"], "foot_anchor": frame["foot_anchor_measured"],
                "detached_alpha_components": frame["detached_alpha_components"],
            }
        entries.append({**entry, "row": 9 + i // 8, "col": i % 8})
    return entries


def compose_previews(root: Path, form: str, entries: list[dict], pilot, toolkit) -> dict:
    base = root / STAGE / form / "review"
    base.mkdir(parents=True, exist_ok=True)
    frames = []
    checks = []
    seen_pixels = set()
    for entry in entries:
        path = root / entry["path"]
        require(fingerprint(path) == entry["sha256"], f"Final PNG hash changed: {path}.")
        with Image.open(path) as image:
            frame = image.copy()
        check = toolkit.analyze_cell(frame, f"{form}/{entry['angle']}")
        require(not check["errors"], f"Final cell failed: {check['errors']}.")
        require(check["pixel_sha256"] not in seen_pixels, f"Duplicate vertices for {form}.")
        seen_pixels.add(check["pixel_sha256"])
        frames.append(frame)
        checks.append({
            "angle": entry["angle"], "solid_height": entry["solid_height"], "foot_anchor": entry["foot_anchor"],
            "detached_alpha_components": entry["detached_alpha_components"], **check,
        })
    labels = [f"{e['angle']} deg" for e in entries]
    outputs = []
    for name, background in (("light", "#eef0f4"), ("dark", "#252932")):
        sheet = pilot.stack([pilot.compose(frames[:8], labels[:8], background),
                             pilot.compose(frames[8:], labels[8:], background)])
        sheet_path = base / f"contact-{name}.png"
        sheet.save(sheet_path)
        animation = [pilot.compose([frame], [label], background, 2) for frame, label in zip(frames, labels)]
        gif_path = base / f"clockwise-{name}.gif"
        animation[0].save(gif_path, save_all=True, append_images=animation[1:], duration=330, loop=0,
                          disposal=2, optimize=False)
        outputs.extend([sheet_path, gif_path])
    adjacency = []
    for i, (a, b) in enumerate(zip(frames, frames[1:] + frames[:1])):
        require(ImageOps.mirror(a).tobytes() != b.tobytes(), f"Adjacent frame is an exact mirror for {form}: {labels[i]}.")
        mask_a, mask_b = [pilot.solid(im.getchannel("A")) for im in (a, b)]
        both = ImageChops.multiply(mask_a, mask_b).histogram()[255]
        either = ImageChops.lighter(mask_a, mask_b).histogram()[255]
        adjacency.append({"from": entries[i]["angle"], "to": entries[(i+1) % 16]["angle"], "silhouette_iou": round(both / either, 5)})
    for li, ri in ((1, 15), (2, 14), (3, 13), (4, 12), (5, 11), (6, 10), (7, 9)):
        require(ImageOps.mirror(frames[li]).tobytes() != frames[ri].tobytes(),
                f"Opposite-side frames are exact mirrors for {form}: {labels[li]}, {labels[ri]}.")
    return {"file_sha256": {p.relative_to(root).as_posix(): fingerprint(p) for p in outputs},
            "frames": checks, "clockwise_adjacency": adjacency}


def finalize(root: Path, reuse: dict) -> None:
    pilot = load_pilot(root)
    toolkit = pilot.load_toolkit(root)
    frames, qa = [], {}
    for form in FORMS:
        entries = choose_form(root, form, reuse)
        frames.extend(entries)
        qa[form] = compose_previews(root, form, entries, pilot, toolkit)
    counts = {status: sum(1 for f in frames if f["human_status"] == status)
              for status in ("ACCEPTED", "PENDING_HUMAN_REVIEW")}
    require(len(frames) == 48 and counts == {"ACCEPTED": 4, "PENDING_HUMAN_REVIEW": 44}, "Incorrect stage totals.")
    base = root / STAGE
    save_json(base / "P4C_STRUCTURE_QA.json", {
        "status": "STRUCTURE_PASS", "total_frames": len(frames), "human_status_counts": counts,
        "resize_rule": "Isotropic scale shared per generation batch; each planted foot anchor translated to 96,195",
        "alpha_rule": "P4 pilot unchanged: raw RGBA PNG, only alpha exactly 1 cleared before registration; all registered borders transparent",
        "forms": qa,
    })
    save_json(base / "P4C_DIRECTION_ASSET_MANIFEST.json", {
        "schema_version": 1, "stage": "P4-C", "baseline_commit": BASELINE, "frame_count": len(frames),
        "angle_order": list(ANGLES), "human_status_counts": counts,
        "masters": {form: {"path": path, "sha256": fingerprint(root / path)} for form, path in MASTERS.items()},
        "frames": frames,
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reuse-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    reuse = register_reuse(root)
    print("Registered four accepted black pilot frames with verified native PNG and human binding.")
    if not args.reuse_only:
        finalize(root, reuse)
        print("Verified and assembled review evidence for 48 directions (4 accepted, 44 pending).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
