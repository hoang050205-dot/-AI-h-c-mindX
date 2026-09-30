# BÁO CÁO THẨM ĐỊNH BỘ CHỨNG TỪ XUẤT NHẬP KHẨU

> **Mã Lô Hàng:** `{{shipment_id}}` | **Mặt Hàng:** {{commodity}}  
> **Ngày Thẩm Định:** {{audit_datetime}} | **Chuyên Gia:** Documentation Audit Specialist (customs:doc-auditor)

---

## 1. TỔNG QUAN TÍNH HỢP LỆ (STATUS OVERVIEW)

### **Đánh giá chung:** `[{{status_badge}}]`  
*(Ví dụ: [HỢP LỆ - ĐỦ ĐIỀU KIỆN KHAI HẢI QUAN] hoặc [CẢNH BÁO - CÓ SAI LỆCH CẦN SỬA TRƯỚC KHI TRUYỀN TỜ KHAI])*

- **Tổng số điểm sai lệch phát hiện:** `{{discrepancy_count}}` lỗi.
- **Tổng số hạng mục đối soát đạt chuẩn:** `{{verified_count}}` tiêu chí.
- **Nhận định rủi ro cốt lõi:**
  - {{risk_summary_1}}
  - {{risk_summary_2}}
  - {{risk_summary_3}}

---

## 2. MA TRẬN PHÁT HIỆN SAI LỆCH (DISCREPANCY & ERROR MATRIX)

*(Chỉ hiển thị nếu phát hiện lỗi sai hoặc điểm chưa khớp)*

| STT | Loại lỗi | Hạng mục / Tiêu chí | Chứng từ A (Giá trị thực tế) | Chứng từ B (Giá trị thực tế) | Hậu quả / Rủi ro Hải quan | Đề xuất khắc phục |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **{{error_type_1}}** | {{criterion_1}} | *{{doc_a_1}}* | *{{doc_b_1}}* | {{risk_1}} | {{remedy_1}} |
| **2** | **{{error_type_2}}** | {{criterion_2}} | *{{doc_a_2}}* | *{{doc_b_2}}* | {{risk_2}} | {{remedy_2}} |

---

## 3. DANH MỤC THÔNG TIN ĐÃ ĐỒNG NHẤT (VERIFIED CHECKLIST)

- [x] **Trình tự thời gian:** Contract Date <= Invoice Date <= B/L On-board Date.
- [x] **Thực thể & Địa chỉ:** Tên và địa chỉ Shipper / Consignee / Notify Party đồng nhất.
- [x] **Cảng biển & Hành trình:** Khớp POL, POD và tuyến tàu vận chuyển.
- [x] **Số lượng & Quy cách:** Số kiện và tổng số lượng khớp giữa PL, B/L và C/O.
- [x] **Tỷ lệ trọng lượng:** Gross Weight >= Net Weight; GW trên PL khớp B/L.
- [x] **Số Container & Seal:** Khớp 100% từng ký tự giữa PL và B/L.
- [x] **Đơn giá & Thành tiền:** Phép tính số học chuẩn xác, khớp tổng trị giá Contract.
- [x] **Mã phân nhóm HS Code:** Khớp tối thiểu 6 chữ số giữa Invoice, C/O và dự kiến tờ khai.
- [x] **Điều kiện giao hàng:** Ghi rõ Incoterms 2020 kèm địa điểm quy định.

---

## 4. KHUYẾN NGHỊ CUỐI CÙNG TRƯỚC KHI TRUYỀN TỜ KHAI

### 4.1. Với Shipper / Nhà cung cấp nước ngoài
- {{shipper_actions}}

### 4.2. Với Hãng tàu / Đại lý Giao nhận (Forwarder)
- {{carrier_actions}}

### 4.3. Với Người Khai Hải Quan tại Cửa khẩu
- {{broker_actions}}
