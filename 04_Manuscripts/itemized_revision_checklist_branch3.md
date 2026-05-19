# Itemized Revision Checklist (branch-3: 山岸・江口) — **手動コミット運用**

**ベースライン（正本）**: `ca57785`（`Manuscript_slope_fracture.qmd`）  
**運用（2026-05-19 改定）**:

1. **1 checklist 行 = あなたが手動で 1 git commit**（エージェントは次の No. に進まない）
2. 各コミットの**直前に** [manuscript-writing-quality/SKILL.md](../../../.claude/skills/manuscript-writing-quality/SKILL.md) を読み、**当該段落だけ** Fool-proof English（鉄則1–12 等）を適用してから保存
3. 数値は Gemini 禁止 — `03_Analysis/results/`・Table 1–5・`ca57785` の既存値のみ
4. コミット前後: `python 04_Manuscripts/_verify_utf8_qmd.py`（UTF-8 ゲート）
5. **実行順**は下表（No.1→32 の表順ではない）

**整合コミット順（32回）**: 21 → 22 → 1 → 2 → … → 32（プラン v2 正本）

| 実行順 | No. | 先生 | 指摘要約 | 状態 | commit（手動記入） |
|--------|-----|------|----------|------|-------------------|
| 1 | 21 | 江 | fracture/surgery rate・Intro proxy | Pending | |
| 2 | 22 | 江 | Abstract に解析目的 | Pending | |
| 3 | 1 | 山 | Abstract 平易化 | Pending | |
| 4 | 2 | 山 | Abstract から HC3/bootstrap 削除 | Pending | |
| 5 | 3 | 山 | OLS/β の平易化 | Pending | |
| 6 | 4 | 山 | per 100,000 年間明示 | Pending | |
| 7 | 5 | 山 | Main Findings 調 | Pending | |
| 8 | 6 | 山 | 調整変数を Abstract に | Pending | |
| 9 | 7 | 山 | hip 特異・末尾簡潔化 | Pending | |
| 10 | 16 | 山 | Abstract トーン | Pending | |
| 11 | 17 | 山 | 上記と同趣旨 | Pending | |
| 12 | 10 | 山 | proportion aged ≥65 years | Pending | |
| 13 | 12 | 山 | rate vs proportion | Pending | |
| 14 | 11 | 山 | Methods ソフト列挙短縮 | Pending | |
| 15 | 23 | 江 | Methods 副次解析明記 | Pending | |
| 16 | 24 | 江 | total fracture（Methods） | Pending | |
| 17 | 13 | 山 | Results §2・Figure 2 削除 | Pending | |
| 18 | 26 | 江 | r=−0.264 の *p* | Pending | |
| 19 | 14 | 山 | 主解析 vs 感度分離 | Pending | |
| 20 | 27 | 江 | 小見出し分割確認 | Pending | |
| 21 | 15 | 山 | Table 5 マスキング平易化 | Pending | |
| 22 | 25 | 江 | 傾斜 range に県名 | Pending | |
| 23 | 8 | 山 | Intro 競合メカニズム（車） | Pending | |
| 24 | 29 | 江 | 新潟・長野の事実確認 | Pending | |
| 25 | 9 | 山 | 県レベル研究意義 | Pending | |
| 26 | 18 | 山 | 居住フレーミング | Pending | |
| 27 | 19 | 山 | Discussion に車利用 | Pending | |
| 28 | 28 | 江 | Discussion 冒頭・調整後 | Pending | |
| 29 | 30 | 江 | environmental correlate | Pending | |
| 30 | 20 | 山 | Strengths 控えめ | Pending | |
| 31 | 31 | 江 | Conclusions 政策中心 | Pending | |
| 32 | 32 | 江 | 図フォント・300 dpi | Pending | |

**自動一括コミット（`run_branch3_itemized_commits.py`）は使用しない。**
