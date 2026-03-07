# -*- coding: utf-8 -*-
"""
insert_figures_to_docx.py
--------------------------
Wordファイル (Manuscript_slope_fracture.docx) の
"Figure 1" / "Figure 2" / "Figure 3" 見出し段落の直後に
対応するPNGを挿入するスクリプト。

実行方法（04_Manuscripts フォルダ内で）:
    python insert_figures_to_docx.py
"""

import os
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree

# ---------------------------------------------------------------------------
# パス設定
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_IN  = os.path.join(SCRIPT_DIR, "Manuscript_slope_fracture.docx")
DOCX_OUT = os.path.join(SCRIPT_DIR, "Manuscript_slope_fracture.docx")  # 上書き

FIGURES_DIR = os.path.join(
    SCRIPT_DIR, "..", "03_Analysis", "results", "figures"
)

# Figure 見出しテキスト → 画像ファイル名のマッピング
FIGURE_MAP = {
    "Figure 1": "scatter_slope_fracture.png",
    "Figure 2": "heatmap_correlation.png",
    "Figure 3": "scatter_matrix.png",
    "Figure 4": "fig_map_slope.png",
    "Figure 5": "fig_map_fracture.png",
    "Figure 6": "fig_map_bivariate.png",
}

IMAGE_WIDTH_INCHES = 5.5  # 挿入幅（インチ）

# ---------------------------------------------------------------------------
# ユーティリティ：段落の直後に新段落を XML 操作で挿入する
# ---------------------------------------------------------------------------
def insert_paragraph_after(paragraph):
    """paragraph の直後に空の段落要素を挿入して返す。"""
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    from docx.text.paragraph import Paragraph
    return Paragraph(new_p, paragraph._parent)


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------
def main():
    if not os.path.exists(DOCX_IN):
        print(f"[ERROR] DOCX not found: {DOCX_IN}")
        return

    doc = Document(DOCX_IN)

    # ---- ① 挿入すべき段落インデックスを収集（後ろから処理するため逆順） ----
    # 段落リストを一度スキャンし、(index, figure_key) のリストを作る
    targets = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text in FIGURE_MAP:
            targets.append((i, text))

    if not targets:
        print("[WARN] 'Figure N' heading paragraphs were not found in the document.")
        print("       Paragraphs in the document:")
        for p in doc.paragraphs:
            if p.text.strip():
                print(f"         '{p.text.strip()}'")
        return

    # 後ろから処理することでインデックスのずれを防ぐ
    for idx, fig_key in reversed(targets):
        img_name = FIGURE_MAP[fig_key]
        img_path = os.path.normpath(os.path.join(FIGURES_DIR, img_name))

        if not os.path.exists(img_path):
            print(f"[WARN] Image not found, skipping: {img_path}")
            continue

        # 対象の段落オブジェクト
        para = doc.paragraphs[idx]

        # 直後に新しい段落を XML レベルで挿入
        new_para = insert_paragraph_after(para)

        # 段落を中央揃えに設定
        new_para.alignment = 1  # WD_ALIGN_PARAGRAPH.CENTER

        # 画像を run として追加
        run = new_para.add_run()
        run.add_picture(img_path, width=Inches(IMAGE_WIDTH_INCHES))

        print(f"[OK] Inserted {img_name} after '{fig_key}'")

    doc.save(DOCX_OUT)
    print(f"\n[OK] Saved: {DOCX_OUT}")


if __name__ == "__main__":
    main()
