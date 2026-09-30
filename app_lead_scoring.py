"""
=============================================================================
HỆ THỐNG CHẤM ĐIỂM & PHÂN LOẠI KHÁCH HÀNG BẤT ĐỘNG SẢN (LEAD SCORING AI)
Phát triển bởi: Phạm Minh Hoàng (AI4A - Antigravity)
Dựa trên:
  1. Skill: real-estate:lead-scoring (SKILL.md & lead_scoring_skill.md)
  2. Quy chuẩn tiêu chí: knowledge-base/tieu_chi_cham_diem.txt
  3. CSDL Khách hàng BĐS: Google Sheets 500+ Leads
=============================================================================
"""

import re
import io
import time
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# CẤU HÌNH TRANG STREAMLIT
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Lead Scoring BĐS | Human-In-The-Loop",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách Modern Enterprise UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: #F8FAFC;
        margin-bottom: 24px;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-card {
        background: #FFFFFF;
        padding: 18px 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 6px;
        color: #0F172A;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 4px;
    }
    
    .handoff-box {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
    
    .tag-hot {
        background-color: #FEE2E2;
        color: #DC2626;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .tag-warm {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .tag-cold {
        background-color: #F1F5F9;
        color: #64748B;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# LOGIC AI SCORING ENGINE (DỰA TRÊN SKILL & TIEU_CHI_CHAM_DIEM.TXT)
# ---------------------------------------------------------------------------
def ai_score_lead(description: str, name: str = "", phone: str = "") -> dict:
    """
    Agentic Heuristic Lead Scoring Engine cho Bất Động Sản:
    Quét mô tả khách hàng theo 5 tiêu chí:
      1. Ngân sách & Năng lực tài chính (0-30đ) + VIP/Phạt
      2. Mức độ quan tâm & Khớp nhu cầu (0-25đ)
      3. Thời gian & Tính cấp thiết (0-20đ)
      4. Nguồn khách & Độ tin cậy (0-15đ)
      5. Mức độ tương tác & Thiện chí (0-10đ)
    Đồng thời áp dụng chuẩn:
      - TIÊU CHÍ CỘNG 50 ĐIỂM (VIP / SIÊU TIỀM NĂNG)
      - TIÊU CHÍ TRỪ 50 ĐIỂM (RÁC / KHÔNG TIỀM NĂNG)
    """
    if not isinstance(description, str) or not description.strip():
        return {
            "diem_so": 0,
            "phan_loai": "❄️ COLD",
            "ly_do_ai": "Mô tả rỗng hoặc không có dữ liệu",
            "goi_y_sales": "Yêu cầu thu thập thêm thông tin từ khách",
            "nhan_to_vip": [],
            "nhan_to_rac": [],
            "sla": "Chăm sóc tự động",
            "trang_thai_duyet": "Chưa duyệt"
        }

    text = description.lower()
    
    # -----------------------------------------------------------------------
    # 1. QUÉT DẤU HIỆU RÁC / TRỪ 50 ĐIỂM (JUNK & RED FLAGS)
    # -----------------------------------------------------------------------
    junk_reasons = []
    
    # a. Không có nhu cầu / Dữ liệu cũ
    if any(k in text for k in ["nhầm số", "không có nhu cầu", "dữ liệu cũ", "nhầm ngành", "lộn số"]):
        junk_reasons.append("Báo nhầm số / không có nhu cầu BĐS / data trộn ngành")
        
    # b. Khách không thiện chí / Hỏi cho vui
    if any(k in text for k in ["hỏi giá cho vui", "chưa có ý định mua", "thái độ không hợp tác", "không hợp tác"]):
        junk_reasons.append("Hỏi giá cho vui / thái độ không hợp tác")
        
    # c. Spam / Quảng cáo ngược
    if any(k in text for k in ["spam", "bảo hiểm", "vay vốn", "mời chào dịch vụ", "quảng cáo ngược"]):
        junk_reasons.append("Spam chào bán dịch vụ khác / chào vay / bảo hiểm")
        
    # d. Lỗi liên lạc nghiêm trọng
    if any(k in text for k in ["thuê bao", "không bắt máy", "không phản hồi zalo", "không nghe máy"]):
        junk_reasons.append("Số điện thoại thuê bao / gọi nhiều lần không nghe máy")
        
    # e. Yêu cầu phi thực tế
    irrational_patterns = [
        r"nhà\s+q1\s+giá\s+1",
        r"nhà\s+quận\s+1\s+giá\s+1",
        r"quận\s+1\s+giá\s+1\s*[-–]?\s*2\s*tỷ",
        r"thuê.*nguyên\s+căn.*2\s*triệu.*trung\s+tâm",
        r"thuê.*2\s*triệu.*trung\s+tâm",
        r"giá\s+thấp\s+vô\s+lý",
        r"vài\s+trăm\s+triệu.*hồ\s+bơi"
    ]
    for pat in irrational_patterns:
        if re.search(pat, text):
            junk_reasons.append("Đòi hỏi mức giá phi thực tế so với thị trường")
            break

    # -----------------------------------------------------------------------
    # 2. QUÉT DẤU HIỆU VIP / CỘNG 50 ĐIỂM (VIP ACCELERATOR)
    # -----------------------------------------------------------------------
    vip_reasons = []
    
    # a. Ngân sách cực lớn / Không thành vấn đề
    vip_budget_kw = ["trên 20 tỷ", "trên 30 tỷ", "20 tỷ", "30 tỷ", "50 tỷ", "tài chính cực mạnh", "tài chính mạnh", "không thành vấn đề", "thanh toán thẳng", "tiền mặt sẵn"]
    if any(k in text for k in vip_budget_kw):
        vip_reasons.append("Ngân sách lớn (≥20-30 tỷ / Thanh toán thẳng / Tài chính cực mạnh)")
        
    # b. Loại hình sản phẩm cao cấp
    vip_products = ["biệt thự đơn lập", "penthouse", "shophouse mặt đường lớn", "quỹ đất công nghiệp", "sàn văn phòng", "diện tích lớn", "2000m2", "hồ bơi riêng", "thang máy riêng"]
    if any(k in text for k in vip_products):
        vip_reasons.append("Loại hình cao cấp (Biệt thự/Penthouse/Shophouse sỉ/Đất CN >2000m2)")
        
    # c. Vị trí đắc địa & Phân khu VIP
    vip_locations = ["ven sông", "phân khu cao cấp nhất", "quận 1", "vinhomes ocean park", "phú mỹ hưng"]
    if any(k in text for k in vip_locations):
        vip_reasons.append("Vị trí đắc địa (Ven sông/Quận 1/Phú Mỹ Hưng/Ocean Park)")
        
    # d. Đối tượng khách hàng VIP
    vip_clients = ["chủ doanh nghiệp", "nhà đầu tư chuyên nghiệp", "mua sỉ", "gom sỉ", "5-10 căn"]
    if any(k in text for k in vip_clients):
        vip_reasons.append("Đối tượng VIP (Chủ doanh nghiệp/Nhà đầu tư gom sỉ)")
        
    # e. Tính cấp thiết & Minh bạch cao
    vip_urgency = ["pháp lý chuẩn 100%", "sổ hồng riêng", "gặp trực tiếp chủ đầu tư", "giám đốc dự án", "đã từng mua nhiều dự án"]
    if any(k in text for k in vip_urgency):
        vip_reasons.append("Đòi hỏi pháp lý 100% / Muốn gặp CĐT / Khách quen tập đoàn")

    # -----------------------------------------------------------------------
    # 3. TÍNH ĐIỂM CHI TIẾT 5 TIÊU CHÍ (BASE 0 - 100 ĐIỂM)
    # -----------------------------------------------------------------------
    # Tiêu chí 1: Ngân sách (0 - 30đ)
    p_budget = 10
    if vip_reasons:
        p_budget = 30
    elif any(k in text for k in ["8-10 tỷ", "8 đến 10 tỷ", "10 tỷ", "12 tỷ", "15 tỷ"]):
        p_budget = 25
    elif any(k in text for k in ["4-5 tỷ", "4 đến 5 tỷ", "5 tỷ", "6 tỷ", "7 tỷ"]):
        p_budget = 18
    elif any(k in text for k in ["2-3 tỷ", "2 đến 3 tỷ", "3 tỷ", "dưới 50 triệu/tháng", "50 triệu"]):
        p_budget = 15
    elif junk_reasons:
        p_budget = 0
        
    # Tiêu chí 2: Mức độ quan tâm / Độ khớp sản phẩm (0 - 25đ)
    p_interest = 12
    if any(k in text for k in ["penthouse", "biệt thự", "shophouse", "sàn văn phòng", "đất công nghiệp"]):
        p_interest = 25
    elif any(k in text for k in ["căn hộ 2pn", "nhà phố liền kề", "mặt bằng kinh doanh spa", "đất nền vùng ven"]):
        p_interest = 20
    elif any(k in text for k in ["cân nhắc giữa 2 dự án", "chính sách chiết khấu", "hỗ trợ vay ngân hàng"]):
        p_interest = 18
        
    # Tiêu chí 3: Thời gian mua & Tính cấp thiết (0 - 20đ)
    p_timeline = 10
    if any(k in text for k in ["cuối tuần này", "trong tuần", "ký hợp đồng dài hạn", "ngay", "muốn đi xem nhà mẫu"]):
        p_timeline = 20
    elif any(k in text for k in ["đầu tư dài hạn", "đang cân nhắc"]):
        p_timeline = 14
    elif any(k in text for k in ["chưa có ý định", "cho vui"]):
        p_timeline = 0
        
    # Tiêu chí 4: Nguồn khách (0 - 15đ)
    p_source = 10
    if any(k in text for k in ["đã từng mua nhiều dự án", "khách quen", "chủ doanh nghiệp lớn"]):
        p_source = 15
    elif any(k in text for k in ["đăng ký xem nhà mẫu", "spa tại quận 1"]):
        p_source = 12
    elif any(k in text for k in ["dữ liệu cũ", "nhầm số"]):
        p_source = 0
        
    # Tiêu chí 5: Tương tác & Thiện chí (0 - 10đ)
    p_engagement = 8
    if any(k in text for k in ["muốn gặp trực tiếp", "muốn đi xem nhà mẫu", "yêu cầu"]):
        p_engagement = 10
    elif any(k in text for k in ["thuê bao", "không bắt máy", "không phản hồi"]):
        p_engagement = 0

    base_score = p_budget + p_interest + p_timeline + p_source + p_engagement
    
    # -----------------------------------------------------------------------
    # 4. KẾT HỢP ĐIỂM THƯỞNG / PHẠT VÀ PHÂN LOẠI
    # -----------------------------------------------------------------------
    total_score = base_score
    
    if junk_reasons:
        # Áp dụng tiêu chí TRỪ 50 ĐIỂM
        total_score -= 50
        total_score = max(0, min(total_score, 45))  # Khóa trần COLD
        phan_loai = "❄️ COLD"
        sla = "Chăm sóc tự động / Không phân Sales"
        ly_do = f"⛔ Phát hiện dấu hiệu rác (-50đ): {'; '.join(junk_reasons)}"
        goi_y = "Loại bỏ khỏi danh sách gọi hàng ngày; đưa vào kịch bản nuôi dưỡng tự động hoặc Blacklist."
        
    elif vip_reasons:
        # Áp dụng tiêu chí CỘNG 50 ĐIỂM
        total_score += 50
        total_score = min(100, max(85, total_score))  # Đảm bảo phân khúc HOT VIP
        phan_loai = "🔥 HOT"
        sla = "≤ 15 Phút (Ưu tiên số 1)"
        ly_do = f"🌟 Đạt tiêu chí Siêu VIP (+50đ): {'; '.join(vip_reasons)}"
        goi_y = f"Bàn giao ngay cho Trưởng phòng/Top Sales gọi trong 15p. Chuẩn bị tài liệu VIP & hồ sơ pháp lý 100%."
        
    else:
        # Phân loại dựa trên điểm cơ sở
        if total_score >= 80 or any(k in text for k in ["xem nhà mẫu vào cuối tuần này", "ký hợp đồng dài hạn"]):
            total_score = min(100, max(80, total_score))
            phan_loai = "🔥 HOT"
            sla = "≤ 15-30 Phút"
            ly_do = "Nhu cầu rõ ràng, thời gian cấp thiết (hẹn xem nhà cuối tuần/ký HĐ ngay)."
            goi_y = "Gọi điện xác nhận lịch hẹn xem nhà mẫu / sa bàn trong ngày hôm nay."
        elif total_score >= 50:
            phan_loai = "⚡ WARM"
            sla = "≤ 2 - 4 Giờ"
            ly_do = "Có nhu cầu thực tế tầm trung, đang cân nhắc tài chính/chính sách chiết khấu."
            goi_y = "Gửi trọn bộ bảng giá, bảng tính dòng tiền ngân hàng qua Zalo và hẹn lịch tư vấn sâu."
        else:
            phan_loai = "❄️ COLD"
            sla = "Chăm sóc tự động"
            ly_do = "Nhu cầu chưa cụ thể hoặc thời gian mua dài hạn."
            goi_y = "Gửi bản tin thị trường định kỳ, chưa cần ưu tiên gọi trực tiếp."

    return {
        "diem_so": int(total_score),
        "phan_loai": phan_loai,
        "ly_do_ai": ly_do,
        "goi_y_sales": goi_y,
        "nhan_to_vip": vip_reasons,
        "nhan_to_rac": junk_reasons,
        "sla": sla,
        "trang_thai_duyet": "Chưa duyệt"
    }


# ---------------------------------------------------------------------------
# HÀM TẢI DỮ LIỆU TỪ GOOGLE SHEETS HOẶC LOCAL CACHE
# ---------------------------------------------------------------------------
DEFAULT_SHEET_URL = "https://docs.google.com/spreadsheets/d/149rRXA8rSQKsAaMW0Kyt3q6Mzv9_KltAXgIXVTnuQoM/export?format=csv&gid=1542775777"

@st.cache_data(show_spinner=False)
def load_dataset(source_url: str):
    """Tải dữ liệu từ URL Google Sheets CSV export"""
    try:
        df = pd.read_csv(source_url)
        # Chuẩn hóa tên cột
        df.columns = [c.strip().lower() for c in df.columns]
        # Đảm bảo các cột cần thiết
        if "id" not in df.columns:
            df["id"] = range(1, len(df) + 1)
        if "sdt" in df.columns:
            df["sdt"] = df["sdt"].astype(str).str.replace(r"\.0$", "", regex=True)
            # Thêm số 0 đầu nếu thiếu
            df["sdt"] = df["sdt"].apply(lambda x: "0" + x if len(x) == 9 else x)
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu từ Google Sheets: {e}")
        # Dữ liệu fallback dự phòng nếu không có mạng
        return pd.DataFrame([
            {"id": 127, "ten_khach": "Bùi Phương Tâm", "sdt": "0790240040", "nhu_cau_mo_ta": "Khách hàng VIP, quan tâm biệt thự đơn lập phân khu cao cấp nhất. Ngân sách trên 30 tỷ, thanh toán thẳng. Yêu cầu vị trí ven sông, hướng Đông Nam."},
            {"id": 28, "ten_khach": "Trần Hoàng Dũng", "sdt": "0943392982", "nhu_cau_mo_ta": "Chủ doanh nghiệp lớn, cần tìm quỹ đất công nghiệp hoặc sàn văn phòng diện tích trên 2000m2 tại khu Đông. Tài chính cực mạnh, yêu cầu pháp lý chuẩn 100%."},
            {"id": 3, "ten_khach": "Lý Đức Cường", "sdt": "0953430096", "nhu_cau_mo_ta": "Quan tâm căn hộ 2PN tại Quận 7 cho gia đình trẻ. Tài chính khoảng 4-5 tỷ, cần hỗ trợ vay ngân hàng 70%. Muốn đi xem nhà mẫu vào cuối tuần này."},
            {"id": 5, "ten_khach": "Ngô Anh Mai", "sdt": "0784760799", "nhu_cau_mo_ta": "Tìm nhà phố liền kề khu vực nội thành, ưu tiên gần trường học và bệnh viện. Ngân sách 8-10 tỷ. Đang cân nhắc giữa 2 dự án, cần tư vấn thêm về chính sách chiết khấu."},
            {"id": 20, "ten_khach": "Hồ Phương Mai", "sdt": "0915805255", "nhu_cau_mo_ta": "Hỏi giá cho vui, chưa có ý định mua trong năm nay. Ngân sách rất thấp so với mặt bằng chung (đòi mua nhà Q1 giá 1 tỷ)."},
            {"id": 70, "ten_khach": "Hồ Đức Lan", "sdt": "0991102318", "nhu_cau_mo_ta": "Spam, gọi điện đến chỉ để quảng cáo ngược lại dịch vụ bảo hiểm."},
            {"id": 7, "ten_khach": "Đặng Hoàng Dũng", "sdt": "0953795436", "nhu_cau_mo_ta": "Số điện thoại hay bị thuê bao, gọi nhiều lần không bắt máy. Nhắn tin Zalo không phản hồi."},
            {"id": 1, "ten_khach": "Phan Văn Hoa", "sdt": "0894782782", "nhu_cau_mo_ta": "Đang tìm thuê mặt bằng kinh doanh spa tại Quận 1, diện tích khoảng 80-100m2. Giá thuê mong muốn dưới 50 triệu/tháng. Cần ký hợp đồng dài hạn."}
        ])


# ---------------------------------------------------------------------------
# KHỞI TẠO SESSION STATE
# ---------------------------------------------------------------------------
if "leads_df" not in st.session_state:
    raw_df = load_dataset(DEFAULT_SHEET_URL)
    
    # Khởi tạo các cột AI Scoring ban đầu nếu chưa có
    if "diem_so" not in raw_df.columns:
        raw_df["diem_so"] = 0
        raw_df["phan_loai"] = "Chưa quét"
        raw_df["trang_thai_duyet"] = "Chưa duyệt"
        raw_df["ly_do_ai"] = "Chưa kích hoạt AI Scoring"
        raw_df["goi_y_sales"] = ""
        raw_df["ghi_chu_sales"] = ""
        
    st.session_state.leads_df = raw_df
    st.session_state.has_scored = False


# ---------------------------------------------------------------------------
# GIAO DIỆN CHÍNH
# ---------------------------------------------------------------------------

# Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="margin: 0; font-size: 1.6rem; font-weight: 700;">🏢 AI Lead Scoring BĐS — Human-In-The-Loop System</h2>
            <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Tự động hóa thẩm định khách hàng tiềm năng 5 tiêu chí (BANT-SE) kết hợp duyệt thủ công qua <code>st.data_editor</code>
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: #2563EB; color: #FFF; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                Skill: real-estate:lead-scoring
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar Điều Khiển
with st.sidebar:
    st.header("⚙️ Bảng Điều Khiển")
    
    st.markdown("### 📥 Nguồn Dữ Liệu")
    data_source_mode = st.radio("Chọn nguồn:", ["Google Sheets Trực Tuyến", "Tải file CSV/Excel lên", "Dữ liệu Mẫu 8 Lead"])
    
    if data_source_mode == "Google Sheets Trực Tuyến":
        sheet_url = st.text_input("URL Google Sheet CSV:", value=DEFAULT_SHEET_URL)
        if st.button("🔄 Tải Lại Dữ Liệu Từ Sheet", use_container_width=True):
            st.session_state.leads_df = load_dataset(sheet_url)
            st.session_state.has_scored = False
            st.rerun()
            
    elif data_source_mode == "Tải file CSV/Excel lên":
        uploaded_file = st.file_uploader("Chọn file CSV hoặc Excel:", type=["csv", "xlsx"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                new_df = pd.read_csv(uploaded_file)
            else:
                new_df = pd.read_excel(uploaded_file)
            new_df.columns = [c.strip().lower() for c in new_df.columns]
            st.session_state.leads_df = new_df
            st.session_state.has_scored = False
            st.success(f"Đã nạp {len(new_df)} dòng dữ liệu!")
            
    elif data_source_mode == "Dữ liệu Mẫu 8 Lead":
        if st.button("Nạp 8 Hồ Sơ Điển Hình", use_container_width=True):
            st.session_state.leads_df = load_dataset("invalid_url_to_force_fallback")
            st.session_state.has_scored = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Tự Động Hóa Chấm Điểm")
    
    limit_leads = st.number_input("Số lượng Lead cần quét (0 = Toàn bộ):", min_value=0, max_value=len(st.session_state.leads_df), value=min(50, len(st.session_state.leads_df)))
    
    btn_run_ai = st.button("🚀 Chạy AI Scoring (Agent)", type="primary", use_container_width=True)
    
    if btn_run_ai:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        target_df = st.session_state.leads_df.copy()
        total_rows = len(target_df) if limit_leads == 0 else limit_leads
        
        for idx in range(total_rows):
            desc = str(target_df.at[idx, "nhu_cau_mo_ta"])
            name = str(target_df.at[idx, "ten_khach"]) if "ten_khach" in target_df.columns else ""
            phone = str(target_df.at[idx, "sdt"]) if "sdt" in target_df.columns else ""
            
            res = ai_score_lead(desc, name, phone)
            target_df.at[idx, "diem_so"] = res["diem_so"]
            target_df.at[idx, "phan_loai"] = res["phan_loai"]
            target_df.at[idx, "ly_do_ai"] = res["ly_do_ai"]
            target_df.at[idx, "goi_y_sales"] = res["goi_y_sales"]
            
            # Giữ nguyên trạng thái duyệt nếu đã duyệt trước đó
            if "trang_thai_duyet" not in target_df.columns or target_df.at[idx, "trang_thai_duyet"] == "Chưa duyệt":
                # Tự động gợi ý trạng thái
                if res["phan_loai"] == "🔥 HOT":
                    target_df.at[idx, "trang_thai_duyet"] = "Chưa duyệt (Gợi ý: Duyệt Giao Sales)"
                elif res["phan_loai"] == "⚡ WARM":
                    target_df.at[idx, "trang_thai_duyet"] = "Chưa duyệt"
                else:
                    target_df.at[idx, "trang_thai_duyet"] = "Chưa duyệt (Gợi ý: Blacklist/Lọc bỏ)"
                    
            if idx % 5 == 0 or idx == total_rows - 1:
                progress_bar.progress((idx + 1) / total_rows)
                status_text.text(f"Đang quét hồ sơ {idx+1}/{total_rows}: {name}...")
                
        time.sleep(0.3)
        progress_bar.empty()
        status_text.empty()
        st.session_state.leads_df = target_df
        st.session_state.has_scored = True
        st.success(f"Hoàn thành chấm điểm cho {total_rows} khách hàng!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Thao Tác Nhanh")
    if st.button("✅ Duyệt Hàng Loạt: Giao Hết HOT Leads", use_container_width=True):
        mask = st.session_state.leads_df["phan_loai"] == "🔥 HOT"
        st.session_state.leads_df.loc[mask, "trang_thai_duyet"] = "✅ Đã duyệt - Giao Sales"
        st.success(f"Đã duyệt giao Sales cho {mask.sum()} HOT Leads!")
        st.rerun()
        
    if st.button("⛔ Blacklist Hàng Loạt: Loại COLD Lead Rác", use_container_width=True):
        mask = st.session_state.leads_df["phan_loai"] == "❄️ COLD"
        st.session_state.leads_df.loc[mask, "trang_thai_duyet"] = "⛔ Từ chối / Blacklist"
        st.warning(f"Đã chuyển {mask.sum()} COLD Leads vào Blacklist!")
        st.rerun()


# ---------------------------------------------------------------------------
# THẺ CHỈ SỐ KPI TỔNG QUAN
# ---------------------------------------------------------------------------
df = st.session_state.leads_df

total_leads = len(df)
hot_count = len(df[df["phan_loai"] == "🔥 HOT"]) if "phan_loai" in df.columns else 0
warm_count = len(df[df["phan_loai"] == "⚡ WARM"]) if "phan_loai" in df.columns else 0
cold_count = len(df[df["phan_loai"] == "❄️ COLD"]) if "phan_loai" in df.columns else 0

approved_count = len(df[df["trang_thai_duyet"].astype(str).str.contains("Đã duyệt", na=False)]) if "trang_thai_duyet" in df.columns else 0
pending_count = total_leads - approved_count

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Tổng Khách Hàng</div>
        <div class="kpi-value">{total_leads:,}</div>
        <div class="kpi-sub">Hồ sơ trong hệ thống</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #EF4444;">
        <div class="kpi-title" style="color: #DC2626;">🔥 Khách Hàng HOT</div>
        <div class="kpi-value" style="color: #DC2626;">{hot_count}</div>
        <div class="kpi-sub">{hot_count/max(1, total_leads):.1%} cơ hội chốt cao</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #F59E0B;">
        <div class="kpi-title" style="color: #D97706;">⚡ Khách Hàng WARM</div>
        <div class="kpi-value" style="color: #D97706;">{warm_count}</div>
        <div class="kpi-sub">{warm_count/max(1, total_leads):.1%} cần chăm sóc</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #64748B;">
        <div class="kpi-title">❄️ Khách Hàng COLD</div>
        <div class="kpi-value">{cold_count}</div>
        <div class="kpi-sub">{cold_count/max(1, total_leads):.1%} lọc rác / Drip</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #10B981;">
        <div class="kpi-title" style="color: #059669;">✅ Con Người Đã Duyệt</div>
        <div class="kpi-value" style="color: #059669;">{approved_count}</div>
        <div class="kpi-sub">{pending_count} hồ sơ đang chờ</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ---------------------------------------------------------------------------
# BỘ LỌC DỮ LIỆU HIỂN THỊ
# ---------------------------------------------------------------------------
st.markdown("### 🔍 Bộ Lọc Danh Sách")
f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 3])

with f_col1:
    filter_tier = st.multiselect(
        "Lọc theo Phân loại AI:",
        options=["🔥 HOT", "⚡ WARM", "❄️ COLD", "Chưa quét"],
        default=[]
    )

with f_col2:
    filter_status = st.multiselect(
        "Lọc theo Trạng thái duyệt:",
        options=sorted(list(set(df["trang_thai_duyet"].dropna().astype(str)))),
        default=[]
    )

with f_col3:
    search_query = st.text_input("🔎 Tìm kiếm theo Tên khách, SĐT, hoặc Từ khóa nhu cầu:", placeholder="Nhập từ khóa...")

# Áp dụng bộ lọc
filtered_df = df.copy()
if filter_tier:
    filtered_df = filtered_df[filtered_df["phan_loai"].isin(filter_tier)]
if filter_status:
    filtered_df = filtered_df[filtered_df["trang_thai_duyet"].isin(filter_status)]
if search_query:
    q = search_query.lower()
    mask = (
        filtered_df["ten_khach"].astype(str).str.lower().str.contains(q) |
        filtered_df["sdt"].astype(str).str.contains(q) |
        filtered_df["nhu_cau_mo_ta"].astype(str).str.lower().str.contains(q)
    )
    filtered_df = filtered_df[mask]


# ---------------------------------------------------------------------------
# BẢNG TƯƠNG TÁC DUYỆT TRẠNG THÁI VỚI ST.DATA_EDITOR (HUMAN-IN-THE-LOOP)
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📝 Bảng Duyệt Khách Hàng Tiềm Năng (Human Approval Table)")
st.caption("💡 **Hướng dẫn:** Bạn có thể nhấp đúp trực tiếp vào cột **`Trạng Thái Duyệt`**, **`Điểm AI`** hoặc **`Ghi Chú Sales`** để điều chỉnh, sau đó nhấn **Lưu Thay Đổi** phía dưới.")

# Cấu hình hiển thị cột cho st.data_editor
column_config = {
    "id": st.column_config.NumberColumn("ID", width="small", disabled=True),
    "ten_khach": st.column_config.TextColumn("Tên Khách Hàng", width="medium"),
    "sdt": st.column_config.TextColumn("Số Điện Thoại", width="small"),
    "diem_so": st.column_config.NumberColumn(
        "Điểm AI",
        help="Thang điểm từ 0 đến 100 theo 5 tiêu chí BANT-SE",
        min_value=0,
        max_value=100,
        step=1,
        width="small"
    ),
    "phan_loai": st.column_config.SelectboxColumn(
        "Phân Loại AI",
        options=["🔥 HOT", "⚡ WARM", "❄️ COLD", "Chưa quét"],
        width="small"
    ),
    "trang_thai_duyet": st.column_config.SelectboxColumn(
        "Trạng Thái Duyệt (Human Action)",
        help="Con người duyệt trạng thái để bàn giao Sales hoặc loại bỏ",
        options=[
            "Chưa duyệt",
            "✅ Đã duyệt - Giao Sales",
            "⚡ Cần xác minh thêm",
            "⛔ Từ chối / Blacklist",
            "Chưa duyệt (Gợi ý: Duyệt Giao Sales)",
            "Chưa duyệt (Gợi ý: Blacklist/Lọc bỏ)"
        ],
        width="medium",
        required=True
    ),
    "nhu_cau_mo_ta": st.column_config.TextColumn("Nhu Cầu Mô Tả Gốc", width="large", disabled=True),
    "ly_do_ai": st.column_config.TextColumn("Lý Do & Dấu Hiệu AI Bắt Được", width="large", disabled=True),
    "goi_y_sales": st.column_config.TextColumn("Kịch Bản Gợi Ý Cho Sales", width="large", disabled=True),
    "ghi_chu_sales": st.column_config.TextColumn("Ghi Chú Của Người Duyệt / Sales", width="medium")
}

# Chọn các cột để hiển thị trên data_editor
display_cols = [
    "id", "ten_khach", "sdt", "diem_so", "phan_loai", 
    "trang_thai_duyet", "ghi_chu_sales", "ly_do_ai", "goi_y_sales", "nhu_cau_mo_ta"
]
# Bổ sung các cột nếu thiếu
for col in display_cols:
    if col not in filtered_df.columns:
        filtered_df[col] = ""

edited_df = st.data_editor(
    filtered_df[display_cols],
    column_config=column_config,
    use_container_width=True,
    num_rows="dynamic",
    height=420,
    key="lead_data_editor"
)

# Nút lưu thay đổi từ editor vào state
col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 4])

with col_btn1:
    if st.button("💾 Lưu Thay Đổi Duyệt", type="primary", use_container_width=True):
        # Cập nhật ngược lại session_state.leads_df dựa trên ID
        main_df = st.session_state.leads_df.set_index("id")
        updated_sub = edited_df.set_index("id")
        main_df.update(updated_sub)
        st.session_state.leads_df = main_df.reset_index()
        st.success("Đã lưu thành công các thay đổi từ bảng duyệt!")
        st.rerun()

with col_btn2:
    # Xuất file CSV đã duyệt
    csv_buffer = io.StringIO()
    st.session_state.leads_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    st.download_button(
        label="📥 Xuất Báo Cáo CSV",
        data=csv_buffer.getvalue(),
        file_name="Lead_Scoring_Human_Approved.csv",
        mime="text/csv",
        use_container_width=True
    )


# ---------------------------------------------------------------------------
# CHI TIẾT THẺ BÀN GIAO LEAD (LEAD HANDOFF CARD VIEWER)
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📇 Xem Chi Tiết Thẻ Bàn Giao Lead (Lead Handoff Card)")

lead_options = [f"ID #{row['id']} - {row['ten_khach']} ({row['phan_loai']} - {row['diem_so']}đ)" for _, row in filtered_df.iterrows()]

if lead_options:
    selected_option = st.selectbox("Chọn một khách hàng để xem phiếu bàn giao Sales chi tiết:", options=lead_options)
    selected_id = int(selected_option.split(" - ")[0].replace("ID #", ""))
    selected_row = df[df["id"] == selected_id].iloc[0]
    
    tier_class = "tag-hot" if "HOT" in str(selected_row["phan_loai"]) else ("tag-warm" if "WARM" in str(selected_row["phan_loai"]) else "tag-cold")
    
    st.markdown(f"""
    <div class="handoff-box">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 14px;">
            <div>
                <span style="font-size: 1.3rem; font-weight: 700; color: #0F172A;">{selected_row['ten_khach']}</span>
                <span style="margin-left: 12px; font-size: 1.1rem; color: #2563EB; font-weight: 600;">📞 {selected_row['sdt']}</span>
            </div>
            <div>
                <span class="{tier_class}">{selected_row['phan_loai']}</span>
                <span style="margin-left: 10px; font-size: 1.2rem; font-weight: 700; color: #1E293B;">Điểm AI: {selected_row['diem_so']}/100</span>
                <span style="margin-left: 12px; background: #E0E7FF; color: #3730A3; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.85rem;">Trạng thái: {selected_row['trang_thai_duyet']}</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <h5 style="margin: 0 0 6px 0; color: #475569;">🎯 Nhu Cầu Gốc Của Khách:</h5>
                <p style="background: #FFFFFF; padding: 12px; border-radius: 6px; border: 1px solid #E2E8F0; color: #1E293B; line-height: 1.5;">
                    "{selected_row['nhu_cau_mo_ta']}"
                </p>
                <h5 style="margin: 12px 0 6px 0; color: #475569;">🧠 Phân Tích Logic & Bằng Chứng AI:</h5>
                <p style="background: #EFF6FF; padding: 12px; border-radius: 6px; border: 1px solid #BFDBFE; color: #1E40AF; line-height: 1.5;">
                    {selected_row['ly_do_ai']}
                </p>
            </div>
            <div>
                <h5 style="margin: 0 0 6px 0; color: #059669;">🔑 Kịch Bản Mở Lời Đề Xuất (Sales Icebreaker Hook):</h5>
                <p style="background: #ECFDF5; padding: 12px; border-radius: 6px; border: 1px solid #A7F3D0; color: #065F46; line-height: 1.5; font-weight: 500;">
                    {selected_row['goi_y_sales']}
                </p>
                <h5 style="margin: 12px 0 6px 0; color: #475569;">⏱️ Cam Kết Thời Gian Phản Hồi (SLA):</h5>
                <p style="background: #FFFBEB; padding: 10px; border-radius: 6px; border: 1px solid #FDE68A; color: #92400E; font-weight: 600;">
                    {"Gọi trong vòng ≤ 15 phút (Golden 15 Minutes)" if "HOT" in str(selected_row['phan_loai']) else ("Liên hệ trong vòng ≤ 2-4 giờ" if "WARM" in str(selected_row['phan_loai']) else "Drip Marketing tự động / Không phân bổ Sales")}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Không có khách hàng nào phù hợp với bộ lọc hiện tại.")


# ---------------------------------------------------------------------------
# FOOTER BẢN QUYỀN
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.82rem; padding: 15px 0;">
    Phát triển bởi <b>Phạm Minh Hoàng</b> — Khóa học <i>Agentic AI with Google Antigravity</i> • Cố vấn: <b>MT Đức Thuận</b> (AI4A)<br>
    Tuân thủ quy chuẩn bảo mật PII Nghị định 13/2023/NĐ-CP & Mô hình Human-In-The-Loop
</div>
""", unsafe_allow_html=True)
