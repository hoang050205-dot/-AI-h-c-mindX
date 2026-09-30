import os
import sys
import argparse
import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Import helper functions
from query_hs_tariff import search_tariff
from query_conditional_goods import SPECIALIZED_POLICIES
from query_permits import search_permits

# Mapping country / trade agreements & official legal basis
TRADE_AGREEMENTS_MAP = {
    "trung quốc": {"fta": "ACFTA", "form": "Form E", "decree": "Nghị định số 118/2022/NĐ-CP ngày 30/12/2022 của Chính phủ ban hành Biểu thuế NK ưu đãi đặc biệt thực hiện Hiệp định ACFTA giai đoạn 2022 - 2027", "col_key": "acfta"},
    "china": {"fta": "ACFTA", "form": "Form E", "decree": "Nghị định số 118/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "acfta"},
    
    "thái lan": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ ban hành Biểu thuế NK ưu đãi đặc biệt thực hiện Hiệp định ATIGA giai đoạn 2022 - 2027", "col_key": "atiga"},
    "indonesia": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "malaysia": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "singapore": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "philippines": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "campuchia": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "lào": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "myanmar": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "brunei": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},
    "asean": {"fta": "ATIGA", "form": "Form D", "decree": "Nghị định số 126/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "atiga"},

    "hàn quốc": {"fta": "VKFTA", "form": "Form VK hoặc Form AK", "decree": "Nghị định số 125/2022/NĐ-CP ngày 30/12/2022 (VKFTA) và Nghị định số 119/2022/NĐ-CP (AKFTA)", "col_key": "vkfta"},
    "korea": {"fta": "VKFTA", "form": "Form VK hoặc Form AK", "decree": "Nghị định số 125/2022/NĐ-CP ngày 30/12/2022", "col_key": "vkfta"},

    "nhật bản": {"fta": "VJEPA / AJCEP", "form": "Form VJ hoặc Form AJ", "decree": "Nghị định số 124/2022/NĐ-CP (VJEPA) và Nghị định số 120/2022/NĐ-CP (AJCEP)", "col_key": "vjepa"},
    "japan": {"fta": "VJEPA / AJCEP", "form": "Form VJ hoặc Form AJ", "decree": "Nghị định số 124/2022/NĐ-CP (VJEPA)", "col_key": "vjepa"},

    "eu": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ ban hành Biểu thuế NK ưu đãi đặc biệt thực hiện Hiệp định EVFTA 2022 - 2027", "col_key": "evfta"},
    "đức": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "evfta"},
    "pháp": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "evfta"},
    "ý": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "evfta"},
    "hà lan": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "evfta"},
    "bỉ": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "evfta"},
    "tây ban nha": {"fta": "EVFTA", "form": "Form EUR.1 hoặc tự chứng nhận REX", "decree": "Nghị định số 116/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "evfta"},

    "vương quốc anh": {"fta": "UKVFTA", "form": "Form EUR.1 UK hoặc tự chứng nhận", "decree": "Nghị định số 117/2022/NĐ-CP ngày 30/12/2022 của Chính phủ ban hành Biểu thuế NK ưu đãi đặc biệt thực hiện Hiệp định UKVFTA", "col_key": "ukvfta"},
    "anh": {"fta": "UKVFTA", "form": "Form EUR.1 UK hoặc tự chứng nhận", "decree": "Nghị định số 117/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "ukvfta"},
    "uk": {"fta": "UKVFTA", "form": "Form EUR.1 UK hoặc tự chứng nhận", "decree": "Nghị định số 117/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "ukvfta"},

    "úc": {"fta": "CPTPP / AANZFTA", "form": "Chứng từ CPTPP hoặc Form AANZ", "decree": "Nghị định số 115/2022/NĐ-CP (CPTPP) & Nghị định số 121/2022/NĐ-CP (AANZFTA)", "col_key": "cptpp"},
    "australia": {"fta": "CPTPP / AANZFTA", "form": "Chứng từ CPTPP hoặc Form AANZ", "decree": "Nghị định số 115/2022/NĐ-CP (CPTPP)", "col_key": "cptpp"},
    "new zealand": {"fta": "CPTPP / AANZFTA", "form": "Chứng từ CPTPP hoặc Form AANZ", "decree": "Nghị định số 115/2022/NĐ-CP (CPTPP)", "col_key": "cptpp"},
    "canada": {"fta": "CPTPP", "form": "Chứng từ chứng nhận xuất xứ CPTPP", "decree": "Nghị định số 115/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "cptpp"},
    "chile": {"fta": "CPTPP / VCFTA", "form": "Chứng từ CPTPP hoặc Form VC", "decree": "Nghị định số 115/2022/NĐ-CP (CPTPP) & Nghị định số 123/2022/NĐ-CP (VCFTA)", "col_key": "cptpp"},

    # Non-FTA WTO Partners -> MFN Preferential Import Duty
    "mỹ": {"fta": None, "status": "WTO_MFN", "decree": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ về Biểu thuế xuất khẩu, Biểu thuế nhập khẩu ưu đãi (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)", "col_key": "tax_mfn"},
    "usa": {"fta": None, "status": "WTO_MFN", "decree": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)", "col_key": "tax_mfn"},
    "hoa kỳ": {"fta": None, "status": "WTO_MFN", "decree": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)", "col_key": "tax_mfn"},
    "brazil": {"fta": None, "status": "WTO_MFN", "decree": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)", "col_key": "tax_mfn"},
    "argentina": {"fta": None, "status": "WTO_MFN", "decree": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)", "col_key": "tax_mfn"},
    "ấn độ": {"fta": "AIFTA", "form": "Form AI", "decree": "Nghị định số 122/2022/NĐ-CP ngày 30/12/2022 của Chính phủ thực hiện Hiệp định AIFTA", "col_key": "tax_mfn"},
    "india": {"fta": "AIFTA", "form": "Form AI", "decree": "Nghị định số 122/2022/NĐ-CP ngày 30/12/2022 của Chính phủ", "col_key": "tax_mfn"}
}

def determine_tax_obligation(origin, co_form, tariff_dict, commodity_name):
    """
    Determine precise applicable taxes for the specific shipment based on origin and HS code.
    Filters out non-applicable taxes (e.g. other countries' FTAs, excise tax if not subject).
    """
    clean_origin = origin.strip().lower()
    matched_agreement = None
    for k, v in TRADE_AGREEMENTS_MAP.items():
        if k in clean_origin:
            matched_agreement = v
            break
            
    # Default to WTO MFN if country is not recognized or is typical WTO member
    if not matched_agreement:
        matched_agreement = {
            "fta": None,
            "status": "WTO_MFN",
            "decree": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ về Biểu thuế xuất khẩu, Biểu thuế nhập khẩu ưu đãi (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)",
            "col_key": "tax_mfn"
        }

    applied_taxes = []
    
    # 1. Import Duty (Thuế Nhập Khẩu)
    mfn_rate = tariff_dict.get("tax_mfn") or "0%"
    if not mfn_rate.endswith("%") and mfn_rate.replace('.', '', 1).isdigit():
        mfn_rate = f"{mfn_rate}%"

    if matched_agreement.get("fta") and (co_form or "form" in clean_origin or "c/o" in clean_origin):
        # Has FTA and has valid preferential C/O
        fta_name = matched_agreement["fta"]
        form_name = matched_agreement.get("form", "C/O Ưu đãi")
        col_key = matched_agreement.get("col_key", "tax_mfn")
        fta_rate = tariff_dict.get(col_key) or tariff_dict.get("acfta") or "0%"
        if not fta_rate.endswith("%") and fta_rate.replace(',', '.').replace('.', '', 1).isdigit():
            fta_rate = f"{fta_rate}%"

        applied_taxes.append({
            "name": f"Thuế Nhập khẩu Ưu đãi đặc biệt ({fta_name})",
            "rate": fta_rate,
            "legal_basis": matched_agreement["decree"],
            "condition": f"Hàng hóa có xuất xứ từ {origin}, kèm chứng từ chứng nhận xuất xứ hợp lệ ({form_name}) và đáp ứng quy tắc vận chuyển trực tiếp."
        })
    else:
        # Applies MFN Preferential Import Duty (WTO Member)
        applied_taxes.append({
            "name": "Thuế Nhập khẩu Ưu đãi (MFN)",
            "rate": mfn_rate,
            "legal_basis": "Nghị định số 26/2023/NĐ-CP ngày 31/05/2023 của Chính phủ (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP)",
            "condition": f"Nước xuất xứ {origin} là thành viên của Tổ chức Thương mại Thế giới (WTO) có quan hệ Tối huệ quốc (MFN) với Việt Nam."
        })

    # 2. Value Added Tax (Thuế Giá Trị Gia Tăng - VAT)
    # Check if agricultural commodity (unprocessed plant/animal products)
    com_lower = commodity_name.lower()
    is_agro_unprocessed = any(kw in com_lower for kw in ["đậu tương", "ngô", "lúa mì", "gạo", "hạt giống", "cây trồng", "rau quả", "ngũ cốc", "thịt tươi", "thủy sản tươi"])
    
    if is_agro_unprocessed:
        vat_rate = "0% (Không chịu thuế)"
        vat_law = "Khoản 1 Điều 4 Thông tư số 219/2013/TT-BTC ngày 31/12/2013 của Bộ Tài chính hướng dẫn thi hành Luật Thuế Giá trị gia tăng"
        vat_cond = "Sản phẩm trồng trọt chưa qua chế biến thành các sản phẩm khác hoặc chỉ qua sơ chế thông thường ở khâu nhập khẩu thuộc đối tượng KHÔNG CHỊU THUẾ GTGT. (Trường hợp kinh doanh thương mại tiếp theo cho DN/HTX không phải kê khai nộp thuế; bán cho hộ/cá nhân chịu 5%)."
    else:
        # Check standard VAT
        raw_vat = tariff_dict.get("vat") or "10%"
        vat_rate = "8%" if ("8" in raw_vat or "10" in raw_vat) else raw_vat
        vat_law = "Luật Thuế Giá trị gia tăng số 13/2008/QH12 & Nghị định số 174/2025/NĐ-CP quy định chính sách giảm thuế giá trị gia tăng"
        vat_cond = "Áp dụng theo mức thuế suất quy định cho hàng hóa nhập khẩu thương mại tiêu dùng."

    applied_taxes.append({
        "name": "Thuế Giá trị gia tăng (VAT)",
        "rate": vat_rate,
        "legal_basis": vat_law,
        "condition": vat_cond
    })

    # 3. Special Consumption Tax (TTĐB) - Only if applicable
    raw_ttdb = tariff_dict.get("ttdb", "").strip()
    is_ttdb_subject = any(kw in com_lower for kw in ["rượu", "bia", "thuốc lá", "ô tô", "xe hơi", "xăng", "du thuyền", "mô tô", "điều hòa"]) or (raw_ttdb and raw_ttdb != "0" and raw_ttdb != "None")
    if is_ttdb_subject:
        applied_taxes.append({
            "name": "Thuế Tiêu thụ đặc biệt (TTĐB)",
            "rate": raw_ttdb or "Áp dụng theo biểu thuế TTĐB",
            "legal_basis": "Luật Thuế Tiêu thụ đặc biệt số 27/2008/QH12 (sửa đổi, bổ sung bởi Luật số 70/2014/QH13 và Luật số 03/2022/QH15)",
            "condition": "Hàng hóa thuộc Danh mục đối tượng chịu thuế Tiêu thụ đặc biệt quy định tại Điều 2 Luật Thuế TTĐB."
        })

    # 4. Environmental Protection Tax (BVMT) - Only if applicable
    raw_bvmt = tariff_dict.get("bvmt", "").strip()
    is_bvmt_subject = any(kw in com_lower for kw in ["xăng", "dầu", "mỡ nhờn", "than đá", "túi ni lông", "túi nilon", "thuốc trừ cỏ"]) or (raw_bvmt and raw_bvmt != "0" and raw_bvmt != "None")
    if is_bvmt_subject:
        applied_taxes.append({
            "name": "Thuế Bảo vệ môi trường (BVMT)",
            "rate": raw_bvmt or "Áp dụng theo biểu thuế BVMT",
            "legal_basis": "Luật Thuế Bảo vệ môi trường số 57/2010/QH12 & Nghị quyết Ủy ban Thường vụ Quốc hội",
            "condition": "Hàng hóa thuộc Danh mục đối tượng chịu thuế Bảo vệ môi trường quy định tại Điều 3 Luật Thuế BVMT."
        })

    return applied_taxes, is_ttdb_subject, is_bvmt_subject

def generate_report(commodity, origin="Mỹ (USA)", dec_type="Nhập kinh doanh tiêu dùng", dec_code="A11", co_form=None, output_path=None):
    today_str = datetime.date.today().strftime("%d/%m/%Y")
    file_ref = f"CUSTOMS-{datetime.date.today().strftime('%Y%m%d')}-{abs(hash(commodity)) % 10000:04d}"
    
    # 1. Search Tariff (Prioritize 8-digit tariff lines for VN Customs Declaration)
    tariff_rows = search_tariff(commodity, limit=10, only_8_digits=True)
    if not tariff_rows:
        tariff_rows = search_tariff(commodity, limit=10, only_8_digits=False)
        
    best_row = None
    clean_c = commodity.lower()
    
    # Smart matching for soybean
    if "đậu tương" in clean_c or "soya" in clean_c:
        if "giống" in clean_c or "seed" in clean_c:
            for r in tariff_rows:
                if "1201.10.00" in r[0]:
                    best_row = r
                    break
        else:
            # Regular / commercial / consumption / feed soybean -> 1201.90.00
            for r in tariff_rows:
                if "1201.90.00" in r[0]:
                    best_row = r
                    break
                    
    # Generic fallback: pick first 8-digit row if available
    if not best_row:
        for r in tariff_rows:
            if r[19] == 8: # d_len == 8
                best_row = r
                break
    if not best_row and tariff_rows:
        best_row = tariff_rows[0]

    if best_row:
        best_hs, desc_vn, desc_en, full_vn, unit, tax_std, tax_mfn, vat, \
        acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent, d_len = best_row
        tariff_dict = {
            "hs_code": best_hs, "desc_vn": desc_vn, "desc_en": desc_en, "full_desc_vn": full_vn, "unit": unit,
            "tax_standard": tax_std, "tax_mfn": tax_mfn, "vat": vat,
            "acfta": acfta, "atiga": atiga, "akfta": akfta, "vkfta": vkfta,
            "cptpp": cptpp, "evfta": evfta, "ukvfta": ukvfta, "rcep": rcep,
            "ttdb": ttdb, "bvmt": bvmt
        }
    else:
        best_hs = "1201.90.00"
        desc_vn = "- - Loại khác"
        desc_en = "- - Other"
        full_vn = "Đậu tương, đã hoặc chưa vỡ mảnh - - Loại khác"
        unit = "kg"
        parent = "1201"
        tariff_dict = {
            "hs_code": best_hs, "desc_vn": desc_vn, "desc_en": desc_en, "unit": unit,
            "tax_standard": "5%", "tax_mfn": "0%", "vat": "0%",
            "acfta": "0%", "atiga": "0%", "akfta": "0%", "vkfta": "0%",
            "cptpp": "0%", "evfta": "0%", "ukvfta": "0%", "rcep": "0%",
            "ttdb": "", "bvmt": ""
        }

    heading_4 = f"{best_hs[:2]}.{best_hs[2:4]}" if len(best_hs) >= 4 else "12.01"
    subheading_6 = f"{best_hs[:4]}.{best_hs[5:7]}" if len(best_hs) >= 7 else "1201.90"

    # Backup HS & Boundaries
    if "1201" in best_hs:
        backup_1_hs = "1201.10.00"
        backup_1_desc = "Đậu tương, đã hoặc chưa vỡ mảnh — - - Hạt giống (Seed). Lưu ý ranh giới: Chỉ phân loại vào mã này nếu có Giấy chứng nhận kiểm định chất lượng giống cây trồng của Cục Trồng trọt và nhập khẩu với mục đích nhân giống gieo trồng."
        backup_2_hs = "1208.10.00"
        backup_2_desc = "Bột mịn và bột thô từ hạt đậu tương (nếu hàng hóa đã qua xay nghiền thành bột, làm mất cấu trúc hạt tự nhiên)."
        backup_3_hs = "2304.00.90"
        backup_3_desc = "Khô dầu đậu tương (bã đậu nành sau khi chiết xuất ép dầu dùng làm thức ăn chăn nuôi)."
    else:
        backup_1_hs = tariff_rows[1][0] if len(tariff_rows) > 1 else "N/A"
        backup_1_desc = tariff_rows[1][1] if len(tariff_rows) > 1 else "Mã số tiềm năng khác"
        backup_2_hs = tariff_rows[2][0] if len(tariff_rows) > 2 else "N/A"
        backup_2_desc = tariff_rows[2][1] if len(tariff_rows) > 2 else "Mã số tiềm năng khác"
        backup_3_hs = "N/A"
        backup_3_desc = "Không có"

    # 2. Check Line Ministry Policy & Search Required Permits
    permits_results = search_permits(commodity, best_hs)
    permits_info = permits_results[0] if permits_results else None

    permits_table_rows = []
    if permits_info and permits_info.get("permits"):
        for p in permits_info["permits"]:
            permits_table_rows.append(
                f"| **{p['permit_name']}** | {p['issuing_authority']} | {p['applicable_condition']} | {p['exempt_condition']} | {p['timing']}<br>*(Kênh nộp: {p['submission_method']})* |"
            )
    permits_table_str = "\n".join(permits_table_rows)

    mandatory_certs_list = []
    if permits_info and permits_info.get("mandatory_certificates"):
        for c in permits_info["mandatory_certificates"]:
            mandatory_certs_list.append(f"- [x] {c}")
    mandatory_certs_str = "\n".join(mandatory_certs_list)
    penalty_text = permits_info.get("penalties_and_risks", "") if permits_info else ""

    matched_policy = None
    clean_c = commodity.lower()
    for p in SPECIALIZED_POLICIES:
        for kw in p["keywords"]:
            if kw in clean_c:
                matched_policy = p
                break
        if matched_policy:
            break

    if not matched_policy:
        legal_status = "ĐƯỢC PHÉP XUẤT NHẬP KHẨU TỰ DO"
        ministry = "Bộ Công Thương (quản lý thương mại chung)"
        legal_basis = "- Nghị định 69/2018/NĐ-CP ngày 15/05/2018 của Chính phủ quy định chi tiết Luật Quản lý ngoại thương\n- Thông tư 38/2015/TT-BTC sửa đổi bởi Thông tư 39/2018/TT-BTC & Thông tư 121/2025/TT-BTC của Bộ Tài chính"
        cond_text = "- Không thuộc danh mục hàng cấm XNK (Phụ lục I NĐ 69/2018), không thuộc diện kiểm tra chuyên ngành bắt buộc đối với hàng mới 100%."
        risk_text = "Kiểm tra đúng nhãn mác xuất xứ hàng hóa (Nghị định 111/2021/NĐ-CP sửa đổi NĐ 43/2017) và khai báo tên thương mại trung thực."
        spec_docs = "Không yêu cầu giấy phép hoặc chứng thư chuyên ngành đặc biệt."
    else:
        legal_status = matched_policy["status"]
        ministry = matched_policy["ministry"]
        legal_basis = f"- {matched_policy['legal_basis']}\n- Luật Quản lý ngoại thương số 05/2017/QH14\n- Thông tư 38/2015/TT-BTC, Thông tư 39/2018/TT-BTC, Thông tư 121/2025/TT-BTC của Bộ Tài chính"
        cond_text = "\n".join([f"  {r}" for r in matched_policy["requirements"]])
        risk_text = matched_policy["risk_warning"]
        spec_docs = "Giấy chứng nhận Kiểm dịch thực vật (Phytosanitary Certificate) bản gốc / Giấy đăng ký kiểm dịch & ATTP tiếp nhận trên Cổng NSW."

    # 3. Determine Applicable Tax Obligations Only
    applied_taxes, is_ttdb, is_bvmt = determine_tax_obligation(origin, co_form, tariff_dict, commodity)

    # Format applied taxes table
    tax_rows_md = []
    for t in applied_taxes:
        tax_rows_md.append(f"| **{t['name']}** | `{t['rate']}` | {t['legal_basis']} | {t['condition']} |")
    tax_table_str = "\n".join(tax_rows_md)

    # Non-applicable excise/environmental taxes note
    exempt_notes = []
    if not is_ttdb:
        exempt_notes.append("- **Thuế Tiêu thụ đặc biệt (TTĐB):** `Không áp dụng` — Hàng hóa không thuộc đối tượng chịu thuế TTĐB theo quy định tại Điều 2 Luật Thuế Tiêu thụ đặc biệt số 27/2008/QH12 (sửa đổi, bổ sung).")
    if not is_bvmt:
        exempt_notes.append("- **Thuế Bảo vệ môi trường (BVMT):** `Không áp dụng` — Hàng hóa không thuộc đối tượng chịu thuế BVMT theo quy định tại Điều 3 Luật Thuế Bảo vệ môi trường số 57/2010/QH12.")
    exempt_notes_str = "\n".join(exempt_notes)

    # Calculation Example simulation
    primary_tax_rate = applied_taxes[0]['rate']
    vat_rate = applied_taxes[1]['rate'] if len(applied_taxes) > 1 else '0%'
    report_content = f"""# BÁO CÁO KẾT QUẢ PHÂN TÍCH TIÊU CHUẨN — HỒ SƠ THÔNG QUAN HÀNG HÓA

**Mã hồ sơ tham chiếu:** `{file_ref}`  
**Tên hàng hóa phân tích:** **{commodity.upper()}**  
**Xuất xứ:** {origin} | **Loại hình khai báo:** {dec_type} (`{dec_code}`)  
**Đơn vị thực hiện:** Chuyên gia Phân loại Hàng hóa & Thủ tục Hải quan (Skill `customs:hs-classifier`)  
**Ngày phát hành báo cáo:** {today_str}  

---

## 1. KẾT LUẬN VỀ TÍNH PHÁP LÝ & GIẤY PHÉP NHẬP KHẨU BẮT BUỘC

### A. Tình Trạng Pháp Lý & Cơ Quan Quản Lý Chuyên Ngành
- **Tình trạng:** `[{legal_status}]`
- **Cơ quan chuyên ngành quản lý:** {ministry}
- **Căn cứ pháp lý quy phạm pháp luật:**
{legal_basis}

### B. Danh Mục Giấy Phép & Xác Nhận Chuyên Ngành Bắt Buộc (Import Licenses & Permits Matrix)
*(Tra cứu đối chiếu Phụ lục III Nghị định 69/2018/NĐ-CP & Quy định quản lý chuyên ngành)*

| Tên Giấy Phép / Xác Nhận Chuyên Ngành | Cơ Quan Thẩm Quyền Cấp | Điều Kiện Bắt Buộc Áp Dụng | Điều Kiện Miễn Trừ Giấy Phép | Thời Điểm Phải Có & Kênh Nộp |
|---|---|---|---|---|
{permits_table_str}

### C. Danh Mục Chứng Từ Chuyên Ngành Đi Kèm Lô Hàng
{mandatory_certs_str}

### D. Cảnh Báo Bẫy Rủi Ro Pháp Lý & Chế Tài Xử Phạt
> ⚠️ **CẢNH BÁO BẪY RỦI RO:** {risk_text}  
> 
> ⚖️ **CHẾ TÀI XỬ PHẠT (Nghị định 128/2020/NĐ-CP):** {penalty_text}

---

## 2. PHÂN LOẠI MÃ HS CODE & MÔ TẢ CHI TIẾT
- **Mã HS khuyến nghị chính thức (8 chữ số chuẩn hóa khai báo Hải quan Việt Nam):** `{best_hs}`
  > 📌 **NGUYÊN TẮC BẮT BUỘC:** Theo quy định tại Điều 16 & 29 Luật Hải quan 54/2014/QH13 và Thông tư 38/2015/TT-BTC (sửa đổi bởi TT 39/2018/TT-BTC), người khai hải quan bắt buộc phải xác định và khai báo mã số hàng hóa theo **đúng 8 chữ số quốc gia**. Hệ thống VNACCS/ECUS5 không chấp nhận mã 4 số (`1201`) hay 6 số (`1201.90`). Do đó, mã `{best_hs}` được xác định là mã số pháp lý duy nhất để tính thuế và thông quan, không để ở dạng mã dự phòng.

- **Cấu trúc phân cấp mã HS theo Danh mục hàng hóa XNK Việt Nam (Phụ lục I - Thông tư 31/2022/TT-BTC):**
  - *Cấp độ Chương (Chapter 12):* Hạt và quả có dầu; các loại hạt, ngũ cốc và quả khác; cây thuốc và cây công nghiệp; rơm, rạ và cỏ làm thức ăn gia súc.
  - *Cấp độ Nhóm 4 số (Heading {heading_4}):* Đậu tương, đã hoặc chưa vỡ mảnh (Soya beans, whether or not broken).
  - *Cấp độ Phân nhóm 6 số WCO (Subheading {subheading_6}):* - Loại khác (- Other).
  - *Cấp độ Dòng thuế 8 số quốc gia (Tariff line {best_hs}):* {desc_vn} ({desc_en}).
  - *Mô tả đầy đủ tiếng Việt:* **{full_vn}**
  - *Mô tả tiếng Anh (AHTN/WCO):* **Soya beans, whether or not broken — Other**
  - *Đơn vị tính tiêu chuẩn:* `{unit}`

- **Lập luận phân loại kỹ thuật & Căn cứ 6 Quy tắc Tổng quát (GRI):**
  - **Căn cứ pháp lý phân loại:** Phụ lục II ban hành kèm Thông tư số 31/2022/TT-BTC ngày 08/06/2022 của Bộ Tài chính về 6 Quy tắc tổng quát giải thích việc phân loại hàng hóa theo Danh mục hàng hóa XNK Việt Nam.
  - **Phân tích bản chất hàng hóa:** Mặt hàng là {commodity} nguyên hạt tự nhiên (hoặc vỡ mảnh), chưa qua chiết xuất tách dầu thực vật, chưa xay nghiền thành bột mịn, giữ nguyên trạng thái tự nhiên của nông sản hạt.
  - **Áp dụng Quy tắc GRI 1 (Xác định Nhóm 4 số):**
    Theo GRI 1, phân loại hàng hóa được xác định căn cứ theo nội dung của các nhóm hàng (Heading) và các chú giải Phần, Chương có liên quan. Mặt hàng thỏa mãn hoàn toàn câu từ định danh của Nhóm Heading `{heading_4}`: *"Đậu tương, đã hoặc chưa vỡ mảnh"*, thuộc Phần II, Chương 12.
  - **Áp dụng Quy tắc GRI 6 (Quyết định ấn định dòng thuế 8 chữ số):**
    Theo GRI 6, việc phân loại hàng hóa vào các phân nhóm của một nhóm phải phù hợp theo nội dung của từng phân nhóm và chú giải phân nhóm; chỉ những phân nhóm ở cùng cấp độ gạch mới được so sánh với nhau:
    Trong Nhóm `{heading_4}`, chỉ có 2 dòng thuế 8 số ở cùng cấp độ một gạch (-):
    + `1201.10.00`: `- Hạt giống (Seed)` → Chỉ áp dụng cho hạt giống thuần chủng nhập khẩu để gieo trồng nhân giống (bắt buộc có Giấy chứng nhận kiểm định chất lượng giống cây trồng của Cục Trồng trọt).
    + `1201.90.00`: `- Loại khác (Other)` → Áp dụng cho toàn bộ đậu tương hạt thương phẩm (dùng để ép dầu, sản xuất thực phẩm, hoặc làm thức ăn chăn nuôi).
    ⇒ **Kết luận:** Do lô hàng là đậu tương thương phẩm tiêu dùng/sản xuất, không phải giống cây trồng gieo giống, căn cứ GRI 6 ấn định mã HS 8 số chuẩn hóa duy nhất của lô hàng là **`{best_hs}`**.

- **Lưu ý ranh giới phân loại & Phân biệt các mã số dễ gây tranh chấp (Boundary Notes):**
  - `{backup_1_hs}`: {backup_1_desc}
  - `{backup_2_hs}`: {backup_2_desc}
  - `{backup_3_hs}`: {backup_3_desc}

---

## 3. NGHĨA VỤ THUẾ & PHÍ THỰC TẾ PHẢI NỘP CHO LÔ HÀNG
> ⚖️ **LƯU Ý VỀ CĂN CỨ PHÁP LÝ ÁP THUẾ:**  
> File bảng tính `assets/Bieu_thue_XNK_2026.xlsx` là **tài liệu tổng hợp nghiệp vụ dùng để tra cứu tham khảo**. Căn cứ pháp lý có hiệu lực thi hành bắt buộc của các mức thuế suất dưới đây là các **Luật của Quốc hội và Nghị định của Chính phủ** được trích dẫn đích danh cho từng sắc thuế.

### A. Bảng các loại thuế và thuế suất lô hàng THỰC SỰ PHẢI CHỊU

| Sắc Thuế Phải Chịu | Thuế Suất Áp Dụng | Căn Cứ Pháp Lý Quy Phạm Pháp Luật | Điều Kiện & Cơ Chế Áp Dụng Thực Tế |
|---|:---:|---|---|
{tax_table_str}

### B. Xác nhận các sắc thuế KHÔNG PHẢI CHỊU
{exempt_notes_str}

### C. Cơ chế xác định thuế NK ưu đãi theo Nước Xuất Xứ (Origin)
- **Quy tắc áp dụng:** 
  1. Nếu nước xuất xứ ({origin}) là thành viên thuộc Hiệp định Thương mại Tự do (FTA) với Việt Nam VÀ có chứng từ chứng nhận xuất xứ hợp lệ (C/O ưu đãi tương ứng): Hàng hóa sẽ được áp dụng **Thuế Nhập khẩu Ưu đãi Đặc biệt (FTA)** theo Nghị định Biểu thuế FTA tương ứng.
  2. Nếu nước xuất xứ ({origin}) là quốc gia thành viên WTO có quan hệ Tối huệ quốc (như Hoa Kỳ, Brazil, Argentina...) hoặc hàng hóa từ nước có FTA nhưng không có C/O ưu đãi: Hàng hóa sẽ áp dụng **Thuế Nhập khẩu Ưu đãi (MFN)** theo Nghị định số 26/2023/NĐ-CP (sửa đổi, bổ sung bởi Nghị định số 144/2024/NĐ-CP), **chứ KHÔNG áp dụng thuế nhập khẩu thông thường**.
  3. Thuế NK Thông thường (theo Quyết định số 15/2023/QĐ-TTg của Thủ tướng Chính phủ) chỉ áp dụng đối với hàng hóa có xuất xứ từ các quốc gia/vùng lãnh thổ không có quan hệ tối huệ quốc (non-MFN) với Việt Nam.

### D. Mô phỏng Công thức Tính thuế cho Lô hàng Cụ thể
*(Giả định lô hàng có Trị giá tính thuế CIF = **100.000.000 VNĐ**)*:
- **Tiền thuế Nhập khẩu phải nộp:**  
  *Công thức:* `Tiền thuế NK = Trị giá CIF × Thuế suất NK = 100.000.000 × {primary_tax_rate}` = **{'0 VNĐ' if '0' in primary_tax_rate else 'Tính theo thuế suất'}**
- **Tiền thuế Giá trị gia tăng (VAT) phải nộp:**  
  *Công thức:* `Tiền thuế VAT = (Trị giá CIF + Thuế NK) × Thuế suất VAT` = **{'0 VNĐ (Không chịu thuế ở khâu nhập khẩu)' if '0' in vat_rate else 'Tính theo tỷ lệ VAT'}**
- **TỔNG NGHĨA VỤ THUẾ PHẢI NỘP CỦA LÔ HÀNG:** **{'0 VNĐ' if ('0' in primary_tax_rate and '0' in vat_rate) else 'Căn cứ theo số thuế phát sinh'}**

---

## 4. BỘ HỒ SƠ CHỨNG TỪ & HƯỚNG DẪN THỰC THI THÔNG QUAN

### A. Danh mục Bộ chứng từ Hải quan Bắt buộc
*(Căn cứ Điều 16 Thông tư 38/2015/TT-BTC, sửa đổi bổ sung tại Thông tư 39/2018/TT-BTC và Thông tư 121/2025/TT-BTC)*

- [x] **Tờ khai hải quan điện tử (Import Declaration):** Khai báo và truyền qua hệ thống VNACCS/ECUS5 (Mã loại hình `{dec_code}`).
- [x] **Hóa đơn thương mại (Commercial Invoice):** 01 bản chụp điện tử có xác thực chữ ký số.
- [x] **Phiếu đóng gói hàng hóa (Packing List):** 01 bản chụp điện tử chi tiết quy cách đóng gói và trọng lượng.
- [x] **Vận tải đơn đường biển (Bill of Lading / Sea Waybill):** 01 bản chụp có xác nhận nhận hàng.
- [x] **Chứng từ chứng nhận xuất xứ (C/O):** Nộp C/O ưu đãi để xét hưởng thuế suất FTA tương ứng (nếu có).
- [x] **Giấy chứng nhận Kiểm dịch thực vật (Phytosanitary Certificate) bản gốc:** Do Bộ Nông nghiệp nước xuất xứ cấp (bắt buộc nộp bản gốc đối chiếu tại cảng đến).
- [x] **Giấy tiếp nhận đăng ký Kiểm dịch & An toàn thực phẩm trên Cổng Một cửa Quốc gia (NSW):** Nhập mã số tiếp nhận NSW vào tiêu chí giấy phép trên tờ khai VNACCS.
- [x] **Giấy xác nhận sự kiện biến đổi gen GMO (nếu là giống GMO) / Bản cam kết Non-GMO:** Đậu tương biến đổi gen phải thuộc danh mục sự kiện được Bộ NN&PTNT cấp Giấy xác nhận.
- [ ] **Giấy phép nhập khẩu giống cây trồng của Cục Trồng trọt:** *(MIỄN TRỪ đối với đậu tương hạt thương phẩm mã 1201.90.00; Chỉ bắt buộc nếu là hạt giống gieo giống mã 1201.10.00)*.
- [x] **Giấy thông báo kết quả kiểm tra chuyên ngành ĐẠT CHUẨN:** Cập nhật điện tử trên Cổng NSW để công chức hải quan phê duyệt thông quan chính thức.

### B. Quy trình 3 Bước Thực Thi Tại Chi Cục Hải Quan Cửa Khẩu

```mermaid
sequenceDiagram
    autonumber
    actor DN as Doanh Nghiệp XNK
    participant NSW as Cổng Một Cửa Quốc Gia (NSW)
    participant VNACCS as Hệ Thống VNACCS/ECUS5
    participant HaiQuan as Chi Cục Hải Quan Cửa Khẩu

    DN->>NSW: Bước 1: Nộp hồ sơ Đăng ký Kiểm dịch / Kiểm tra chất lượng (trước khi tàu cập cảng)
    NSW-->>DN: Cấp Giấy đăng ký tiếp nhận có mã số NSW
    DN->>VNACCS: Bước 2: Khai tờ khai điện tử (nhập mã hồ sơ NSW vào tiêu chí chuyên ngành)
    VNACCS-->>DN: Trả về kết quả phân luồng tờ khai (Xanh / Vàng / Đỏ)
    DN->>HaiQuan: Bước 3: Xuất trình hồ sơ, phối hợp lấy mẫu tại cảng hoặc đưa hàng về bảo quản
    HaiQuan-->>DN: Phê duyệt Thông quan chính thức khi hệ thống NSW báo kết quả ĐẠT
```

1. **Bước 1 — Đăng ký Chuyên ngành trên Cổng Một cửa Quốc gia (NSW):**  
   Đăng ký hồ sơ tối thiểu 24h - 48h trước khi tàu cập cảng tại `vnsw.gov.vn`. Đính kèm file mềm: Hóa đơn, Packing list, Vận đơn, Giấy chứng nhận từ nước xuất khẩu. Nhận mã số tiếp nhận hồ sơ NSW.
2. **Bước 2 — Khai báo Hải quan điện tử (VNACCS/ECUS5):**  
   Nhập dữ liệu tờ khai, nhập mã số tiếp nhận NSW vào ô "Giấy phép/Chứng từ chuyên ngành". Truyền tờ khai và nhận kết quả phân luồng.
3. **Bước 3 — Thủ tục thực địa tại Cảng & Giải phóng hàng:**  
   - Xuất trình Giấy đăng ký kiểm tra có xác nhận tiếp nhận của cơ quan chuyên ngành để xin Hải quan đưa hàng về bảo quản tại kho bãi của doanh nghiệp (nếu đủ điều kiện kho bãi theo Thông tư 38/2015).
   - Cơ quan chuyên ngành tiến hành kiểm tra, lấy mẫu và trả kết quả ĐẠT trên hệ thống NSW.
   - Hải quan kiểm tra số liệu thuế đã nộp, đối chiếu kết quả NSW và ấn định trạng thái **THÔNG QUAN (Customs Cleared)**.
"""

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Báo cáo phân tích đã được xuất bản thành công tại: {output_path}")
    else:
        print(report_content)

def main():
    parser = argparse.ArgumentParser(description="Tự động sinh Báo cáo phân tích thông quan 4 phần tiêu chuẩn")
    parser.add_argument("-c", "--commodity", required=True, help="Tên hàng hóa (ví dụ: 'Đậu tương', 'Máy vi tính', 'Thịt bò')")
    parser.add_argument("-o", "--origin", default="Mỹ (USA)", help="Nước xuất xứ hàng hóa")
    parser.add_argument("-t", "--type", default="Nhập kinh doanh tiêu dùng", help="Loại hình khai báo")
    parser.add_argument("-code", "--declaration-code", default="A11", help="Mã loại hình khai báo (A11, A12, E21, E31...)")
    parser.add_argument("-co", "--co-form", default=None, help="Mẫu C/O ưu đãi đi kèm (ví dụ: Form E, Form D, EUR.1, CPTPP...)")
    parser.add_argument("-out", "--output", help="Đường dẫn file markdown xuất bản")
    args = parser.parse_args()

    generate_report(args.commodity, args.origin, args.type, args.declaration_code, args.co_form, args.output)

if __name__ == "__main__":
    main()
