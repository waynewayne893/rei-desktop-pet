#!/usr/bin/env python3
"""
Rei Desktop Pet — Unified Zero-Extra-Dependency Cross-Platform Atlas & QA Toolkit.

Uses ONLY Python 3.11+ standard library + Pillow (with libwebp) as the canonical
cloud & local image-processing core (no NumPy/SciPy required; works in restricted
offline-PyPI cloud sandboxes). Windows native OpenAI.Codex `validate_atlas.py --require-v2`
remains the final platform gate for local Windows desktop pet delivery.

Contains zero proprietary code from external packages; implements the public
Rei Desktop Pet / Codex Pets v1-v2 grid geometry and QA specification documented in:
  - 09_项目文档/CODEX_PETS_COMPATIBILITY.md
  - 09_项目文档/REI_P4_ACTION_SPEC.md
  - 07_QA验收/REI_P4B_ASSET_MANIFEST.json

Subcommands:
  verify            Verify frozen masters, P2 backups, derived masters, 171 frames,
                    and 3 committed standard atlases (pixel + hash + structure).
  validate-atlas    Validate any standard (1536x1872) or extended v2 (1536x2288)
                    PNG/WebP RGBA atlas (--require-v2 supported).
  reassemble        Independently reassemble all 3 standard 1536x1872 PNG atlases from
                    171 frames, compare pixels & SHA-256, and inspect PNG encoder diffs.
  build-compat      Build the temporary P4-COMPAT v2 test package (`rei-compat-test`)
                    from existing rei-school 57 frames + 16 directional test cells +
                    (0,6) neutral cell + 14 transparent blanks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import struct
import sys
import zipfile
import zlib
from collections import deque
from pathlib import Path
from typing import Any

import PIL
from PIL import Image, ImageDraw, ImageFont, features

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

LOOK_DIRECTIONS: list[dict[str, Any]] = [
    {"row": 9, "col": 0, "deg": 0.0, "deg_label": "000°", "compass": "N", "cn": "UP"},
    {"row": 9, "col": 1, "deg": 22.5, "deg_label": "022.5°", "compass": "NNE", "cn": "UP-R"},
    {"row": 9, "col": 2, "deg": 45.0, "deg_label": "045°", "compass": "NE", "cn": "UP-R"},
    {"row": 9, "col": 3, "deg": 67.5, "deg_label": "067.5°", "compass": "ENE", "cn": "R-UP"},
    {"row": 9, "col": 4, "deg": 90.0, "deg_label": "090°", "compass": "E", "cn": "RIGHT"},
    {"row": 9, "col": 5, "deg": 112.5, "deg_label": "112.5°", "compass": "ESE", "cn": "R-DN"},
    {"row": 9, "col": 6, "deg": 135.0, "deg_label": "135°", "compass": "SE", "cn": "DN-R"},
    {"row": 9, "col": 7, "deg": 157.5, "deg_label": "157.5°", "compass": "SSE", "cn": "DN-R"},
    {"row": 10, "col": 0, "deg": 180.0, "deg_label": "180°", "compass": "S", "cn": "DOWN"},
    {"row": 10, "col": 1, "deg": 202.5, "deg_label": "202.5°", "compass": "SSW", "cn": "DN-L"},
    {"row": 10, "col": 2, "deg": 225.0, "deg_label": "225°", "compass": "SW", "cn": "DN-L"},
    {"row": 10, "col": 3, "deg": 247.5, "deg_label": "247.5°", "compass": "WSW", "cn": "L-DN"},
    {"row": 10, "col": 4, "deg": 270.0, "deg_label": "270°", "compass": "W", "cn": "LEFT"},
    {"row": 10, "col": 5, "deg": 292.5, "deg_label": "292.5°", "compass": "WNW", "cn": "L-UP"},
    {"row": 10, "col": 6, "deg": 315.0, "deg_label": "315°", "compass": "NW", "cn": "UP-L"},
    {"row": 10, "col": 7, "deg": 337.5, "deg_label": "337.5°", "compass": "NNW", "cn": "UP-L"},
]

ZERO_CELL_BYTES = b"\x00" * (CELL_W * CELL_H * 4)


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_font(size: int = 15, bold: bool = False) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "C:/Windows/Fonts/consolab.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "C:/Windows/Fonts/consola.ttf",
        ]
    )
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
    raw = bytearray(rgba.tobytes())
    for i in range(0, len(raw), 4):
        if raw[i + 3] == 0:
            raw[i] = 0
            raw[i + 1] = 0
            raw[i + 2] = 0
    return Image.frombytes("RGBA", rgba.size, bytes(raw))


def count_transparent_rgb_residue(raw: bytes) -> int:
    residue = 0
    for i in range(0, len(raw), 4):
        if raw[i + 3] == 0 and (raw[i] or raw[i + 1] or raw[i + 2]):
            residue += 1
    return residue


def count_8_connected(mask: bytearray, width: int, height: int) -> int:
    visited = bytearray(len(mask))
    components = 0
    total = width * height
    for idx in range(total):
        if mask[idx] and not visited[idx]:
            components += 1
            visited[idx] = 1
            q: deque[int] = deque([idx])
            while q:
                cur = q.popleft()
                cy, cx = divmod(cur, width)
                y0 = cy - 1 if cy > 0 else 0
                y1 = cy + 1 if cy + 1 < height else height - 1
                x0 = cx - 1 if cx > 0 else 0
                x1 = cx + 1 if cx + 1 < width else width - 1
                for ny in range(y0, y1 + 1):
                    row_off = ny * width
                    for nx in range(x0, x1 + 1):
                        nidx = row_off + nx
                        if mask[nidx] and not visited[nidx]:
                            visited[nidx] = 1
                            q.append(nidx)
    return components


def analyze_cell(im: Image.Image, label: str) -> dict[str, Any]:
    errors: list[str] = []
    if im.mode != "RGBA" or im.size != (CELL_W, CELL_H):
        errors.append(f"{label}: expected RGBA {(CELL_W, CELL_H)}, got {im.mode} {im.size}")
        return {"errors": errors}

    raw = im.tobytes()
    border_non_transparent = 0
    hidden_rgb = 0
    nontransparent = 0
    solid_count = 0
    solid_mask = bytearray(CELL_W * CELL_H)
    alpha_mask = bytearray(CELL_W * CELL_H)
    min_x, min_y = CELL_W, CELL_H
    max_x, max_y = -1, -1

    for y in range(CELL_H):
        row_off = y * CELL_W
        is_y_border = y == 0 or y == CELL_H - 1
        for x in range(CELL_W):
            pidx = row_off + x
            off = pidx * 4
            r, g, b, a = raw[off], raw[off + 1], raw[off + 2], raw[off + 3]
            if a == 0:
                if r or g or b:
                    hidden_rgb += 1
            else:
                nontransparent += 1
                alpha_mask[pidx] = 1
                if is_y_border or x == 0 or x == CELL_W - 1:
                    border_non_transparent += 1
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
                if a >= 128:
                    solid_count += 1
                    solid_mask[pidx] = 1

    if border_non_transparent > 0:
        errors.append(f"{label}: non-transparent pixel on cell border ({border_non_transparent} px)")
    if hidden_rgb > 0:
        errors.append(f"{label}: non-zero RGB hidden in transparent pixels ({hidden_rgb} px)")

    solid_components = 0
    alpha_components = 0
    if solid_count < 100:
        errors.append(f"{label}: foreground too sparse ({solid_count} solid pixels)")
    else:
        solid_components = count_8_connected(solid_mask, CELL_W, CELL_H)
        alpha_components = count_8_connected(alpha_mask, CELL_W, CELL_H)
        if solid_components != 1:
            errors.append(f"{label}: expected 1 opaque connected component, got {solid_components}")

    bbox = [min_x, min_y, max_x + 1, max_y + 1] if max_x >= 0 else None
    margins = (
        {
            "left": min_x,
            "top": min_y,
            "right": CELL_W - 1 - max_x,
            "bottom": CELL_H - 1 - max_y,
        }
        if max_x >= 0
        else None
    )
    return {
        "nontransparent_pixels": nontransparent,
        "solid_pixels": solid_count,
        "solid_components": solid_components,
        "alpha_components": alpha_components,
        "hidden_rgb_pixels": hidden_rgb,
        "border_non_transparent_pixels": border_non_transparent,
        "alpha_bbox": bbox,
        "margins": margins,
        "pixel_sha256": sha256_bytes(raw),
        "errors": errors,
    }


def validate_atlas_image(path: Path, require_v2: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    with Image.open(path) as raw_im:
        fmt = raw_im.format
        size = raw_im.size
        mode = raw_im.mode
        n_frames = getattr(raw_im, "n_frames", 1)
        if n_frames != 1:
            errors.append(f"Expected single-frame image, got {n_frames} frames")
        if mode != "RGBA":
            errors.append(f"Expected RGBA mode, got {mode}")
        is_ext = size == EXT_SIZE
        is_std = size == STD_SIZE
        if require_v2 and not is_ext:
            errors.append(f"Expected extended v2 size {EXT_SIZE}, got {size}")
        elif not is_std and not is_ext:
            errors.append(f"Expected {STD_SIZE} or {EXT_SIZE}, got {size}")
        if errors:
            return {
                "ok": False,
                "path": str(path),
                "format": fmt,
                "size": list(size),
                "mode": mode,
                "n_frames": n_frames,
                "errors": errors,
                "warnings": warnings,
            }

        raw_im.load()
        full_bytes = raw_im.tobytes()
        residue = count_transparent_rgb_residue(full_bytes)
        if residue > 0:
            errors.append(f"Image has {residue} transparent pixels with non-zero RGB residue")

        rows = EXT_ROWS if is_ext else STD_ROWS
        active_cells = 0
        blank_cells = 0
        cell_reports: list[dict[str, Any]] = []

        for r in range(rows):
            if r < STD_ROWS:
                state_name, _, expected_n = ROW_SPECS[r]
            else:
                state_name, expected_n = f"look-row-{r}", 8
            row_hashes: set[str] = set()
            for c in range(COLS):
                x0, y0 = c * CELL_W, r * CELL_H
                cell_im = raw_im.crop((x0, y0, x0 + CELL_W, y0 + CELL_H))
                is_neutral = is_ext and (r, c) == EXT_NEUTRAL_CELL
                is_used = c < expected_n or is_neutral
                if is_used:
                    active_cells += 1
                    stats = analyze_cell(cell_im, f"{state_name} ({r},{c})")
                    errors.extend(stats["errors"])
                    digest = stats["pixel_sha256"]
                    if not is_neutral:
                        if digest in row_hashes:
                            errors.append(f"{state_name} ({r},{c}): duplicate frame pixels in row")
                        row_hashes.add(digest)
                    cell_reports.append(
                        {
                            "state": state_name,
                            "row": r,
                            "column": c,
                            "used": True,
                            "is_neutral_cell": is_neutral,
                            "nontransparent_pixels": stats["nontransparent_pixels"],
                            "solid_pixels": stats["solid_pixels"],
                            "solid_components": stats["solid_components"],
                            "alpha_components": stats["alpha_components"],
                            "margins": stats["margins"],
                            "pixel_sha256": digest,
                        }
                    )
                else:
                    blank_cells += 1
                    cell_bytes = cell_im.tobytes()
                    if cell_bytes != ZERO_CELL_BYTES:
                        errors.append(f"{state_name} ({r},{c}): unused cell is not completely transparent/zero")
                    cell_reports.append(
                        {
                            "state": state_name,
                            "row": r,
                            "column": c,
                            "used": False,
                            "nontransparent_pixels": 0,
                        }
                    )

    return {
        "ok": len(errors) == 0,
        "path": str(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "format": fmt,
        "size": list(size),
        "mode": mode,
        "n_frames": n_frames,
        "sprite_version_number": 2 if is_ext else 1,
        "variant": "extended-v2" if is_ext else "standard-v1",
        "transparent_rgb_residue_pixels": residue,
        "active_cells": active_cells,
        "blank_cells": blank_cells,
        "errors": errors,
        "warnings": warnings,
        "cells": cell_reports,
    }


def inspect_png_chunks(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8
    chunks: list[dict[str, Any]] = []
    idat_stream = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        ctype = data[pos + 4 : pos + 8].decode("ascii", errors="replace")
        payload = data[pos + 8 : pos + 8 + length]
        if ctype == "IDAT":
            idat_stream.extend(payload)
        chunks.append({"type": ctype, "length": length})
        pos += 12 + length
    zlib_cmf = idat_stream[0] if len(idat_stream) >= 2 else None
    zlib_flg = idat_stream[1] if len(idat_stream) >= 2 else None
    zlib_flevel = ((zlib_flg >> 6) & 0x3) if zlib_flg is not None else None
    return {
        "bytes": len(data),
        "chunk_count": len(chunks),
        "chunk_types": [c["type"] for c in chunks],
        "idat_total_bytes": len(idat_stream),
        "idat_chunks": sum(1 for c in chunks if c["type"] == "IDAT"),
        "zlib_cmf_hex": f"0x{zlib_cmf:02x}" if zlib_cmf is not None else None,
        "zlib_flg_hex": f"0x{zlib_flg:02x}" if zlib_flg is not None else None,
        "zlib_flevel": zlib_flevel,
    }


def cmd_verify(root: Path) -> int:
    freeze = json.loads((root / "00_原始美术母版/REI_ART_FREEZE_MANIFEST.json").read_text(encoding="utf-8"))
    gate = json.loads((root / "07_QA验收/P4-B/gate.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "07_QA验收/REI_P4B_ASSET_MANIFEST.json").read_text(encoding="utf-8"))

    errors: list[str] = []
    frozen_checked = 0
    derived_checked = 0

    for asset in freeze["assets"]:
        orig = root / "00_原始美术母版" / asset["filename"]
        backup = root / asset["backup_path"]
        if not orig.exists() or sha256_file(orig) != asset["sha256"]:
            errors.append(f"Frozen master hash mismatch: {orig}")
        else:
            frozen_checked += 1
        if not backup.exists() or sha256_file(backup) != asset["backup_sha256"]:
            errors.append(f"Frozen backup hash mismatch: {backup}")
        else:
            frozen_checked += 1

    for inp in gate["inputs"]:
        mp = root / inp["master_path"]
        if not mp.exists() or sha256_file(mp) != inp["master_sha256"]:
            errors.append(f"Derived master hash mismatch: {mp}")
        else:
            derived_checked += 1

    frame_count = 0
    for row in manifest["registered_rows"]:
        for fr in row["frames"]:
            fp = root / fr["path"]
            if not fp.exists() or sha256_file(fp) != fr["sha256"]:
                errors.append(f"Frame hash mismatch: {fr['path']}")
                continue
            with Image.open(fp) as im:
                im.load()
                stats = analyze_cell(im, fr["path"])
                errors.extend(stats["errors"])
            frame_count += 1

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
        "ok": len(errors) == 0 and frozen_checked == 6 and derived_checked == 3 and frame_count == 171 and len(atlas_reports) == 3,
        "engine": "unified-stdlib-pillow",
        "python": platform.python_version(),
        "pillow": PIL.__version__,
        "libwebp": features.version("webp"),
        "zlib": zlib.ZLIB_VERSION,
        "root": str(root),
        "verified_frozen_and_backups": frozen_checked,
        "verified_derived_masters": derived_checked,
        "verified_frames": frame_count,
        "verified_atlases": len(atlas_reports),
        "atlases": [
            {
                "path": r["path"],
                "sha256": r["sha256"],
                "ok": r["ok"],
                "active_cells": r["active_cells"],
                "blank_cells": r["blank_cells"],
                "transparent_rgb_residue_pixels": r["transparent_rgb_residue_pixels"],
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
            ref_im.load()
            ref_bytes = ref_im.tobytes()
            canvas_bytes = canvas.tobytes()
            pixel_identical = canvas_bytes == ref_bytes
            pixel_sha256 = sha256_bytes(canvas_bytes)
            ref_pixel_sha256 = sha256_bytes(ref_bytes)

        sha_actual = sha256_file(out_atlas)
        sha_expected = expected_atlas[pid]["sha256"]
        sha_identical = sha_actual == sha_expected

        encoder_diff = None
        if pixel_identical and not sha_identical:
            encoder_diff = {
                "actual_png": inspect_png_chunks(out_atlas),
                "committed_png": inspect_png_chunks(ref_path),
            }

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
        summary.append(
            {
                "id": pid,
                "out_atlas": str(out_atlas),
                "validation_ok": val["ok"],
                "pixel_identical_to_committed": pixel_identical,
                "raw_rgba_pixel_sha256": pixel_sha256,
                "committed_raw_rgba_pixel_sha256": ref_pixel_sha256,
                "sha256_actual": sha_actual,
                "sha256_committed": sha_expected,
                "sha256_identical": sha_identical,
                "actual_bytes": out_atlas.stat().st_size,
                "committed_bytes": ref_path.stat().st_size,
                "encoder_diff_analysis": encoder_diff,
                "active_cells": val["active_cells"],
                "blank_cells": val["blank_cells"],
                "errors": val["errors"],
            }
        )

    print(
        json.dumps(
            {
                "ok": all_ok,
                "engine": "unified-stdlib-pillow",
                "python": platform.python_version(),
                "pillow": PIL.__version__,
                "libwebp": features.version("webp"),
                "zlib": zlib.ZLIB_VERSION,
                "reassembled": summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_ok else 1


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    text: str,
    font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=font, fill=fill)


def make_directional_test_cell(spec: dict[str, Any]) -> Image.Image:
    im = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    cx, cy = CELL_W / 2.0, CELL_H / 2.0
    rad = math.radians(spec["deg"])
    dx = math.sin(rad)
    dy = -math.cos(rad)
    px = -dy
    py = dx

    ring_r = 49.0
    tip_r = 80.0
    base_r = 42.0
    half_base = 17.0

    tip = (cx + dx * tip_r, cy + dy * tip_r)
    base_l = (cx + dx * base_r + px * half_base, cy + dy * base_r + py * half_base)
    base_r_pt = (cx + dx * base_r - px * half_base, cy + dy * base_r - py * half_base)

    outer_tip = (cx + dx * (tip_r + 4.5), cy + dy * (tip_r + 4.5))
    outer_l = (cx + dx * (base_r - 2.0) + px * (half_base + 4.5), cy + dy * (base_r - 2.0) + py * (half_base + 4.5))
    outer_r = (cx + dx * (base_r - 2.0) - px * (half_base + 4.5), cy + dy * (base_r - 2.0) - py * (half_base + 4.5))
    draw.polygon([outer_tip, outer_l, outer_r], fill=(235, 246, 255, 255))
    draw.ellipse(
        [cx - (ring_r + 4), cy - (ring_r + 4), cx + (ring_r + 4), cy + (ring_r + 4)],
        fill=(235, 246, 255, 255),
    )

    draw.polygon([tip, base_l, base_r_pt], fill=(232, 56, 68, 255))
    tick_start = (cx + dx * (ring_r + 1.0), cy + dy * (ring_r + 1.0))
    tick_end = (cx + dx * (tip_r - 8.0), cy + dy * (tip_r - 8.0))
    draw.line([tick_start, tick_end], fill=(255, 232, 160, 255), width=4)

    draw.ellipse(
        [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
        fill=(20, 34, 58, 255),
        outline=(98, 178, 245, 255),
        width=3,
    )

    font_tag = load_font(10, bold=True)
    font_deg = load_font(17, bold=True)
    font_dir = load_font(15, bold=True)
    font_cell = load_font(10, bold=False)

    draw_centered_text(draw, cx, cy - 28, "TEST DIR", font_tag, (145, 208, 255, 255))
    draw_centered_text(draw, cx, cy - 8, spec["deg_label"], font_deg, (255, 255, 255, 255))
    draw_centered_text(draw, cx, cy + 13, spec["compass"], font_dir, (255, 204, 102, 255))
    draw_centered_text(
        draw,
        cx,
        cy + 30,
        f"R{spec['row']}C{spec['col']}",
        font_cell,
        (195, 222, 248, 255),
    )

    return clear_transparent_rgb(im)


def make_neutral_reference_cell(idle_frame0: Image.Image) -> Image.Image:
    base = clear_transparent_rgb(idle_frame0).copy()
    draw = ImageDraw.Draw(base)

    raw = base.tobytes()
    foot_max_y = 0
    for y in range(CELL_H):
        for x in range(CELL_W):
            a = raw[(y * CELL_W + x) * 4 + 3]
            if a >= 128 and y >= 170 and y > foot_max_y:
                foot_max_y = y

    y1 = min(CELL_H - 5, foot_max_y + 8)
    y0 = y1 - 18
    x0, x1 = 40, 152
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=7,
        fill=(20, 34, 58, 255),
        outline=(118, 205, 255, 255),
        width=2,
    )
    font = load_font(11, bold=True)
    draw_centered_text(draw, (x0 + x1) / 2.0, (y0 + y1) / 2.0, "NEUTRAL (0,6)", font, (255, 255, 255, 255))
    return clear_transparent_rgb(base)


def render_v2_contact_sheet(atlas: Image.Image, out_path: Path, dark: bool) -> None:
    bg = "#131a26" if dark else "#e5edf9"
    cell_bg = "#1d2638" if dark else "#f0f3f9"
    blank_bg = "#101622" if dark else "#dce4f2"
    text_col = "#d8e6ff" if dark else "#142845"
    sub_col = "#7e95b8" if dark else "#647896"
    font = load_font(15, bold=False)
    font_small = load_font(11, bold=False)

    row_h = 236
    board = Image.new("RGB", (1572, row_h * EXT_ROWS + 6), bg)
    draw = ImageDraw.Draw(board)

    row_titles = [
        "0  idle  |  6 frames + (0,6) neutral ref + 1 blank",
        "1  running-right  |  8 frames",
        "2  running-left  |  8 frames",
        "3  waving  |  4 frames + 4 blanks",
        "4  jumping  |  5 frames + 3 blanks",
        "5  failed  |  8 frames",
        "6  waiting  |  6 frames + 2 blanks",
        "7  running  |  6 frames + 2 blanks",
        "8  review  |  6 frames + 2 blanks",
        "9  TEMP-LOOK-A  |  8 directional test badges (000..157.5 deg) — NOT P4-C ART",
        "10 TEMP-LOOK-B  |  8 directional test badges (180..337.5 deg) — NOT P4-C ART",
    ]

    for r in range(EXT_ROWS):
        y = r * row_h + 3
        draw.text((9, y), row_titles[r], font=font, fill=text_col)
        expected_n = ROW_SPECS[r][2] if r < STD_ROWS else 8
        for c in range(COLS):
            is_used = c < expected_n or (r, c) == EXT_NEUTRAL_CELL
            crop = atlas.crop((c * CELL_W, r * CELL_H, (c + 1) * CELL_W, (r + 1) * CELL_H))
            tile = Image.new("RGBA", (CELL_W, CELL_H), cell_bg if is_used else blank_bg)
            tile.alpha_composite(crop)
            tx, ty = 6 + 196 * c, y + 20
            board.paste(tile.convert("RGB"), (tx, ty))
            if not is_used:
                draw.text((tx + 62, ty + 96), "BLANK", font=font_small, fill=sub_col)

    board.save(out_path, format="PNG")


def cmd_build_compat(root: Path, out_dir: Path) -> int:
    manifest_src = json.loads((root / "07_QA验收/REI_P4B_ASSET_MANIFEST.json").read_text(encoding="utf-8"))
    rows_by_state = {r["state"]: r for r in manifest_src["registered_rows"] if r["id"] == "rei-school"}

    out_dir.mkdir(parents=True, exist_ok=True)
    pkg_dir = out_dir / "rei-compat-test"
    pkg_dir.mkdir(parents=True, exist_ok=True)

    canvas = Image.new("RGBA", EXT_SIZE, (0, 0, 0, 0))
    source_frame_records: list[dict[str, Any]] = []
    source_frame_bytes: dict[tuple[int, int], bytes] = {}
    idle_frame0: Image.Image | None = None

    for state, row_idx, expected_n in ROW_SPECS:
        row = rows_by_state[state]
        assert len(row["frames"]) == expected_n
        for col_idx, fr in enumerate(row["frames"]):
            fp = root / fr["path"]
            actual_sha = sha256_file(fp)
            if actual_sha != fr["sha256"]:
                raise RuntimeError(f"Source frame hash mismatch for {fr['path']}")
            with Image.open(fp) as im:
                frame = clear_transparent_rgb(im)
                assert frame.size == (CELL_W, CELL_H)
                canvas.paste(frame, (col_idx * CELL_W, row_idx * CELL_H))
                source_frame_bytes[(row_idx, col_idx)] = frame.tobytes()
                if row_idx == 0 and col_idx == 0:
                    idle_frame0 = frame.copy()
                source_frame_records.append(
                    {
                        "state": state,
                        "row": row_idx,
                        "col": col_idx,
                        "source_path": fr["path"],
                        "source_sha256": actual_sha,
                    }
                )

    assert idle_frame0 is not None
    assert len(source_frame_records) == 57

    neutral_cell = make_neutral_reference_cell(idle_frame0)
    canvas.paste(neutral_cell, (EXT_NEUTRAL_CELL[1] * CELL_W, EXT_NEUTRAL_CELL[0] * CELL_H))

    directional_records: list[dict[str, Any]] = []
    for spec in LOOK_DIRECTIONS:
        cell_im = make_directional_test_cell(spec)
        canvas.paste(cell_im, (spec["col"] * CELL_W, spec["row"] * CELL_H))
        cell_stats = analyze_cell(cell_im, f"look ({spec['row']},{spec['col']})")
        if cell_stats["errors"]:
            raise RuntimeError(f"Generated directional test cell failed QA: {cell_stats['errors']}")
        directional_records.append(
            {
                "row": spec["row"],
                "col": spec["col"],
                "deg": spec["deg"],
                "deg_label": spec["deg_label"],
                "compass": spec["compass"],
                "pixel_sha256": cell_stats["pixel_sha256"],
                "nontransparent_pixels": cell_stats["nontransparent_pixels"],
                "solid_pixels": cell_stats["solid_pixels"],
                "solid_components": cell_stats["solid_components"],
                "alpha_components": cell_stats["alpha_components"],
                "margins": cell_stats["margins"],
            }
        )

    canvas = clear_transparent_rgb(canvas)

    webp_path = pkg_dir / "spritesheet.webp"
    canvas.save(webp_path, format="WEBP", lossless=True, quality=100, method=6, exact=True)

    pet_meta = {
        "id": "rei-compat-test",
        "displayName": "Rei Compat Test (Temporary)",
        "description": "Temporary P4-COMPAT v2 extended atlas test package using 57 rei-school standard frames, 16 directional test badges, and (0,6) neutral reference cell. Not for formal P4-C/P5 release.",
        "spriteVersionNumber": 2,
        "spritesheetPath": "spritesheet.webp",
    }
    pet_json_path = pkg_dir / "pet.json"
    pet_json_path.write_text(json.dumps(pet_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    webp_val = validate_atlas_image(webp_path, require_v2=True)
    with Image.open(webp_path) as decoded:
        decoded.load()
        decoded_bytes = decoded.tobytes()
        lossless_roundtrip_ok = decoded_bytes == canvas.tobytes()
        standard_frames_pixel_identical = True
        mismatched_frames: list[str] = []
        for (r, c), expected_raw in source_frame_bytes.items():
            crop_bytes = decoded.crop((c * CELL_W, r * CELL_H, (c + 1) * CELL_W, (r + 1) * CELL_H)).tobytes()
            if crop_bytes != expected_raw:
                standard_frames_pixel_identical = False
                mismatched_frames.append(f"({r},{c})")

    parsed_pet_json = json.loads(pet_json_path.read_text(encoding="utf-8"))
    pet_json_checks = {
        "valid_json": True,
        "id_equals_rei_compat_test": parsed_pet_json.get("id") == "rei-compat-test",
        "sprite_version_number_equals_2": parsed_pet_json.get("spriteVersionNumber") == 2,
        "spritesheet_path_equals_spritesheet_webp": parsed_pet_json.get("spritesheetPath") == "spritesheet.webp",
        "referenced_spritesheet_exists": (pkg_dir / parsed_pet_json["spritesheetPath"]).exists(),
        "required_keys_present": all(
            k in parsed_pet_json for k in ("id", "displayName", "description", "spriteVersionNumber", "spritesheetPath")
        ),
        "no_asuka_id_collision": not str(parsed_pet_json.get("id", "")).startswith("asuka"),
    }
    pet_json_ok = all(pet_json_checks.values())

    light_sheet = out_dir / "rei-compat-test-contact-sheet.png"
    dark_sheet = out_dir / "rei-compat-test-contact-sheet-dark.png"
    with Image.open(webp_path) as decoded:
        decoded.load()
        render_v2_contact_sheet(decoded, light_sheet, dark=False)
        render_v2_contact_sheet(decoded, dark_sheet, dark=True)

    zip_path = out_dir / "rei-compat-test.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel_name, src_file in [
            ("rei-compat-test/pet.json", pet_json_path),
            ("rei-compat-test/spritesheet.webp", webp_path),
        ]:
            zi = zipfile.ZipInfo(filename=rel_name, date_time=(2026, 11, 27, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, src_file.read_bytes())

    with zipfile.ZipFile(zip_path, "r") as zf:
        zip_entries = zf.namelist()
        zip_integrity_ok = (
            zf.testzip() is None
            and zf.read("rei-compat-test/pet.json") == pet_json_path.read_bytes()
            and zf.read("rei-compat-test/spritesheet.webp") == webp_path.read_bytes()
        )

    def rel(p: Path) -> str:
        try:
            return p.relative_to(root).as_posix()
        except ValueError:
            return p.as_posix()

    overall_ok = (
        webp_val["ok"]
        and lossless_roundtrip_ok
        and standard_frames_pixel_identical
        and pet_json_ok
        and zip_integrity_ok
        and webp_val["active_cells"] == 74
        and webp_val["blank_cells"] == 14
        and webp_val["transparent_rgb_residue_pixels"] == 0
    )

    compat_manifest = {
        "schema_version": 1,
        "stage": "REI-PET-CLOUD-BOOTSTRAP / P4-COMPAT",
        "purpose": "Temporary Codex Desktop Pets v2 extended atlas compatibility pre-verification package. NOT a formal P4-C/P4-D/P5 release.",
        "temporary_directional_assets_excluded_from_p4c": True,
        "test_pet_id": "rei-compat-test",
        "expected_codex_selector_id": "custom:rei-compat-test",
        "source_form": "rei-school",
        "source_standard_frames_count": 57,
        "neutral_reference_cell": {
            "row": 0,
            "col": 6,
            "base_frame": "03_校服绫波丽/P4-A/selected/idle/frames/00.png",
            "visual_marker": "NEUTRAL (0,6) connected bottom pill",
        },
        "temporary_directional_cells_count": 16,
        "blank_cells_count": 14,
        "total_active_cells": 74,
        "grid": {"columns": COLS, "rows": EXT_ROWS, "cell_width": CELL_W, "cell_height": CELL_H, "width": EXT_SIZE[0], "height": EXT_SIZE[1]},
        "builder": {
            "script": "06_共用工具/rei_atlas_tools.py",
            "python": platform.python_version(),
            "pillow": PIL.__version__,
            "libwebp": features.version("webp"),
            "webp_encoding": {"format": "WEBP", "lossless": True, "quality": 100, "method": 6, "exact": True},
        },
        "deliverables": {
            "pet_json": {"path": rel(pet_json_path), "bytes": pet_json_path.stat().st_size, "sha256": sha256_file(pet_json_path)},
            "spritesheet_webp": {
                "path": rel(webp_path),
                "bytes": webp_path.stat().st_size,
                "sha256": sha256_file(webp_path),
                "decoded_rgba_pixel_sha256": sha256_bytes(decoded_bytes),
            },
            "downloadable_zip": {
                "path": rel(zip_path),
                "bytes": zip_path.stat().st_size,
                "sha256": sha256_file(zip_path),
                "entries": zip_entries,
            },
            "contact_sheet_light": {"path": rel(light_sheet), "bytes": light_sheet.stat().st_size, "sha256": sha256_file(light_sheet)},
            "contact_sheet_dark": {"path": rel(dark_sheet), "bytes": dark_sheet.stat().st_size, "sha256": sha256_file(dark_sheet)},
        },
        "source_frames": source_frame_records,
        "temporary_directional_cells": directional_records,
    }

    offline_qa = {
        "schema_version": 1,
        "stage": "REI-PET-CLOUD-BOOTSTRAP / P4-COMPAT",
        "overall_status": "OFFLINE_COMPAT_PASS" if overall_ok else "OFFLINE_COMPAT_FAIL",
        "ok": overall_ok,
        "not_formal_art_acceptance": True,
        "windows_native_validation_pending": True,
        "webp_checks": {
            "path": rel(webp_path),
            "sha256": webp_val["sha256"],
            "bytes": webp_val["bytes"],
            "format": webp_val["format"],
            "mode": webp_val["mode"],
            "size": webp_val["size"],
            "n_frames": webp_val["n_frames"],
            "sprite_version_number": webp_val["sprite_version_number"],
            "active_cells": webp_val["active_cells"],
            "blank_cells": webp_val["blank_cells"],
            "transparent_rgb_residue_pixels": webp_val["transparent_rgb_residue_pixels"],
            "lossless_roundtrip_pixel_identical": lossless_roundtrip_ok,
            "standard_57_frames_pixel_identical_to_rei_school": standard_frames_pixel_identical,
            "mismatched_standard_frames": mismatched_frames,
            "require_v2_validation_ok": webp_val["ok"],
            "errors": webp_val["errors"],
            "warnings": webp_val["warnings"],
        },
        "pet_json_checks": {
            "path": rel(pet_json_path),
            "sha256": sha256_file(pet_json_path),
            "ok": pet_json_ok,
            "checks": pet_json_checks,
            "content": parsed_pet_json,
        },
        "zip_archive_checks": {
            "path": rel(zip_path),
            "sha256": sha256_file(zip_path),
            "ok": zip_integrity_ok,
            "entries": zip_entries,
        },
        "cell_summary": {
            "total_cells": 88,
            "active_standard_action_cells": 57,
            "active_neutral_reference_cells": 1,
            "active_temp_directional_cells": 16,
            "blank_transparent_cells": 14,
            "all_active_cells_single_solid_component": all(c["solid_components"] == 1 for c in webp_val["cells"] if c["used"]),
            "all_temp_cells_single_alpha_component": all(d["alpha_components"] == 1 for d in directional_records),
        },
        "cells": webp_val["cells"],
    }

    manifest_path = out_dir / "COMPAT_TEST_MANIFEST.json"
    qa_path = out_dir / "COMPAT_OFFLINE_QA.json"
    manifest_path.write_text(json.dumps(compat_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qa_path.write_text(json.dumps(offline_qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": overall_ok,
                "manifest": rel(manifest_path),
                "offline_qa": rel(qa_path),
                "deliverables": compat_manifest["deliverables"],
                "webp_active_cells": webp_val["active_cells"],
                "webp_blank_cells": webp_val["blank_cells"],
                "transparent_rgb_residue_pixels": webp_val["transparent_rgb_residue_pixels"],
                "lossless_roundtrip_pixel_identical": lossless_roundtrip_ok,
                "standard_57_frames_pixel_identical": standard_frames_pixel_identical,
                "pet_json_ok": pet_json_ok,
                "zip_integrity_ok": zip_integrity_ok,
                "errors": webp_val["errors"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if overall_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Rei Desktop Pet unified stdlib+Pillow atlas & QA toolkit")
    parser.add_argument("--root", type=Path, default=default_root(), help="Path to repository root")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("verify", help="Verify frozen masters, derived masters, 171 frames, and 3 standard atlases")

    p_val = sub.add_parser("validate-atlas", help="Validate a single standard or v2 atlas image")
    p_val.add_argument("atlas", type=Path)
    p_val.add_argument("--require-v2", action="store_true")

    p_rea = sub.add_parser("reassemble", help="Reassemble 3 standard atlases from 171 frames into --out-dir")
    p_rea.add_argument("--out-dir", type=Path, required=True)
    p_rea.add_argument("--write-sheets", action="store_true")

    p_compat = sub.add_parser("build-compat", help="Build temporary rei-compat-test v2 compatibility package")
    p_compat.add_argument("--out-dir", type=Path, required=True)

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
    if args.cmd == "build-compat":
        return cmd_build_compat(root, args.out_dir.resolve())
    return 2


if __name__ == "__main__":
    sys.exit(main())
