import json
from pathlib import Path


DATA_PATH = Path("work/analysis/consistent/xnk_edra_slide_data.json")
RANKING_PATH = Path("work/analysis/consistent/xnk_brand_ranking.json")
SELLOUT_PATH = Path("work/analysis/consistent/sellout_edra_slide_data.json")
OUTPUT = Path("outputs/edra-import-sellout-dashboard.html")


def build_html(data):
    data_json = json.dumps(data, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>EDRA XNK Volume Slides</title>
<style>
:root {{
  --black:#050505; --panel:#101014; --panel2:#17121f; --line:#2b2b32;
  --text:#ffffff; --muted:#b8b8c7; --orange:#ff6a00; --purple:#8b5cf6;
  --pink:#ec4899; --green:#22c55e; --red:#ef4444; --cyan:#06b6d4;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; overflow:hidden; background:#050505; color:var(--text); font-family:Aptos, Inter, Segoe UI, Arial, sans-serif; }}
.slides {{ height:100vh; display:flex; transition:transform .55s cubic-bezier(.22,.8,.22,1); }}
.slide {{ min-width:100vw; height:100vh; padding:0; display:flex; align-items:center; justify-content:center; background:
  radial-gradient(circle at 78% 18%, rgba(139,92,246,.23), transparent 28%),
  radial-gradient(circle at 12% 84%, rgba(255,106,0,.18), transparent 30%),
  linear-gradient(135deg, #050505 0%, #0c0c10 50%, #150c1f 100%); position:relative; overflow:hidden; }}
.slide:before {{ content:""; position:absolute; inset:0; background:linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px); background-size:80px 80px; mask-image:linear-gradient(to bottom, transparent, black 18%, black 82%, transparent); }}
.content {{ position:relative; z-index:1; width:min(100vw,177.7778vh); height:min(100vh,56.25vw); padding:34px 56px 30px; display:grid; grid-template-rows:auto 1fr auto; gap:12px; }}
.top {{ display:flex; justify-content:space-between; align-items:center; color:var(--muted); font-size:13px; font-weight:900; text-transform:uppercase; letter-spacing:.08em; }}
.logo {{ display:flex; align-items:center; height:34px; }}
.logo img {{ height:34px; width:auto; display:block; object-fit:contain; filter:drop-shadow(0 8px 18px rgba(0,0,0,.35)); }}
h1 {{ margin:2px 0 4px; font-size:44px; line-height:1.02; letter-spacing:-.05em; max-width:1180px; }}
h2 {{ margin:0; font-size:30px; letter-spacing:-.035em; }}
.sub {{ margin:0; color:#d8d8e3; font-size:17px; line-height:1.32; max-width:1180px; }}
.body {{ display:grid; gap:18px; align-content:stretch; height:100%; }}
.body > .card {{ min-height:0; }}
.two {{ grid-template-columns:1.08fr .92fr; }} .three {{ grid-template-columns:repeat(3,1fr); }}
.card {{ background:linear-gradient(180deg, rgba(16,16,20,.92), rgba(13,13,18,.92)); border:1px solid var(--line); border-radius:26px; padding:20px; box-shadow:0 24px 80px rgba(0,0,0,.35); }}
.kpis {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; margin-top:20px; }}
.kpi {{ min-height:138px; }} .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; font-weight:900; letter-spacing:.08em; }}
.num {{ margin-top:8px; font-size:48px; font-weight:950; letter-spacing:-.05em; }}
.note {{ color:#d1d5db; font-size:14px; margin-top:6px; line-height:1.38; }}
.chart {{ height:500px; }} svg {{ width:100%; height:100%; overflow:visible; }}
.bar {{ transform-origin:left center; animation:grow .85s ease both; }} @keyframes grow {{ from {{ transform:scaleX(0); opacity:.35; }} to {{ transform:scaleX(1); opacity:1; }} }}
table {{ width:100%; border-collapse:collapse; font-size:15px; }} th,td {{ padding:12px 11px; border-bottom:1px solid var(--line); text-align:right; }} th:first-child,td:first-child {{ text-align:left; }} th {{ color:var(--muted); background:#181820; font-size:11px; text-transform:uppercase; letter-spacing:.08em; }}
.pos {{ color:var(--green); font-weight:950; }} .neg {{ color:var(--red); font-weight:950; }}
.foot {{ display:flex; justify-content:space-between; color:var(--muted); font-size:11px; }}
.nav {{ position:fixed; bottom:18px; left:50%; transform:translateX(-50%); z-index:9; display:flex; gap:8px; padding:8px 12px; border:1px solid #383842; background:rgba(0,0,0,.68); border-radius:999px; }}
.dot {{ width:9px; height:9px; border:0; border-radius:50%; background:#555565; cursor:pointer; }} .dot.active {{ width:28px; border-radius:999px; background:var(--orange); }}
.arrow {{ position:fixed; top:50%; transform:translateY(-50%); z-index:9; width:46px; height:46px; border-radius:50%; border:1px solid #383842; background:rgba(0,0,0,.7); color:white; font-size:24px; cursor:pointer; }} .prev {{ left:16px; }} .next {{ right:16px; }}
.edit-toolbar {{ position:fixed; right:18px; bottom:18px; z-index:99999; display:flex; gap:8px; align-items:center; padding:8px; border:1px solid #464652; border-radius:999px; background:rgba(0,0,0,.72); backdrop-filter:blur(12px); box-shadow:0 18px 55px rgba(0,0,0,.45); pointer-events:auto; }}
.edit-toolbar button {{ border:1px solid #3a3a44; background:#111119; color:#fff; border-radius:999px; padding:10px 13px; font-size:12px; font-weight:950; cursor:pointer; pointer-events:auto; }}
.edit-toolbar button.primary {{ background:var(--orange); color:#111; border-color:var(--orange); }}
.edit-toolbar .edit-extra {{ display:none; gap:8px; }}
body.editing .edit-toolbar {{ left:50%; right:auto; bottom:18px; transform:translateX(-50%); border-radius:18px; background:rgba(0,0,0,.86); }}
body.editing .edit-toolbar .edit-extra {{ display:flex; }}
.edit-status {{ display:none; position:fixed; left:50%; bottom:78px; transform:translateX(-50%); z-index:99999; max-width:620px; padding:10px 14px; border:1px solid rgba(255,106,0,.55); border-radius:16px; background:rgba(10,10,14,.92); color:#fff; font-size:13px; line-height:1.35; box-shadow:0 18px 55px rgba(0,0,0,.38); }}
body.editing .edit-status {{ display:block; }}
body.presenting .edit-toolbar, body.presenting .edit-status {{ display:none!important; }}
body.editing [contenteditable="true"] {{ outline:1px dashed rgba(255,106,0,.65); outline-offset:3px; border-radius:8px; cursor:text; }}
body.editing .editable-image {{ cursor:pointer; border-color:var(--orange); background:rgba(255,106,0,.06); }}
.editable-image img {{ width:100%; height:100%; object-fit:contain; display:block; border-radius:18px; }}
.product-image-grid {{ display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr; gap:14px; min-height:470px; }}
.product-image-grid .placeholder {{ min-height:0; height:100%; font-size:16px; padding:16px; }}
.product-image-grid .placeholder span {{ font-size:12px; color:var(--muted); }}
.placeholder {{ border:2px dashed #4b5563; border-radius:24px; min-height:360px; display:flex; align-items:center; justify-content:center; color:var(--muted); text-align:center; font-size:18px; line-height:1.5; padding:22px; }}
.rank-badge {{ display:inline-flex; align-items:center; justify-content:center; width:88px; height:88px; border-radius:24px; background:linear-gradient(135deg,var(--orange),#ffb000); color:#111; font-size:34px; font-weight:950; box-shadow:0 18px 60px rgba(255,106,0,.28); }}
.metric-strip {{ display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin-top:14px; }}
.mini-metric {{ border:1px solid var(--line); background:#0b0b10; border-radius:18px; padding:14px; }}
.mini-metric b {{ display:block; color:var(--orange); font-size:22px; margin-top:5px; }}
.product-divider-body {{ grid-template-columns:1fr 1.05fr; align-items:center; gap:26px; }}
.product-divider-title {{ font-size:60px; }}
.product-preview-list {{ display:grid; gap:8px; align-content:center; }}
.product-preview-item {{ display:grid; grid-template-columns:38px 1fr auto; gap:12px; align-items:center; border:1px solid var(--line); border-radius:16px; padding:10px 12px; background:#0b0b10; }}
.product-preview-item .rank {{ width:30px; height:30px; display:flex; align-items:center; justify-content:center; border-radius:10px; background:rgba(255,106,0,.16); color:var(--orange); font-weight:950; }}
.product-preview-item b {{ display:block; color:var(--text); font-size:19px; letter-spacing:-.02em; }}
.product-preview-item .note {{ margin-top:2px; font-size:12px; line-height:1.2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.product-preview-item .qty {{ color:var(--orange); font-weight:950; font-size:16px; }}
.glow-card {{ position:relative; overflow:hidden; }}
.glow-card:after {{ content:""; position:absolute; right:-70px; bottom:-70px; width:210px; height:210px; border-radius:50%; background:rgba(255,106,0,.16); filter:blur(8px); }}
@media (max-width:1000px) {{ body {{ overflow:auto; }} .slides {{ display:block; transform:none!important; height:auto; }} .slide {{ height:auto; min-height:100vh; }} .two,.three,.kpis {{ grid-template-columns:1fr; }} .nav,.arrow {{ display:none; }} }}
</style>
</head>
<body>
<button class="arrow prev" onclick="go(-1)">‹</button><button class="arrow next" onclick="go(1)">›</button>
<div class="edit-toolbar">
  <button class="primary" id="editToggle" type="button">Edit</button>
  <div class="edit-extra">
    <button id="saveBtn" type="button">Save</button>
    <button id="downloadHtmlBtn" type="button">Download HTML</button>
    <button id="exportBtn" type="button">Export</button>
    <button id="importBtn" type="button">Import</button>
    <button id="resetBtn" type="button">Reset</button>
  </div>
  <button id="presentBtn" type="button">Present</button>
</div>
<div class="edit-status"><b>Edit mode is ON.</b> Click text to type directly. Click product image placeholders to upload photos. Press <b>E</b> to turn edit mode on/off. Press <b>P</b> to hide all edit controls for presenting.</div>
<input id="editImport" type="file" accept="application/json" style="display:none">
<input id="imagePicker" type="file" accept="image/*" style="display:none">
<main class="slides" id="slides">
  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>00 · Opening</div></div>
    <div class="body two">
      <div style="align-self:center">
        <div class="label" style="color:var(--orange)">Partner Presentation</div>
        <h1 style="font-size:64px;max-width:980px">EDRA Import & Sell-out Performance</h1>
        <p class="sub" style="font-size:22px;max-width:920px">A quantity-first business review across EDRA core categories: Keyboard, Mouse, Headset, Monitor and Chair.</p>
        <div class="metric-strip" style="grid-template-columns:repeat(3,1fr);margin-top:34px">
          <div class="mini-metric"><div class="label">Period</div><b>2025 + 5M2026</b><div class="note">Full-year and same-period view</div></div>
          <div class="mini-metric"><div class="label">Main Metric</div><b>Quantity</b><div class="note">Units only</div></div>
          <div class="mini-metric"><div class="label">Flow</div><b>Import → Sell-out</b><div class="note">Supply to market movement</div></div>
        </div>
      </div>
      <div class="card glow-card" style="display:flex;align-items:center;justify-content:center;min-height:560px">
        <img src="assets/edra-logo.png" alt="EDRA" style="width:78%;height:auto;filter:drop-shadow(0 30px 80px rgba(255,106,0,.18))">
      </div>
    </div>
    <div class="foot"><span>EDRA volume review</span><span>00</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>01 · Introduction</div></div>
    <div class="body two">
      <div>
        <h1>EDRA Volume Performance Review</h1>
        <p class="sub">A quantity-focused review for partner discussion, covering import/XNK and sell-out performance across EDRA core product groups.</p>
        <div class="kpis">
          <div class="card kpi"><div class="label">Part 1</div><div class="num" style="color:var(--orange)">XNK</div><div class="note">Import volume, ranking and market share</div></div>
          <div class="card kpi"><div class="label">Part 2</div><div class="num" style="color:var(--purple)">Sell-out</div><div class="note">Sales quantity, trend and best sellers</div></div>
          <div class="card kpi"><div class="label">Scope</div><div class="num" style="color:var(--green)">5</div><div class="note">Keyboard · Mouse · Headset · Monitor · Chair</div></div>
        </div>
      </div>
      <div class="card glow-card">
        <h2>How to Read This Deck</h2>
        <div style="display:grid;gap:16px;margin-top:22px">
          <div class="mini-metric"><div class="label">Time Period</div><b>2025 + 5M2026</b><div class="note">Full-year 2025 and January-May 2026 where available.</div></div>
          <div class="mini-metric"><div class="label">Main Metric</div><b>Quantity</b><div class="note">All visuals focus on units. Revenue, margin and inventory are intentionally excluded.</div></div>
          <div class="mini-metric"><div class="label">Story Flow</div><b>Import → Sell-out</b><div class="note">First establish supply/import position, then show market movement through sell-out.</div></div>
        </div>
      </div>
    </div>
    <div class="foot"><span>Prepared for partner presentation</span><span>Volume only</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>02 · Table of Contents</div></div>
    <div class="body two" style="grid-template-columns:.9fr 1.1fr;align-items:stretch;gap:22px">
      <div class="card glow-card" style="display:grid;align-content:center;padding:32px">
        <div class="label" style="color:var(--orange)">Deck Roadmap</div>
        <h1 style="font-size:56px;margin-top:10px">Table of Contents</h1>
        <p class="sub" style="font-size:20px">A quantity-first storyline built for partner discussion: import position first, sell-out movement second.</p>
        <div class="metric-strip" style="grid-template-columns:1fr 1fr;margin-top:30px">
          <div class="mini-metric"><div class="label">Part 1</div><b>XNK</b><div class="note">Supply-side volume and ranking</div></div>
          <div class="mini-metric"><div class="label">Part 2</div><b>Sell-out</b><div class="note">Sales-side volume and best sellers</div></div>
        </div>
      </div>
      <div style="display:grid;grid-template-rows:1fr auto;gap:16px">
        <div class="card" style="display:grid;gap:12px;padding:24px">
          <div style="display:grid;grid-template-columns:58px 1fr;gap:16px;align-items:center;border-bottom:1px solid var(--line);padding-bottom:14px">
            <div class="rank-badge" style="width:54px;height:54px;border-radius:18px;font-size:22px">01</div>
            <div><div class="label">Import / XNK Overview</div><h2 style="font-size:26px;color:var(--orange)">Total volume, year split, monthly trend</h2></div>
          </div>
          <div style="display:grid;grid-template-columns:58px 1fr;gap:16px;align-items:center;border-bottom:1px solid var(--line);padding-bottom:14px">
            <div class="rank-badge" style="width:54px;height:54px;border-radius:18px;font-size:22px;background:linear-gradient(135deg,var(--purple),#c084fc)">02</div>
            <div><div class="label">Brand Ranking</div><h2 style="font-size:26px;color:var(--purple)">EDRA rank and market share by group</h2></div>
          </div>
          <div style="display:grid;grid-template-columns:58px 1fr;gap:16px;align-items:center;border-bottom:1px solid var(--line);padding-bottom:14px">
            <div class="rank-badge" style="width:54px;height:54px;border-radius:18px;font-size:22px">03</div>
            <div><div class="label">Sell-out Performance</div><h2 style="font-size:26px;color:var(--orange)">Year totals, group split and movement</h2></div>
          </div>
          <div style="display:grid;grid-template-columns:58px 1fr;gap:16px;align-items:center">
            <div class="rank-badge" style="width:54px;height:54px;border-radius:18px;font-size:22px;background:linear-gradient(135deg,var(--purple),#c084fc)">04</div>
            <div><div class="label">Top Products</div><h2 style="font-size:26px;color:var(--purple)">Best sellers and editable product highlights</h2></div>
          </div>
        </div>
        <div class="metric-strip" style="grid-template-columns:repeat(5,1fr);margin-top:0">
          <div class="mini-metric"><div class="label">Group</div><b>Monitor</b></div>
          <div class="mini-metric"><div class="label">Group</div><b>Keyboard</b></div>
          <div class="mini-metric"><div class="label">Group</div><b>Mouse</b></div>
          <div class="mini-metric"><div class="label">Group</div><b>Headset</b></div>
          <div class="mini-metric"><div class="label">Group</div><b>Chair</b></div>
        </div>
      </div>
    </div>
    <div class="foot"><span>Import first, sell-out second</span><span>02</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>03 · Section Divider</div></div>
    <div class="body two">
      <div style="align-self:center">
        <div class="label" style="color:var(--orange)">Part 1</div>
        <h1 style="font-size:72px">Import / XNK Analysis</h1>
        <p class="sub" style="font-size:22px">Supply-side quantity review: EDRA import volume, monthly trend, same-period growth, ranking and market share by product group.</p>
      </div>
      <div class="card glow-card" style="display:grid;align-content:center;gap:18px">
        <div class="mini-metric"><div class="label">Core Question</div><b>How strong is EDRA's imported volume position?</b><div class="note">By group, by month and against other brands.</div></div>
        <div class="mini-metric"><div class="label">Views Included</div><b>Overview · Trend · Ranking · Share</b><div class="note">All based on quantity, not revenue.</div></div>
      </div>
    </div>
    <div class="foot"><span>Part 1 begins</span><span>03</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>04 · XNK Data Reset</div></div>
    <div class="body two">
      <div>
        <h1>EDRA Import Volume Review</h1>
        <p class="sub">Part 1 uses the new XNK files only: brand-level Keyboard, Mouse, Headset, Monitor, plus Chair import files. Volume only, no revenue or inventory inference.</p>
        <div class="kpis">
          <div class="card kpi"><div class="label">2025 Import</div><div class="num" id="kpi2025" style="color:var(--orange)"></div><div class="note">Full-year EDRA quantity</div></div>
          <div class="card kpi"><div class="label">5M2026 Import</div><div class="num" id="kpi2026" style="color:var(--purple)"></div><div class="note">January-May EDRA quantity</div></div>
          <div class="card kpi"><div class="label">Product Groups</div><div class="num">5</div><div class="note">Keyboard · Mouse · Headset · Monitor · Chair</div></div>
        </div>
      </div>
      <div class="card glow-card"><h2>Deck Structure</h2><p class="sub" style="margin-top:20px">Part 1: XNK overview, 2025 split, 5M2026 split, same-period comparison, monthly trend and brand ranking. Part 2 is reserved for sell-out once you send the final consistent files.</p><div class="metric-strip" id="coverMiniMetrics"></div></div>
    </div>
    <div class="foot"><span>Style: EDRA black / orange / purple</span><span>Volume only</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>05 · XNK Overview</div></div>
    <div><h1>Total EDRA XNK by Product Group</h1><p class="sub">Total import quantity across 2025 + 5M2026, separated by product group.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="overviewChart"></div></div><div class="card glow-card"><h2>Exact Numbers</h2><div id="overviewTable" style="margin-top:18px"></div><div class="metric-strip" id="overviewMiniMetrics"></div></div></div>
    <div class="foot"><span>Source: new XNK files</span><span>05</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>06 · 2025</div></div>
    <div><h1>EDRA XNK 2025</h1><p class="sub">Full-year 2025 import quantity by product group.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="y2025Chart"></div></div><div class="card"><h2>2025 Table</h2><div id="y2025Table" style="margin-top:18px"></div></div></div>
    <div class="foot"><span>2025 full-year</span><span>06</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>07 · 5M2026</div></div>
    <div><h1>EDRA XNK 5M2026</h1><p class="sub">January-May 2026 import quantity by product group.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="y2026Chart"></div></div><div class="card"><h2>5M2026 Table</h2><div id="y2026Table" style="margin-top:18px"></div></div></div>
    <div class="foot"><span>2026 data covers January-May</span><span>07</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>08 · Same-period Growth</div></div>
    <div><h1>5M2026 vs 5M2025</h1><p class="sub">Same-period quantity comparison by product group.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="growthChart"></div></div><div class="card"><h2>Growth Table</h2><div id="growthTable" style="margin-top:18px"></div></div></div>
    <div class="foot"><span>January-May comparison</span><span>08</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>09 · Monthly Trend</div></div>
    <div><h1>EDRA XNK Monthly Trend</h1><p class="sub">Total import quantity by month with a 3-month trend line.</p></div>
    <div class="card"><div class="chart" id="monthlyChart"></div></div>
    <div class="foot"><span>Bars = monthly quantity · Line = 3-month trend</span><span>09</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>10 · Product Group Detail</div></div>
    <div><h1>Product Group Comparison</h1><p class="sub">Each product group shown with 2025, 5M2026 and same-period growth.</p></div>
    <div class="card"><div id="detailCards"></div></div>
    <div class="foot"><span>EDRA XNK by product group</span><span>10</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>11 · Brand Ranking</div></div>
    <div><h1>EDRA Ranking vs Other Brands</h1><p class="sub">Brand-level XNK ranking by product group. Chair source is EDRA-only, so it does not have a comparable brand benchmark.</p></div>
    <div class="card glow-card"><h2>EDRA Rank Board</h2><div id="rankSummaryCards" style="margin-top:22px"></div></div>
    <div class="foot"><span>Ranking based on total 2025 + 5M2026 import quantity</span><span>11</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>12 · Keyboard Ranking</div></div>
    <div><h1>Keyboard Import Ranking</h1><p class="sub">EDRA position against other brands in keyboard import quantity.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="rankKeyboardChart"></div></div><div class="card glow-card"><h2>EDRA Position</h2><div id="rankKeyboardInfo" style="margin-top:18px"></div><div class="chart" style="height:150px" id="rankKeyboardMini"></div></div></div>
    <div class="foot"><span>Keyboard brand ranking</span><span>12</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>13 · Mouse Ranking</div></div>
    <div><h1>Mouse Import Ranking</h1><p class="sub">EDRA position against other brands in mouse import quantity.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="rankMouseChart"></div></div><div class="card glow-card"><h2>EDRA Position</h2><div id="rankMouseInfo" style="margin-top:18px"></div><div class="chart" style="height:150px" id="rankMouseMini"></div></div></div>
    <div class="foot"><span>Mouse brand ranking</span><span>13</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>14 · Headset Ranking</div></div>
    <div><h1>Headset Import Ranking</h1><p class="sub">EDRA position against other brands in headset import quantity.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="rankHeadsetChart"></div></div><div class="card glow-card"><h2>EDRA Position</h2><div id="rankHeadsetInfo" style="margin-top:18px"></div><div class="chart" style="height:150px" id="rankHeadsetMini"></div></div></div>
    <div class="foot"><span>Headset brand ranking</span><span>14</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>15 · Monitor Ranking</div></div>
    <div><h1>Monitor Import Ranking</h1><p class="sub">EDRA position against other brands in monitor import quantity.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="rankMonitorChart"></div></div><div class="card glow-card"><h2>EDRA Position</h2><div id="rankMonitorInfo" style="margin-top:18px"></div><div class="chart" style="height:150px" id="rankMonitorMini"></div></div></div>
    <div class="foot"><span>Monitor brand ranking</span><span>15</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>16 · Section Divider</div></div>
    <div class="body two">
      <div style="align-self:center">
        <div class="label" style="color:var(--purple)">Part 2</div>
        <h1 style="font-size:72px">Sell-out Analysis</h1>
        <p class="sub" style="font-size:22px">Sales-side quantity review: total sell-out by year, product group split, monthly movement, and best-selling products by period.</p>
      </div>
      <div class="card glow-card" style="display:grid;align-content:center;gap:18px">
        <div class="mini-metric"><div class="label">Core Question</div><b>Which products are moving fastest in-market?</b><div class="note">Separated by 2025 and 5M2026 to avoid blended signals.</div></div>
        <div class="mini-metric"><div class="label">Views Included</div><b>Year split · Trend · Best sellers</b><div class="note">Filtered to EDRA / E-Dra and the five requested groups.</div></div>
      </div>
    </div>
    <div class="foot"><span>Part 2 begins</span><span>16</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>17 · Sell-out Overview</div></div>
    <div><h1>Sell-out Quantity by Year</h1><p class="sub">Total sell-out quantity for each period, then split by product group. Quantity only, separated from import/XNK.</p></div>
    <div class="card glow-card"><div id="selloutYearSplit"></div></div>
    <div class="foot"><span>Sell-out source: 2025 full-year + 5M2026</span><span>17</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>18 · Sell-out Groups</div></div>
    <div><h1>Sell-out by Product Group</h1><p class="sub">Total sell-out quantity across 2025 + 5M2026.</p></div>
    <div class="body two"><div class="card"><div id="selloutGroupCards"></div></div><div class="card"><h2>Exact Numbers</h2><div id="selloutGroupTable" style="margin-top:18px"></div></div></div>
    <div class="foot"><span>Volume only</span><span>18</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>19 · Sell-out YoY</div></div>
    <div><h1>Sell-out 5M2026 vs 5M2025</h1><p class="sub">Same-period sell-out quantity comparison by group.</p></div>
    <div class="body two"><div class="card"><div class="chart" id="selloutYoyChart"></div></div><div class="card"><h2>Sell-out Growth Table</h2><div id="selloutYoyTable" style="margin-top:18px"></div></div></div>
    <div class="foot"><span>January-May comparison</span><span>19</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>20 · Sell-out Trend</div></div>
    <div><h1>Sell-out Monthly Trend</h1><p class="sub">Monthly sell-out quantity across all EDRA product groups.</p></div>
    <div class="card"><div class="chart" id="selloutMonthlyChart"></div></div>
    <div class="foot"><span>Bars = sell-out quantity</span><span>20</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>21 · Top 5 Sell-out</div></div>
    <div><h1>Best-selling Products by Year</h1><p class="sub">Top sell-out products are separated into 2025 full-year and 5M2026, so seasonal mix does not get blended.</p></div>
    <div class="body two"><div class="card"><h2>Top 5 · 2025</h2><div id="selloutTop2025" style="margin-top:12px"></div></div><div class="card glow-card"><h2>Top 5 · 5M2026</h2><div id="selloutTop2026" style="margin-top:12px"></div></div></div>
    <div class="foot"><span>Best sellers split by period</span><span>21</span></div>
  </div></section>

  <section class="slide"><div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>22 · Top by Group</div></div>
    <div><h1>Best Sellers by Group and Year</h1><p class="sub">Top items are split by product group and by period, avoiding a blended 2025 + 5M2026 view.</p></div>
    <div class="card"><div id="selloutTopByCategory"></div></div>
    <div class="foot"><span>Top item list by category</span><span>22</span></div>
  </div></section>
</main>
<div class="nav" id="nav"></div>
<script>
const DATA = {data_json};
const RANKING = {{ranking_json}};
const SELLOUT = {{sellout_json}};
const cats = DATA.categories;
const c = {{ orange:'#ff6a00', purple:'#8b5cf6', green:'#22c55e', red:'#ef4444', text:'#fff', muted:'#b8b8c7', line:'#2b2b32' }};
let current = 0;
const fmt = n => Number(n||0).toLocaleString('en-US');
const short = n => {{ n=Number(n||0); if(n>=1000000) return (n/1000000).toFixed(2)+'M'; if(n>=1000) return Math.round(n/1000)+'K'; return fmt(n); }};
const pct = n => n==null ? 'n/a' : ((n>=0?'+':'')+(n*100).toFixed(1)+'%');
const sharePct = n => n==null ? 'n/a' : (n*100).toFixed(2)+'%';
const el = id => document.getElementById(id);
function svgEl(name, attrs={{}}) {{ const x=document.createElementNS('http://www.w3.org/2000/svg', name); Object.entries(attrs).forEach(([k,v])=>x.setAttribute(k,v)); return x; }}
function rows() {{ return DATA.yoy; }}
function table(id, headers, body) {{ el(id).innerHTML = `<table><thead><tr>${{headers.map(h=>`<th>${{h}}</th>`).join('')}}</tr></thead><tbody>${{body.map(r=>`<tr>${{r.map((x,i)=>`<td>${{typeof x==='object'?`<span class="${{x.cls||''}}">${{x.text}}</span>`:i===0?`<b>${{x}}</b>`:x}}</td>`).join('')}}</tr>`).join('')}}</tbody></table>`; }}
function barChart(id, dataRows, key, color) {{
  el(id).innerHTML=''; const max=Math.max(...dataRows.map(r=>r[key]),1); const svg=svgEl('svg',{{viewBox:'0 0 930 420'}});
  dataRows.forEach((r,i)=>{{ const y=36+i*72; svg.appendChild(svgEl('text',{{x:0,y:y+20,fill:c.text,'font-size':18,'font-weight':900}})).textContent=r.category; svg.appendChild(svgEl('rect',{{x:150,y,width:530,height:28,rx:14,fill:'#24242d'}})); svg.appendChild(svgEl('rect',{{class:'bar',x:150,y,width:Math.max(2,530*r[key]/max),height:28,rx:14,fill:color}})); svg.appendChild(svgEl('text',{{x:710,y:y+21,fill:color,'font-size':17,'font-weight':900}})).textContent=fmt(r[key]); }});
  el(id).appendChild(svg);
}}
function growthChart() {{
  const dataRows=rows(); el('growthChart').innerHTML='';
  const max=Math.max(...dataRows.flatMap(r=>[r.five_m_2025,r.five_m_2026]),1);
  const svg=svgEl('svg',{{viewBox:'0 0 980 470'}});
  const base=338; const chartH=235;
  svg.appendChild(svgEl('rect',{{x:600,y:18,width:22,height:12,rx:6,fill:'#6b7280'}}));
  svg.appendChild(svgEl('text',{{x:630,y:30,fill:c.muted,'font-size':13,'font-weight':900}})).textContent='5M2025';
  svg.appendChild(svgEl('rect',{{x:730,y:18,width:22,height:12,rx:6,fill:c.orange}}));
  svg.appendChild(svgEl('text',{{x:760,y:30,fill:c.muted,'font-size':13,'font-weight':900}})).textContent='5M2026';
  dataRows.forEach((r,i)=>{{
    const x=78+i*174; const h25=r.five_m_2025/max*chartH; const h26=r.five_m_2026/max*chartH;
    svg.appendChild(svgEl('rect',{{class:'bar',x:x,y:base-h25,width:50,height:h25,rx:12,fill:'#6b7280'}}));
    svg.appendChild(svgEl('rect',{{class:'bar',x:x+58,y:base-h26,width:50,height:h26,rx:12,fill:c.orange}}));
    svg.appendChild(svgEl('text',{{x:x+25,y:base-h25-10,fill:c.muted,'font-size':12,'font-weight':900,'text-anchor':'middle'}})).textContent=short(r.five_m_2025);
    svg.appendChild(svgEl('text',{{x:x+83,y:base-h26-10,fill:c.orange,'font-size':12,'font-weight':950,'text-anchor':'middle'}})).textContent=short(r.five_m_2026);
    svg.appendChild(svgEl('text',{{x:x+54,y:386,fill:c.text,'font-size':15,'font-weight':950,'text-anchor':'middle'}})).textContent=r.category;
    const val=r.growth_pct||0; const color=val>=0?c.green:c.red;
    svg.appendChild(svgEl('text',{{x:x+54,y:414,fill:color,'font-size':16,'font-weight':950,'text-anchor':'middle'}})).textContent=pct(val);
  }});
  svg.appendChild(svgEl('line',{{x1:36,y1:base,x2:940,y2:base,stroke:c.line,'stroke-width':1}}));
  el('growthChart').appendChild(svg);
}}
function monthlyChart() {{
  const dataRows=DATA.total_month; el('monthlyChart').innerHTML=''; const max=Math.max(...dataRows.map(r=>r.quantity),1); const svg=svgEl('svg',{{viewBox:'0 0 1080 440'}}); const pts=[];
  dataRows.forEach((r,i)=>{{ const x=42+i*59; const h=r.quantity/max*270; pts.push({{x:x+16,y:330-h,qty:r.quantity}}); svg.appendChild(svgEl('rect',{{class:'bar',x,y:330-h,width:30,height:h,rx:8,fill:c.orange}})); if(i%2===0) svg.appendChild(svgEl('text',{{x:x+15,y:360,fill:c.muted,'font-size':10,'text-anchor':'middle'}})).textContent=r.period.slice(2); svg.appendChild(svgEl('text',{{x:x+15,y:Math.max(24,318-h),fill:c.text,'font-size':9,'font-weight':900,'text-anchor':'middle'}})).textContent=short(r.quantity); }});
  const ma=dataRows.map((r,i)=>{{ const s=Math.max(0,i-2); const slice=dataRows.slice(s,i+1); const avg=slice.reduce((a,b)=>a+b.quantity,0)/slice.length; return {{x:42+i*59+16,y:330-avg/max*270}}; }});
  svg.appendChild(svgEl('polyline',{{points:ma.map(p=>`${{p.x}},${{p.y}}`).join(' '),fill:'none',stroke:c.purple,'stroke-width':4,'stroke-linecap':'round','stroke-linejoin':'round'}}));
  svg.appendChild(svgEl('line',{{x1:760,y1:28,x2:840,y2:28,stroke:c.purple,'stroke-width':4,'stroke-linecap':'round'}}));
  svg.appendChild(svgEl('text',{{x:852,y:33,fill:c.purple,'font-size':13,'font-weight':900}})).textContent='3-month trend';
  svg.appendChild(svgEl('line',{{x1:34,y1:330,x2:1048,y2:330,stroke:c.line,'stroke-width':1}})); el('monthlyChart').appendChild(svg);
}}
function detailCards() {{
  el('detailCards').innerHTML = `<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px">${{rows().map(r=>`<div class="card" style="box-shadow:none;min-height:220px"><div class="label">${{r.category}}</div><div class="num" style="font-size:32px;color:var(--orange)">${{short(r.total_2025)}}</div><div class="note">2025 import</div><div class="num" style="font-size:30px;color:var(--purple)">${{short(r.total_2026_5m)}}</div><div class="note">5M2026 import</div><div class="${{r.growth_pct>=0?'pos':'neg'}}" style="margin-top:10px;font-size:20px">${{pct(r.growth_pct)}}</div></div>`).join('')}}</div>`;
}}
function miniMetrics(id) {{
  el(id).innerHTML = rows().map(r=>`<div class="mini-metric"><div class="label">${{r.category}}</div><b>${{short(r.total_2025+r.total_2026_5m)}}</b><div class="note">Total</div></div>`).join('');
}}
function rankingChart(id, category) {{
  const block = RANKING[category]; el(id).innerHTML=''; const rows = block.rows; const max = Math.max(...rows.map(r=>r.quantity),1); const svg=svgEl('svg',{{viewBox:'0 0 940 460'}});
  rows.forEach((r,i)=>{{ const y=24+i*34; const isEdra=String(r.brand).toUpperCase()==='EDRA'; const color=isEdra?c.green:c.orange; svg.appendChild(svgEl('text',{{x:0,y:y+15,fill:isEdra?c.green:c.muted,'font-size':13,'font-weight':900}})).textContent='#'+r.rank; svg.appendChild(svgEl('text',{{x:54,y:y+15,fill:c.text,'font-size':13,'font-weight':900}})).textContent=r.brand; svg.appendChild(svgEl('rect',{{x:180,y,width:535,height:20,rx:10,fill:'#24242d'}})); svg.appendChild(svgEl('rect',{{class:'bar',x:180,y,width:Math.max(2,535*r.quantity/max),height:20,rx:10,fill:color}})); svg.appendChild(svgEl('text',{{x:740,y:y+16,fill:color,'font-size':13,'font-weight':900}})).textContent=fmt(r.quantity); if(isEdra) svg.appendChild(svgEl('text',{{x:845,y:y+16,fill:c.green,'font-size':12,'font-weight':900}})).textContent='EDRA'; }});
  el(id).appendChild(svg);
}}
function rankingInfo(id, category) {{
  const e = RANKING[category].edra;
  const marketTotal = RANKING[category].rows.reduce((a,b)=>a+(b.quantity||0),0);
  const share = marketTotal ? e.quantity / marketTotal : null;
  el(id).innerHTML = `<div style="display:flex;gap:20px;align-items:center;margin-bottom:22px"><div class="rank-badge">#${{e.rank}}</div><div><div class="label">EDRA Rank</div><div class="num" style="font-size:38px;color:var(--green)">${{fmt(e.quantity)}}</div><div class="note">Total import quantity · 2025 + 5M2026</div></div></div><div class="metric-strip" style="grid-template-columns:1fr 1fr;margin-top:18px"><div class="mini-metric"><div class="label">Market Share</div><b>${{sharePct(share)}}</b><div class="note">EDRA / all ranked brands</div></div><div class="mini-metric"><div class="label">Brand-market Qty</div><b>${{short(marketTotal)}}</b><div class="note">${{fmt(marketTotal)}} units</div></div></div><p class="sub" style="margin-top:20px">EDRA ranks #${{e.rank}} in ${{category}}, with ${{sharePct(share)}} market share in the supplied import brand data.</p>`;
}}
function rankingMini(id, category) {{
  const block = RANKING[category]; const e = block.edra; const leader = block.rows[0]; el(id).innerHTML=''; const svg=svgEl('svg',{{viewBox:'0 0 460 150'}});
  const vals=[{{label:'Leader', value:leader.quantity, color:c.orange}}, {{label:'EDRA', value:e.quantity, color:c.green}}]; const max=Math.max(...vals.map(v=>v.value),1);
  vals.forEach((v,i)=>{{ const y=30+i*48; svg.appendChild(svgEl('text',{{x:0,y:y+15,fill:c.text,'font-size':14,'font-weight':900}})).textContent=v.label; svg.appendChild(svgEl('rect',{{x:86,y,width:250,height:20,rx:10,fill:'#24242d'}})); svg.appendChild(svgEl('rect',{{class:'bar',x:86,y,width:Math.max(2,250*v.value/max),height:20,rx:10,fill:v.color}})); svg.appendChild(svgEl('text',{{x:352,y:y+15,fill:v.color,'font-size':13,'font-weight':900}})).textContent=short(v.value); }});
  el(id).appendChild(svg);
}}
function rankSummary() {{
  const summary = ['Keyboard','Mouse','Headset','Monitor'].map(cat=>{{ const marketTotal=RANKING[cat].rows.reduce((a,b)=>a+(b.quantity||0),0); return {{category:cat, marketTotal, share:marketTotal?RANKING[cat].edra.quantity/marketTotal:null, ...RANKING[cat].edra}}; }});
  el('rankSummaryCards').innerHTML = `<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px">${{summary.map((r,i)=>`
    <div style="position:relative;min-height:390px;border:1px solid var(--line);border-radius:26px;padding:22px;background:linear-gradient(180deg,rgba(24,24,32,.95),rgba(10,10,14,.96));overflow:hidden">
      <div style="position:absolute;right:-44px;top:-44px;width:150px;height:150px;border-radius:50%;background:${{i%2===0?'rgba(255,106,0,.18)':'rgba(139,92,246,.18)'}};filter:blur(2px)"></div>
      <div class="label">${{r.category}}</div>
      <div style="margin-top:20px;display:flex;align-items:center;justify-content:center">
        <div style="width:120px;height:120px;border-radius:34px;background:linear-gradient(135deg,var(--orange),#ffb000);color:#111;display:flex;align-items:center;justify-content:center;font-size:46px;font-weight:950;box-shadow:0 24px 70px rgba(255,106,0,.26)">#${{r.rank}}</div>
      </div>
      <div style="margin-top:22px;text-align:center">
        <div class="label">EDRA Quantity</div>
        <div class="num" style="font-size:36px;color:var(--text)">${{fmt(r.quantity)}}</div>
        <div class="note" style="margin-top:10px">Total XNK · 2025 + 5M2026</div>
        <div style="margin-top:16px;border-top:1px solid var(--line);padding-top:14px">
          <div class="label">Market Share</div>
          <div style="font-size:28px;font-weight:950;color:var(--green);margin-top:5px">${{sharePct(r.share)}}</div>
          <div class="note">of ${{short(r.marketTotal)}} brand-market units</div>
        </div>
      </div>
    </div>`).join('')}}</div>`;
  el('rankSummaryCards').innerHTML += `<div style="margin-top:18px;border:1px solid var(--line);border-radius:18px;padding:14px 18px;color:var(--muted);font-size:14px">Detailed brand comparison continues in slides 09-12 for each product group.</div>`;
}}
function selloutRows() {{ return ['Keyboard','Mouse','Headset','Monitor','Chair'].map(cat=>{{ const r=SELLOUT.category_total.find(x=>x.category===cat)||{{sold_quantity:0}}; return {{category:cat, quantity:r.sold_quantity||0}}; }}); }}
function selloutYearSplit() {{
  const cats=['Keyboard','Mouse','Headset','Monitor','Chair'];
  const block = (year,label,color) => {{
    const rows = cats.map(cat=>SELLOUT.yearly.find(r=>Number(r.year)===year && r.category===cat)||{{category:cat,sold_quantity:0}});
    const total = rows.reduce((a,b)=>a+(b.sold_quantity||0),0);
    return `<div style="border:1px solid var(--line);border-radius:28px;padding:22px;background:rgba(10,10,16,.72);min-height:430px">
      <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:20px">
        <div><div class="label">${{label}}</div><div class="num" style="font-size:62px;color:${{color}}">${{fmt(total)}}</div></div>
        <div class="note" style="text-align:right;margin-bottom:12px">Total sell-out quantity<br>${{year===2025?'Full-year 2025':'January-May 2026'}}</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:24px">${{rows.map(r=>`
        <div style="border:1px solid var(--line);border-radius:20px;padding:16px;background:#0b0b10;min-height:160px">
          <div class="label">${{r.category}}</div>
          <div style="font-size:28px;font-weight:950;color:${{color}};margin-top:12px">${{short(r.sold_quantity)}}</div>
          <div class="note">${{fmt(r.sold_quantity)}} units</div>
        </div>`).join('')}}</div>
    </div>`;
  }};
  el('selloutYearSplit').innerHTML = `<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">${{block(2025,'2025 Sell-out', 'var(--orange)')}}${{block(2026,'5M2026 Sell-out', 'var(--purple)')}}</div>`;
}}
function selloutGroupCards() {{
  const rows=selloutRows(); const total=Math.max(rows.reduce((a,b)=>a+b.quantity,0),1);
  el('selloutGroupCards').innerHTML = `<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px">${{rows.map((r,i)=>`
    <div style="min-height:310px;border:1px solid var(--line);border-radius:24px;padding:18px;background:#0b0b10;display:flex;flex-direction:column;justify-content:space-between">
      <div><div class="label">${{r.category}}</div><div class="num" style="font-size:34px;color:var(--orange)">${{short(r.quantity)}}</div><div class="note">${{fmt(r.quantity)}} units</div></div>
      <div style="height:150px;border-radius:20px;background:conic-gradient(var(--orange) ${{Math.max(3,r.quantity/total*100)}}%, #24242d 0);display:flex;align-items:center;justify-content:center">
        <div style="width:94px;height:94px;border-radius:50%;background:#0b0b10;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:950">${{(r.quantity/total*100).toFixed(1)}}%</div>
      </div>
    </div>`).join('')}}</div>`;
  table('selloutGroupTable',['Product','Sell-out Qty','Share'],rows.map(r=>[r.category,fmt(r.quantity),(r.quantity/total*100).toFixed(1)+'%']));
}}
function selloutYoyChart() {{
  const dataRows=['Keyboard','Mouse','Headset','Monitor','Chair'].map(cat=>SELLOUT.yoy_5m.find(r=>r.category===cat)||{{category:cat,five_m_2025:0,five_m_2026:0,growth_pct:null}});
  el('selloutYoyChart').innerHTML=''; const max=Math.max(...dataRows.flatMap(r=>[r.five_m_2025,r.five_m_2026]),1); const svg=svgEl('svg',{{viewBox:'0 0 980 470'}}); const base=338; const chartH=235;
  svg.appendChild(svgEl('rect',{{x:600,y:18,width:22,height:12,rx:6,fill:'#6b7280'}})); svg.appendChild(svgEl('text',{{x:630,y:30,fill:c.muted,'font-size':13,'font-weight':900}})).textContent='5M2025';
  svg.appendChild(svgEl('rect',{{x:730,y:18,width:22,height:12,rx:6,fill:c.orange}})); svg.appendChild(svgEl('text',{{x:760,y:30,fill:c.muted,'font-size':13,'font-weight':900}})).textContent='5M2026';
  dataRows.forEach((r,i)=>{{ const x=78+i*174; const h25=r.five_m_2025/max*chartH; const h26=r.five_m_2026/max*chartH; svg.appendChild(svgEl('rect',{{class:'bar',x:x,y:base-h25,width:50,height:h25,rx:12,fill:'#6b7280'}})); svg.appendChild(svgEl('rect',{{class:'bar',x:x+58,y:base-h26,width:50,height:h26,rx:12,fill:c.orange}})); svg.appendChild(svgEl('text',{{x:x+25,y:base-h25-10,fill:c.muted,'font-size':12,'font-weight':900,'text-anchor':'middle'}})).textContent=short(r.five_m_2025); svg.appendChild(svgEl('text',{{x:x+83,y:base-h26-10,fill:c.orange,'font-size':12,'font-weight':950,'text-anchor':'middle'}})).textContent=short(r.five_m_2026); svg.appendChild(svgEl('text',{{x:x+54,y:386,fill:c.text,'font-size':15,'font-weight':950,'text-anchor':'middle'}})).textContent=r.category; const color=(r.growth_pct||0)>=0?c.green:c.red; svg.appendChild(svgEl('text',{{x:x+54,y:414,fill:color,'font-size':16,'font-weight':950,'text-anchor':'middle'}})).textContent=pct(r.growth_pct); }});
  svg.appendChild(svgEl('line',{{x1:36,y1:base,x2:940,y2:base,stroke:c.line,'stroke-width':1}})); el('selloutYoyChart').appendChild(svg);
  table('selloutYoyTable',['Product','5M2025','5M2026','Growth'],dataRows.map(r=>[r.category,fmt(r.five_m_2025),fmt(r.five_m_2026),{{text:pct(r.growth_pct),cls:(r.growth_pct||0)>=0?'pos':'neg'}}]));
}}
function selloutMonthlyChart() {{
  const dataRows=SELLOUT.total_month; el('selloutMonthlyChart').innerHTML='';
  const max=Math.max(...dataRows.map(r=>r.sold_quantity),1); const svg=svgEl('svg',{{viewBox:'0 0 1080 440'}});
  const x0=58, y0=340, chartW=960, chartH=270, step=chartW/(dataRows.length-1);
  [0,.25,.5,.75,1].forEach(t=>{{ const y=y0-chartH*t; svg.appendChild(svgEl('line',{{x1:x0,y1:y,x2:x0+chartW,y2:y,stroke:c.line,'stroke-width':1,opacity:t===0?1:.55}})); if(t>0) svg.appendChild(svgEl('text',{{x:8,y:y+4,fill:c.muted,'font-size':10}})).textContent=short(max*t); }});
  const pts=dataRows.map((r,i)=>{{ return {{x:x0+i*step,y:y0-(r.sold_quantity/max*chartH),...r}}; }});
  const area = `${{x0}},${{y0}} ` + pts.map(p=>`${{p.x}},${{p.y}}`).join(' ') + ` ${{x0+chartW}},${{y0}}`;
  svg.appendChild(svgEl('polygon',{{points:area,fill:'rgba(255,106,0,.14)'}}));
  svg.appendChild(svgEl('polyline',{{points:pts.map(p=>`${{p.x}},${{p.y}}`).join(' '),fill:'none',stroke:c.orange,'stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round'}}));
  pts.forEach((p,i)=>{{ svg.appendChild(svgEl('circle',{{cx:p.x,cy:p.y,r:i<12?5:6,fill:i<12?c.orange:c.purple,stroke:'#09090d','stroke-width':3}})); if(i%2===0) svg.appendChild(svgEl('text',{{x:p.x,y:374,fill:c.muted,'font-size':10,'text-anchor':'middle'}})).textContent=p.period.slice(2); }});
  const peak=pts.reduce((a,b)=>b.sold_quantity>a.sold_quantity?b:a,pts[0]);
  svg.appendChild(svgEl('line',{{x1:peak.x,y1:peak.y-10,x2:peak.x,y2:peak.y-52,stroke:c.green,'stroke-width':2,'stroke-dasharray':'5 5'}}));
  svg.appendChild(svgEl('text',{{x:peak.x,y:Math.max(24,peak.y-62),fill:c.green,'font-size':15,'font-weight':950,'text-anchor':'middle'}})).textContent=`Peak ${{short(peak.sold_quantity)}}`;
  svg.appendChild(svgEl('rect',{{x:760,y:24,width:18,height:10,rx:5,fill:c.orange}})); svg.appendChild(svgEl('text',{{x:786,y:34,fill:c.muted,'font-size':12,'font-weight':900}})).textContent='2025';
  svg.appendChild(svgEl('rect',{{x:840,y:24,width:18,height:10,rx:5,fill:c.purple}})); svg.appendChild(svgEl('text',{{x:866,y:34,fill:c.muted,'font-size':12,'font-weight':900}})).textContent='5M2026';
  el('selloutMonthlyChart').appendChild(svg);
}}
function selloutTop() {{
  const list = (year,color) => SELLOUT.top10_by_year.filter(r=>Number(r.year)===year).map((r,i)=>`<div style="display:grid;grid-template-columns:46px 1fr 94px;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line)"><div style="width:36px;height:36px;border-radius:12px;background:${{i<3?color:'#24242d'}};color:${{i<3?'#111':'var(--text)'}};display:flex;align-items:center;justify-content:center;font-weight:950">#${{i+1}}</div><div><b style="font-size:14px">${{r.item}}</b><div class="note" style="margin-top:1px;font-size:12px">${{r.category}}</div></div><div style="text-align:right;color:${{color}};font-weight:950">${{fmt(r.sold_quantity)}}</div></div>`).join('');
  el('selloutTop2025').innerHTML = list(2025,'var(--orange)');
  el('selloutTop2026').innerHTML = list(2026,'var(--purple)');
}}
function selloutTopByCategory() {{
  const cats=['Keyboard','Mouse','Headset','Monitor','Chair'];
  const list = (cat,year,color) => SELLOUT.top_by_category_year.filter(r=>r.category===cat && Number(r.year)===year).slice(0,5).map((r,i)=>`<div style="display:grid;grid-template-columns:22px 1fr 42px;gap:6px;align-items:center;padding:4px 0;border-bottom:1px solid var(--line)"><b style="color:${{color}};font-size:11px">#${{i+1}}</b><span style="font-size:11px;font-weight:900;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${{r.item}}</span><span style="font-size:11px;color:${{color}};font-weight:950;text-align:right">${{short(r.sold_quantity)}}</span></div>`).join('');
  el('selloutTopByCategory').innerHTML = `<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px">${{cats.map(cat=>`
    <div style="border:1px solid var(--line);border-radius:20px;padding:12px;background:#0b0b10;min-height:455px">
      <div class="label">${{cat}}</div>
      <div style="margin-top:9px;border-top:1px solid var(--line);padding-top:8px"><div style="font-weight:950;color:var(--orange);margin-bottom:3px;font-size:13px">Top 5 · 2025</div>${{list(cat,2025,'var(--orange)')}}</div>
      <div style="margin-top:10px;border-top:1px solid var(--line);padding-top:8px"><div style="font-weight:950;color:var(--purple);margin-bottom:3px;font-size:13px">Top 5 · 5M2026</div>${{list(cat,2026,'var(--purple)')}}</div>
    </div>`).join('')}}</div>`;
}}
function buildProductSlides() {{
  const main=document.getElementById('slides');
  const groupOrder = ['Monitor','Keyboard','Mouse','Headset','Chair'];
  const groupLabel = {{Monitor:'Monitor',Keyboard:'Keyboard',Mouse:'Mouse',Headset:'Headset',Chair:'Chair'}};
  const seen = new Map();
  SELLOUT.top_by_category_year.forEach(r=>{{
    const key = r.item;
    if(!seen.has(key)) seen.set(key, {{...r, periods:[`${{r.year===2026?'5M2026':'2025'}} · #${{SELLOUT.top_by_category_year.filter(x=>x.category===r.category && x.year===r.year).findIndex(x=>x.item===r.item)+1}} in ${{r.category}}`]}});
    else seen.get(key).periods.push(`${{r.year===2026?'5M2026':'2025'}} · #${{SELLOUT.top_by_category_year.filter(x=>x.category===r.category && x.year===r.year).findIndex(x=>x.item===r.item)+1}} in ${{r.category}}`);
  }});
  const highlights = [...seen.values()].sort((a,b)=>groupOrder.indexOf(a.category)-groupOrder.indexOf(b.category) || a.item.localeCompare(b.item));
  const grouped = groupOrder.map(cat=>({{category:cat, items:highlights.filter(r=>r.category===cat)}})).filter(g=>g.items.length);
  let slideNo = 23;

  const intro=document.createElement('section'); intro.className='slide';
  intro.innerHTML = `<div class="content">
    <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>${{String(slideNo).padStart(2,'0')}} · Top Product Highlights</div></div>
    <div><h1>Top Product Highlights</h1><p class="sub">Product detail slides are organized by product group, using the exact best-seller codes from slide 22.</p></div>
    <div class="card glow-card"><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;height:100%;align-items:stretch">${{grouped.map((g,i)=>`
      <div style="border:1px solid var(--line);border-radius:24px;padding:20px;background:#0b0b10;display:flex;flex-direction:column;justify-content:space-between">
        <div><div class="label">${{i+1}} · ${{groupLabel[g.category]}}</div><div class="num" style="font-size:40px;color:${{g.category==='Monitor'?'var(--purple)':'var(--orange)'}}">${{g.items.length}}</div><div class="note">unique best-seller codes</div></div>
        <div style="height:10px;border-radius:999px;background:${{g.category==='Monitor'?'var(--purple)':'var(--orange)'}}"></div>
      </div>`).join('')}}</div></div>
    <div class="foot"><span>Grouped product highlight section</span><span>${{String(slideNo).padStart(2,'0')}}</span></div>
  </div>`;
  main.appendChild(intro);
  slideNo += 1;

  grouped.forEach(g=>{{
    const divider=document.createElement('section'); divider.className='slide';
    divider.innerHTML = `<div class="content">
      <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>${{String(slideNo).padStart(2,'0')}} · ${{groupLabel[g.category]}} Highlights</div></div>
      <div class="body two product-divider-body">
        <div style="align-self:center">
          <div class="label" style="color:${{g.category==='Monitor'?'var(--purple)':'var(--orange)'}}">Top Product Group</div>
          <h1 class="product-divider-title">${{groupLabel[g.category]}}</h1>
          <p class="sub" style="font-size:20px">${{g.items.length}} unique best-seller codes from slide 22. Product slides for this group follow next.</p>
          <div class="metric-strip" style="grid-template-columns:1fr 1fr;margin-top:24px">
            <div class="mini-metric"><div class="label">Preview</div><b>Top 5</b><div class="note">Shown here only as a group entry slide</div></div>
            <div class="mini-metric"><div class="label">Next</div><b>Product Slides</b><div class="note">One editable placeholder per code</div></div>
          </div>
        </div>
        <div class="card glow-card product-preview-list">${{g.items.slice(0,5).map((r,i)=>`<div class="product-preview-item">
          <div class="rank">#${{i+1}}</div>
          <div><b>${{r.item}}</b><div class="note">${{r.periods.join(' · ')}}</div></div>
          <div class="qty">${{short(r.sold_quantity)}}</div>
        </div>`).join('')}}</div>
      </div>
      <div class="foot"><span>${{groupLabel[g.category]}} product highlight group</span><span>${{String(slideNo).padStart(2,'0')}}</span></div>
    </div>`;
    main.appendChild(divider);
    slideNo += 1;

    g.items.forEach((r)=>{{
    const section=document.createElement('section'); section.className='slide';
    section.innerHTML = `<div class="content">
      <div class="top"><div class="logo"><img src="assets/edra-logo.png" alt="EDRA"></div><div>${{String(slideNo).padStart(2,'0')}} · ${{groupLabel[g.category]}} Highlight</div></div>
      <div><h1>${{r.item}}</h1><p class="sub">${{groupLabel[g.category]}} product highlight generated from the exact best-seller codes shown on slide 22. Image area is intentionally left blank for product photo insertion.</p></div>
      <div class="body two">
        <div class="product-image-grid">
          ${{[1,2,3,4].map(n=>`<div class="placeholder editable-image" data-image-key="${{r.item}}-${{n}}" title="Enable Edit mode, then click to add product photo">Product Image ${{n}}<br><span>Add product photo here</span></div>`).join('')}}
        </div>
        <div class="card glow-card"><div class="label">Product Name</div><h2 style="margin-top:10px">${{r.product_name}}</h2><div class="metric-strip" style="grid-template-columns:1fr 1fr;margin-top:28px"><div class="mini-metric"><div class="label">Type</div><b>${{r.category}}</b></div><div class="mini-metric"><div class="label">Best-seller Source</div><b>Slide 22</b></div></div><div style="margin-top:24px;border-top:1px solid var(--line);padding-top:18px"><div class="label">Appears In</div><div style="display:grid;gap:9px;margin-top:12px">${{r.periods.map(p=>`<div style="border:1px solid var(--line);border-radius:14px;padding:10px 12px;background:#0b0b10;font-weight:900;color:var(--orange)">${{p}}</div>`).join('')}}</div></div></div>
      </div>
      <div class="foot"><span>Product slide from slide 22 best-seller groups</span><span>${{String(slideNo).padStart(2,'0')}}</span></div>
    </div>`;
    main.appendChild(section);
    slideNo += 1;
    }});
  }});
}}
function render() {{
  el('kpi2025').textContent=short(DATA.totals.total_2025); el('kpi2026').textContent=short(DATA.totals.total_2026_5m);
  miniMetrics('coverMiniMetrics');
  barChart('overviewChart', rows().map(r=>({{category:r.category,total:r.total_2025+r.total_2026_5m}})), 'total', c.orange);
  table('overviewTable',['Product','2025','5M2026','Total'],rows().map(r=>[r.category,fmt(r.total_2025),fmt(r.total_2026_5m),fmt(r.total_2025+r.total_2026_5m)]));
  miniMetrics('overviewMiniMetrics');
  barChart('y2025Chart', rows(), 'total_2025', c.orange); table('y2025Table',['Product','2025 Quantity'],rows().map(r=>[r.category,fmt(r.total_2025)]));
  barChart('y2026Chart', rows(), 'total_2026_5m', c.purple); table('y2026Table',['Product','5M2026 Quantity'],rows().map(r=>[r.category,fmt(r.total_2026_5m)]));
  growthChart(); table('growthTable',['Product','5M2025','5M2026','Growth'],rows().map(r=>[r.category,fmt(r.five_m_2025),fmt(r.five_m_2026),{{text:pct(r.growth_pct),cls:r.growth_pct>=0?'pos':'neg'}}]));
  monthlyChart(); detailCards();
  rankSummary();
  ['Keyboard','Mouse','Headset','Monitor'].forEach(cat=>{{ rankingChart('rank'+cat+'Chart', cat); rankingInfo('rank'+cat+'Info', cat); rankingMini('rank'+cat+'Mini', cat); }});
  selloutYearSplit(); selloutGroupCards(); selloutYoyChart(); selloutMonthlyChart(); selloutTop(); selloutTopByCategory(); buildProductSlides();
}}
const EDIT_KEY = 'edra_dashboard_user_edits_v1';
const BASE_HTML_SOURCE = document.documentElement.outerHTML;
let editMode = false;
let editStore = {{texts:{{}}, images:{{}}}};
let activeImageKey = null;
function loadEditStore() {{
  try {{ editStore = JSON.parse(localStorage.getItem(EDIT_KEY) || '{{"texts":{{}},"images":{{}}}}'); }}
  catch(e) {{ editStore = {{texts:{{}}, images:{{}}}}; }}
  editStore.texts = editStore.texts || {{}};
  editStore.images = editStore.images || {{}};
}}
function editableTextNodes() {{
  return [...document.querySelectorAll('.slide h1,.slide h2,.slide .sub,.slide .note,.slide .label,.slide .foot span,.slide .mini-metric b,.slide .product-preview-item b')];
}}
function assignEditKeys() {{
  editableTextNodes().forEach(node=>{{
    const slide = node.closest('.slide');
    const slideIndex = [...document.querySelectorAll('.slide')].indexOf(slide);
    const peers = editableTextNodes().filter(n=>n.closest('.slide')===slide);
    node.dataset.editKey = `${{slideIndex}}:${{peers.indexOf(node)}}:${{node.tagName.toLowerCase()}}:${{[...node.classList].join('.')}}`;
  }});
}}
function applyEdits() {{
  loadEditStore();
  assignEditKeys();
  editableTextNodes().forEach(node=>{{ if(editStore.texts[node.dataset.editKey] !== undefined) node.innerHTML = editStore.texts[node.dataset.editKey]; }});
  document.querySelectorAll('.editable-image').forEach(box=>{{
    const src = editStore.images[box.dataset.imageKey];
    if(src) box.innerHTML = `<img src="${{src}}" alt="${{box.dataset.imageKey}}">`;
  }});
}}
function setEditMode(on) {{
  editMode = on;
  document.body.classList.toggle('editing', editMode);
  document.getElementById('editToggle').textContent = editMode ? 'Done' : 'Edit';
  editableTextNodes().forEach(node=>{{
    node.contentEditable = editMode ? 'true' : 'false';
    node.spellcheck = false;
  }});
}}
function toggleEditMode() {{
  setEditMode(!editMode);
  if(!editMode) saveEdits(false);
}}
function saveEdits(showAlert=true) {{
  assignEditKeys();
  editableTextNodes().forEach(node=>{{ editStore.texts[node.dataset.editKey] = node.innerHTML; }});
  try {{
    localStorage.setItem(EDIT_KEY, JSON.stringify(editStore));
    if(showAlert) alert('Saved edits in this browser. Use Export to keep a backup file.');
  }} catch(e) {{
    alert('Could not save all edits. Images may be too large. Use smaller images or Export current edits.');
  }}
}}
async function compressImage(file) {{
  const dataUrl = await new Promise((resolve,reject)=>{{ const r=new FileReader(); r.onload=()=>resolve(r.result); r.onerror=reject; r.readAsDataURL(file); }});
  const img = await new Promise((resolve,reject)=>{{ const i=new Image(); i.onload=()=>resolve(i); i.onerror=reject; i.src=dataUrl; }});
  const max = 1400;
  const scale = Math.min(1, max / Math.max(img.width, img.height));
  const canvas = document.createElement('canvas');
  canvas.width = Math.round(img.width * scale);
  canvas.height = Math.round(img.height * scale);
  canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/jpeg', .86);
}}
document.getElementById('imagePicker').addEventListener('change', async e=>{{
  const file = e.target.files && e.target.files[0];
  if(!file || !activeImageKey) return;
  const src = await compressImage(file);
  editStore.images[activeImageKey] = src;
  document.querySelectorAll(`.editable-image[data-image-key="${{CSS.escape(activeImageKey)}}"]`).forEach(box=>{{ box.innerHTML = `<img src="${{src}}" alt="${{activeImageKey}}">`; }});
  saveEdits(false);
  e.target.value = '';
}});
document.addEventListener('click', e=>{{
  const box = e.target.closest('.editable-image');
  if(!box || !editMode) return;
  activeImageKey = box.dataset.imageKey;
  document.getElementById('imagePicker').click();
}});
document.addEventListener('input', e=>{{ if(editMode && e.target.dataset && e.target.dataset.editKey) saveEdits(false); }});
function exportEdits() {{
  saveEdits(false);
  const blob = new Blob([JSON.stringify(editStore,null,2)], {{type:'application/json'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'edra-dashboard-edits.json';
  a.click();
  URL.revokeObjectURL(a.href);
}}
function downloadEditedHtml() {{
  saveEdits(false);
  const marker = 'render(); applyEdits(); nav();';
  const embedded = `localStorage.setItem(EDIT_KEY, ${{JSON.stringify(JSON.stringify(editStore)).replace(/<\\//g,'<\\\\/')}}); render(); applyEdits(); nav();`;
  const html = BASE_HTML_SOURCE.includes(marker) ? BASE_HTML_SOURCE.replace(marker, embedded) : document.documentElement.outerHTML;
  const blob = new Blob(['<!doctype html>\\n' + html], {{type:'text/html'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'edra-dashboard-edited.html';
  a.click();
  URL.revokeObjectURL(a.href);
}}
document.getElementById('editImport').addEventListener('change', e=>{{
  const file = e.target.files && e.target.files[0];
  if(!file) return;
  const r = new FileReader();
  r.onload = () => {{
    try {{
      editStore = JSON.parse(r.result);
      editStore.texts = editStore.texts || {{}};
      editStore.images = editStore.images || {{}};
      localStorage.setItem(EDIT_KEY, JSON.stringify(editStore));
      applyEdits();
      alert('Imported edits.');
    }} catch(err) {{ alert('Import file is not valid JSON.'); }}
  }};
  r.readAsText(file);
  e.target.value = '';
}});
function clearEdits() {{
  if(!confirm('Reset all text and image edits saved in this browser?')) return;
  localStorage.removeItem(EDIT_KEY);
  location.reload();
}}
function nav() {{ const n=el('nav'); document.querySelectorAll('.slide').forEach((_,i)=>{{ const b=document.createElement('button'); b.className='dot'; b.onclick=()=>goTo(i); n.appendChild(b); }}); update(); }}
function go(d) {{ const count=document.querySelectorAll('.slide').length; goTo(Math.max(0,Math.min(count-1,current+d))); }}
function goTo(i) {{ current=i; el('slides').style.transform=`translateX(${{-100*i}}vw)`; update(); }}
function update() {{ [...el('nav').children].forEach((b,i)=>b.classList.toggle('active',i===current)); }}
function bindEditorButtons() {{
  const bind = (id, fn) => {{ const btn=document.getElementById(id); if(btn) btn.addEventListener('click', e=>{{ e.preventDefault(); e.stopPropagation(); fn(); }}); }};
  bind('editToggle', toggleEditMode);
  bind('saveBtn', () => saveEdits());
  bind('downloadHtmlBtn', downloadEditedHtml);
  bind('exportBtn', exportEdits);
  bind('importBtn', () => document.getElementById('editImport').click());
  bind('resetBtn', clearEdits);
  bind('presentBtn', togglePresentMode);
}}
function togglePresentMode() {{
  if(editMode) setEditMode(false);
  document.body.classList.toggle('presenting');
}}
document.addEventListener('keydown',e=>{{
  if(e.target && e.target.isContentEditable) return;
  if(e.key==='ArrowRight')go(1);
  if(e.key==='ArrowLeft')go(-1);
  if(e.key && e.key.toLowerCase()==='e') toggleEditMode();
  if(e.key && e.key.toLowerCase()==='p') togglePresentMode();
}});
render(); applyEdits(); nav();
bindEditorButtons();
</script>
</body>
</html>"""


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    ranking = json.loads(RANKING_PATH.read_text(encoding="utf-8")) if RANKING_PATH.exists() else {}
    sellout = json.loads(SELLOUT_PATH.read_text(encoding="utf-8")) if SELLOUT_PATH.exists() else {}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    html = build_html(data).replace("{ranking_json}", json.dumps(ranking, ensure_ascii=False))
    html = html.replace("{sellout_json}", json.dumps(sellout, ensure_ascii=False))
    OUTPUT.write_text(html, encoding="utf-8")
    print(OUTPUT.resolve())


if __name__ == "__main__":
    main()



