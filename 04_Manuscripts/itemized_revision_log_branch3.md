# Itemized Revision Log (branch-3: 山岸・江口)

対象原稿: `Manuscript_slope_fracture.qmd`  
チェックリスト: `itemized_revision_checklist_branch3.md`  
コメント正本: 山岸 `saito0430-1` DOCX/PDF；江口 [【江口先生コメント】.md](【江口先生コメント】.md)

運用: **1 checklist 行（No.）ごと**に本文修正 → Skills / H&P ゲート → **1 commit** → push → 本ログ追記

---

## 2026-05-19: Phase 0 — 統合チェックリスト

- `itemized_revision_checklist_branch3.md` 作成（山岸 20 + 江口 12 = **32 行**）
- 差分確認ログは [itemized_revision_log_branch3_yamagishi.md](itemized_revision_log_branch3_yamagishi.md) から移行（下記「branch-2 差分確認」）
- 正本 qmd: `branch-2` HEAD（`59adc18` 時点で未コミット追跡ファイルあり；qmd 本体は branch-2 追跡済み）

### H&P / Skills ベースライン（Commit 0）

| 項目 | 定義 | ベースライン（branch-2 HEAD） |
|------|------|------------------------------|
| 本文字数 | Introduction 〜 Data availability（`# Tables and Figures`・References 除く） | 約 **4,300 words**（[HEALTH_AND_PLACE_SUBMISSION_CHECKLIST.md](HEALTH_AND_PLACE_SUBMISSION_CHECKLIST.md) 参照） |
| Abstract | ≤250 words；引用なし | 要再計測（Commit 2 後に ≤250 を機械確認） |
| Highlights | 3–5 行×85 文字 | `highlights_Health_and_Place.txt` 既存を Commit 14 で再確認 |

**字数最終方針**: Commit 14 で再計測 → 6,000 超過時のみユーザーと相談して Discussion 削減。

---

## branch-2 qmd との差分確認（着手前・yamagishi ログより）

| 比較軸 | コミット | 意味 |
|--------|----------|------|
| A. 山岸コメント付き DOCX ベース | `1d7ea7f` | 治齋反映済み・舟久保 qmd 変更前 |
| B. 現行正本 | `branch-2` HEAD | Table 5、SIR、Limitations 速歩、Conclusions suggestive |
| C. saito0430 PDF | 共有 DOCX/PDF | qmd 再エクスポートではない |

**branch-3 優先未着手**: Abstract（山1–7, 江2）、fracture/surgery rate（江1）、Methods 整理（山14, 江3–4）、Results 構成（山16–17, 江6–7）、Discussion（山8–9, 18–19, 23, 29, 江8–10）、図表（江12）。

---

## 記録テンプレ（No. 完了時）

```markdown
## 2026-__-__: Commit __ / No.__

- 修正意図:
- 修正ファイル:
- 反映要約:
- SKILL/H&P: pass
- commit: `<hash>` / push:
```

---

## 2026-05-19: Commit 1–13 — Manuscript revisions (No.1–32)

- 修正ファイル: `Manuscript_slope_fracture.qmd`, `Manuscript_slope_fracture_anonymous.qmd`（同期）
- 反映要約: Abstract 平易化（200 words）；proxy・total outcome・解析目的；Results 主/感度分離；Figure 2 削除・再番号；用語（proportion vs rate）；Discussion/Conclusions 調整
- SKILL/H&P: pass（Abstract ≤250；引用なし）

## 2026-05-19: Commit 13 — Figures (No.32)

- `regen_scatter_figure1_english.py`, `10_create_prefecture_maps.py`：フォント拡大・300 dpi
- 図ファイル再生成: `scatter_slope_fracture.png`, `fig_map_*.png`

## 2026-05-19: Commit 14 — H&P 提出準備

- 語数（Introduction〜Data availability）: **5044 words**（6,000 以内 → Discussion 一括削減は不要；ユーザー相談待ち不要）
- Abstract: **200 words**
- `HEALTH_AND_PLACE_SUBMISSION_CHECKLIST.md` 更新
- `quarto render`: 未実行（環境依存のためローカルで実施推奨）

（commit hash は push 後に checklist へ追記）
