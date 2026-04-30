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

## 2026-04-30: No.4 未調整交絡（気候・医療資源）

- 修正意図: 未測定交絡の具体例（気候・医療資源）を本文で明示する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: Limitationsの未測定交絡リストへ `climate (snowfall and icing)` を追加。
- SKILL準拠チェック: Limitationsで客観的・具体的に列挙し、主張の強さを抑制。

## 2026-04-30: No.5 空間相関の可能性

- 修正意図: コメント対応の判断根拠を残しつつ、合意方針どおり本文の追加変更は行わない。
- 修正ファイル:
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: 「今回は追加解析せず、本文変更なし」の対応を明示してチェックリストをDone化。
- SKILL準拠チェック: 本文へ不要な断定・過剰追記を行わない方針を維持。

## 2026-04-30: No.6 線形性仮定

- 修正意図: 大平先生コメント（グラフ上、線形性を否定する結果ではないため今回は無視でOK）に沿って運用する。
- 修正ファイル:
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: No.6は本文の新規追記なし（非修正対応）とし、チェックリスト/ログに判断根拠を明記。
- SKILL準拠チェック: 不要な本文追記を行わず、過剰解釈を回避する方針を維持。

## 2026-04-30: No.7 曝露指標（都道府県平均傾斜）の粗さ

- 修正意図: 都道府県平均傾斜という粗い曝露指標の限界が本文に適切に反映されているかを確認し、項目別運用として確定する。
- 修正ファイル:
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: `Manuscript_slope_fracture.qmd` の Limitations に既に「prefecture as a whole」「does not capture micro-scale terrain variations」が明記されていることを確認。本文追加修正は不要と判定。
- SKILL準拠チェック: 既存limitationは簡潔かつ客観的で、過剰主張なく妥当と確認。

## 2026-04-30: No.8 年齢構成不一致（歩行速度40–74 vs 骨折高齢）

- 修正意図: 大平先生コメントの3点（40–74データ制約、直接影響の限定性、Limitation明記）を本文で明示する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約:
  - Discussionに「40–74歳質問票集計しか公開されていないため、文脈共変量として扱う」文を追加。
  - Limitationsに「当該集計が唯一の公開タブであること」「最高齢群への直接関連は限定的」を追加。
- SKILL準拠チェック: 断定回避（likely limited）、簡潔表現、Limitationsでの制約明示を確認。

## 2026-04-30: No.8 wording fix（「唯一」表現の明確化）

- 修正意図: 「唯一」の解釈がNDB全体を指すように読める曖昧性を除去する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: `the only publicly released prefecture-level questionnaire tabulation` を `the only ... tabulation used for this analysis` に置換。
- SKILL準拠チェック: 誤読を招く過剰表現を避け、意味を限定した明確な文へ調整。

## 2026-04-30: No.8 wording fix 2（for which → because）

- 修正意図: 限界説明文の接続をより自然で明快な英語に統一する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: Limitations該当文の `for which` を `because` に置換。
- SKILL準拠チェック: 冗長性を減らし、平易で誤解の少ない接続へ改善。

## 2026-04-30: No.9 年齢標準化不足（粗率）をDeferred化

- 修正意図: 大平先生コメント「寳澤先生コメント参照」に従い、No.9をNo.12と連動処理する。
- 修正ファイル:
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: No.9は単独確定せず Deferred として記録。本文変更は行わない。
- SKILL準拠チェック: 先行して不要な重複修正を避け、整合性優先の運用とした。

## 2026-04-30: No.10 結果解釈の強さ（因果を弱める）

- 修正意図: 因果を示唆しすぎる語感を抑え、関連の示唆として統一する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約:
  - Discussionで `demonstrated` を `showed` に変更。
  - Discussionで `amplifying` を `potentially amplifying` に変更。
  - Conclusionsで `remained positively associated` を `was positively associated` に変更。
- SKILL準拠チェック: 断定を弱める語へ置換し、結論の慎重性を向上。

## 2026-04-30: No.11 biological plausibility文のトーン調整

- 修正意図: 島袋先生コメントに沿って、biological plausibility節の断定性をさらに弱める。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約:
  - `is biologically plausible and supported` → `may be biologically plausible and may be partly supported`
  - `predominant fall mechanism` → `a common fall mechanism`
  - `confirmed` → `suggested`
  - `maximizing fracture vulnerability` → `potentially increasing fracture vulnerability`
- SKILL準拠チェック: may/partly/potentially を使用し、過剰断定を回避。

## 2026-04-30: No.12（No.9同時）高齢化率調整のみでは不十分／年齢標準化不足

- 修正意図: 年齢構造の交絡懸念に対し、公開データのマスキング制約を前提とした補完感度分析（`"-" = 0/5/9`）を本文へ統合し、No.9とNo.12を同時解消する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch2.md`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約:
  - Methodsに、年齢階級別手術表＋e-Stat人口を用いた間接法SIR/ISRの感度分析手順（`0/5/9`シナリオ）を追記。
  - Resultsに、各シナリオでのISR回帰係数（β, 95%CI, *p*）を並記し、符号安定・効果量変動を明示。
  - Discussionに、公開データのマスキング制約下での解釈方針（頑健性確認として扱う）を追記。
  - Limitationsに、補完依存性と二次マスキングの可能性を明記し、番号を Fifth〜Ninth に再整列。
- SKILL準拠チェック: 短文化、断定回避（robustness checks / interpret cautiously）、時制整合を確認。

## 2026-04-30: Results文体微修正（解釈文の削除）

- 修正意図: Resultsでは事実記述に徹するため、解釈文（`We therefore interpret ...`）を削除する。
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - `04_Manuscripts/itemized_revision_log_branch2.md`
- 反映要約: Hip fracture回帰結果段落から、`Results` 内の解釈表現を1文削除。
- SKILL準拠チェック: Resultsの「事実を淡々と記述」の原則に整合。
