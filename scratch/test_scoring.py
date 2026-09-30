import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"c:\Minh Hoang\Antigravity học\my-workspace")
from app_lead_scoring import ai_score_lead

test_cases = [
    ("Bùi Phương Tâm", "Khách hàng VIP, quan tâm biệt thự đơn lập phân khu cao cấp nhất. Ngân sách trên 30 tỷ, thanh toán thẳng. Yêu cầu vị trí ven sông, hướng Đông Nam. Đã từng mua nhiều dự án của tập đoàn."),
    ("Trần Hoàng Dũng", "Chủ doanh nghiệp lớn, cần tìm quỹ đất công nghiệp hoặc sàn văn phòng diện tích trên 2000m2 tại khu Đông. Tài chính cực mạnh, yêu cầu pháp lý chuẩn 100%."),
    ("Lý Đức Cường", "Quan tâm căn hộ 2PN tại Quận 7 cho gia đình trẻ. Tài chính khoảng 4-5 tỷ, cần hỗ trợ vay ngân hàng 70%. Muốn đi xem nhà mẫu vào cuối tuần này."),
    ("Ngô Anh Mai", "Tìm nhà phố liền kề khu vực nội thành, ưu tiên gần trường học và bệnh viện. Ngân sách 8-10 tỷ. Đang cân nhắc giữa 2 dự án, cần tư vấn thêm về chính sách chiết khấu."),
    ("Hồ Phương Mai", "Hỏi giá cho vui, chưa có ý định mua trong năm nay. Ngân sách rất thấp so với mặt bằng chung (đòi mua nhà Q1 giá 1 tỷ)."),
    ("Hồ Đức Lan", "Spam, gọi điện đến chỉ để quảng cáo ngược lại dịch vụ bảo hiểm."),
    ("Đặng Hoàng Dũng", "Số điện thoại hay bị thuê bao, gọi nhiều lần không bắt máy. Nhắn tin Zalo không phản hồi."),
]

print("=== KIỂM THỬ AI SCORING LOGIC ===")
for name, desc in test_cases:
    res = ai_score_lead(desc, name)
    print(f"\n[{name}] -> Điểm: {res['diem_so']} | Phân loại: {res['phan_loai']}")
    print(f"  Lý do: {res['ly_do_ai']}")
    print(f"  Gợi ý Sales: {res['goi_y_sales']}")
