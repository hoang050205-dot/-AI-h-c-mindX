# BÁO CÁO THẨM ĐỊNH BỘ CHỨNG TỪ XUẤT NHẬP KHẨU (v3.0 PRO)
> **Mã Lô Hàng:** `SHP-2026-KR-VN-001` | **Mặt Hàng:** Dây chuyền chiết rót và đóng nắp chai tự động (Automatic Liquid Filling and Capping Line)
> **Thời Điểm Kiểm Toán:** 02/10/2026 22:48:00 | **Chuyên Viên:** Documentation Audit Specialist
> **Khung Nghiệp Vụ:** Hệ thống 5 Lớp Kiểm Soát & Danh Mục Toàn Diện 36 Bẫy Lỗi Thực Chiến
> **Chỉ Số An Toàn (Risk Score):** `10/100 Điểm`

---

## 1. TỔNG QUAN TÍNH HỢP LỆ (STATUS OVERVIEW)

### **Đánh giá chung:** `[CẢNH BÁO - CÓ SAI LỆCH CẦN SỬA TRƯỚC KHI TRUYỀN TỜ KHAI]`

- **Điểm an toàn hồ sơ:** `10 / 100`.
- **Tổng số điểm sai lệch phát hiện:** `7` lỗi (Cần xử lý trước khi truyền tờ khai).
- **Tổng số hạng mục đối soát đạt chuẩn:** `23` tiêu chí.

### **Tóm tắt rủi ro then chốt:**
1. **[L1-02] Vận đơn xếp hàng trước ngày phát hành Hóa đơn** (`CRITICAL`): Hàng hóa đã xếp lên tàu vận chuyển trước khi xuất hóa đơn thương mại. Hồ sơ đối phó, nguy cơ chuyển luồng Đỏ kiểm hóa 10...
2. **[L1-03] C/O cấp sau ngày tàu chạy quá 3 ngày thiếu tích Retroactive** (`CRITICAL`): Vi phạm quy tắc cấp C/O hồi tố của Hiệp định thương mại tự do (FTA). Hải quan cửa khẩu sẽ BÁC BỎ C/O ngay lập tức, truy ...
3. **[L2-03] Bất nhất ký tự địa chỉ Người nhận hàng (Consignee Address)** (`MEDIUM`): Lỗi đánh máy địa chỉ trên vận đơn so với ĐKKD; Hải quan có thể nghi ngờ sai địa chỉ trụ sở hoặc từ chối tính hợp lệ của ...
4. **[L3-02] Sai lệch Tổng trọng lượng Gross Weight giữa PL và B/L (Lệch 400.00 KGS)** (`CRITICAL`): Lệch Manifest cổng Một cửa quốc gia (NSW). Phạt tiền đối với hành vi khai sai so với thực tế về lượng, trọng lượng trên ...
5. **[L4-01] Phép tính Thành tiền Dòng 2 (Automatic Bottle Feeding & Cap...)** (`CRITICAL`): Sai số học trên hóa đơn thương mại. VNACCS sẽ báo lỗi không khớp trị giá tính thuế hoặc bị nghi ngờ gian lận trị giá. Sa...
6. **[L4-03] Tổng trị giá hóa đơn so với Hợp đồng ngoại thương** (`HIGH`): Tổng giá trị thanh toán trên Invoice không khớp với Hợp đồng. Ngân hàng từ chối chuyển tiền T/T hoặc thanh toán L/C theo...
7. **[L4-04] Phân nhóm mã HS 6 số giữa Hóa đơn thương mại và C/O** (`CRITICAL`): Bất nhất mã HS giữa C/O và Bộ chứng từ. Hải quan từ chối áp dụng thuế suất ưu đãi đặc biệt (0%), tạm giữ C/O để xác minh...

---

## 2. MA TRẬN PHÁT HIỆN SAI LỆCH (DISCREPANCY & ERROR MATRIX)

| STT | Mã Lỗi | Cấp độ | Tiêu chí đối soát | Chứng từ A (Thực tế) | Chứng từ B (Thực tế) | Rủi ro pháp lý & Chế tài NĐ 128 | Đề xuất khắc phục |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `L1-02` | **CRITICAL** | Vận đơn xếp hàng trước ngày phát hành Hóa đơn | *Commercial Invoice Date: 08/09/2026* | *B/L On-board Date: 05/09/2026* | Hàng hóa đã xếp lên tàu vận chuyển trước khi xuất hóa đơn thương mại. Hồ sơ đối phó, nguy cơ chuyển luồng Đỏ kiểm hóa 100%. | Yêu cầu Shipper thu hồi và phát hành lại Invoice trước hoặc trùng ngày tàu chạy (05/09/2026). |
| **2** | `L1-03` | **CRITICAL** | C/O cấp sau ngày tàu chạy quá 3 ngày thiếu tích Retroactive | *C/O Date: 12/09/2026 (Sau B/L 7 ngày)* | *Ô số 13 C/O: Chưa đánh dấu '[x] ISSUED RETROACTIVELY'* | Vi phạm quy tắc cấp C/O hồi tố của Hiệp định thương mại tự do (FTA). Hải quan cửa khẩu sẽ BÁC BỎ C/O ngay lập tức, truy thu thuế MFN. | 1) Đề nghị Shipper xin cơ quan cấp xuất xứ cấp lại C/O có tích chọn ô 'ISSUED RETROACTIVELY'.<br>2) Khai báo xin NỢ C/O trong vòng 30 ngày trên VNACCS (Thông tư 38/2015 & TT 121/2025/TT-BTC) để thông quan trước. |
| **3** | `L2-03` | **MEDIUM** | Bất nhất ký tự địa chỉ Người nhận hàng (Consignee Address) | *Hợp đồng / Hóa đơn: 'So 45 Duong Tam Trinh, Phuong Mai Dong, Quan Hoang Mai, Ha Noi, Vietnam'* | *Vận đơn B/L: 'So 45 Duong Tam Trinh, Phuong Mai Dong, Quan Haong Mai, Ha Noi, Vietnam' (Sai lệch 2 ký tự)* | Lỗi đánh máy địa chỉ trên vận đơn so với ĐKKD; Hải quan có thể nghi ngờ sai địa chỉ trụ sở hoặc từ chối tính hợp lệ của C/O. | 1) Làm Công văn giải trình lỗi đánh máy do Hãng tàu lập gửi Chi cục Hải quan.<br>2) Đề nghị Hãng tàu sửa Manifest trên Cổng NSW và cấp Giấy đính chính. |
| **4** | `L3-02` | **CRITICAL** | Sai lệch Tổng trọng lượng Gross Weight giữa PL và B/L (Lệch 400.00 KGS) | *Packing List: 18,450.00 KGS* | *Bill of Lading: 18,050.00 KGS (Lệch 400.00 KGS)* | Lệch Manifest cổng Một cửa quốc gia (NSW). Phạt tiền đối với hành vi khai sai so với thực tế về lượng, trọng lượng trên bản lược khai hàng hóa (Manifest); nguy cơ chuyển luồng Đỏ kiểm hóa 100%. Căn cứ: Điều 7 hoặc Điều 8 Nghị định 128/2020/NĐ-CP (1.000.000đ - 3.000.000đ). | 1) Yêu cầu Đại lý Hãng tàu (KMTC INCHEON V.2608S) gửi điện đính chính Manifest trên Cổng NSW sửa thành 18,450.00 KGS.<br>2) Đề nghị Hãng tàu cấp Giấy đính chính Vận đơn (B/L Correction). |
| **5** | `L4-01` | **CRITICAL** | Phép tính Thành tiền Dòng 2 (Automatic Bottle Feeding & Cap...) | *Phép tính đúng: 1 x $25,000.00 = $25,000.00* | *Ghi trên Invoice: $23,000.00 (Lệch $2,000.00)* | Sai số học trên hóa đơn thương mại. VNACCS sẽ báo lỗi không khớp trị giá tính thuế hoặc bị nghi ngờ gian lận trị giá. Sai lệch số học trị giá hải quan làm thiếu số tiền thuế phải nộp; bị ấn định thuế và xử phạt hành chính 20% theo quy định. | Yêu cầu Shipper sửa lại Commercial Invoice: Sửa thành tiền Dòng 2 thành $25,000.00 và cập nhật lại Tổng hóa đơn. |
| **6** | `L4-03` | **HIGH** | Tổng trị giá hóa đơn so với Hợp đồng ngoại thương | *Commercial Invoice Total: $113,000.00* | *Sales Contract Total: $115,000.00* | Tổng giá trị thanh toán trên Invoice không khớp với Hợp đồng. Ngân hàng từ chối chuyển tiền T/T hoặc thanh toán L/C theo UCP 600. | Phát hành lại Commercial Invoice khớp chính xác số tiền $115,000.00 với Hợp đồng ngoại thương. |
| **7** | `L4-04` | **CRITICAL** | Phân nhóm mã HS 6 số giữa Hóa đơn thương mại và C/O | *Commercial Invoice: 8479.89* | *C/O Ô số 8: 8479.90 (Khác 6 số đầu)* | Bất nhất mã HS giữa C/O và Bộ chứng từ. Hải quan từ chối áp dụng thuế suất ưu đãi đặc biệt (0%), tạm giữ C/O để xác minh xuất xứ kéo dài 2-6 tháng. Phạt 20% tính trên số tiền thuế khai thiếu do áp sai mã số HS hoặc bị bác ưu đãi C/O, cộng tiền chậm nộp 0.03%/ngày theo Điều 9 NĐ 128. | 1) Đề nghị Shipper liên hệ cơ quan cấp xuất xứ (Korea Chamber of Commerce and Industry (KCCI)) cấp lại C/O với mã HS chuẩn 8479.89.<br>2) Khai báo NỢ C/O trong vòng 30 ngày (TT 38/2015 & TT 121/2025/TT-BTC) để giải phóng hàng trước.<br>3) Kích hoạt 'customs-hs-classifier' để thẩm định và tính Tax Delta. |

---

## 3. DANH MỤC TIÊU CHÍ ĐÃ ĐỐI SOÁT HỢP LỆ (VERIFIED CHECKLIST)

- [x] **Trình tự thời gian:** Invoice Date (08/09/2026) >= Contract Date (15/08/2026) [ĐẠT - L1-01]
- [x] **Hiệu lực C/O:** C/O còn hiệu lực trong vòng 12 tháng kể từ ngày cấp [ĐẠT - L1-04]
- [x] **Bảo hiểm hàng hải:** Insurance Date <= B/L Date hợp lệ theo Incoterms [ĐẠT - L1-05]
- [x] **Thời gian đóng gói:** PL Date <= B/L Date [ĐẠT - L1-06]
- [x] **Tên Shipper:** Tên Shipper đồng nhất giữa Contract và B/L [ĐẠT - L2-01]
- [x] **Tên Consignee:** Tên Consignee đồng nhất trên các chứng từ [ĐẠT - L2-01]
- [x] **Mã số thuế (Tax ID):** Mã số thuế [0109876543] đồng nhất giữa Contract và Invoice [ĐẠT - L2-04]
- [x] **Cảng xếp hàng (POL):** Cảng POL (Busan Port, Korea) đồng nhất trên các chứng từ [ĐẠT - L2-07]
- [x] **Cảng dỡ hàng (POD):** Cảng POD (Cat Lai Port, Ho Chi Minh City, Vietnam) đồng nhất trên các chứng từ [ĐẠT - L2-07]
- [x] **Tỷ lệ trọng lượng:** PL Gross Weight (18,450.00 KGS) >= Net Weight (16,800.00 KGS) [ĐẠT - L3-01]
- [x] **Số lượng kiện:** Khớp chính xác 8 kiện hàng giữa PL và B/L [ĐẠT - L3-03]
- [x] **Đơn vị tính (UOM):** Đơn vị tính đồng nhất (SET) [ĐẠT - L3-04]
- [x] **Số Container:** Container No. [KMTU7894561] khớp 100% giữa PL và B/L [ĐẠT - L3-05]
- [x] **Số Chì (Seal):** Seal No. [KMTC88921] khớp 100% giữa PL và B/L [ĐẠT - L3-05]
- [x] **Hun trùng ISPM 15:** Bao bì kiện gỗ [WOODEN CASES] đạt chuẩn quốc tế ISPM 15 [ĐẠT - L3-06]
- [x] **Thể tích khối (CBM):** Khớp 48.50 CBM giữa PL và B/L [ĐẠT - L3-07]
- [x] **Cộng dồn Subtotal:** Tổng cộng các dòng khớp chính xác $113,000.00 [ĐẠT - L4-02]
- [x] **Điều kiện Incoterms:** Incoterms 2020 thể hiện đầy đủ điều kiện và nơi đến (CIF CAT LAI PORT, HO CHI MINH CITY, VIETNAM INCOTERMS 2020) [ĐẠT - L4-05]
- [x] **Bóc tách chi phí:** Điều kiện CIF/CFR đã bao gồm trọn gói cước biển và bảo hiểm theo tập quán quốc tế [ĐẠT - L4-06]
- [x] **Đồng tiền thanh toán:** Đồng tiền [USD] đồng nhất giữa Contract và Invoice [ĐẠT - L4-08]
- [x] **Tiêu chí xuất xứ C/O:** Tiêu chí xuất xứ [CTH] ghi nhận chuẩn xác theo FTA [ĐẠT - L5-01]
- [x] **Thủ tục Nợ C/O:** Đủ điều kiện áp dụng cơ chế Khai Nợ C/O trong vòng 30 ngày theo Thông tư 38/2015 và TT 121/2025/TT-BTC để giải phóng hàng [ĐẠT - L5-04]
- [x] **Tra cứu Chế tài NĐ 128:** Ước tính rủi ro chế tài xử phạt nếu không khắc phục: Phạt 20% số thuế thiếu + Tiền chậm nộp 0.03%/ngày (Điều 9 NĐ 128) [TỰ ĐỘNG - L5-05]

---

## 4. LỘ TRÌNH HÀNH ĐỘNG 3 NHÓM ĐỐI TÁC TRƯỚC KHI TRUYỀN TỜ KHAI

### 4.1. Hành động với Nhà xuất khẩu / Shipper (`HANSUNG TECH CO., LTD.`)
1. Yêu cầu Shipper sửa lại Commercial Invoice: Sửa thành tiền Dòng 2 thành $25,000.00 và cập nhật lại Tổng hóa đơn.
2. 1) Đề nghị Shipper liên hệ cơ quan cấp xuất xứ (Korea Chamber of Commerce and Industry (KCCI)) cấp lại C/O với mã HS chuẩn 8479.89.
3. Phát hành lại Commercial Invoice khớp chính xác số tiền $115,000.00 với Hợp đồng ngoại thương.
4. Yêu cầu Shipper thu hồi và phát hành lại Invoice trước hoặc trùng ngày tàu chạy (05/09/2026).
5. 1) Đề nghị Shipper xin cơ quan cấp xuất xứ cấp lại C/O có tích chọn ô 'ISSUED RETROACTIVELY'.

### 4.2. Hành động với Hãng tàu / Đại lý Giao nhận (`KMTC INCHEON V.2608S`)
1. 1) Làm Công văn giải trình lỗi đánh máy do Hãng tàu lập gửi Chi cục Hải quan.
2) Đề nghị Hãng tàu sửa Manifest trên Cổng NSW và cấp Giấy đính chính.
2. 1) Yêu cầu Đại lý Hãng tàu (KMTC INCHEON V.2608S) gửi điện đính chính Manifest trên Cổng NSW sửa thành 18,450.00 KGS.
2) Đề nghị Hãng tàu cấp Giấy đính chính Vận đơn (B/L Correction).

### 4.3. Phương án xử lý của Người khai Hải quan tại (`Cat Lai Port, Ho Chi Minh City, Vietnam`)
1. 1) Đề nghị Shipper xin cơ quan cấp xuất xứ cấp lại C/O có tích chọn ô 'ISSUED RETROACTIVELY'.
2) Khai báo xin NỢ C/O trong vòng 30 ngày trên VNACCS (Thông tư 38/2015 & TT 121/2025/TT-BTC) để thông quan trước.
2. 1) Đề nghị Shipper liên hệ cơ quan cấp xuất xứ (Korea Chamber of Commerce and Industry (KCCI)) cấp lại C/O với mã HS chuẩn 8479.89.
2) Khai báo NỢ C/O trong vòng 30 ngày (TT 38/2015 & TT 121/2025/TT-BTC) để giải phóng hàng trước.
3) Kích hoạt 'customs-hs-classifier' để thẩm định và tính Tax Delta.
3. 1) Làm Công văn giải trình lỗi đánh máy do Hãng tàu lập gửi Chi cục Hải quan.
2) Đề nghị Hãng tàu sửa Manifest trên Cổng NSW và cấp Giấy đính chính.