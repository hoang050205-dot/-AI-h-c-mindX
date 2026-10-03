#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diff_legal_clauses.py — So Sánh Phả Hệ Sửa Đổi Đa Tầng (Multi-Tier Clause Diff)
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / AI4A Antigravity
Mô tả: Bóc tách sự thay đổi của quy phạm pháp luật qua các thời kỳ (TT 38 -> TT 39 -> TT 121/2025),
       chỉ rõ điểm khác biệt mấu chốt, bẫy rủi ro và khuyến nghị tuân thủ doanh nghiệp.
Zero external dependencies.
"""

import sys
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
        sys.exit(1)
    return sqlite3.connect(str(DB_PATH))

def list_diff_keys():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT article_key, article_title, subject FROM genealogy_diff ORDER BY id ASC;")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_diff_detail(key=""):
    conn = get_connection()
    cursor = conn.cursor()
    if key and key != "all":
        cursor.execute("""
        SELECT article_key, article_title, subject, version_original, version_amended_1, version_latest_2026, key_differences, compliance_trap, action_recommendation
        FROM genealogy_diff
        WHERE article_key LIKE ? OR article_title LIKE ?;
        """, (f"%{key}%", f"%{key}%"))
    else:
        cursor.execute("""
        SELECT article_key, article_title, subject, version_original, version_amended_1, version_latest_2026, key_differences, compliance_trap, action_recommendation
        FROM genealogy_diff
        ORDER BY id ASC;
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def format_markdown_table(row):
    key, title, subj, v_orig, v_amend, v_2026, diffs_text, trap, action = row
    md = []
    md.append(f"### 🔄 ĐỐI CHIẾU PHẢ HỆ ĐA TẦNG: {title.upper()}")
    md.append(f"**Chủ đề:** {subj}\n")
    md.append("| Giai đoạn văn bản | Số hiệu quy chuẩn | Nội dung quy định then chốt |")
    md.append("|:---|:---|:---|")
    md.append(f"| **1. Quy định gốc** | Thông tư 38/2015/TT-BTC | {v_orig} |")
    md.append(f"| **2. Sửa đổi giai đoạn 1** | Thông tư 39/2018/TT-BTC | {v_amend} |")
    md.append(f"| **3. Cập nhật mới nhất 2026** | Thông tư 121/2025/TT-BTC | **{v_2026}** |")
    md.append("")
    md.append(f"> ⚡ **Điểm khác biệt mấu chốt:** {diffs_text}")
    md.append(f"> ")
    md.append(f"> ⚠️ **Bẫy rủi ro doanh nghiệp:** {trap}")
    md.append(f"> ")
    md.append(f"> 💡 **Khuyến nghị hành động:** {action}")
    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="So Sánh Phả Hệ Sửa Đổi Đa Tầng (Multi-Tier Clause Diff)")
    parser.add_argument("-k", "--key", type=str, default="", help="Mã đối chiếu hoặc số điều (VD: '16', '20', 'vat', 'xu_phat', 'all')")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh mục các cặp điều khoản hỗ trợ đối chiếu")
    parser.add_argument("--markdown", action="store_true", help="Xuất định dạng bảng Markdown nhúng vào báo cáo")

    args = parser.parse_args()

    if args.list:
        keys = list_diff_keys()
        print("=== DANH MỤC CÁC CẶP ĐIỀU KHOẢN HỖ TRỢ ĐỐI CHIẾU PHẢ HỆ SỬA ĐỔI ===")
        for idx, (k, t, s) in enumerate(keys, 1):
            print(f"[{idx}] Khóa tra cứu: `{k}`")
            print(f"    • Tiêu đề: {t}")
            print(f"    • Chủ đề:  {s}")
        return

    target = args.key or "all"
    rows = get_diff_detail(target)
    if not rows:
        print(f"[THÔNG BÁO] Không tìm thấy dữ liệu đối chiếu cho: '{target}'")
        print("Dùng --list để xem danh sách các khóa đối chiếu có sẵn.")
        return

    if args.markdown:
        for r in rows:
            print(format_markdown_table(r))
            print("\n---\n")
    else:
        for r in rows:
            key, title, subj, v_orig, v_amend, v_2026, diffs_text, trap, action = r
            print("=" * 88)
            print(f"🔄 ĐỐI CHIẾU PHẢ HỆ: {title.upper()}")
            print(f"• Chủ đề nghiệp vụ: {subj}")
            print("-" * 88)
            print(f"[TẦNG 1 - GỐC (TT 38/2015)]:\n  {v_orig}\n")
            print(f"[TẦNG 2 - SỬA ĐỔI (TT 39/2018)]:\n  {v_amend}\n")
            print(f"[TẦNG 3 - HIỆN HÀNH 2026 (TT 121/2025)]:\n  {v_2026}\n")
            print("-" * 88)
            print(f"⚡ ĐIỂM KHÁC BIỆT MẤU CHỐT: {diffs_text}")
            print(f"⚠️  BẪY RỦI RO DOANH NGHIỆP: {trap}")
            print(f"💡 KHUYẾN NGHỊ HÀNH ĐỘNG:   {action}")
            print("=" * 88 + "\n")

if __name__ == "__main__":
    main()
