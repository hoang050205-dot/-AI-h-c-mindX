"""
=============================================================================
HỆ THỐNG CHẤM ĐIỂM & PHÂN LOẠI KHÁCH HÀNG BẤT ĐỘNG SẢN (AI LEAD SCORING v2.1)
Phát triển bởi: Phạm Minh Hoàng (AI4A - Antigravity)
Dựa trên:
  1. Skill: real-estate:lead-scoring (SKILL.md & lead_scoring_skill.md)
  2. Quy chuẩn tiêu chí: knowledge-base/tieu_chi_cham_diem.txt
  3. Dữ liệu: khach_hang_bds_500.xlsx / Google Sheets Private qua Service Account
=============================================================================
"""

import os
import re
import io
import time
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import altair as alt
import streamlit as st

# Thư viện xác thực Google Cloud Service Account & Google Sheets
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT & GIAO DIỆN
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Lead Scoring BĐS Pro | Quản Trị Khách Hàng Tiềm Năng",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách Modern Enterprise UI & Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
        padding: 22px 28px;
        border-radius: 12px;
        color: #F8FAFC;
        margin-bottom: 20px;
        border-left: 6px solid #2563EB;
        box-shadow: 0 4px 10px -2px rgba(0, 0, 0, 0.12);
    }
    
    .kpi-card {
        background: #FFFFFF;
        padding: 16px 18px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.08);
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        margin-top: 4px;
        color: #0F172A;
    }
    .kpi-sub {
        font-size: 0.76rem;
        color: #94A3B8;
        margin-top: 3px;
    }
    
    .handoff-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 22px 26px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-top: 10px;
    }
    
    .tag-hot {
        background-color: #FEE2E2;
        color: #DC2626;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #FCA5A5;
        display: inline-block;
    }
    .tag-warm {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #FCD34D;
        display: inline-block;
    }
    .tag-cold {
        background-color: #F1F5F9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #CBD5E1;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 2. LOGIC AI LEAD SCORING ENGINE (THEO TIEU_CHI_CHAM_DIEM.TXT & SKILL)
# ---------------------------------------------------------------------------
def ai_score_lead(description: str, name: str = "", phone: str = "", hot_threshold: int = 80, warm_threshold: int = 50) -> dict:
    """
    AI Lead Scoring Engine cho Bất Động Sản:
    Quét mô tả khách hàng theo 5 tiêu chí:
      1. Ngân sách & Năng lực tài chính (Budget: 0-30đ)
      2. Mức độ quan tâm & Độ khớp nhu cầu (Need & Product Fit: 0-25đ)
      3. Thời gian mua & Tính cấp thiết (Timeline & Urgency: 0-20đ)
      4. Nguồn khách & Độ tin cậy (Lead Source: 0-15đ)
      5. Mức độ tương tác & Thiện chí (Engagement: 0-10đ)
    
    Tích hợp chính xác 2 nhóm tiêu chí đặc thù từ tieu_chi_cham_diem.txt:
      - TIÊU CHÍ CỘNG 50 ĐIỂM (VIP / SIÊU TIỀM NĂNG):
        + Ngân sách lớn: cụ thể từ 20 tỷ trở lên hoặc "tài chính mạnh", "không thành vấn đề"
        + Loại hình cao cấp: "Biệt thự đơn lập", "Penthouse", "Shophouse mặt đường lớn", "Quỹ đất công nghiệp", "Sàn văn phòng diện tích lớn"
        + Vị trí đắc địa: "Quận 1", "Ven sông", "Vinhomes Ocean Park", "Phú Mỹ Hưng"
        + Đối tượng: "Chủ doanh nghiệp", "Nhà đầu tư chuyên nghiệp", "Mua sỉ", "Mua số lượng lớn"
        + Cấp thiết & Minh bạch: "Pháp lý chuẩn 100%", "Sổ hồng riêng", "Muốn gặp trực tiếp chủ đầu tư để đàm phán"
      - TIÊU CHÍ TRỪ 50 ĐIỂM (RÁC / KHÔNG TIỀM NĂNG):
        + Yêu cầu phi thực tế: giá thấp vô lý (nhà Q1 giá 1-2 tỷ, nhà trung tâm vài trăm triệu)
        + Không có nhu cầu: "Nhầm số", "Không có nhu cầu", "Dữ liệu cũ", "Nhầm ngành"
        + Khách hàng không thiện chí: "Hỏi giá cho vui", "Chưa có ý định mua", "Thái độ không hợp tác"
        + Spam/Quảng cáo: "Bảo hiểm", "Vay vốn", "Mời chào dịch vụ"
        + Thông tin liên lạc lỗi: "Thuê bao", "Gọi nhiều lần không bắt máy", "Không phản hồi Zalo"
    """
    if not isinstance(description, str) or not description.strip():
        return {
            "diem_so": 0,
            "trang_thai": "COLD",
            "ly_do_ai": "Mô tả trống hoặc không có thông tin nhu cầu",
            "goi_y_sales": "Chưa có thông tin để tư vấn, cần thu thập thêm",
            "sla": "Chăm sóc tự động",
            "tags": ["Trống"]
        }

    text = description.lower()
    detected_tags = []
    
    # -----------------------------------------------------------------------
    # A. RÀ SOÁT TIÊU CHÍ TRỪ 50 ĐIỂM (KHÁCH HÀNG RÁC / KHÔNG TIỀM NĂNG)
    # -----------------------------------------------------------------------
    junk_reasons = []
    
    # 1. Không có nhu cầu / dữ liệu cũ / nhầm số
    if any(k in text for k in ["nhầm số", "không có nhu cầu", "dữ liệu cũ", "nhầm ngành", "lộn số", "không nhu cầu"]):
        junk_reasons.append("Nhầm số / không có nhu cầu BĐS / data cũ trộn ngành")
        detected_tags.append("Nhầm số/Không nhu cầu")
        
    # 2. Khách không thiện chí / hỏi cho vui
    if any(k in text for k in ["hỏi giá cho vui", "chưa có ý định mua", "thái độ không hợp tác", "không hợp tác", "cho vui"]):
        junk_reasons.append("Hỏi giá cho vui / chưa có ý định mua / thái độ không hợp tác")
        detected_tags.append("Hỏi cho vui")
        
    # 3. Spam / quảng cáo dịch vụ khác
    if any(k in text for k in ["spam", "bảo hiểm", "vay vốn", "mời chào dịch vụ", "quảng cáo ngược"]):
        junk_reasons.append("Spam dịch vụ bảo hiểm / vay vốn / mời chào ngoài ngành")
        detected_tags.append("Spam dịch vụ")
        
    # 4. Lỗi liên lạc nghiêm trọng
    if any(k in text for k in ["thuê bao", "không bắt máy", "không phản hồi zalo", "không nghe máy", "chặn số"]):
        junk_reasons.append("Số thuê bao / gọi nhiều lần không bắt máy / không rep Zalo")
        detected_tags.append("Lỗi liên lạc")
        
    # 5. Yêu cầu phi thực tế so với thị trường
    irrational_patterns = [
        r"nhà\s+q1\s+giá\s+1",
        r"nhà\s+quận\s+1\s+giá\s+1",
        r"quận\s+1\s+giá\s+1\s*[-–]?\s*2\s*tỷ",
        r"thuê.*nguyên\s+căn.*2\s*triệu.*trung\s+tâm",
        r"thuê.*2\s*triệu.*trung\s+tâm",
        r"vài\s+trăm\s+triệu.*hồ\s+bơi",
        r"giá\s+thấp\s+vô\s+lý"
    ]
    for pat in irrational_patterns:
        if re.search(pat, text):
            junk_reasons.append("Yêu cầu giá phi thực tế (VD: Nhà Q1 giá 1-2 tỷ / Thuê TT 2 triệu)")
            detected_tags.append("Giá phi thực tế")
            break

    # -----------------------------------------------------------------------
    # B. RÀ SOÁT TIÊU CHÍ CỘNG 50 ĐIỂM (KHÁCH HÀNG VIP / SIÊU TIỀM NĂNG)
    # -----------------------------------------------------------------------
    vip_reasons = []
    
    # 1. Ngân sách lớn
    vip_budget_kw = ["trên 20 tỷ", "trên 30 tỷ", "20 tỷ", "30 tỷ", "50 tỷ", "tài chính mạnh", "tài chính cực mạnh", "không thành vấn đề", "thanh toán thẳng", "tiền mặt sẵn"]
    if any(k in text for k in vip_budget_kw):
        vip_reasons.append("Ngân sách lớn ≥20-30 tỷ / tài chính mạnh / thanh toán thẳng")
        detected_tags.append("Tài chính ≥20-30 tỷ")
        
    # 2. Loại hình cao cấp
    vip_products = ["biệt thự đơn lập", "penthouse", "shophouse mặt đường lớn", "quỹ đất công nghiệp", "sàn văn phòng", "diện tích lớn", "2000m2", "hồ bơi riêng", "thang máy riêng"]
    if any(k in text for k in vip_products):
        vip_reasons.append("Loại hình cao cấp (Biệt thự đơn lập / Penthouse / Shophouse / Đất CN >2000m2)")
        detected_tags.append("Biệt thự/Penthouse/Đất CN")
        
    # 3. Vị trí đắc địa
    vip_locations = ["ven sông", "phân khu cao cấp nhất", "quận 1", "vinhomes ocean park", "phú mỹ hưng"]
    if any(k in text for k in vip_locations):
        vip_reasons.append("Vị trí đắc địa (Ven sông / Quận 1 / Ocean Park / Phú Mỹ Hưng)")
        detected_tags.append("Vị trí đắc địa")
        
    # 4. Đối tượng khách hàng VIP
    vip_clients = ["chủ doanh nghiệp", "nhà đầu tư chuyên nghiệp", "mua sỉ", "mua số lượng lớn", "gom sỉ", "5-10 căn"]
    if any(k in text for k in vip_clients):
        vip_reasons.append("Đối tượng VIP (Chủ doanh nghiệp / Nhà đầu tư gom sỉ)")
        detected_tags.append("Chủ DN/Mua sỉ")
        
    # 5. Tính cấp thiết & Minh bạch cao
    vip_urgency = ["pháp lý chuẩn 100%", "sổ hồng riêng", "gặp trực tiếp chủ đầu tư", "giám đốc dự án", "đã từng mua nhiều dự án"]
    if any(k in text for k in vip_urgency):
        vip_reasons.append("Pháp lý chuẩn 100% / Muốn gặp CĐT / Khách quen tập đoàn")
        detected_tags.append("Pháp lý chuẩn/Gặp CĐT")

    # -----------------------------------------------------------------------
    # C. ĐÁNH GIÁ 5 TIÊU CHÍ CƠ SỞ (THANG 100 ĐIỂM)
    # -----------------------------------------------------------------------
    # 1. Ngân sách (0 - 30 điểm)
    p_budget = 10
    if vip_reasons:
        p_budget = 30
    elif any(k in text for k in ["8-10 tỷ", "8 đến 10 tỷ", "10 tỷ", "12 tỷ", "15 tỷ"]):
        p_budget = 25
        detected_tags.append("8-15 tỷ")
    elif any(k in text for k in ["4-5 tỷ", "4 đến 5 tỷ", "5 tỷ", "6 tỷ", "7 tỷ"]):
        p_budget = 18
        detected_tags.append("4-7 tỷ")
    elif any(k in text for k in ["2-3 tỷ", "2 đến 3 tỷ", "3 tỷ", "dưới 50 triệu/tháng", "50 triệu"]):
        p_budget = 14
        detected_tags.append("2-3 tỷ")
    elif junk_reasons:
        p_budget = 0
        
    # 2. Mức độ quan tâm / Khớp nhu cầu (0 - 25 điểm)
    p_interest = 12
    if any(k in text for k in ["penthouse", "biệt thự", "shophouse", "sàn văn phòng", "đất công nghiệp"]):
        p_interest = 25
    elif any(k in text for k in ["căn hộ 2pn", "nhà phố liền kề", "mặt bằng kinh doanh spa", "đất nền vùng ven"]):
        p_interest = 20
        detected_tags.append("Căn hộ/Nhà phố/Mặt bằng")
    elif any(k in text for k in ["cân nhắc giữa 2 dự án", "chính sách chiết khấu", "hỗ trợ vay ngân hàng"]):
        p_interest = 18
        detected_tags.append("Vay ngân hàng/Cân nhắc")
        
    # 3. Thời gian mua & Tính cấp thiết (0 - 20 điểm)
    p_timeline = 10
    if any(k in text for k in ["cuối tuần này", "trong tuần", "ký hợp đồng dài hạn", "ngay", "muốn đi xem nhà mẫu", "tháng này"]):
        p_timeline = 20
        detected_tags.append("Xem nhà cuối tuần/Ký HĐ ngay")
    elif any(k in text for k in ["đầu tư dài hạn", "đang cân nhắc"]):
        p_timeline = 14
        detected_tags.append("Đầu tư dài hạn")
    elif any(k in text for k in ["chưa có ý định", "cho vui"]):
        p_timeline = 0
        
    # 4. Nguồn khách & Uy tín (0 - 15 điểm)
    p_source = 10
    if any(k in text for k in ["đã từng mua nhiều dự án", "khách quen", "chủ doanh nghiệp lớn"]):
        p_source = 15
        detected_tags.append("Khách quen tập đoàn")
    elif any(k in text for k in ["đăng ký xem nhà mẫu", "spa tại quận 1", "tìm thuê"]):
        p_source = 12
    elif any(k in text for k in ["dữ liệu cũ", "nhầm số"]):
        p_source = 0
        
    # 5. Mức độ tương tác (0 - 10 điểm)
    p_engagement = 8
    if any(k in text for k in ["muốn gặp trực tiếp", "muốn đi xem nhà mẫu", "yêu cầu"]):
        p_engagement = 10
    elif any(k in text for k in ["thuê bao", "không bắt máy", "không phản hồi"]):
        p_engagement = 0

    base_score = p_budget + p_interest + p_timeline + p_source + p_engagement
    
    # -----------------------------------------------------------------------
    # D. TỔNG HỢP ĐIỂM & GỢI Ý TRẠNG THÁI (HOT / WARM / COLD)
    # -----------------------------------------------------------------------
    total_score = base_score
    
    if junk_reasons:
        # Tiêu chí trừ 50 điểm
        total_score -= 50
        total_score = max(0, min(total_score, 40))
        trang_thai = "COLD"
        ly_do = f"⛔ Trừ 50đ (Dấu hiệu rác/loại trừ): {'; '.join(junk_reasons)}"
        goi_y = "Loại bỏ khỏi danh sách gọi hàng ngày; đưa vào kịch bản nuôi dưỡng tự động hoặc Blacklist."
        sla = "Chăm sóc tự động / Không phân Sales"
        
    elif vip_reasons:
        # Tiêu chí cộng 50 điểm
        total_score += 50
        total_score = min(100, max(85, total_score))
        trang_thai = "HOT"
        ly_do = f"🌟 Cộng 50đ (Khách VIP/Siêu tiềm năng): {'; '.join(vip_reasons)}"
        goi_y = "Bàn giao ngay cho Trưởng phòng/Top Sales gọi trong vòng 15 phút. Chuẩn bị hồ sơ pháp lý & layout VIP."
        sla = "≤ 15 Phút (Golden Speed to Lead)"
        
    else:
        # Điểm cơ sở
        if total_score >= hot_threshold or any(k in text for k in ["xem nhà mẫu vào cuối tuần này", "ký hợp đồng dài hạn"]):
            total_score = min(100, max(hot_threshold, total_score))
            trang_thai = "HOT"
            ly_do = "Nhu cầu rõ ràng, thời gian cấp thiết (hẹn xem nhà cuối tuần/ký HĐ ngay)."
            goi_y = "Gọi điện xác nhận lịch hẹn xem nhà mẫu / sa bàn trong ngày hôm nay."
            sla = "≤ 15-30 Phút"
        elif total_score >= warm_threshold:
            trang_thai = "WARM"
            ly_do = "Có nhu cầu thực tế tầm trung, đang cân nhắc tài chính/chính sách chiết khấu."
            goi_y = "Gửi trọn bộ bảng giá, bảng tính dòng tiền ngân hàng qua Zalo và hẹn lịch tư vấn sâu."
            sla = "≤ 2 - 4 Giờ"
        else:
            trang_thai = "COLD"
            ly_do = "Nhu cầu chưa cụ thể hoặc thời gian mua dài hạn."
            goi_y = "Gửi bản tin thị trường định kỳ, chưa cần ưu tiên gọi trực tiếp."
            sla = "Chăm sóc tự động"

    return {
        "diem_so": int(total_score),
        "trang_thai": trang_thai,
        "ly_do_ai": ly_do,
        "goi_y_sales": goi_y,
        "sla": sla,
        "tags": detected_tags if detected_tags else ["Khác"]
    }


# ---------------------------------------------------------------------------
# 3. XÁC THỰC GOOGLE CLOUD SERVICE ACCOUNT & ĐỌC PRIVATE SHEET
# ---------------------------------------------------------------------------
def get_gspread_client():
    """
    Khởi tạo gspread client sử dụng Google Cloud Service Account
    Ưu tiên đọc từ st.secrets["gcp_service_account"] (.streamlit/secrets.toml)
    Fallback: file json service_account.json nếu có ở local
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 1. Thử nạp từ st.secrets (Streamlit Secrets Management)
    try:
        if "gcp_service_account" in st.secrets:
            sa_info = dict(st.secrets["gcp_service_account"])
            # Chuẩn hóa nếu private_key bị escape thừa
            if "private_key" in sa_info:
                sa_info["private_key"] = sa_info["private_key"].replace("\\n", "\n")
            creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
            return gspread.authorize(creds)
    except Exception:
        pass
        
    # 2. Thử nạp từ các file json cục bộ
    for path in ["service_account.json", ".streamlit/service_account.json", "credential.json", "credentials.json"]:
        if os.path.exists(path):
            try:
                creds = Credentials.from_service_account_file(path, scopes=scopes)
                return gspread.authorize(creds)
            except Exception:
                continue
                
    return None


def load_private_sheet(sheet_id_or_url: str, worksheet_identifier=0):
    """
    Đọc Google Sheet private thông qua gspread + Google Cloud Service Account
    Không cần công khai link (public sharing), chỉ cần Share Sheet cho email của Service Account!
    """
    client = get_gspread_client()
    if client is None:
        raise ValueError(
            "Chưa tìm thấy cấu hình Google Cloud Service Account!\n"
            "Vui lòng tạo file `.streamlit/secrets.toml` chứa khóa `[gcp_service_account]` (xem mẫu tại `.streamlit/secrets.toml.example`)."
        )
        
    sheet_id = sheet_id_or_url.strip()
    if "spreadsheets/d/" in sheet_id:
        match = re.search(r"spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_id)
        if match:
            sheet_id = match.group(1)
            
    try:
        spreadsheet = client.open_by_key(sheet_id)
    except Exception as e:
        raise RuntimeError(
            f"Không thể mở Google Sheet với ID '{sheet_id}'. Chi tiết: {e}.\n"
            "Hãy kiểm tra lại xem bạn đã bấm 'Chia sẻ' (Share) bảng tính này cho email của Service Account chưa!"
        )
        
    if isinstance(worksheet_identifier, int):
        worksheet = spreadsheet.get_worksheet(worksheet_identifier)
    else:
        worksheet = spreadsheet.worksheet(worksheet_identifier)
        
    records = worksheet.get_all_records()
    if not records:
        values = worksheet.get_all_values()
        if values and len(values) > 1:
            header = [str(c).strip().lower() for c in values[0]]
            df = pd.DataFrame(values[1:], columns=header)
        else:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame(records)
        
    return df


# ---------------------------------------------------------------------------
# 4. HÀM TẢI DỮ LIỆU ĐA NGUỒN (LOCAL / PRIVATE SHEET / PUBLIC LINK / UPLOAD)
# ---------------------------------------------------------------------------
LOCAL_FILE = "khach_hang_bds_500.xlsx"
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/149rRXA8rSQKsAaMW0Kyt3q6Mzv9_KltAXgIXVTnuQoM/export?format=csv&gid=1542775777"
DEFAULT_PRIVATE_SHEET_ID = "149rRXA8rSQKsAaMW0Kyt3q6Mzv9_KltAXgIXVTnuQoM"

def load_data(source_type="local", custom_url="", uploaded_file=None, sheet_id=""):
    """Nạp dữ liệu từ file local, Google Sheets private (SA), Google Sheets public hoặc upload"""
    df = None
    try:
        if source_type == "local" and os.path.exists(LOCAL_FILE):
            df = pd.read_excel(LOCAL_FILE)
        elif source_type == "private_sheet" and sheet_id:
            df = load_private_sheet(sheet_id)
        elif source_type == "sheet" and custom_url:
            if "export?format=csv" not in custom_url and "/edit" in custom_url:
                custom_url = re.sub(r"/edit.*", "/export?format=csv&gid=1542775777", custom_url)
            df = pd.read_csv(custom_url)
        elif source_type == "upload" and uploaded_file is not None:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        elif os.path.exists(LOCAL_FILE):
            df = pd.read_excel(LOCAL_FILE)
            
        if df is not None:
            df.columns = [c.strip().lower() for c in df.columns]
            if "id" not in df.columns:
                df.insert(0, "id", range(1, len(df) + 1))
            if "sdt" in df.columns:
                df["sdt"] = df["sdt"].astype(str).str.replace(r"\.0$", "", regex=True)
                df["sdt"] = df["sdt"].apply(lambda x: "0" + x if len(x) == 9 and not x.startswith("0") else x)
            return df
    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu ({source_type}): {e}")
        
    return pd.DataFrame([
        {"id": 1, "ten_khach": "Bùi Phương Tâm", "sdt": "0790240040", "nhu_cau_mo_ta": "Khách hàng VIP, quan tâm biệt thự đơn lập phân khu cao cấp nhất. Ngân sách trên 30 tỷ, thanh toán thẳng. Yêu cầu vị trí ven sông, hướng Đông Nam."},
        {"id": 2, "ten_khach": "Hồ Hồng Linh", "sdt": "0915805255", "nhu_cau_mo_ta": "Khách hàng nhầm số, không có nhu cầu về bất động sản. Có vẻ là dữ liệu cũ."},
        {"id": 3, "ten_khach": "Lý Đức Cường", "sdt": "0953430096", "nhu_cau_mo_ta": "Quan tâm căn hộ 2PN tại Quận 7 cho gia đình trẻ. Tài chính khoảng 4-5 tỷ, cần hỗ trợ vay ngân hàng 70%. Muốn đi xem nhà mẫu vào cuối tuần này."},
        {"id": 4, "ten_khach": "Lê Anh Lan", "sdt": "0914842426", "nhu_cau_mo_ta": "Khách hàng tìm mua Penthouse diện tích lớn, yêu cầu có hồ bơi riêng và sân vườn trên cao. Tài chính không thành vấn đề."},
        {"id": 5, "ten_khach": "Ngô Anh Mai", "sdt": "0784760799", "nhu_cau_mo_ta": "Tìm nhà phố liền kề khu vực nội thành, ưu tiên gần trường học và bệnh viện. Ngân sách 8-10 tỷ. Đang cân nhắc giữa 2 dự án, cần tư vấn thêm về chính sách chiết khấu."}
    ])


# ---------------------------------------------------------------------------
# 5. HÀM TẠO FILE EXCEL LEADS_SCORED.XLSX ĐỊNH DẠNG DOANH NGHIỆP
# ---------------------------------------------------------------------------
def generate_excel_bytes(approved_df: pd.DataFrame) -> bytes:
    """Tạo workbook Excel định dạng sang trọng, chuẩn doanh nghiệp từ danh sách khách đã duyệt"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads Đã Duyệt"
    ws.views.sheetView[0].showGridLines = True

    # Palette màu doanh nghiệp
    navy_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    font_body = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)
    
    fill_hot = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    font_hot = Font(name="Calibri", size=10, bold=True, color="DC2626")
    
    fill_warm = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    font_warm = Font(name="Calibri", size=10, bold=True, color="D97706")
    
    fill_cold = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    font_cold = Font(name="Calibri", size=10, color="475569")
    
    thin_side = Side(border_style="thin", color="D1D5DB")
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # Tiêu đề bảng cột
    columns = [
        ("Mã KH", "id", 10, "center"),
        ("Tên Khách Hàng", "ten_khach", 22, "left"),
        ("Số Điện Thoại", "sdt", 16, "center"),
        ("Điểm Số", "diem_so", 12, "center"),
        ("Trạng Thái", "trang_thai", 15, "center"),
        ("Đã Duyệt", "da_duyet", 12, "center"),
        ("Lý Do AI Chấm Điểm", "ly_do_ai", 45, "left"),
        ("Mô Tả Nhu Cầu Gốc", "nhu_cau_mo_ta", 50, "left"),
        ("Ghi Chú Sales", "ghi_chu_sales", 25, "left")
    ]

    for col_idx, (header_text, _, width, _) in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_idx, value=header_text)
        cell.font = font_header
        cell.fill = navy_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.row_dimensions[1].height = 28

    for row_idx, (_, row_data) in enumerate(approved_df.iterrows(), 2):
        tier = str(row_data.get("trang_thai", "")).upper()
        for col_idx, (_, key, _, align) in enumerate(columns, 1):
            val = row_data.get(key, "")
            if key == "da_duyet":
                val = "Đã duyệt" if val else "Chưa duyệt"
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_body
            cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=(key in ["ly_do_ai", "nhu_cau_mo_ta"]))
            cell.border = border_all
            
            if key == "trang_thai":
                if "HOT" in tier:
                    cell.fill = fill_hot
                    cell.font = font_hot
                elif "WARM" in tier:
                    cell.fill = fill_warm
                    cell.font = font_warm
                else:
                    cell.fill = fill_cold
                    cell.font = font_cold
            elif key == "diem_so":
                cell.font = font_bold
                
        ws.row_dimensions[row_idx].height = 24

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 6. KHỞI TẠO VÀ ĐỒNG BỘ SESSION STATE
# ---------------------------------------------------------------------------
if "leads_df" not in st.session_state:
    initial_df = load_data(source_type="local")
    
    if "da_duyet" not in initial_df.columns:
        initial_df.insert(0, "da_duyet", False)
    if "diem_so" not in initial_df.columns:
        initial_df["diem_so"] = 0
    if "trang_thai" not in initial_df.columns:
        initial_df["trang_thai"] = "COLD"
    if "ly_do_ai" not in initial_df.columns:
        initial_df["ly_do_ai"] = "Chưa kích hoạt AI Scoring"
    if "ghi_chu_sales" not in initial_df.columns:
        initial_df["ghi_chu_sales"] = ""
        
    st.session_state.leads_df = initial_df
    st.session_state.has_run_scoring = False

if "hot_thresh" not in st.session_state:
    st.session_state.hot_thresh = 80
if "warm_thresh" not in st.session_state:
    st.session_state.warm_thresh = 50
if "auto_approve_hot" not in st.session_state:
    st.session_state.auto_approve_hot = True


# ---------------------------------------------------------------------------
# 7. HEADER BANNER DOANH NGHIỆP
# ---------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <h2 style="margin: 0; font-size: 1.55rem; font-weight: 700; letter-spacing: -0.5px;">
                🏢 AI Lead Scoring Bất Động Sản Pro — Enterprise Edition
            </h2>
            <p style="margin: 5px 0 0 0; color: #94A3B8; font-size: 0.92rem;">
                Tự động thẩm định khách hàng 5 tiêu chí theo <code>tieu_chi_cham_diem.txt</code> • Kết nối Google Sheets Private qua Service Account
            </p>
        </div>
        <div style="display: flex; gap: 8px;">
            <span style="background: #2563EB; color: #FFF; padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.3px;">
                Skill: real-estate:lead-scoring
            </span>
            <span style="background: #059669; color: #FFF; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                v2.1 Private Sheet
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 8. SIDEBAR ĐIỀU KHIỂN & CẤU HÌNH NGUỒN DỮ LIỆU
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Nguồn Dữ Liệu & Bộ Máy AI")
    
    source_choice = st.radio(
        "Chọn nguồn nạp dữ liệu:",
        [
            "File khach_hang_bds_500.xlsx (Mặc định)",
            "🔒 Google Sheets Private (Service Account)",
            "🌐 Link Google Sheets Public (CSV Export)",
            "📁 Tải file Excel/CSV từ máy"
        ],
        index=0
    )
    
    # 1. File local
    if source_choice == "File khach_hang_bds_500.xlsx (Mặc định)":
        if st.button("🔄 Nạp Lại Dữ Liệu Từ File Gốc", use_container_width=True):
            loaded = load_data(source_type="local")
            loaded.insert(0, "da_duyet", False)
            loaded["diem_so"] = 0
            loaded["trang_thai"] = "COLD"
            loaded["ly_do_ai"] = "Chưa kích hoạt AI Scoring"
            loaded["ghi_chu_sales"] = ""
            st.session_state.leads_df = loaded
            st.session_state.has_run_scoring = False
            st.success("Đã nạp lại file khach_hang_bds_500.xlsx!")
            st.rerun()

    # 2. Google Sheets Private (Service Account)
    elif source_choice == "🔒 Google Sheets Private (Service Account)":
        sa_ready = get_gspread_client() is not None
        if sa_ready:
            st.success("🟢 Service Account đã kết nối sẵn sàng!")
        else:
            st.warning("⚠️ Chưa cấu hình secrets.toml cho Service Account.")
            with st.expander("ℹ️ Hướng dẫn cấu hình nhanh"):
                st.markdown("""
                1. Tạo Service Account trên Google Cloud Console & tải khóa JSON.
                2. Điền vào `.streamlit/secrets.toml` (xem mẫu `.streamlit/secrets.toml.example`).
                3. **Chia sẻ (Share)** Sheet của bạn cho email Service Account!
                """)
                
        private_id_input = st.text_input(
            "Nhập Sheet ID Private:",
            value=DEFAULT_PRIVATE_SHEET_ID,
            help="Mã ID nằm giữa /d/ và /edit trong URL Google Sheet"
        )
        
        if st.button("🔐 Nạp Dữ Liệu Private Sheet", use_container_width=True):
            with st.spinner("Đang kết nối Service Account và đọc dữ liệu private..."):
                loaded = load_data(source_type="private_sheet", sheet_id=private_id_input)
                if loaded is not None and len(loaded) > 0:
                    loaded.insert(0, "da_duyet", False)
                    loaded["diem_so"] = 0
                    loaded["trang_thai"] = "COLD"
                    loaded["ly_do_ai"] = "Chưa kích hoạt AI Scoring"
                    loaded["ghi_chu_sales"] = ""
                    st.session_state.leads_df = loaded
                    st.session_state.has_run_scoring = False
                    st.success(f"Đã nạp thành công {len(loaded)} dòng từ Private Google Sheet!")
                    st.rerun()
                else:
                    st.error("Không thể đọc dữ liệu. Vui lòng kiểm tra lại cấu hình Service Account và quyền Share!")
            
    # 3. Google Sheets Public
    elif source_choice == "🌐 Link Google Sheets Public (CSV Export)":
        sheet_link = st.text_input("Nhập link Google Sheet:", value=DEFAULT_SHEET_URL)
        if st.button("🌐 Tải Dữ Liệu Từ Sheet Public", use_container_width=True):
            loaded = load_data(source_type="sheet", custom_url=sheet_link)
            loaded.insert(0, "da_duyet", False)
            loaded["diem_so"] = 0
            loaded["trang_thai"] = "COLD"
            loaded["ly_do_ai"] = "Chưa kích hoạt AI Scoring"
            loaded["ghi_chu_sales"] = ""
            st.session_state.leads_df = loaded
            st.session_state.has_run_scoring = False
            st.success(f"Đã tải {len(loaded)} dòng từ Google Sheets!")
            st.rerun()
            
    # 4. Upload từ máy
    elif source_choice == "📁 Tải file Excel/CSV từ máy":
        up_file = st.file_uploader("Chọn file (.xlsx, .csv):", type=["xlsx", "csv"])
        if up_file is not None and st.button("📥 Nạp File Tải Lên", use_container_width=True):
            loaded = load_data(source_type="upload", uploaded_file=up_file)
            loaded.insert(0, "da_duyet", False)
            loaded["diem_so"] = 0
            loaded["trang_thai"] = "COLD"
            loaded["ly_do_ai"] = "Chưa kích hoạt AI Scoring"
            loaded["ghi_chu_sales"] = ""
            st.session_state.leads_df = loaded
            st.session_state.has_run_scoring = False
            st.success(f"Đã nạp {len(loaded)} dòng từ file upload!")
            st.rerun()

    st.markdown("---")
    st.subheader("🤖 AI Scoring Engine")
    st.caption("Quét và chấm điểm tự động theo 5 tiêu chí: Ngân sách, Nhu cầu, Thời gian, Nguồn, Tương tác (+/- 50đ VIP/Rác).")
    
    max_scan = len(st.session_state.leads_df)
    scan_limit = st.slider("Số lượng khách cần chấm điểm:", min_value=1, max_value=max_scan, value=min(500, max_scan))
    
    if st.button("🚀 Kích Hoạt AI Scoring", type="primary", use_container_width=True):
        progress = st.progress(0)
        status = st.empty()
        
        df_target = st.session_state.leads_df.copy()
        
        for i in range(scan_limit):
            desc = str(df_target.at[i, "nhu_cau_mo_ta"])
            name = str(df_target.at[i, "ten_khach"]) if "ten_khach" in df_target.columns else ""
            phone = str(df_target.at[i, "sdt"]) if "sdt" in df_target.columns else ""
            
            res = ai_score_lead(desc, name, phone, hot_threshold=st.session_state.hot_thresh, warm_threshold=st.session_state.warm_thresh)
            df_target.at[i, "diem_so"] = res["diem_so"]
            df_target.at[i, "trang_thai"] = res["trang_thai"]
            df_target.at[i, "ly_do_ai"] = res["ly_do_ai"]
            
            if st.session_state.auto_approve_hot and res["trang_thai"] == "HOT" and not df_target.at[i, "da_duyet"]:
                df_target.at[i, "da_duyet"] = True
                
            if i % 15 == 0 or i == scan_limit - 1:
                progress.progress((i + 1) / scan_limit)
                status.caption(f"Đang phân tích khách {i+1}/{scan_limit}: {name}...")
                
        time.sleep(0.2)
        progress.empty()
        status.empty()
        st.session_state.leads_df = df_target
        st.session_state.has_run_scoring = True
        st.success(f"Đã chấm điểm thành công cho {scan_limit} khách hàng!")
        st.rerun()

    st.markdown("---")
    st.subheader("📌 Tác Vụ Duyệt Hàng Loạt")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("✅ Duyệt HOT", use_container_width=True, help="Tích chọn duyệt cho toàn bộ khách hàng HOT"):
            mask = st.session_state.leads_df["trang_thai"] == "HOT"
            st.session_state.leads_df.loc[mask, "da_duyet"] = True
            st.success(f"Đã duyệt {mask.sum()} khách HOT!")
            st.rerun()
    with col_s2:
        if st.button("❌ Bỏ Duyệt", use_container_width=True, help="Bỏ chọn duyệt tất cả"):
            st.session_state.leads_df["da_duyet"] = False
            st.info("Đã hủy tích chọn duyệt cho tất cả khách hàng.")
            st.rerun()


# ---------------------------------------------------------------------------
# 9. YÊU CẦU 6: HIỂN THỊ METRIC TỔNG QUAN (5 METRICS CHUẨN)
# ---------------------------------------------------------------------------
df = st.session_state.leads_df

total_leads = len(df)
hot_count = len(df[df["trang_thai"] == "HOT"])
warm_count = len(df[df["trang_thai"] == "WARM"])
cold_count = len(df[df["trang_thai"] == "COLD"])
approved_count = len(df[df["da_duyet"] == True])

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Tổng Khách Hàng</div>
        <div class="kpi-value">{total_leads:,}</div>
        <div class="kpi-sub">Hồ sơ dữ liệu</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #EF4444;">
        <div class="kpi-title" style="color: #DC2626;">🔥 Khách HOT</div>
        <div class="kpi-value" style="color: #DC2626;">{hot_count:,}</div>
        <div class="kpi-sub">{hot_count/max(1, total_leads):.1%} cơ hội chốt cao</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #F59E0B;">
        <div class="kpi-title" style="color: #D97706;">⚡ Khách WARM</div>
        <div class="kpi-value" style="color: #D97706;">{warm_count:,}</div>
        <div class="kpi-sub">{warm_count/max(1, total_leads):.1%} cần chăm sóc</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #64748B;">
        <div class="kpi-title" style="color: #475569;">❄️ Khách COLD</div>
        <div class="kpi-value" style="color: #475569;">{cold_count:,}</div>
        <div class="kpi-sub">{cold_count/max(1, total_leads):.1%} nuôi dưỡng / Rác</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #10B981;">
        <div class="kpi-title" style="color: #059669;">✅ Đã Duyệt</div>
        <div class="kpi-value" style="color: #059669;">{approved_count:,}</div>
        <div class="kpi-sub">{approved_count/max(1, total_leads):.1%} sẵn sàng xuất file</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ---------------------------------------------------------------------------
# 10. ĐIỀU HƯỚNG TABS ĐA NĂNG
# ---------------------------------------------------------------------------
tab_main, tab_card, tab_analytics, tab_quick, tab_config = st.tabs([
    "📋 Bảng Duyệt Khách Hàng (st.data_editor)",
    "📇 Thẻ Bàn Giao Lead Chi Tiết & Kịch Bản Sales",
    "📊 Báo Cáo Phân Tích Thông Minh (BI Analytics)",
    "⚡ Thẩm Định Nhanh 1 Khách Hàng",
    "⚙️ Cấu Hình Ma Trận & Hướng Dẫn Service Account"
])


# ===========================================================================
# TAB 1: BẢNG DUYỆT KHÁCH HÀNG (YÊU CẦU 3, 4, 5)
# ===========================================================================
with tab_main:
    # Bộ lọc danh sách
    f1, f2, f3 = st.columns([1.5, 1.5, 3])
    with f1:
        filter_status = st.multiselect(
            "Lọc theo Trạng Thái:",
            options=["HOT", "WARM", "COLD"],
            default=[],
            help="Lọc danh sách theo trạng thái phân loại"
        )
    with f2:
        filter_approval = st.selectbox(
            "Lọc theo Duyệt:",
            options=["Tất cả", "Chỉ khách ĐÃ duyệt", "Chỉ khách CHƯA duyệt"],
            index=0
        )
    with f3:
        search_text = st.text_input(
            "🔎 Tìm kiếm nhanh (Tên khách, SĐT, hoặc Từ khóa nhu cầu):",
            placeholder="Nhập tên, số điện thoại, hoặc từ khóa mô tả..."
        )

    filtered_df = df.copy()

    if filter_status:
        filtered_df = filtered_df[filtered_df["trang_thai"].isin(filter_status)]

    if filter_approval == "Chỉ khách ĐÃ duyệt":
        filtered_df = filtered_df[filtered_df["da_duyet"] == True]
    elif filter_approval == "Chỉ khách CHƯA duyệt":
        filtered_df = filtered_df[filtered_df["da_duyet"] == False]

    if search_text.strip():
        q = search_text.strip().lower()
        mask = (
            filtered_df["ten_khach"].astype(str).str.lower().str.contains(q) |
            filtered_df["sdt"].astype(str).str.contains(q) |
            filtered_df["nhu_cau_mo_ta"].astype(str).str.lower().str.contains(q) |
            filtered_df["ly_do_ai"].astype(str).str.lower().str.contains(q)
        )
        filtered_df = filtered_df[mask]

    st.markdown("### 📝 Bảng Dữ Liệu Khách Hàng (Tương tác duyệt & Chỉnh sửa điểm)")
    st.caption("💡 **Hướng dẫn cho Sales:** Tích chọn cột **`Đã duyệt`** để chọn khách cần xuất Excel. Bạn có thể **sửa trực tiếp Điểm Số** (0 - 100) hoặc đổi **Trạng Thái** (HOT / WARM / COLD) trên bảng, sau đó bấm **💾 Lưu Thay Đổi**.")

    column_config = {
        "da_duyet": st.column_config.CheckboxColumn(
            "Đã duyệt",
            help="Tích chọn để duyệt khách hàng này",
            default=False,
            width="small"
        ),
        "id": st.column_config.NumberColumn(
            "Mã KH",
            help="ID duy nhất của khách hàng",
            disabled=True,
            width="small"
        ),
        "ten_khach": st.column_config.TextColumn(
            "Tên Khách Hàng",
            width="medium"
        ),
        "sdt": st.column_config.TextColumn(
            "Số Điện Thoại",
            width="small"
        ),
        "diem_so": st.column_config.NumberColumn(
            "Điểm Số",
            help="Thang điểm từ 0 đến 100 theo 5 tiêu chí (Sales có thể chỉnh sửa)",
            min_value=0,
            max_value=100,
            step=1,
            width="small"
        ),
        "trang_thai": st.column_config.SelectboxColumn(
            "Trạng Thái",
            help="3 lựa chọn phân loại chính xác: HOT / WARM / COLD (tự động gợi ý theo điểm)",
            options=["HOT", "WARM", "COLD"],
            width="small",
            required=True
        ),
        "ghi_chu_sales": st.column_config.TextColumn(
            "Ghi Chú Sales",
            help="Ghi chú phản hồi thực tế từ chuyên viên tư vấn",
            width="medium"
        ),
        "ly_do_ai": st.column_config.TextColumn(
            "Lý Do AI Chấm Điểm",
            help="Dấu hiệu nhận diện từ tieu_chi_cham_diem.txt",
            disabled=True,
            width="large"
        ),
        "nhu_cau_mo_ta": st.column_config.TextColumn(
            "Mô Tả Nhu Cầu Gốc",
            help="Nội dung nhu cầu khách để lại",
            disabled=True,
            width="large"
        )
    }

    display_cols = [
        "da_duyet", "id", "ten_khach", "sdt", "diem_so", "trang_thai", 
        "ghi_chu_sales", "ly_do_ai", "nhu_cau_mo_ta"
    ]
    for col in display_cols:
        if col not in filtered_df.columns:
            filtered_df[col] = ""

    edited_df = st.data_editor(
        filtered_df[display_cols],
        column_config=column_config,
        use_container_width=True,
        num_rows="dynamic",
        height=430,
        key="lead_scoring_editor"
    )

    col_act1, col_act2, col_act3 = st.columns([2.5, 2.5, 3])

    with col_act1:
        if st.button("💾 Lưu Thay Đổi Vừa Chỉnh Sửa", type="secondary", use_container_width=True):
            sub_update = edited_df[["id", "da_duyet", "diem_so", "trang_thai", "ghi_chu_sales"]].set_index("id")
            
            for row_id, r in sub_update.iterrows():
                sc = r["diem_so"]
                if sc >= st.session_state.hot_thresh and r["trang_thai"] != "HOT":
                    sub_update.at[row_id, "trang_thai"] = "HOT"
                elif st.session_state.warm_thresh <= sc < st.session_state.hot_thresh and r["trang_thai"] != "WARM":
                    sub_update.at[row_id, "trang_thai"] = "WARM"
                elif sc < st.session_state.warm_thresh and r["trang_thai"] != "COLD":
                    sub_update.at[row_id, "trang_thai"] = "COLD"
                    
            master = st.session_state.leads_df.set_index("id")
            master.update(sub_update)
            st.session_state.leads_df = master.reset_index()
            st.success("Đã lưu các chỉnh sửa và cập nhật trạng thái tương ứng!")
            st.rerun()

    with col_act2:
        btn_export = st.button("✅ Duyệt và Xuất Excel", type="primary", use_container_width=True)

    approved_leads = st.session_state.leads_df[st.session_state.leads_df["da_duyet"] == True]

    if btn_export:
        if len(approved_leads) == 0:
            st.warning("⚠️ Hiện chưa có khách hàng nào được tích chọn 'Đã duyệt'. Vui lòng tích chọn ít nhất một khách hàng ở cột 'Đã duyệt' hoặc bấm '✅ Duyệt HOT' tại menu bên trái trước khi xuất Excel.")
        else:
            excel_bytes = generate_excel_bytes(approved_leads)
            export_filename = "leads_scored.xlsx"
            with open(export_filename, "wb") as f:
                f.write(excel_bytes)
            st.success(f"🎉 Đã xuất thành công {len(approved_leads)} khách hàng đã duyệt vào file `{export_filename}`!")

    if len(approved_leads) > 0:
        excel_data = generate_excel_bytes(approved_leads)
        with col_act3:
            st.download_button(
                label=f"📥 Tải Về File leads_scored.xlsx ({len(approved_leads)} khách)",
                data=excel_data,
                file_name="leads_scored.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )


# ===========================================================================
# TAB 2: THẺ BÀN GIAO LEAD CHI TIẾT & KỊCH BẢN SALES
# ===========================================================================
with tab_card:
    st.markdown("### 📇 Thẻ Bàn Giao Khách Hàng Tiềm Năng (Lead Handoff Card)")
    st.caption("Cung cấp đầy đủ thông tin bối cảnh, bằng chứng AI nhận diện và kịch bản mở lời chuẩn hóa giúp Sales chốt hẹn xem nhà.")

    card_options = [
        f"Mã KH #{row['id']} — {row['ten_khach']} ({row['trang_thai']} - {row['diem_so']}đ)"
        for _, row in filtered_df.iterrows()
    ]

    if card_options:
        selected_option = st.selectbox(
            "Chọn khách hàng để xem phiếu bàn giao:",
            options=card_options,
            key="card_lead_selector"
        )
        selected_id = int(selected_option.split(" — ")[0].replace("Mã KH #", ""))
        sel_lead = df[df["id"] == selected_id].iloc[0]
        
        tier_tag = "tag-hot" if sel_lead["trang_thai"] == "HOT" else ("tag-warm" if sel_lead["trang_thai"] == "WARM" else "tag-cold")
        duyet_badge = "✅ ĐÃ DUYỆT" if sel_lead["da_duyet"] else "⏳ CHƯA DUYỆT"
        duyet_bg = "#DCFCE7" if sel_lead["da_duyet"] else "#F1F5F9"
        duyet_color = "#15803D" if sel_lead["da_duyet"] else "#64748B"
        
        clean_phone = re.sub(r"\D", "", str(sel_lead['sdt']))
        if clean_phone.startswith("84"):
            clean_phone = "0" + clean_phone[2:]
            
        zalo_link = f"https://zalo.me/{clean_phone}"
        tel_link = f"tel:{clean_phone}"
        
        if sel_lead["trang_thai"] == "HOT":
            script_text = f"Dạ em chào anh/chị {sel_lead['ten_khach']}, em là phụ trách phân khúc cao cấp tại dự án. Em nhận được thông tin anh/chị đang tìm hiểu dòng sản phẩm biệt thự/penthouse với ngân sách tài chính mạnh. Hiện bên em đang có suất ngoại giao vị trí đẹp ven sông vừa mở bán, em xin phép gửi thông tin mặt bằng chi tiết qua Zalo cho anh/chị trước nhé ạ!"
        elif sel_lead["trang_thai"] == "WARM":
            script_text = f"Dạ em chào anh/chị {sel_lead['ten_khach']}, em thấy anh/chị đang quan tâm căn hộ/nhà phố và cân nhắc phương án vay ngân hàng. Em đã chuẩn bị sẵn bảng tính tiến độ dòng tiền và chính sách chiết khấu tốt nhất tuần này, em gửi qua Zalo anh/chị xem thử nhé ạ!"
        else:
            script_text = f"Dạ em chào anh/chị {sel_lead['ten_khach']}, em liên hệ để gửi tặng anh/chị cẩm nang quy hoạch và bản tin thị trường BĐS tháng này ạ."

        st.markdown(f"""
        <div class="handoff-box">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 14px; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="font-size: 1.45rem; font-weight: 700; color: #0F172A;">{sel_lead['ten_khach']}</span>
                    <span style="margin-left: 14px; font-size: 1.15rem; color: #2563EB; font-weight: 600;">📞 {sel_lead['sdt']}</span>
                    <a href="{tel_link}" style="margin-left: 10px; background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; padding: 3px 10px; border-radius: 6px; font-size: 0.8rem; text-decoration: none; font-weight: 600;">📱 Bấm Gọi</a>
                    <a href="{zalo_link}" target="_blank" style="margin-left: 6px; background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD; padding: 3px 10px; border-radius: 6px; font-size: 0.8rem; text-decoration: none; font-weight: 600;">💬 Nhắn Zalo</a>
                </div>
                <div>
                    <span class="{tier_tag}">{sel_lead['trang_thai']}</span>
                    <span style="margin-left: 10px; font-size: 1.2rem; font-weight: 700; color: #1E293B;">Điểm: {sel_lead['diem_so']}/100</span>
                    <span style="margin-left: 12px; background: {duyet_bg}; color: {duyet_color}; padding: 5px 12px; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">
                        {duyet_badge}
                    </span>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                <div>
                    <h5 style="margin: 0 0 6px 0; color: #475569; font-weight: 600;">🎯 Nhu Cầu Gốc Của Khách:</h5>
                    <p style="background: #F8FAFC; padding: 14px; border-radius: 8px; border: 1px solid #E2E8F0; color: #1E293B; line-height: 1.6; font-size: 0.93rem;">
                        "{sel_lead['nhu_cau_mo_ta']}"
                    </p>
                    <h5 style="margin: 14px 0 6px 0; color: #475569; font-weight: 600;">🧠 Căn Cứ & Bằng Chứng AI Nhận Diện:</h5>
                    <p style="background: #EFF6FF; padding: 14px; border-radius: 8px; border: 1px solid #BFDBFE; color: #1E40AF; line-height: 1.6; font-size: 0.93rem;">
                        {sel_lead['ly_do_ai']}
                    </p>
                </div>
                <div>
                    <h5 style="margin: 0 0 6px 0; color: #059669; font-weight: 600;">🔑 Gợi Ý Kịch Bản Mở Lời Cho Sales (Icebreaker Hook):</h5>
                    <p style="background: #ECFDF5; padding: 14px; border-radius: 8px; border: 1px solid #A7F3D0; color: #065F46; line-height: 1.6; font-weight: 500; font-size: 0.93rem;">
                        "{script_text}"
                    </p>
                    <h5 style="margin: 14px 0 6px 0; color: #475569; font-weight: 600;">⏱️ Cam Kết Thời Gian Phản Hồi (SLA Handoff Protocol):</h5>
                    <p style="background: #FFFBEB; padding: 12px 14px; border-radius: 8px; border: 1px solid #FDE68A; color: #92400E; font-weight: 600; font-size: 0.92rem;">
                        {"Gọi trong vòng ≤ 15 phút (Golden 15 Minutes) • Phân bổ Trưởng phòng/Top Sales" if sel_lead["trang_thai"] == "HOT" else ("Liên hệ trong vòng ≤ 2-4 giờ làm việc • Gửi bảng tính dòng tiền" if sel_lead["trang_thai"] == "WARM" else "Chăm sóc tự động 24h bằng Email Drip / Tin ZNS • Không phân Sales gọi trực tiếp")}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("📋 Sao chép nhanh tin nhắn gửi khách:", value=script_text, height=75)
    else:
        st.info("Không có khách hàng nào phù hợp với bộ lọc hiện tại.")


# ===========================================================================
# TAB 3: BÁO CÁO PHÂN TÍCH THÔNG MINH (BI ANALYTICS)
# ===========================================================================
with tab_analytics:
    st.markdown("### 📊 Báo Cáo Phân Tích Dữ Liệu Khách Hàng Tiềm Năng")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("Cơ cấu Khách Hàng theo Phân Hạng")
        tier_counts = df["trang_thai"].value_counts().reset_index()
        tier_counts.columns = ["Trạng Thái", "Số Lượng"]
        
        chart_tier = alt.Chart(tier_counts).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("Trạng Thái:N", title="Phân Hạng"),
            y=alt.Y("Số Lượng:Q", title="Số Lượng Khách"),
            color=alt.Color("Trạng Thái:N", scale=alt.Scale(
                domain=["HOT", "WARM", "COLD"],
                range=["#DC2626", "#F59E0B", "#64748B"]
            ), legend=None),
            tooltip=["Trạng Thái", "Số Lượng"]
        ).properties(height=280)
        st.altair_chart(chart_tier, use_container_width=True)

    with col_c2:
        st.subheader("Phân Phối Điểm Số (Score Distribution)")
        chart_hist = alt.Chart(df).mark_bar(color="#2563EB", opacity=0.75).encode(
            x=alt.X("diem_so:Q", bin=alt.Bin(maxbins=20), title="Điểm Số AI (0 - 100)"),
            y=alt.Y("count()", title="Tần Suất / Số Lượng"),
            tooltip=["count()"]
        ).properties(height=280)
        st.altair_chart(chart_hist, use_container_width=True)

    st.markdown("---")
    col_c3, col_c4 = st.columns(2)
    
    with col_c3:
        st.subheader("Tỷ Lệ Duyệt Hồ Sơ")
        approval_summary = pd.DataFrame({
            "Trạng Thái": ["Đã Duyệt", "Chưa Duyệt"],
            "Số Lượng": [approved_count, total_leads - approved_count]
        })
        chart_appr = alt.Chart(approval_summary).mark_arc(innerRadius=60).encode(
            theta=alt.Theta(field="Số Lượng", type="quantitative"),
            color=alt.Color(field="Trạng Thái", type="nominal", scale=alt.Scale(
                domain=["Đã Duyệt", "Chưa Duyệt"],
                range=["#10B981", "#E2E8F0"]
            )),
            tooltip=["Trạng Thái", "Số Lượng"]
        ).properties(height=260)
        st.altair_chart(chart_appr, use_container_width=True)

    with col_c4:
        st.subheader("Ước Tính Giá Trị Cơ Hội (Sales Pipeline)")
        est_hot_value = hot_count * 15
        est_warm_value = warm_count * 6
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px;">
            <p style="margin: 0; color: #64748B; font-weight: 600;">💰 Tổng giá trị giỏ hàng tiềm năng HOT:</p>
            <h3 style="margin: 6px 0 14px 0; color: #DC2626;">~ {est_hot_value:,} Tỷ VNĐ</h3>
            <p style="margin: 0; color: #64748B; font-weight: 600;">⚡ Tổng giá trị giỏ hàng tiềm năng WARM:</p>
            <h3 style="margin: 6px 0 0 0; color: #D97706;">~ {est_warm_value:,} Tỷ VNĐ</h3>
        </div>
        """, unsafe_allow_html=True)


# ===========================================================================
# TAB 4: THẨM ĐỊNH NHANH 1 KHÁCH HÀNG MỚI
# ===========================================================================
with tab_quick:
    st.markdown("### ⚡ Thẩm Định Nhanh 1 Khách Hàng (Single Lead Quick Assessment)")
    st.caption("Nhập nhanh thông tin của một khách hàng mới từ cuộc gọi, form web hoặc Zalo để AI chấm điểm tức thì.")

    with st.form("quick_lead_form"):
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            q_name = st.text_input("Tên khách hàng:", placeholder="VD: Nguyễn Văn An")
        with col_q2:
            q_phone = st.text_input("Số điện thoại:", placeholder="VD: 0912345678")
            
        q_desc = st.text_area(
            "Mô tả nhu cầu khách để lại:",
            placeholder="VD: Anh An quan tâm biệt thự đơn lập ven sông, tài chính khoảng 25 tỷ thanh toán thẳng, muốn xem nhà mẫu cuối tuần này...",
            height=110
        )
        
        btn_quick_eval = st.form_submit_button("🚀 Chấm Điểm Ngay", type="primary")

    if btn_quick_eval:
        if not q_desc.strip():
            st.error("Vui lòng nhập mô tả nhu cầu khách hàng.")
        else:
            q_res = ai_score_lead(q_desc, q_name, q_phone, hot_threshold=st.session_state.hot_thresh, warm_threshold=st.session_state.warm_thresh)
            
            st.markdown("#### 🎯 Kết Quả Đánh Giá AI:")
            q_col1, q_col2, q_col3 = st.columns(3)
            with q_col1:
                st.metric("Điểm Số", f"{q_res['diem_so']}/100")
            with q_col2:
                st.metric("Phân Hạng", q_res["trang_thai"])
            with q_col3:
                st.metric("Cam Kết SLA", q_res["sla"])
                
            st.info(f"**Căn cứ AI:** {q_res['ly_do_ai']}")
            st.success(f"**Gợi ý kịch bản mở lời:** {q_res['goi_y_sales']}")
            
            if st.button("➕ Thêm Khách Hàng Này Vào Danh Sách Quản Trị", type="secondary"):
                new_id = len(st.session_state.leads_df) + 1
                new_row = {
                    "da_duyet": True if q_res["trang_thai"] == "HOT" else False,
                    "id": new_id,
                    "ten_khach": q_name if q_name else f"Khách Hàng #{new_id}",
                    "sdt": q_phone if q_phone else "Chưa có",
                    "diem_so": q_res["diem_so"],
                    "trang_thai": q_res["trang_thai"],
                    "ly_do_ai": q_res["ly_do_ai"],
                    "nhu_cau_mo_ta": q_desc,
                    "ghi_chu_sales": "Được thẩm định nhanh qua Tab Quick Assessment"
                }
                st.session_state.leads_df = pd.concat([st.session_state.leads_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Đã lưu khách hàng #{new_id} vào danh sách quản trị!")
                st.rerun()


# ===========================================================================
# TAB 5: CẤU HÌNH MA TRẬN & HƯỚNG DẪN SERVICE ACCOUNT
# ===========================================================================
with tab_config:
    st.markdown("### ⚙️ Cấu Hình Ma Trận Điểm Số & Thiết Lập Service Account")
    st.caption("Cho phép tùy chỉnh ngưỡng điểm và xem hướng dẫn chi tiết kết nối Google Cloud Service Account để đọc Private Sheet.")

    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        st.session_state.hot_thresh = st.slider("Ngưỡng điểm HOT (Điểm ≥ ngưỡng này):", min_value=70, max_value=95, value=st.session_state.hot_thresh)
        st.session_state.warm_thresh = st.slider("Ngưỡng điểm WARM (Điểm ≥ ngưỡng này):", min_value=40, max_value=75, value=st.session_state.warm_thresh)
    with col_cfg2:
        st.session_state.auto_approve_hot = st.checkbox("Tự động tích chọn duyệt cho khách hàng HOT khi AI quét xong", value=st.session_state.auto_approve_hot)
        st.markdown("""
        **Quy tắc tiêu chuẩn (tieu_chi_cham_diem.txt):**
        - Thưởng VIP: +50 điểm (≥ 20-30 tỷ, Shophouse sỉ, Penthouse, Đất CN > 2000m2)
        - Phạt Rác: -50 điểm (Nhầm số, đòi mua Q1 giá 1 tỷ, spam bảo hiểm, thuê bao)
        """)

    st.markdown("---")
    st.markdown("### 📖 HƯỚNG DẪN TẠO GOOGLE CLOUD SERVICE ACCOUNT (ĐỌC SHEET PRIVATE)")
    
    st.markdown("""
    Để đọc Google Sheet private mà **không cần công khai link** (Public Link), bạn thực hiện theo 5 bước sau:

    #### Bước 1: Tạo Project trên Google Cloud Console
    1. Truy cập [Google Cloud Console](https://console.cloud.google.com/).
    2. Đăng nhập tài khoản Google và nhấn chọn **Select a project** > **New Project**.
    3. Đặt tên project (ví dụ: `BDS-Lead-Scoring`) rồi nhấn **Create**.

    #### Bước 2: Bật Google Sheets API và Google Drive API
    1. Vào thanh tìm kiếm gõ **Google Sheets API** > Nhấn **Enable**.
    2. Vào thanh tìm kiếm gõ **Google Drive API** > Nhấn **Enable**.

    #### Bước 3: Tạo Service Account (Tài khoản dịch vụ)
    1. Vào menu **IAM & Admin** > **Service Accounts**.
    2. Nhấn nút **+ Create Service Account**.
    3. Điền tên (ví dụ: `lead-scoring-sa`), nhấn **Create and Continue**.
    4. Tại mục phân quyền (Role), chọn quyền **Viewer** (hoặc **Editor**), rồi nhấn **Done**.
    5. Copy lại địa chỉ **Email** của Service Account vừa tạo (dạng: `lead-scoring-sa@ten-project.iam.gserviceaccount.com`).

    #### Bước 4: Tạo Khóa (Key JSON)
    1. Nhấp vào tên Service Account vừa tạo.
    2. Chuyển sang tab **Keys** > Nhấn **Add Key** > Chọn **Create new key**.
    3. Chọn định dạng **JSON** > Nhấn **Create**. File JSON khóa bí mật sẽ tự động tải về máy bạn.

    #### Bước 5: Cấu hình vào Streamlit Secrets (`.streamlit/secrets.toml`)
    1. Mở file JSON vừa tải về bằng Notepad/VSCode.
    2. Tạo file `.streamlit/secrets.toml` trong thư mục workspace (theo file mẫu `.streamlit/secrets.toml.example`).
    3. Dán các thông tin vào theo cấu trúc TOML:
    ```toml
    [gcp_service_account]
    type = "service_account"
    project_id = "ten-project-cua-ban"
    private_key_id = "..."
    private_key = "-----BEGIN PRIVATE KEY-----\\nMIIEv...\\n-----END PRIVATE KEY-----\\n"
    client_email = "lead-scoring-sa@ten-project.iam.gserviceaccount.com"
    client_id = "..."
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "..."
    ```

    #### ⭐ Bước 6: QUAN TRỌNG NHẤT — Chia Sẻ Google Sheet Private
    - Mở file Google Sheet Private của bạn lên.
    - Nhấn nút **Chia sẻ (Share)** ở góc trên bên phải.
    - Dán địa chỉ email của Service Account (`...iam.gserviceaccount.com`) vào ô mời.
    - Chọn quyền **Người xem (Viewer)** hoặc **Người chỉnh sửa (Editor)** > Nhấn **Gửi (Send)**.
    - Copy mã **Sheet ID** (chuỗi nằm giữa `/d/` và `/edit` trên thanh URL) dán vào ứng dụng là xong!
    """)


# ---------------------------------------------------------------------------
# 11. FOOTER BẢN QUYỀN
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.82rem; padding: 12px 0;">
    Phát triển bởi <b>Phạm Minh Hoàng</b> — Khóa học <i>Agentic AI with Google Antigravity</i> • Cố vấn: <b>MT Đức Thuận</b> (AI4A)<br>
    Tuân thủ quy chuẩn bảo mật dữ liệu PII Nghị định 13/2023/NĐ-CP & Mô hình Human-In-The-Loop
</div>
""", unsafe_allow_html=True)
