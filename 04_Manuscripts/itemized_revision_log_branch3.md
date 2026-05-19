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
