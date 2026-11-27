#!/usr/bin/env python3
"""
Rei Desktop Pet — Visual Review Center V1.0 Data & Offline Package Builder.

Uses ONLY Python 3.11+ standard library (zero external dependencies) and reads
directly from the repository's canonical manifests without modifying any frozen
assets or candidate frames:
  - 07_QA验收/REI_P4B_ASSET_MANIFEST.json
  - 07_QA验收/REI_P4B_RESUME_MATRIX.json
  - 07_QA验收/P4-B/gate.json

Outputs into `07_QA验收/Review-Center/`:
  - assets/review-data.js           (repo-relative JS bundle, zero fetch() CORS issues)
  - REI_ART_REVIEW_TEMPLATE.json    (canonical review JSON template with asset hashes)
  - rei-review-center-v1.0-offline.zip  (self-contained double-click offline ZIP bundle)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from rei_atlas_tools import ROW_DURATIONS, ROW_SPECS, default_root, sha256_bytes, sha256_file  # noqa: E402

FORM_META: list[dict[str, str]] = [
    {
        "id": "rei-school",
        "label": "校服绫波丽",
        "short_label": "校服",
        "dir": "03_校服绫波丽",
        "master_path": "02_标准化母版/rei-school/master-rgba.png",
        "master_label": "P3 派生 RGBA 母版",
        "offline_master": "media/masters/rei-school-master.png",
    },
    {
        "id": "rei-white",
        "label": "白色战斗服 (00)",
        "short_label": "白服",
        "dir": "04_白色战斗服",
        "master_path": "02_标准化母版/P3-FIX/rei-white-master-rgba-p3-fix.png",
        "master_label": "P3-FIX 透明修复母版",
        "offline_master": "media/masters/rei-white-master-p3-fix.png",
    },
    {
        "id": "rei-black",
        "label": "黑色战斗服 (09)",
        "short_label": "黑服",
        "dir": "05_黑色战斗服",
        "master_path": "02_标准化母版/rei-black/master-rgba.png",
        "master_label": "P3 派生 RGBA 母版",
        "offline_master": "media/masters/rei-black-master.png",
    },
]

QA_WATCH_NOTES: dict[str, str] = {
    "rei-school::waiting": "F6 举掌状态切回 F1 双手交握的循环过渡较直接，请重点复核循环观感。",
    "rei-black::review": "F1–F4 保持扶臂、F5–F6 转为垂臂，循环回 F1 存在姿态切换，请重点复核。",
    "rei-black::waving": "F1/F4 双臂放松垂放（未保持扶臂默认姿态），请确认是否接受该姿态设定。",
}

MARKING_SHEETS: dict[str, dict[str, str]] = {
    "white": {
        "title": "白色战斗服 00 胸前标识高分专检拼图",
        "repo_path": "07_QA验收/P4-B/p4b-chest-markings-qa-white.png",
        "offline_path": "media/markings/p4b-chest-markings-qa-white.png",
    },
    "black": {
        "title": "黑色战斗服 09 胸前标识高分专检拼图",
        "repo_path": "07_QA验收/P4-B/p4b-chest-markings-qa-black.png",
        "offline_path": "media/markings/p4b-chest-markings-qa-black.png",
    },
}


def compute_action_asset_hash(
    form_id: str,
    state_name: str,
    selected_version: str,
    source_sha256: str,
    frame_sha256s: list[str],
) -> str:
    payload = json.dumps(
        {
            "id": form_id,
            "state": state_name,
            "selected_version": selected_version,
            "source_sha256": source_sha256,
            "frame_sha256s": frame_sha256s,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def git_head_sha(root: Path) -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(root), text=True).strip()
        return out
    except Exception:
        return "UNKNOWN"


def build_pilot_payload(root: Path, offline_media: dict[str, Path], offline: bool) -> dict[str, Any]:
    pilot_dir = root / "07_QA验收/CODEX-CLOUD-ART-PILOT"
    manifest = json.loads((pilot_dir / "CODEX_CLOUD_ART_PILOT_MANIFEST.json").read_text(encoding="utf-8"))
    hashes = {asset["path"]: asset["sha256"] for asset in manifest["assets"]}

    def media(relative: str) -> str:
        path = pilot_dir / relative
        if sha256_file(path) != hashes[relative]:
            raise ValueError(f"Pilot asset hash mismatch: {relative}")
        packed = f"media/pilot/{relative}"
        offline_media[packed] = path
        return packed if offline else f"../CODEX-CLOUD-ART-PILOT/{relative}"

    def source(result: dict[str, Any]) -> dict[str, str]:
        return {
            "version": f"codex-cloud-pilot/{result['attempt']}",
            "sourceSha256": hashes[result["raw"]],
        }

    def frame(entry: dict[str, Any]) -> dict[str, str]:
        path = entry["path"]
        return {"src": media(path), "sha256": hashes[path]}

    selected = {item["group"]: item for item in manifest["results"] if item["structure"] == "STRUCTURE_PASS"}
    waiting = selected["waiting"]
    directions = selected["directions"]
    if len(waiting["frames"]) != 6 or [Path(f["path"]).stem for f in directions["frames"]] != ["000", "090", "180", "270"]:
        raise ValueError("Pilot must contain six waiting and four cardinal-direction frames")
    master_path = "02_标准化母版/rei-black/master-rgba.png"
    master_hash = next(item["sha256"] for item in manifest["source"]["inputs"] if item["path"] == master_path)
    if sha256_file(root / master_path) != master_hash:
        raise ValueError("Black pilot reference master hash mismatch")
    failed = next(item for item in manifest["results"] if item["structure"] == "FAILED")

    return {
        "frameCount": 10,
        "blackMaster": {"version": "P3 派生 RGBA 母版", "sha256": master_hash},
        "samples": [
            {"id": "waiting", **source(waiting), "frames": [frame(entry) for entry in waiting["frames"]]},
            *[
                {"id": Path(entry["path"]).stem, **source(directions), "frames": [frame(entry)]}
                for entry in directions["frames"]
            ],
        ],
        "links": {
            "waiting": [
                {"label": "原始 RGBA 条带", "src": media(waiting["raw"])},
                {"label": "浅底对比 GIF", "src": media("evidence/waiting-attempt-01-comparison-light.gif")},
                {"label": "深底对比 GIF", "src": media("evidence/waiting-attempt-01-comparison-dark.gif")},
                {"label": "明暗底边缘", "src": media("evidence/waiting-attempt-01-edges.png")},
                {"label": "手部细节", "src": media("evidence/waiting-attempt-01-hands.png")},
            ],
            "directions": [
                {"label": "原始 RGBA 条带", "src": media(directions["raw"])},
                {"label": "明暗底四方向接触表", "src": media("evidence/directions-attempt-02-contact.png")},
                {"label": "面部、视线与 09 细节", "src": media("evidence/directions-attempt-02-face-and-09.png")},
                {"label": "首次失败原图", "src": media(failed["raw"])},
                {"label": "首次失败检测记录", "src": media(failed["qa"])},
            ],
        },
    }


def build_review_center(root: Path, review_dir: Path) -> dict[str, Any]:
    asset_manifest = json.loads((root / "07_QA验收/REI_P4B_ASSET_MANIFEST.json").read_text(encoding="utf-8"))
    resume_matrix = json.loads((root / "07_QA验收/REI_P4B_RESUME_MATRIX.json").read_text(encoding="utf-8"))

    manifest_rows = {(r["id"], r["state"]): r for r in asset_manifest["registered_rows"]}
    matrix_rows = {(r["id"], r["state"]): r for r in resume_matrix["matrix_3x9"]}

    # Track every media file needed for the offline ZIP: (zip_rel_path, src_abs_path)
    offline_media: dict[str, Path] = {}

    def build_forms_payload(offline: bool) -> list[dict[str, Any]]:
        out = []
        for f in FORM_META:
            abs_m = root / f["master_path"]
            assert abs_m.exists(), f"Missing master: {abs_m}"
            m_sha = sha256_file(abs_m)
            offline_media[f["offline_master"]] = abs_m
            out.append(
                {
                    "id": f["id"],
                    "label": f["label"],
                    "short_label": f["short_label"],
                    "master_label": f["master_label"],
                    "master_repo_path": f["master_path"],
                    "master_sha256": m_sha,
                    "master_src": f["offline_master"] if offline else f"../../{f['master_path']}",
                }
            )
        return out

    def build_marking_sheets(offline: bool) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, spec in MARKING_SHEETS.items():
            abs_p = root / spec["repo_path"]
            assert abs_p.exists(), f"Missing marking sheet: {abs_p}"
            offline_media[spec["offline_path"]] = abs_p
            out[k] = {
                "title": spec["title"],
                "repo_path": spec["repo_path"],
                "sha256": sha256_file(abs_p),
                "src": spec["offline_path"] if offline else f"../../{spec['repo_path']}",
            }
        return out

    def build_historical_comparison(form_id: str, state_name: str, offline: bool) -> dict[str, Any] | None:
        if form_id == "rei-black" and state_name == "running-right":
            old_dir = root / "05_黑色战斗服/P4-A/selected/running-right/frames"
            old_src = root / "05_黑色战斗服/P4-A/originals/running-right/attempt-01/source.png"
            assert old_src.exists()
            old_frames = []
            for idx in range(8):
                fp = old_dir / f"{idx:02d}.png"
                assert fp.exists(), f"Missing rejected black frame: {fp}"
                off_rel = f"media/rejected/rei-black-running-right-old/{idx:02d}.png"
                offline_media[off_rel] = fp
                old_frames.append(
                    {
                        "index": idx,
                        "repo_path": f"05_黑色战斗服/P4-A/selected/running-right/frames/{idx:02d}.png",
                        "sha256": sha256_file(fp),
                        "src": off_rel if offline else f"../../05_黑色战斗服/P4-A/selected/running-right/frames/{idx:02d}.png",
                    }
                )
            return {
                "type": "animated-frames",
                "old_version": "P4-A/attempt-01 (已拒收旧版)",
                "old_source_sha256": sha256_file(old_src),
                "reason": "用户人工验收拒收旧版黑服右跑，已由 FIX-BLACK 新版替代并人工验收通过（8 帧 ACCEPTED）；旧版原图与帧仅保留供新旧对照，严禁进入图集。",
                "old_frames": old_frames,
            }

        if form_id == "rei-white" and state_name == "idle":
            old_strip = root / "04_白色战斗服/P4-A/originals/idle/attempt-01/source.png"
            new_strip = root / "04_白色战斗服/P4-A/originals/idle/attempt-02/source.png"
            assert old_strip.exists() and new_strip.exists()
            off_old = "media/rejected/rei-white-idle-attempt-01-source.png"
            off_new = "media/rejected/rei-white-idle-attempt-02-source.png"
            offline_media[off_old] = old_strip
            offline_media[off_new] = new_strip
            return {
                "type": "source-strips",
                "old_version": "P4-A/attempt-01 (透明背景缺陷拒收)",
                "old_source_sha256": sha256_file(old_strip),
                "old_strip_src": off_old if offline else "../../04_白色战斗服/P4-A/originals/idle/attempt-01/source.png",
                "new_strip_src": off_new if offline else "../../04_白色战斗服/P4-A/originals/idle/attempt-02/source.png",
                "reason": "白服 idle attempt-01 因原生透明通道缺陷被拒收，已由 attempt-02 原生真透明条带修复并锁定为 P4-A 受保护基线。",
            }
        return None

    def build_actions_payload(offline: bool) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        for state_name, row_idx, expected_n in ROW_SPECS:
            durations = list(ROW_DURATIONS[state_name])
            assert len(durations) == expected_n
            for fmeta in FORM_META:
                fid = fmeta["id"]
                mrow = manifest_rows[(fid, state_name)]
                xrow = matrix_rows[(fid, state_name)]
                assert len(mrow["frames"]) == expected_n
                assert mrow["frame_duration_ms"] == durations, f"Timing mismatch on {fid}/{state_name}"

                frames_payload = []
                frame_sha256s = []
                for idx, fr in enumerate(mrow["frames"]):
                    fp = root / fr["path"]
                    assert fp.exists(), f"Missing frame: {fp}"
                    actual_sha = sha256_file(fp)
                    assert actual_sha == fr["sha256"], f"Frame hash mismatch: {fr['path']}"
                    assert actual_sha == xrow["frame_sha256s"][idx], f"Matrix hash mismatch: {fr['path']}"

                    off_rel = f"media/frames/{fid}/{state_name}/{idx:02d}.png"
                    offline_media[off_rel] = fp
                    frame_sha256s.append(actual_sha)
                    frames_payload.append(
                        {
                            "index": idx,
                            "repo_path": fr["path"],
                            "sha256": actual_sha,
                            "bytes": fp.stat().st_size,
                            "duration_ms": durations[idx],
                            "src": off_rel if offline else f"../../{fr['path']}",
                        }
                    )

                source_path = xrow["source_path"]
                source_abs = root / source_path
                assert source_abs.exists(), f"Missing source strip: {source_abs}"
                source_sha = sha256_file(source_abs)
                assert source_sha == xrow["source_sha256"]

                key = f"{fid}::{state_name}"
                action_hash = compute_action_asset_hash(
                    fid, state_name, xrow["selected_version"], source_sha, frame_sha256s
                )
                # Governance rule: ONLY rei-black::running-right (8 frames) is explicitly ACCEPTED.
                is_preapproved = fid == "rei-black" and state_name == "running-right"
                assert is_preapproved == (xrow["status"] == "ACCEPTED")

                actions.append(
                    {
                        "key": key,
                        "id": fid,
                        "state": state_name,
                        "row": row_idx,
                        "frame_count": expected_n,
                        "durations_ms": durations,
                        "selected_version": xrow["selected_version"],
                        "origin_phase": xrow["origin_phase"],
                        "produced_by": xrow["produced_by"],
                        "protected_p4a_baseline": bool(xrow["protected_p4a_baseline"]),
                        "structure_qa": xrow["structure_qa"],
                        "source_path": source_path,
                        "source_sha256": source_sha,
                        "action_asset_hash": action_hash,
                        "initial_status": "ACCEPTED" if is_preapproved else "PENDING",
                        "initial_comment": (
                            "用户已明确人工验收通过的 FIX-BLACK 新版黑服右跑（8 帧），禁止重做。"
                            if is_preapproved
                            else ""
                        ),
                        "initial_updated_at": "2026-11-27T00:00:00Z" if is_preapproved else None,
                        "locked_preapproved": is_preapproved,
                        "qa_attention": key in QA_WATCH_NOTES,
                        "qa_attention_note": QA_WATCH_NOTES.get(key),
                        "agy_visual_notes": xrow.get("agy_visual_notes", ""),
                        "frames": frames_payload,
                        "historical_comparison": build_historical_comparison(fid, state_name, offline=offline),
                    }
                )
        return actions

    repo_actions = build_actions_payload(offline=False)
    offline_actions = build_actions_payload(offline=True)
    assert len(repo_actions) == 27
    total_frames = sum(a["frame_count"] for a in repo_actions)
    assert total_frames == 171

    manifest_fingerprint = sha256_bytes(
        json.dumps(
            [{"key": a["key"], "action_asset_hash": a["action_asset_hash"]} for a in repo_actions],
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    rows_meta = [
        {"state": st, "row": r, "expected_frames": n, "durations_ms": list(ROW_DURATIONS[st])}
        for st, r, n in ROW_SPECS
    ]
    baseline_commit = git_head_sha(root)
    # Keep the official baseline revision stable when only review tooling changes.
    previous_template = root / "07_QA验收/Review-Center/REI_ART_REVIEW_TEMPLATE.json"
    if previous_template.is_file():
        previous = json.loads(previous_template.read_text(encoding="utf-8"))
        if previous.get("manifest_fingerprint") == manifest_fingerprint:
            baseline_commit = previous["baseline_commit"]

    def make_bundle(offline: bool) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "project": "rei-desktop-pet",
            "tool": "Rei Review Center V1.0",
            "stage": "P4-B PARTIAL",
            "bundle_mode": "offline-zip" if offline else "repo-relative",
            "baseline_commit": baseline_commit,
            "manifest_fingerprint": manifest_fingerprint,
            "total_actions": 27,
            "total_frames": 171,
            "forms": build_forms_payload(offline=offline),
            "rows": rows_meta,
            "marking_sheets": build_marking_sheets(offline=offline),
            "actions": offline_actions if offline else repo_actions,
        }

    repo_bundle = make_bundle(offline=False)
    offline_bundle = make_bundle(offline=True)

    assets_dir = review_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    repo_data_js = assets_dir / "review-data.js"
    repo_data_js.write_text(
        "window.REI_REVIEW_DATA = " + json.dumps(repo_bundle, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    # Canonical baseline review template JSON (REI_ART_REVIEW_TEMPLATE.json)
    template_payload = {
        "schema_version": 1,
        "project": "rei-desktop-pet",
        "tool": "Rei Review Center V1.0",
        "stage": "P4-B PARTIAL",
        "baseline_commit": baseline_commit,
        "manifest_fingerprint": manifest_fingerprint,
        "exported_at": None,
        "structure_pass_never_auto_accepted": True,
        "summary": {
            "total_actions": 27,
            "total_frames": 171,
            "actions_by_status": {"ACCEPTED": 1, "NEEDS_FIX": 0, "REJECTED": 0, "PENDING": 26},
            "frames_by_status": {"ACCEPTED": 8, "NEEDS_FIX": 0, "REJECTED": 0, "PENDING": 163},
            "invalidated_actions": 0,
        },
        "decisions": [
            {
                "key": a["key"],
                "id": a["id"],
                "state": a["state"],
                "row": a["row"],
                "frame_count": a["frame_count"],
                "status": a["initial_status"],
                "comment": a["initial_comment"],
                "updated_at": a["initial_updated_at"],
                "selected_version": a["selected_version"],
                "source_sha256": a["source_sha256"],
                "action_asset_hash": a["action_asset_hash"],
                "frame_sha256s": [f["sha256"] for f in a["frames"]],
                "locked_preapproved": a["locked_preapproved"],
                "invalidated": False,
                "invalidated_reason": None,
                "stale_previous_status": None,
                "stale_previous_asset_hash": None,
            }
            for a in repo_actions
        ],
    }
    template_path = review_dir / "REI_ART_REVIEW_TEMPLATE.json"
    template_path.write_text(json.dumps(template_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pilot_repo_data = build_pilot_payload(root, offline_media, offline=False)
    pilot_offline_data = build_pilot_payload(root, offline_media, offline=True)
    (assets_dir / "pilot-data.js").write_text(
        "window.REI_PILOT_DATA = " + json.dumps(pilot_repo_data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    # Build deterministic self-contained offline ZIP package
    offline_data_js_bytes = (
        "window.REI_REVIEW_DATA = " + json.dumps(offline_bundle, ensure_ascii=False, indent=2) + ";\n"
    ).encode("utf-8")

    zip_path = review_dir / "rei-review-center-v1.0-offline.zip"
    static_files = [
        ("rei-review-center-v1.0/index.html", review_dir / "index.html"),
        ("rei-review-center-v1.0/pilot.html", review_dir / "pilot.html"),
        ("rei-review-center-v1.0/assets/pilot.css", assets_dir / "pilot.css"),
        ("rei-review-center-v1.0/assets/pilot.js", assets_dir / "pilot.js"),
        ("rei-review-center-v1.0/assets/styles.css", assets_dir / "styles.css"),
        ("rei-review-center-v1.0/assets/app.js", assets_dir / "app.js"),
        ("rei-review-center-v1.0/REI_ART_REVIEW_TEMPLATE.json", template_path),
    ]
    readme_path = review_dir / "REVIEW_CENTER_README.md"
    if readme_path.exists():
        static_files.append(("rei-review-center-v1.0/REVIEW_CENTER_README.md", readme_path))

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        def write_entry(arcname: str, data: bytes) -> None:
            zi = zipfile.ZipInfo(filename=arcname, date_time=(2026, 11, 27, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, data)

        for arcname, src in static_files:
            assert src.exists(), f"Missing static review file: {src}"
            write_entry(arcname, src.read_bytes())

        write_entry("rei-review-center-v1.0/assets/review-data.js", offline_data_js_bytes)
        pilot_script = "window.REI_PILOT_DATA = " + json.dumps(pilot_offline_data, ensure_ascii=False, indent=2) + ";\n"
        write_entry("rei-review-center-v1.0/assets/pilot-data.js", pilot_script.encode("utf-8"))

        for rel_media in sorted(offline_media.keys()):
            src = offline_media[rel_media]
            write_entry(f"rei-review-center-v1.0/{rel_media}", src.read_bytes())

    # Verify ZIP integrity
    with zipfile.ZipFile(zip_path, "r") as zf:
        assert zf.testzip() is None
        zip_entries = zf.namelist()

    return {
        "ok": True,
        "total_actions": 27,
        "total_frames": 171,
        "pre_accepted_actions": 1,
        "pre_accepted_frames": 8,
        "pending_actions": 26,
        "pending_frames": 163,
        "manifest_fingerprint": manifest_fingerprint,
        "offline_media_files_bundled": len(offline_media),
        "zip_entries_count": len(zip_entries),
        "deliverables": {
            "repo_data_js": {"path": repo_data_js.relative_to(root).as_posix(), "bytes": repo_data_js.stat().st_size, "sha256": sha256_file(repo_data_js)},
            "template_json": {"path": template_path.relative_to(root).as_posix(), "bytes": template_path.stat().st_size, "sha256": sha256_file(template_path)},
            "offline_zip": {"path": zip_path.relative_to(root).as_posix(), "bytes": zip_path.stat().st_size, "sha256": sha256_file(zip_path)},
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Rei Review Center V1.0 data bundle and offline ZIP")
    parser.add_argument("--root", type=Path, default=default_root(), help="Path to repository root")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Review Center directory (default: <root>/07_QA验收/Review-Center)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    out_dir = args.out_dir.resolve() if args.out_dir else (root / "07_QA验收/Review-Center")
    res = build_review_center(root, out_dir)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
