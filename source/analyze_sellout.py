import json
import re
from pathlib import Path

import pandas as pd


FILES = {
    2025: Path(r"C:\Users\Admin\Downloads\sell out 2025.xlsx"),
    2026: Path(r"C:\Users\Admin\Downloads\sellout 2026.xlsx"),
}
OUT_DIR = Path("work/analysis/consistent")
PRODUCT_ORDER = ["Keyboard", "Mouse", "Headset", "Monitor", "Chair"]


def text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm(value):
    return text(value).lower()


def is_edra(code, name):
    name_l = norm(name)
    return bool(re.search(r"\be\s*-?\s*dra\b|\bedra\b", name_l, flags=re.I))


def classify(code, name):
    code_u = text(code).upper()
    name_l = norm(name)
    if "giá đỡ" in name_l or "gia do" in name_l or code_u.startswith("EMA"):
        return None
    if "bàn di" in name_l or "ban di" in name_l or code_u.startswith("EMP"):
        return None
    if "bàn phím" in name_l or "ban phim" in name_l:
        return "Keyboard"
    if "tai nghe" in name_l or "headset" in name_l or "headphone" in name_l:
        return "Headset"
    if "màn hình máy tính" in name_l or "man hinh may tinh" in name_l:
        return "Monitor"
    if "ghế" in name_l or re.search(r"\bghe\b", name_l):
        return "Chair"
    if "chuột" in name_l or "chuot" in name_l:
        return "Mouse"
    return None


def product_code(code, name):
    code_u = text(code).upper()
    if code_u and code_u != "NAN":
        return code_u
    match = re.search(r"\b(E[A-Z]{1,3}[A-Z0-9-]{2,})\b", text(name), flags=re.I)
    return match.group(1).upper() if match else text(name)[:80]


def short_name(name, code):
    code_u = product_code(code, name)
    clean = re.sub(r"\s+", " ", text(name))
    if len(clean) > 95:
        clean = clean[:92] + "..."
    return clean or code_u


def read_file(path, year):
    raw = pd.read_excel(path, sheet_name=0, header=None)
    header_idx = None
    for idx, row in raw.head(30).iterrows():
        vals = [text(v) for v in row.tolist()]
        if "Tên hàng" in vals and "Tổng số lượng bán" in vals:
            header_idx = idx
            break
    if header_idx is None:
        raise ValueError(f"Cannot find header row in {path}")

    df = raw.iloc[header_idx + 1 :].copy()
    df.columns = [text(v) for v in raw.iloc[header_idx].tolist()]
    df = df.loc[:, [c for c in df.columns if c]]

    rows = []
    for _, row in df.iterrows():
        date = pd.to_datetime(row.get("Ngày hạch toán"), errors="coerce")
        code = row.get("Mã hàng")
        name = row.get("Tên hàng")
        sold = pd.to_numeric(row.get("Tổng số lượng bán"), errors="coerce")
        returned = pd.to_numeric(row.get("Tổng số lượng trả lại"), errors="coerce")
        if pd.isna(date) or pd.isna(sold) or sold <= 0:
            continue
        if not is_edra(code, name):
            continue
        category = classify(code, name)
        if category not in PRODUCT_ORDER:
            continue
        rows.append(
            {
                "year": int(year),
                "month": int(date.month),
                "period": f"{int(year)}-{int(date.month):02d}",
                "category": category,
                "item": product_code(code, name),
                "product_name": short_name(name, code),
                "sold_quantity": float(sold),
                "returned_quantity": float(0 if pd.isna(returned) else returned),
            }
        )
    return rows


def records(df):
    return df.astype(object).where(pd.notna(df), None).to_dict(orient="records")


def complete_categories(df, year_col="year"):
    all_years = sorted(df[year_col].unique()) if year_col in df.columns and len(df) else [2025, 2026]
    base = pd.MultiIndex.from_product([all_years, PRODUCT_ORDER], names=[year_col, "category"]).to_frame(index=False)
    return base.merge(df, on=[year_col, "category"], how="left").fillna({"sold_quantity": 0})


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = pd.DataFrame([r for year, path in FILES.items() for r in read_file(path, year)])
    raw.to_csv(OUT_DIR / "sellout_edra_normalized.csv", index=False, encoding="utf-8-sig")

    yearly = raw.groupby(["year", "category"], as_index=False)["sold_quantity"].sum()
    yearly = complete_categories(yearly).sort_values(["year", "category"])

    monthly = raw.groupby(["year", "month", "period", "category"], as_index=False)["sold_quantity"].sum()
    total_month = raw.groupby(["year", "month", "period"], as_index=False)["sold_quantity"].sum().sort_values(["year", "month"])

    by_cat = raw.groupby(["category"], as_index=False)["sold_quantity"].sum()
    by_cat = pd.DataFrame({"category": PRODUCT_ORDER}).merge(by_cat, on="category", how="left").fillna({"sold_quantity": 0})
    by_cat["category"] = pd.Categorical(by_cat["category"], PRODUCT_ORDER, ordered=True)
    by_cat = by_cat.sort_values("category")

    jan_may = raw[raw["month"].between(1, 5)]
    pivot = jan_may.groupby(["category", "year"], as_index=False)["sold_quantity"].sum().pivot_table(
        index="category", columns="year", values="sold_quantity", fill_value=0
    )
    for year in [2025, 2026]:
        if year not in pivot.columns:
            pivot[year] = 0
    yoy = pivot.reset_index().rename(columns={2025: "five_m_2025", 2026: "five_m_2026"})
    yoy["category"] = pd.Categorical(yoy["category"], PRODUCT_ORDER, ordered=True)
    yoy = yoy.sort_values("category")
    yoy["growth_abs"] = yoy["five_m_2026"] - yoy["five_m_2025"]
    yoy["growth_pct"] = yoy.apply(lambda r: None if r["five_m_2025"] == 0 else r["growth_abs"] / r["five_m_2025"], axis=1)

    item_totals = (
        raw.groupby(["category", "item", "product_name"], as_index=False)["sold_quantity"]
        .sum()
        .sort_values("sold_quantity", ascending=False)
    )
    top10 = item_totals.head(5).copy()
    top10_by_year = (
        raw.groupby(["year", "category", "item", "product_name"], as_index=False)["sold_quantity"]
        .sum()
        .sort_values(["year", "sold_quantity"], ascending=[True, False])
        .groupby("year", as_index=False)
        .head(5)
    )
    top_by_category = (
        item_totals.sort_values(["category", "sold_quantity"], ascending=[True, False])
        .groupby("category", as_index=False)
        .head(8)
    )
    top_by_category_year = (
        raw.groupby(["year", "category", "item", "product_name"], as_index=False)["sold_quantity"]
        .sum()
        .sort_values(["year", "category", "sold_quantity"], ascending=[True, True, False])
        .groupby(["year", "category"], as_index=False)
        .head(5)
    )

    payload = {
        "totals": {
            "total_2025": float(yearly[yearly["year"].eq(2025)]["sold_quantity"].sum()),
            "total_2026_5m": float(yearly[yearly["year"].eq(2026)]["sold_quantity"].sum()),
            "total_all": float(raw["sold_quantity"].sum()),
        },
        "yearly": records(yearly),
        "monthly": records(monthly),
        "total_month": records(total_month),
        "category_total": records(by_cat),
        "yoy_5m": records(yoy),
        "top10": records(top10),
        "top10_by_year": records(top10_by_year),
        "top_by_category": records(top_by_category),
        "top_by_category_year": records(top_by_category_year),
    }
    (OUT_DIR / "sellout_edra_slide_data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(payload["totals"], ensure_ascii=False, indent=2))
    print(top10[["category", "item", "sold_quantity"]].to_string(index=False))


if __name__ == "__main__":
    main()
