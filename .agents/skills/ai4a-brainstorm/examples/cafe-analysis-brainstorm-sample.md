# Ví Dụ Mẫu: Brainstorm Brief Phân Tích Quán Cafe Quận 1 (AI4A)

**Dự án:** Phân loại và Xây dựng Dashboard Thị Trường Cà Phê Quận 1 cho Khách Hàng Làm Việc Từ Xa  
**Học viên:** Minh Hoàng  
**Mentor:** MT Đức Thuận  
**Khung tham chiếu:** AI4A Brainstorm Contract (`ai4a:brainstorm`)  
**Ngày thực hiện:** 09/09/2026  

---

## 1. Bản Hợp Đồng Thực Thi (The 4-Field Contract)

| Trường Hợp Đồng | Định Nghĩa & Ranh Giới Cụ Thể |
|---|---|
| **🎯 Outcome** | File bảng tính Excel chuẩn hóa (`outputs/reports/Quan_Cafe_Quan_1_Cleaned.xlsx`) chứa 22 bản ghi, Executive Dashboard tự động hiển thị đúng giá trị mà không bị lỗi số 0, kèm báo cáo tóm tắt insight kinh doanh. |
| **🛡️ Constraints** | - Địa bàn khảo sát: Giới hạn nghiêm ngặt trong 7 phường trọng điểm Quận 1.<br>- Giá tiền: Phải tách thành 3 cột số nguyên (`PRICE_MIN_VND`, `PRICE_MAX_VND`, `PRICE_AVG_VND`) dạng integer để tính toán được.<br>- Bảo mật: Không lưu số điện thoại cá nhân hay thông tin nhạy cảm của khách hàng. |
| **🚫 Non-goals** | - Không crawl dữ liệu bình luận chi tiết theo thời gian thực.<br>- Không tích hợp cổng đặt bàn hay đặt đồ uống trực tuyến.<br>- Không mở rộng sang các quận khác trong chu kỳ này. |
| **✅ Acceptance Criteria** | - Đủ tối thiểu 15-20 quán (thực tế 22 quán đạt chuẩn).<br>- Tỷ lệ trùng lặp: **0%**.<br>- Điểm Google Rating: 100% nằm trong khoảng từ 4.0 đến 5.0.<br>- File mở được mượt mà trên cả Excel Desktop, Web và WPS Office. |

---

## 2. So Sánh Các Phương Án Kỹ Thuật (Option Exploration)

### Approach 1 (Lean / Direct): Script Python openpyxl đơn lẻ
- **Khái niệm:** Dùng 1 kịch bản Python (`sample-data/build_cafe_dataset.py`) chứa dữ liệu đã thẩm định, định dạng trực tiếp các ô và ghi kèm giá trị số thực (pre-calculated values) vào Dashboard.
- **Ưu điểm:** Triển khai nhanh trong 1 giờ, 0 chi phí API, chạy offline hoàn toàn độc lập.
- **Nhược điểm:** Phải cập nhật thủ công danh sách quán khi có địa điểm mới.
- **Giả định cốt lõi:** Schema 16 trường không thay đổi trong suốt quá trình tạo workbook.
- **Điểm gãy đầu tiên:** Thêm quán mới nhưng nhập sai kiểu dữ liệu trường giá tiền.

### Approach 2 (Workflow / Agentic): Pipeline 2 Tác tử (Crawler Agent + Analyst Agent)
- **Khái niệm:** Agent 1 tìm kiếm và chuẩn hóa dữ liệu trên mạng $\rightarrow$ Human Checkpoint duyệt danh sách $\rightarrow$ Agent 2 phân tích thị phần và dựng file Excel.
- **Ưu điểm:** Khả năng mở rộng tốt hơn khi cần thêm quán hoặc cập nhật định kỳ hàng tháng.
- **Nhược điểm:** Tốn token, cần thiết kế cấu trúc bàn giao (handoff schema) chặt chẽ giữa 2 agents.
- **Giả định cốt lõi:** Agent 1 trích xuất dữ liệu web chính xác và không bị bot-detection chặn IP.
- **Điểm gãy đầu tiên:** Agent 1 trả về dữ liệu thiếu trường `PRICE_MAX_VND` làm gián đoạn Agent 2.

### Approach 3 (Advanced / Scalable): Hệ Thống Đa Nền Tảng (Google Places API + Postgres + Streamlit)
- **Khái niệm:** Gọi API Google Maps tự động, lưu vào cơ sở dữ liệu và dựng Dashboard tương tác bằng Streamlit/React.
- **Ưu điểm:** Cực kỳ chuyên nghiệp, dữ liệu thời gian thực cho toàn thành phố.
- **Nhược điểm:** Tốn chi phí thẻ tín dụng cho Google API, quá phức tạp so với mục tiêu học tập (Vi phạm nguyên tắc KISS).
- **Giả định cốt lõi:** Có ngân sách duy trì Google Cloud Platform và máy chủ web.
- **Điểm gãy đầu tiên:** Google API hết quota hoặc phát sinh chi phí ngoài tầm kiểm soát.

---

## 3. Quyết Định Kiến Trúc & Khuyến Nghị

- **Lựa chọn:** **Approach 1 (Lean / Direct)** kết hợp cơ chế kiểm soát chất lượng dữ liệu của Buổi 2.
- **Lý do lựa chọn:** Đáp ứng 100% tiêu chí nghiệm thu với chi phí và rủi ro thấp nhất (Cheapest to abandon). Đảm bảo tính ổn định tuyệt đối khi trình chiếu trên lớp học.
- **Hành động tiếp theo:** Cập nhật mục tiêu và kết quả đo lường vào `docs/pdca-log.md` (Cycle #02).
