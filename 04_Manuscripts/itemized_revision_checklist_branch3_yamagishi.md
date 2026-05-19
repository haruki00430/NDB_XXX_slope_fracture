# Itemized Revision Checklist (branch-3: 山岸先生)

対象コメント正本: `Manuscript_slope_fracture_20260425_saito0430-1.docx` / `.pdf`（Word コメント ID: **山1〜山31**）  
対象原稿（修正先）: `Manuscript_slope_fracture.qmd`（必要に応じ `Manuscript_slope_fracture_anonymous.qmd` を同期）  
ベースライン: 佐藤・寳澤・島袋コメント反映済み版（`saito0430-1`）。舟久保先生ラウンド（branch-2）の qmd 反映状況は項目着手前に差分確認すること。

運用: **1 checklist 行 = 1 commit** → push → `itemized_revision_log_branch3_yamagishi.md` 追記 → SKILL 準拠確認

## 推奨着手順（セクション依存のため）

1. **No.1〜7**（Abstract 全体）→ **No.16〜17**（Abstract と Discussion の整合）  
2. **No.12**（rate / proportion 用語；全文に波及しうる）  
3. **No.10〜11, 13〜15**（Methods / Results）  
4. **No.8〜9**（Introduction / Discussion・Conclusions の意義）  
5. **No.18〜20**（Discussion / Strengths）

---

| No. | 山ID | 指摘事項（要約） | 対応方針 | 主な修正セクション | 状態 | commit |
|-----|------|------------------|----------|-------------------|------|--------|
| 1 | 山1 | Abstract が難解。統計に詳しくない読者にも分析のイメージが伝わるよう、**本文トーンに寄せて**重要メッセージをストレートに | Abstract を平易化・再構成（IMRAD 抄録体ではなく読みやすい 1 段落） | Abstract | Pending | |
| 2 | 山2 | 感度分析（HC3・bootstrap）の記述は Abstract に不要 | Abstract から感度分析の細部を削除（本文・Table 脚注へ） | Abstract | Pending | |
| 3 | 山3 | 「これ」（OLS / β 等）の意味がわかりにくい | Abstract で回帰・係数を平易に言い換え、または最小限の説明を追加 | Abstract | Pending | |
| 4 | 山4 | per 100,000 が**年間**かどうか不明 | 分母・期間（令和5年集計＝年間 per 100,000 等）を明示 | Abstract; Methods §2 | Pending | |
| 5 | 山5 | 一部の統計表現がわかりにくい。**Discussion の言い方の方が明確** | Abstract の結果記述を Discussion Main Findings に近い表現へ | Abstract | Pending | |
| 6 | 山6 | 調整した変数が Abstract だけでは伝わらない | 調整共変量（高齢者割合・速歩・人口密度）を Abstract に明記 | Abstract | Pending | |
| 7 | 山7 | Abstract 末尾の慎重表現・細部は不要。核心は「**傾斜が急い県で大腿骨骨折手術が多く、上腕・前腕では関係ない**」 | Abstract 結論を hip 特異性中心に簡潔化。過度な inferential sensitivity 文言は本文へ | Abstract | Pending | |
| 8 | 山8 | 傾斜地＝足腰が鍛えられる／逆に**車利用が増える**という別メカニズムの言及 | Introduction（仮説・先行研究の直後）に competing mechanisms を短く追記 | Introduction | Pending | |
| 9 | 山9 | 県レベル集計の代表性（山岳県の平野居住）— Limitation だけでなく**研究意義**を Discussion または Conclusions で強調 | Discussion または Conclusions に ecological N=47 の意義・政策示唆を追記 | Discussion; Conclusions | Pending | |
| 10 | 山10 | 「aging rate」が年間の高齢化進行に読める。**proportion aged ≥65 years** のみでよい | Methods §5・全文で用語統一（Table キャプション含む） | Methods; 全文 | Pending | |
| 11 | 山14 | Methods 末尾の**再現性・ソフトウェア詳細段落**は不要では | ジャーナル要項と照合し、過剰なら Data availability / 補足へ移すか短縮 | Methods | Pending | |
| 12 | 山15 | 疫学の **rate**（時間単位）と単純割合の混同。**proportion** を使うべき箇所を整理 | fast walking 等は proportion に。手術は incidence rate（per 100,000/year）と定義を明示 | Methods; Results; Tables | Pending | |
| 13 | 山16 | Results §2 の相関記述と **Table 2** が重複。どちらかに集約 | 本文を要約に留め Table 2 を参照、または §2 を削減 | Results §2 | Pending | |
| 14 | 山17 | Results の **HC3・bootstrap・残差診断**段落は必要か | 主結果は Table 3 に集約し、本文は 1〜2 文に圧縮するか Limitations へ移すか判断 | Results §3 | Pending | |
| 15 | 山19 | マスキング `"-"` の意味が不明。「秘匿セルを 0 と仮定したとき」等、**読者向けに各シナリオを言い換え** | Results（ISR 感度分析）; Methods（既存手順の平易化） | Results; Methods | Pending | |
| 16 | 山21 | Abstract も Discussion Main Findings のような書き方が理解しやすい | No.1・5・7 と統合して Abstract を Main Findings 調に改稿 | Abstract | Pending | |
| 17 | 山22 | 上記と同趣旨（Biological plausibility 冒頭付近のコメント） | No.16 と同一コミット可。別コミットの場合は Abstract 最終調整のみ | Abstract | Pending | |
| 18 | 山23 | 「傾斜そのもの」より**「そのような県に住むこと」との関連**が研究の特徴 | Discussion Main Findings / Conclusions のフレーミングを residence in steeper prefectures へ | Discussion; Conclusions | Pending | |
| 19 | 山29 | **自動車利用**の影響が Discussion にない（地方・高齢・傾斜地では車依存） | Discussion（Limitations または Walking speed 節）に car reliance / unmeasured confounding を追記。追加解析は別途判断 | Discussion; Limitations | Pending | |
| 20 | 山31 | Strengths の「internal evidence consistent with mechanism」は**根拠なし言い過ぎ** | Strengths の表現を控えめに（suggestive / consistent with が妥当な範囲へ） | Discussion §7 Strengths | Pending | |

---

## コメント全文インデックス（山岸先生のみ）

| 山ID | コメント原文（抜粋） | PDF 目安 |
|------|----------------------|----------|
| 山1 | abstract が難解。本文の書き方を持ってくる。重要メッセージをストレートに | p.1 |
| 山2 | 感度分析の話は abstract には不要 | p.1 |
| 山3 | これが何を意味するのかわかりにくい（説明必要） | p.1 |
| 山4 | 年間10万人当たりという意味ですか？ | p.1 |
| 山5 | Discussion の表現の方がわかりやすい | p.1 |
| 山6 | 何で調整したのかも書く必要 | p.1 |
| 山7 | 抄録最後の細かい話は不要。傾斜が強い県で股関節のみ関連、を明確に | p.2 |
| 山8 | 坂で足腰が鍛えられる／車を使う人が多いのでは | p.3 |
| 山9 | 県レベルで十分か。意義を discussion または conclusion で | p.3 |
| 山10 | aging rate → proportion aged ≥65 years のみでよいのでは | p.5 |
| 山14 | 再現性・ソフトウェア列挙段落は不要では | p.7 |
| 山15 | rate vs proportion（ほかも同様） | p.8 |
| 山16 | Table 2 と何が違うか。どちらかだけでよい | p.8 |
| 山17 | HC3・bootstrap 段落は必要ですか | p.9 |
| 山19 | `"-"` の意味。秘匿セルを 0 と仮定したとき、等と書く | p.9 |
| 山21 | abstract も Main Findings のような書き方がよい | p.10 |
| 山22 | 同上（abstract をこのように） | p.10 |
| 山23 | 「そのような県に住んでいること」との関連が特徴 | p.10 |
| 山29 | 車の影響が考察されていない | p.14 |
| 山31 | Strengths が根拠なし言い過ぎ | p.16 |

**注**: 山11〜13・18・20・24〜28・30 等は **治齋**（既反映済みコメント）のため本 checklist には含めない。

---

## 着手前チェック（毎回）

- [ ] `Manuscript_slope_fracture.qmd` が branch-2（舟久保）最新か `git log` / diff で確認
- [ ] 修正後: Abstract ↔ Conclusions の主張強度一致
- [ ] `.claude/skills/manuscript-writing-quality/SKILL.md` で Fool-proof English 確認
- [ ] 匿名版 qmd へ同一修正を同期（該当セクションがある場合）
