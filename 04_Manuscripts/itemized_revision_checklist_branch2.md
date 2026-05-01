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
| 13 | 傾斜指標の解釈（個人曝露との乖離） | Done | 大平先生回答に従い今回は本文変更なし（査読者指摘時に対応）。ログ更新のみ実施 | No.13 commit |
| 14 | 行動・生活環境の影響（地域特性・交絡） | Done | 医療アクセス/残余交絡は既対応済み。地域構造指標の追記は論理一貫性の観点で今回は見送り（本文変更なし） | No.14 commit |
| 15 | 追加解析提案（自動車保有率・歩数など） | Done | 大平先生回答に従い主解析への追加感度分析は見送り（本文変更なし）。必要時は査読対応で検討 | No.15 commit |
| 16 | 歩行速度の解釈（能力と曝露の差） | Done | Limitationsに「fast-walkingは能力指標であり歩行量/坂道曝露の直接代理ではない」を1文追記（匿名版にも同期） | No.16 commit |
| 17 | 統計的解釈（控えめ表現・N=47） | Done | Conclusions等で「suggestive rather than confirmatory」を明記し、匿名版の断定表現も控えめ化（N=47の不安定性を反映） | No.17 commit |
| 18 | 体裁・形式（引用位置／Figure整合） | Done | 本文変更なし。投稿直前に引用番号位置・Figure参照/別添ファイル名整合を最終点検する運用をログ化 | No.18 commit |
