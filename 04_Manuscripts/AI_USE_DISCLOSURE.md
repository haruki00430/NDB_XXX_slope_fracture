# 生成AI・エージェント利用開示（論文別）

> 本ファイルは [00_Docs/templates/AI_USE_DISCLOSURE.template.md](../../../00_Docs/templates/AI_USE_DISCLOSURE.template.md) に基づく。運用は [CIRCS_NDB_MANUSCRIPT_AI_RULEBOOK.md](../../../00_Docs/07_Setup/CIRCS_NDB_MANUSCRIPT_AI_RULEBOOK.md) を参照。

---

## メタデータ

| 項目 | 内容 |
|------|------|
| 論文仮題 | 地形傾斜度と高齢者骨折リスク・歩行習慣の関連 |
| 論文仮題（英語） | Terrain slope, fracture risk, and walking habits in older adults (ecological study) |
| プロジェクトパス | `projects/NDB_XXX_slope_fracture/` |
| 対象誌（候補） | （追記） |
| 最終更新日 | 2026-04-08 |
| 記録責任者 | 通信著者（`Manuscript_slope_fracture.qmd` の YAML `author` と同一。投稿前に実名へ） |

**原稿の正本**: `04_Manuscripts/Manuscript_slope_fracture.qmd`

---

## 使用ツール一覧

| ツール・サービス | 区分 | モデル・バージョン（分かる範囲） | 主な用途 |
|------------------|------|----------------------------------|----------|
| Cursor | クラウドエージェント（設定依存） | 利用時点のエージェントモデル | DEM・骨折手術抽出・媒介分析・Quarto |
| LM Studio 等 | ローカル | — | 使用時は追記 |

**注**: AIを著者にしない。

---

## 研究段階別の利用

### 1. データ整備・ETL・スクリプト生成

| 日付 | ツール | 実施内容（1行） | 備考 |
|------|--------|-----------------|------|
| （追記） | Cursor 等 | 地形・NDB・e-Stat 統合 | `analysis/`・`docs/` |

### 2. 探索的スクリーニング／ローカルLLM

| 日付 | ツール | 実施内容（1行） | 備考 |
|------|--------|-----------------|------|
| — | — | **該当なし**（用いた場合は追記） |  |

### 3. 確証的分析・可視化

| 日付 | ツール | 実施内容（1行） | 備考 |
|------|--------|-----------------|------|
| （追記） | Cursor 等 | 回帰・媒介・感度 | `results/` |

### 4. 原稿

| 日付 | ツール | 実施内容（1行） | 備考 |
|------|--------|-----------------|------|
| （追記） | Cursor 等 | Quarto 推敲 |  |

### 5. 参考文献

| 日付 | ツール | 実施内容（1行） | 備考 |
|------|--------|-----------------|------|
| （追記） | Cursor 等 | `references.bib` |  |

---

## データ境界

### 外部クラウドLLMに**送らなかった**もの

- [x] NDB 生データの実数値・スクリーンショット
- [x] 個票・再識別可能な細集計の丸貼り

### 送ったもの（機微度が低い範囲）

| 種別 | 例 |
|------|-----|
| メタデータ・コード | 列名、スクリプト、パス |

### ローカルLLMに入力したもの

| 種別 | 例 |
|------|-----|
| （追記） |  |

---

## 人間による検証

| 段階 | 確認内容 | 実施者 | 日付 |
|------|----------|--------|------|
| コード・数値・引用・解釈 | DEM 処理・骨折コード・媒介経路 | 著者 | （追記） |

---

## 投稿用短文ドラフト

### 日本語（案）

本研究では、文献整理、コード補助、英文推敲、原稿構成の支援に生成AIを利用した。外部クラウドAIには個人情報およびNDB生データの実数値を入力せず、必要時のみ機微性の低いメタデータ（変数名、コード断片、手順記述）を用いた。統計手法の選択、解析結果、解釈、結論は著者が最終確認・修正し、内容に対する責任は著者が負う。生成AIは著者に含めていない。

### English (draft)

During the preparation of this work, the authors used AI-assisted coding and writing tools to support manuscript preparation and analysis scripting. The authors reviewed and edited all AI-assisted outputs, were solely responsible for the selection of statistical methods, interpretation of findings, conclusions, and references, and take full responsibility for the final content. AI was not listed as an author.

---

## 変更履歴

| 日付 | 変更内容 |
|------|----------|
| 2026-04-08 | 初版（プロジェクト一括整備） |
| 2026-04-14 | 投稿原稿・匿名稿・本ファイルの English draft を同一文に同期（AI開示文を簡潔化・統一） |
