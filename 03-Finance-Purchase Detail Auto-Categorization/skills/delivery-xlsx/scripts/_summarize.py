#!/usr/bin/env python3
'Er Ci Jia Gong:An Shi Cai Fen Lei Hui Zong Jin E -> Cafeteria April Purchase Summary.xlsx\nBing Sheng Cheng Cafeteria April Purchase Analysis.html(Zi Dai SVG Bing Tu,Wu Wai Bu Yi Lai).'
import json
from pathlib import Path
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

BASE = Path('/Users/dielalangli/Desktop/AI training/Traintime AI training/training course/02 Auto-Classification of Procurement')
SRC = BASE / "Cafeteria April Purchases - Categorized.xlsx"
OUT_XLSX = BASE / "Cafeteria April Purchase Summary.xlsx"
OUT_HTML = BASE / "Cafeteria April Purchase Analysis.html"

# Formal colour (in order of subject code)
COLORS = {
    "1403.01.01": "#B03A2E",
    "1403.01.02": "#1E8449",
    "1403.01.03": "#CA6F1E",
    "1403.01.04": "#B7950B",
    "1403.01.05": "#2471A3",
    "1403.01.06": "#6C3483",
    "1403.01.07": "#117A65",
}

# 1. Read and aggregate
wb = load_workbook(SRC, data_only=True)
ws = wb.active
# Headline of the GPS.
hdr = None
for r in range(1, 6):
    vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    if 'Subject code' in vals and 'Name of subject' in vals and 'Amount' in vals:
        hdr = r
        break
assert hdr is not None, 'No tablehead line found'
hmap = {ws.cell(hdr, c).value: c for c in range(1, ws.max_column + 1)}
c_code = hmap['Subject code']; c_subj = hmap['Name of subject']; c_amt = hmap['Amount']

agg = {}  # code -> {subject, amount}
for r in range(hdr + 1, ws.max_row + 1):
    subj = ws.cell(r, c_subj).value
    code = ws.cell(r, c_code).value
    if not subj:
        continue  # Total rows/empty rows
    amt = ws.cell(r, c_amt).value
    try:
        amt = float(amt)
    except (TypeError, ValueError):
        continue
    d = agg.setdefault(code, {"subject": subj, "amount": 0.0})
    d["amount"] += amt

rows = sorted(agg.items(), key=lambda x: x[0])  # Sort by subject code
total = sum(d["amount"] for _, d in rows)

# 2. Write summary xxx -
wb2 = Workbook(); ws2 = wb2.active
ws2.title = 'Summary of acquisitions'
title_font = Font(bold=True, size=14, color="FFFFFF")
hdr_font = Font(bold=True, color="FFFFFF")
hdr_fill = PatternFill("solid", fgColor="2C3E50")
title_fill = PatternFill("solid", fgColor="1F618D")
center = Alignment(horizontal="center", vertical="center")
right = Alignment(horizontal="right", vertical="center")
thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

ws2.merge_cells("A1:D1")
ws2["A1"] = 'Summary of food intakes in April (by food products)'
ws2["A1"].font = title_font; ws2["A1"].fill = title_fill
ws2["A1"].alignment = center
ws2.row_dimensions[1].height = 26

heads = ['Subject code', 'Name of subject', 'Amount (dollars)', 'Percentage']
for j, h in enumerate(heads, start=1):
    c = ws2.cell(2, j, h); c.font = hdr_font; c.fill = hdr_fill
    c.alignment = center; c.border = border

r = 3
for code, d in rows:
    pct = d["amount"] / total * 100
    ws2.cell(r, 1, code).border = border
    ws2.cell(r, 2, d["subject"]).border = border
    ac = ws2.cell(r, 3, round(d["amount"], 2)); ac.number_format = "#,##0.00"; ac.alignment = right; ac.border = border
    pc = ws2.cell(r, 4, round(pct, 2) / 100); pc.number_format = "0.00%"; pc.alignment = right; pc.border = border
    r += 1
# Total rows
ws2.cell(r, 1, "").border = border
ws2.cell(r, 2, 'Total').font = Font(bold=True); ws2.cell(r, 2).border = border
tc = ws2.cell(r, 3, round(total, 2)); tc.number_format = "#,##0.00"; tc.font = Font(bold=True); tc.alignment = right; tc.border = border
pc = ws2.cell(r, 4, 1.0); pc.number_format = "0.00%"; pc.font = Font(bold=True); pc.alignment = right; pc.border = border
for col, w in zip("ABCD", (12, 14, 14, 10)):
    ws2.column_dimensions[col].width = w

wb2.save(OUT_XLSX)
print('Summary xxx:', OUT_XLSX)

# 3. Generate SVG pies -
import math
cx, cy, R = 220, 220, 170
slices = []
start = 0.0
for code, d in rows:
    frac = d["amount"] / total
    end = start + frac
    a0 = start * 2 * math.pi - math.pi / 2
    a1 = end * 2 * math.pi - math.pi / 2
    x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
    x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
    large = 1 if frac > 0.5 else 0
    path = f"M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} A{R:.1f},{R:.1f} 0 {large} 1 {x1:.1f},{y1:.1f} Z"
    # Tab Position (Big Slicing Only)
    mid = (start + end) / 2 * 2 * math.pi - math.pi / 2
    lx, ly = cx + R * 0.62 * math.cos(mid), cy + R * 0.62 * math.sin(mid)
    slices.append({
        "code": code, "subject": d["subject"], "amount": d["amount"],
        "pct": frac * 100, "color": COLORS.get(code, "#888"),
        "path": path, "lx": lx, "ly": ly,
    })
    start = end

paths_svg = "\n".join(
    f'<path d="{s["path"]}" fill="{s["color"]}" stroke="#ffffff" stroke-width="1.5"/>' for s in slices
)
labels_svg = "\n".join(
    f'<text x="{s["lx"]:.1f}" y="{s["ly"]:.1f}" text-anchor="middle" dominant-baseline="middle" '
    f'fill="#ffffff" font-size="13" font-weight="bold">{s["pct"]:.1f}%</text>'
    for s in slices if s["pct"] >= 6
)
legend_html = "\n".join(
    f'<div class="legend-item"><span class="swatch" style="background:{s["color"]}"></span>'
    f'<span class="lg-name">{s["subject"]}</span>'
    f'<span class="lg-amt">¥{s["amount"]:,.2f}</span>'
    f'<span class="lg-pct">{s["pct"]:.2f}%</span></div>'
    for s in slices
)
rows_html = "\n".join(
    f'<tr><td>{s["code"]}</td><td><span class="dot" style="background:{s["color"]}"></span>{s["subject"]}</td>'
    f'<td class="num">¥{s["amount"]:,.2f}</td><td class="num">{s["pct"]:.2f}%</td></tr>'
    for s in slices
)

html = f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
<meta charset=\" UTF-8\"'\"
♪ The world is so full of shit ♪
<title>Analysis of the arrival of April's food
♪ Style ♪
*{ box-sizing: border-box; }}}
  body {{{ margin:0; font-family:\"Microsoft YaHei\",\"PingFang SC\",\"Hiragino Sans GB\",\"Source Han Sans CN\",sans-serif;
         background:#f5f6f8; color:#2c3e50; }}}
  .wrap {{{ max-width:920px; margin:32px auto; background:#fff; border-radius:10px;
          box-shadow:0 2px 12px rgba(0,0,0,.08); padding:36px 44px; }}}
  h1 {{{ font-size:24px; margin:0 0 4px; color:#1f618d; }}}
  .sub {{{ color:#7f8c8d; font-size:14px; margin-bottom:28px; }}}
  .grid {{{ display:flex; gap:40px; align-items:center; flex-wrap:wrap; justify-content:center; }}}
  .chart-box {{{ flex:0 0 auto; }}}
  .legend {{{ flex:1 1 280px; min-width:260px; }}}
  .legend-item {{{ display:flex; align-items:center; padding:9px 6px; border-bottom:1px solid #eef0f2; font-size:14px; }}}
  .swatch {{{ width:14px; height:14px; border-radius:3px; margin-right:10px; flex:0 0 auto; }}}
  .lg-name {{{ flex:1 1 auto; }}}
  .lg-amt {{{ margin-left:auto; margin-right:18px; color:#555; font-variant-numeric:tabular-nums; }}}
  .lg-pct {{{ width:64px; text-align:right; font-weight:bold; color:#2c3e50; font-variant-numeric:tabular-nums; }}}
  table {{{ width:100%; border-collapse:collapse; margin-top:30px; font-size:14px; }}}
  th,td {{{ padding:10px 12px; border-bottom:1px solid #eef0f2; text-align:left; }}}
  th {{{ background:#1f618d; color:#fff; font-weight:600; }}}
  td.num, th.num {{{ text-align:right; font-variant-numeric:tabular-nums; }}}
  tr:last-child td {{{ border-bottom:none; }}}
  .dot {{{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px; vertical-align:middle; }}}
  tfoot td {{{ font-weight:bold; border-top:2px solid #d5d9dd; }}}
  .foot {{{ margin-top:18px; font-size:12px; color:#95a5a6; text-align:center; }}}</style>
</head >
♪ Hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey, hey.
♪ Div class ♪
<h1 >Analysis of arrival in April
<div class= \"sub\" >. Data period: April 2026. Total amount of incoming: ¥{total:,.2f}</div>
    <div class=\"grid\">
      <div class=\"chart-box\">
        <svg width=\"440\" height=\"440\" viewBox=\"0 0 440 440\" xmlns=\"http://www.w3.org/2000/svg\">
          {paths_svg}
          {labels_svg}
          <circle cx=\"{cx}\" cy=\"{cy}\" r=\"62\" fill=\"#ffffff\"/>
          <text x=\"{cx}\" y=\"{cy-6}\" text-anchor=\"middle\" font-size=\"14\" fill=\"# 7f8c8d\"'The total amount of the goods received is </text>
<text x=\"{cx}\" y=\"{cy+18}\" text-anchor=\"middle\" font-size=\"20\" font-weight=\"bold\" fill=\"#2c3e50\">¥{total:,.0f}</text>
        </svg>
      </div>
      <div class=\"legend\">
        {legend_html}</div>
</div>
- I'm sorry.
- I'm sorry.
Subject code < t > < /th > Cadastre < /th > < num > Amount (dollar) < /th > < class > < num > Share < /th > < /t >
</thead >
- No, no, no, no.{rows_html}</tbody >
♪ tfoot ♪
♪ td ♪ td ♪ td ♪ td class ♪ num ♪{total:,.2f}</td><td class=\"num\">100.00%</td></tr>
      </tfoot>
    </table>
    <div class=\"foot\">Shu Ju Lai Yuan:Cafeteria April Purchases - Categorized.xlsx · You delivery-xlsx Skill Fen Lei Hou Er Ci Hui Zong</div>
  </div>
</body>
</html>
"""
OUT_HTML.write_text(html, encoding="utf-8")
print('Analyse HTML:', OUT_HTML)

# Output validation summary
print('--- Summarizing verification ---')
for code, d in rows:
    print(f"  {code} {d['subject']}: ¥{d['amount']:,.2f} ({d['amount']/total*100:.2f}%)")
print(f"Total: ¥{total:,.2f}")
