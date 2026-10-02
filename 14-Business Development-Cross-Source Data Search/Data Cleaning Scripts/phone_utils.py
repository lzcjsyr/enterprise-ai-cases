# -*- coding: utf-8 -*-
'Public module for telephone de-sensitization (for step3  / step4  (Shared)\nRules:\nCellular number: retain top 3 + back 4 and replace middle 4 with **** (135****2816)\n2. Remove the markings of the [acting] [empty] [inactive] sign, and (Xing Ming) information\n3. Uncoded and uncoded (0756-2290201)\n4. Multiple numbers in the same cell: replace with a line after weight (\n) Separating'
import re
import math

SPLIT_RE = re.compile(r"[,，;；、/\s]+")
MOBILE_RE = re.compile(r"1[3-9]\d{9}")

# National marker: 3-bit megacities only, with 4-bit districts remaining in the remaining cities No. No.
BIG_CITY = {"010", "020", "021", "022", "023", "024", "025", "027", "028", "029"}



def to_text(v):
    'Cell Value - > Text (number compatible cells, e.g. 13560782816.0)'
    if v is None:
        return None
    if isinstance(v, float):
        if math.isnan(v):
            return None
        if v.is_integer():
            return str(int(v))
    if isinstance(v, int) and not isinstance(v, bool):
        return str(v)
    return str(v)


def clean_phone_cell(v):
    'Remove (Xing Ming), [activated number] additional information, then unseparate the number clip'
    s = to_text(v)
    if s is None:
        return []
    s = re.sub(r"[（(][^）)]*[）)]", "", s)   # Go on, go on.
    s = re.sub(r"【[^】]*】", "", s)           # Go, [activator] [empty]
    return [p for p in SPLIT_RE.split(s) if p.strip()]


def mask_mobile(digits):
    'Mobile number dialed: 135****2816'
    return digits[:3] + "****" + digits[-4:]


def fmt_fixed(digits):
    'Speculator: Unified format for "Zone Number - Main Number"\n- 3-bit (ten big cities, etc. 010/020) or 4-bit (0756/0755 etc.) split according to the national standard\n- No beginning: after filling 0 (Excel lost zero in the numbers); 7/8 main sign from Pearlhead. 0756.'
    s = digits if digits.startswith("0") else "0" + digits
    if 9 <= len(s) <= 12 and s[1] != "0":      # 9-12 bits: Area + Main
        n = 3 if s[:3] in BIG_CITY else 4      # Three in the 10 big cities, the other four.
        if 6 <= len(s) - n <= 9:               # 6-9 is considered valid.
            return f"{s[:n]}-{s[n:]}"
    # Local number of the Pearl Sea (7/8 primary and not zone number): supplement 0756
    if len(digits) in (7, 8) and not digits.startswith("0"):
        return f"0756-{digits}"
    return digits  # Keep non-standard numbers as they are


def mobile_text(v):
    'Cell- > Call text; no valid number returns None'
    nums = []
    for p in clean_phone_cell(v):
        m = MOBILE_RE.search(p)
        if m and m.group(0) not in nums:
            nums.append(m.group(0))
    return "\n".join(mask_mobile(x) for x in nums) if nums else None


def fixed_text(v):
    'Strong-word cell -> Area-Main Number line break text; No one returned'
    nums = []
    for p in clean_phone_cell(v):
        d = re.sub(r"[^\d]", "", p)
        if len(d) >= 7 and d not in nums:
            nums.append(d)
    return "\n".join(fmt_fixed(x) for x in nums) if nums else None
