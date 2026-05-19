# Itemized Revision Checklist (branch-3: 山岸・江口) — **手動コミット運用**

**コメント正本**: `Manuscript_slope_fracture_20260425_saito0430-1.pdf`（右欄の **[山1]…[山31]**）  
**突合ソース**: 同上 PDF のマークダウン化＋`Manuscript_slope_fracture_20260425_saito0430-1_saito0519.docx` の Word コメント（著者「山岸」20件）  
**注意**: PDF の **山番号** と Word 内部 `comment_id` は一致しません。下表の **山ID** を先生への説明用の正本とします。

**ベースライン（正本 qmd）**: `ca57785`  
**運用**:

1. **1 checklist 行 = 手動 1 git commit**（エージェントは次の No. に進まない）
2. 各コミット前に `manuscript-writing-quality` を**当該段落のみ**適用
3. 数値は Gemini 禁止 — `03_Analysis/results/`・Table 1–5・`ca57785` のみ
4. `python 04_Manuscripts/_verify_utf8_qmd.py`
5. **実行順**は下表「整合コミット順」（表の No. 順ではない）

**整合コミット順（32回）**: 21 → 22 → 1 → 2 → … → 32

### 済みコミットと山IDの対応メモ（要確認）

| 済み Checklist No. | 実際に反映した山IDの意図 | 未反映の山ID |
|-------------------|--------------------------|--------------|
| 1 | 山1（Abstract 全体平易化） | — |
| 2 | 山2（Abstract 感度分析削除） | — |
| 3 | **山5**（β の平易化）として実施 | **山3**（8.57°・SD の意味説明）が未対応 |

---

## 山岸先生（No.1–20）— PDF 正本

| No. | 山ID | Word ID | ハイライト（PDF アンカー） | 指摘（要約） | 主な対応箇所 |
|-----|------|---------|---------------------------|--------------|--------------|
| 1 | **山1** | 1 | Abstract 見出し付近 | 抄録が難解。統計に詳しくない読者にも分析のイメージが湧くように。本文より Abstract の方が難解なので**本文の書き方を持ってくる**。重要メッセージをストレートに。 | Abstract |
| 2 | **山2** | 31 | OLS / HC3 / bootstrap 文 | **感度分析の話は細かいので Abstract には不要**では。 | Abstract |
| 3 | **山3** | 35 | `Mean slope was 8.57 degrees (SD 3.16)` | **これが何を意味するのかわかりにくい。説明が必要。**（β ではなく記述統計・傾斜指標の意味） | Abstract |
| 4 | **山4** | 42 | `100,000` | **年間10万人当たりという意味ですか？** | Abstract（必要なら Methods §2） |
| 5 | **山5** | 45 | `β = 5.65` | **意味がよくわからない。Discussion で使われている表現の方がわかりやすい**（例：1度増ごと約3.5件/10万人）。 | Abstract |
| 6 | **山6** | 50 | 調整後の関連文（ハイライト範囲は段落全体） | **これだけでは何かよくわからない。何で調整したのかも書く必要がある。** | Abstract |
| 7 | **山7** | 62 | `inferential sensitivity at small ecological N…` | **抄録の最後でこのようなことは言わない方がよい。** 重要なのは「傾斜が強い県に住む人では股関節骨折手術が多いが、それ以外の骨折は関係ない」が明確に伝わること。細部は本文で。 | Abstract |
| 8 | **山8** | 65 | `chronic deconditioning and increased frailty` | 傾斜地は坂で足腰が鍛えられるのでは？**逆にしんどくて車を使う人が多いのでは？** | Introduction |
| 9 | **山9** | 76 | `prefectural-level` | **県レベルで十分か。** 山は多いが人は平野に住む。**それでも研究を出す意義**を Discussion / Conclusion で強調。 | Introduction; Discussion / Conclusions |
| 10 | **山10** | 119 | `Aging rate` | **老年人口割合のことか。** aging rate だと年間の高齢化進行に見える。**`proportion of individuals aged ≥65 years` だけでよいのでは。** | Methods |
| 11 | **山14** | 142 | `(not by image-generative AI tools)` | **これは不要では？**（図表生成ソフト列挙の冗長部分） | Methods |
| 12 | **山15** | 146 | `rate`（aging rate 等） | 疫学の **rate は単位時間**。単なる割合なら **proportion**。**ほかも同様。** | Methods; Results; 全文用語 |
| 13 | **山16** | 147 | `Figure 2` | **Table 2 と何が違うか。どちらかだけでよいのでは。** | Results; Figure 番号 |
| 14 | **山17** | 150 | `(both intervals include null)` 付近の感度段落 | **これは必要ですか？**（残差診断・Shapiro・HC3/bootstrap の長文） | Results |
| 15 | **山19** | 152 | `"-"` マスキング記述 | **`"-"` が何を意味するかわからない。**「秘匿セルを0と仮定したとき」など**言葉で説明**。 | Results; Table 5 |
| 16 | **山21** | 160 | `Each additional degree… approximately 3.5… per 100,000` | **Abstract もこのような書き方の方が理解されやすい**（Discussion Main Findings 調）。 | Abstract |
| 17 | **山22** | 161 | `specific to hip fractures… humerus or forearm` | **ここも同様に、Abstract をこのように書く方がわかりやすい**（部位特異性）。 | Abstract |
| 18 | **山23** | 162 | `steeper habitable terrain` | **「そのような県に住んでいること」との関連**の方が本研究の特徴を表せる。 | Discussion |
| 19 | **山29** | 219 | `Older adults residing in high-slope regions…` | **車の影響が考察にない。** 地方の傾斜地では高齢者は**ほぼ車**では。 | Discussion |
| 20 | **山31** | 225 | `cost-effective` | **根拠がなければ言い過ぎ。** | Discussion §6 Policy |

**山岸コメントで PDF に存在しない番号**（治齋・他先生のみ）: 山11–13, 山18, 山20, 山24–28, 山30 など。

**旧チェックリストとの主な訂正**:

- No.3 は「OLS/β」ではなく **山3＝8.57° (SD) の説明**。
- No.5 は「Main Findings 調」→ **山5＝β の平易化**（山21 はその具体例の参照）。
- No.11 は「Methods 短縮」→ **山14＝生成AI否定の1文が不要か**。
- No.14 は「主解析 vs 感度分離」→ **山17＝感度・診断段落の要否**（小見出し整理は江口 No.27 と連動）。

---

## 江口先生（No.21–32）

| 実行順 | No. | 先生 | 指摘要約 | 状態 | commit（手動記入） |
|--------|-----|------|----------|------|-------------------|
| 1 | 21 | 江 | fracture/surgery rate・Intro proxy | | |
| 2 | 22 | 江 | Abstract に解析目的 | | |
| 3 | 1 | 山 | 山1 Abstract 平易化 | | |
| 4 | 2 | 山 | 山2 感度分析を Abstract から削除 | | |
| 5 | 3 | 山 | **山3** 平均傾斜 8.57° (SD) の説明 | | |
| 6 | 4 | 山 | 山4 per 100,000 年間明示 | | |
| 7 | 5 | 山 | 山5 β／回帰結果の平易化 | | |
| 8 | 6 | 山 | 山6 調整変数を Abstract に | | |
| 9 | 7 | 山 | 山7 hip 特異・末尾簡潔化 | | |
| 10 | 16 | 山 | 山21 Abstract トーン（3.5件/10万） | | |
| 11 | 17 | 山 | 山22 部位特異を Abstract に | | |
| 12 | 10 | 山 | 山10 proportion aged ≥65 years | | |
| 13 | 12 | 山 | 山15 rate vs proportion | | |
| 14 | 11 | 山 | 山14 Methods 冗長文（AI否定） | | |
| 15 | 23 | 江 | Methods 副次解析明記 | | |
| 16 | 24 | 江 | total fracture（Methods） | | |
| 17 | 13 | 山 | 山16 Results・Figure 2 削除 | | |
| 18 | 26 | 江 | r=−0.264 の *p* | | |
| 19 | 14 | 山 | 山17 感度・診断段落の整理 | | |
| 20 | 27 | 江 | 小見出し分割（No.14 と整合） | | |
| 21 | 15 | 山 | 山19 Table 5 マスキング平易化 | | |
| 22 | 25 | 江 | 傾斜 range に県名 | | |
| 23 | 8 | 山 | 山8 Intro 競合メカニズム（車） | | |
| 24 | 29 | 江 | 新潟・長野の事実確認 | | |
| 25 | 9 | 山 | 山9 県レベル研究意義 | | |
| 26 | 18 | 山 | 山23 居住フレーミング | | |
| 27 | 19 | 山 | 山29 Discussion に車利用 | | |
| 28 | 28 | 江 | Discussion 冒頭・調整後 | | |
| 29 | 30 | 江 | environmental correlate | | |
| 30 | 20 | 山 | 山31 Strengths／Policy 控えめ | | |
| 31 | 31 | 江 | Conclusions 政策中心 | | |
| 32 | 32 | 江 | 図フォント・300 dpi | | |

**自動一括コミット（`run_branch3_itemized_commits.py`）は使用しない。**

**参照ファイル（抽出ログ）**: `_yamagishi_highlights.txt`（ハイライト付き）、`_yamagishi_comments_saito0519.txt`
