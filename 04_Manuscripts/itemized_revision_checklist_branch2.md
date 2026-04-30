# Itemized Revision Checklist (branch-2)

対象コメント正本: `comment_response_checklist_slope_fracture_20260430.md`（No.1〜12）  
対象原稿: `Manuscript_slope_fracture.qmd`

| No. | 指摘事項（要約） | 状態 | 反映箇所メモ | commit |
|---|---|---|---|---|
| 1 | 高齢化率・歩行速度の位置づけ（交絡/媒介） | Done | MethodsのModel定義直下に「confounder-adjustment variables」明記 | No.1 commit |
| 2 | サンプルサイズとモデル安定性（N=47） | Done | Methodsにsmall-Nでの係数安定性/多重共線性診断への言及を追記 | No.2 commit |
| 3 | アウトカムは発症でなく手術率 | Done | Limitationsに「surgery rates rather than true fracture incidence」を追記 | No.3 commit |
| 4 | 未調整交絡（気候・医療資源） | Done | Limitationsの未測定交絡にclimate（snowfall and icing）を明記 | No.4 commit |
| 5 | 空間相関の可能性 | Done | 大平先生方針（今回は無視でOK）に基づき本文変更なしを明示 | No.5 commit |
| 6 | 線形性仮定 | Done | 大平先生方針（今回は無視でOK）に基づき本文変更なし | No.6 commit |
| 7 | 曝露指標（都道府県平均傾斜）の粗さ | Done | Limitationsに「prefecture as a whole / does not capture micro-scale terrain variations」を既記載確認（本文追記なし） | No.7 commit |
| 8 | 年齢構成不一致（歩行速度40–74 vs 骨折高齢） | Done | Discussion/Limitationsに「40–74のみ公開」「直接影響は限定的」「限界明記」を追記（唯一表現の誤解回避に微修正済み） | No.8 commit + No.8 wording-fix commit |
| 9 | 年齢標準化不足（粗率） | Done | No.12と同時処理で、Methods/Results/Discussion/Limitationsに補完前提SIR/ISR感度分析を追記 | No.12+9 combined commit |
| 10 | 結果解釈の強さ（因果を弱める） | Done | Discussion/Conclusionsで demonstrated→showed, remained→was, amplifying→potentially amplifying に調整 | No.10 commit |
| 11 | biological plausibility文が断定的 | Done | Discussion 2の冒頭文を may / partly supported / suggested / potentially に調整 | No.11 commit |
| 12 | 高齢化率調整のみでは不十分（80歳以上等） | Done | No.9と同時に、マスキング補完シナリオ（0/5/9）による間接法SIR/ISR感度分析の結果と解釈制約を明記 | No.12+9 combined commit |
