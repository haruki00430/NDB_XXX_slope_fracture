# Health & Place 投稿規定チェックリスト

出典: *Guide for authors* (Elsevier, Health & Place) および [journal guide](https://www.sciencedirect.com/journal/health-and-place/publish/guide-for-authors)。提出直前に公式ページの最新版と必ず照合すること。

## 原稿体裁

- [x] 通常論文 4000–6000 語（図・表・参考文献除く）。branch-3 改稿後 **5044 words**（Introduction〜Data availability；`_wordcount_branch3.py`）。6,000 以内のため Discussion 一括削減は見送り。
- [x] Abstract 250 語以下、参照なし（**200 words**）。
- [x] Keywords 1–7（英語）。複合語は最小限に。
- [x] Highlights は別ファイル（ファイル名に `highlights`）、3–5 点、各 **85 文字以内（スペース含む）**。→ `highlights_Health_and_Place.txt`
- [ ] 編集可能ソース（`.docx` / `.tex` 等）。提出用 PDF はソースに代わらない。→ Quarto で `.docx` 生成し EM にアップロード。
- [ ] 単段組（Word）。表は編集可能テキスト、縦罫線・セル内シャドウ回避。→ 原稿内 *Submission note* 参照。Word 取り込み後に罫線調整。

## 二重匿名査読

- [ ] タイトルページ（著者・所属・連絡先・謝辞・利益相反・資金（該当時））を**別ファイル**。→ `Title_page_Health_and_Place_template.md` を参照。
- [ ] 匿名原稿に著者名・所属・謝辞・資金を含めない。→ `Manuscript_slope_fracture_anonymous.qmd` 利用。

## 図表・地図

- [x] 図は別添ファイル、本文で Figure を参照。→ 原稿 *Submission note* に EM 用の別ファイル添付を明記。
- [x] 地図: 研究域の境界が国際的合意を意味しない旨の注記（該当時）。→ Figure 3–5 キャプションに誌の表記に沿った注記あり。

## データ・倫理・CRediT

- [x] Data availability / データ表明（共有不可の理由も可）。
- [ ] CRediT（対応著者が共同著者の役割を記載）。→ **タイトルページ**に記載（本文では案内のみ）。
- [ ] 資金・利益相反（該当なしも宣言ツールで明示）。→ Elsevier の declarations ツールで `.docx` 生成し EM にアップロード。

## 生成 AI（Elsevier 必須の場合）

- [x] 原稿に、参考文献の直前に **Declaration of generative AI…** セクションを挿入済み。Grammar/スペルチェックのみの場合は Elsevier の例に従い **該当セクションを削除** するか、実態に合わせて文面を修正すること。

## 参考文献

- [ ] 本文とリストの対応、欠番なし。
- [ ] DOI を付与できる文献には DOI を記載推奨。

## Web 版との差分

提出直前に公式 *Guide for authors* を開き、上記と矛盾する追加要件がないか確認する。
