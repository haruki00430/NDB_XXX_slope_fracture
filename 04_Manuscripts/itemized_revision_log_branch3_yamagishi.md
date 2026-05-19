# Itemized Revision Log (branch-3: 山岸先生)

対象原稿: `Manuscript_slope_fracture.qmd`  
チェックリスト: `itemized_revision_checklist_branch3_yamagishi.md`  
コメント正本: `Manuscript_slope_fracture_20260425_saito0430-1.docx` / `.pdf`

運用: **1 checklist 行（No.）ごと**に本文修正 → SKILL 準拠確認 → **1 commit** → push → 本ログ追記

---

## 2026-05-19: Setup

- branch-3 用チェックリスト・ログを作成（山岸先生コメント **20 項目**；Word ID 山1〜31 のうち治齋以外）。
- ベース DOCX/PDF は **2026-04-25 版**（舟久保先生コメント未反映の治齋修正版）。
- 修正先 qmd は、原則 **branch-2 完了後の最新** `Manuscript_slope_fracture.qmd` を正本とする（着手前に差分確認）。

### 記録テンプレ（No. 完了時にコピーして追記）

```markdown
## 2026-__-__: No.__ （山__）________

- 修正意図:
- 修正ファイル:
  - `04_Manuscripts/Manuscript_slope_fracture.qmd`
  - （該当時）`04_Manuscripts/Manuscript_slope_fracture_anonymous.qmd`
  - `04_Manuscripts/itemized_revision_checklist_branch3_yamagishi.md`
  - `04_Manuscripts/itemized_revision_log_branch3_yamagishi.md`
- 反映要約:
- SKILL 準拠チェック:
- commit: `<hash>` / push:
```

---

## 2026-05-19: branch-2 qmd との差分確認（着手前）

### 比較の取り方

| 比較軸 | コミット / ファイル | 意味 |
|--------|---------------------|------|
| **A. 山岸先生コメント付き DOCX/PDF のベース** | `1d7ea7f`（2026-04-30 20:47） | 佐藤・寳澤・島袋（治齋）反映済み。**舟久保 branch-2 の qmd 本文変更前**の最終点 |
| **B. 現行正本** | `HEAD`（`branch-2`, `ca57785`） | 舟久保 No.16–17、Table 5、SIR 用語統一まで反映 |
| **C. 共有 DOCX/PDF** | `Manuscript_slope_fracture_20260425_saito0430-1.*` | 山岸先生がコメントした見た目。**qmd からの再エクスポートではない**（Methods に FY2021 記載など古い箇所が残存） |

### A → B（branch-2 が qmd に追加したもの）

`git diff 1d7ea7f..HEAD -- Manuscript_slope_fracture.qmd`（+17 / −4 行）

| 区分 | 内容 | branch-2 対応 |
|------|------|----------------|
| Methods | SIR 初出定義・「indirectly standardized surgery rate」表記へ統一 | Table 5 作業（`6c2b89b`〜`ca57785`） |
| Results | ISR 感度の長文（`"-"=0/5/9` と β 列挙）を削除 → **Table 5 参照の 2 文**に圧縮 | 同上（**山19「`-` の説明」は未解消**—表見出しに `"-"` 残存） |
| Limitations | fast-walking は能力指標であり歩行量・坂道曝露の代理ではない、を 1 文追加 | No.16（`e7b1092`） |
| Conclusions | `suggestive rather than confirmatory`（*N*=47）を追記 | No.17（`c07fcdd`） |
| Tables | **Table 5**（間接標準化感度・3 シナリオ）新設 | `6c2b89b` |

**branch-2 で本文変更なし（ログのみ）**: No.13–15（舟久保：個人曝露乖離、地域構造、**自動車保有率の追加解析見送り**）。→ **山29（車の考察）**は qmd にはまだ手を入れていない。

### C（saito0430 PDF）と B（現行 qmd）の主なずれ

| 項目 | saito0430-1（PDF） | 現行 qmd（HEAD） | branch-3 への示唆 |
|------|-------------------|------------------|-------------------|
| Study Design 期間 | 「fiscal year 2021」と記載（p.4） | Reiwa 4/5 を明記（10th NDB） | **DOCX は古い**；qmd は修正済み。再提出用 DOCX は qmd から再レンダリング要 |
| Results ISR 段落 | `"-"=0/5/9` の β 全文（治齋18） | Table 5 + 短文 | qmd は進んでいる；**山19** は Table 5 キャプション・Methods の言い換えが残タスク |
| Abstract | HC3/bootstrap 含む難解版 | **1d7ea7f 以来未変更** | 山1–7, 16–17 は **ほぼ全て未対応** |
| Figure 2 + Table 2 | 両方あり | 両方あり | **山16 未対応** |
| 再現性ソフトウェア段落 | Methods 末尾に長文 | 同様に残存 | **山14 未対応** |
| Conclusions | `suggestive` なし（PDF） | あり（branch-2） | 山岸 DOCX より qmd が新しい |

### branch-3（山岸）で優先すべき未着手項目（qmd 現状ベース）

1. **Abstract 一式**（山1–7）— branch-2 でも未着手  
2. **用語** aging rate / rate vs proportion（山10, 15）  
3. **Introduction** 競合メカニズム・県レベル意義（山8, 9）  
4. **Results** Figure2/Table2、HC3 段落の要否（山16, 17）  
5. **マスキング説明**（山19）— Table 5 導入後も `"-"` 表記が残る  
6. **Discussion** 居住・車利用・Strengths トーン（山21–23, 29, 31）  
7. **Methods 再現性段落**（山14）

### 結論（作業開始点）

- **正本は `Manuscript_slope_fracture.qmd`（HEAD）** とする。`saito0430-1.docx` はコメント索引用とし、本文は qmd を編集後に再出力する。  
- branch-2 の舟久保対応のうち **本文に入ったのは No.16–17 と Table 5 系のみ**；No.15（車の追加解析見送り）と **山29（車の考察記述）** は別問題として整理する。  
- branch-3 は **Abstract（No.1）から着手**して問題なし。

---

（以下、No.1 以降の完了記録を追記）
