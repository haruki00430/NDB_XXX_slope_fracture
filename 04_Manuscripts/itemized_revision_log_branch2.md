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

## 2026-04-30: No.2 サンプルサイズとモデル安定性（N=47）

- 修正意図: small-N下での推定安定性と多重共線性懸念に対する本文上の明示を追加。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: Statistical Analysisに、*N*=47での係数安定性・多重共線性診断（condition numberを含む）を確認し慎重解釈する旨を追記。
- SKILL準拠チェック: Methodsの簡潔な追記で過剰主張を回避し、解釈の慎重性を維持。

## 2026-04-30: No.3 アウトカム（手術率）の解釈

- 修正意図: アウトカムが発症率ではなく手術率である制約を明示する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: Limitationsに「surgery rates rather than true fracture incidence」および治療方針・アクセス差の影響可能性を追加。
- SKILL準拠チェック: limitationを具体化しつつ、断定的因果主張を避ける記述へ調整。
