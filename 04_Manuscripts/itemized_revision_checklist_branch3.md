# Itemized Revision Checklist (branch-3: 山岸・江口)

対象コメント正本:

- 山岸: `Manuscript_slope_fracture_20260425_saito0430-1.docx` / `.pdf`（Word ID: **山1〜山31**、治齋除く）
- 江口: [【江口先生コメント】.md](【江口先生コメント】.md)

対象原稿: `Manuscript_slope_fracture.qmd`（同期: `Manuscript_slope_fracture_anonymous.qmd`）  
ベースライン: `branch-2` HEAD（舟久保 No.16–17、Table 5、SIR 用語反映済み）

運用: **1 checklist 行 = 1 commit**（複数行は「推奨 Commit」列で束ね）→ push → `itemized_revision_log_branch3.md` 追記 → Skills / H&P ゲート

準拠: Health & Place 投稿規定、`manuscript-writing-quality`、`manuscript-revision`（Gemini g260519 ①–④は**参照のみ・コピペ禁止**）

## 推奨コミット順

| Phase / Commit | No. |
|----------------|-----|
| 0 | （本ファイル・ログ作成） |
| 1 | 21 |
| 2 | 1–7, 16–17, 22 |
| 3 | 12, 30（一部） |
| 4 | 10 |
| 5 | 11, 23, 24 |
| 6 | 13, 26 |
| 7 | 14, 15, 27 |
| 8 | 25 |
| 9 | 8 |
| 10 | 29 |
| 11 | 9, 18, 19, 28, 30 |
| 12 | 7, 20, 31 |
| 13 | 32 |
| 14 | H&P 提出準備（語数再計測・相談後削減） |

---

## A. 山岸先生（No.1–20）

| No. | 先生 | 元ID | 指摘要約 | 対応方針 | 主な修正セクション | 推奨 Commit | Gemini | Skills | 状態 | commit |
|-----|------|------|----------|----------|-------------------|-------------|--------|--------|------|--------|
| 1 | 山 | 山1 | Abstract が難解。重要メッセージをストレートに | 平易な 1 段落（≤250 words）；本文トーンに寄せる | Abstract | 2 | ① 構成のみ | MQ, MR, H&P | Pending | |
| 2 | 山 | 山2 | HC3・bootstrap は Abstract に不要 | 感度分析の細部を削除（本文・Table 脚注へ） | Abstract | 2 | ① | MQ, MR, H&P | Pending | |
| 3 | 山 | 山3 | OLS / β 等の意味が不明 | 回帰・係数を平易に言い換え | Abstract | 2 | ① | MQ, MR | Pending | |
| 4 | 山 | 山4 | per 100,000 が年間か不明 | 令和5年・年間 per 100,000 を明示 | Abstract; Methods §2 | 2 | — | MR | Pending | |
| 5 | 山 | 山5 | Discussion の表現の方が明確 | 結果記述を Main Findings 調に | Abstract | 2 | ① | MQ | Pending | |
| 6 | 山 | 山6 | 調整変数が Abstract で不明 | 高齢者割合・速歩・人口密度を明記 | Abstract | 2 | — | MQ | Pending | |
| 7 | 山 | 山7 | 抄録末尾の細部は不要。股関節特異を明確に | hip 特異中心に簡潔化 | Abstract; Conclusions | 2, 12 | ① | MQ | Pending | |
| 8 | 山 | 山8 | 足腰強化 vs **車利用**の競合メカニズム | Introduction に competing mechanisms を短く追記 | Introduction | 9 | ① | MQ | Pending | |
| 9 | 山 | 山9 | 県レベル集計の**研究意義**を Discussion/Conclusions で | ecological N=47 の意義・政策示唆 | Discussion; Conclusions | 11 | ① | MQ, spatial | Pending | |
| 10 | 山 | 山10 | aging rate → **proportion aged ≥65 years** | 全文で用語統一 | Methods; 全文 | 4 | — | MR | Pending | |
| 11 | 山 | 山14 | Methods 末尾の再現性・ソフトウェア段落が過長 | 短縮または Data availability へ | Methods | 5 | — | MR | Pending | |
| 12 | 山 | 山15 | rate vs proportion の混同 | fast walking は proportion；手術は rate/year と定義 | Methods; Results; Tables | 3 | ③ | MR | Pending | |
| 13 | 山 | 山16 | Results §2 と Table 2 が重複；Figure 2 整理 | §2 を要約化；Figure 2 削除・番号振り直し | Results §2; Figures | 6 | ② | MR | Pending | |
| 14 | 山 | 山17 | HC3・bootstrap・残差診断段落 | 本文 1–2 文＋ Table 3 脚注 | Results §3 | 7 | ② | MQ | Pending | |
| 15 | 山 | 山19 | マスキング `"-"` の意味不明 | 各シナリオを読者向けに言い換え | Results; Methods; Table 5 | 7 | ② | MR | Pending | |
| 16 | 山 | 山21 | Abstract を Main Findings 調に | No.1–7 と統合（Commit 2） | Abstract | 2 | ① | MQ | Pending | |
| 17 | 山 | 山22 | 上記と同趣旨 | Commit 2 に統合 | Abstract | 2 | ① | MQ | Pending | |
| 18 | 山 | 山23 | **居住**（そのような県に住むこと）のフレーミング | Discussion / Conclusions の表現を修正 | Discussion; Conclusions | 11 | ④ 骨子のみ | MQ | Pending | |
| 19 | 山 | 山29 | **自動車利用**が Discussion にない | Limitations 等に car reliance を短く追記（追加解析なし） | Discussion; Limitations | 11 | ① | MQ | Pending | |
| 20 | 山 | 山31 | Strengths が言い過ぎ | 控えめな表現へ | Discussion §7 | 12 | — | MQ | Pending | |

## B. 江口先生（No.21–32）

| No. | 先生 | 元ID | 指摘要約 | 対応方針 | 主な修正セクション | 推奨 Commit | Gemini | Skills | 状態 | commit |
|-----|------|------|----------|----------|-------------------|-------------|--------|--------|------|--------|
| 21 | 江 | 江1 | アウトカムは**手術率（proxy）** | 全文で fracture / surgery rate を厳密化；Intro に proxy 1 文 | 全文; Introduction | 1 | ③, ④ 骨子 | MQ, MR | Pending | |
| 22 | 江 | 江2 | Abstract に**解析の目的**不足 | 多変数回帰の目的を明示 | Abstract | 2 | ③ | MQ, MR, H&P | Pending | |
| 23 | 江 | 江3 | Intro 媒介経路 vs Methods/Results のズレ | 副次解析（aging / fast-walking を outcome）を Methods に明記 | Methods §6 | 5 | ③, ④ 骨子 | MQ | Pending | |
| 24 | 江 | 江4 | **全骨折（total）** が Methods に無い | Outcome §2 に total を追記 | Methods §2 | 5 | ④ 骨子 | MR | Pending | |
| 25 | 江 | 江5 | 傾斜 range に**県名** | データ確認のうえ min/max 県を記載 | Results §1 | 8 | — | MR | Pending | |
| 26 | 江 | 江6 | r = −0.264 に **p 値**なし | Table 2 / 本文で統一 | Results §2 | 6 | — | MR | Pending | |
| 27 | 江 | 江7 | 主解析と感度分析が混在 | Primary / Sensitivity 小見出しで分割 | Results §3 | 7 | ③ | MQ | Pending | |
| 28 | 江 | 江8 | Discussion 冒頭に**調整後**明記 | After adjusting for... を β 文の前に | Discussion §1 | 11 | ③ | MQ | Pending | |
| 29 | 江 | 江9 | 新潟・長野・山形がデータと一致するか | 散布図で確認；修正または削除 | Discussion §3 | 10 | — | MR | Pending | |
| 30 | 江 | 江10 | risk factor / hazard は不適切 | environmental correlate 等へ | Discussion; Limitations | 3, 11 | ③ | MQ, spatial | Pending | |
| 31 | 江 | 江11 | Conclusion が結果の繰り返し | OLS・β・p を削減；政策的メッセージ中心 | Conclusions | 12 | ③, ④ 骨子 | MQ | Pending | |
| 32 | 江 | 江12 | 図の文字が小さい；表の改行 | フォント・300 dpi；表列幅調整 | Figures; Tables | 13 | — | H&P | Pending | |

---

## 着手前チェック（毎コミット）

- [ ] `branch-2` / `branch-3` 上で正本 qmd を編集
- [ ] Abstract ↔ Conclusions の主張強度一致
- [ ] `manuscript-writing-quality` / `manuscript-revision` 確認
- [ ] 匿名版 qmd 同期（該当セクション）
- [ ] ログに `SKILL/H&P: pass` 記録

## 字数方針

- branch-3 中は Discussion を先回り一括削減しない
- **Commit 14** で Introduction〜Data availability を再計測し、6,000 超過時はユーザーと相談後に削減
