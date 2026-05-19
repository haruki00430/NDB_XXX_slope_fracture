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

## 2026-05-19: チェックリスト訂正（PDF・DOCX 再突合）

- **正本**: `Manuscript_slope_fracture_20260425_saito0430-1.pdf` の [山1]–[山31] 表記
- **訂正要点**:
  - **山3** = `8.57 degrees (SD 3.16)` の意味説明（旧 No.3「OLS/β」と不一致）
  - **山5** = `β = 5.65` の平易化（Discussion 調）→ 手動コミット「No.3」で実施済みの内容は **山5** に相当
  - **山14** = Methods の `(not by image-generative AI tools)` 不要（旧 No.11「Methods 短縮」と不一致）
- **未対応**: **山3**（平均傾斜の説明）は次コミットで対応（整合順では Checklist **No.3** として再定義）
- 詳細: `itemized_revision_checklist_branch3.md` 山岸表を全面差し替え
