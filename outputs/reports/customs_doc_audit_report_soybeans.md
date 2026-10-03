# BÁO CÁO THẨM ĐỊNH BỘ CHỨNG TỪ XUẤT NHẬP KHẨU (v3.0 PRO)
> **Mã Lô Hàng:** `SHP-2026-US-VN-SOY88` | **Mặt Hàng:** Hạt đậu tương vàng nguyên hạt chưa bóc vỏ dùng làm thức ăn chăn nuôi (Yellow Soybeans in Bulk)
> **Thời Điểm Kiểm Toán:** 02/10/2026 22:49:05 | **Chuyên Viên:** Documentation Audit Specialist
> **Khung Nghiệp Vụ:** Hệ thống 5 Lớp Kiểm Soát & Danh Mục Toàn Diện 36 Bẫy Lỗi Thực Chiến
> **Chỉ Số An Toàn (Risk Score):** `45/100 Điểm`

---

## 1. TỔNG QUAN TÍNH HỢP LỆ (STATUS OVERVIEW)

### **Đánh giá chung:** `[CẢNH BÁO - CÓ SAI LỆCH CẦN SỬA TRƯỚC KHI TRUYỀN TỜ KHAI]`

- **Điểm an toàn hồ sơ:** `45 / 100`.
- **Tổng số điểm sai lệch phát hiện:** `4` lỗi (Cần xử lý trước khi truyền tờ khai).
- **Tổng số hạng mục đối soát đạt chuẩn:** `24` tiêu chí.

### **Tóm tắt rủi ro then chốt:**
1. **[L1-01] Hóa đơn phát hành trước Hợp đồng ngoại thương** (`CRITICAL`): Nghiệp vụ bất hợp lý; Hải quan nghi ngờ hợp đồng đối phó hoặc làm khống, dẫn tới nguy cơ thanh tra sau thông quan....
2. **[L3-02] Sai lệch Tổng trọng lượng Gross Weight giữa PL và B/L (Lệch 1,500.00 KGS)** (`CRITICAL`): Lệch Manifest cổng Một cửa quốc gia (NSW). Phạt tiền đối với hành vi khai sai so với thực tế về lượng, trọng lượng trên ...
3. **[L4-01] Phép tính Thành tiền Dòng 1 (US Yellow Soybeans Grade 2 or ...)** (`CRITICAL`): Sai số học trên hóa đơn thương mại. VNACCS sẽ báo lỗi không khớp trị giá tính thuế hoặc bị nghi ngờ gian lận trị giá. Sa...
4. **[L4-03] Tổng trị giá hóa đơn so với Hợp đồng ngoại thương** (`HIGH`): Tổng giá trị thanh toán trên Invoice không khớp với Hợp đồng. Ngân hàng từ chối chuyển tiền T/T hoặc thanh toán L/C theo...

---

## 2. MA TRẬN PHÁT HIỆN SAI LỆCH (DISCREPANCY & ERROR MATRIX)

| STT | Mã Lỗi | Cấp độ | Tiêu chí đối soát | Chứng từ A (Thực tế) | Chứng từ B (Thực tế) | Rủi ro pháp lý & Chế tài NĐ 128 | Đề xuất khắc phục |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `L1-01` | **CRITICAL** | Hóa đơn phát hành trước Hợp đồng ngoại thương | *Invoice Date: 10/09/2026* | *Contract Date: 15/09/2026* | Nghiệp vụ bất hợp lý; Hải quan nghi ngờ hợp đồng đối phó hoặc làm khống, dẫn tới nguy cơ thanh tra sau thông quan. | Yêu cầu Shipper điều chỉnh lại ngày phát hành Commercial Invoice bằng hoặc sau ngày ký kết hợp đồng. |
| **2** | `L3-02` | **CRITICAL** | Sai lệch Tổng trọng lượng Gross Weight giữa PL và B/L (Lệch 1,500.00 KGS) | *Packing List: 500,000.00 KGS* | *Bill of Lading: 498,500.00 KGS (Lệch 1,500.00 KGS)* | Lệch Manifest cổng Một cửa quốc gia (NSW). Phạt tiền đối với hành vi khai sai so với thực tế về lượng, trọng lượng trên bản lược khai hàng hóa (Manifest); nguy cơ chuyển luồng Đỏ kiểm hóa 100%. Căn cứ: Điều 7 hoặc Điều 8 Nghị định 128/2020/NĐ-CP (1.000.000đ - 3.000.000đ). | 1) Yêu cầu Đại lý Hãng tàu (MV OCEAN PIONEER V.2610N) gửi điện đính chính Manifest trên Cổng NSW sửa thành 500,000.00 KGS.<br>2) Đề nghị Hãng tàu cấp Giấy đính chính Vận đơn (B/L Correction). |
| **3** | `L4-01` | **CRITICAL** | Phép tính Thành tiền Dòng 1 (US Yellow Soybeans Grade 2 or ...) | *Phép tính đúng: 500 x $540.00 = $270,000.00* | *Ghi trên Invoice: $260,000.00 (Lệch $10,000.00)* | Sai số học trên hóa đơn thương mại. VNACCS sẽ báo lỗi không khớp trị giá tính thuế hoặc bị nghi ngờ gian lận trị giá. Sai lệch số học trị giá hải quan làm thiếu số tiền thuế phải nộp; bị ấn định thuế và xử phạt hành chính 20% theo quy định. | Yêu cầu Shipper sửa lại Commercial Invoice: Sửa thành tiền Dòng 1 thành $270,000.00 và cập nhật lại Tổng hóa đơn. |
| **4** | `L4-03` | **HIGH** | Tổng trị giá hóa đơn so với Hợp đồng ngoại thương | *Commercial Invoice Total: $260,000.00* | *Sales Contract Total: $270,000.00* | Tổng giá trị thanh toán trên Invoice không khớp với Hợp đồng. Ngân hàng từ chối chuyển tiền T/T hoặc thanh toán L/C theo UCP 600. | Phát hành lại Commercial Invoice khớp chính xác số tiền $270,000.00 với Hợp đồng ngoại thương. |

---

## 3. DANH MỤC TIÊU CHÍ ĐÃ ĐỐI SOÁT HỢP LỆ (VERIFIED CHECKLIST)

- [x] **Trình tự thời gian:** B/L On-board Date >= Invoice Date [ĐẠT - L1-02]
- [x] **Trình tự thời gian C/O:** C/O cấp trong thời hạn 3 ngày chuẩn (22/09/2026) [ĐẠT - L1-03]
- [x] **Hiệu lực C/O:** C/O còn hiệu lực trong vòng 12 tháng kể từ ngày cấp [ĐẠT - L1-04]
- [x] **Thời gian đóng gói:** PL Date <= B/L Date [ĐẠT - L1-06]
- [x] **Tên Shipper:** Tên Shipper đồng nhất giữa Contract và B/L [ĐẠT - L2-01]
- [x] **Tên Consignee:** Tên Consignee đồng nhất trên các chứng từ [ĐẠT - L2-01]
- [x] **Địa chỉ pháp lý:** Địa chỉ Consignee đồng nhất 100% trên các chứng từ [ĐẠT - L2-03]
- [x] **Mã số thuế (Tax ID):** Mã số thuế [0201234567] đồng nhất giữa Contract và Invoice [ĐẠT - L2-04]
- [x] **Cảng xếp hàng (POL):** Cảng POL (New Orleans Port, USA) đồng nhất trên các chứng từ [ĐẠT - L2-07]
- [x] **Cảng dỡ hàng (POD):** Cảng POD (Dinh Vu Port, Hai Phong, Vietnam) đồng nhất trên các chứng từ [ĐẠT - L2-07]
- [x] **Tỷ lệ trọng lượng:** PL Gross Weight (500,000.00 KGS) >= Net Weight (500,000.00 KGS) [ĐẠT - L3-01]
- [x] **Số lượng kiện:** Khớp chính xác 1 kiện hàng giữa PL và B/L [ĐẠT - L3-03]
- [x] **Đơn vị tính (UOM):** Đơn vị tính đồng nhất (MT) [ĐẠT - L3-04]
- [x] **Số Container:** Container No. [BULK-HOLD-01] khớp 100% giữa PL và B/L [ĐẠT - L3-05]
- [x] **Số Chì (Seal):** Seal No. [BULK-NIL] khớp 100% giữa PL và B/L [ĐẠT - L3-05]
- [x] **Thể tích khối (CBM):** Khớp 680.00 CBM giữa PL và B/L [ĐẠT - L3-07]
- [x] **Cộng dồn Subtotal:** Tổng cộng các dòng khớp chính xác $260,000.00 [ĐẠT - L4-02]
- [x] **Mã phân nhóm HS:** Khớp 6 số đầu (120190) giữa Invoice và C/O [ĐẠT - L4-04]
- [x] **Điều kiện Incoterms:** Incoterms 2020 thể hiện đầy đủ điều kiện và nơi đến (CFR DINH VU PORT, HAI PHONG, VIETNAM INCOTERMS 2020) [ĐẠT - L4-05]
- [x] **Bóc tách chi phí:** Điều kiện CIF/CFR đã bao gồm trọn gói cước biển và bảo hiểm theo tập quán quốc tế [ĐẠT - L4-06]
- [x] **Đồng tiền thanh toán:** Đồng tiền [USD] đồng nhất giữa Contract và Invoice [ĐẠT - L4-08]
- [x] **Tiêu chí xuất xứ C/O:** Tiêu chí xuất xứ [WO] ghi nhận chuẩn xác theo FTA [ĐẠT - L5-01]
- [x] **Thủ tục Nợ C/O:** Đủ điều kiện áp dụng cơ chế Khai Nợ C/O trong vòng 30 ngày theo Thông tư 38/2015 và TT 121/2025/TT-BTC để giải phóng hàng [ĐẠT - L5-04]
- [x] **Tra cứu Chế tài NĐ 128:** Ước tính rủi ro chế tài xử phạt nếu không khắc phục: Phạt 20% số thuế thiếu + Tiền chậm nộp 0.03%/ngày (Điều 9 NĐ 128) [TỰ ĐỘNG - L5-05]

---

## 4. LỘ TRÌNH HÀNH ĐỘNG 3 NHÓM ĐỐI TÁC TRƯỚC KHI TRUYỀN TỜ KHAI

### 4.1. Hành động với Nhà xuất khẩu / Shipper (`MIDWEST GRAIN EXPORTERS LLC`)
1. Yêu cầu Shipper điều chỉnh lại ngày phát hành Commercial Invoice bằng hoặc sau ngày ký kết hợp đồng.
2. Phát hành lại Commercial Invoice khớp chính xác số tiền $270,000.00 với Hợp đồng ngoại thương.
3. Yêu cầu Shipper sửa lại Commercial Invoice: Sửa thành tiền Dòng 1 thành $270,000.00 và cập nhật lại Tổng hóa đơn.

### 4.2. Hành động với Hãng tàu / Đại lý Giao nhận (`MV OCEAN PIONEER V.2610N`)
1. 1) Yêu cầu Đại lý Hãng tàu (MV OCEAN PIONEER V.2610N) gửi điện đính chính Manifest trên Cổng NSW sửa thành 500,000.00 KGS.
2) Đề nghị Hãng tàu cấp Giấy đính chính Vận đơn (B/L Correction).

### 4.3. Phương án xử lý của Người khai Hải quan tại (`Dinh Vu Port, Hai Phong, Vietnam`)
- Sẵn sàng bấm nút truyền tờ khai chính thức lên VNACCS.