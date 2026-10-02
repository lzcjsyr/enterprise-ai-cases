# -*- coding: utf-8 -*-
'\nZhao Shang Qi Ye Zhi Shi Ku - Step 3 Tuo Min(He Bing Ban)\nGong Neng:\n1. Shou Ji Hao Da Ma:Bao Liu Qian3Wei+Hou4Wei,Zhong Jian4Wei Yong **** Ti Dai(Ru 135****2816)\n2. Qu Chu Hao Ma Hou De[Huo Yue Hao][Kong Hao][Chen Mo Hao][Fei Huo Yue Hao]Deng Biao Ji,Yi Ji (Xing Ming) Xin Xi\n3. Gu Hua Bu Da Ma,Zi Dong Chai Fen「Qu Hao-Zhu Hao Ma」(Ru 0756-2290201)\n4. Tong Yi Dan Yuan Ge Nei Duo Ge Hao Ma Yong Huan Hang(\n)Fen Ge,Dan Yuan Ge Kai Qi Zi Dong Huan Hang\nShu Ru:Shu Chu/Intermediate Table - Cleaned.csv\nShu Chu:Shu Chu/Business Directory Summary - 1922 Companies - Redacted.xlsx(Han Tuo Min Hou De Zhong Jian Biaocsv)\n\nZhu:Tuo Min Gui Ze Tong Yi Wei Hu Zai phone_utils.py,Yu step4(Yuan Shi Wen Jian Tuo Min)Gong Yong\n'
import os
import numpy as np
import pandas as pd
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

from phone_utils import mobile_text, fixed_text

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Output')
SRC_CSV = os.path.join(OUT_DIR, "Intermediate Table - Cleaned.csv")
OUT_XLSX = os.path.join(OUT_DIR, "Business Directory Summary - 1922 Companies - Redacted.xlsx")
OUT_CSV = os.path.join(OUT_DIR, "Intermediate Table - Cleaned - Redacted.csv")

# - - - De-sensitization of implementation - - -
df = pd.read_csv(SRC_CSV)
df['Contact and Mobile Number'] = df['Contact and Mobile Number'].apply(lambda v: mobile_text(v) or np.nan)
df['Landline'] = df['Landline'].apply(lambda v: fixed_text(v) or np.nan)

# Mid-table after dissensitisation (for other re-use)
df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

# - - Write Excel (three sheets, including an overview of reservations, and a break in format) - - - - -
with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name='Corporate summary')
    summary = pd.DataFrame({
        'Statistics': ['Total number of enterprises', 'Overwrite carriers', '- Yes, United Social Credit Code.', "There's a time to be built.", 'Yes, registered capital.', "It's in the area.",
                   'Number of data sources files'],
        'Value': [len(df), df['Business Park / Incubator'].nunique(),
                df['Unified Social Credit Code'].notna().sum(), df['Date Established'].notna().sum(),
                df['Registered Capital (RMB 10,000s)'].notna().sum(), df['District'].notna().sum(),
                df['Data Source'].nunique()],
    })
    summary.to_excel(writer, index=False, sheet_name='Data overview')
    df.groupby(['Business Park / Incubator', 'District'])['Company Name'].count().to_excel(writer, sheet_name='Carrier x-area distribution')

    # - Format: Numbering Columns automatically line-spinning, vertically top alignment, width
    ws = writer.sheets['Corporate summary']
    headers = [c.value for c in ws[1]]
    wrap_cols = {'Contact and Mobile Number': 34, 'Landline': 30}
    for name, width in wrap_cols.items():
        if name in headers:
            ci = headers.index(name) + 1
            ws.column_dimensions[get_column_letter(ci)].width = width
            for row in ws.iter_rows(min_row=2, min_col=ci, max_col=ci):
                for cell in row:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
    # Qi Ye Ming Cheng & & & & Widen
    if 'Company Name' in headers:
        ws.column_dimensions[get_column_letter(headers.index('Company Name') + 1)].width = 30

print(f"[Dream] Cell phone coded (pre-retain 3 and 4 and middle ****) marked/ Xing Ming")
print(f"[AG/CC] Splitd \"Zone Number - Main Number\", multiple number swaps")
print(f"[Output]{OUT_XLSX}")
print(f"[Output]{OUT_CSV}")

# Sample reconciliation
print('[Sampled Checking]')
for i in [0, 1, 5, 40, 41, 45]:
    print(f"Cell phone number [s]{i}]: {repr(df.loc[i, 'Contact and Mobile Number'])}")
    print(f"♪ The words are ♪{i}]:   {repr(df.loc[i, 'Landline'])}")
