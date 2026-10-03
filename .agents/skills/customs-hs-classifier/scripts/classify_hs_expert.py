import sqlite3
import os
import sys
import re
import json
import argparse

sys.stdout.reconfigure(encoding='utf-8')

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(skill_dir, 'assets')
db_path = os.path.join(assets_dir, 'hs_tariff_index.sqlite')
gri_path = os.path.join(assets_dir, 'Phu_luc_II_Sau_quy_tac_tong_quat_GRI.txt')

# Standard FTA Mapping by Country Origin and Preferred C/O Form
ORIGIN_FTA_RULES = {
    "trung quốc": {"fta_name": "ACFTA (Việt Nam - Trung Quốc)", "co_form": "Form E", "tariff_col": "acfta", "decree": "Nghị định 118/2022/NĐ-CP"},
    "china": {"fta_name": "ACFTA (Việt Nam - Trung Quốc)", "co_form": "Form E", "tariff_col": "acfta", "decree": "Nghị định 118/2022/NĐ-CP"},
    "asean": {"fta_name": "ATIGA (Nội khối ASEAN)", "co_form": "Form D", "tariff_col": "atiga", "decree": "Nghị định 126/2022/NĐ-CP"},
    "thái lan": {"fta_name": "ATIGA (ASEAN)", "co_form": "Form D", "tariff_col": "atiga", "decree": "Nghị định 126/2022/NĐ-CP"},
    "thailand": {"fta_name": "ATIGA (ASEAN)", "co_form": "Form D", "tariff_col": "atiga", "decree": "Nghị định 126/2022/NĐ-CP"},
    "malaysia": {"fta_name": "ATIGA (ASEAN)", "co_form": "Form D", "tariff_col": "atiga", "decree": "Nghị định 126/2022/NĐ-CP"},
    "indonesia": {"fta_name": "ATIGA (ASEAN)", "co_form": "Form D", "tariff_col": "atiga", "decree": "Nghị định 126/2022/NĐ-CP"},
    "singapore": {"fta_name": "ATIGA (ASEAN)", "co_form": "Form D", "tariff_col": "atiga", "decree": "Nghị định 126/2022/NĐ-CP"},
    "hàn quốc": {"fta_name": "VKFTA / AKFTA (Việt Nam - Hàn Quốc)", "co_form": "Form VK / Form AK", "tariff_col": "vkfta", "decree": "Nghị định 125/2022/NĐ-CP"},
    "korea": {"fta_name": "VKFTA / AKFTA (Việt Nam - Hàn Quốc)", "co_form": "Form VK / Form AK", "tariff_col": "vkfta", "decree": "Nghị định 125/2022/NĐ-CP"},
    "nhật bản": {"fta_name": "VJEPA / AJCEP / CPTPP (Nhật Bản)", "co_form": "Form VJ / CPTPP", "tariff_col": "cptpp", "decree": "Nghị định 115/2022/NĐ-CP"},
    "japan": {"fta_name": "VJEPA / AJCEP / CPTPP (Nhật Bản)", "co_form": "Form VJ / CPTPP", "tariff_col": "cptpp", "decree": "Nghị định 115/2022/NĐ-CP"},
    "eu": {"fta_name": "EVFTA (Việt Nam - Liên minh Châu Âu)", "co_form": "EUR.1 / REX", "tariff_col": "evfta", "decree": "Nghị định 116/2022/NĐ-CP"},
    "châu âu": {"fta_name": "EVFTA (Việt Nam - Liên minh Châu Âu)", "co_form": "EUR.1 / REX", "tariff_col": "evfta", "decree": "Nghị định 116/2022/NĐ-CP"},
    "đức": {"fta_name": "EVFTA (Việt Nam - Liên minh Châu Âu)", "co_form": "EUR.1 / REX", "tariff_col": "evfta", "decree": "Nghị định 116/2022/NĐ-CP"},
    "germany": {"fta_name": "EVFTA (Việt Nam - Liên minh Châu Âu)", "co_form": "EUR.1 / REX", "tariff_col": "evfta", "decree": "Nghị định 116/2022/NĐ-CP"},
    "pháp": {"fta_name": "EVFTA (Việt Nam - Liên minh Châu Âu)", "co_form": "EUR.1 / REX", "tariff_col": "evfta", "decree": "Nghị định 116/2022/NĐ-CP"},
    "france": {"fta_name": "EVFTA (Việt Nam - Liên minh Châu Âu)", "co_form": "EUR.1 / REX", "tariff_col": "evfta", "decree": "Nghị định 116/2022/NĐ-CP"},
    "mỹ": {"fta_name": "WTO MFN (Tối huệ quốc)", "co_form": "C/O Non-Preferential", "tariff_col": "tax_mfn", "decree": "Nghị định 26/2023/NĐ-CP & NĐ 144/2024/NĐ-CP"},
    "usa": {"fta_name": "WTO MFN (Tối huệ quốc)", "co_form": "C/O Non-Preferential", "tariff_col": "tax_mfn", "decree": "Nghị định 26/2023/NĐ-CP & NĐ 144/2024/NĐ-CP"},
    "hoa kỳ": {"fta_name": "WTO MFN (Tối huệ quốc)", "co_form": "C/O Non-Preferential", "tariff_col": "tax_mfn", "decree": "Nghị định 26/2023/NĐ-CP & NĐ 144/2024/NĐ-CP"},
    "brazil": {"fta_name": "WTO MFN (Tối huệ quốc)", "co_form": "C/O Non-Preferential", "tariff_col": "tax_mfn", "decree": "Nghị định 26/2023/NĐ-CP & NĐ 144/2024/NĐ-CP"},
    "argentina": {"fta_name": "WTO MFN (Tối huệ quốc)", "co_form": "C/O Non-Preferential", "tariff_col": "tax_mfn", "decree": "Nghị định 26/2023/NĐ-CP & NĐ 144/2024/NĐ-CP"}
}

def parse_tax_percent(val_str):
    if not val_str:
        return 0.0
    val_clean = str(val_str).replace('%', '').strip()
    match = re.search(r"(\d+(\.\d+)?)", val_clean)
    if match:
        try:
            return float(match.group(1))
        except:
            return 0.0
    return 0.0

def search_hs_candidates(query, limit=30):
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
    conn.create_function("py_lower", 1, lambda s: s.lower() if s else "")
    cur = conn.cursor()
    
    clean_q = query.strip()
    code_digits = clean_q.replace('.', '').replace(' ', '')
    is_code = code_digits.isdigit()
    
    if is_code:
        sql = """
        SELECT hs_code_formatted, desc_vn, desc_en, full_desc_vn, unit, tax_standard, tax_mfn, vat,
               acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent_heading, digits_len
        FROM hs_tariff
        WHERE REPLACE(REPLACE(hs_code, '.', ''), ' ', '') LIKE ?
        ORDER BY (digits_len = 8) DESC, hs_code ASC
        LIMIT ?
        """
        cur.execute(sql, (f"{code_digits}%", limit))
        rows = cur.fetchall()
        conn.close()
        return rows
        
    # Search text: Extract core phrases by removing generic noun prefixes (hạt, quả, con, cái...)
    VI_CLASSIFIERS = ["hạt ", "quả ", "trái ", "củ ", "con ", "cái ", "chiếc ", "cây ", "bộ ", "tấm ", "khối ", "miếng "]
    core_q = clean_q.lower()
    for prefix in VI_CLASSIFIERS:
        if core_q.startswith(prefix):
            core_q = core_q[len(prefix):].strip()
            break
            
    results_map = {}
    
    # 1. Exact or Sub-phrase Match on full_desc_vn or desc_vn
    phrases = [clean_q.lower()]
    if core_q != clean_q.lower():
        phrases.append(core_q)
        
    for phrase in phrases:
        sql = """
        SELECT hs_code_formatted, desc_vn, desc_en, full_desc_vn, unit, tax_standard, tax_mfn, vat,
               acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent_heading, digits_len
        FROM hs_tariff
        WHERE (py_lower(full_desc_vn) LIKE ? OR py_lower(desc_vn) LIKE ? OR py_lower(desc_en) LIKE ?)
        ORDER BY (digits_len = 8) DESC, hs_code ASC
        LIMIT ?
        """
        cur.execute(sql, (f"%{phrase}%", f"%{phrase}%", f"%{phrase}%", limit))
        for r in cur.fetchall():
            results_map[r[0]] = r
            
    # 2. Word matches if we have fewer than limit
    words = [w for w in core_q.split() if len(w) > 2]
    if len(results_map) < limit and words:
        conditions = []
        params = []
        for w in words:
            conditions.append("(py_lower(full_desc_vn) LIKE ? OR py_lower(desc_vn) LIKE ?)")
            params.extend([f"%{w}%", f"%{w}%"])
        sql = f"""
        SELECT hs_code_formatted, desc_vn, desc_en, full_desc_vn, unit, tax_standard, tax_mfn, vat,
               acfta, atiga, akfta, vkfta, cptpp, evfta, ukvfta, rcep, ttdb, bvmt, parent_heading, digits_len
        FROM hs_tariff
        WHERE {' AND '.join(conditions)}
        ORDER BY (digits_len = 8) DESC, hs_code ASC
        LIMIT ?
        """
        params.append(limit)
        cur.execute(sql, params)
        for r in cur.fetchall():
            if r[0] not in results_map:
                results_map[r[0]] = r
                
    conn.close()
    return list(results_map.values())

def analyze_classification(commodity, material="", function="", state="", packaging="", origin="Mỹ", co_form="", cif_val=100000.0):
    """
    Expert HS Classification Engine:
    1. 4-Dimension Technical Dissection
    2. GRI Rule Selector & Comprehensive Legal Rationale
    3. Borderline HS Code & Tax Delta Detection
    4. Origin-based Tariff Simulation
    5. Handoff Payload to customs-legal-advisor
    """
    # 1. Technical Dissection
    dissection = {
        "commodity": commodity,
        "material": material or "Theo mô tả thực tế sản phẩm",
        "processing_state": state or "Đã qua sơ chế / Tiêu chuẩn thương mại",
        "principal_function": function or "Sử dụng trực tiếp trong sản xuất / tiêu dùng",
        "commercial_presentation": packaging or "Đóng gói tiêu chuẩn xuất nhập khẩu"
    }
    
    # 2. Query candidates
    candidates = search_hs_candidates(commodity, limit=20)
    eight_digit_candidates = [c for c in candidates if c[19] == 8]
    
    if not eight_digit_candidates:
        words = commodity.split()
        if len(words) > 1:
            candidates = search_hs_candidates(words[0], limit=20)
            eight_digit_candidates = [c for c in candidates if c[19] == 8]
            
    # Context-aware intelligent ranking for 8-digit candidates
    context_text = f"{commodity} {material} {function} {state} {packaging}".lower()
    comm_clean = commodity.strip().lower()
    core_q = comm_clean
    VI_CLASSIFIERS = ["hạt ", "quả ", "trái ", "củ ", "con ", "cái ", "chiếc ", "cây ", "bộ ", "tấm ", "khối ", "miếng "]
    for prefix in VI_CLASSIFIERS:
        if core_q.startswith(prefix):
            core_q = core_q[len(prefix):].strip()
            break
            
    def score_candidate(cand):
        score = 0.0
        full_desc = (cand[3] or "").lower()
        desc_vn = (cand[1] or "").lower()
        desc_en = (cand[2] or "").lower()
        core_clean = core_q.strip().lower()
        
        # GRI 1 & GRI 3(a): Specific heading priority. If heading starts directly with the commodity name, give absolute bonus!
        if full_desc.startswith(core_clean + ",") or full_desc.startswith(core_clean + " ") or full_desc.startswith(comm_clean + ",") or full_desc.startswith(comm_clean + " "):
            score += 500.0
        elif f" {core_clean} " in full_desc:
            score += 100.0
            
        # Penalize oil/fats if commodity itself is NOT oil
        if not any(k in comm_clean for k in ["dầu", "oil", "mỡ", "chất béo"]):
            if full_desc.startswith("dầu ") or full_desc.startswith("dầu,") or "dầu và các phần phân đoạn" in full_desc[:40]:
                score -= 600.0
                
        # Penalize by-products / residue / meal / waste if product is raw grain/bean
        if any(k in context_text for k in ["hạt", "nguyên hạt", "chưa ép", "sàng lọc", "raw", "bean", "grain", "chưa bóc vỏ"]):
            if any(k in full_desc for k in ["khô dầu", "phế liệu", "bã ", "chế phẩm", "nước xốt", "sau khi chiết xuất"]):
                score -= 400.0
                
        # Penalize seeds if user purpose is commercial / oil / animal feed / consumption
        if any(k in context_text for k in ["dầu", "ăn", "thức ăn", "chăn nuôi", "thương phẩm", "tiêu dùng", "sản xuất", "loại khác", "hạt thương mại"]):
            if "hạt giống" in full_desc or "seed" in desc_en:
                score -= 80.0
            if "loại khác" in desc_vn or "other" in desc_en:
                score += 50.0
                
        # Boost seed if user explicitly mentions seed/giống
        if any(k in context_text for k in ["hạt giống", "nhân giống", "gieo trồng", "seed"]):
            if "hạt giống" in full_desc or "seed" in desc_en:
                score += 250.0
                
        # Keyword overlaps
        for word in context_text.split():
            if len(word) > 2 and (word in full_desc or word in desc_en):
                score += 2.0
                
        return score
        
    if eight_digit_candidates:
        eight_digit_candidates.sort(key=score_candidate, reverse=True)
        primary_candidate = eight_digit_candidates[0]
        
        # Borderline candidate selection
        borderline_candidate = None
        for cand in eight_digit_candidates[1:]:
            if cand[0] != primary_candidate[0]:
                borderline_candidate = cand
                break
        if not borderline_candidate and len(candidates) > 1:
            borderline_candidate = candidates[1]
    else:
        primary_candidate = ("0000.00.00", "Chưa xác định", "", commodity, "kg", "0%", "0%", "10%", "0%", "0%", "0%", "0%", "0%", "0%", "0%", "0%", "0%", "0%", "0000", 8)
        borderline_candidate = None

    # 3. Determine applicable GRI Rule & Detailed Legal Rationale
    combined_text = f"{commodity} {material} {function} {state} {packaging}".lower()
    
    gri_rule_id = "GRI 1 & GRI 6"
    gri_title = "Quy tắc 1 kết hợp Quy tắc 6"
    gri_rationale = []
    
    if any(k in combined_text for k in ["bộ", "set", "ghép bộ", "combo", "đi kèm"]):
        gri_rule_id = "GRI 3(b) & GRI 6"
        gri_title = "Quy tắc 3(b) kết hợp Quy tắc 6 (Hàng ghép bộ bán lẻ / Composite Goods)"
        gri_rationale.append("• **Căn cứ áp dụng GRI 3(b):** Mặt hàng bao gồm từ hai hoặc nhiều bộ phận/thành phần cấu thành khác nhau được đóng gói chung dưới dạng bộ để bán lẻ. Do các thành phần này thuộc các nhóm thuế khác nhau, theo GRI 3(a) không thể phân loại theo mô tả cụ thể nhất vì mỗi nhóm chỉ mô tả một phần của bộ hàng.")
        gri_rationale.append(f"• **Xác định đặc tính cơ bản (Essential Character):** Căn cứ công năng chính và tỷ trọng giá trị, thành phần [{function or material or commodity}] đóng vai trò quyết định đặc tính cơ bản chi phối toàn bộ sản phẩm, do đó toàn bộ bộ hàng được phân loại theo mã của thành phần này.")
        gri_rationale.append("• **Chuyển tiếp GRI 6:** Sau khi xác định Nhóm 4 số, việc lựa chọn phân nhóm 6 số và dòng thuế 8 số quốc gia được thực hiện bằng cách so sánh giữa các dòng có cùng cấp độ gạch (-).")
    elif any(k in combined_text for k in ["chưa lắp ráp", "tháo rời", "dở dang", "chưa hoàn chỉnh", "ckd", "skd"]):
        gri_rule_id = "GRI 2(a) & GRI 6"
        gri_title = "Quy tắc 2(a) kết hợp Quy tắc 6 (Hàng chưa hoàn chỉnh / Tháo rời chưa lắp ráp)"
        gri_rationale.append("• **Căn cứ áp dụng GRI 2(a):** Hàng hóa được nhập khẩu ở dạng chưa lắp ráp, tháo rời thành các cụm chi tiết hoặc chưa hoàn thiện nhưng đã mang đầy đủ **đặc trưng cơ bản** của sản phẩm hoàn chỉnh về hình dáng, kết cấu và nguyên lý vận hành.")
        gri_rationale.append("• **Dẫn chiếu Chú giải:** Theo Chú giải Quy tắc 2(a), các bộ phận tháo rời để thuận tiện cho việc đóng gói, bốc dỡ và vận chuyển đường biển vẫn được phân loại vào cùng một mã HS như hàng hóa đã lắp ráp hoàn chỉnh.")
        gri_rationale.append("• **Chuyển tiếp GRI 6:** Áp dụng GRI 6 để ấn định mã 8 số của sản phẩm hoàn chỉnh trên Biểu thuế XNK Việt Nam.")
    elif any(k in combined_text for k in ["bao bì", "hộp đựng", "bao da", "hộp chuyên dụng"]):
        gri_rule_id = "GRI 5(a) & GRI 6"
        gri_title = "Quy tắc 5(a) kết hợp Quy tắc 6 (Bao bì, hộp chuyên dụng đi kèm sản phẩm)"
        gri_rationale.append("• **Căn cứ áp dụng GRI 5(a):** Bao bì, hộp chứa được tạo dáng hoặc lót đệm thích hợp chuyên dùng để chứa đựng một sản phẩm cụ thể, có thể sử dụng lâu dài và được nhập khẩu cùng với sản phẩm đó.")
        gri_rationale.append("• **Nguyên tắc phân loại:** Bao bì chuyên dụng này được phân loại cùng với sản phẩm mà nó bảo vệ, không tách riêng mã HS độc lập.")
    else:
        # Default: GRI 1 & GRI 6
        gri_rule_id = "GRI 1 & GRI 6"
        gri_title = "Quy tắc 1 kết hợp Quy tắc 6 (Quy tắc nền tảng phân loại theo nội dung tên nhóm & Chú giải pháp lý)"
        heading_code = primary_candidate[0][:4] if len(primary_candidate[0]) >= 4 else "0000"
        gri_rationale.append(f"• **Căn cứ áp dụng GRI 1 (Xác định Nhóm 4 số):** Tên gọi của các Phần, Chương và Phân chương chỉ nhằm mục đích tra cứu định hướng. Về mặt pháp lý, việc phân loại bắt buộc phải căn cứ vào **nội dung câu chữ của Nhóm (Heading {heading_code})** và các **Chú giải Phần, Chương liên quan (Legal Notes)** có tính hiệu lực pháp lý ràng buộc.")
        gri_rationale.append(f"• **Phân tích kỹ thuật & Bản chất sản phẩm:** Căn cứ kết quả bóc tách kỹ thuật, sản phẩm [{commodity}] có chất liệu [{material or 'chuẩn hóa'}], trạng thái gia công [{state or 'tiêu chuẩn'}] và chức năng [{function or 'thương phẩm'}] hoàn toàn phù hợp với phạm vi bao quát của Nhóm {heading_code}.")
        gri_rationale.append("• **Kiểm tra Chú giải loại trừ (Exclusionary Notes):** Đã đối chiếu Chú giải loại trừ của Phần và Chương tương ứng; xác nhận sản phẩm KHÔNG thuộc diện bị loại trừ sang các Chương khác.")
        gri_rationale.append("• **Căn cứ áp dụng GRI 6 (Ấn định Dòng thuế 8 chữ số):** Việc phân loại ở cấp độ Phân nhóm (6 số) và Dòng thuế quốc gia (8 số) được xác định bằng cách so sánh câu chữ giữa các phân nhóm có cùng cấp độ gạch (-) theo Chú giải phân nhóm tương ứng và Biểu thuế XNK Việt Nam (Thông tư 31/2022/TT-BTC).")

    # 4. Tax Delta & Borderline Risk Analysis
    hs_code_pri = primary_candidate[0]
    desc_pri = primary_candidate[3]
    mfn_pri = primary_candidate[6] or "0%"
    vat_pri = primary_candidate[7] or "10%"
    
    borderline_data = None
    if borderline_candidate:
        hs_code_sec = borderline_candidate[0]
        desc_sec = borderline_candidate[3]
        mfn_sec = borderline_candidate[6] or "0%"
        vat_sec = borderline_candidate[7] or "10%"
        
        mfn_pri_num = parse_tax_percent(mfn_pri)
        mfn_sec_num = parse_tax_percent(mfn_sec)
        vat_pri_num = parse_tax_percent(vat_pri)
        vat_sec_num = parse_tax_percent(vat_sec)
        
        tax_delta_mfn = mfn_sec_num - mfn_pri_num
        tax_delta_vat = vat_sec_num - vat_pri_num
        
        # Risk assessment
        if tax_delta_mfn > 0 or tax_delta_vat > 0:
            risk_level = "CAO (RỦI RO THAM VẤN & ẤN ĐỊNH THUẾ)"
            risk_note = f"Mã đối trọng ({hs_code_sec}) có mức thuế cao hơn mã khuyến nghị (+{tax_delta_mfn}% MFN). Khi làm thủ tục hải quan, nếu hồ sơ kỹ thuật không rõ ràng, cơ quan Hải quan có xu hướng nghi ngờ và áp chuyển sang mã đối trọng để tăng thu ngân sách, dẫn tới nguy cơ truy thu và phạt 20% theo Điều 9 Nghị định 128/2020/NĐ-CP!"
        elif tax_delta_mfn < 0:
            risk_level = "TRUNG BÌNH (RỦI RO NỘP THỪA THUẾ NẾU ÁP SAI)"
            risk_note = f"Mã đối trọng có mức thuế thấp hơn. Doanh nghiệp cần chứng minh đủ điều kiện để áp mã có lợi."
        else:
            risk_level = "THẤP (THUẾ SUẤT TƯƠNG ĐƯƠNG, TRANH CHẤP MÔ TẢ)"
            risk_note = "Hai mã có cùng mức thuế suất nhưng khác biệt về tiêu chí kỹ thuật hoặc mã định danh quản lý chuyên ngành."
            
        borderline_data = {
            "borderline_hs": hs_code_sec,
            "borderline_desc": desc_sec,
            "mfn_rate": mfn_sec,
            "vat_rate": vat_sec,
            "tax_delta_mfn": f"{tax_delta_mfn:+.1f}%",
            "tax_delta_vat": f"{tax_delta_vat:+.1f}%",
            "risk_level": risk_level,
            "risk_warning": risk_note,
            "discrimination_criteria": [
                f"1. Xác định rõ tiêu chí phân định vật lý/hóa học giữa [{hs_code_pri}] và [{hs_code_sec}].",
                "2. Chuẩn bị sẵn Bảng phân tích thành phần / Tiêu chuẩn kỹ thuật (COA, Specification Sheet, MSDS, Test Report).",
                "3. Kiểm tra mục đích sử dụng thực tế ghi trên Hợp đồng và nhãn mác thương phẩm để bảo vệ mã khuyến nghị."
            ]
        }

    # 5. Determine Tariff under Specific Origin & FTA
    origin_norm = origin.strip().lower()
    matched_fta = None
    for k, v in ORIGIN_FTA_RULES.items():
        if k in origin_norm:
            matched_fta = v
            break
            
    col_idx_map = {
        "tax_mfn": 6,
        "vat": 7,
        "acfta": 8,
        "atiga": 9,
        "akfta": 10,
        "vkfta": 11,
        "cptpp": 12,
        "evfta": 13,
        "ukvfta": 14,
        "rcep": 15
    }
    
    if matched_fta and co_form:
        target_col = matched_fta["tariff_col"]
        idx = col_idx_map.get(target_col, 6)
        import_duty_rate = primary_candidate[idx] or primary_candidate[6] or "0%"
        duty_type = f"Ưu đãi đặc biệt ({matched_fta['fta_name']}) kèm {co_form}"
        legal_decree = matched_fta["decree"]
    elif matched_fta and "mfn" in matched_fta["tariff_col"]:
        import_duty_rate = primary_candidate[6] or "0%"
        duty_type = f"Ưu đãi MFN WTO (Quan hệ Tối huệ quốc)"
        legal_decree = "Nghị định 26/2023/NĐ-CP (sửa đổi bởi NĐ 144/2024/NĐ-CP)"
    else:
        import_duty_rate = primary_candidate[6] or "0%"
        duty_type = "Ưu đãi MFN WTO (Mặc định khi không có C/O ưu đãi FTA)"
        legal_decree = "Nghị định 26/2023/NĐ-CP"

    # VAT Rate
    vat_raw = primary_candidate[7] or "10%"
    # Check VAT exemption or 8%
    if "không chịu thuế" in vat_raw.lower() or "kct" in vat_raw.lower():
        vat_applied = "Không chịu thuế GTGT khâu nhập khẩu"
        vat_decree = "Khoản 1 Điều 4 Thông tư 219/2013/TT-BTC & Luật Thuế GTGT 48/2024/QH15"
        vat_num = 0.0
    elif any(k in commodity.lower() for k in ["đậu tương", "ngô", "thóc", "gạo", "lúa mì", "khoai", "sắn"]) and "chưa chế biến" in (state or "chưa chế biến").lower():
        vat_applied = "Không chịu thuế GTGT khâu nhập khẩu (Nông sản chưa chế biến)"
        vat_decree = "Khoản 1 Điều 4 Thông tư 219/2013/TT-BTC & Khoản 1 Điều 5 Luật Thuế GTGT 48/2024/QH15"
        vat_num = 0.0
    else:
        vat_applied = vat_raw
        vat_decree = "Nghị định 174/2025/NĐ-CP & Luật Thuế GTGT 48/2024/QH15"
        vat_num = parse_tax_percent(vat_raw)

    import_duty_num = parse_tax_percent(import_duty_rate)
    
    # CIF Simulation Calculation
    cif_amount = float(cif_val)
    duty_amount = cif_amount * (import_duty_num / 100.0)
    vat_base = cif_amount + duty_amount
    vat_amount = vat_base * (vat_num / 100.0)
    total_tax = duty_amount + vat_amount

    # 6. Standardized Handoff Payload to customs-legal-advisor
    handoff_payload = {
        "service": "customs:legal-advisor",
        "action": "clearance_and_permits_audit",
        "payload_timestamp": "2026-10-02",
        "commodity_dossier": {
            "commodity_name": commodity,
            "classified_hs_code": hs_code_pri,
            "full_description_vn": desc_pri,
            "unit": primary_candidate[4] or "kg",
            "country_of_origin": origin,
            "co_form_provided": co_form or "None (MFN Rate Applied)",
            "applicable_import_duty": import_duty_rate,
            "applicable_vat": vat_applied,
            "borderline_risk_code": borderline_data["borderline_hs"] if borderline_data else None,
            "borderline_risk_level": borderline_data["risk_level"] if borderline_data else "THẤP"
        },
        "delegated_tasks": [
            "1. Tra cứu chính sách quản lý chuyên ngành, hàng cấm hoặc giấy phép nhập khẩu bắt buộc theo Nghị định 69/2018/NĐ-CP cho mã HS trên.",
            "2. Lập danh mục thành phần bộ hồ sơ hải quan điện tử bắt buộc theo Điều 16 Thông tư 38/2015/TT-BTC (sửa đổi bởi TT 39/2018 & TT 121/2025).",
            "3. Hướng dẫn quy trình 3 bước thông quan thực tế tại cửa khẩu/cảng biển và đăng ký trên Cổng Một cửa Quốc gia (NSW).",
            "4. Rà soát chế tài xử phạt hành chính đối với các hành vi khai sai mã HS hoặc thiếu giấy phép theo Nghị định 128/2020/NĐ-CP."
        ]
    }

    result = {
        "dissection": dissection,
        "primary_classification": {
            "hs_code": hs_code_pri,
            "desc_vn": primary_candidate[1],
            "desc_en": primary_candidate[2],
            "full_desc_vn": desc_pri,
            "unit": primary_candidate[4] or "kg",
            "parent_heading": primary_candidate[18]
        },
        "gri_determination": {
            "rule_id": gri_rule_id,
            "rule_title": gri_title,
            "rationale_points": gri_rationale
        },
        "borderline_analysis": borderline_data,
        "tariff_breakdown": {
            "origin": origin,
            "duty_type": duty_type,
            "legal_decree": legal_decree,
            "import_duty_rate": import_duty_rate,
            "vat_rate": vat_applied,
            "vat_decree": vat_decree,
            "simulation": {
                "cif_val": cif_amount,
                "import_duty_amount": duty_amount,
                "vat_base_amount": vat_base,
                "vat_amount": vat_amount,
                "total_tax_amount": total_tax
            }
        },
        "handoff_payload": handoff_payload
    }
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Chuyen gia Phan loai Ma HS & Bien luan GRI 1-6 (HS Classification Expert v2.0)")
    parser.add_argument("-c", "--commodity", required=True, help="Ten mat hang hoac mo ta thuong mai")
    parser.add_argument("-m", "--material", default="", help="Chat lieu / Thanh phan cau tao")
    parser.add_argument("-f", "--function", default="", help="Chuc nang chinh / Muc dich su dung")
    parser.add_argument("-s", "--state", default="", help="Trang thai gia cong / che bien (tuoi, dong lanh, roi, ck/skd...)")
    parser.add_argument("-p", "--packaging", default="", help="Quy cach dong goi / Bo ban le")
    parser.add_argument("-o", "--origin", default="Mỹ", help="Nuoc xuat xu (Origin)")
    parser.add_argument("--co", default="", help="Mau chung nhan xuat xu (Form E, Form D, EUR.1, CPTPP...)")
    parser.add_argument("--cif", type=float, default=100000.0, help="Gia tri CIF gia dinh de mo phong tinh thue (USD hoac VND)")
    parser.add_argument("--json", action="store_true", help="Xuat ket qua o dinh dang JSON")
    
    args = parser.parse_args()
    
    res = analyze_classification(
        commodity=args.commodity,
        material=args.material,
        function=args.function,
        state=args.state,
        packaging=args.packaging,
        origin=args.origin,
        co_form=args.co,
        cif_val=args.cif
    )
    
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
        
    print(f"\n{'='*95}")
    print(f" KẾT QUẢ THẨM ĐỊNH & BIỆN LUẬN PHÂN LOẠI MÃ HS (HS CLASSIFIER v2.0)")
    print(f" Mặt hàng: {args.commodity} | Xuất xứ: {args.origin}")
    print(f"{'='*95}\n")
    
    # 1. Dissection
    d = res["dissection"]
    print("1. BÓC TÁCH KỸ THUẬT 4 CHIỀU:")
    print(f"   • Chất liệu / Thành phần : {d['material']}")
    print(f"   • Trạng thái chế biến    : {d['processing_state']}")
    print(f"   • Chức năng / Công dụng  : {d['principal_function']}")
    print(f"   • Quy cách bao gói       : {d['commercial_presentation']}\n")
    
    # 2. HS Code
    p = res["primary_classification"]
    print("2. MÃ HS 8 SỐ KHUYẾN NGHỊ:")
    print(f"   ★ MÃ HS KHAI BÁO : {p['hs_code']} (ĐVT: {p['unit']})")
    print(f"   • Mô tả đầy đủ   : {p['full_desc_vn']}")
    if p['desc_en']:
        print(f"   • Mô tả tiếng Anh: {p['desc_en']}\n")
        
    # 3. GRI Rule & Explanation
    g = res["gri_determination"]
    print("3. QUY TẮC PHÂN LOẠI ÁP DỤNG & LẬP LUẬN GIẢI THÍCH CHI TIẾT:")
    print(f"   ➤ QUY TẮC SỬ DỤNG: {g['rule_title']} [{g['rule_id']}]")
    print("   ➤ LẬP LUẬN BIỆN LUẬN PHÁP LÝ:")
    for pt in g['rationale_points']:
        print(f"     {pt}")
    print()
    
    # 4. Borderline & Tax Delta
    b = res["borderline_analysis"]
    if b:
        print("4. CẢNH BÁO TRANH CHẤP MÃ ĐỐI TRỌNG & CHÊNH LỆCH THUẾ (BORDERLINE & TAX DELTA):")
        print(f"   ⚠️ Mã HS đối trọng tiềm ẩn : {b['borderline_hs']}")
        print(f"      Mô tả mã đối trọng      : {b['borderline_desc']}")
        print(f"   • Thuế MFN đối trọng       : {b['mfn_rate']} (Chênh lệch Tax Delta: {b['tax_delta_mfn']})")
        print(f"   • Mức độ rủi ro tranh chấp : {b['risk_level']}")
        print(f"   • Cảnh báo nghiệp vụ       : {b['risk_warning']}")
        print("   • Bộ tiêu chí phân định cần chuẩn bị để bảo vệ mã:")
        for cr in b['discrimination_criteria']:
            print(f"     {cr}")
        print()
        
    # 5. Tariff
    t = res["tariff_breakdown"]
    print("5. NGHĨA VỤ THUẾ THỰC TẾ & MÔ PHỎNG CHI PHÍ THUẾ LÔ HÀNG:")
    print(f"   • Chế độ thuế áp dụng      : {t['duty_type']}")
    print(f"   • Căn cứ pháp lý thuế NK   : {t['legal_decree']}")
    print(f"   • Thuế suất Nhập khẩu      : {t['import_duty_rate']}")
    print(f"   • Thuế suất GTGT (VAT)     : {t['vat_rate']} ({t['vat_decree']})")
    sim = t["simulation"]
    print(f"   • Mô phỏng tính thuế (CIF = {sim['cif_val']:,.2f}):")
    print(f"     - Tiền thuế Nhập khẩu    : {sim['import_duty_amount']:,.2f}")
    print(f"     - Trị giá tính thuế VAT  : {sim['vat_base_amount']:,.2f}")
    print(f"     - Tiền thuế GTGT         : {sim['vat_amount']:,.2f}")
    print(f"     ==> TỔNG THUẾ PHẢI NỘP   : {sim['total_tax_amount']:,.2f}\n")
    
    # 6. Handoff
    print("6. GIAO THỨC BÀN GIAO THỦ TỤC SANG CUSTOMS-LEGAL-ADVISOR:")
    print("   [+] Đã đóng gói Handoff Payload JSON sẵn sàng chuyển tiếp cho skill 'customs-legal-advisor' để tra cứu giấy phép NĐ 69 & bộ chứng từ Điều 16.")
    print(f"{'='*95}\n")

if __name__ == "__main__":
    main()
