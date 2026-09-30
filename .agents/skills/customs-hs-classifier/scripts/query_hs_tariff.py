import sqlite3
import os
import sys
import argparse

sys.stdout.reconfigure(encoding='utf-8')

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(skill_dir, 'assets')
db_path = os.path.join(assets_dir, 'hs_tariff_index.sqlite')

def search_tariff(query, limit=10, only_8_digits=False):
    if not os.path.exists(db_path):
        print(f"Error: Database index not found at {db_path}. Please run build_index.py first.")
        return []

    conn = sqlite3.connect(db_path)
    # Register Python lower function for proper Unicode Vietnamese case folding
    conn.create_function("py_lower", 1, lambda s: s.lower() if s else "")
    cur = conn.cursor()
    
    clean_q = query.strip()
    
    # Check if query looks like HS code (e.g., "1201", "1201.90", "12019000", "8471")
    code_digits = clean_q.replace('.', '').replace(' ', '')
    is_code = code_digits.isdigit()
    
    filter_8 = "AND digits_len = 8" if only_8_digits else ""
    
    if is_code:
        # Search by HS code prefix
        sql = f"""
        SELECT hs_code_formatted, desc_vn, desc_en, full_desc_vn, unit, tax_standard, tax_mfn, vat,
               acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent_heading, digits_len
        FROM hs_tariff
        WHERE REPLACE(REPLACE(hs_code, '.', ''), ' ', '') LIKE ? {filter_8}
        ORDER BY (digits_len = 8) DESC, hs_code ASC
        LIMIT ?
        """
        cur.execute(sql, (f"{code_digits}%", limit))
    else:
        # Search by keyword in full description (Vietnamese or English) with py_lower
        words = clean_q.lower().split()
        conditions = []
        params = []
        for w in words:
            conditions.append("(py_lower(full_desc_vn) LIKE ? OR py_lower(full_desc_en) LIKE ? OR py_lower(desc_vn) LIKE ?)")
            params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
        
        sql = f"""
        SELECT hs_code_formatted, desc_vn, desc_en, full_desc_vn, unit, tax_standard, tax_mfn, vat,
               acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent_heading, digits_len
        FROM hs_tariff
        WHERE {' AND '.join(conditions)} {filter_8}
        ORDER BY (digits_len = 8) DESC, hs_code ASC
        LIMIT ?
        """
        params.append(limit)
        cur.execute(sql, params)
        
    rows = cur.fetchall()
    conn.close()
    return rows

def format_results(rows, query):
    if not rows:
        print(f"\n[!] Khong tim thay ket qua phu hop cho tu khoa / ma HS: '{query}'")
        return
        
    print(f"\n{'='*95}")
    print(f" KET QUA TRA CUU BIEU THUE XNK 2026 CHO: '{query}' ({len(rows)} ket qua)")
    print(f"{'='*95}\n")
    
    for idx, r in enumerate(rows, 1):
        hs_fmt, desc_vn, desc_en, full_vn, unit, tax_std, tax_mfn, vat, \
        acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent, d_len = r
        
        tier = "DÒNG THUẾ 8 CHỮ SỐ (KHAI BÁO HQ)" if d_len == 8 else ("PHÂN NHÓM 6 SỐ" if d_len == 6 else "NHÓM 4 SỐ (HEADING)")
        print(f"[{idx}] MÃ HS: {hs_fmt} [{tier}] | ĐVT: {unit or 'N/A'}")
        print(f"    - Mo ta day du: {full_vn}")
        if desc_en:
            print(f"    - Mo ta EN    : {desc_en}")
        print(f"    - NGHIA VU THUE:")
        print(f"      + Thue NK Thong thuong: {tax_std or 'N/A'}")
        print(f"      + Thue NK Uu dai (MFN): {tax_mfn or '0%'}")
        print(f"      + Thue GTGT (VAT)     : {vat or 'Theo Luat VAT'}")
        print(f"      + Uu dai FTA:")
        print(f"        * ACFTA (Form E)    : {acfta or 'N/A'}  | ATIGA (Form D) : {atiga or 'N/A'}")
        print(f"        * EVFTA (EUR.1)     : {evfta or 'N/A'}  | CPTPP          : {cptpp or 'N/A'}")
        print(f"        * VKFTA (Form VK)   : {vkfta or 'N/A'}  | AKFTA (Form AK): {akfta or 'N/A'}")
        print(f"        * UKVFTA            : {ukvfta or 'N/A'}  | RCEP           : {rcep or 'N/A'}")
        if ttdb or bvmt:
            print(f"      + Thue khac: TTDB = {ttdb or '0%'} | BVMT = {bvmt or '0%'}")
        print(f"{'-'*95}")

def main():
    parser = argparse.ArgumentParser(description="Tra cuu Ma HS va Thue suat tu Bieu Thue XNK 2026")
    parser.add_argument("-q", "--query", required=True, help="Ma HS hoac tu khoa hang hoa")
    parser.add_argument("-l", "--limit", type=int, default=5, help="So luong ket qua toi da")
    parser.add_argument("--only-8", action="store_true", help="Chi tim cac dong thue 8 chu so de khai bao hai quan")
    args = parser.parse_args()
    
    results = search_tariff(args.query, args.limit, args.only_8)
    format_results(results, args.query)

if __name__ == "__main__":
    main()
