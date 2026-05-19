# -*- coding: utf-8 -*-
import re
from pathlib import Path

t = Path("Manuscript_slope_fracture.qmd").read_text(encoding="utf-8")
ab = re.search(r"# Abstract\n\n(.*?)\n\n\*\*Keywords", t, re.S).group(1)
main = re.search(r"# Introduction\n(.*?)# References", t, re.S).group(1)
w = lambda s: len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", s))
print("abstract_words", w(ab))
print("main_body_words", w(main))
