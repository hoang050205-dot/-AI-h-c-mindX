import openpyxl
import sqlite3
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(skill_dir, 'assets')
xlsx_path = os.path.join(assets_dir, 'Bieu_thue_XNK_2026.xlsx')
db_path = os.path.join(assets_dir, 'hs_tariff_index.sqlite')

print(f"Indexing {xlsx_path} into {db_path} with parent-child hierarchy...")
t0 = time.time()

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS hs_tariff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hs_code TEXT,
    hs_code_formatted TEXT,
    digits_len INTEGER,
    parent_heading TEXT,
    desc_vn TEXT,
    desc_en TEXT,
    full_desc_vn TEXT,
    full_desc_en TEXT,
    unit TEXT,
    tax_standard TEXT,
    tax_mfn TEXT,
    vat TEXT,
    acfta TEXT,
    atiga TEXT,
    akfta TEXT,
    vkfta TEXT,
    cptpp TEXT,
    evfta TEXT,
    ukvfta TEXT,
    rcep TEXT,
    ttdb TEXT,
    bvmt TEXT
)
""")

cur.execute("CREATE INDEX idx_hs_code ON hs_tariff(hs_code)")
cur.execute("CREATE INDEX idx_digits_len ON hs_tariff(digits_len)")
cur.execute("CREATE INDEX idx_parent ON hs_tariff(parent_heading)")

wb = openpyxl.load_workbook(xlsx_path, read_only=True)
ws = wb['BT2026']

def clean(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s == "None" else s

current_heading_code = ""
current_heading_vn = ""
current_heading_en = ""
current_subheading_vn = ""
current_subheading_en = ""

batch = []
for idx, row in enumerate(ws.iter_rows(values_only=True)):
    if idx < 3: # Skip header rows
        continue
    
    hs = clean(row[5])
    desc_vn = clean(row[6])
    desc_en = clean(row[7])
    
    if not hs and not desc_vn:
        continue

    digits = hs.replace('.', '').replace(' ', '')
    d_len = len(digits) if digits.isdigit() else 0
    
    # Format HS code
    if d_len == 8:
        formatted_hs = f"{digits[:4]}.{digits[4:6]}.{digits[6:8]}"
    elif d_len == 6:
        formatted_hs = f"{digits[:4]}.{digits[4:6]}"
    elif d_len == 4:
        formatted_hs = digits
    else:
        formatted_hs = hs

    # Track hierarchy
    if d_len == 4:
        current_heading_code = digits
        current_heading_vn = desc_vn
        current_heading_en = desc_en
        current_subheading_vn = ""
        current_subheading_en = ""
        full_vn = desc_vn
        full_en = desc_en
    elif d_len == 6:
        current_subheading_vn = desc_vn
        current_subheading_en = desc_en
        full_vn = f"{current_heading_vn} - {desc_vn}".strip(' -')
        full_en = f"{current_heading_en} - {desc_en}".strip(' -')
    elif d_len == 8:
        # 8-digit tariff line inherits parent heading and subheading if available
        parts_vn = [p for p in [current_heading_vn, current_subheading_vn, desc_vn] if p]
        parts_en = [p for p in [current_heading_en, current_subheading_en, desc_en] if p]
        full_vn = " - ".join(parts_vn)
        full_en = " - ".join(parts_en)
    else:
        full_vn = desc_vn
        full_en = desc_en
    
    unit = clean(row[8]) if len(row) > 8 else ""
    tax_standard = clean(row[10]) if len(row) > 10 else ""
    tax_mfn = clean(row[13]) if len(row) > 13 else ""
    vat = clean(row[16]) if len(row) > 16 else ""
    acfta = clean(row[19]) if len(row) > 19 else ""
    atiga = clean(row[22]) if len(row) > 22 else ""
    akfta = clean(row[31]) if len(row) > 31 else ""
    vkfta = clean(row[40]) if len(row) > 40 else ""
    cptpp = clean(row[49]) if len(row) > 49 else ""
    evfta = clean(row[58]) if len(row) > 58 else ""
    ukvfta = clean(row[61]) if len(row) > 61 else ""
    rcep = clean(row[73]) if len(row) > 73 else ""
    ttdb = clean(row[84]) if len(row) > 84 else ""
    bvmt = clean(row[99]) if len(row) > 99 else ""

    batch.append((
        hs, formatted_hs, d_len, current_heading_code,
        desc_vn, desc_en, full_vn, full_en, unit,
        tax_standard, tax_mfn, vat,
        acfta, atiga, akfta, vkfta,
        cptpp, evfta, ukvfta, rcep,
        ttdb, bvmt
    ))
    
    if len(batch) >= 1000:
        cur.executemany("""
        INSERT INTO hs_tariff (
            hs_code, hs_code_formatted, digits_len, parent_heading,
            desc_vn, desc_en, full_desc_vn, full_desc_en, unit,
            tax_standard, tax_mfn, vat,
            acfta, atiga, akfta, vkfta,
            cptpp, evfta, ukvfta, rcep,
            ttdb, bvmt
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)
        batch = []

if batch:
    cur.executemany("""
    INSERT INTO hs_tariff (
        hs_code, hs_code_formatted, digits_len, parent_heading,
        desc_vn, desc_en, full_desc_vn, full_desc_en, unit,
        tax_standard, tax_mfn, vat,
        acfta, atiga, akfta, vkfta,
        cptpp, evfta, ukvfta, rcep,
        ttdb, bvmt
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, batch)

conn.commit()

# Check total count
cur.execute("SELECT COUNT(*) FROM hs_tariff")
cnt = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM hs_tariff WHERE digits_len = 8")
cnt8 = cur.fetchone()[0]
conn.close()

print(f"Successfully indexed {cnt:,} rows ({cnt8:,} 8-digit tariff lines) in {time.time()-t0:.2f}s! SQLite DB: {db_path} ({os.path.getsize(db_path):,} bytes)")
