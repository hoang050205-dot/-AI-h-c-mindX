#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_legal_clauses.py — Tra Cứu Toàn Văn Cấp Điều/Khoản Pháp Lý Hải Quan (FTS5)
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / AI4A Antigravity
Mô tả: Công cụ CLI tra cứu siêu tốc (<15ms) cấp Điều/Khoản trong CSDL SQLite FTS5,
       hỗ trợ trích xuất nguyên văn, đối chiếu phả hệ và kiểm tra chế tài xử phạt NĐ 128.
Zero external dependencies (chỉ dùng Python stdlib).
"""

import os
import sys
import json
import sqlite3
import argparse
from pathlib import Path

# UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
DB_PATH = WORKSPACE_ROOT / "knowledge-base" / "legal-assets" / "customs_legal_index.sqlite"

def get_connection():
    if not DB_PATH.exists():
        print(f"[LỖI] Không tìm thấy tệp CSDL: {DB_PATH}", file=sys.stderr)
        print("Vui lòng chạy script build_legal_index.py để khởi tạo CSDL trước.", file=sys.stderr)
        sys.exit(1)
    return sqlite3.connect(str(DB_PATH))

def search_clauses(query="", article="", doc="", sanctions_only=False, limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    
    results = []
    
    # 1. Tìm theo chế tài xử phạt Nghị định 128
    if sanctions_only:
        sql = """
        SELECT id, doc_number, doc_title, article_number, article_title, clause_number, content, tags, effective_status
        FROM legal_clauses
        WHERE doc_number LIKE '%128/2020%'
        ORDER BY id ASC;
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results

    # 2. Tìm theo FTS5 hoặc lọc kết hợp
    if query:
        # Chuẩn hóa query cho FTS5 (hỗ trợ tìm kiếm từ khóa ghép)
        fts_query = query.strip()
        # Loại bỏ các ký tự đặc biệt nguy hiểm cho syntax FTS5
        clean_query = "".join(c for c in fts_query if c.isalnum() or c.isspace() or c in ("-", "_", "/"))
        words = clean_query.split()
        if len(words) > 1:
            fts_expression = " OR ".join(f'"{w}"' for w in words)
        else:
            fts_expression = f'"{clean_query}"'
            
        sql = """
        SELECT c.id, c.doc_number, c.doc_title, c.article_number, c.article_title, c.clause_number, c.content, c.tags, c.effective_status
        FROM legal_clauses_fts f
        JOIN legal_clauses c ON f.rowid = c.id
        WHERE legal_clauses_fts MATCH ?
        """
        params = [fts_expression]
        
        if article:
            sql += " AND c.article_number LIKE ?"
            params.append(f"%{article}%")
        if doc:
            sql += " AND c.doc_number LIKE ?"
            params.append(f"%{doc}%")
            
        sql += f" LIMIT {limit};"
        
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        except sqlite3.OperationalError:
            # Fallback sang tìm kiếm LIKE thông thường nếu FTS5 gặp cú pháp đặc biệt
            like_sql = """
            SELECT id, doc_number, doc_title, article_number, article_title, clause_number, content, tags, effective_status
            FROM legal_clauses
            WHERE (content LIKE ? OR article_title LIKE ? OR tags LIKE ?)
            """
            like_params = [f"%{query}%", f"%{query}%", f"%{query}%"]
            if article:
                like_sql += " AND article_number LIKE ?"
                like_params.append(f"%{article}%")
            if doc:
                like_sql += " AND doc_number LIKE ?"
                like_params.append(f"%{doc}%")
            like_sql += f" LIMIT {limit};"
            cursor.execute(like_sql, like_params)
            results = cursor.fetchall()
    elif article or doc:
        sql = """
        SELECT id, doc_number, doc_title, article_number, article_title, clause_number, content, tags, effective_status
        FROM legal_clauses
        WHERE 1=1
        """
        params = []
        if article:
            sql += " AND article_number LIKE ?"
            params.append(f"%{article}%")
        if doc:
            sql += " AND doc_number LIKE ?"
            params.append(f"%{doc}%")
        sql += f" LIMIT {limit};"
        cursor.execute(sql, params)
        results = cursor.fetchall()
    else:
        cursor.execute(f"SELECT id, doc_number, doc_title, article_number, article_title, clause_number, content, tags, effective_status FROM legal_clauses LIMIT {limit};")
        results = cursor.fetchall()

    conn.close()
    return results

def get_genealogy_diff(key=""):
    conn = get_connection()
    cursor = conn.cursor()
    if key:
        cursor.execute("""
        SELECT article_key, article_title, subject, version_original, version_amended_1, version_latest_2026, key_differences, compliance_trap, action_recommendation
        FROM genealogy_diff
        WHERE article_key LIKE ? OR article_title LIKE ?;
        """, (f"%{key}%", f"%{key}%"))
    else:
        cursor.execute("""
        SELECT article_key, article_title, subject, version_original, version_amended_1, version_latest_2026, key_differences, compliance_trap, action_recommendation
        FROM genealogy_diff;
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def format_terminal_box(row):
    _, doc_num, _, art_num, art_title, clause_num, content, tags, status = row
    output = []
    output.append(f"┌─ 📜 [{doc_num}] {art_num} — {art_title} ({clause_num})")
    output.append(f"│  • Trạng thái hiệu lực: {status}")
    output.append(f"│  • Từ khóa: {tags}")
    output.append("├─ [NỘI DUNG QUY PHẠM ĐIỀU KHOẢN]:")
    
    # Chia dòng đẹp mắt
    words = content.split()
    line = "│  "
    for w in words:
        if len(line) + len(w) + 1 > 88:
            output.append(line)
            line = "│  " + w
        else:
            line += (" " if line != "│  " else "") + w
    if line != "│  ":
        output.append(line)
    output.append("└" + "─" * 88)
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Tra cứu CSDL Pháp lý & Thủ tục Hải quan Cấp Điều/Khoản (SQLite FTS5)")
    parser.add_argument("-q", "--query", type=str, default="", help="Từ khóa nghiệp vụ (VD: 'e-C/O', 'báo cáo quyết toán', 'khai bổ sung', 'giảm thuế 8%')")
    parser.add_argument("-a", "--article", type=str, default="", help="Số Điều cần tra cứu (VD: 'Điều 16', 'Điều 20', 'Điều 8', 'Điều 9')")
    parser.add_argument("-d", "--doc", type=str, default="", help="Số hiệu văn bản (VD: '38/2015', '39/2018', '121/2025', '128/2020', '174/2025')")
    parser.add_argument("--sanctions", action="store_true", help="Tra cứu toàn bộ chế tài xử phạt VPHC Hải quan theo Nghị định 128/2020")
    parser.add_argument("--diff", type=str, nargs="?", const="all", help="Xuất bảng đối chiếu phả hệ sửa đổi đa tầng (VD: --diff 16, --diff 20, --diff vat)")
    parser.add_argument("--json", action="store_true", help="Xuất định dạng JSON cho agent/subagent")
    parser.add_argument("--limit", type=int, default=5, help="Số lượng kết quả tối đa (mặc định: 5)")

    args = parser.parse_args()

    # Xử lý chế độ DIFF
    if args.diff:
        diff_key = "" if args.diff == "all" else args.diff
        diffs = get_genealogy_diff(diff_key)
        if not diffs:
            print(f"[THÔNG BÁO] Không tìm thấy dữ liệu đối chiếu phả hệ cho: '{args.diff}'")
            print("Các cặp điều khoản hỗ trợ đối chiếu: '16' (Hồ sơ HQ), '20' (Khai bổ sung), 'vat' (Thuế 8%), 'xu_phat' (NĐ 128).")
            return
        
        print("=" * 90)
        print("🔄 BẢNG ĐỐI CHIẾU PHẢ HỆ SỬA ĐỔI ĐA TẦNG (MULTI-TIER CLAUSE DIFF)")
        print("=" * 90)
        for d in diffs:
            key, title, subj, v_orig, v_amend, v_2026, diffs_text, trap, action = d
            print(f"\n📌 {title.upper()}")
            print(f"• Chủ đề nghiệp vụ: {subj}")
            print("┌" + "─" * 88)
            print(f"│ 1. QUY ĐỊNH GỐC (TT 38/2015):\n│    {v_orig}")
            print(f"│ 2. SỬA ĐỔI BỔ SUNG (TT 39/2018):\n│    {v_amend}")
            print(f"│ 3. HIỆN HÀNH NĂM 2026 (TT 121/2025 / NĐ MỚI NHẤT):\n│    {v_2026}")
            print("├" + "─" * 88)
            print(f"│ ⚡ ĐIỂM KHÁC BIỆT MẤU CHỐT: {diffs_text}")
            print(f"│ ⚠️  BẪY RỦI RO DOANH NGHIỆP: {trap}")
            print(f"│ 💡 KHUYẾN NGHỊ HÀNH ĐỘNG:   {action}")
            print("└" + "─" * 88)
        return

    # Xử lý chế độ Tra cứu Điều/Khoản
    results = search_clauses(
        query=args.query,
        article=args.article,
        doc=args.doc,
        sanctions_only=args.sanctions,
        limit=args.limit
    )

    if not results:
        print(f"[THÔNG BÁO] Không tìm thấy Điều/Khoản phù hợp với tiêu chí tra cứu.")
        print("Gợi ý từ khóa: 'e-C/O', 'báo cáo quyết toán', 'khai sai tên hàng', 'phạt thiếu thuế', 'giảm thuế 8%', 'kiểm tra sau thông quan'.")
        return

    if args.json:
        data = []
        for r in results:
            data.append({
                "id": r[0], "doc_number": r[1], "doc_title": r[2],
                "article_number": r[3], "article_title": r[4],
                "clause_number": r[5], "content": r[6],
                "tags": r[7], "effective_status": r[8]
            })
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    header = f"=== TÌM THẤY {len(results)} ĐIỀU/KHOẢN TRỌNG TÂM (SQLITE FTS5 ENGINE) ==="
    print(header)
    for r in results:
        print(format_terminal_box(r))
        print()

if __name__ == "__main__":
    main()
