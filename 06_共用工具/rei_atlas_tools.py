#!/usr/bin/env python3
"""
Rei Desktop Pet — Clean-Room Cross-Platform Atlas & QA Toolkit.

100% independently authored for Linux / macOS / Windows cloud and local execution.
Contains zero proprietary code from external packages; implements the public
Rei Desktop Pet / Codex Pets v1-v2 grid geometry and QA specification documented in:
  - 09_项目文档/CODEX_PETS_COMPATIBILITY.md
  - 09_项目文档/REI_P4_ACTION_SPEC.md
  - 07_QA验收/REI_P4B_ASSET_MANIFEST.json

Subcommands:
  verify            Verify frozen masters, P3/P3-FIX masters, 171 frames, and 3 standard atlases.
  validate-atlas    Validate a standard (1536x1872) or extended v2 (1536x2288) RGBA atlas.
  reassemble        Independently reassemble all 3 standard 1536x1872 atlases from 171 frames
                    and compare pixel-for-pixel against committed delivery atlases.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

CELL_W = 192
CELL_H = 208
COLS = 8
STD_ROWS = 9
EXT_ROWS = 11
STD_SIZE = (COLS * CELL_W, STD_ROWS * CELL_H)  # (1536, 1872)
EXT_SIZE = (COLS * CELL_W, EXT_ROWS * CELL_H)  # (1536, 2288)
EXT_NEUTRAL_CELL = (0, 6)

ROW_SPECS: list[tuple[str, int, int]] = [
    ("idle", 0, 6),
    ("running-right", 1, 8),
    ("running-left", 2, 8),
    ("waving", 3, 4),
    ("jumping", 4, 5),
    ("failed", 5, 8),
    ("waiting", 6, 6),
    ("running", 7, 6),
    ("review", 8, 6),
]

ROW_DURATIONS: dict[str, list[int]] = {
    "idle": [280, 110, 110, 140, 140, 320],
    "running-right": [120] * 7 + [220],
    "running-left": [120] * 7 + [220],
    "waving": [140] * 3 + [280],
    "jumping": [140] * 4 + [280],
    "failed": [140] * 7 + [240],
    "waiting": [150] * 5 + [260],
    "running": [120] * 5 + [220],
    "review": [150] * 5 + [280],
}

FORMS: dict[str, str] = {
    "rei-school": "03_校服绫波丽",
    "rei-white": "04_白色战斗服",
    "rei-black": "05_黑色战斗服",
}

EIGHT_CONN = np.ones((3, 3), dtype=np.uint8)


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def load_font(size: int = 15) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "C:/Windows/Fonts/consola.ttf",
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def clear_transparent_rgb(im: Image.Image) -> Image.Image:
    rgba = im.convert("RGBA")
    arr = np.array(rgba, copy=True)
    arr[arr[:, :, 3] == 0, :3] = 0
    return Image.fromarray(arr, mode="RGBA")


def check_frame_array(arr: np.ndarray, label: str) -> list[str]:
    errors: list[str] = []
    if arr.shape != (CELL_H, CELL_W, 4):
        errors.append(f"{label}: expected shape {(CELL_H, CELL_W, 4)}, got {arr.shape}")
        return errors
    alpha = arr[:, :, 3]
    if np.any(alpha[[0, -1], :]) or np.any(alpha[:, [0, -1]]):
        errors.append(f"{label}: non-transparent pixel on cell border")
    if np.any(arr[alpha == 0, :3]):
        errors.append(f"{label}: non-zero RGB hidden in transparent pixels")
    solid = alpha >= 128
    solid_count = int(np.sum(solid))
    if solid_count < 100:
        errors.append(f"{label}: foreground too sparse ({solid_count} solid pixels)")
    else:
        n_comp = int(ndimage.label(solid, structure=EIGHT_CONN)[1])
        if n_comp != 1:
            errors.append(f"{label}: expected 1 opaque connected component, got {n_comp}")
    return errors


def validate_atlas_image(path: Path, require_v2: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    with Image.open(path) as raw:
        size = raw.size
        mode = raw.mode
        if mode != "RGBA":
            errors.append(f"Expected RGBA mode, got {mode}")
        is_ext = size == EXT_SIZE
        is_std = size == STD_SIZE
        if require_v2 and not is_ext:
            errors.append(f"Expected extended v2 size {EXT_SIZE}, got {size}")
        elif not is_std and not is_ext:
            errors.append(f"Expected {STD_SIZE} or {EXT_SIZE}, got {size}")
        if errors:
            return {"ok": False, "path": str(path), "size": list(size), "mode": mode, "errors": errors, "warnings": warnings}

        arr = np.asarray(raw)
        rows = EXT_ROWS if is_ext else STD_ROWS
        active_cells = 0
        blank_cells = 0

        for r in range(rows):
            if r < STD_ROWS:
                state_name, _, expected_n = ROW_SPECS[r]
            else:
                state_name, expected_n = f"look-row-{r}", 8
            row_hashes: set[bytes] = set()
            for c in range(COLS):
                y0, y1 = r * CELL_H, (r + 1) * CELL_H
                x0, x1 = c * CELL_W, (c + 1) * CELL_W
                cell = arr[y0:y1, x0:x1]
                is_used = c < expected_n or (is_ext and (r, c) == EXT_NEUTRAL_CELL)
                if is_used:
                    active_cells += 1
                    cell_errs = check_frame_array(cell, f"{state_name} ({r},{c})")
                    errors.extend(cell_errs)
                    if c < expected_n:
                        digest = hashlib.sha256(cell.tobytes()).digest()
                        if digest in row_hashes:
                            errors.append(f"{state_name} ({r},{c}): duplicate frame pixels in row")
                        row_hashes.add(digest)
                else:
                    blank_cells += 1
                    if np.any(cell):
                        errors.append(f"{state_name} ({r},{c}): unused cell is not completely transparent/zero")

    return {
        "ok": len(errors) == 0,
        "path": str(path),
        "sha256": sha256_file(path),
        "size": list(size),
        "mode": mode,
        "variant": "extended-v2" if is_ext else "standard-v1",
        "active_cells": active_cells,
        "blank_cells": blank_cells,
        "errors": errors,
        "warnings": warnings,
    }


def cmd_verify(root: Path) -> int:
    freeze = json.loads((root / "00_原始美术母版/REI_ART_FREEZE_MANIFEST.json").read_text(encoding="utf-8"))
    gate = json.loads((root / "07_QA验收/P4-B/gate.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "07_QA验收/REI_P4B_ASSET_MANIFEST.json").read_text(encoding="utf-8"))

    errors: list[str] = []

    # 1. Frozen masters & backups
    for asset in freeze["assets"]:
        orig = root / "00_原始美术母版" / asset["filename"]
        backup = root / asset["backup_path"]
        if not orig.exists() or sha256_file(orig) != asset["sha256"]:
            errors.append(f"Frozen master hash mismatch: {orig}")
        if not backup.exists() or sha256_file(backup) != asset["backup_sha256"]:
            errors.append(f"Frozen backup hash mismatch: {backup}")

    # 2. Derived P3 / P3-FIX masters
    for inp in gate["inputs"]:
        mp = root / inp["master_path"]
        if not mp.exists() or sha256_file(mp) != inp["master_sha256"]:
            errors.append(f"Derived master hash mismatch: {mp}")

    # 3. All 171 frames
    frame_count = 0
    for row in manifest["registered_rows"]:
        for fr in row["frames"]:
            fp = root / fr["path"]
            if not fp.exists() or sha256_file(fp) != fr["sha256"]:
                errors.append(f"Frame hash mismatch: {fr['path']}")
                continue
            with Image.open(fp) as im:
                errors.extend(check_frame_array(np.asarray(im), fr["path"]))
            frame_count += 1

    # 4. All 3 standard atlases
    atlas_reports = []
    for atlas in manifest["atlases"]:
        ap = root / atlas["atlas"]["path"]
        if not ap.exists() or sha256_file(ap) != atlas["atlas"]["sha256"]:
            errors.append(f"Atlas hash mismatch: {atlas['atlas']['path']}")
            continue
        rep = validate_atlas_image(ap, require_v2=False)
        atlas_reports.append(rep)
        if not rep["ok"]:
            errors.extend(rep["errors"])

    result = {
        "ok": len(errors) == 0 and frame_count == 171 and len(atlas_reports) == 3,
        "root": str(root),
        "verified_frames": frame_count,
        "verified_atlases": len(atlas_reports),
        "atlases": [
            {
                "path": r["path"],
                "sha256": r["sha256"],
                "ok": r["ok"],
                "active_cells": r["active_cells"],
                "blank_cells": r["blank_cells"],
            }
            for r in atlas_reports
        ],
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def cmd_reassemble(root: Path, out_dir: Path, write_sheets: bool) -> int:
    manifest = json.loads((root / "07_QA验收/REI_P4B_ASSET_MANIFEST.json").read_text(encoding="utf-8"))
    rows_by_key = {(r["id"], r["state"]): r for r in manifest["registered_rows"]}
    expected_atlas = {a["id"]: a["atlas"] for a in manifest["atlases"]}

    out_dir.mkdir(parents=True, exist_ok=True)
    font = load_font(15)
    summary = []
    all_ok = True

    for pid in FORMS:
        canvas = Image.new("RGBA", STD_SIZE, (0, 0, 0, 0))
        row_imgs: dict[str, list[Image.Image]] = {}
        for state, row_idx, expected_n in ROW_SPECS:
            row = rows_by_key[(pid, state)]
            frames = []
            for col_idx, fr in enumerate(row["frames"]):
                with Image.open(root / fr["path"]) as im:
                    frame = clear_transparent_rgb(im)
                    assert frame.size == (CELL_W, CELL_H)
                    canvas.paste(frame, (col_idx * CELL_W, row_idx * CELL_H))
                    frames.append(frame)
            assert len(frames) == expected_n
            row_imgs[state] = frames

        canvas = clear_transparent_rgb(canvas)
        out_atlas = out_dir / f"{pid}-spritesheet-standard.png"
        canvas.save(out_atlas, format="PNG")
        val = validate_atlas_image(out_atlas, require_v2=False)

        ref_path = root / expected_atlas[pid]["path"]
        with Image.open(ref_path) as ref_im:
            pixel_identical = np.array_equal(np.asarray(canvas), np.asarray(ref_im))
        sha_actual = sha256_file(out_atlas)
        sha_expected = expected_atlas[pid]["sha256"]

        if write_sheets:
            board = Image.new("RGB", (1572, 236 * 9 + 6), "#e5edf9")
            draw = ImageDraw.Draw(board)
            for state, row_idx, expected_n in ROW_SPECS:
                y = row_idx * 236 + 3
                draw.text((9, y), f"{row_idx}  {state}  |  {expected_n} frames", font=font, fill="#142845")
                for col_idx, im in enumerate(row_imgs[state]):
                    cell = Image.new("RGBA", (CELL_W, CELL_H), "#f0f3f9")
                    cell.alpha_composite(im)
                    board.paste(cell.convert("RGB"), (6 + 196 * col_idx, y + 20))
            board.save(out_dir / f"{pid}-standard-contact-sheet.png", format="PNG")

        item_ok = val["ok"] and pixel_identical
        all_ok = all_ok and item_ok
        summary.append({
            "id": pid,
            "out_atlas": str(out_atlas),
            "validation_ok": val["ok"],
            "pixel_identical_to_committed": pixel_identical,
            "sha256_actual": sha_actual,
            "sha256_committed": sha_expected,
            "sha256_identical": sha_actual == sha_expected,
            "active_cells": val["active_cells"],
            "blank_cells": val["blank_cells"],
            "errors": val["errors"],
        })

    print(json.dumps({"ok": all_ok, "reassembled": summary}, ensure_ascii=False, indent=2))
    return 0 if all_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Rei Desktop Pet cross-platform atlas & QA toolkit")
    parser.add_argument("--root", type=Path, default=default_root(), help="Path to repository root")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("verify", help="Verify masters, 171 frames, and 3 standard atlases")

    p_val = sub.add_parser("validate-atlas", help="Validate a single standard or v2 atlas image")
    p_val.add_argument("atlas", type=Path)
    p_val.add_argument("--require-v2", action="store_true")

    p_rea = sub.add_parser("reassemble", help="Reassemble 3 standard atlases from 171 frames into --out-dir")
    p_rea.add_argument("--out-dir", type=Path, required=True)
    p_rea.add_argument("--write-sheets", action="store_true")

    args = parser.parse_args()
    root = args.root.resolve()

    if args.cmd == "verify":
        return cmd_verify(root)
    if args.cmd == "validate-atlas":
        rep = validate_atlas_image(args.atlas.resolve(), require_v2=args.require_v2)
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0 if rep["ok"] else 1
    if args.cmd == "reassemble":
        return cmd_reassemble(root, args.out_dir.resolve(), args.write_sheets)
    return 2


if __name__ == "__main__":
    sys.exit(main())
