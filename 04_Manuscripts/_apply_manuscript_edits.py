# -*- coding: utf-8 -*-
"""Apply supervisor 10-point edits + safe reference renumbering (SharedWorkspace path only)."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(r"c:\Users\user\SharedWorkspace\projects\NDB_Research_Hub\projects\NDB_XXX_slope_fracture\04_Manuscripts")
SRC = BASE / "Manuscript_slope_fracture.qmd.backup"
OUT = BASE / "Manuscript_slope_fracture.qmd"

REMOVED = {
    14, 23, 29, 34, 37, 38, 39, 41, 43,
    47, 48, 49, 50,
    53, 54, 55, 63, 64,
}


def split_three_parts(text: str) -> tuple[str, str, str]:
    """Return (pre_refs, ref_block_from_heading, tail_from_tables_separator)."""
    idx = text.index("\n# References\n")
    pre = text[:idx]
    rest = text[idx + 1 :]  # starts with # References\n
    m2 = re.search(r"\n---\n\n\n\n# Tables and Figures", rest)
    if not m2:
        raise SystemExit("missing tables marker")
    ref_block = rest[: m2.start()]
    tail = rest[m2.start() :]
    return pre, ref_block, tail


def parse_refs(ref_block: str) -> dict[int, str]:
    d: dict[int, str] = {}
    for line in ref_block.splitlines(keepends=True):
        if re.match(r"^\d+\)\s", line):
            d[int(line.split(")", 1)[0])] = line
    return d


def protect_sample_sizes(s: str) -> tuple[str, list[str]]:
    keys: list[str] = []

    def repl(m: re.Match[str]) -> str:
        keys.append(m.group(0))
        return f"«S{len(keys) - 1}»"

    out = re.sub(r"\(N\s*=\s*\d+\)", repl, s)
    return out, keys


def unprotect(s: str, keys: list[str]) -> str:
    for i, k in enumerate(keys):
        s = s.replace(f"«S{i}»", k)
    return s


def strip_removed_citations(body: str) -> str:
    for rid in sorted(REMOVED, reverse=True):
        body = re.sub(rf",\s*{rid}\),\s*", ", ", body)
        body = re.sub(rf"(?<=\)){rid}\),\s*", "", body)
        body = re.sub(rf"(?<![0-9]){rid}\),\s*", "", body)
        body = re.sub(rf",\s*{rid}\)(?=[\s.])", "", body)
        body = re.sub(rf"(?<![0-9]){rid}\)(?=[\s\n])", "", body)
    body = re.sub(r",\s*,", ",", body)
    body = re.sub(r"\(\s*,", "(", body)
    body = re.sub(r",\s*\)", ")", body)
    return body


def renumber_body(body: str, old_to_new: dict[int, int]) -> str:
    # Allow citations immediately after letters (e.g., "...risk16), 17)")
    cite = re.compile(
        r"(?:^|(?<=[^0-9]))([1-9]|[1-5][0-9]|6[0-6])\)(?=[,\s.\n]|$)"
    )

    def repl(m: re.Match[str]) -> str:
        n = int(m.group(1))
        newn = old_to_new.get(n)
        if newn is None:
            return m.group(0)
        return f"{newn})"

    return cite.sub(repl, body)


def edit_pre_refs(pre: str) -> str:
    # ① Main Findings closing sentence
    pre = pre.replace(
        "This association was specific to hip fractures and was not observed for humerus or forearm fractures.\n\n## 2. Biological Plausibility",
        "This association was specific to hip fractures and was not observed for humerus or forearm fractures. Together, these findings suggest that, at the population level, steeper habitable terrain tracks hip-specific surgical burden beyond compositional aging and self-reported walking pace, consistent with outdoor environments amplifying lateral-fall mechanisms rather than raising fracture risk indiscriminately across skeletal sites.\n\n## 2. Biological Plausibility",
    )
    # Methods ⑧ companion
    pre = pre.replace(
        "We first examined the distribution of all variables using descriptive statistics (mean, SD, median, range).",
        "We first examined the distribution of all variables using descriptive statistics (mean, SD, minimum, and maximum).",
    )
    # ② Role of aging — remove Japan-only block, keep double burden
    pre = pre.replace(
        "populations.44), 45), 46) Since the high economic growth period of the 1960s, labor-age youth have continuously migrated from mountainous areas in Shikoku, Chugoku, and inland Kyushu toward urban plains (Tokyo, Osaka-Kyoto-Kobe), leaving behind an aging residual population.45), 47)\n\nThis outmigration has led to the emergence of \"Genkai-shuraku\" (marginal villages), defined as communities where more than 50% of residents are aged 65 or older and basic community functions are severely impaired.48), 49) In these depopulated mountainous settlements (Kaso), public transportation, healthcare infrastructure (including orthopedic surgeon availability), snow removal services, and social support networks have deteriorated or collapsed entirely.49), 50) Older adults in these high-slope prefectures thus face a double burden:",
        "populations.44), 45), 46) Older adults in these high-slope prefectures thus face a double burden:",
    )
    # ③④⑤ Conclusions shorten
    pre = pre.replace(
        "consistent with the biomechanical literature demonstrating that lateral falls on inclined terrain specifically increase impact loading to the greater trochanter.\n\nOur findings align with international ecological evidence from Norway (NOREPOS) and China (CHARLS), establishing terrain slope as a globally relevant environmental risk factor for hip fracture. In the context of Japan's accelerating rural aging and depopulation of mountainous areas (Kaso, Genkai-shuraku), these results highlight the double burden faced by older adults in high-slope prefectures: chronic exposure to biomechanically challenging terrain compounded by social isolation and healthcare infrastructure decline.\n\nThese findings have direct policy implications. Topographic characteristics should be incorporated into community-level fracture prevention strategies, with prioritization of resources toward high-slope prefectures. Japan's \"Active Guide\" physical activity recommendations require environment-specific adaptation for mountainous regions, integrating balance training, anti-slip footwear, outdoor handrail installation, and pedestrian infrastructure design that explicitly accounts for slope gradient. Given the irreversible demographic shift toward an aging society and the escalating economic burden of hip fracture care (exceeding 1,000 billion yen annually), upstream environmental interventions targeting terrain-related hazards represent a cost-effective public health strategy.\n\nFuture studies",
        "consistent with the biomechanical literature demonstrating that lateral falls on inclined terrain specifically increase impact loading to the greater trochanter.\n\nFuture studies",
    )
    return pre


def apply_consolidations(pre: str) -> str:
    pre = pre.replace(
        "Previous studies have demonstrated that environmental terrain features are associated with physical activity levels and walking speed in community-dwelling older adults.14), 15)",
        "Previous studies have demonstrated that environmental terrain features are associated with physical activity levels and walking speed in community-dwelling older adults.15)",
    )
    pre = pre.replace(
        "elevated hip fracture risk,21), 22), 23) but",
        "elevated hip fracture risk,21), 22) but",
    )
    pre = pre.replace(
        "compared to those in flat coastal regions.21), 38), 39)",
        "compared to those in flat coastal regions.21)",
    )
    pre = pre.replace(
        "amplified this geographic risk,40), 41)",
        "amplified this geographic risk,40)",
    )
    pre = pre.replace(
        "among overweight individuals and women.22), 23)",
        "among overweight individuals and women.22)",
    )
    pre = pre.replace(
        "fracture risk.42), 43)",
        "fracture risk.42)",
    )
    pre = pre.replace(
        "In Japan, Nakamura et al. reported that outdoor activity and terrain characteristics influenced walking speed and muscle strength in community-dwelling older adults in mountainous regions.14)",
        "In Japan, Fujita et al. reported that frequent outdoor activity predicts physical function in rural community-dwelling older adults.15)",
    )
    pre = pre.replace(
        "maximizing fracture vulnerability.28), 29)",
        "maximizing fracture vulnerability.28)",
    )
    pre = pre.replace(
        "during forward falls on flat surfaces.33), 34)",
        "during forward falls on flat surfaces.33)",
    )
    pre = pre.replace(
        "who retain arm-protective reflexes.36), 37)",
        "who retain arm-protective reflexes.36)",
    )
    pre = pre.replace(
        "sarcopenia, frailty, and mortality.16), 17), 18), 53)",
        "sarcopenia, frailty, and mortality.16), 17), 18)",
    )
    pre = pre.replace(
        "significantly elevate hip fracture incidence.17), 54)",
        "significantly elevate hip fracture incidence.17)",
    )
    pre = pre.replace(
        "on complex outdoor terrain.19), 55)",
        "on complex outdoor terrain.19)",
    )
    pre = pre.replace(
        "under the Health Japan 21 (second edition) framework.61), 62), 63)",
        "under the Health Japan 21 (second edition) framework.61), 62)",
    )
    pre = pre.replace(
        "not individual motivation alone.61), 64)",
        "not individual motivation alone.61)",
    )
    return pre


def edit_tail(tail: str) -> str:
    # Table 1 remove Median column
    tail = tail.replace(
        "| Variable | Unit | N | Mean | SD | Min | Median | Max |\n| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |\n| **Outcome variables** | | | | | | | |\n| Total fracture surgery rate | per 100,000 | 47 | 352.75 | 54.85 | 249.22 | 356.11 | 446.68 |\n| Hip (femur) fracture surgery rate | per 100,000 | 47 | 253.99 | 37.57 | 167.61 | 253.87 | 329.62 |\n| Humerus fracture surgery rate | per 100,000 | 47 | 35.59 | 7.52 | 22.39 | 35.56 | 50.45 |\n| Forearm fracture surgery rate | per 100,000 | 47 | 63.18 | 15.59 | 33.49 | 60.84 | 106.33 |\n| **Exposure variable** | | | | | | | |\n| Habitable-area-weighted slope | degrees | 47 | 8.57 | 3.16 | 1.81 | 8.36 | 15.43 |\n| Simple mean slope | degrees | 47 | 8.28 | 2.90 | 1.88 | 8.18 | 14.22 |\n| **Covariate variables** | | | | | | | |\n| Aging rate (≥65 years) | % | 47 | 30.74 | 3.10 | 22.61 | 31.26 | 36.45 |\n| Fast walking rate | % | 47 | 48.62 | 4.34 | 29.79 | 49.23 | 57.30 |\n| Population density | persons/km² | 47 | 657 | 1,223 | 62.63 | 265.44 | 6,402.64 |",
        "| Variable | Unit | N | Mean | SD | Min | Max |\n| :--- | :--- | ---: | ---: | ---: | ---: | ---: |\n| **Outcome variables** | | | | | | |\n| Total fracture surgery rate | per 100,000 | 47 | 352.75 | 54.85 | 249.22 | 446.68 |\n| Hip (femur) fracture surgery rate | per 100,000 | 47 | 253.99 | 37.57 | 167.61 | 329.62 |\n| Humerus fracture surgery rate | per 100,000 | 47 | 35.59 | 7.52 | 22.39 | 50.45 |\n| Forearm fracture surgery rate | per 100,000 | 47 | 63.18 | 15.59 | 33.49 | 106.33 |\n| **Exposure variable** | | | | | | |\n| Habitable-area-weighted slope | degrees | 47 | 8.57 | 3.16 | 1.81 | 15.43 |\n| Simple mean slope | degrees | 47 | 8.28 | 2.90 | 1.88 | 14.22 |\n| **Covariate variables** | | | | | | |\n| Aging rate (≥65 years) | % | 47 | 30.74 | 3.10 | 22.61 | 36.45 |\n| Fast walking rate | % | 47 | 48.62 | 4.34 | 29.79 | 57.30 |\n| Population density | persons/km² | 47 | 657 | 1,223 | 62.63 | 6,402.64 |",
    )
    # ⑩ Figure 3 remove + renumber
    tail = tail.replace(
        "**Figure 1.** Scatter plot showing the association between habitable-area-weighted terrain slope (degrees) and hip fracture surgery rate (per 100,000 population) across 47 Japanese prefectures. Each point represents one prefecture. The solid line represents the simple linear regression fit.\n\n**Figure 2.**",
        "**Figure 1.** Scatter plot showing the association between habitable-area-weighted terrain slope (degrees) and hip fracture surgery rate (per 100,000 population) across 47 Japanese prefectures. Each point represents one prefecture, labeled with the prefecture name in English. The solid line represents the simple linear regression fit.\n\n**Figure 2.**",
    )
    tail = tail.replace(
        "**Figure 3.** Scatter matrix showing pairwise relationships among terrain slope, hip fracture rate, aging rate, and fast walking rate across 47 Japanese prefectures.\n\n**Figure 4.**",
        "**Figure 3.**",
    )
    tail = tail.replace(
        "**Figure 5.** Prefectural distribution of hip fracture surgery rate",
        "**Figure 4.** Prefectural distribution of hip fracture surgery rate",
    )
    tail = tail.replace(
        "**Figure 6.** Bivariate choropleth map",
        "**Figure 5.** Bivariate choropleth map",
    )
    tail = tail.replace(
        "## Figure 3\n\n![](../03_Analysis/results/figures/scatter_matrix.png)\n\n## Figure 4\n",
        "## Figure 3\n",
    )
    tail = tail.replace("## Figure 5\n", "## Figure 4\n")
    tail = tail.replace("## Figure 6\n", "## Figure 5\n")
    return tail


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    pre, ref_block, tail = split_three_parts(text)
    pre = edit_pre_refs(pre)
    pre = apply_consolidations(pre)
    tail = edit_tail(tail)

    kept = [n for n in range(1, 67) if n not in REMOVED]
    old_to_new = {old: i + 1 for i, old in enumerate(kept)}
    ref_dict = parse_refs(ref_block)

    pre, keys = protect_sample_sizes(pre)
    pre = strip_removed_citations(pre)
    pre = renumber_body(pre, old_to_new)
    pre = unprotect(pre, keys)

    new_ref_lines = []
    for old in kept:
        line = ref_dict[old]
        rest = line.split(")", 1)[1].lstrip()
        new_ref_lines.append(f"{old_to_new[old]}) {rest}")
    new_ref_block = "# References\n\n" + "".join(new_ref_lines)

    out = pre + "\n" + new_ref_block + "\n" + tail.lstrip("\n")
    OUT.write_text(out, encoding="utf-8")
    print("Wrote", OUT)
    print("References:", len(kept))


if __name__ == "__main__":
    main()
