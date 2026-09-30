#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ingest_legal_asset.py — Tự Động Hóa Nạp Tài Liệu Pháp Lý Vào CSDL Cục Bộ
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / Antigravity AI
Mô tả: Tiếp nhận văn bản mới tải từ Thư Viện Pháp Luật / Cổng TTĐT Chính phủ,
       chuẩn hóa tên tệp, bóc tách metadata, tự động cập nhật legal_assets_registry.json
       và README.md catalog. BẮT BUỘC hỗ trợ chế độ xem trước (Dry-run / Human Checkpoint).
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Đảm bảo UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def find_paths():
    """Tìm đường dẫn thư mục legal-assets và registry.json"""
    base_dirs = [
        Path("knowledge-base/legal-assets"),
        Path("../knowledge-base/legal-assets"),
        Path("../../knowledge-base/legal-assets"),
        Path(os.path.expanduser("c:/Minh Hoang/Antigravity học/my-workspace/knowledge-base/legal-assets"))
    ]
    for b in base_dirs:
        reg = b / "legal_assets_registry.json"
        if reg.exists():
            return b, reg
    return None, None

def generate_standard_filename(doc_type, doc_number, title):
    """Sinh tên file chuẩn hóa tiếng Việt không dấu, không khoảng trắng"""
    import re
    # Chuẩn hóa loại văn bản
    prefix = "Van_Ban"
    t_lower = doc_type.lower()
    if "luật" in t_lower:
        prefix = "Luat"
    elif "nghị định" in t_lower or "nghi dinh" in t_lower:
        prefix = "Nghi_Dinh"
    elif "thông tư" in t_lower or "thong tu" in t_lower:
        prefix = "Thong_Tu"
    elif "nghị quyết" in t_lower or "nghi quyet" in t_lower:
        prefix = "Nghi_Quyet"
    elif "quyết định" in t_lower or "quyet dinh" in t_lower:
        prefix = "Quyet_Dinh"
        
    # Thay thế các ký tự tiếng Việt thông dụng trước khi regex
    char_map = {
        'Đ': 'D', 'đ': 'd', 'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A', 'Ắ': 'A', 'Ằ': 'A',
        'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A', 'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E',
        'Ẹ': 'E', 'Ế': 'E', 'Ề': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E', 'Í': 'I',
        'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I', 'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O',
        'Õ': 'O', 'Ọ': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
        'Ớ': 'O', 'Ờ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O', 'Ú': 'U', 'Ù': 'U',
        'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ử': 'U', 'Ữ': 'U',
        'Ự': 'U', 'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y'
    }
    num_norm = doc_number
    for k, v in char_map.items():
        num_norm = num_norm.replace(k, v).replace(k.lower(), v.lower())
    
    # Làm sạch số hiệu
    clean_num = re.sub(r'[^a-zA-Z0-9]', '_', num_norm).strip('_')
    clean_num = re.sub(r'_+', '_', clean_num)
    return f"{prefix}_{clean_num}.pdf"

def ingest_document(file_path, metadata, dry_run=True):
    assets_dir, reg_path = find_paths()
    if not assets_dir or not reg_path:
        print("[LỖI] Không tìm thấy thư mục knowledge-base/legal-assets trong workspace.", file=sys.stderr)
        return False
        
    with open(reg_path, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    docs = db.get("documents", [])
    
    # Kiểm tra trùng lặp số hiệu
    doc_number = metadata.get("doc_number", "").strip()
    existing = [d for d in docs if d.get("doc_number", "").lower() == doc_number.lower()]
    if existing:
        print(f"[CẢNH BÁO] Văn bản có số hiệu '{doc_number}' đã tồn tại trong CSDL (ID: {existing[0].get('id')}).")
        if not metadata.get("force", False):
            print("Hủy tác vụ để tránh ghi đè dữ liệu. Dùng --force nếu muốn cập nhật lại.")
            return False

    # Tạo ID mới
    next_id_num = len(docs) + 1
    new_id = f"DOC-{next_id_num:02d}"
    
    # Chuẩn hóa tên file
    src_p = Path(file_path) if file_path else None
    ext = src_p.suffix if src_p else ".pdf"
    std_filename = metadata.get("file_name") or generate_standard_filename(
        metadata.get("type", "Thông tư"),
        doc_number,
        metadata.get("title", "")
    )
    if not std_filename.endswith(ext):
        std_filename = Path(std_filename).stem + ext
        
    dst_p = assets_dir / std_filename
    
    # Bóc tách thông tin
    new_entry = {
        "id": new_id,
        "doc_number": doc_number,
        "type": metadata.get("type", "Thông tư"),
        "issuing_authority": metadata.get("issuing_authority", "Cơ quan nhà nước"),
        "issue_date": metadata.get("issue_date", "2026-01-01"),
        "effective_date": metadata.get("effective_date", "2026-01-01"),
        "status": metadata.get("status", "Còn hiệu lực"),
        "title": metadata.get("title", f"Văn bản số {doc_number}"),
        "file_name": std_filename,
        "file_size_bytes": src_p.stat().st_size if src_p and src_p.exists() else 0,
        "original_path": str(src_p.resolve()) if src_p and src_p.exists() else metadata.get("source_url", "Thư Viện Pháp Luật"),
        "hierarchy_level": metadata.get("hierarchy_level", 3),
        "category": metadata.get("category", "Văn bản nghiệp vụ hải quan mới"),
        "summary": metadata.get("summary", "Được cập nhật tự động từ nguồn tra cứu chính thống."),
        "relations": metadata.get("relations", {}),
        "key_articles": metadata.get("key_articles", []),
        "keywords": metadata.get("keywords", [doc_number.lower()])
    }
    
    # In bản tóm tắt Human Checkpoint
    print("=" * 70)
    print("📋 [HUMAN CHECKPOINT] PHIẾU THẨM ĐỊNH NẠP TÀI LIỆU VÀO CSDL PHÁP LÝ")
    print("=" * 70)
    print(f"• Mã lưu trữ định danh:  {new_id}")
    print(f"• Số hiệu văn bản:       {new_entry['doc_number']}")
    print(f"• Loại & Thẩm quyền:     {new_entry['type']} — {new_entry['issuing_authority']}")
    print(f"• Tiêu đề văn bản:       {new_entry['title']}")
    print(f"• Ngày ban hành / HL:    {new_entry['issue_date']} / {new_entry['effective_date']}")
    print(f"• Tình trạng hiệu lực:   {new_entry['status']}")
    print(f"• Nguồn dữ liệu:         {new_entry['original_path']}")
    print(f"• File đích trong CSDL:  knowledge-base/legal-assets/{std_filename}")
    print(f"• Dung lượng:            {new_entry['file_size_bytes']:,} bytes")
    print("-" * 70)
    print(f"• Tóm tắt nội dung:      {new_entry['summary']}")
    print(f"• Điều khoản then chốt:  {', '.join(new_entry['key_articles'][:2]) if new_entry['key_articles'] else 'N/A'}")
    print("=" * 70)
    
    if dry_run:
        print("⚠️ CHẾ ĐỘ XEM TRƯỚC (DRY-RUN): Chưa có dữ liệu nào bị thay đổi.")
        print("👉 Để thực thi nạp chính thức sau khi được sự đồng ý của bạn, chạy lệnh với cờ: --confirm")
        return True
        
    # Thực thi nạp chính thức (Confirmed)
    if src_p and src_p.exists():
        shutil.copy2(src_p, dst_p)
        print(f"✅ Đã sao chép tệp an toàn vào: {dst_p}")
    else:
        print(f"ℹ️ Đã ghi nhận metadata URL từ nguồn trực tuyến.")
        
    docs.append(new_entry)
    db["total_documents"] = len(docs)
    db["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã cập nhật tệp registry máy đọc: {reg_path}")
    
    # Cập nhật README.md của legal-assets
    readme_path = assets_dir / "README.md"
    if readme_path.exists():
        try:
            update_readme_catalog(readme_path, new_entry)
            print(f"✅ Đã cập nhật bảng danh mục Catalog trong: {readme_path}")
        except Exception as e:
            print(f"⚠️ Lỗi khi cập nhật README.md: {e}")
            
    print(f"\n🎉 HOÀN TẤT NẠP TÀI LIỆU {new_entry['doc_number']} VÀO CSDL CỤC BỘ THÀNH CÔNG!")
    return True

def update_readme_catalog(readme_path, entry):
    """Bổ sung dòng tài liệu mới vào bảng danh mục trong README.md"""
    content = readme_path.read_text(encoding="utf-8")
    table_marker = "| Mã ID | Số hiệu văn bản |"
    if table_marker in content:
        lines = content.splitlines()
        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            # Tìm cuối bảng danh mục
            if line.startswith("| **DOC-") and not inserted:
                pass
            if line.startswith("---") and inserted is False:
                # Chèn trước vạch phân cách tiếp theo
                pass
        # Đơn giản hơn: chèn vào sau dòng DOC cuối cùng
        last_doc_idx = -1
        for idx, l in enumerate(lines):
            if l.startswith("| **DOC-"):
                last_doc_idx = idx
        if last_doc_idx != -1:
            size_mb = entry['file_size_bytes'] / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB" if size_mb >= 0.1 else f"{entry['file_size_bytes']/1024:.0f} KB"
            new_row = f"| **{entry['id']}** | **{entry['doc_number']}** | {entry['issuing_authority']} | {entry['issue_date']} | {entry['effective_date']} | {entry['status']} | [{entry['file_name']}](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/knowledge-base/legal-assets/{entry['file_name']}) | {size_str} |"
            lines.insert(last_doc_idx + 1, new_row)
            readme_path.write_text("\n".join(lines), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Tự động hóa nạp tài liệu pháp lý vào CSDL Cục Bộ")
    parser.add_argument("--file", type=str, default="", help="Đường dẫn tệp tài liệu cục bộ (PDF hoặc DOC)")
    parser.add_argument("--doc-number", type=str, required=True, help="Số hiệu văn bản (VD: '18/2026/TT-BTC')")
    parser.add_argument("--type", type=str, default="Thông tư", help="Loại văn bản (Luật, Nghị định, Thông tư...)")
    parser.add_argument("--authority", type=str, default="Bộ Tài chính", help="Cơ quan ban hành")
    parser.add_argument("--title", type=str, default="", help="Tên hoặc trích yếu văn bản")
    parser.add_argument("--issue-date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Ngày ban hành (YYYY-MM-DD)")
    parser.add_argument("--effective-date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Ngày có hiệu lực (YYYY-MM-DD)")
    parser.add_argument("--status", type=str, default="Còn hiệu lực", help="Tình trạng hiệu lực")
    parser.add_argument("--summary", type=str, default="", help="Tóm tắt nội dung cốt lõi")
    parser.add_argument("--source-url", type=str, default="https://thuvienphapluat.vn", help="URL nguồn trên Thư Viện Pháp Luật hoặc Cổng TTĐT Chính phủ")
    parser.add_argument("--confirm", action="store_true", help="Xác nhận nạp chính thức (Human Approval Confirmed)")
    parser.add_argument("--force", action="store_true", help="Ghi đè nếu số hiệu đã tồn tại")

    args = parser.parse_args()
    
    meta = {
        "doc_number": args.doc_number,
        "type": args.type,
        "issuing_authority": args.authority,
        "title": args.title or f"{args.type} số {args.doc_number}",
        "issue_date": args.issue_date,
        "effective_date": args.effective_date,
        "status": args.status,
        "summary": args.summary or "Tài liệu nghiệp vụ bổ sung phục vụ tra cứu hải quan.",
        "source_url": args.source_url,
        "force": args.force,
        "category": f"{args.type} hướng dẫn mới",
        "keywords": [args.doc_number.lower(), args.type.lower(), "tra cứu tự động"]
    }
    
    dry_run = not args.confirm
    ingest_document(args.file, meta, dry_run=dry_run)

if __name__ == "__main__":
    main()
