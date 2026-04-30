# Itemized Revision Log (branch-2)

対象原稿: `Manuscript_slope_fracture.qmd`  
運用: 1修正項目ごとに本文修正→SKILL準拠確認→コミット→push→記録

## 2026-04-30: Setup

- 作業運用ファイルを作成した（本ログ / 実行用チェックリスト）。
- 次回以降、No.ごとに以下を追記する。
  - 対象No.
  - 修正意図
  - 修正ファイル
  - 反映要約
  - SKILL準拠チェック結果
  - commit hash / push結果

## 2026-04-30: No.1 高齢化率・歩行速度の位置づけ（交絡/媒介）

- 修正意図: 交絡調整として扱う方針を本文で明示し、媒介断定を避ける。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: MethodsのModel定義直下に「aging rate / fast walking rateをformal mediatorではなくconfounder-adjustment variableとして扱う」文を追加。
- SKILL準拠チェック: 断定回避（causal claimを限定）、短文化、Methodsの過去形文脈との整合を確認。
