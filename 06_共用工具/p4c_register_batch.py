#!/usr/bin/env python3
"""Register a new P4-C generation batch under the approved pilot Alpha gate."""
from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import re

from PIL import Image, UnidentifiedImageError

FORMS = ("rei-school", "rei-white", "rei-black")
ANGLES = ("000", "022.5", "045", "067.5", "090", "112.5", "135", "157.5",
          "180", "202.5", "225", "247.5", "270", "292.5", "315", "337.5")


def load_pilot(root: Path):
    spec = spec_from_file_location("pilot_qa", root / "07_QA验收/CODEX-CLOUD-ART-PILOT/pilot_qa.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def detached_alpha(image: Image.Image) -> list[dict[str, int]]:
    w, h = image.size
    values = image.getchannel("A").tobytes()
    unvisited = {divmod(i, w) for i, alpha in enumerate(values) if alpha}
    groups = []
    while unvisited:
        queue = deque([unvisited.pop()])
        size = peak = 0
        while queue:
            y, x = queue.popleft()
            size += 1
            peak = max(peak, values[y * w + x])
            for ny in range(max(0, y - 1), min(h, y + 2)):
                for nx in range(max(0, x - 1), min(w, x + 2)):
                    if (ny, nx) in unvisited:
                        unvisited.remove((ny, nx))
                        queue.append((ny, nx))
        groups.append({"pixel_count": size, "max_alpha_u8": peak})
    return sorted(groups, key=lambda group: (group["pixel_count"], group["max_alpha_u8"]), reverse=True)[1:] if groups else []


def fingerprint(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def register_batch(root: Path, form: str, batch: str, angles: list[str]) -> dict:
    base = root / "07_QA验收/P4-C" / form
    source = base / "raw" / f"{batch}.png"
    prompt = source.with_suffix(".txt")
    pilot = load_pilot(root)
    toolkit = pilot.load_toolkit(root)
    result = {
        "form": form, "batch": batch, "angles": angles,
        "source_path": source.relative_to(root).as_posix(),
        "source_sha256": fingerprint(source),
    }
    if prompt.is_file():
        result["prompt_path"] = prompt.relative_to(root).as_posix()
        result["prompt_sha256"] = fingerprint(prompt)
    try:
        raw, poses, errors = pilot.inspect(source, len(angles))
    except (UnidentifiedImageError, OSError) as error:
        raw, poses, errors = {}, [], [str(error)]
    result["raw"], result["errors"] = raw, errors
    frames = []
    if len(poses) == len(angles):
        target = base / "attempts" / batch
        target.mkdir(parents=True, exist_ok=True)
        images, registration = pilot.register(poses, angles, target, toolkit, False)
        frames = registration["frames"]
        for frame, image in zip(frames, images):
            path = target / f"{frame['id']}.png"
            frame["path"] = path.relative_to(root).as_posix()
            frame["sha256"] = fingerprint(path)
            frame["detached_alpha_components"] = detached_alpha(image)
            if frame["solid_height"] is None or abs(frame["solid_height"] - 188) > 4:
                frame["errors"].append("Standing height outside 188 px ±4 registration check.")
            foot_x, foot_y = frame["foot_anchor_measured"]
            if foot_x is None or abs(foot_x - 96) > 2 or abs(foot_y - 195) > 2:
                frame["errors"].append("Foot anchor outside (96,195) ±2 registration check.")
        if len({frame["pixel_sha256"] for frame in frames}) != len(angles):
            errors.append("Duplicate output pixels within a generation batch.")
        result["registration"] = registration
    result["structure"] = "STRUCTURE_PASS" if frames and not errors and not any(f["errors"] for f in frames) else "FAILED"
    save_json(base / "batches" / f"{batch}.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--form", required=True, choices=FORMS)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--angles", required=True, nargs="+", choices=ANGLES)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.batch):
        parser.error("Batch must use lowercase ASCII letters, digits and hyphens.")
    if len(args.angles) != len(set(args.angles)):
        parser.error("Angles must be unique.")
    result = register_batch(args.root.resolve(), args.form, args.batch, args.angles)
    print(json.dumps({
        "batch": args.batch, "structure": result["structure"], "errors": result["errors"],
        "frames": [{"angle": f["id"], "height": f["solid_height"], "foot": f["foot_anchor_measured"],
                    "errors": f["errors"]} for f in result.get("registration", {}).get("frames", [])],
    }, ensure_ascii=False, indent=2))
    return int(result["structure"] != "STRUCTURE_PASS")


if __name__ == "__main__":
    raise SystemExit(main())
