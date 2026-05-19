# -*- coding: utf-8 -*-
"""Extract Word comments with highlighted range text."""
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
    return "".join(parts)


def main() -> None:
    docx = Path(sys.argv[1])
    out = Path(sys.argv[2])
    author_filter = sys.argv[3] if len(sys.argv) > 3 else "山岸"

    with zipfile.ZipFile(docx) as z:
        comments_root = ET.fromstring(z.read("word/comments.xml"))
        comments: dict[str, dict[str, str]] = {}
        for c in comments_root.findall(f"{W}comment"):
            cid = c.get(f"{W}id", "")
            comments[cid] = {
                "author": c.get(f"{W}author", ""),
                "text": text_of(c).strip(),
            }
        doc = ET.fromstring(z.read("word/document.xml"))

    # highlighted spans per comment id
    highlight: dict[str, str] = {}
    for p in doc.iter(f"{W}p"):
        active: dict[str, list[str]] = {}
        for child in list(p):
            tag = child.tag
            if tag == f"{W}commentRangeStart":
                cid = child.get(f"{W}id", "")
                if cid:
                    active[cid] = []
            elif tag == f"{W}commentRangeEnd":
                cid = child.get(f"{W}id", "")
                if cid and cid in active:
                    highlight[cid] = re.sub(
                        r"\s+", " ", "".join(active[cid]).strip()
                    )[:500]
                    del active[cid]
            elif tag == f"{W}r":
                t = text_of(child)
                if t:
                    for parts in active.values():
                        parts.append(t)

    lines = [f"FILE: {docx.name}\n", "=" * 80 + "\n"]
    n = 0
    for cid in sorted(comments.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        c = comments[cid]
        if author_filter and author_filter not in c["author"]:
            continue
        n += 1
        lines.append(f"\n### word_id={cid}\n")
        if cid in highlight and highlight[cid]:
            lines.append(f"HIGHLIGHT: {highlight[cid]}\n")
        elif cid in highlight:
            pass
        lines.append(f"COMMENT: {c['text']}\n")
    lines.append(f"\nTOTAL: {n}\n")
    out.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
