#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C/O Form-Specific Box Audit & Verification Readiness Engine (audit_co_box.py)
Chuyên viên Cao cấp Thẩm định Quy tắc Xuất xứ Hàng hóa (ROO Specialist)
Quét chi tiết từng ô (Box-by-Box), bắt lỗi Hóa đơn bên thứ ba, Cấp sau, Vận chuyển trực tiếp & Đánh giá Questionnaire Hải quan.
"""

import sys
import json
import argparse
import io
from datetime import datetime
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str or date_str == "N/A":
        return None
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%d.%m.%Y"]:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            pass
    return None

def audit_co_form(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    data structure:
    {
      "co_reference_no": str,
      "form_type": "Form D" | "Form EUR.1" | "Form CPTPP" | "Form RCEP" | "Form E",
      "fta": "ATIGA" | "EVFTA" | "CPTPP" | "RCEP" | "ACFTA",
      "issuing_country": str,
      "importing_country": str,
      "issue_date": "YYYY-MM-DD",
      "declaration_date": "YYYY-MM-DD",
      "declaration_no": str,
      "bl_date": "YYYY-MM-DD",
      "bl_type": "Through B/L" | "Direct B/L" | "Transshipment",
      "transit_country": str or None,
      "has_cnm_cert": bool, # Certificate of Non-Manipulation
      "exporter": {"name": str, "country": str, "address": str},
      "consignee": {"name": str, "country": str, "address": str},
      "producer": {"name": str, "country": str, "address": str},
      "invoice": {
         "no": str,
         "date": "YYYY-MM-DD",
         "issuer_name": str,
         "issuer_country": str,
         "currency": str,
         "fob_amount": float,
         "exw_amount": float
      },
      "co_boxes": {
         "box_1_exporter": str,
         "box_2_consignee": str,
         "box_3_producer": str, # For RCEP
         "box_7_description": str,
         "box_8_criterion": str,
         "box_9_fob_or_qty": str,
         "box_10_invoice": str,
         "box_13_ticks": {
             "third_party_invoicing": bool,
             "issued_retroactively": bool,
             "accumulation": bool,
             "partial_cumulation": bool,
             "de_minimis": bool
         }
      },
      "readiness_checklist": {
         "has_cost_statement": bool,
         "has_bom": bool,
         "has_raw_material_invoices": bool,
         "has_accounting_inventory_records": bool,
         "has_manufacturing_process_chart": bool
      }
    }
    """
    co_no = data.get("co_reference_no", "N/A")
    form_type = data.get("form_type", "Form D")
    fta = data.get("fta", "ATIGA").upper()
    issue_date = parse_date(data.get("issue_date", ""))
    decl_date = parse_date(data.get("declaration_date", ""))
    bl_date = parse_date(data.get("bl_date", ""))
    
    boxes = data.get("co_boxes", {})
    ticks = boxes.get("box_13_ticks", {})
    invoice = data.get("invoice", {})
    exporter = data.get("exporter", {})
    
    findings = []
    box_matrix = []
    
    # 1. Box 1 & Exporter Consistency
    b1_text = boxes.get("box_1_exporter", "")
    if exporter.get("name", "").lower() not in b1_text.lower():
        findings.append({
            "box": "Box 1",
            "level": "CẢNH BÁO",
            "title": "Tên Người xuất khẩu không khớp",
            "detail": f"Tên trên hồ sơ ({exporter.get('name')}) không khớp với nội dung Box 1 ({b1_text})"
        })
        box_matrix.append({"box": "Box 1", "field": "Exporter", "status": "LỆCH", "risk": "Vừa", "note": "Kiểm tra ủy quyền hoặc chi nhánh"})
    else:
        box_matrix.append({"box": "Box 1", "field": "Exporter", "status": "KHỚP", "risk": "An toàn", "note": "Khớp thông tin người xuất khẩu"})

    # 2. Box 3 (Producer) - Special RCEP check
    if form_type == "Form RCEP":
        b3_text = boxes.get("box_3_producer", "").strip()
        valid_rcep_b3 = any(kw in b3_text.upper() for kw in ["SAME AS EXPORTER", "NOT AVAILABLE", "CONFIDENTIAL", "SEE BOX 8"]) or len(b3_text) > 5
        if not valid_rcep_b3:
            findings.append({
                "box": "Box 3",
                "level": "NGHIÊM TRỌNG",
                "title": "Quy cách khai báo Box 3 Form RCEP không chuẩn",
                "detail": "Form RCEP bắt buộc ghi Nhà sản xuất hoặc ghi rõ một trong các cụm từ: 'SAME AS EXPORTER', 'NOT AVAILABLE', 'CONFIDENTIAL', 'SEE BOX 8'."
            })
            box_matrix.append({"box": "Box 3", "field": "Producer (RCEP)", "status": "LỖI QUY CÁCH", "risk": "Cao", "note": "Phải ghi đúng chuẩn RCEP"})
        else:
            box_matrix.append({"box": "Box 3", "field": "Producer (RCEP)", "status": "HỢP LỆ", "risk": "An toàn", "note": b3_text})

    # 3. Third Party Invoicing Check
    is_third_party = False
    inv_issuer = invoice.get("issuer_name", "").strip()
    inv_country = invoice.get("issuer_country", "").strip()
    exp_name = exporter.get("name", "").strip()
    exp_country = exporter.get("country", "").strip()

    if inv_issuer and exp_name and (inv_issuer.lower() != exp_name.lower() or (inv_country and exp_country and inv_country.lower() != exp_country.lower())):
        is_third_party = True

    b13_third_party = ticks.get("third_party_invoicing", False)
    if is_third_party:
        if not b13_third_party:
            findings.append({
                "box": "Box 13 / Box 7" if form_type != "Form EUR.1" else "Box 7",
                "level": "RẤT NGHIÊM TRỌNG",
                "title": "Bỏ sót đánh dấu Hóa đơn bên thứ ba (Third Country Invoicing)",
                "detail": f"Hóa đơn do {inv_issuer} ({inv_country}) phát hành khác Exporter {exp_name} ({exp_country}) nhưng C/O KHÔNG tick chọn Third Country Invoicing! Nguy cơ bị bác C/O 100% tại Cửa khẩu."
            })
            box_matrix.append({"box": "Box 13", "field": "Third Country Invoicing", "status": "THIẾU TICK", "risk": "Rất cao", "note": "Hóa đơn bên thứ 3 nhưng chưa tick"})
        else:
            # Check Box 7 mentions third party company name & country
            b7_desc = boxes.get("box_7_description", "")
            if inv_issuer.lower() not in b7_desc.lower():
                findings.append({
                    "box": "Box 7",
                    "level": "CẢNH BÁO",
                    "title": "Box 7 chưa thể hiện đầy đủ tên Công ty Bên thứ ba",
                    "detail": f"Đã tick Third Party Invoicing nhưng Box 7 chưa ghi rõ tên bên phát hành hóa đơn ({inv_issuer}) theo quy định FTA."
                })
                box_matrix.append({"box": "Box 7", "field": "Third Party Remarks", "status": "THIẾU TÊN", "risk": "Trung bình", "note": f"Cần thể hiện {inv_issuer}"})
            else:
                box_matrix.append({"box": "Box 13 / Box 7", "field": "Third Party Invoicing", "status": "HỢP LỆ", "risk": "An toàn", "note": "Đã tick và ghi rõ tên công ty bên thứ 3"})
    else:
        if b13_third_party:
            findings.append({
                "box": "Box 13",
                "level": "CẢNH BÁO",
                "title": "Tick nhầm ô Third Country Invoicing",
                "detail": "Người phát hành hóa đơn trùng với Exporter nhưng C/O lại tick Third Party Invoicing."
            })
            box_matrix.append({"box": "Box 13", "field": "Third Party Invoicing", "status": "TICK THỪA", "risk": "Thấp", "note": "Không có bên thứ 3 nhưng vẫn tick"})

    # 4. Issued Retroactively Check (> 3 days after export/BL date)
    if issue_date and bl_date:
        diff_days = (issue_date - bl_date).days
        b13_retro = ticks.get("issued_retroactively", False)
        if diff_days > 3:
            if not b13_retro:
                findings.append({
                    "box": "Box 13" if form_type != "Form EUR.1" else "Box 7",
                    "level": "RẤT NGHIÊM TRỌNG",
                    "title": "Thiếu tick C/O Cấp sau (Issued Retroactively)",
                    "detail": f"C/O được cấp sau ngày tàu chạy (B/L date {bl_date.strftime('%d/%m/%Y')}) {diff_days} ngày (> 3 ngày) nhưng không tick ô 'Issued Retroactively'!"
                })
                box_matrix.append({"box": "Box 13", "field": "Issued Retroactively", "status": "THIẾU TICK", "risk": "Rất cao", "note": f"Cấp sau {diff_days} ngày nhưng chưa tick"})
            else:
                box_matrix.append({"box": "Box 13", "field": "Issued Retroactively", "status": "HỢP LỆ", "risk": "An toàn", "note": f"Đã tick hợp lệ (Cấp sau {diff_days} ngày)"})
        else:
            if b13_retro:
                box_matrix.append({"box": "Box 13", "field": "Issued Retroactively", "status": "TICK TRƯỚC", "risk": "Thấp", "note": "Cấp trong hạn 3 ngày nhưng vẫn tick (chấp nhận được)"})
            else:
                box_matrix.append({"box": "Box 13", "field": "Issued Retroactively", "status": "HỢP LỆ", "risk": "An toàn", "note": "Cấp đúng hạn thông thường (<= 3 ngày)"})

    # 5. Box 9 (FOB Value) Mandate in Form D
    if form_type == "Form D":
        imp_c = data.get("importing_country", "").upper()
        b9_val = boxes.get("box_9_fob_or_qty", "")
        if imp_c not in ["CAMBODIA", "CAMPUCHIA", "MYANMAR"]:
            if not any(char.isdigit() for char in b9_val):
                findings.append({
                    "box": "Box 9",
                    "level": "NGHIÊM TRỌNG",
                    "title": "Form D thiếu giá trị FOB tại Box 9",
                    "detail": f"Xuất sang {imp_c} bắt buộc phải thể hiện trị giá FOB tại Box 9 của Form D (trừ ngoại lệ Campuchia, Myanmar)."
                })
                box_matrix.append({"box": "Box 9", "field": "FOB Value (Form D)", "status": "THIẾU FOB", "risk": "Cao", "note": "Bắt buộc ghi FOB đối với nước này"})
            else:
                box_matrix.append({"box": "Box 9", "field": "FOB Value (Form D)", "status": "HỢP LỆ", "risk": "An toàn", "note": f"Đã ghi nhận FOB: {b9_val}"})

    # 6. Form EUR.1 Specific Checks
    if form_type == "Form EUR.1":
        box_matrix.append({"box": "Box 11 / 12", "field": "Chứng thực Hải quan & Người XK", "status": "HỢP LỆ", "risk": "An toàn", "note": "Mẫu EUR.1 gồm 14 ô theo chuẩn EVFTA"})
        # Check Value limit requirement (EXW based)
        if invoice.get("exw_amount", 0) <= 0 and invoice.get("fob_amount", 0) > 0:
            findings.append({
                "box": "Box 10 / Invoice",
                "level": "CẢNH BÁO",
                "title": "Hồ sơ EVFTA thiếu chứng từ Giá xuất xưởng (EXW)",
                "detail": "Quy tắc giá trị EVFTA căn cứ trên Giá xuất xưởng EXW chứ không căn cứ trên FOB. Cần bảng chiết tính EXW lưu hồ sơ."
            })

    # 7. Direct Consignment & Transit Checks
    bl_type = data.get("bl_type", "Through B/L")
    transit = data.get("transit_country")
    has_cnm = data.get("has_cnm_cert", False)

    transit_status = "ĐẠT"
    if transit and transit != "None":
        if bl_type == "Through B/L":
            transit_note = f"Quá cảnh qua {transit} có Vận đơn suốt (Through B/L)"
        elif has_cnm:
            transit_note = f"Quá cảnh qua {transit} có Giấy xác nhận không can thiệp (CNM) của Hải quan trung chuyển"
        else:
            transit_status = "RỦI RO CAO"
            transit_note = f"Quá cảnh qua {transit} nhưng KHÔNG có Through B/L và KHÔNG có CNM"
            findings.append({
                "box": "Vận chuyển",
                "level": "RẤT NGHIÊM TRỌNG",
                "title": "Vi phạm Quy tắc Vận chuyển trực tiếp (Direct Consignment)",
                "detail": f"Hàng hóa quá cảnh qua {transit} nhưng thiếu cả Through B/L và Chứng thư CNM của Hải quan nước quá cảnh."
            })
    else:
        transit_note = "Vận chuyển thẳng từ nước xuất khẩu sang Việt Nam"

    # 8. Validity Period (12 months)
    validity_ok = True
    if issue_date and decl_date:
        validity_days = (decl_date - issue_date).days
        if validity_days > 365:
            validity_ok = False
            findings.append({
                "box": "Thời hạn hiệu lực",
                "level": "RẤT NGHIÊM TRỌNG",
                "title": "C/O Đã hết hạn hiệu lực (> 12 tháng)",
                "detail": f"C/O cấp ngày {issue_date.strftime('%d/%m/%Y')}, tờ khai đăng ký ngày {decl_date.strftime('%d/%m/%Y')} ({validity_days} ngày > 365 ngày)."
            })

    # 9. Verification Readiness Score (Checklist 5 items)
    checklist = data.get("readiness_checklist", {})
    chk_items = [
        ("has_cost_statement", "Bảng kê chi phí sản xuất (Cost Statement)", 25),
        ("has_bom", "Bảng kê định mức nguyên liệu (BOM)", 25),
        ("has_raw_material_invoices", "Hóa đơn VAT / Tờ khai NVL đầu vào", 20),
        ("has_accounting_inventory_records", "Chứng từ kế toán kho nguyên liệu (FIFO/LIFO)", 15),
        ("has_manufacturing_process_chart", "Sơ đồ quy trình sản xuất chi tiết", 15)
    ]
    
    score = 0
    missing_docs = []
    ready_docs = []
    for key, name, weight in chk_items:
        if checklist.get(key, False):
            score += weight
            ready_docs.append(f"{name} (+{weight}đ)")
        else:
            missing_docs.append(f"{name} ({weight}đ)")

    # Overall Audit Verdict
    has_critical = any(f["level"] == "RẤT NGHIÊM TRỌNG" for f in findings)
    has_warning = any(f["level"] in ["NGHIÊM TRỌNG", "CẢNH BÁO"] for f in findings)

    if has_critical:
        overall_status = "KHÔNG HỢP LỆ — NGUY CƠ BÁC C/O VÀ TRUY THU THUẾ RẤT CAO"
        verdict_badge = "REJECTED_RISK"
    elif has_warning:
        overall_status = "CẢNH BÁO — CÓ SAI SÓT CẦN GIẢI TRÌNH BỔ SUNG"
        verdict_badge = "WARNING"
    else:
        overall_status = "HỢP LỆ — ĐỦ ĐIỀU KIỆN HƯỞNG THUẾ SUẤT ƯU ĐÃI ĐẶC BIỆT FTA"
        verdict_badge = "QUALIFIED"

    return {
        "co_reference_no": co_no,
        "form_type": form_type,
        "fta": fta,
        "overall_status": overall_status,
        "verdict_badge": verdict_badge,
        "findings_count": len(findings),
        "findings": findings,
        "box_matrix": box_matrix,
        "direct_consignment": {
            "status": transit_status,
            "route_detail": transit_note,
            "bl_type": bl_type
        },
        "validity": {
            "passed": validity_ok,
            "issue_date": issue_date.strftime("%d/%m/%Y") if issue_date else "N/A",
            "declaration_date": decl_date.strftime("%d/%m/%Y") if decl_date else "N/A"
        },
        "verification_readiness": {
            "score": score,
            "max_score": 100,
            "status": "RẤT TỐT (SẴN SÀNG)" if score >= 85 else ("TRUNG BÌNH (CẦN BỔ SUNG)" if score >= 50 else "YẾU (RỦI RO CAO KHI KIỂM TRA SAU THÔNG QUAN)"),
            "ready_docs": ready_docs,
            "missing_docs": missing_docs,
            "statutory_deadlines": {
                "domestic_retention": "Tối thiểu 5 năm (Nghị định 31/2018/NĐ-CP)",
                "fta_retention": "Tối thiểu 3 năm",
                "questionnaire_reply": "Tối đa 90 ngày kể từ ngày nhận yêu cầu",
                "visit_consent": "Tối đa 30 ngày để chấp thuận kiểm tra thực địa",
                "total_process": "180 ngày (300 ngày đối với EVFTA)"
            }
        }
    }

def main():
    parser = argparse.ArgumentParser(description="C/O Box-by-Box Audit & Verification Readiness Engine")
    parser.add_argument("--file", "-f", type=str, required=True, help="Đường dẫn file JSON chứa dữ liệu hồ sơ C/O")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON thuần")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        payload = json.load(f)

    res = audit_co_form(payload)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("=" * 75)
        print(f"📋 BÁO CÁO THẨM ĐỊNH HỒ SƠ C/O: {res['co_reference_no']} ({res['form_type']} - {res['fta']})")
        print("=" * 75)
        print(f"KẾT LUẬN TỔNG QUAN: {res['overall_status']}")
        print(f"Tổng số vấn đề phát hiện: {res['findings_count']}")
        print("-" * 75)

        if res["findings"]:
            print("🚨 DANH SÁCH SAI LỆCH & RỦI RO PHÁP LÝ:")
            for idx, item in enumerate(res["findings"], 1):
                print(f"  {idx}. [{item['level']}] [{item['box']}] {item['title']}")
                print(f"     -> {item['detail']}")
            print("-" * 75)

        print("📦 MA TRẬN ĐỐI CHIẾU BOX-BY-BOX:")
        for b in res["box_matrix"]:
            print(f"  • {b['box']} ({b['field']}): [{b['status']}] - Rủi ro: {b['risk']} | Ghi chú: {b['note']}")

        print("-" * 75)
        print(f"🚢 VẬN CHUYỂN TRỰC TIẾP: [{res['direct_consignment']['status']}] {res['direct_consignment']['route_detail']}")
        print(f"⏳ THỜI HẠN HIỆU LỰC: {'HỢP LỆ (Trong hạn 12 tháng)' if res['validity']['passed'] else 'HẾT HẠN HIỆU LỰC'}")

        print("-" * 75)
        vr = res["verification_readiness"]
        print(f"🛡️ ĐIỂM SẴN SÀNG XÁC MINH HẢI QUAN (QUESTIONNAIRE): {vr['score']}/100 [{vr['status']}]")
        if vr["missing_docs"]:
            print("  ⚠️ Chứng từ còn thiếu:")
            for m in vr["missing_docs"]:
                print(f"    - {m}")
        print("=" * 75)

if __name__ == "__main__":
    main()
