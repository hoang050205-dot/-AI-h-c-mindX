#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROO Origin Calculation Engine (calculate_origin.py)
Chuyên viên Cao cấp Thẩm định Quy tắc Xuất xứ Hàng hóa (ROO Specialist)
Hỗ trợ tính toán RVC, VL, De Minimis, CTC Ngoại trừ, Rà soát Gia công đơn giản.
"""

import sys
import json
import argparse
import io
from typing import Dict, Any, List, Optional

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def calculate_rvc_build_down(fob: float, vnm: float) -> Dict[str, Any]:
    if fob <= 0:
        raise ValueError("Trị giá FOB phải lớn hơn 0")
    rvc = ((fob - vnm) / fob) * 100.0
    return {
        "formula": "Build-down: ((FOB - VNM) / FOB) * 100%",
        "fob": fob,
        "vnm": vnm,
        "rvc_percentage": round(rvc, 2)
    }

def calculate_rvc_build_up(fob: float, vom: float, labor: float, overhead: float, other: float, profit: float) -> Dict[str, Any]:
    if fob <= 0:
        raise ValueError("Trị giá FOB phải lớn hơn 0")
    total_added = vom + labor + overhead + other + profit
    rvc = (total_added / fob) * 100.0
    return {
        "formula": "Build-up: ((VOM + Direct Labor + Overhead + Other + Profit) / FOB) * 100%",
        "fob": fob,
        "vom": vom,
        "labor": labor,
        "overhead": overhead,
        "other": other,
        "profit": profit,
        "total_added": total_added,
        "rvc_percentage": round(rvc, 2)
    }

def calculate_rvc_net_cost(net_cost: float, vnm: float) -> Dict[str, Any]:
    if net_cost <= 0:
        raise ValueError("Chi phí tịnh (Net Cost) phải lớn hơn 0")
    rvc = ((net_cost - vnm) / net_cost) * 100.0
    return {
        "formula": "Net Cost: ((Net Cost - VNM) / Net Cost) * 100%",
        "net_cost": net_cost,
        "vnm": vnm,
        "rvc_percentage": round(rvc, 2)
    }

def calculate_rvc_focus_value(goods_value: float, non_orig_focus: float) -> Dict[str, Any]:
    if goods_value <= 0:
        raise ValueError("Trị giá hàng hóa phải lớn hơn 0")
    rvc = ((goods_value - non_orig_focus) / goods_value) * 100.0
    return {
        "formula": "Focus Value: ((Trị giá hàng - VNM đặc trưng) / Trị giá hàng) * 100%",
        "goods_value": goods_value,
        "non_orig_focus": non_orig_focus,
        "rvc_percentage": round(rvc, 2)
    }

def calculate_evfta_value_limit(exw: float, vnm: float, threshold: float = 70.0) -> Dict[str, Any]:
    if exw <= 0:
        raise ValueError("Trị giá xuất xưởng (EXW) phải lớn hơn 0")
    vnm_ratio = (vnm / exw) * 100.0
    passed = vnm_ratio <= threshold
    return {
        "formula": "Value Limit EVFTA: (VNM / EXW) * 100% <= Threshold%",
        "exw": exw,
        "vnm": vnm,
        "threshold": threshold,
        "vnm_ratio": round(vnm_ratio, 2),
        "passed": passed,
        "margin": round(threshold - vnm_ratio, 2)
    }

def check_de_minimis(base_val: float, non_qualifying_vnm: float, threshold: float = 10.0, basis: str = "FOB") -> Dict[str, Any]:
    if base_val <= 0:
        return {"applicable": False, "reason": "Base value is zero or negative"}
    ratio = (non_qualifying_vnm / base_val) * 100.0
    passed = ratio <= threshold
    return {
        "basis": basis,
        "base_val": base_val,
        "non_qualifying_vnm": non_qualifying_vnm,
        "tolerance_ratio": round(ratio, 2),
        "threshold": threshold,
        "passed": passed,
        "status": "ĐẠT TIÊU CHÍ QUA DE MINIMIS" if passed else "VƯỢT NGƯỠNG DE MINIMIS (KHÔNG ĐẠT)"
    }

def evaluate_ctc(finished_hs: str, materials: List[Dict[str, Any]], rule_type: str = "CTH", exceptions: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    materials: [{"name": str, "hs": str, "originating": bool, "val": float}]
    rule_type: CC (2 digits), CTH (4 digits), CTSH (6 digits)
    exceptions: list of HS chapters/headings that are forbidden for non-originating materials
    """
    f_hs = finished_hs.replace(".", "").strip()
    cut_len = 2 if rule_type.upper() == "CC" else (4 if rule_type.upper() == "CTH" else 6)
    finished_prefix = f_hs[:cut_len]

    failed_materials = []
    exception_hits = []

    for mat in materials:
        if mat.get("originating", False):
            continue  # Nguyên liệu đã có xuất xứ không cần xét CTC
        
        m_hs = mat.get("hs", "").replace(".", "").strip()
        m_prefix = m_hs[:cut_len]

        # Kiểm tra ngoại trừ
        if exceptions:
            for exc in exceptions:
                clean_exc = exc.replace(".", "").strip()
                if m_hs.startswith(clean_exc):
                    exception_hits.append({
                        "name": mat.get("name"),
                        "hs": mat.get("hs"),
                        "exception_rule": exc,
                        "val": mat.get("val", 0.0)
                    })

        # Kiểm tra chuyển đổi mã số
        if m_prefix == finished_prefix:
            failed_materials.append({
                "name": mat.get("name"),
                "hs": mat.get("hs"),
                "val": mat.get("val", 0.0)
            })

    passed = len(failed_materials) == 0 and len(exception_hits) == 0

    return {
        "finished_hs": finished_hs,
        "rule_type": rule_type,
        "exceptions": exceptions or [],
        "passed": passed,
        "failed_materials": failed_materials,
        "exception_hits": exception_hits,
        "non_qualifying_count": len(failed_materials) + len(exception_hits)
    }

def check_simple_operations(process_steps: List[str]) -> Dict[str, Any]:
    forbidden_keywords = [
        ("bảo quản", "Bảo quản thông thường trong vận chuyển/lưu kho"),
        ("sấy khô", "Sấy khô cơ học đơn giản"),
        ("đóng gói", "Đóng gói / đóng túi bán lẻ"),
        ("dán nhãn", "Dán nhãn mác bao bì"),
        ("pha loãng", "Pha loãng đơn giản bằng nước hoặc dung môi"),
        ("lắp ráp đơn giản", "Lắp ráp đơn giản các linh kiện rời"),
        ("lau bụi", "Lau chùi, làm sạch bề mặt"),
        ("rửa", "Rửa hoặc chọn lọc"),
        ("giết mổ", "Giết mổ động vật đơn thuần")
    ]
    
    flagged = []
    for step in process_steps:
        s_lower = step.lower()
        for kw, desc in forbidden_keywords:
            if kw in s_lower:
                flagged.append({"step": step, "keyword": kw, "warning": desc})
                break
                
    has_complex = any(kw not in step.lower() for step in process_steps for kw, _ in forbidden_keywords) or len(process_steps) > len(flagged)
    
    return {
        "total_steps": len(process_steps),
        "flagged_steps": flagged,
        "risk_level": "CAO" if len(flagged) == len(process_steps) and len(process_steps) > 0 else ("TRUNG BÌNH" if len(flagged) > 0 else "AN TOÀN"),
        "verdict": "Quy trình có công đoạn phức tạp vượt qua gia công đơn giản" if (len(flagged) < len(process_steps) and len(process_steps) > 0) else "CẢNH BÁO: Toàn bộ quy trình chỉ gồm các công đoạn gia công đơn giản!"
    }

def run_comprehensive_roo_audit(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    data format:
    {
      "product_name": str,
      "finished_hs": str,
      "origin_country": str,
      "fta": "ATIGA" | "EVFTA" | "CPTPP" | "RCEP" | "ACFTA",
      "declared_criterion": str,  # e.g. "CTH", "RVC 40%", "VL 70%", "WO", "PE"
      "fob": float,
      "exw": float,
      "materials": [
         {"name": str, "hs": str, "originating": bool, "val": float, "weight": float}
      ],
      "process_steps": [str],
      "psr_rule": str # e.g. "CTH ngoại trừ 11.05", "RVC 40% hoặc CTH", "VL 70%"
    }
    """
    fta = data.get("fta", "ATIGA").upper()
    fob = float(data.get("fob", 0.0))
    exw = float(data.get("exw", 0.0))
    materials = data.get("materials", [])
    process_steps = data.get("process_steps", [])
    declared = data.get("declared_criterion", "")

    total_vnm = sum(m.get("val", 0.0) for m in materials if not m.get("originating", False))
    total_vom = sum(m.get("val", 0.0) for m in materials if m.get("originating", False))

    analysis = {
        "fta": fta,
        "product_name": data.get("product_name", "N/A"),
        "finished_hs": data.get("finished_hs", "N/A"),
        "declared_criterion": declared,
        "fob": fob,
        "exw": exw,
        "vnm_total": total_vnm,
        "vom_total": total_vom,
        "checks": {}
    }

    # 1. Check Simple Operations
    if process_steps:
        analysis["checks"]["simple_operations"] = check_simple_operations(process_steps)

    # 2. Check RVC Build-down (if FOB provided)
    if fob > 0:
        rvc_bd = calculate_rvc_build_down(fob, total_vnm)
        threshold = 40.0
        if fta == "CPTPP":
            threshold = 45.0
        passed = rvc_bd["rvc_percentage"] >= threshold
        analysis["checks"]["rvc_build_down"] = {
            **rvc_bd,
            "threshold": threshold,
            "passed": passed,
            "margin": round(rvc_bd["rvc_percentage"] - threshold, 2)
        }

    # 3. Check EVFTA Value Limit (if EXW provided or FTA is EVFTA)
    if exw > 0:
        analysis["checks"]["evfta_value_limit"] = calculate_evfta_value_limit(exw, total_vnm, threshold=70.0)

    # 4. Check CTC if rule specified
    psr = data.get("psr_rule", "")
    rule_type = "CTH"
    exceptions = []
    if "CC" in psr:
        rule_type = "CC"
    elif "CTSH" in psr:
        rule_type = "CTSH"

    if "ngoại trừ" in psr.lower() or "except" in psr.lower():
        # trích xuất ngoại trừ đơn giản
        parts = psr.replace("ngoại trừ", "except").split("except")
        if len(parts) > 1:
            exc_str = parts[1].strip()
            exceptions = [x.strip() for x in exc_str.replace("nhóm", "").replace("chương", "").replace("heading", "").replace("chapter", "").split(",")]

    ctc_res = evaluate_ctc(data.get("finished_hs", ""), materials, rule_type, exceptions)
    analysis["checks"]["ctc_analysis"] = ctc_res

    # 5. Check De Minimis if CTC failed
    if not ctc_res["passed"] and fob > 0:
        non_qualifying_val = sum(m.get("val", 0.0) for m in ctc_res["failed_materials"]) + sum(m.get("val", 0.0) for m in ctc_res["exception_hits"])
        analysis["checks"]["de_minimis"] = check_de_minimis(fob, non_qualifying_val, threshold=10.0, basis="FOB")

    # Overall Verdict
    eligible = False
    verdict_reasons = []

    if "WO" in declared.upper():
        if total_vnm == 0 and all(m.get("originating", False) for m in materials):
            eligible = True
            verdict_reasons.append("Đáp ứng tiêu chí WO: Không có nguyên liệu ngoài khối.")
        else:
            verdict_reasons.append(f"Không đạt WO: Có {total_vnm} USD nguyên liệu không rõ xuất xứ / nhập khẩu.")
    elif "PE" in declared.upper():
        if total_vnm == 0:
            eligible = True
            verdict_reasons.append("Đáp ứng tiêu chí PE: Sản xuất hoàn toàn từ nguyên liệu có sẵn xuất xứ FTA.")
        else:
            verdict_reasons.append(f"Không đạt PE: Tồn tại nguyên liệu VNM {total_vnm} USD.")
    else:
        # Check PSR
        ctc_ok = ctc_res["passed"]
        de_minimis_ok = analysis["checks"].get("de_minimis", {}).get("passed", False)
        rvc_ok = analysis["checks"].get("rvc_build_down", {}).get("passed", False)
        vl_ok = analysis["checks"].get("evfta_value_limit", {}).get("passed", False)

        if fta == "EVFTA":
            if vl_ok or ctc_ok:
                eligible = True
                verdict_reasons.append("Đạt tiêu chí EVFTA (Value Limit hoặc CTC).")
        else:
            if ctc_ok:
                eligible = True
                verdict_reasons.append(f"Đạt chuyển đổi mã số {rule_type}.")
            elif de_minimis_ok:
                eligible = True
                verdict_reasons.append(f"Đạt tiêu chuẩn xuất xứ thông qua cơ chế Dung sai De Minimis (<= 10% FOB).")
            elif rvc_ok:
                eligible = True
                verdict_reasons.append(f"Đạt hàm lượng giá trị khu vực RVC Build-down ({analysis['checks']['rvc_build_down']['rvc_percentage']}% >= {analysis['checks']['rvc_build_down']['threshold']}%).")
            else:
                verdict_reasons.append("Không đạt cả CTC, De Minimis và ngưỡng RVC yêu cầu.")

    analysis["overall_verdict"] = {
        "eligible": eligible,
        "status": "HỢP LỆ (ĐẠT TIÊU CHUẨN XUẤT XỨ)" if eligible else "CẢNH BÁO: KHÔNG ĐỦ ĐIỀU KIỆN CẤP C/O",
        "reasons": verdict_reasons
    }

    return analysis

def main():
    parser = argparse.ArgumentParser(description="ROO Origin & RVC/VL/De Minimis Calculation Engine")
    parser.add_argument("--file", "-f", type=str, help="Đường dẫn file JSON chứa thông tin tính toán xuất xứ")
    parser.add_argument("--fob", type=float, help="Trị giá FOB (USD)")
    parser.add_argument("--vnm", type=float, help="Trị giá nguyên liệu không xuất xứ (USD)")
    parser.add_argument("--exw", type=float, help="Trị giá xuất xưởng EXW (cho EVFTA)")
    parser.add_argument("--fta", type=str, default="ATIGA", help="Hiệp định (ATIGA, EVFTA, CPTPP, RCEP, ACFTA)")
    parser.add_argument("--rule", type=str, default="CTH", help="Quy tắc PSR (CTH, CC, CTSH)")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON thuần")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload = json.load(f)
        result = run_comprehensive_roo_audit(payload)
    elif args.fob is not None and args.vnm is not None:
        payload = {
            "product_name": "Lô hàng mẫu CLI",
            "finished_hs": "8483.40.90",
            "fta": args.fta,
            "declared_criterion": f"RVC 40% / {args.rule}",
            "fob": args.fob,
            "exw": args.exw or (args.fob * 0.95),
            "materials": [
                {"name": "Thép tấm nhập khẩu", "hs": "7208.39.00", "originating": False, "val": args.vnm},
                {"name": "Vòng bi nội khối", "hs": "8482.10.00", "originating": True, "val": max(args.fob - args.vnm, 0)}
            ],
            "process_steps": ["Cắt gọt phôi thép", "Gia công tiện CNC độ chính xác cao", "Nhiệt luyện tôi cứng bề mặt", "Lắp ráp vòng bi và cân bằng động"],
            "psr_rule": f"CTH hoặc RVC 40%"
        }
        result = run_comprehensive_roo_audit(payload)
    else:
        print("[!] Vui lòng cung cấp file JSON (--file) hoặc nhập --fob và --vnm để chạy tính toán.")
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print(f"📊 BÁO CÁO TÍNH TOÁN XUẤT XỨ (ROO ENGINE) — {result['fta']}")
        print("=" * 70)
        print(f"Sản phẩm: {result['product_name']} | HS: {result['finished_hs']}")
        print(f"Tiêu chí khai báo: {result['declared_criterion']}")
        print(f"Trị giá FOB: {result['fob']:,.2f} USD | EXW: {result['exw']:,.2f} USD")
        print(f"Tổng VNM (Không xuất xứ): {result['vnm_total']:,.2f} USD | VOM (Nội khối): {result['vom_total']:,.2f} USD")
        print("-" * 70)

        if "rvc_build_down" in result["checks"]:
            rb = result["checks"]["rvc_build_down"]
            status_symbol = "✅ ĐẠT" if rb["passed"] else "❌ KHÔNG ĐẠT"
            print(f"Hàm lượng RVC Build-down: {rb['rvc_percentage']}% (Ngưỡng yêu cầu: {rb['threshold']}%) -> {status_symbol} (Biên an toàn: {rb['margin']}%)")

        if "evfta_value_limit" in result["checks"]:
            vl = result["checks"]["evfta_value_limit"]
            status_symbol = "✅ ĐẠT" if vl["passed"] else "❌ VƯỢT HẠN MỨC"
            print(f"Value Limit EVFTA (VNM/EXW): {vl['vnm_ratio']}% (Ngưỡng tối đa: {vl['threshold']}%) -> {status_symbol}")

        if "ctc_analysis" in result["checks"]:
            ctc = result["checks"]["ctc_analysis"]
            ctc_symbol = "✅ ĐẠT" if ctc["passed"] else "❌ KHÔNG ĐẠT"
            print(f"Chuyển đổi mã số ({ctc['rule_type']}): {ctc_symbol}")
            if ctc["exception_hits"]:
                print(f"  ⚠️ Vướng ngoại trừ: {len(ctc['exception_hits'])} nguyên liệu")

        if "de_minimis" in result["checks"]:
            dm = result["checks"]["de_minimis"]
            dm_symbol = "✅ ĐẠT" if dm["passed"] else "❌ VƯỢT 10%"
            print(f"Cơ chế Dung sai De Minimis: {dm['tolerance_ratio']}% FOB (Ngưỡng: {dm['threshold']}%) -> {dm_symbol} ({dm['status']})")

        if "simple_operations" in result["checks"]:
            so = result["checks"]["simple_operations"]
            print(f"Rà soát gia công đơn giản: {so['risk_level']} -> {so['verdict']}")

        print("-" * 70)
        ov = result["overall_verdict"]
        print(f"KẾT LUẬN CUỐI CÙNG: {ov['status']}")
        for r in ov["reasons"]:
            print(f"  • {r}")
        print("=" * 70)

if __name__ == "__main__":
    main()
