# -*- coding: utf-8 -*-
'Rendering the Enterprise Knowledge Bank - Data cleansing Step 2\nFunction: Check check to check the results back to fill + take logical corrections in the area + generate final delivery to Excel'
import pandas as pd
import numpy as np
import os, re

OUT_DIR = '/Users/dielalangli/Desktop/AI training/Train/06 Recruit data/output'
df = pd.read_csv(os.path.join(OUT_DIR, "Intermediate Table - Cleaned.csv"))

# - - - To attempt to check back and fill (based on the results of eight sample tests) - - -
QCC_FILL = {
    'Yi Zhang Tong Shu Zi Technology (Zhuhai) Co., Ltd.': {'Unified Social Credit Code': "91440402MA7HUW591Y", 'Paid-in Capital (RMB 10,000s)': 149.0,
        'National Industry Classification - Subcategory': 'Information systems integration services', 'Registered Address': 'Road 168, Chau Cai, Pearl Sea, 5th Floor, 5th Floor, 5th Floor, 5th Floor, Cloud Creek Valley Digital Estate, B-Mey Creek Business Square',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for consistency on the two elements.'},
    'Shang Jiao Da(Zhuhai) Intelligent Technology Co., Ltd.': {'Paid-in Capital (RMB 10,000s)': 107.69,
        'National Industry Classification - Subcategory': 'Technology extension services', 'Registered Address': 'Two 1005 offices at Mae Creek Business Square, 168 Chau Quan District, Pearl Sea',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for consistency on the two elements.'},
    'Hua Min Education Technology (Zhuhai) Co., Ltd.': {'Unified Social Credit Code': "91440400MA5464Q09F", 'Date Established': "2019-12-10",
        'National Industry Classification - Subcategory': 'Other software development', 'Registered Address': "188 New Sa'il, China Bay, Chuhai City, 15th Floor 504-1",
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for credit code completion; register high-novel area (unlike the address of the Chan Chong region)'},
    'Shi Min Ban Dao Ti Ji Shu(Zhuhai) Co., Ltd.': {'Unified Social Credit Code': "91440402MAE3QAGC4P",
        'National Industry Classification - Subcategory': 'Integrated circuit design', 'Registered Address': '1323, 1st industrial building, Cheonhai, 828th floor, May Boulevard Road',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for complete credit codes; reconciled registered capital/found time'},
    'Yuan He Chuang Xin Technology (Zhuhai) Co., Ltd.': {'Unified Social Credit Code': "91440402MADBHLD11J",
        'National Industry Classification - Subcategory': 'Other software development', 'Registered Address': '1st floor, 401st floor, B1st, 19th floor, Yanhuku Road, Chuhai City',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for complete credit codes;registered reconciliation'},
    'Hua Peng Jiu Dian Management (Zhuhai) Co., Ltd.': {'Unified Social Credit Code': "91440402MADAW8AT7R",
        'National Industry Classification - Subcategory': 'Management services of other organizations', 'Registered Address': '33 Trixie Fairy Street, Pearl Sea City, First Floor, A02.',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for credit code complete.'},
    'Zhong Zhou Bao Shun Ren Li Zi Yuan Co., Ltd.': {'Unified Social Credit Code': "91440400MACH9RY70Q", 'Registered Capital (RMB 10,000s)': 5200.0, 'Date Established': "2023-05-22",
        'National Industry Classification - Subcategory': 'Human resources services', 'Registered Address': 'South-Standing Science and Technology Park, Chuhai, north of the building, is located in room 207, east of Industrial Park 2.',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check for full credit code + registered capital 52 million + start-up time'},
    'Zhuhai Ling Zheng Jin Shu Cai Liao Co., Ltd.': {'Unified Social Credit Code': "91440400MA4UKKUX6B", 'Legal Representative': 'Guo Jun Jie',
        'National Industry Classification - Subcategory': 'Wholesale', 'Registered Address': '12, 106 plants, 615 Wallway Road, former mountain industrial zone, Pearl Sea City',
        'Registration status': 'Survivors (in camp, open, registered)', 'Verify Remarks': 'Check to complete the credit code + legal person (missing source table)'},
}

def backfill(row):
    'Filling down the missing field to the business in the hit.'
    name = row['Company Name']
    if name not in QCC_FILL:
        return row
    for k, v in QCC_FILL[name].items():
        if k == 'Verify Remarks':
            row['Verify Remarks'] = v
        elif pd.isna(row[k]) or k == 'Registration status':
            row[k] = v
    return row

df['Verify Remarks'] = np.nan
df['Registration status'] = np.nan
df = df.apply(backfill, axis=1)

# - - - in the region (white list + key map of park) - - -
DISTRICT_PATTERNS = [
    ('The harmonium.', ['The harmonium.']),
    ('Gao Xin District', ['Gao Xin', 'Tang Jia Wan', 'Kim Ting.']),
    ('Xiangzhou District', ['Shanko!', 'Southscreen', 'Front Mountain', 'Kenpei', 'Gida.', 'Wan!', 'Trish.', 'Mae-hwa.', 'Fengshan', 'Lion Mountain.', 'Maybrook.']),
    ('Gulf of Gold', ['Golden Bay.', 'Three.', 'Red flag', 'Paings', 'South Water']),
    ('Door area.', ['Door!', 'Ii-Sashi.', 'White beak.', 'Business.', 'Linzhou.']),
]

def extract_district_v2(addr):
    if addr is None or (isinstance(addr, float) and pd.isna(addr)):
        return None
    s = str(addr)
    # 1) Accurate model: XX Zone of Pearlhead / XX Zone of Pearlhead / New Zone of Pearlhead /
    m = re.search('Pearl Sea (Zone of Zhuo Zhongqin, Xianzhou, Xianxiang Zone, Xianxiang Zone, Xianxiang Zone)', s)
    if m:
        return {'The new Zone of the Transon.': 'The harmonium.', 'Transon Zone of Deep Zone': 'The harmonium.'}.get(m.group(1), m.group(1))
    # 2) Chu Hae Xin District (no "city")
    m = re.search('Chuhai (New Zoning Zone, High New Zone)', s)
    if m:
        return 'Gao Xin District' if m.group(1) == 'Gao Xin District' else 'The harmonium.'
    # 3) Park/town key word mapping
    for district, kws in DISTRICT_PATTERNS:
        for kw in kws:
            if kw in s:
                return district
    return None

def pick_district(r):
    v = extract_district_v2(r['Registered Address'])
    if v:
        return v
    return extract_district_v2(r['Mailing Address'])

df['District'] = df.apply(pick_district, axis=1)

# - - Validation of results statistics   - -
filled = df[df['Verify Remarks'].notna()]
print(f"[Examining] Backfilled/checked{len(filled)}Home.")
print('Details:')
for _, r in filled.iterrows():
    print(f"    {r['Company Name'][:22]:24s} | {r['Verify Remarks']}")

print(f"\n [in] region successfully extracted{df['District'].notna().sum()} / {len(df)}Home ({(df['District'].notna().mean()*100):.1f}%)")
print(df['District'].value_counts().to_string())

# - - - Final listing order - - -
FINAL_COLS = ['Company Name', 'Unified Social Credit Code', 'Legal Representative', 'Contact and Mobile Number', 'Landline', 'Email',
              'Date Established', 'Registered Capital (RMB 10,000s)', 'Paid-in Capital (RMB 10,000s)', 'Employees Enrolled in Social Insurance',
              'National Industry Classification - Major Category', 'National Industry Classification - Subcategory', 'Business Park / Incubator', 'District',
              'Registered Address', 'Mailing Address', 'Latest Relocation Date', 'Company Profile',
              'Registration status', 'Verify Remarks', 'Data Source']
df = df[FINAL_COLS].copy()

# - - - Final Excel - - -
xlsx_path = os.path.join(OUT_DIR, "Business Directory Summary - 1922 Companies.xlsx")
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name='Corporate summary')
    # Overview
    summary = pd.DataFrame({
        'Statistics': ['Total number of enterprises', 'Overwrite carriers', '- Yes, United Social Credit Code.', "There's a time to be built.", 'Yes, registered capital.', "It's in the area.",
                   'Check check/compensation', 'Number of data sources files'],
        'Value': [len(df), df['Business Park / Incubator'].nunique(),
                df['Unified Social Credit Code'].notna().sum(), df['Date Established'].notna().sum(),
                df['Registered Capital (RMB 10,000s)'].notna().sum(), df['District'].notna().sum(),
                len(filled), df['Data Source'].nunique()],
    })
    summary.to_excel(writer, index=False, sheet_name='Data overview')
    df.groupby(['Business Park / Incubator', 'District'])['Company Name'].count().to_excel(writer, sheet_name='Carrier x-area distribution')

print(f"\\n[output]{xlsx_path}")
print(f"Total number of enterprises:{len(df)}• Carrier:{df['Business Park / Incubator'].nunique()}There's a code:{df['Unified Social Credit Code'].notna().sum()}• Area:{df['District'].notna().sum()}")
