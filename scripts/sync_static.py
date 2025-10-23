#!/usr/bin/env python3
"""Copy contents of src/static -> public preserving directory structure and binary files."""
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / 'src' / 'static'
DST = Path(__file__).resolve().parents[1] / 'public'

if not SRC.exists():
    print(f"Source static dir not found: {SRC}")
    raise SystemExit(1)

if DST.exists():
    # remove existing public content
    shutil.rmtree(DST)

shutil.copytree(SRC, DST)
print(f"Copied {SRC} -> {DST}")
