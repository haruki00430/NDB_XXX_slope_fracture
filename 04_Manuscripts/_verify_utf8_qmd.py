# -*- coding: utf-8 -*-
"""UTF-8 gate before each manual commit. Run from 04_Manuscripts/: python _verify_utf8_qmd.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for name in ("Manuscript_slope_fracture.qmd", "Manuscript_slope_fracture_anonymous.qmd"):
    path = ROOT / name
    if not path.exists():
        if name.endswith("_anonymous.qmd"):
            continue
        raise SystemExit(f"missing {name}")
    text = path.read_text(encoding="utf-8")
    if "窶" in text or "\ufffd" in text:
        raise SystemExit(f"mojibake in {name}")
    if not text.startswith("---\n"):
        raise SystemExit(f"{name}: invalid YAML front matter")
print("UTF-8: pass")
