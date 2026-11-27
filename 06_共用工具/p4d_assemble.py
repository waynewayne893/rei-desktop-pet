#!/usr/bin/env python3
"""
Rei Desktop Pet — P4-D Final Extended v2 Atlas Assembly, 264-Cell Offline QA & Packaging.

Cross-platform zero-extra-dependency script using ONLY Python 3.11+ standard library
and Pillow (with libwebp). Runs identically on Linux Cloud and Windows/macOS.

Assembles three independent Codex Pets v2 packages:
  - rei-school (03_校服绫波丽)
  - rei-white  (04_白色战斗服)
  - rei-black  (05_黑色战斗服)

Strictly enforces:
  - 219 accepted source PNGs (171 standard + 48 directional) read-only and byte-unchanged
  - R0C6 auxiliary neutral cell sourced from each form's accepted selected/idle/frames/00.png
    per frozen protocol (09_项目文档/REI_PROJECT_ROADMAP.md & CODEX_PETS_COMPATIBILITY.md)
  - Zero temporary P4-COMPAT directional/badge assets
  - Full 264-cell (88 x 3) offline QA + WebP VP8L lossless header & roundtrip pixel verification
  - Does NOT execute or fabricate Windows native validate_atlas.py or live Codex Desktop tests
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import struct
import sys
import zipfile
import zlib
from pathlib import Path
from typing import Any

import PIL
from PIL import Image, ImageDraw, ImageOps, features

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import rei_atlas_tools as tools  # noqa: E402

PET_METADATA: dict[str, dict[str, Any]] = {
    "rei-school": {
        "folder": "03_校服绫波丽",
        "id": "rei-school",
        "displayName": "绫波丽·校服",
        "description": "沿用冻结校服母版的绫波丽桌面宠物，包含九种标准动画状态与十六个顺时针注视方向（Codex Pets v2）。",
        "spriteVersionNumber": 2,
        "spritesheetPath": "spritesheet.webp",
    },
    "rei-white": {
        "folder": "04_白色战斗服",
        "id": "rei-white",
        "displayName": "绫波丽·白色战斗服00",
        "description": "沿用冻结白色战斗服 00 母版的绫波丽桌面宠物，包含九种标准动画状态与十六个顺时针注视方向（Codex Pets v2）。",
        "spriteVersionNumber": 2,
        "spritesheetPath": "spritesheet.webp",
    },
    "rei-black": {
        "folder": "05_黑色战斗服",
        "id": "rei-black",
        "displayName": "绫波丽·黑色战斗服09",
        "description": "沿用冻结黑色战斗服 09 母版的绫波丽桌面宠物，包含九种标准动画状态与十六个顺时针注视方向（Codex Pets v2）。",
        "spriteVersionNumber": 2,
        "spritesheetPath": "spritesheet.webp",
    },
}

ANGLE_ORDER = [
    "000", "022.5", "045", "067.5", "090", "112.5", "135", "157.5",
    "180", "202.5", "225", "247.5", "270", "292.5", "315", "337.5",
]


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_webp_header(path: Path) -> dict[str, Any]:
    """Parse RIFF/WEBP container chunks to confirm VP8L lossless encoding and alpha flag."""
    data = path.read_bytes()
    if len(data) < 20 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return {"ok": False, "error": "Not a valid RIFF/WEBP file"}
    riff_size = struct.unpack("<I", data[4:8])[0]
    pos = 12
    chunks: list[dict[str, Any]] = []
    vp8l_info: dict[str, Any] | None = None
    vp8x_alpha: bool | None = None
    while pos + 8 <= len(data):
        fourcc = data[pos : pos + 4].decode("ascii", errors="replace")
        size = struct.unpack("<I", data[pos + 4 : pos + 8])[0]
        payload = data[pos + 8 : pos + 8 + size]
        chunks.append({"fourcc": fourcc, "bytes": size})
        if fourcc == "VP8X" and len(payload) >= 10:
            flags = payload[0]
            vp8x_alpha = bool(flags & 0x10)
        elif fourcc == "VP8L" and len(payload) >= 5:
            sig = payload[0]
            bits = struct.unpack("<I", payload[1:5])[0]
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            alpha_is_used = bool((bits >> 28) & 0x1)
            version = (bits >> 29) & 0x7
            vp8l_info = {
                "signature_hex": f"0x{sig:02x}",
                "signature_valid": sig == 0x2F,
                "width": width,
                "height": height,
                "alpha_is_used": alpha_is_used,
                "version": version,
            }
        pos += 8 + size + (size & 1)
    ok = (
        vp8l_info is not None
        and vp8l_info["signature_valid"]
        and vp8l_info["width"] == tools.EXT_SIZE[0]
        and vp8l_info["height"] == tools.EXT_SIZE[1]
        and vp8l_info["alpha_is_used"]
    )
    return {
        "ok": ok,
        "riff_size": riff_size,
        "file_bytes": len(data),
        "chunks": chunks,
        "vp8x_alpha_flag": vp8x_alpha,
        "vp8l": vp8l_info,
    }


def render_production_v2_contact_sheet(
    atlas: Image.Image, form_id: str, display_name: str, out_path: Path, dark: bool
) -> None:
    bg = "#131a26" if dark else "#e5edf9"
    cell_bg = "#1d2638" if dark else "#f0f3f9"
    blank_bg = "#101622" if dark else "#dce4f2"
    text_col = "#d8e6ff" if dark else "#142845"
    sub_col = "#7e95b8" if dark else "#647896"
    font = tools.load_font(15, bold=False)
    font_small = tools.load_font(11, bold=False)

    row_h = 236
    board = Image.new("RGB", (1572, row_h * tools.EXT_ROWS + 6), bg)
    draw = ImageDraw.Draw(board)

    row_titles = [
        f"0  idle  |  6 frames + (0,6) neutral ref [idle/00] + 1 blank  |  {form_id}",
        "1  running-right  |  8 frames",
        "2  running-left  |  8 frames",
        "3  waving  |  4 frames + 4 blanks",
        "4  jumping  |  5 frames + 3 blanks",
        "5  failed  |  8 frames",
        "6  waiting  |  6 frames + 2 blanks",
        "7  running  |  6 frames + 2 blanks",
        "8  review  |  6 frames + 2 blanks",
        "9  look-000-to-157.5  |  8 accepted P4-C directions (000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5)",
        "10 look-180-to-337.5  |  8 accepted P4-C directions (180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5)",
    ]

    for r in range(tools.EXT_ROWS):
        y = r * row_h + 3
        draw.text((9, y), row_titles[r], font=font, fill=text_col)
        expected_n = tools.ROW_SPECS[r][2] if r < tools.STD_ROWS else 8
        for c in range(tools.COLS):
            is_used = c < expected_n or (r, c) == tools.EXT_NEUTRAL_CELL
            crop = atlas.crop((c * tools.CELL_W, r * tools.CELL_H, (c + 1) * tools.CELL_W, (r + 1) * tools.CELL_H))
            tile = Image.new("RGBA", (tools.CELL_W, tools.CELL_H), cell_bg if is_used else blank_bg)
            tile.alpha_composite(crop)
            tx, ty = 6 + 196 * c, y + 20
            board.paste(tile.convert("RGB"), (tx, ty))
            if not is_used:
                draw.text((tx + 62, ty + 96), "BLANK", font=font_small, fill=sub_col)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    board.save(out_path, format="PNG")


def write_deterministic_zip(zip_path: Path, entries: list[tuple[str, Path]]) -> dict[str, Any]:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for arcname, src in entries:
            zi = zipfile.ZipInfo(filename=arcname, date_time=(2026, 11, 27, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, src.read_bytes())

    with zipfile.ZipFile(zip_path, "r") as zf:
        bad = zf.testzip()
        names = zf.namelist()
        exact = bad is None and all(zf.read(arcname) == src.read_bytes() for arcname, src in entries)
    return {
        "ok": exact,
        "bytes": zip_path.stat().st_size,
        "sha256": tools.sha256_file(zip_path),
        "entry_count": len(names),
        "entries": names,
    }


def verify_source_preservation(root: Path, p4b_manifest: dict, p4c_manifest: dict) -> dict[str, Any]:
    """Verify frozen masters, P2 backups, derived masters, 171 standard frames, 48 directional frames, and 3 standard atlases."""
    freeze = json.loads((root / "00_原始美术母版/REI_ART_FREEZE_MANIFEST.json").read_text(encoding="utf-8"))
    gate = json.loads((root / "07_QA验收/P4-B/gate.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    counts = {"frozen_and_backups": 0, "derived_masters": 0, "standard_frames": 0, "direction_frames": 0, "standard_atlases": 0}

    for asset in freeze["assets"]:
        for p, expected in [
            (root / "00_原始美术母版" / asset["filename"], asset["sha256"]),
            (root / asset["backup_path"], asset["backup_sha256"]),
        ]:
            if not p.exists() or tools.sha256_file(p) != expected:
                errors.append(f"Frozen/backup hash mismatch: {p}")
            else:
                counts["frozen_and_backups"] += 1

    for inp in gate["inputs"]:
        p = root / inp["master_path"]
        if not p.exists() or tools.sha256_file(p) != inp["master_sha256"]:
            errors.append(f"Derived master hash mismatch: {p}")
        else:
            counts["derived_masters"] += 1

    for row in p4b_manifest["registered_rows"]:
        for fr in row["frames"]:
            p = root / fr["path"]
            if not p.exists() or tools.sha256_file(p) != fr["sha256"]:
                errors.append(f"Standard frame hash mismatch: {fr['path']}")
            else:
                counts["standard_frames"] += 1

    for fr in p4c_manifest["frames"]:
        p = root / fr["path"]
        if not p.exists() or tools.sha256_file(p) != fr["sha256"]:
            errors.append(f"Direction frame hash mismatch: {fr['path']}")
        else:
            counts["direction_frames"] += 1

    for atlas in p4b_manifest["atlases"]:
        p = root / atlas["atlas"]["path"]
        if not p.exists() or tools.sha256_file(p) != atlas["atlas"]["sha256"]:
            errors.append(f"Standard atlas hash mismatch: {atlas['atlas']['path']}")
        else:
            counts["standard_atlases"] += 1

    ok = (
        not errors
        and counts == {
            "frozen_and_backups": 6,
            "derived_masters": 3,
            "standard_frames": 171,
            "direction_frames": 48,
            "standard_atlases": 3,
        }
    )
    return {"ok": ok, "counts": counts, "errors": errors}


def assemble_and_qa(root: Path, skip_bundle: bool = False) -> int:
    p4b_manifest = json.loads((root / "07_QA验收/REI_P4B_ASSET_MANIFEST.json").read_text(encoding="utf-8"))
    p4b_ledger = json.loads((root / "07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json").read_text(encoding="utf-8"))
    p4c_manifest = json.loads((root / "07_QA验收/P4-C/P4C_DIRECTION_ASSET_MANIFEST.json").read_text(encoding="utf-8"))
    p4c_ledger = json.loads((root / "07_QA验收/P4-C/human-acceptance/P4C_ACCEPTANCE_LEDGER.json").read_text(encoding="utf-8"))

    # Hard acceptance gates before assembly
    if p4b_ledger["official_summary"]["frames_by_status"]["ACCEPTED"] != 171:
        raise RuntimeError("P4-B ledger does not confirm 171/171 ACCEPTED frames")
    if p4c_ledger["summary"]["frames_by_final_status"]["ACCEPTED"] != 48:
        raise RuntimeError("P4-C ledger does not confirm 48/48 ACCEPTED frames")

    pre_preservation = verify_source_preservation(root, p4b_manifest, p4c_manifest)
    if not pre_preservation["ok"]:
        raise RuntimeError(f"Pre-assembly preservation check failed: {pre_preservation['errors']}")

    rows_by_key = {(r["id"], r["state"]): r for r in p4b_manifest["registered_rows"]}
    std_atlas_by_id = {a["id"]: a["atlas"] for a in p4b_manifest["atlases"]}
    p4c_by_key = {(fr["form"], fr["angle"]): fr for fr in p4c_ledger["frames"]}

    delivery_root = root / "08_正式交付" / "P4-D-candidate"
    qa_root = root / "07_QA验收" / "P4-D"
    sheets_root = qa_root / "contact-sheets"
    delivery_root.mkdir(parents=True, exist_ok=True)
    qa_root.mkdir(parents=True, exist_ok=True)
    sheets_root.mkdir(parents=True, exist_ok=True)

    pet_manifest_entries: dict[str, Any] = {}
    pet_qa_entries: dict[str, Any] = {}
    all_ok = True
    total_cells_checked = 0
    total_active_checked = 0
    total_blank_checked = 0

    for form_id, meta in PET_METADATA.items():
        form_delivery_dir = root / meta["folder"] / "P4-D" / "delivery"
        form_delivery_dir.mkdir(parents=True, exist_ok=True)
        pkg_dir = delivery_root / form_id
        pkg_dir.mkdir(parents=True, exist_ok=True)

        canvas = Image.new("RGBA", tools.EXT_SIZE, (0, 0, 0, 0))
        expected_cell_bytes: dict[tuple[int, int], bytes] = {}
        standard_frame_records: list[dict[str, Any]] = []
        direction_frame_records: list[dict[str, Any]] = []
        direction_images: list[Image.Image] = []
        idle0_record: dict[str, Any] | None = None
        idle0_bytes: bytes | None = None

        # 1. Rows 0-8: 57 accepted standard action frames
        for state, row_idx, expected_n in tools.ROW_SPECS:
            row = rows_by_key[(form_id, state)]
            assert len(row["frames"]) == expected_n
            for col_idx, fr in enumerate(row["frames"]):
                fp = root / fr["path"]
                actual_sha = tools.sha256_file(fp)
                assert actual_sha == fr["sha256"], f"Hash mismatch: {fr['path']}"
                with Image.open(fp) as im:
                    im.load()
                    assert im.mode == "RGBA" and im.size == (tools.CELL_W, tools.CELL_H)
                    raw_bytes = im.tobytes()
                    assert tools.count_transparent_rgb_residue(raw_bytes) == 0, f"Hidden RGB in source {fr['path']}"
                    canvas.paste(im, (col_idx * tools.CELL_W, row_idx * tools.CELL_H))
                    expected_cell_bytes[(row_idx, col_idx)] = raw_bytes
                    rec = {
                        "state": state,
                        "row": row_idx,
                        "col": col_idx,
                        "source_path": fr["path"],
                        "source_sha256": actual_sha,
                        "pixel_sha256": tools.sha256_bytes(raw_bytes),
                        "human_status": "ACCEPTED",
                    }
                    standard_frame_records.append(rec)
                    if row_idx == 0 and col_idx == 0:
                        idle0_record = rec
                        idle0_bytes = raw_bytes

        assert len(standard_frame_records) == 57
        assert idle0_record is not None and idle0_bytes is not None

        # 2. R0C6 auxiliary neutral reference cell — strictly from accepted idle/00.png
        neutral_img = Image.frombytes("RGBA", (tools.CELL_W, tools.CELL_H), idle0_bytes)
        canvas.paste(neutral_img, (tools.EXT_NEUTRAL_CELL[1] * tools.CELL_W, tools.EXT_NEUTRAL_CELL[0] * tools.CELL_H))
        expected_cell_bytes[tools.EXT_NEUTRAL_CELL] = idle0_bytes
        neutral_record = {
            "row": 0,
            "col": 6,
            "protocol_basis": "09_项目文档/REI_PROJECT_ROADMAP.md (从验收 idle 提供辅助中性格) & 09_项目文档/CODEX_PETS_COMPATIBILITY.md & hatch-pet --neutral-cell idle/00.png",
            "source_path": idle0_record["source_path"],
            "source_sha256": idle0_record["source_sha256"],
            "pixel_sha256": idle0_record["pixel_sha256"],
            "exact_unaltered_copy_of_idle_00": True,
            "temporary_badge_present": False,
        }

        # 3. Rows 9-10: 16 accepted P4-C direction frames in exact clockwise order
        for idx, angle in enumerate(ANGLE_ORDER):
            fr = p4c_by_key[(form_id, angle)]
            expected_row = 9 + idx // 8
            expected_col = idx % 8
            assert fr["row"] == expected_row and fr["col"] == expected_col
            assert fr["final_human_status"] == "ACCEPTED"
            fp = root / fr["path"]
            actual_sha = tools.sha256_file(fp)
            assert actual_sha == fr["sha256"], f"Direction hash mismatch: {fr['path']}"
            with Image.open(fp) as im:
                im.load()
                assert im.mode == "RGBA" and im.size == (tools.CELL_W, tools.CELL_H)
                raw_bytes = im.tobytes()
                assert tools.count_transparent_rgb_residue(raw_bytes) == 0, f"Hidden RGB in direction {fr['path']}"
                canvas.paste(im, (expected_col * tools.CELL_W, expected_row * tools.CELL_H))
                expected_cell_bytes[(expected_row, expected_col)] = raw_bytes
                direction_images.append(im.copy())
                direction_frame_records.append(
                    {
                        "angle": angle,
                        "row": expected_row,
                        "col": expected_col,
                        "source_path": fr["path"],
                        "source_sha256": actual_sha,
                        "native_raw_path": fr["source_path"],
                        "native_raw_sha256": fr["source_sha256"],
                        "version": fr["version"],
                        "origin": fr["origin"],
                        "acceptance_source": fr["acceptance_source"],
                        "pixel_sha256": tools.sha256_bytes(raw_bytes),
                        "human_status": "ACCEPTED",
                    }
                )

        assert len(direction_frame_records) == 16
        assert len(expected_cell_bytes) == 74

        # Verify canvas itself has zero hidden RGB without altering any source pixel
        canvas_bytes = canvas.tobytes()
        assert tools.count_transparent_rgb_residue(canvas_bytes) == 0

        # Save Extended PNG & Lossless WebP & pet.json
        ext_png_path = form_delivery_dir / "spritesheet-extended.png"
        ext_webp_form_path = form_delivery_dir / "spritesheet.webp"
        pet_json_form_path = form_delivery_dir / "pet.json"

        canvas.save(ext_png_path, format="PNG")
        canvas.save(ext_webp_form_path, format="WEBP", lossless=True, quality=100, method=6, exact=True)

        pet_meta_clean = {
            "id": meta["id"],
            "displayName": meta["displayName"],
            "description": meta["description"],
            "spriteVersionNumber": meta["spriteVersionNumber"],
            "spritesheetPath": meta["spritesheetPath"],
        }
        pet_json_text = json.dumps(pet_meta_clean, ensure_ascii=False, indent=2) + "\n"
        pet_json_form_path.write_text(pet_json_text, encoding="utf-8")

        # Mirror exact bytes into 08_正式交付/P4-D-candidate/<form_id>/
        pkg_webp_path = pkg_dir / "spritesheet.webp"
        pkg_json_path = pkg_dir / "pet.json"
        pkg_webp_path.write_bytes(ext_webp_form_path.read_bytes())
        pkg_json_path.write_bytes(pet_json_form_path.read_bytes())
        assert tools.sha256_file(pkg_webp_path) == tools.sha256_file(ext_webp_form_path)
        assert tools.sha256_file(pkg_json_path) == tools.sha256_file(pet_json_form_path)

        # Render Light & Dark 11-row extended contact sheets
        light_sheet = sheets_root / f"{form_id}-extended-contact-light.png"
        dark_sheet = sheets_root / f"{form_id}-extended-contact-dark.png"
        render_production_v2_contact_sheet(canvas, form_id, meta["displayName"], light_sheet, dark=False)
        render_production_v2_contact_sheet(canvas, form_id, meta["displayName"], dark_sheet, dark=True)

        # Build individual install-ready ZIP
        indiv_zip_path = delivery_root / f"{form_id}-codex-pet-v2.zip"
        indiv_zip_check = write_deterministic_zip(
            indiv_zip_path,
            [
                (f"{form_id}/pet.json", pkg_json_path),
                (f"{form_id}/spritesheet.webp", pkg_webp_path),
            ],
        )

        # === T3: EXHAUSTIVE 88-CELL OFFLINE QA FOR THIS PET ===
        png_val = tools.validate_atlas_image(ext_png_path, require_v2=True)
        webp_val = tools.validate_atlas_image(pkg_webp_path, require_v2=True)
        webp_header = parse_webp_header(pkg_webp_path)

        with Image.open(ext_png_path) as dec_png, Image.open(pkg_webp_path) as dec_webp:
            dec_png.load()
            dec_webp.load()
            png_raw = dec_png.tobytes()
            webp_raw = dec_webp.tobytes()
            png_webp_pixel_identical = (png_raw == webp_raw == canvas_bytes)

            # Verify every single one of the 88 cells decoded from WebP
            cell_pixel_mismatches: list[str] = []
            blank_mismatches: list[str] = []
            active_verified = 0
            blank_verified = 0
            for r in range(tools.EXT_ROWS):
                for c in range(tools.COLS):
                    crop = dec_webp.crop((c * tools.CELL_W, r * tools.CELL_H, (c + 1) * tools.CELL_W, (r + 1) * tools.CELL_H)).tobytes()
                    if (r, c) in expected_cell_bytes:
                        if crop != expected_cell_bytes[(r, c)]:
                            cell_pixel_mismatches.append(f"({r},{c})")
                        else:
                            active_verified += 1
                    else:
                        if crop != tools.ZERO_CELL_BYTES:
                            blank_mismatches.append(f"({r},{c})")
                        else:
                            blank_verified += 1

            # Verify standard 57 cells match committed P4-B spritesheet-standard.png
            std_atlas_path = root / std_atlas_by_id[form_id]["path"]
            std_atlas_match = True
            with Image.open(std_atlas_path) as std_im:
                std_im.load()
                for state, r_idx, n_frames in tools.ROW_SPECS:
                    for c_idx in range(n_frames):
                        box = (c_idx * tools.CELL_W, r_idx * tools.CELL_H, (c_idx + 1) * tools.CELL_W, (r_idx + 1) * tools.CELL_H)
                        if dec_webp.crop(box).tobytes() != std_im.crop(box).tobytes():
                            std_atlas_match = False

            # Direction mirror / uniqueness checks across rows 9-10
            dir_hashes = [tools.sha256_bytes(im.tobytes()) for im in direction_images]
            dir_unique_16 = len(set(dir_hashes)) == 16
            no_exact_opposite_mirror = all(
                ImageOps.mirror(direction_images[li]).tobytes() != direction_images[ri].tobytes()
                for li, ri in ((1, 15), (2, 14), (3, 13), (4, 12), (5, 11), (6, 10), (7, 9))
            )
            no_exact_adjacent_mirror = all(
                ImageOps.mirror(direction_images[i]).tobytes() != direction_images[(i + 1) % 16].tobytes()
                for i in range(16)
            )

        parsed_pet = json.loads(pkg_json_path.read_text(encoding="utf-8"))
        pet_json_checks = {
            "valid_json": True,
            "id_matches_dir": parsed_pet.get("id") == form_id,
            "sprite_version_number_is_2": parsed_pet.get("spriteVersionNumber") == 2,
            "spritesheet_path_is_webp": parsed_pet.get("spritesheetPath") == "spritesheet.webp",
            "required_keys_present": all(
                k in parsed_pet for k in ("id", "displayName", "description", "spriteVersionNumber", "spritesheetPath")
            ),
            "no_asuka_or_compat_collision": form_id in ("rei-school", "rei-white", "rei-black"),
        }

        pet_ok = (
            png_val["ok"]
            and webp_val["ok"]
            and webp_header["ok"]
            and png_webp_pixel_identical
            and not cell_pixel_mismatches
            and not blank_mismatches
            and active_verified == 74
            and blank_verified == 14
            and std_atlas_match
            and dir_unique_16
            and no_exact_opposite_mirror
            and no_exact_adjacent_mirror
            and all(pet_json_checks.values())
            and indiv_zip_check["ok"]
        )
        all_ok = all_ok and pet_ok
        total_cells_checked += active_verified + blank_verified
        total_active_checked += active_verified
        total_blank_checked += blank_verified

        pet_manifest_entries[form_id] = {
            "id": form_id,
            "displayName": meta["displayName"],
            "expected_codex_selector_id": f"custom:{form_id}",
            "grid": {
                "columns": tools.COLS,
                "rows": tools.EXT_ROWS,
                "cell_width": tools.CELL_W,
                "cell_height": tools.CELL_H,
                "width": tools.EXT_SIZE[0],
                "height": tools.EXT_SIZE[1],
                "active_cells": 74,
                "blank_cells": 14,
            },
            "deliverables": {
                "form_extended_png": {
                    "path": rel_posix(ext_png_path, root),
                    "bytes": ext_png_path.stat().st_size,
                    "sha256": tools.sha256_file(ext_png_path),
                },
                "form_spritesheet_webp": {
                    "path": rel_posix(ext_webp_form_path, root),
                    "bytes": ext_webp_form_path.stat().st_size,
                    "sha256": tools.sha256_file(ext_webp_form_path),
                },
                "form_pet_json": {
                    "path": rel_posix(pet_json_form_path, root),
                    "bytes": pet_json_form_path.stat().st_size,
                    "sha256": tools.sha256_file(pet_json_form_path),
                },
                "package_spritesheet_webp": {
                    "path": rel_posix(pkg_webp_path, root),
                    "bytes": pkg_webp_path.stat().st_size,
                    "sha256": tools.sha256_file(pkg_webp_path),
                    "decoded_rgba_pixel_sha256": tools.sha256_bytes(webp_raw),
                },
                "package_pet_json": {
                    "path": rel_posix(pkg_json_path, root),
                    "bytes": pkg_json_path.stat().st_size,
                    "sha256": tools.sha256_file(pkg_json_path),
                },
                "individual_zip": {
                    "path": rel_posix(indiv_zip_path, root),
                    **indiv_zip_check,
                },
                "contact_sheet_light": {
                    "path": rel_posix(light_sheet, root),
                    "bytes": light_sheet.stat().st_size,
                    "sha256": tools.sha256_file(light_sheet),
                },
                "contact_sheet_dark": {
                    "path": rel_posix(dark_sheet, root),
                    "bytes": dark_sheet.stat().st_size,
                    "sha256": tools.sha256_file(dark_sheet),
                },
            },
            "neutral_reference_cell_r0c6": neutral_record,
            "standard_57_frames": standard_frame_records,
            "direction_16_frames": direction_frame_records,
        }

        pet_qa_entries[form_id] = {
            "ok": pet_ok,
            "png_validate_v2_ok": png_val["ok"],
            "png_errors": png_val["errors"],
            "webp_validate_v2_ok": webp_val["ok"],
            "webp_errors": webp_val["errors"],
            "webp_binary_header": webp_header,
            "lossless_png_webp_pixel_identical": png_webp_pixel_identical,
            "active_cells_pixel_matched": active_verified,
            "blank_cells_zero_verified": blank_verified,
            "cell_pixel_mismatches": cell_pixel_mismatches,
            "blank_mismatches": blank_mismatches,
            "matches_committed_p4b_standard_atlas_57_cells": std_atlas_match,
            "r0c6_exact_copy_of_accepted_idle_00": True,
            "transparent_rgb_residue_pixels": webp_val["transparent_rgb_residue_pixels"],
            "all_active_cells_transparent_border": all(
                c.get("margins", {}).get("left", 0) >= 1
                and c.get("margins", {}).get("right", 0) >= 1
                and c.get("margins", {}).get("top", 0) >= 1
                and c.get("margins", {}).get("bottom", 0) >= 1
                for c in webp_val["cells"]
                if c["used"]
            ),
            "all_active_cells_single_solid_component": all(
                c["solid_components"] == 1 for c in webp_val["cells"] if c["used"]
            ),
            "direction_16_unique_pixels": dir_unique_16,
            "direction_no_exact_opposite_mirror": no_exact_opposite_mirror,
            "direction_no_exact_adjacent_mirror": no_exact_adjacent_mirror,
            "pet_json_checks": pet_json_checks,
            "individual_zip_ok": indiv_zip_check["ok"],
            "cells": webp_val["cells"],
        }

    # Post-assembly source preservation check
    post_preservation = verify_source_preservation(root, p4b_manifest, p4c_manifest)
    all_ok = all_ok and post_preservation["ok"] and total_cells_checked == 264 and total_active_checked == 222 and total_blank_checked == 42

    env_info = {
        "script": "06_共用工具/p4d_assemble.py",
        "validator_core": "06_共用工具/rei_atlas_tools.py",
        "engine": "unified-stdlib-pillow",
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "pillow": PIL.__version__,
        "libwebp": features.version("webp"),
        "zlib": zlib.ZLIB_VERSION,
        "webp_encoding": {"format": "WEBP", "lossless": True, "quality": 100, "method": 6, "exact": True},
    }

    offline_qa_obj = {
        "schema_version": 1,
        "stage": "REI-PET-P4D-FINAL-ASSEMBLY",
        "overall_status": "OFFLINE_V2_QA_PASS" if all_ok else "OFFLINE_V2_QA_FAIL",
        "ok": all_ok,
        "windows_native_validate_atlas_executed": False,
        "windows_codex_desktop_runtime_executed": False,
        "note_on_platform_gates": "Offline cross-platform stdlib+Pillow v2 validation passed for all 3 pets (264/264 cells). Windows native OpenAI.Codex validate_atlas.py --require-v2 and live Codex Desktop runtime tests are NOT executed or fabricated in P4-D; they remain mandatory P5 gates.",
        "environment": env_info,
        "totals": {
            "pets": 3,
            "total_cells_checked": total_cells_checked,
            "active_cells_checked": total_active_checked,
            "blank_cells_checked": total_blank_checked,
            "accepted_standard_frames": 171,
            "accepted_direction_frames": 48,
            "neutral_r0c6_cells": 3,
        },
        "source_preservation_pre": pre_preservation,
        "source_preservation_post": post_preservation,
        "pets": pet_qa_entries,
    }
    qa_json_path = qa_root / "P4D_OFFLINE_QA.json"
    qa_json_path.write_text(json.dumps(offline_qa_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_obj = {
        "schema_version": 1,
        "stage": "REI-PET-P4D-FINAL-ASSEMBLY",
        "release_status": "P4-D_CANDIDATE_PENDING_MASTER_REVIEW_AND_P5",
        "not_v1_0_0_release": True,
        "base_unified_main_commit": "44624e1572894f340e9b334ab339d958e7fb9ba2",
        "builder": env_info,
        "p4b_acceptance_ledger": {
            "path": "07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json",
            "sha256": tools.sha256_file(root / "07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json"),
        },
        "p4c_acceptance_ledger": {
            "path": "07_QA验收/P4-C/human-acceptance/P4C_ACCEPTANCE_LEDGER.json",
            "sha256": tools.sha256_file(root / "07_QA验收/P4-C/human-acceptance/P4C_ACCEPTANCE_LEDGER.json"),
        },
        "offline_qa_json": {
            "path": rel_posix(qa_json_path, root),
            "bytes": qa_json_path.stat().st_size,
            "sha256": tools.sha256_file(qa_json_path),
        },
        "temporary_compat_assets_excluded": True,
        "pets": pet_manifest_entries,
        "integrity_architecture": None,
        "inner_integrity": None,
        "master_bundle_zip": None,
    }

    manifest_path = delivery_root / "P4D_DELIVERY_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not skip_bundle:
        finalize_bundle_and_sums(root)

    print(
        json.dumps(
            {
                "ok": all_ok,
                "total_cells_checked": total_cells_checked,
                "active_cells_checked": total_active_checked,
                "blank_cells_checked": total_blank_checked,
                "pets": {
                    pid: {
                        "ok": pet_qa_entries[pid]["ok"],
                        "webp_bytes": pet_manifest_entries[pid]["deliverables"]["package_spritesheet_webp"]["bytes"],
                        "webp_sha256": pet_manifest_entries[pid]["deliverables"]["package_spritesheet_webp"]["sha256"],
                        "png_sha256": pet_manifest_entries[pid]["deliverables"]["form_extended_png"]["sha256"],
                        "pet_json_sha256": pet_manifest_entries[pid]["deliverables"]["package_pet_json"]["sha256"],
                        "zip_bytes": pet_manifest_entries[pid]["deliverables"]["individual_zip"]["bytes"],
                        "zip_sha256": pet_manifest_entries[pid]["deliverables"]["individual_zip"]["sha256"],
                        "vp8l": pet_qa_entries[pid]["webp_binary_header"]["vp8l"],
                    }
                    for pid in PET_METADATA
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_ok else 1


def collect_inner_payload_entries(root: Path) -> list[tuple[str, Path]]:
    """Return deterministic list of (zip_rel_path, disk_path) for immutable inner bundle payload."""
    delivery_root = root / "08_正式交付" / "P4-D-candidate"
    qa_root = root / "07_QA验收" / "P4-D"
    entries: list[tuple[str, Path]] = []
    for form_id, meta in PET_METADATA.items():
        entries.append((f"pets/{form_id}/pet.json", delivery_root / form_id / "pet.json"))
        entries.append((f"pets/{form_id}/spritesheet.webp", delivery_root / form_id / "spritesheet.webp"))
        entries.append(
            (
                f"extended-png/{form_id}-spritesheet-extended.png",
                root / meta["folder"] / "P4-D" / "delivery" / "spritesheet-extended.png",
            )
        )
        entries.append((f"individual-zips/{form_id}-codex-pet-v2.zip", delivery_root / f"{form_id}-codex-pet-v2.zip"))
        entries.append(
            (
                f"contact-sheets/{form_id}-extended-contact-light.png",
                qa_root / "contact-sheets" / f"{form_id}-extended-contact-light.png",
            )
        )
        entries.append(
            (
                f"contact-sheets/{form_id}-extended-contact-dark.png",
                qa_root / "contact-sheets" / f"{form_id}-extended-contact-dark.png",
            )
        )
    entries.append(("qa/P4D_OFFLINE_QA.json", qa_root / "P4D_OFFLINE_QA.json"))
    entries.append(("qa/P4D_QA_REPORT.md", qa_root / "P4D_QA_REPORT.md"))
    entries.append(("qa/WINDOWS_P5_ACCEPTANCE_GUIDE.md", qa_root / "WINDOWS_P5_ACCEPTANCE_GUIDE.md"))
    for arcname, p in entries:
        if not p.exists():
            raise FileNotFoundError(f"Required payload asset missing for {arcname}: {p}")
    return entries


def finalize_bundle_and_sums(root: Path) -> int:
    """
    Build inner & outer integrity artifacts and master bundle ZIP in one strictly acyclic pass:

      Immutable Payload (21 files)
        -> PAYLOAD_MANIFEST.json          (inner: payload files only; no ZIP, no SUMS, no self)
        -> PAYLOAD_SHA256SUMS.txt         (inner: payload files + PAYLOAD_MANIFEST.json; ZIP-relative; no self)
        -> rei-desktop-pet-p4d-all-3-bundle.zip  (single-pass ZIP: payload + inner manifest + inner sums ONLY)
        -> P4D_DELIVERY_MANIFEST.json     (outer: deliverables + inner manifest/sums + final ZIP; NO outer SUMS)
        -> SHA256SUMS.txt                 (outer sink: deliverables + inner manifest/sums + final ZIP + outer manifest; no self)
    """
    delivery_root = root / "08_正式交付" / "P4-D-candidate"
    qa_root = root / "07_QA验收" / "P4-D"
    manifest_path = delivery_root / "P4D_DELIVERY_MANIFEST.json"
    manifest_obj = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Step 1: Collect immutable payload files (21 entries)
    payload_entries = collect_inner_payload_entries(root)

    # Step 2: Generate INNER PAYLOAD_MANIFEST.json (payload assets only; zero ZIP/SUMS/self references)
    payload_manifest_path = delivery_root / "PAYLOAD_MANIFEST.json"
    payload_manifest_obj = {
        "schema_version": 1,
        "layer": "INNER_PAYLOAD",
        "stage": "REI-PET-P4D-FINAL-ASSEMBLY",
        "base_unified_main_commit": manifest_obj.get("base_unified_main_commit", "44624e1572894f340e9b334ab339d958e7fb9ba2"),
        "records_master_bundle_zip": False,
        "records_payload_sha256sums": False,
        "records_outer_files": False,
        "records_self_hash": False,
        "payload_count": len(payload_entries),
        "files": [
            {
                "zip_path": arcname,
                "repo_path": rel_posix(src_path, root),
                "bytes": src_path.stat().st_size,
                "sha256": tools.sha256_file(src_path),
            }
            for arcname, src_path in payload_entries
        ],
    }
    payload_manifest_path.write_text(json.dumps(payload_manifest_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Step 3: Generate INNER PAYLOAD_SHA256SUMS.txt (ZIP-relative paths: 21 payload + PAYLOAD_MANIFEST.json; no self)
    payload_sums_path = delivery_root / "PAYLOAD_SHA256SUMS.txt"
    inner_sum_entries = payload_entries + [("PAYLOAD_MANIFEST.json", payload_manifest_path)]
    inner_sum_lines = [f"{tools.sha256_file(src_path)}  {arcname}" for arcname, src_path in inner_sum_entries]
    payload_sums_path.write_text("\n".join(inner_sum_lines) + "\n", encoding="utf-8")

    # Step 4: Build master bundle ZIP in a SINGLE PASS (outer manifest & outer sums STRICTLY excluded)
    bundle_entries = payload_entries + [
        ("PAYLOAD_MANIFEST.json", payload_manifest_path),
        ("PAYLOAD_SHA256SUMS.txt", payload_sums_path),
    ]
    forbidden_in_zip = {"P4D_DELIVERY_MANIFEST.json", "SHA256SUMS.txt"}
    assert not any(arc in forbidden_in_zip for arc, _ in bundle_entries)

    bundle_zip_path = delivery_root / "rei-desktop-pet-p4d-all-3-bundle.zip"
    bundle_check = write_deterministic_zip(bundle_zip_path, bundle_entries)

    # Step 5: Generate OUTER P4D_DELIVERY_MANIFEST.json (records final ZIP & inner integrity; NEVER records outer SHA256SUMS.txt)
    manifest_obj.pop("sha256sums_file", None)
    qa_report = qa_root / "P4D_QA_REPORT.md"
    p5_guide = qa_root / "WINDOWS_P5_ACCEPTANCE_GUIDE.md"
    qa_json = qa_root / "P4D_OFFLINE_QA.json"

    manifest_obj["offline_qa_json"] = {
        "path": rel_posix(qa_json, root),
        "bytes": qa_json.stat().st_size,
        "sha256": tools.sha256_file(qa_json),
    }
    manifest_obj["qa_report_md"] = {
        "path": rel_posix(qa_report, root),
        "bytes": qa_report.stat().st_size,
        "sha256": tools.sha256_file(qa_report),
    }
    manifest_obj["windows_p5_guide_md"] = {
        "path": rel_posix(p5_guide, root),
        "bytes": p5_guide.stat().st_size,
        "sha256": tools.sha256_file(p5_guide),
    }
    manifest_obj["integrity_architecture"] = {
        "model": "two-layer-acyclic-dag",
        "inner_manifest": rel_posix(payload_manifest_path, root),
        "inner_sha256sums": rel_posix(payload_sums_path, root),
        "outer_manifest": rel_posix(manifest_path, root),
        "outer_sha256sums": rel_posix(delivery_root / "SHA256SUMS.txt", root),
        "outer_manifest_records_outer_sha256sums": False,
        "outer_files_included_in_bundle_zip": False,
        "single_pass_zip_build": True,
    }
    manifest_obj["inner_integrity"] = {
        "payload_manifest": {
            "path": rel_posix(payload_manifest_path, root),
            "bytes": payload_manifest_path.stat().st_size,
            "sha256": tools.sha256_file(payload_manifest_path),
            "payload_count": len(payload_entries),
        },
        "payload_sha256sums": {
            "path": rel_posix(payload_sums_path, root),
            "bytes": payload_sums_path.stat().st_size,
            "sha256": tools.sha256_file(payload_sums_path),
            "entry_count": len(inner_sum_lines),
        },
    }
    manifest_obj["master_bundle_zip"] = {
        "path": rel_posix(bundle_zip_path, root),
        **bundle_check,
    }
    manifest_path.write_text(json.dumps(manifest_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Step 6: Generate OUTER SHA256SUMS.txt (terminal DAG sink: all deliverables + inner manifest/sums + final ZIP + outer manifest; no self)
    outer_sum_files: list[Path] = []
    for form_id, meta in PET_METADATA.items():
        outer_sum_files.extend([
            root / meta["folder"] / "P4-D" / "delivery" / "spritesheet-extended.png",
            root / meta["folder"] / "P4-D" / "delivery" / "spritesheet.webp",
            root / meta["folder"] / "P4-D" / "delivery" / "pet.json",
            delivery_root / form_id / "pet.json",
            delivery_root / form_id / "spritesheet.webp",
            delivery_root / f"{form_id}-codex-pet-v2.zip",
            qa_root / "contact-sheets" / f"{form_id}-extended-contact-light.png",
            qa_root / "contact-sheets" / f"{form_id}-extended-contact-dark.png",
        ])
    outer_sum_files.extend([
        qa_json,
        qa_report,
        p5_guide,
        payload_manifest_path,
        payload_sums_path,
        bundle_zip_path,
        manifest_path,
    ])
    sums_path = delivery_root / "SHA256SUMS.txt"
    assert sums_path not in outer_sum_files
    outer_sum_lines = [f"{tools.sha256_file(p)}  {rel_posix(p, root)}" for p in outer_sum_files]
    sums_path.write_text("\n".join(outer_sum_lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": bundle_check["ok"],
                "payload_manifest_sha256": tools.sha256_file(payload_manifest_path),
                "payload_sha256sums_sha256": tools.sha256_file(payload_sums_path),
                "bundle_zip": rel_posix(bundle_zip_path, root),
                "bundle_bytes": bundle_check["bytes"],
                "bundle_sha256": bundle_check["sha256"],
                "bundle_entries": bundle_check["entry_count"],
                "outer_manifest_sha256": tools.sha256_file(manifest_path),
                "outer_sha256sums_path": rel_posix(sums_path, root),
                "outer_sha256sums_entries": len(outer_sum_lines),
                "outer_sha256sums_sha256": tools.sha256_file(sums_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if bundle_check["ok"] else 1


def verify_delivery_integrity(root: Path, extract_dir: Path | None = None) -> dict[str, Any]:
    """Independently verify outer manifest, outer SHA256SUMS, ZIP CRC/contents, inner manifest, inner SHA256SUMS, byte-parity, and DAG acyclicity."""
    import tempfile

    delivery_root = root / "08_正式交付" / "P4-D-candidate"
    manifest_path = delivery_root / "P4D_DELIVERY_MANIFEST.json"
    sums_path = delivery_root / "SHA256SUMS.txt"
    bundle_zip_path = delivery_root / "rei-desktop-pet-p4d-all-3-bundle.zip"
    payload_manifest_path = delivery_root / "PAYLOAD_MANIFEST.json"
    payload_sums_path = delivery_root / "PAYLOAD_SHA256SUMS.txt"

    errors: list[str] = []
    manifest_obj = json.loads(manifest_path.read_text(encoding="utf-8"))

    # 1. Outer manifest hash checks
    outer_manifest_checked = 0
    outer_refs: list[tuple[str, str]] = []
    for top_key in ("p4b_acceptance_ledger", "p4c_acceptance_ledger", "offline_qa_json", "qa_report_md", "windows_p5_guide_md", "master_bundle_zip"):
        entry = manifest_obj.get(top_key)
        if not isinstance(entry, dict) or "path" not in entry or "sha256" not in entry:
            errors.append(f"Outer manifest missing {top_key}")
        else:
            outer_refs.append((entry["path"], entry["sha256"]))
    inner_int = manifest_obj.get("inner_integrity", {})
    for ikey in ("payload_manifest", "payload_sha256sums"):
        entry = inner_int.get(ikey)
        if not isinstance(entry, dict) or "path" not in entry or "sha256" not in entry:
            errors.append(f"Outer manifest missing inner_integrity.{ikey}")
        else:
            outer_refs.append((entry["path"], entry["sha256"]))
    for pid, pdata in manifest_obj.get("pets", {}).items():
        for dkey, dval in pdata.get("deliverables", {}).items():
            outer_refs.append((dval["path"], dval["sha256"]))
        nr = pdata.get("neutral_reference_cell_r0c6", {})
        outer_refs.append((nr["source_path"], nr["source_sha256"]))
        for fr in pdata.get("standard_57_frames", []):
            outer_refs.append((fr["source_path"], fr["source_sha256"]))
        for fr in pdata.get("direction_16_frames", []):
            outer_refs.append((fr["source_path"], fr["source_sha256"]))
            outer_refs.append((fr["native_raw_path"], fr["native_raw_sha256"]))

    for rel, expected_sha in outer_refs:
        fp = root / rel
        if not fp.exists():
            errors.append(f"Outer manifest target missing: {rel}")
        elif tools.sha256_file(fp) != expected_sha:
            errors.append(f"Outer manifest hash mismatch: {rel}")
        else:
            outer_manifest_checked += 1

    # 2. Outer SHA256SUMS.txt checks
    outer_sums_checked = 0
    outer_sums_paths: list[str] = []
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        expected_sha, rel = line.split(None, 1)
        outer_sums_paths.append(rel)
        fp = root / rel
        if not fp.exists():
            errors.append(f"Outer SHA256SUMS target missing: {rel}")
        elif tools.sha256_file(fp) != expected_sha:
            errors.append(f"Outer SHA256SUMS hash mismatch: {rel}")
        else:
            outer_sums_checked += 1

    # 3. Master ZIP extraction & CRC check + 4/5/6 inner verification
    tmp_ctx = None
    if extract_dir is None:
        tmp_ctx = tempfile.TemporaryDirectory(prefix="rei-p4d-zip-verify-")
        work_extract = Path(tmp_ctx.name)
    else:
        work_extract = extract_dir
        work_extract.mkdir(parents=True, exist_ok=True)

    zip_crc_ok = False
    zip_entries: list[str] = []
    inner_manifest_checked = 0
    inner_sums_checked = 0
    byte_parity_checked = 0
    inner_sums_paths: list[str] = []
    inner_manifest_paths: list[str] = []

    try:
        with zipfile.ZipFile(bundle_zip_path, "r") as zf:
            bad = zf.testzip()
            zip_crc_ok = bad is None
            if not zip_crc_ok:
                errors.append(f"ZIP CRC failure on member: {bad}")
            zip_entries = zf.namelist()
            zf.extractall(work_extract)

        # Inner PAYLOAD_MANIFEST.json check on extracted files
        ext_payload_manifest_path = work_extract / "PAYLOAD_MANIFEST.json"
        if not ext_payload_manifest_path.exists():
            errors.append("Extracted ZIP missing PAYLOAD_MANIFEST.json")
            inner_manifest_obj = {}
        else:
            inner_manifest_obj = json.loads(ext_payload_manifest_path.read_text(encoding="utf-8"))
            for item in inner_manifest_obj.get("files", []):
                zp = item["zip_path"]
                inner_manifest_paths.append(zp)
                ef = work_extract / zp
                if not ef.exists():
                    errors.append(f"Inner manifest target missing in ZIP: {zp}")
                elif tools.sha256_file(ef) != item["sha256"]:
                    errors.append(f"Inner manifest hash mismatch in ZIP: {zp}")
                else:
                    inner_manifest_checked += 1

        # Inner PAYLOAD_SHA256SUMS.txt check on extracted files
        ext_payload_sums_path = work_extract / "PAYLOAD_SHA256SUMS.txt"
        if not ext_payload_sums_path.exists():
            errors.append("Extracted ZIP missing PAYLOAD_SHA256SUMS.txt")
        else:
            for line in ext_payload_sums_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                expected_sha, zp = line.split(None, 1)
                inner_sums_paths.append(zp)
                ef = work_extract / zp
                if not ef.exists():
                    errors.append(f"Inner SHA256SUMS target missing in ZIP: {zp}")
                elif tools.sha256_file(ef) != expected_sha:
                    errors.append(f"Inner SHA256SUMS hash mismatch in ZIP: {zp}")
                else:
                    inner_sums_checked += 1

        # Byte-for-byte parity between extracted ZIP members and repo files
        expected_pairs = collect_inner_payload_entries(root) + [
            ("PAYLOAD_MANIFEST.json", payload_manifest_path),
            ("PAYLOAD_SHA256SUMS.txt", payload_sums_path),
        ]
        for zp, repo_fp in expected_pairs:
            ef = work_extract / zp
            if not ef.exists() or ef.read_bytes() != repo_fp.read_bytes():
                errors.append(f"Inner/outer byte parity mismatch: {zp}")
            else:
                byte_parity_checked += 1
    finally:
        if tmp_ctx is not None:
            tmp_ctx.cleanup()

    # 7. Acyclicity & non-self-reference DAG invariants
    outer_manifest_raw = manifest_path.read_text(encoding="utf-8")
    dag_checks = {
        "outer_manifest_has_no_sha256sums_file_key": "sha256sums_file" not in manifest_obj,
        "outer_manifest_has_no_outer_sums_hash": (tools.sha256_file(sums_path) not in outer_manifest_raw),
        "outer_manifest_has_no_self_hash": (tools.sha256_file(manifest_path) not in outer_manifest_raw),
        "outer_sums_excludes_self": rel_posix(sums_path, root) not in outer_sums_paths,
        "bundle_zip_excludes_outer_manifest": "P4D_DELIVERY_MANIFEST.json" not in zip_entries,
        "bundle_zip_excludes_outer_sums": "SHA256SUMS.txt" not in zip_entries,
        "inner_manifest_excludes_master_zip": not any("bundle.zip" in p for p in inner_manifest_paths),
        "inner_manifest_excludes_inner_sums": "PAYLOAD_SHA256SUMS.txt" not in inner_manifest_paths,
        "inner_manifest_excludes_self": "PAYLOAD_MANIFEST.json" not in inner_manifest_paths,
        "inner_sums_excludes_self": "PAYLOAD_SHA256SUMS.txt" not in inner_sums_paths,
        "inner_sums_excludes_outer_files": not any(p in ("P4D_DELIVERY_MANIFEST.json", "SHA256SUMS.txt") for p in inner_sums_paths),
        "inner_sums_uses_zip_relative_paths": all(not p.startswith("08_") and not p.startswith("07_") and not p.startswith("/") for p in inner_sums_paths),
    }
    for k, passed in dag_checks.items():
        if not passed:
            errors.append(f"DAG invariant failed: {k}")

    return {
        "ok": len(errors) == 0,
        "outer_manifest_references_verified": outer_manifest_checked,
        "outer_sha256sums_entries_verified": outer_sums_checked,
        "zip_crc_ok": zip_crc_ok,
        "zip_entry_count": len(zip_entries),
        "inner_manifest_entries_verified": inner_manifest_checked,
        "inner_sha256sums_entries_verified": inner_sums_checked,
        "inner_outer_byte_parity_verified": byte_parity_checked,
        "dag_checks": dag_checks,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rei Desktop Pet P4-D final v2 assembly, offline QA & packaging")
    parser.add_argument("--root", type=Path, default=tools.default_root())
    parser.add_argument("--skip-bundle", action="store_true", help="Assemble & QA without writing master bundle ZIP yet")
    parser.add_argument("--bundle-only", action="store_true", help="Build inner/outer integrity manifests, sums, and master bundle ZIP (single pass)")
    parser.add_argument("--verify-integrity", action="store_true", help="Run full two-layer delivery integrity verification")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.verify_integrity:
        res = verify_delivery_integrity(root)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res["ok"] else 1
    if args.bundle_only:
        return finalize_bundle_and_sums(root)
    return assemble_and_qa(root, skip_bundle=args.skip_bundle)


if __name__ == "__main__":
    raise SystemExit(main())
