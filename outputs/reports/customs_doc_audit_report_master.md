# BÁO CÁO THẨM ĐỊNH BỘ CHỨNG TỪ XUẤT NHẬP KHẨU
> **Mã Lô Hàng:** `SHP-2026-KR-VN-001` | **Mặt Hàng:** Dây chuyền chiết rót và đóng nắp chai tự động (Automatic Liquid Filling and Capping Line)
> **Ngày Thẩm Định:** 16/09/2026 20:37:06 | **Chuyên Gia:** Documentation Audit Specialist (customs:doc-auditor)
> **Khung Nghiệp Vụ:** Hệ thống 5 Lớp Kiểm Soát & Danh mục 36 Bẫy Lỗi Thực Chiến

---

## 1. TỔNG QUAN TÍNH HỢP LỆ (STATUS OVERVIEW)

### **Đánh giá chung:** `[CẢNH BÁO - CÓ SAI LỆCH CẦN SỬA TRƯỚC KHI TRUYỀN TỜ KHAI]`

- **Tổng số điểm sai lệch phát hiện:** `7` lỗi nghiêm trọng cần xử lý.
- **Tổng số hạng mục đối soát đạt chuẩn:** `15` tiêu chí.
- **Tóm tắt các rủi ro cốt lõi phát hiện:**
  1. **[L1-02] Trình tự Hóa đơn & Vận đơn tàu chạy:** Invoice Date: 08/09/2026 $\leftrightarrow$ B/L On-board Date: 05/09/2026.
  2. **[L1-03] C/O cấp sau ngày tàu chạy (Retroactive Rule):** C/O Issue Date: 12/09/2026 (sau B/L 7 ngày) $\leftrightarrow$ Ô 13: Bỏ trống '[ ] ISSUED RETROACTIVELY'.
  3. **[L2-03] Địa chỉ Người nhận hàng (Consignee Address):** Contract/Invoice/PL: 'Quan Hoang Mai, Ha Noi' $\leftrightarrow$ B/L Consignee Address: 'Quan Haong Mai, Ha Noi'.
  4. **[L3-02] Tổng trọng lượng Gross Weight (GW):** Packing List: 18,450.00 KGS (và C/O: 18,450 KGS) $\leftrightarrow$ Bill of Lading (B/L): 18,050.00 KGS.
  5. **[L4-01] Phép tính Thành tiền Dòng 2 (Automatic Bottle Feeding & Capping ...):** Phép tính đúng: 1 x $25,000.00 = $25,000.00 $\leftrightarrow$ Ghi trên Invoice: $23,000.00 (Lệch $2,000.00).
  6. **[L4-03] Tổng trị giá hóa đơn so với Hợp đồng:** Commercial Invoice Total: $113,000.00 $\leftrightarrow$ Sales Contract Total: $115,000.00.
  7. **[L4-04] Phân nhóm mã HS 6 số giữa Hóa đơn và C/O:** Commercial Invoice: 8479.89 (Máy móc nguyên chiếc) $\leftrightarrow$ C/O Form AK Ô số 8: 8479.90 (Phụ tùng, bộ phận máy).

---

## 2. MA TRẬN PHÁT HIỆN SAI LỆCH (DISCREPANCY & ERROR MATRIX)

| STT | Mã Lỗi | Loại lỗi | Hạng mục / Tiêu chí | Chứng từ A (Giá trị thực tế) | Chứng từ B (Giá trị thực tế) | Hậu quả / Rủi ro Hải quan | Đề xuất khắc phục |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `L1-02` | **Trình tự thời gian** | Trình tự Hóa đơn & Vận đơn tàu chạy | *Invoice Date: 08/09/2026* | *B/L On-board Date: 05/09/2026* | Hóa đơn thương mại xuất sau khi hàng đã bốc lên tàu. Nghiệp vụ giao thương bất hợp lý; Hải quan nghi ngờ hồ sơ giả lập đối phó, nguy cơ chuyển luồng Đỏ kiểm hóa 100%. | Yêu cầu Shipper thu hồi và phát hành lại Commercial Invoice trước hoặc trùng ngày On-board của B/L (trước 05/09/2026). |
| **2** | `L1-03` | **Quy tắc C/O & Thời gian** | C/O cấp sau ngày tàu chạy (Retroactive Rule) | *C/O Issue Date: 12/09/2026 (sau B/L 7 ngày)* | *Ô 13: Bỏ trống '[ ] ISSUED RETROACTIVELY'* | Vi phạm Quy tắc cấp C/O hồi tố của Hiệp định thương mại tự do (FTA). Hải quan cửa khẩu sẽ bác bỏ C/O ngay lập tức, doanh nghiệp bị truy thu thuế MFN. | 1) Đề nghị Shipper liên hệ cơ quan cấp xuất xứ (KCCI) cấp lại C/O Form AK có tích chọn ô 'ISSUED RETROACTIVELY'.<br>2) Khai báo xin NỢ C/O trong vòng 30 ngày trên tờ khai điện tử theo Thông tư 38/2015 và TT 121/2025/TT-BTC để giải phóng hàng trước. |
| **3** | `L2-03` | **Lỗi chính tả / Thực thể** | Địa chỉ Người nhận hàng (Consignee Address) | *Contract/Invoice/PL: 'Quan Hoang Mai, Ha Noi'* | *B/L Consignee Address: 'Quan Haong Mai, Ha Noi'* | Lỗi gõ sai chữ (Typo). Hải quan tiếp nhận có thể từ chối tính hợp lệ của vận đơn so với C/O hoặc tờ khai, có nguy cơ nghi ngờ giao nhầm người nhận hàng. | 1) Làm Công văn cam kết sai sót chính tả do lỗi đánh máy của Hãng tàu gửi Chi cục Hải quan.<br>2) Xin Hãng tàu (KMTC Line) đính chính Manifest điện tử trên Cổng NSW và phát hành B/L sửa đổi. |
| **4** | `L3-02` | **Lệch số liệu trọng lượng** | Tổng trọng lượng Gross Weight (GW) | *Packing List: 18,450.00 KGS (và C/O: 18,450 KGS)* | *Bill of Lading (B/L): 18,050.00 KGS* | Lệch chính xác 400.00 KGS (nguy cơ gõ nhầm hoặc lệch cân cầu cảng). Hải quan cửa khẩu sẽ bắt cân lại tại cổng cảng Cát Lái; sai lệch Manifest trên cổng NSW dẫn đến phạt vi phạm hành chính (Nghị định 128/2020/NĐ-CP) và chuyển luồng Đỏ kiểm hóa. | 1) Liên hệ KMTC Line gửi điện sửa Manifest trên hệ thống Một cửa quốc gia (sửa từ 18,050 thành 18,450 KGS).<br>2) Yêu cầu đại lý hãng tàu phát hành B/L điều chỉnh hoặc cấp Chứng thư đính chính (Certificate of Correction). |
| **5** | `L4-01` | **Số học từng dòng** | Phép tính Thành tiền Dòng 2 (Automatic Bottle Feeding & Capping ...) | *Phép tính đúng: 1 x $25,000.00 = $25,000.00* | *Ghi trên Invoice: $23,000.00 (Lệch $2,000.00)* | Sai lệch số học trên hóa đơn thương mại. Khi truyền tờ khai VNACCS, hệ thống sẽ báo lỗi không khớp trị giá tính thuế hoặc Hải quan kiểm tra hồ sơ giấy nghi ngờ gian lận trị giá. | Yêu cầu Shipper sửa lại Commercial Invoice: Cập nhật lại phép tính đúng của Dòng 2 thành $25,000.00 và tổng giá trị Invoice thành $115,000.00 khớp Hợp đồng. |
| **6** | `L4-03` | **Bất nhất trị giá** | Tổng trị giá hóa đơn so với Hợp đồng | *Commercial Invoice Total: $113,000.00* | *Sales Contract Total: $115,000.00* | Tổng trị giá thanh toán trên Invoice ($113,000) không khớp với Hợp đồng ($115,000). Ngân hàng từ chối chuyển tiền T/T hoặc thanh toán L/C (UCP 600). | Phát hành lại Commercial Invoice với tổng số tiền $115,000.00 khớp với Hợp đồng ngoại thương. |
| **7** | `L4-04` | **Lệch mã số HS Code** | Phân nhóm mã HS 6 số giữa Hóa đơn và C/O | *Commercial Invoice: 8479.89 (Máy móc nguyên chiếc)* | *C/O Form AK Ô số 8: 8479.90 (Phụ tùng, bộ phận máy)* | Bất nhất mã HS 6 chữ số giữa C/O và Bộ chứng từ. Hải quan sẽ từ chối áp dụng thuế suất ưu đãi đặc biệt AKFTA (0%), áp thuế MFN hoặc tạm giữ C/O để tiến hành xác minh xuất xứ (Verification) kéo dài 2-6 tháng. | 1) Đề nghị Shipper liên hệ KCCI cấp lại C/O Form AK với mã HS chuẩn 8479.89.<br>2) Trường hợp tàu đã cập cảng cần lấy hàng gấp: Tiến hành thủ tục KHAI NỢ C/O trong vòng 30 ngày (theo Thông tư 38/2015 và TT 121/2025/TT-BTC), tạm nộp thuế MFN và xin hoàn thuế sau khi nộp C/O chuẩn. |

---

## 3. DANH MỤC THÔNG TIN ĐÃ ĐỒNG NHẤT (VERIFIED CHECKLIST)

- [x] **Trình tự thời gian:** Invoice Date (08/09/2026) >= Contract Date (15/08/2026) [ĐẠT - L1-01]
- [x] **Hiệu lực C/O:** C/O còn hiệu lực trong thời hạn 12 tháng kể từ ngày cấp (12/09/2026) [ĐẠT - L1-04]
- [x] **Bảo hiểm hàng hải:** Insurance Date (03/09/2026) <= B/L Date (05/09/2026) [ĐẠT - L1-05]
- [x] **Thời gian đóng gói:** PL Date (04/09/2026) <= B/L Date (05/09/2026) [ĐẠT - L1-06]
- [x] **Mã số thuế (Tax ID):** Mã số thuế [0109876543] đồng nhất giữa Contract và Invoice [ĐẠT - L2-04]
- [x] **Cảng xếp hàng (POL):** Busan Port đồng nhất trên Contract, Invoice và B/L [ĐẠT - L2-07]
- [x] **Cảng dỡ hàng (POD):** Cat Lai Port đồng nhất trên Contract, Invoice và B/L [ĐẠT - L2-07]
- [x] **Tỷ lệ trọng lượng:** PL Gross Weight (18,450.00 KGS) >= Net Weight (16,800.00 KGS) [ĐẠT - L3-01]
- [x] **Số lượng kiện:** Khớp 8 Wooden Cases giữa PL, B/L và C/O [ĐẠT - L3-03]
- [x] **Số Container:** Container No. [KMTU7894561] khớp 100% giữa PL và B/L [ĐẠT - L3-05]
- [x] **Số Chì (Seal):** Seal No. [KMTC88921] khớp 100% giữa PL và B/L [ĐẠT - L3-05]
- [x] **Hun trùng ISPM 15:** Kiện gỗ [WOODEN CASES] tuân thủ tiêu chuẩn hun trùng quốc tế ISPM 15 [ĐẠT - L3-06]
- [x] **Đồng tiền thanh toán:** Đồng tiền [USD] đồng nhất giữa Contract và Invoice [ĐẠT - L4-08]
- [x] **Tiêu chí xuất xứ C/O:** Tiêu chí [CTH] ghi nhận hợp lệ theo quy tắc AKFTA [ĐẠT - L5-01]
- [x] **Điều kiện giao hàng:** Incoterms thể hiện rõ ràng địa điểm [CIF Cat Lai Port, Ho Chi Minh City, Vietnam Incoterms 2020] [ĐẠT]

---

## 4. KHUYẾN NGHỊ CUỐI CÙNG TRƯỚC KHI TRUYỀN TỜ KHAI

Để bảo đảm lô hàng được thông quan thuận lợi, tránh bị xử phạt vi phạm hành chính (Nghị định 128/2020/NĐ-CP) và được hưởng trọn vẹn thuế suất ưu đãi đặc biệt AKFTA (0%), người làm thủ tục bắt buộc thực hiện theo lộ trình hành động sau:

### 4.1. Hành động khẩn cấp với Shipper (Hansung Tech Co., Ltd.)
1. **Phát hành lại Commercial Invoice:** Sửa lại ngày phát hành về ngày **28/08/2026** (trước 05/09/2026); sửa phép tính Dòng 2 thành `$25,000.00` và tổng hóa đơn thành `$115,000.00` khớp 100% với Sales Contract.
2. **Xin cấp lại C/O Form AK thay thế (Replacement C/O):** Yêu cầu Shipper đề nghị KCCI phát hành lại C/O Form AK với 2 điểm bắt buộc:
   - Tích chọn ô số 13: `[x] ISSUED RETROACTIVELY` (do ngày cấp 12/09/2026 sau ngày tàu chạy 05/09/2026).
   - Sửa lại mã HS tại Ô số 8 thành **`8479.89`** (máy nguyên chiếc đồng nhất với Invoice).

### 4.2. Hành động với Hãng tàu / Đại lý Giao nhận (KMTC Line)
1. **Đính chính Manifest điện tử:** Nộp công văn yêu cầu KMTC Line gửi điện đính chính Manifest trên Cổng Thông tin Một cửa quốc gia (NSW) đối với chỉ tiêu Tổng trọng lượng: Sửa từ `18,050.00 KGS` thành `18,450.00 KGS` theo đúng Packing List gốc.
2. **Phát hành Giấy đính chính Vận đơn (B/L Correction / Certificate):** Làm rõ lỗi đánh máy địa chỉ Consignee (`Haong Mai` $\rightarrow$ `Hoang Mai`) và số liệu Gross Weight.

### 4.3. Phương án xử lý của Người Khai Hải Quan tại Cửa khẩu Cát Lái
1. **Khai nợ C/O hợp pháp:** Do việc xin cấp lại C/O từ Hàn Quốc mất từ 3 - 5 ngày làm việc, khi truyền tờ khai chính thức trên VNACCS, khai báo mã lý do **NỢ C/O TẠI THỜI ĐIỂM ĐĂNG KÝ TỜ KHAI** theo quy định tại Thông tư 38/2015/TT-BTC (sửa đổi tại TT 39/2018 và TT 121/2025/TT-BTC). Doanh nghiệp sẽ tạm nộp theo thuế suất MFN và nộp C/O bổ sung trong vòng 30 ngày để hoàn thuế.
2. **Chuẩn bị Thư giải trình:** Soạn thảo sẵn công văn giải trình về việc sai lệch trọng lượng B/L đã được hãng tàu sửa đổi Manifest, xuất trình phiếu cân cầu cảng khi tiếp nhận hồ sơ nếu tờ khai rơi vào luồng Vàng/Đỏ.