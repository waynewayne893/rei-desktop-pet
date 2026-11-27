#!/usr/bin/env python3
"""
Backwards-compatible CLI alias & symbol shim for `06_共用工具/rei_atlas_tools.py`.

Preserved for historical traceability from `REI-PET-CLOUD-BOOTSTRAP` (`c5b5b4f`).
All canonical verification, standard atlas reassembly, v2 validation, and
P4-COMPAT build implementations now live in the unified single source of truth:
`06_共用工具/rei_atlas_tools.py` (Python stdlib + Pillow, zero extra dependencies).
"""

from __future__ import annotations

import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from rei_atlas_tools import (  # noqa: E402, F401
    CELL_H,
    CELL_W,
    COLS,
    EXT_NEUTRAL_CELL,
    EXT_ROWS,
    EXT_SIZE,
    FORMS,
    LOOK_DIRECTIONS,
    ROW_DURATIONS,
    ROW_SPECS,
    STD_ROWS,
    STD_SIZE,
    analyze_cell,
    clear_transparent_rgb,
    cmd_build_compat,
    cmd_reassemble,
    cmd_verify,
    count_8_connected,
    count_transparent_rgb_residue,
    default_root,
    inspect_png_chunks,
    load_font,
    main,
    sha256_bytes,
    sha256_file,
    validate_atlas_image,
)

if __name__ == "__main__":
    sys.exit(main())
