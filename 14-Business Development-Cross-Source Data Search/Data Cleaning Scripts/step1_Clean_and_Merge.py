# -*- coding: utf-8 -*-
'Rendering Enterprise Knowledge Bank - Data cleansing Step 1\nFunction: Consolidation of 7 source files (10 sets), harmonization of schema, standardization of formats, and removal of Heavy'
import pandas as pd
import numpy as np
import os, glob, re

SRC = '/Users/dielalangli/Desktop/AI training/Train/06 Recruit data/raw data'
OUT_DIR = '/Users/dielalangli/Desktop/AI training/Train/06 Recruit data/output'
os.makedirs(OUT_DIR, exist_ok=True)

# - - Unified Schema - -
COLS = [
    'Company Name', 'Unified Social Credit Code', 'Legal Representative', 'Contact and Mobile Number', 'Landline', 'Email',
    'Date Established', 'Registered Capital (RMB 10,000s)', 'Paid-in Capital (RMB 10,000s)', 'Employees Enrolled in Social Insurance',
    'National Industry Classification - Major Category', 'National Industry Classification - Subcategory', 'Business Park / Incubator', 'District',
    'Registered Address', 'Mailing Address', 'Latest Relocation Date', 'Company Profile', 'Data Source'
]

def clean_str(v):
    'Clean String: Go to Tab/Line Break/Line End Space/ Merge Additional Space'
    if pd.isna(v):
        return np.nan
    s = str(v).replace("\t", "").replace("\n", "").replace("\r", "").strip()
    s = re.sub(r"\s+", " ", s)
    return s if s else np.nan

def parse_amount(v):
    "RMB 300.0 million' '50 million' '50 million' '20' '150 million ♪ I'm not sure ♪"
    if pd.isna(v):
        return np.nan
    s = str(v).strip().replace(",", "").replace("，", "")
    m = re.search('([\\d.] ) \\ ( trillions of dollars and millions of dollars)?', s)
    if not m:
        return np.nan
    num = float(m.group(1))
    unit = m.group(2) or ""
    if unit in ('Billiones.', 'Billions.'):
        return round(num * 10000, 2)
    if unit in ('Thousand', 'Ten thousand dollars.'):
        return round(num, 2)
    return round(num, 2)  # No unit is processed at a million dollars.

def parse_count(v):
    "Social security population '1 (2024) ' - > 1"
    if pd.isna(v):
        return np.nan
    m = re.search(r"(\d+)", str(v))
    return int(m.group(1)) if m else np.nan

def parse_date(v):
    if pd.isna(v):
        return np.nan
    try:
        return pd.to_datetime(str(v).strip(), errors="coerce").strftime("%Y-%m-%d")
    except Exception:
        return np.nan

def extract_district(addr):
    'Location of location: Cheonzhou District/Gin Bay District/Domen District/Gahno Xin, etc.'
    if pd.isna(addr):
        return np.nan
    s = str(addr)
    m = re.search('Pearlhead City ([ \\\\] u4e00-\\ u9fa5♪ 2 ♪ 6 ♪ (? ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪', s)
    if m:
        return 'Zhuhai City' + m.group(1)
    m2 = re.search('([\\ u4e00-\\ u9fa5♪ 2 ♪ 6 ♪ (? ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪ New ♪ ♪', s)
    return m2.group(1) if m2 else np.nan

# - - - Read & map - - -
frames = []
def add_frame(df, carrier, source, colmap):
    'Colmap: Target List - > Source List (or Noone)'
    row = pd.DataFrame(index=df.index, columns=COLS)
    for tgt, src in colmap.items():
        if src is not None and src in df.columns:
            row[tgt] = df[src]
    row['Business Park / Incubator'] = carrier
    row['Data Source'] = source
    frames.append(row)

files = sorted(glob.glob(os.path.join(SRC, "*.xlsx")))

for f in files:
    base = os.path.basename(f)
    xl = pd.ExcelFile(f)
    for sn in xl.sheet_names:
        df = pd.read_excel(f, sheet_name=sn)
        df.columns = [str(c) for c in df.columns]

        if base == "China-Israel Accelerator Company List - 2026-07-15.xlsx":
            add_frame(df, 'Center by Accelerator', base, {
                'Company Name': 'Company Name', 'Legal Representative': 'Legal persons', 'Contact and Mobile Number': 'Contact and Mobile Number',
                'Employees Enrolled in Social Insurance': 'Employees Enrolled in Social Insurance', 'National Industry Classification - Major Category': 'National standard industry (industry subcategory)',
                'Registered Capital (RMB 10,000s)': 'Registered funds', 'Latest Relocation Date': 'Latest Relocation Date',
                'Company Profile': 'Company Profile', 'Registered Address': 'Registered Address', 'Mailing Address': 'Mailing Address', 'Landline': 'Landline'})
        elif base == "Jicheng - 2026-07-31.xlsx":
            carrier = f"Scramble-{sn}"
            add_frame(df, carrier, base, {
                'Company Name': 'Company Name', 'Legal Representative': 'Legal persons', 'Contact and Mobile Number': 'Contact and Mobile Number',
                'Landline': 'Landline', 'National Industry Classification - Subcategory': 'National standard industry (segment)',
                'Date Established': 'Date Established', 'Latest Relocation Date': 'Latest Relocation Date', 'Company Profile': 'Company Profile',
                'Employees Enrolled in Social Insurance': 'Employees Enrolled in Social Insurance', 'Registered Capital (RMB 10,000s)': 'Registered Capital', 'Paid-in Capital (RMB 10,000s)': 'Paid-in Capital',
                'Mailing Address': 'Mailing Address', 'Unified Social Credit Code': 'Unified Social Credit Code' if 'Unified Social Credit Code' in df.columns else None})
        elif base == "Cloud Valley Business List - 2026-08-03.xlsx":
            add_frame(df, 'The Hollow Valley.', base, {
                'Company Name': 'Company Name', 'Legal Representative': 'Legal persons', 'Contact and Mobile Number': 'Contact and Mobile Number',
                'Landline': 'Landline', 'National Industry Classification - Subcategory': 'National standard industry (segment)',
                'Date Established': 'Date Established', 'Latest Relocation Date': 'Latest Relocation Date', 'Company Profile': 'Company Profile',
                'Employees Enrolled in Social Insurance': 'Employees Enrolled in Social Insurance', 'Registered Capital (RMB 10,000s)': 'Registered Capital', 'Paid-in Capital (RMB 10,000s)': 'Paid-in Capital',
                'Mailing Address': 'Mailing Address', 'Unified Social Credit Code': 'Unified Social Credit Code'})
        elif base == "Ruifeng Building - 2026-08-06.xlsx":
            add_frame(df, 'Raffon Building.', base, {
                'Company Name': 'Company Name', 'Legal Representative': 'Legal persons', 'Contact and Mobile Number': 'Contact and Mobile Number',
                'Landline': 'Landline', 'Email': 'Email', 'National Industry Classification - Subcategory': 'National standard industry (segment)',
                'Date Established': 'Date Established', 'Latest Relocation Date': 'Latest Relocation Date', 'Company Profile': 'Company Profile',
                'Employees Enrolled in Social Insurance': 'Employees Enrolled in Social Insurance', 'Registered Capital (RMB 10,000s)': 'Registered Capital', 'Paid-in Capital (RMB 10,000s)': 'Paid-in Capital'})
        elif base == "Meixing Industrial Park - 2026-08-06.xlsx":
            add_frame(df, 'America Industries.', base, {
                'Company Name': 'Company Name', 'Legal Representative': 'Legal persons', 'Contact and Mobile Number': 'Contact and Mobile Number',
                'Landline': 'Landline', 'Email': 'Email', 'National Industry Classification - Subcategory': 'National standard industry (segment)',
                'Date Established': 'Date Established', 'Latest Relocation Date': 'Latest Relocation Date', 'Company Profile': 'Company Profile',
                'Employees Enrolled in Social Insurance': 'Employees Enrolled in Social Insurance', 'Registered Capital (RMB 10,000s)': 'Registered Capital', 'Paid-in Capital (RMB 10,000s)': 'Paid-in Capital',
                'Mailing Address': 'Mailing Address', 'Unified Social Credit Code': 'Unified Social Credit Code'})
        elif base == "Nanping Technology Park.xlsx":
            add_frame(df, 'South Screen Technology Park', base, {
                'Company Name': 'Company Name', 'Legal Representative': 'Legal persons', 'Contact and Mobile Number': 'Contact and Mobile Number',
                'Landline': 'Landline', 'Employees Enrolled in Social Insurance': 'Employees Enrolled in Social Insurance', 'Latest Relocation Date': 'Latest Relocation Date',
                'Registered Address': 'Registered Address', 'Mailing Address': 'Mailing Address', 'Company Profile': 'Remarks'})
        elif base == "Registered Enterprises in Fuxi Industrial Zone.xlsx":
            # Special: Title in line 1, heading to row0(= actual line 2)
            if str(df.columns[0]).startswith('Forkley Industrial District'):
                header_row = df.iloc[0]
                df = df.iloc[1:].copy()
                df.columns = [str(h) for h in header_row]
            add_frame(df, 'Forkley Industrial District', base, {
                'Company Name': 'Name of the park enterprise', 'Registered Capital (RMB 10,000s)': 'Registered funds',
                'Date Established': 'Registration Time', 'Company Profile': 'Business Scope'})

raw = pd.concat(frames, ignore_index=True)
print(f"[Read] Number of lines before merging (including repetition):{len(raw)}")

# - - - Purge - - - Cleaning
for c in ['Company Name', 'Unified Social Credit Code', 'Legal Representative', 'Contact and Mobile Number', 'Landline', 'Email',
          'National Industry Classification - Major Category', 'National Industry Classification - Subcategory', 'Business Park / Incubator', 'District', 'Registered Address', 'Mailing Address', 'Company Profile']:
    raw[c] = raw[c].apply(clean_str)
for c in ['Registered Capital (RMB 10,000s)', 'Paid-in Capital (RMB 10,000s)']:
    raw[c] = raw[c].apply(parse_amount)
raw['Employees Enrolled in Social Insurance'] = raw['Employees Enrolled in Social Insurance'].apply(parse_count)
for c in ['Date Established', 'Latest Relocation Date']:
    raw[c] = raw[c].apply(parse_date)

# Retrieval (priority registered address, secondary address)
raw['District'] = raw.apply(lambda r: extract_district(r['Registered Address']) or extract_district(r['Mailing Address']), axis=1)

# - - Repeated checks in the cloud valley - -
yxg_a = raw[raw['Data Source'] == "Jicheng - 2026-07-31.xlsx"]
yxg_b = raw[raw['Data Source'] == "Cloud Valley Business List - 2026-08-03.xlsx"]
print(f"[Wind Creek Valley]{len(yxg_a)}Independent ={len(yxg_b)}Full overlap of business name ={len(set(yxg_a['Company Name']) & set(yxg_b['Company Name']))}")

# - - - Go to the heavy weight (by Qi Ye Ming Cheng) - - -
dup_mask = raw['Company Name'].duplicated(keep="first")
dup_df = raw[dup_mask]
raw_dedup = raw[~dup_mask].copy()
print(f"[Drive] Repeat business{dup_mask.sum()}Home (reservation first appeared)")

# Repeat distribution
print('[Repeated breakdown -- by carrier]')
print(raw[dup_mask].groupby('Business Park / Incubator')['Company Name'].count().to_string())

# Missing Rate
print('[Leaves after cleaning]')
miss = (raw_dedup.isnull().mean() * 100).round(1)
print(dict(miss[miss > 0]))

# - - to preserve the intermediate results - - -
raw_dedup.to_csv(os.path.join(OUT_DIR, "Intermediate Table - Cleaned.csv"), index=False, encoding="utf-8-sig")
print(f"\\n[saved] intermediate table:{OUT_DIR}/Intermediate Table - Cleaned.csv  Gong{len(raw_dedup)}Home.")
print('[statisticalized by carrier]')
print(raw_dedup.groupby('Business Park / Incubator')['Company Name'].count().to_string())
