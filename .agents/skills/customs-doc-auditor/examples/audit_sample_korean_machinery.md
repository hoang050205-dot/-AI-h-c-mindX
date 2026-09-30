# VÍ DỤ MẪU: THẨM ĐỊNH BỘ CHỨNG TỪ NHẬP KHẨU DÂY CHUYỀN CHIẾT RÓT (HÀN QUỐC - CÁT LÁI)

> **Mục đích:** Bản ghi minh họa quy trình thẩm định 5 lớp và đối chiếu chéo thực tế trên lô hàng mẫu cài cắm 6 bẫy lỗi kinh điển.  
> **Lệnh thực thi:** `/customs:doc-auditor --input sample-data/import_docs_sample.json` hoặc chạy script `python .agents/skills/customs-doc-auditor/scripts/audit_docs.py`.

---

## 1. DỮ LIỆU ĐẦU VÀO CỦA BỘ HỒ SƠ

- **Mã lô hàng:** `SHP-2026-KR-VN-001`
- **Mặt hàng:** Dây chuyền chiết rót và đóng nắp chai tự động (Model: AFC-2026-KR)
- **Các chứng từ cung cấp:**
  1. *Sales Contract:* No. HSC-VH-2026/08, Ngày 15/08/2026, Trị giá USD 115,000.00 CIF Cat Lai Port.
  2. *Commercial Invoice:* No. INV-20260828, Ngày 08/09/2026, Trị giá USD 113,000.00.
  3. *Packing List:* No. PL-20260828, Ngày 04/09/2026, GW: 18,450.00 KGS, NW: 16,800.00 KGS, 8 kiện.
  4. *Bill of Lading:* No. KMTCBUS20260901, On-board Date 05/09/2026, GW: 18,050.00 KGS, Địa chỉ Consignee: `Quan Haong Mai`.
  5. *C/O Form AK:* No. KCCI-2026-AK-0912, Ngày 12/09/2026, Ô 8 ghi HS `8479.90`, Ô 13 bỏ trống `[ ] ISSUED RETROACTIVELY`.
  6. *Insurance Certificate:* Ngày 03/09/2026, Trị giá 110% CIF (USD 126,500.00).

---

## 2. QUÁ TRÌNH RÀ SOÁT TUẦN TỰ 5 LỚP

### Lớp 1: Date Chronology (Trình tự thời gian)
- `Contract Date (15/08/2026) <= B/L Date (05/09/2026)` $\rightarrow$ HỢP LỆ.
- `Invoice Date (08/09/2026)` xuất hiện **SAU** `B/L Date (05/09/2026)` $\rightarrow$ **PHÁT HIỆN LỖI 1 (NGHIÊM TRỌNG):** Nghiệp vụ giao thương bất hợp lý, hàng đã lên tàu chạy 3 ngày mới xuất hóa đơn.
- `C/O Date (12/09/2026)` cấp sau `B/L Date (05/09/2026)` **7 ngày** nhưng Ô 13 không tích `ISSUED RETROACTIVELY` $\rightarrow$ **PHÁT HIỆN LỖI 2 (RẤT NẶNG):** Bị từ chối C/O Form AK theo quy tắc AKFTA.
- `Insurance Date (03/09/2026) <= B/L Date (05/09/2026)` $\rightarrow$ HỢP LỆ.

### Lớp 2: Entity & Typo Cross-check (Thực thể & Lỗi chính tả)
- Tên Shipper, MST Buyer: Đồng nhất.
- Địa chỉ Consignee trên B/L: ghi `Quan Haong Mai, Ha Noi` trong khi Contract/Invoice/PL ghi `Quan Hoang Mai, Ha Noi` $\rightarrow$ **PHÁT HIỆN LỖI 3:** Lỗi gõ sai chữ (Typo).
- Cảng đi (Busan) và Cảng đến (Cát Lái): Đồng nhất.

### Lớp 3: Cargo Details (Khối lượng & Đóng gói)
- Số kiện: 8 Wooden Cases khớp trên PL, B/L, C/O.
- Tỷ lệ trọng lượng: `GW (18,450) >= NW (16,800)` $\rightarrow$ HỢP LỆ.
- So sánh PL GW vs B/L GW: PL ghi `18,450.00 KGS` nhưng B/L ghi `18,050.00 KGS` $\rightarrow$ **PHÁT HIỆN LỖI 4 (NGHIÊM TRỌNG):** Lệch đúng **400.00 KGS**. Khả năng cao do hãng tàu gõ nhầm hoặc sai lệch Manifest. Hải quan cân cầu cảng sẽ phát hiện ngay, bị phạt vi phạm hành chính NĐ 128/2020.
- Số Container `KMTU7894561` & Số Chì `KMTC88921`: Khớp 100%.

### Lớp 4: Valuation & Goods Description & HS Code
- Nhân lại phép tính dòng 2 của Invoice: `1 SET x $25,000 = $23,000` $\rightarrow$ **PHÁT HIỆN LỖI 5:** Lỗi tính toán số học trên hóa đơn!
- Tổng hóa đơn ($113,000) không khớp với Hợp đồng ($115,000) $\rightarrow$ **PHÁT HIỆN LỖI 6:** Lệch điều khoản thanh toán quốc tế $2,000.
- Mã HS trên Invoice ghi `8479.89` (máy nguyên chiếc) nhưng trên C/O Form AK Ô 8 ghi `8479.90` (phụ tùng, linh kiện rời) $\rightarrow$ **PHÁT HIỆN LỖI 7:** Bất nhất mã phân nhóm HS 6 số, nguy cơ bị bác ưu đãi thuế.

### Lớp 5: Customs Compliance & Strategic Actions
- Tổng hợp toàn bộ 7 lỗi và lập Ma trận sai lệch.
- Đưa ra giải pháp tình thế cứu nguy: **Khai nợ C/O trong vòng 30 ngày** trên tờ khai điện tử để kéo dài thời gian xin KCCI cấp lại C/O đúng quy cách.

---

## 3. KẾT QUẢ ĐẦU RA MẪU

Báo cáo chi tiết đã được xuất bản hoàn chỉnh tại:  
👉 [customs_doc_audit_report_master.md](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/outputs/reports/customs_doc_audit_report_master.md)
