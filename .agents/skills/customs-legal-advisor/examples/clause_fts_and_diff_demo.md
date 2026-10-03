# VÍ DỤ MINH HỌA: TRA CỨU FTS5 CẤP ĐIỀU/KHOẢN & ĐỐI CHIẾU PHẢ HỆ (v2.0)

---

### TÌNH HUỐNG 1: TRA CỨU NGUYÊN VĂN CẤP ĐIỀU/KHOẢN VỀ e-C/O NĂM 2026

**Câu hỏi người dùng:**
> "Năm 2026 làm thủ tục nhập khẩu có cần phải scan đính kèm C/O điện tử (e-C/O) lên hệ thống VNACCS nữa không?"

**Lệnh thực thi nội bộ của Agent:**
```powershell
python .agents/skills/customs-legal-advisor/scripts/query_legal_clauses.py -q "e-C/O" -d "121/2025"
```

**Phản hồi của Chuyên gia Pháp chế v2.0:**
> Căn cứ theo **Khoản 2 Điều 1 Thông tư số 121/2025/TT-BTC** (sửa đổi Điều 16 Thông tư 38/2015/TT-BTC, có hiệu lực từ ngày 01/02/2026):
> 
> *"Đối với chứng từ chứng nhận xuất xứ điện tử (e-C/O), giấy phép điện tử, chứng thư chuyên ngành đã được cơ quan cấp truyền dữ liệu trực tiếp qua Cổng thông tin một cửa quốc gia (NSW) hoặc Cơ chế một cửa ASEAN (ASW), **người khai hải quan chỉ cần khai báo mã số chứng từ trên tờ khai hải quan, KHÔNG PHẢI NỘP LẠI BẢN SCAN ĐÍNH KÈM**. Cơ quan hải quan tự động kiểm tra, đối soát và thông quan trên hệ thống CNTT thế hệ mới."*
> 
> **Khuyến nghị thực thi:**  
> 1. Kiểm tra trạng thái đã tiếp nhận và lấy Mã số tiếp nhận e-C/O trên Cổng Một cửa Quốc gia (NSW).  
> 2. Điền mã số này vào ô ghi chú tờ khai VNACCS.  
> 3. Không scan đính kèm để tránh trùng lặp dữ liệu và đẩy nhanh tốc độ thông quan luồng Vàng/Xanh.

---

### TÌNH HUỐNG 2: SO SÁNH ĐỐI CHIẾU PHẢ HỆ ĐIỀU 16 (HỒ SƠ HẢI QUAN)

**Câu hỏi người dùng:**
> "So sánh giúp tôi quy định nộp hồ sơ hải quan từ Thông tư 38 đến Thông tư 39 và Thông tư 121/2025 mới nhất có gì khác biệt?"

**Lệnh thực thi nội bộ của Agent:**
```powershell
python .agents/skills/customs-legal-advisor/scripts/diff_legal_clauses.py -k 16 --markdown
```

**Bảng đối chiếu xuất ra:**
| Giai đoạn văn bản | Số hiệu quy chuẩn | Nội dung quy định then chốt |
|:---|:---|:---|
| **1. Quy định gốc** | Thông tư 38/2015/TT-BTC | Cho phép nộp 01 bản chụp có ký tên, đóng dấu xác nhận sao y của doanh nghiệp đối với Hóa đơn, Vận đơn, Packing List. |
| **2. Sửa đổi giai đoạn 1** | Thông tư 39/2018/TT-BTC | Bãi bỏ nộp bản giấy. Chuyển sang nộp 100% bản điện tử scan đính kèm chữ ký số qua VNACCS (V5). Chỉ nộp bản giấy với C/O bản gốc và giấy phép bản chính. |
| **3. Cập nhật mới nhất 2026** | Thông tư 121/2025/TT-BTC | Đối với e-C/O và Giấy phép đã liên thông qua Cổng một cửa quốc gia (NSW/ASW), chỉ cần khai báo mã số chứng từ trên tờ khai, KHÔNG phải nộp lại bản scan đính kèm. |

> ⚡ **Điểm khác biệt mấu chốt:** Bản chụp giấy sao y (2015) ──► Bản scan ký số qua V5 (2018) ──► Tự động đối soát mã điện tử NSW không cần scan (2026).  
> ⚠️ **Bẫy rủi ro:** Vẫn in bản giấy mang ra Chi cục Hải quan nộp (bị từ chối tiếp nhận vì vi phạm thủ tục hải quan điện tử); hoặc scan đính kèm trùng lặp chứng từ đã có trên NSW gây nghẽn đường truyền.

---

### TÌNH HUỐNG 3: TRA CỨU CHẾ TÀI XỬ PHẠT KHAI THIẾU THUẾ (NGHỊ ĐỊNH 128/2020)

**Câu hỏi người dùng:**
> "Doanh nghiệp khai nhầm mã thuế suất VAT 8% cho linh kiện kim loại nằm trong Phụ lục I loại trừ, nếu Hải quan phát hiện thì bị xử phạt như thế nào?"

**Lệnh thực thi nội bộ của Agent:**
```powershell
python .agents/skills/customs-legal-advisor/scripts/query_legal_clauses.py -a "Điều 9" -d "128/2020"
```

**Phản hồi của Chuyên gia Pháp chế v2.0:**
> Căn cứ theo **Khoản 2 Điều 9 Nghị định số 128/2020/NĐ-CP** (sửa đổi bởi Nghị định 102/2021/NĐ-CP):
> 
> 1. **Khung xử phạt tiền:** Phạt **20% tính trên số tiền thuế khai thiếu** (khoản chênh lệch giữa mức thuế suất đúng 10% và mức đã khai 8%).  
> 2. **Tiền thuế truy thu & tiền chậm nộp:** Doanh nghiệp buộc phải nộp đủ 100% số tiền thuế khai thiếu vào Ngân sách Nhà nước cộng với tiền chậm nộp tính theo mức **0.03%/ngày** trên số tiền thuế chậm nộp (Luật Quản lý thuế).  
> 3. **Rủi ro phân luồng:** Doanh nghiệp sẽ bị ghi nhận lỗi trên CSDL Quản lý rủi ro của Tổng cục Hải quan, có thể bị hạ mức xếp hạng tuân thủ và chuyển sang luồng Vàng hoặc luồng Đỏ cho các lô hàng kế tiếp.  
> 
> **Hành động khắc phục khẩn cấp:**  
> Nếu cơ quan hải quan **chưa lập biên bản vi phạm hành chính**, doanh nghiệp cần chủ động nộp ngay tờ khai bổ sung AMA/AMC và nộp đủ số tiền thuế thiếu vào kho bạc để được giảm mức phạt xuống **10%** theo quy định tại Khoản 1 Điều 9 NĐ 128/2020!
