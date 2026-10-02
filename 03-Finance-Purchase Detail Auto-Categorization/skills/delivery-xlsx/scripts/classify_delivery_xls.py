#!/usr/bin/env python3
'Excel Sales Subclass - AI Driven I/O Tool (Flexible Version).\n\nDesign principles: Scripts do not make any "understanding/judgement" but read, write, extract.\nAll the formats are understood (the line header, the line name, the line and the new column) by AI.\nAI passed the conclusions through parameters/maps JSON to the script, which faithfully implements.\n\nSuborder:\nread - Give the whole table \'s shape and the original shape of the previous rows to AI for AI to understand format\nNames - Draws a unique name by the list of titles in the front row of the table specified by AI (full scan)\nWriter - Press the map given by AI JSON, write the classification back to Excel'

import io, json, sys, re, argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Protocol, cast

import importlib

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
import openpyxl


# xlrd no type stakes, here is the minimum Protocol to describe the interface that the script actually used to avoid the import module returning to Any.
class _XlrdCell(Protocol):
    value: object

class _XlrdSheet(Protocol):
    nrows: int
    ncols: int
    def cell(self, row: int, col: int) -> _XlrdCell: ...

class _XlrdBook(Protocol):
    def sheet_by_index(self, n: int) -> _XlrdSheet: ...

class _XlrdModule(Protocol):
    def open_workbook(self, filename: str, logfile: object = ...) -> _XlrdBook: ...


# ---------------------------------------------------------------------------
# Standardize the name - remove the specification/unit/bracket to facilitate focus items during AI classification Category
# ---------------------------------------------------------------------------

def normalize_name(name: str) -> str:
    text = name.strip()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"^[（(][^）)]+[）)]", "", text)
    prev = ""
    while text != prev:
        prev = text
        text = re.sub(
            '^(.*) [x*x/-\\d\\s]+ (?: kg|g|ml|l|lShenglShenglShengsShengs$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$$$$$)',
            r"\1", text, flags=re.IGNORECASE,
        )
        text = re.sub(
            '^(.*)\\d+(?: kg|g|ml|l|l|lShengsShengs$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$s$$s$$s$$$$$$s$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',
            r"\1", text, flags=re.IGNORECASE,
        )
        text = re.sub('^(.*)/(?:?? * *?? *??? * * * $ $ $ $ $ $ $ * * $ $ * $ $ $ $? $ $ $??????????????????????????????????????????????????????????????????????????????????????????', r"\1", text)
        text = re.sub(r"^(.*)[xX*×/]\d+$", r"\1", text)
    text = re.sub(
        '\\d+(?: \\d+) * (?: kg|ml|l*l*l*l*l*s*s*s*s*s*s*s*s*s*s*s*s*s*s*s*s*s*s*s*s***************************???????**??*??????????????*???????????????????????????????????*???????????*????Sheng**?*?**?*****************Sheng Sheng???????******????????????????????????????????????',
        "", text, flags=re.IGNORECASE,
    )
    text = re.sub(r'[（()）\-+*#/"]', "", text)
    return text


# ---------------------------------------------------------------------------
# Excel Read (pressure xlrd noise)
# ---------------------------------------------------------------------------

def _read(path: Path) -> list[list[object]]:
    ext = path.suffix.lower()
    if ext == ".xls":
        try:
            xlrd_mod = cast(_XlrdModule, cast("object", importlib.import_module("xlrd")))
        except ImportError:
            raise RuntimeError('Read.xls needs xlrd, install: pip install xlrd') from None
        # Open workbook of xlrd bound the logfile default to the then sys.stdout, when the function is defined.
        # So re-direction only is not possible " OLE2  "inconsistency" like a police alarm,
        # You have to go in the logfile in a visible way, or the alarm will get into stdout pollution JSON output.
        sink = io.StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = sink
        try:
            wb = xlrd_mod.open_workbook(str(path), logfile=sink)
        finally:
            sys.stdout, sys.stderr = old_out, old_err
        sheet = wb.sheet_by_index(0)
        return [[sheet.cell(r, c).value for c in range(sheet.ncols)]
                for r in range(sheet.nrows)]
    elif ext == ".xlsx":
        wb = openpyxl.load_workbook(path, data_only=True)
        sheet = wb.active
        return [list(row) for row in sheet.iter_rows(values_only=True)] if sheet else []
    else:
        raise ValueError(f"Unsupported file type:{ext}(only support.xls/.xlsx)")


def _cell(v: object) -> object:
    'Convert cell values to AI friendly JSON format.'
    if v is None:
        return None
    if isinstance(v, float):
        # Integer (e. g. 12.0) to int, avoiding AI confusion
        return int(v) if v.is_integer() else v
    if isinstance(v, (int,)):
        return v
    return str(v).strip()


# ---------------------------------------------------------------------------
# read - Hand over table shape and sample to AI, by AI judgement format (script is not ticking)
# ---------------------------------------------------------------------------

PREVIEW_LIMIT = 60  # Here, let's go to AI, see the maximum number of lines.


def cmd_read(input_file: str) -> int:
    path = Path(input_file).expanduser().resolve()
    if not path.is_file():
        print(f"ERRO: File does not exist{path}", file=sys.stderr)
        return 1

    rows = _read(path)
    total_cols = max((len(r) for r in rows), default=0)

    # Only as a "tip" output, AI can be adopted or ignored; scripts do not make any hard judgement based on this.
    suggestions = _suggest_header(rows)

    preview = [
        {"row_index": i, "cells": [_cell(c) for c in rows[i]]}
        for i in range(min(len(rows), PREVIEW_LIMIT))
    ]

    result = {
        "input_file": str(path),
        "total_rows": len(rows),
        "total_cols": total_cols,
        "suggestions": suggestions,
        "preview_rows": preview,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


# Classic keywords, from high to low by specificity.
# Reason for the layering: column like "unit name" "client name" also contains "name" if only a loose substring matches,
# They'll hit them first and miss the real trade names. So sweep the strong signals and then back them down.
_NAME_KEYWORDS: tuple[tuple[str, ...], ...] = (
    ('Trade names', 'Name of goods', 'Name of the material', 'Inventory name', 'Product name', 'Practising Name'),
    ('Commodities', 'Goods', 'Materials', 'Inventory'),
    ('Name',),
)


def _suggest_header(rows: list[list[object]]) -> dict[str, int]:
    'Try to give AI a starting point; return to one if you can\'t find it, never miss it.\n\nNote: This is just a "tip" and the final headline and character list must be AI based on a sample.\nWeak keywords can easily be mischaracterised in the "unit name" column, not directly accepted.'
    for i, row in enumerate(rows):
        if not row:
            continue
        if len([c for c in row if c is not None and str(c).strip()]) < 2:
            continue
        for tier in _NAME_KEYWORDS:
            hit = next((j for j, c in enumerate(row)
                        if c is not None and any(k in str(c) for k in tier)), -1)
            if hit >= 0:
                return {"header_row": i, "name_col": hit}
    return {"header_row": -1, "name_col": -1}


# ---------------------------------------------------------------------------
# Names - Draws a unique name by the list of titles in the front row of the table specified by AI (full scan)
# ---------------------------------------------------------------------------

def cmd_names(input_file: str, header_idx: int, name_col: int) -> int:
    path = Path(input_file).expanduser().resolve()
    if not path.is_file():
        print(f"ERRO: File does not exist{path}", file=sys.stderr)
        return 1
    if header_idx < 0 or name_col < 0:
        print('ERRO: Must provide --header-idx and --name-col', file=sys.stderr)
        return 1

    rows = _read(path)
    if header_idx >= len(rows):
        print(f"ERROR: header_idx={header_idx}Over and above total lines{len(rows)}", file=sys.stderr)
        return 1

    seen: dict[str, str] = {}  # normalized → original
    for r in range(header_idx + 1, len(rows)):
        row = rows[r]
        if not row or name_col >= len(row):
            continue
        name = str(row[name_col]).strip() if row[name_col] is not None else ""
        if not name:
            continue
        n = normalize_name(name)
        if n and n not in seen:
            seen[n] = name

    result = {
        "input_file": str(path),
        "header_idx": header_idx,
        "col_name_idx": name_col,
        "data_rows": len(rows) - header_idx - 1,
        "unique_count": len(seen),
        "unique_names": [
            {"normalized": n, "original": o} for n, o in seen.items()
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Writer - Map by AI JSON Rewrite Classification
# ---------------------------------------------------------------------------

def cmd_write(input_file: str, output_file: str, map_file: str) -> int:
    input_path = Path(input_file).expanduser().resolve()
    output_path = Path(output_file).expanduser().resolve()
    map_path = Path(map_file).expanduser().resolve()

    if not input_path.is_file():
        print(f"ERRO: Input file does not exist{input_path}", file=sys.stderr)
        return 1
    if not map_path.is_file():
        print(f"ERRO: Category Map File does not exist{map_path}", file=sys.stderr)
        return 1

    with open(map_path, encoding="utf-8") as f:
        mapping = json.load(f)

    classifications: dict[str, dict[str, str]] = mapping.get("classifications", {})
    header_idx: int = mapping.get("header_idx", -1)
    col_name: int = mapping.get("col_name_idx", -1)

    if not classifications or header_idx < 0 or col_name < 0:
        print('ERRO: Uncorrect categories map format, missing classifications / header idx / col name idx',
              file=sys.stderr)
        return 1

    rows = _read(input_path)

    # Insert position for new column: Prioritize AI visible specified insert idx; otherwise degradation to "Pre-Remark column/end of line"
    if "insert_idx" in mapping and mapping["insert_idx"] is not None:
        insert_idx = int(mapping["insert_idx"])
    else:
        col_remark = mapping.get("col_remark_idx", -1)
        insert_idx = col_remark if col_remark != -1 else len(rows[header_idx])

    out_rows: list[tuple[list[object], bool]] = []
    header_font = Font(bold=True)

    # Line Before the Table Header
    for r in range(header_idx):
        old = list(rows[r])
        out_rows.append((old[:insert_idx] + ["", ""] + old[insert_idx:], False))

    # Header Line
    old = list(rows[header_idx])
    out_rows.append((old[:insert_idx] + ['Subject code', 'Name of subject'] + old[insert_idx:], True))

    # Data Row
    for r in range(header_idx + 1, len(rows)):
        old = list(rows[r])
        if not old:
            continue
        non_empty = [c for c in old if c is not None and str(c).strip() != ""]
        if not non_empty:
            out_rows.append((old[:insert_idx] + ["", ""] + old[insert_idx:], False))
            continue

        name = str(old[col_name]).strip() if col_name < len(old) else ""
        if name:
            key = normalize_name(name)
            cls = classifications.get(key, {})
            code, subject = cls.get("code", ""), cls.get("subject", "")
        else:
            code, subject = "", ""

        out_rows.append((old[:insert_idx] + [code, subject] + old[insert_idx:], False))

    # Writing
    wb = Workbook()
    ws = wb.active
    assert ws is not None, 'New Workbook necessarily contains at least one sheet'
    ws.title = 'Classified'

    for r_idx, (row_data, is_header) in enumerate(out_rows, start=1):
        ws.append(row_data)
        if is_header:
            for cell in ws[r_idx]:
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.freeze_panes = f"A{header_idx + 2}"

    # Generate column letters with column numbers + get column letter, avoiding reliance on col cells[0] (possibly MergedCell)
    for col_idx, col_cells in enumerate(ws.columns, start=1):
        max_len = max((len(str(c.value or "")) for c in col_cells), default=0)
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max(max_len + 2, 10), 28)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"XLSX={output_path}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description='Excel Classification I/O Tool (AI driver flexible version)')
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_read = sub.add_parser("read", help='dump table structure for AI understanding (without making any judgement)')
    _ = p_read.add_argument("input_file")

    p_names = sub.add_parser("names", help='Extract the object from the tablehead + list specified by AI Synchronising folder')
    _ = p_names.add_argument("input_file")
    _ = p_names.add_argument("--header-idx", type=int, required=True)
    _ = p_names.add_argument("--name-col", type=int, required=True)

    p_write = sub.add_parser("write", help='Map the results of the classification by AI')
    _ = p_write.add_argument("input_file")
    _ = p_write.add_argument("--output", required=True)
    _ = p_write.add_argument("--map", required=True)

    # Accept resolution results using structured namespace:  CliArgs is a subcategory of Namespace with default values for fields.
    # Therefore, args.* has a certain type (replaces the default Any attribute for angparse) and does not need a past.
    @dataclass
    class _CliArgs(argparse.Namespace):
        cmd: str = ""
        input_file: str = ""
        header_idx: int = 0
        name_col: int = 0
        output: str = ""
        map: str = ""

    ns = _CliArgs()
    _ = parser.parse_args(namespace=ns)
    args = ns

    if args.cmd == "read":
        return cmd_read(args.input_file)
    elif args.cmd == "names":
        return cmd_names(args.input_file, args.header_idx, args.name_col)
    elif args.cmd == "write":
        return cmd_write(args.input_file, args.output, args.map)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
