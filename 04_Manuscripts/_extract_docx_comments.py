# -*- coding: utf-8 -*-
"""Extract Word comments from docx (one-off helper)."""
from __future__ import annotations

import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def text_of(el: ET.Element) -> str:
    parts: list[str] = []
    for t in el.iter(f"{W}t"):
        if t.text:
            parts.append(t.text)
        if t.tail:
            parts.append(t.tail)
    return "".join(parts).strip()


def main() -> None:
    docx = Path(__file__).resolve().parent / (
        "Manuscript_slope_fracture_20260425_saito0430(1).docx"
    )
    if len(sys.argv) > 1:
        docx = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    with zipfile.ZipFile(docx) as z:
        comments_root = ET.fromstring(z.read("word/comments.xml"))
        comments: dict[str, dict[str, str]] = {}
        for c in comments_root.findall(f"{W}comment"):
            cid = c.get(f"{W}id", "")
            comments[cid] = {
                "author": c.get(f"{W}author", ""),
                "date": c.get(f"{W}date", ""),
                "text": text_of(c),
            }

        doc = ET.fromstring(z.read("word/document.xml"))

    # Map comment id -> paragraph excerpt (first paragraph containing reference)
    anchor: dict[str, str] = {}
    for p in doc.iter(f"{W}p"):
        ptext = text_of(p)
        if not ptext:
            continue
        for ref in p.findall(f".//{W}commentReference"):
            cid = ref.get(f"{W}id", "")
            if cid and cid not in anchor:
                anchor[cid] = ptext[:400]

    lines: list[str] = [f"FILE: {docx.name}\n", "=" * 80 + "\n"]
    y_count = 0
    for cid in sorted(comments.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        c = comments[cid]
        author = c["author"]
        yamagishi_only = "--all" not in sys.argv
        if yamagishi_only and "山岸" not in author:
            continue
        y_count += 1
        lines.append(f"\n[山岸] word_comment_id={cid}\n")
        if cid in anchor:
            snip = re.sub(r"\s+", " ", anchor[cid])
            lines.append(f"ANCHOR: {snip}\n")
        lines.append(f"TEXT: {c['text']}\n")
    lines.append(f"\nTOTAL Yamagishi comments: {y_count}\n")
    text = "".join(lines)
    if out:
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
