# Itemized Revision Log (branch-3) — 手動コミット運用

**リセット日**: 2026-05-19  
**理由**: 自動32コミットは康永 Skill（`manuscript-writing-quality`）の鉄則に基づく英文リライトを実施しておらず、パッチ＋ログ上の `MQ: pass` のみだったため、修正をすべて取り消し（`ca57785` に復帰）。

**正本 qmd**: `ca57785` = `git rev-parse ca57785`  
**リモート**: `origin/branch-3` を `ca57785` に合わせ済み（要 `git pull` on other PCs）

---

## 手動コミット時の記録テンプレ（No. 完了ごとに追記）

```markdown
## No.XX (exec N/32)

- commit: `<hash>`
- 変更範囲: （例: Abstract 1段落）
- MQ: （鉄則番号を列挙。例: 鉄則1 短文化、鉄則10 significant のみ）
- DATA: （数値を触った場合のみ 正本パス）
- UTF-8: pass
```

---

（以下、手動コミットごとに追記）

---

## No.21（exec 1/32）— エージェント草案（未コミット・要確認）

- **変更範囲**: Introduction（仮説・研究目的）、Methods §2、Abstract 1文（手術率用語のみ）
- **MQ**: 鉄則1（長文分割）、鉄則3（We obtained / We extracted）、鉄則6（may be associated）、鉄則11（能動態）
- **DATA**: 数値新規なし；total の定義は3部位合算（既存 Table 1 構成と整合）
- **UTF-8**: pass（`_verify_utf8_qmd.py`）
- **残作業（No.22以降）**: Results/Discussion 内の `fracture rate` 表記は未一括置換（意図的に No.21 範囲外）

**コミット例**: `No.21 (exec 1/32): Eguchi proxy terminology and surgery-rate framing (Intro, Methods §2)`

---

## No.22（exec 2/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（解析目的の明示）
- **MQ**: 鉄則1（OLS 文を分割）、鉄則4（We used … at 文頭）、鉄則11（能動態）；JAMA Objective 要素
- **DATA**: 調整変数・モデルは ca57785 / Methods と整合（数値変更なし）
- **UTF-8**: pass
- **意図的に未変更**: HC3/bootstrap の削除（No.2）、Abstract 全体の平易化（No.1 以降）

---

## No.1（exec 3/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（山1：平易化・マクロストーリー）
- **MQ**: 鉄則1（セミコロン連結を短文化）、2（burden/imposes→place a heavy burden）、4（We studied / We linked）、5（hip fracture を文頭）、11（能動態）
- **DATA**: 数値・β・*p*・HC3・*B*=5000 は ca57785/Table 照合値のまま
- **UTF-8**: pass
- **体裁**: Abstract は単一段落のまま（H&P 向け）
- **意図的に未変更**: HC3/bootstrap 削除（No.2）、OLS/β の言い換え（No.3）、年間 per 100,000（No.4）、Main Findings 調（No.5）、調整変数の追加説明（No.6）、末尾簡潔化（No.7）

---

## No.2（exec 4/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（山2：HC3・bootstrap・OLS 頑健性の記述削除）
- **削除**: `We fitted OLS…`, `HC3… (*B* = 5000)`, `HC3 and bootstrap intervals… borderline`, `conventional standard errors`（HC3 との対比句）
- **MQ**: 鉄則1（統計細部の削減）、2（冗長な頑健性列挙の除去）
- **DATA**: 主解析の β・CI・*p* は変更なし；感度分析の詳細は本文・Table 3 脚注に残置
- **UTF-8**: pass
- **意図的に未変更**: β/OLS の平易化（No.3）、末尾の *N*=47 注意（No.7 で整理可）

---

## No.3（exec 5/32）— エージェント草案（未コミット）【山3・再実施】

- **前提**: qmd を **No.2 コミット `3552974`** の状態に戻した（誤って実施していた山5＝β 平易化は取り消し）
- **変更範囲**: Abstract のみ（**山3**：`8.57 degrees (SD 3.16)` の意味説明）
- **置換（康永推奨案・2文）**: `Across prefectures, the mean terrain slope was 8.57 degrees (SD, 3.16). Slopes ranged from 1.81 to 15.43 degrees, reflecting how steep residential land is in each prefecture.`
- **MQ**: 鉄則1（分割）・2・4・7・11
- **DATA**: 8.57, 3.16, 1.81, 15.43 は本文 Table 1 と同一
- **UTF-8**: （コミット前に検証）
- **意図的に未変更**: β 記法（**山5** → Checklist No.5）、年間 per 100,000（山4）、県名（山25）

---

## No.4（exec 6/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（**山4**：per 100,000 ＝ 年間・人口10万人当たりか）
- **置換**: (1) `Annual fracture surgery rates (per 100,000 population per year)`＋Reiwa 5 期間 (2) `The mean annual hip fracture surgery rate was 254.0 per 100,000 population`
- **MQ**: 鉄則1・4（The mean… was）；鉄則2（Methods §2 の annual rates と用語整合）
- **DATA**: 254.0・SD 37.6・令和5年度は変更なし（Methods §2: annual rates per 100,000）
- **UTF-8**: pass
- **意図的に未変更**: Methods §2（既に annual と明記）、β 平易化（山5）

---

## No.5（exec 7/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（**山5**：`β = 5.65` / `β = 3.49` → Discussion Main Findings 調）
- **置換**: 約5.7件・約3.5件 per 100,000 population per degree；CI・*p* は Table 3 のまま
- **MQ**: 鉄則1・4（Steeper terrain was / each additional degree corresponded）；鉄則5（hip fracture を文頭）；鉄則2（unadjusted models 削除）
- **DATA**: 5.65→5.7、3.49→3.5 は丸めのみ；No.4 の annual per 100,000 population と整合
- **UTF-8**: pass
- **意図的に未変更**: 調整変数の列挙（山6）、抄録末尾（山7）

---

## No.6（exec 8/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（**山6**：調整後結果に調整変数を明示）
- **置換**: `After covariate adjustment` → `After adjustment for aging rate, fast walking rate, and population density`（Methods Model 2 と整合）
- **MQ**: 鉄則4（After adjustment… each additional degree）；鉄則2（covariate adjustment の曖昧語を具体化）
- **DATA**: 調整変数セットは Table 3 Model 2 と同一
- **UTF-8**: pass
- **意図的に未変更**: `before covariate adjustment`（未調整側は山6のハイライト外）、aging rate 用語（山10）

---

## No.7（exec 9/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（**山7**：末尾簡潔化・hip 特異メッセージ）
- **削除**: lateral-fall mechanisms、`inferential sensitivity at small ecological *N*`（本文へ）
- **置換**: `The association was specific to hip fracture surgery rates and was not observed for humerus or forearm fracture surgeries.`
- **MQ**: 鉄則1・5（hip を文頭）；鉄則2（重複する2文を1文に）；鉄則6（過剰な方法論的留保を Abstract から除去）
- **UTF-8**: pass
- **意図的に未変更**: 居住フレーミング（山23）、山21–22 の追加 polish（No.16–17）

---

## No.16（exec 10/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（**山21**：Discussion Main Findings 調の結果記述）
- **置換**: 調整前後を `each additional degree of slope corresponded to approximately X…` で平行化；調整後に `terrain slope was positively associated with annual hip fracture surgery rates` を追加（Discussion §1 と同趣旨）
- **MQ**: 鉄則1（短文分割）・4・5；鉄則2（`those covariates` で調整変数の反復を抑制）
- **DATA**: 5.7・3.5・CI・*p* 不変
- **UTF-8**: pass
- **意図的に未変更**: 末尾 hip 特異文（No.7）、`under the primary OLS parameterization`（Abstract では不入）
- **意図的に未変更**: 山22 向け部位特異の追加（No.17 で差分があれば最小限）

---

## No.17（exec 11/32）— エージェント草案（未コミット）

- **変更範囲**: Abstract のみ（**山22**：部位特異の書き方を Discussion §1 に合わせる）
- **置換**: `The association` → `The adjusted association`；`fracture surgeries` → `fracture surgery rates`（対称）
- **参照**: Discussion「The adjusted association was specific to hip fractures and was not observed for humerus or forearm fractures.」
- **MQ**: 鉄則4・5；鉄則2（調整後であることを明示）
- **UTF-8**: pass
- **意図的に未変更**: 結果3文（No.16 済み）、fracture vs surgery の全文統一（江口 No.21 済み部分のみ Abstract 内）

---

## No.10（exec 12/32）— エージェント草案（未コミット）

- **変更範囲**: Methods **§5 Additional Covariates のみ**（**山10**）
- **置換**: `Aging rate (proportion of individuals aged ≥65 years, %)` → `The proportion of individuals aged ≥65 years (%)`（定義文1文）
- **MQ**: 鉄則4（老年人口割合の定義を誤解しない表現）；鉄則2（共変量ラベル `aging rate` は Abstract・Results・表・Discussion では維持）
- **DATA**: 不変
- **UTF-8**: pass
- **意図的に未変更**: 全文の `aging rate` / `Aging rate` / `## 4. Role of Aging Rate`（**山15** = No.12 で rate vs proportion を検討）

---

## No.12（exec 13/32）— エージェント草案（未コミット）

- **変更範囲**: Methods（§4–§6）・Results・Discussion・Conclusions・表・Abstract（**山15**：単なる割合の `rate` → `proportion`）
- **置換**:
  - `aging rate` / `Aging rate` → `proportion aged ≥65 years` / `Proportion aged ≥65 years`（§5 定義文は No.10 済みのまま）
  - `fast walking rate` → `fast-walking proportion`；Methods §4 は `proportion with fast habitual walking`
  - 表1–4・Table 2 行列ラベルを同期；Discussion §4 見出し `Proportion Aged ≥65 Years`
- **MQ**: 鉄則4（疫学用語：割合と発生率の区別）
- **DATA**: 不変
- **UTF-8**: pass
- **意図的に未変更**: `fracture surgery rate`・`surgery rate`・`rate of elevation change`・`national age-specific surgery rates`・`compositional aging` / `rural aging`（一般語）

---

## No.11（exec 14/32）— エージェント草案（未コミット）

- **変更範囲**: Methods §6 末尾・図生成1文のみ（**山14**：PDF コメントは括弧内に限定）
- **削除**: `(not by image-generative AI tools)` のみ
- **置換後**: `…generated programmatically from study data using reproducible Python workflows…`（パッケージ列挙・Figure 1–5 の手順は維持）
- **MQ**: 鉄則2（指摘箇所のみ修正；過剰削除を回避）
- **UTF-8**: pass
- **意図的に未変更**: 文末の AI 利用開示セクション（図は生成AI未使用の明示はそちらで維持）
- **注**: 初版草案で長文全体を可用性1文に差し替えていたが、PDF 突合のうえ括弧削除に限定

---

## No.13（exec 15/32）— エージェント草案（未コミット）

- **変更範囲**: Results §2・Figure 凡例・埋め込み・Methods 図生成1文（**山16**：Table 2 と重複する Figure 2 削除）
- **削除**: Figure 2（相関ヒートマップ）の本文言及・凡例・`heatmap_correlation.png` 埋め込み
- **繰り下げ**: 旧 Figure 3–5 → **Figure 2–4**（地図3枚）
- **Results §2**: Table 2 で相関を提示、Figure 1 で主要 exposure–outcome のみ図示；fast-walking の *p* = 0.073（Table 2 の *r* = −0.264、*N* = 47 と整合）
- **MQ**: 鉄則2（Table と Figure の役割分担）
- **UTF-8**: pass
- **意図的に未変更**: §3 見出し「Primary Regression…」（No.14 以降）；解析スクリプト・図ファイル名（提出時は Figure_2–4 として地図を指定）

---

## No.23（exec 16/32）— エージェント草案（未コミット）（山23）

- **PDF 再確認**（`Manuscript_slope_fracture_20260425_saito0430-1.pdf` / `_yamagishi_highlights.txt` word_id=162）:
  - ハイライト: `steeper habitable terrain`
  - コメント: 「**そのような県に住んでいること**、との関連という方がこの研究の特徴を表せる」
- **番号メモ**: 山岸表の **No.18 = 山23**（Discussion）。整合順の **Checklist No.23** は江口・Methods 副次解析（別項目）— 本コミットは **山23 のみ**
- **変更範囲**: Discussion §1 Main Findings の締め1文のみ
- **置換**: `steeper habitable terrain may track … at the population level` → `residence in prefectures with steeper habitable terrain may be associated with … at the prefecture level`（県単位生态学の解釈を明示）
- **MQ**: 鉄則4・5（研究デザインと整合した framing）；鉄則2（過剰な Main Findings 全面書き換えは No.18 相当の別コミットとして回避）
- **UTF-8**: pass
- **意図的に未変更**: Comparison 節の dose-response 記述；Biological Plausibility の地形メカニズム（No.19 山29 で車利用を別途）

---

## No.26（exec 17/32）— エージェント草案（未コミット）

- **変更範囲**: Discussion §5（江口：地形–fast-walking の相関 *p* 追記）
- **確認**: Results §2 は No.13 済み `(r = −0.264, *p* = 0.073)`（Table 2 と整合）
- **置換**: Discussion の `(r = −0.264)` → `(r = −0.264, *p* = 0.073)`（正本・匿名版）
- **DATA**: *r*・*p* は Table 2（*N* = 47）と一致；α = 0.05 では非有意である旨は Results の “weak negative” で既出のため Discussion では *p* 値のみ追記
- **UTF-8**: pass
- **意図的に未変更**: Table 2 行列の個別 *p* 脚注；humerus/forearm の *r* = 0.138・0.177

---

## No.14（exec 18/32）— エージェント草案（未コミット）（山17）

- **PDF 再確認**（word_id=150）:
  - ハイライト: **`(both intervals include null)` のみ**
  - コメント: 「これは必要ですか？」
  - **採用方針**: 括弧句のみ削除（残差診断・Shapiro・HC3/bootstrap の段落全体は維持）
- **変更範囲**: Results §3・Model 2 直後の感度1文（正本 qmd のみ；匿名版は当該段落なし）
- **置換**: `…was −0.03 to 7.09 (both intervals include null).` → `…was −0.03 to 7.09.`
- **康永 MQ**: 鉄則2（CI と *p* = 0.063 でヌル含有は読者が判断可能なため冗長）；鉄則6（「inferential fragility」は維持）
- **DATA**: HC3・bootstrap の区間・*p* 不変
- **UTF-8**: pass
- **意図的に未変更**: Limitations §8・Conclusions の borderline 記述；Table 3 脚注；No.14 旧案の感度段落全面削除・小見出し分割（No.27）

---

## No.15（山19）— エージェント草案（未コミット）

- **PDF 再確認**（word_id=152）: ハイライトは Results §3 の間接標準化段落（`"-"` 表記）。コメント「秘匿セルを0と仮定したとき」など**言葉で説明**。
- **寳澤先生**: 間接標準化の提案は既にユーザー追記済み。No.15 は**マスキング記号の平易化**と表記統一（ISR→indirectly standardized rate、*p* 体裁）に限定。
- **変更範囲**: Methods §6（開示抑制の説明）、Results §3（間接標準化段落）、Table 5、Limitations 第5点、匿名版同期
- **康永 MQ**: 鉄則1・2（短文、`"-" = 0` を prose に）；鉄則4（主語・動詞を前に）；鉄則6（sensitivity only／replacement assumption で断定を抑制）
- **DATA**: Table 5 の β・CI・*p* は変更なし（5.71/3.61/3.64 等）
- **UTF-8**: pass
- **意図的に未変更**: 寳澤提案の分析手順そのもの（既存）；Discussion の間接標準化解釈段落（別コミット可）

---

## 2026-05-19: チェックリスト訂正（PDF・DOCX 再突合）

- **正本**: `Manuscript_slope_fracture_20260425_saito0430-1.pdf` の [山1]–[山31] 表記
- **訂正要点**:
  - **山3** = `8.57 degrees (SD 3.16)` の意味説明（旧 No.3「OLS/β」と不一致）
  - **山5** = `β = 5.65` の平易化（Discussion 調）→ 手動コミット「No.3」で実施済みの内容は **山5** に相当
  - **山14** = Methods の `(not by image-generative AI tools)` 不要（旧 No.11「Methods 短縮」と不一致）
- **未対応**: **山3**（平均傾斜の説明）は次コミットで対応（整合順では Checklist **No.3** として再定義）
- 詳細: `itemized_revision_checklist_branch3.md` 山岸表を全面差し替え
