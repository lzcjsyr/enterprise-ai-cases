# -*- coding: utf-8 -*-
'Rendering Enterprise Knowledge Bank - Step 4 Source Sensitization\nFunction: To generate a copy of each Excel under raw data/ (structure, table head, other columns completely unchanged), only to process telephone columns:\n- Cell phone number: 4 in **** dial number (135****2816), remove signs such as [activated number] [empty number] (Xing Ming)\n- Scramble: uncoded, uncoded, as "Zone Number - Main Number" (0756-2290201)\n- Multiple numbers in the same cell: toggle + line breaks; number columns automatically open cells Invert Okay.\nInput: Original data/*.xlsx (no change to original document)\nOutput: Original data desensitization/ <original filename>\n\nNote: Dissensitization rule uniform maintained at phone utils.py, with step3(Multiple dissensitization)'
import os
import glob
import copy
import openpyxl
from openpyxl.utils import get_column_letter

from phone_utils import mobile_text, fixed_text

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE, 'Original data')
OUT_DIR = os.path.join(BASE, 'Source data dissensitization')
os.makedirs(OUT_DIR, exist_ok=True)

LINE_H = 15.0          # About 15 pounds per line.
MAX_COL_W = 26         # Numberbar Maximum Limit


def find_phone_cols(ws):
    "Find a watch header in the first three lines and return (table first line, {column: 'mobile'/ 'fixed'})"
    for r in range(1, 4):
        cols = {}
        for c in range(1, ws.max_column + 1):
            v = ws.cell(r, c).value
            if v is None:
                continue
            s = str(v)
            if 'Cell phone.' in s:
                cols[c] = "mobile"
            elif 'Landline' in s:
                cols[c] = "fixed"
        if "mobile" in cols.values():
            return r, cols
    return None, {}


def process_sheet(ws):
    'Handle a single shell line, return (number of dialphones, split the number of words, clear the empty number)'
    hrow, cols = find_phone_cols(ws)
    if not hrow:
        return None
    n_mobile = n_fixed = n_clean = 0
    for r in range(hrow + 1, ws.max_row + 1):
        max_lines = 1
        for c, kind in cols.items():
            cell = ws.cell(r, c)
            old = cell.value
            if old is None:
                continue                      # Vacuum, don't move.
            if str(old).strip() == "":
                if str(old) != "":            # \t Unvisible Decontamination Value: Empty
                    cell.value = None
                    n_clean += 1
                continue
            new = mobile_text(old) if kind == "mobile" else fixed_text(old)
            cell.value = new                  # No valid number of dirty data - emptied
            al = copy.copy(cell.alignment)    # Keep original alignment, add new lines only
            al.wrap_text = True
            al.vertical = "top"
            cell.alignment = al
            if new is None:
                n_clean += 1
                continue
            if kind == "mobile":
                n_mobile += 1
            else:
                n_fixed += 1
            max_lines = max(max_lines, new.count("\n") + 1)
        # Line high: complete display when multiple numbers
        if max_lines > 1:
            cur = ws.row_dimensions[r].height or 0
            ws.row_dimensions[r].height = max(cur, LINE_H * max_lines)
    # Column width: Adapting to text in a maximum row (broad, not narrow)
    for c in cols:
        letter = get_column_letter(c)
        longest = 0
        for r in range(hrow + 1, ws.max_row + 1):
            v = ws.cell(r, c).value
            if isinstance(v, str):
                longest = max(longest, max((len(x) for x in v.split("\n")), default=0))
        need = min(longest + 2, MAX_COL_W)
        ws.column_dimensions[letter].width = max(ws.column_dimensions[letter].width or 0, need)
    return n_mobile, n_fixed, n_clean


def main():
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*.xlsx")))
    print(f"[Scan] Raw data{len(files)}File - > Output to Original Data Desensitization/")
    for f in files:
        name = os.path.basename(f)
        wb = openpyxl.load_workbook(f)        # Full load, keep all formats
        total = [0, 0, 0]
        no_phone_sheets = []
        for sn in wb.sheetnames:
            ws = wb[sn]
            r = process_sheet(ws)
            if r is None:
                no_phone_sheets.append(sn)
            else:
                for i, x in enumerate(r):
                    total[i] += x
        out = os.path.join(OUT_DIR, name)
        wb.save(out)
        wb.close()
        note = f"(No telephone line:{'/'.join(no_phone_sheets)}）" if no_phone_sheets else ""
        print(f"  √ {name}{note}:  Cell phone.{total[0]}Gogh, the word.{total[1]}Grill"
              + (f", Empty the dirty data{total[2]}Grill" if total[2] else ""))
    print(f"\n [completed] co-generated{len(files)}A dissensitized copy:{OUT_DIR}")


if __name__ == "__main__":
    main()
