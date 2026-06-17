import json
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\Admin\Documents")
FILES = {
    2025: "edra theo brand 2025.xlsx",
    2026: "edra theo brand 2026.xlsx",
}
OUT = Path("work/analysis/consistent/xnk_brand_ranking.json")

CATEGORY_KEYS = {
    "ban phim": "Keyboard",
    "chuot": "Mouse",
    "tai nghe": "Headset",
    "man hinh": "Monitor",
}


def clean_text(value):
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.replace("đ", "d")


def find_file(name):
    matches = list(ROOT.rglob(name))
    if not matches:
        raise FileNotFoundError(name)
    return matches[0]


def category_from_title(title):
    text = clean_text(title)
    for key, val in CATEGORY_KEYS.items():
        if key in text:
            return val
    return None


def parse_file(path, year):
    df = pd.read_excel(path, header=None)
    current = None
    total_col = None
    rows = []

    for _, row in df.iterrows():
        first = row.iloc[0]
        if isinstance(first, str):
            category = category_from_title(first)
            if category:
                current = category
                total_col = None
                continue

            if clean_text(first) == "brands" and current:
                total_col = None
                for col, value in row.items():
                    if clean_text(value) == "total":
                        total_col = col
                        break
                continue

        if current and total_col is not None and pd.notna(first):
            brand = str(first).strip().upper().replace("E-DRA", "EDRA")
            if not brand or brand in ["TOTAL", "NAN"]:
                continue
            qty = pd.to_numeric(row.iloc[total_col], errors="coerce")
            if pd.notna(qty):
                rows.append(
                    {
                        "year": year,
                        "category": current,
                        "brand": brand,
                        "quantity": float(qty),
                    }
                )
    return rows


def ranking_payload(group):
    total = group.groupby("brand", as_index=False)["quantity"].sum().sort_values("quantity", ascending=False)
    total["rank"] = range(1, len(total) + 1)
    top = total.head(12).copy()
    edra = total[total["brand"].eq("EDRA")]
    if len(edra) and "EDRA" not in set(top["brand"]):
        top = pd.concat([top, edra], ignore_index=True)
    return {
        "rows": top.astype(object).where(pd.notna(top), None).to_dict(orient="records"),
        "edra": edra.astype(object).where(pd.notna(edra), None).to_dict(orient="records")[0] if len(edra) else None,
    }


def main():
    rows = []
    for year, name in FILES.items():
        rows.extend(parse_file(find_file(name), year))

    raw = pd.DataFrame(rows)
    if raw.empty:
        raise ValueError("No ranking rows parsed from brand files")

    payload = {}
    for category, group in raw.groupby("category"):
        item = ranking_payload(group)
        item["by_year"] = {
            str(int(year)): ranking_payload(year_group)
            for year, year_group in group.groupby("year")
        }
        payload[category] = item

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)
    for cat, item in payload.items():
        print(cat)
        for year in ["2025", "2026"]:
            print(" ", year, item["by_year"].get(year, {}).get("edra"))


if __name__ == "__main__":
    main()
