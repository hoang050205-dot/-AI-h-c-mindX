#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_legal_assets.py — Tra cứu CSDL Pháp lý & Thủ tục Hải quan Cục bộ
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / Antigravity AI
Mô tả: Công cụ CLI tìm kiếm văn bản pháp luật, phân loại phả hệ và sinh bản tóm tắt Giai đoạn 1 (Search & Brief).
Không phụ thuộc thư viện ngoài (Zero external dependencies).
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Đảm bảo UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def find_registry_path():
    """Tìm đường dẫn tệp legal_assets_registry.json trong workspace"""
    candidates = [
        Path("knowledge-base/legal-assets/legal_assets_registry.json"),
        Path("../knowledge-base/legal-assets/legal_assets_registry.json"),
        Path("../../knowledge-base/legal-assets/legal_assets_registry.json"),
        Path(os.path.expanduser("c:/Minh Hoang/Antigravity học/my-workspace/knowledge-base/legal-assets/legal_assets_registry.json"))
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def load_registry(registry_path):
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search_documents(db, query, doc_id=None):
    docs = db.get("documents", [])
    results = []
    
    q = (query or "").lower().strip()
    target_doc = (doc_id or "").lower().strip()
    
    for doc in docs:
        score = 0
        doc_num = doc.get("doc_number", "").lower()
        title = doc.get("title", "").lower()
        summary = doc.get("summary", "").lower()
        keywords = [k.lower() for k in doc.get("keywords", [])]
        articles = [a.lower() for a in doc.get("key_articles", [])]
        
        # Lọc chính xác số hiệu nếu có
        if target_doc:
            if target_doc in doc_num or target_doc in doc.get("id", "").lower() or target_doc in doc.get("file_name", "").lower():
                results.append((doc, 100))
            continue
            
        if not q:
            results.append((doc, 1))
            continue
            
        if q in doc_num:
            score += 40
        if q in title:
            score += 30
        for kw in keywords:
            if q in kw or kw in q:
                score += 25
        if q in summary:
            score += 15
        for art in articles:
            if q in art:
                score += 10
                
        # Khớp từ khóa từng phần
        words = q.split()
        if len(words) > 1:
            matched_words = sum(1 for w in words if w in doc_num or w in title or w in summary or any(w in kw for kw in keywords))
            score += matched_words * 5

        if score > 0:
            results.append((doc, score))
            
    # Sắp xếp theo độ liên quan giảm dần
    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]

def format_stage1_brief(doc):
    """Xuất định dạng Giai đoạn 1 (Search & Brief) chuẩn 4 gạch đầu dòng"""
    doc_num = doc.get("doc_number", "N/A")
    title = doc.get("title", "N/A")
    authority = doc.get("issuing_authority", "N/A")
    issue_date = doc.get("issue_date", "N/A")
    effective_date = doc.get("effective_date", "N/A")
    summary = doc.get("summary", "N/A")
    key_articles = doc.get("key_articles", [])
    
    # Rút gọn tóm tắt 2-3 câu
    summary_sentences = [s.strip() for s in summary.split(".") if s.strip()]
    concise_summary = ". ".join(summary_sentences[:2])
    if concise_summary and not concise_summary.endswith("."):
        concise_summary += "."
        
    articles_str = "; ".join(key_articles[:3]) if key_articles else "Các điều khoản thi hành chung."

    output = []
    output.append(f"### 📌 KẾT QUẢ GIAI ĐOẠN 1 (SEARCH & BRIEF): {doc_num}")
    output.append(f"- **Số hiệu & Tên văn bản:** {title}")
    output.append(f"- **Cơ quan ban hành & Ngày ban hành:** {authority} (Ban hành: {issue_date} | Hiệu lực: {effective_date})")
    output.append(f"- **Nội dung bao quát ngắn gọn:** {concise_summary}")
    output.append(f"- **Từ khóa/Điều khoản then chốt cần tra cứu:** {articles_str}")
    output.append(f"- **Vị trí file nội bộ trong Workspace:** `knowledge-base/legal-assets/{doc.get('file_name')}`")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Tra cứu CSDL Pháp lý & Thủ tục Hải quan Cục bộ")
    parser.add_argument("-q", "--query", type=str, default="", help="Từ khóa nghiệp vụ (VD: 'giảm thuế VAT', 'hồ sơ điện tử', 'phân luồng')")
    parser.add_argument("-d", "--doc", type=str, default="", help="Số hiệu văn bản (VD: '38/2015', '39/2018', '121/2025', '167/2025', '174/2025', '54/2014')")
    parser.add_argument("--brief", action="store_true", help="Xuất theo mẫu chuẩn Giai đoạn 1 (Search & Brief)")
    parser.add_argument("--list", action="store_true", help="Liệt kê toàn bộ danh mục văn bản trong CSDL")
    
    args = parser.parse_args()
    
    reg_path = find_registry_path()
    if not reg_path:
        print("[LỖI] Không tìm thấy file legal_assets_registry.json trong workspace.", file=sys.stderr)
        sys.exit(1)
        
    db = load_registry(reg_path)
    
    if args.list:
        print(f"=== CSDL PHÁP LÝ HẢI QUAN: {db.get('total_documents', 0)} VĂN BẢN ĐÃ LẬP CHỈ MỤC ===")
        for d in db.get("documents", []):
            print(f"[{d.get('id')}] {d.get('doc_number')} - {d.get('title')} ({d.get('status')})")
        return

    results = search_documents(db, args.query, args.doc)
    if not results:
        print(f"[THÔNG BÁO] Không tìm thấy văn bản phù hợp với từ khóa: '{args.query or args.doc}'")
        print("Gợi ý tra cứu: 'thủ tục hải quan', 'thuế vat', 'giảm thuế 8%', 'hồ sơ nộp điện tử', 'báo cáo quyết toán', '121/2025', '38/2015'.")
        return

    # Lấy tối đa 1 đến 3 văn bản trọng tâm nhất theo đúng nguyên tắc Giai đoạn 1
    top_results = results[:3]
    
    if args.brief:
        for doc in top_results:
            print(format_stage1_brief(doc))
            print("-" * 60)
    else:
        print(f"Tìm thấy {len(results)} văn bản phù hợp. Trích xuất {len(top_results)} văn bản trọng tâm nhất:")
        for idx, doc in enumerate(top_results, 1):
            print(f"\n[{idx}] {doc.get('doc_number')} — {doc.get('title')}")
            print(f"    • Cơ quan & Ngày: {doc.get('issuing_authority')} ({doc.get('issue_date')})")
            print(f"    • Hiệu lực: {doc.get('effective_date')} | Tình trạng: {doc.get('status')}")
            print(f"    • Tệp: knowledge-base/legal-assets/{doc.get('file_name')}")

if __name__ == "__main__":
    main()
