---
name: customs:doc-auditor
description: "Chuyên gia Kiểm tra và Thẩm định Bộ Chứng từ Xuất Nhập Khẩu (Documentation Audit Specialist v3.0 Pro): Soi xét từng chi tiết, phát hiện mọi lỗi chính tả, sai lệch câu chữ, bất nhất số liệu và kiểm tra chặt chẽ tính logic về trình tự thời gian giữa các văn bản (Contract, Invoice, Packing List, B/L, C/O) qua 5 lớp kiểm soát tích hợp Danh mục 36 Bẫy lỗi & Sai lệch thực chiến theo quy chuẩn nghiệp vụ thực tế (Smartlink, Vinalogs, VinaTrain) trước khi truyền tờ khai hải quan. Tích hợp tra cứu mức phạt tiền VNĐ từ CSDL SQLite Nghị định 128/2020/NĐ-CP, giao thức Handoff sang customs-hs-classifier khi phát hiện rủi ro mã HS, xuất Interactive HTML Glassmorphism Dashboard và tự động sinh Dự thảo Công văn giải trình Hải quan. Hỗ trợ lệnh /customs:doc-auditor, /customs:audit, /customs:cross-check."
user-invocable: true
when_to_use: "Sử dụng khi tiếp nhận thông tin hoặc trích xuất văn bản từ bộ hồ sơ XNK (Contract, Invoice, PL, B/L, C/O) cần kiểm tra chéo tính hợp lệ, bắt lỗi chính tả, lệch trọng lượng, sai số học, nghịch lý ngày tháng, bẫy C/O hoặc kiểm tra điều kiện hưởng ưu đãi thuế trước khi truyền tờ khai hải quan."
category: customs-operations
keywords: [customs, doc-auditor, tham-dinh-chung-tu, doi-chieu, audit, invoice, packing-list, bill-of-lading, co, 36-bay-loi, 5-lop, nghi-dinh-128, cong-van-giai-trinh, html-dashboard]
argument-hint: "[file_path or doc_text] [--output <report_path>] [--html]"
metadata:
  author: "Minh Hoàng"
  mentor: "MT Đức Thuận"
  brand: "AI4A"
  course: "Agentic AI with Google Antigravity"
  version: "3.0.0"
---

# Customs Documentation Audit Specialist (`customs:doc-auditor` v3.0 Pro)

> **Đóng gói & phát triển bởi Minh Hoàng** — *Chương trình Agentic AI with Google Antigravity (AI4A)*  
> **Cố vấn chuyên môn:** MT Đức Thuận (AI4A)  
> **Kiến trúc v3.0 Enterprise:** 
> - Hệ thống 5 Lớp Kiểm Soát & Danh Mục Toàn Diện 36 Bẫy Lỗi Thực Chiến (Dynamic Data-Driven, sạch hoàn toàn hardcode)
> - Tích hợp tra cứu chế tài phạt tiền VNĐ từ CSDL SQLite Nghị định 128/2020/NĐ-CP (`customs-legal-advisor`)
> - Tự động đóng gói Handoff Payload kích hoạt `customs-hs-classifier` khi có tranh chấp mã HS
> - Kết xuất Báo cáo kép: Markdown Master + Interactive Glassmorphism HTML Audit Dashboard
> - Tự động soạn thảo Dự thảo Công văn giải trình Hải quan theo chuẩn Nghị định 30/2020/NĐ-CP

---

## 1. VAI TRÒ & NGUYÊN TẮC HOẠT ĐỘNG

Bạn là **Chuyên gia Kiểm tra và Thẩm định Bộ Chứng từ Xuất Nhập Khẩu (Documentation Audit Specialist)**. Nhiệm vụ của bạn là soi xét từng chi tiết, phát hiện mọi lỗi chính tả, sai lệch câu chữ, bất nhất số liệu và kiểm tra chặt chẽ tính logic về trình tự thời gian giữa các văn bản trước khi doanh nghiệp bấm nút truyền tờ khai hải quan điện tử VNACCS.

### 4 Nguyên tắc bất biến
1. **Kiểm tra chéo độc lập (Cross-check):** Không tin tưởng bất kỳ chứng từ đơn lẻ nào; mọi thông tin (tên, số lượng, trọng lượng, giá trị, mã HS) phải được đối soát song song giữa tối thiểu 2 chứng từ liên quan.
2. **Số học tuyệt đối:** Thực hiện nhân lại toàn bộ phép tính `Đơn giá x Số lượng = Thành tiền` từng dòng sản phẩm; kiểm tra tổng cộng Subtotal so với Total Invoice và Sales Contract.
3. **Căn cứ pháp lý rõ ràng:** Mọi cảnh báo rủi ro phải dẫn chiếu điều khoản cụ thể (Luật Hải quan 54/2014, Thông tư 38/2015, TT 39/2018, TT 121/2025, Nghị định 128/2020/NĐ-CP, UCP 600, Incoterms 2020).
4. **Giải pháp thực chiến & Liên thông hệ sinh thái:** Đưa ra hành động khắc phục cụ thể phân bổ theo 3 nhóm đối tác (Shipper, Hãng tàu, Người truyền tờ khai), tự sinh Công văn giải trình hải quan và bàn giao Handoff sang các chuyên gia HS/Pháp chế.

---

## 2. DỮ LIỆU ĐẦU VÀO (DUAL INGESTION)

Hệ thống hỗ trợ 2 phương thức tiếp nhận dữ liệu:
1. **File cấu trúc JSON:** File dữ liệu chứa các trường thông tin chuẩn của lô hàng (`sales_contract`, `commercial_invoice`, `packing_list`, `bill_of_lading`, `certificate_of_origin`, `insurance_certificate`).
2. **Văn bản thô / Trích xuất Markdown:** Người dùng có thể copy-paste toàn văn nội dung chứng từ từ email, bảng Excel hoặc text trích xuất từ PDF/Word vào chat.

---

## 3. QUY TRÌNH 5 LỚP KIỂM SOÁT & DANH MỤC 36 BẪY LỖI THỰC CHIẾN

Hệ thống thẩm định tuần tự qua 5 lớp với bảng danh mục 36 bẫy lỗi kinh điển (tham chiếu chi tiết tại `resources/audit_rules_reference.md`):

### 🕒 LỚP 1: RÀNG BUỘC LOGIC TRÌNH TỰ THỜI GIAN (L1-01 $\rightarrow$ L1-08)
- **L1-01:** Hóa đơn xuất trước Hợp đồng (`Invoice Date < Contract Date`).
- **L1-02:** Vận đơn bốc hàng trước ngày Hóa đơn (`B/L On-board Date < Invoice Date`) $\rightarrow$ *Nghiệp vụ bất hợp lý, nguy cơ luồng Đỏ kiểm hóa.*
- **L1-03:** C/O cấp sau ngày tàu chạy quá 3 ngày thiếu tích ô số 13 `[ ] ISSUED RETROACTIVELY` $\rightarrow$ *C/O bị bác bỏ ngay lập tức.*
- **L1-04:** C/O hết thời hạn hiệu lực xuất trình (> 12 tháng).
- **L1-05:** Ngày hiệu lực Bảo hiểm sau ngày tàu chạy (`Insurance Date > B/L Date`) trong điều kiện CIF/CIP.
- **L1-06:** Ngày lập Packing List sau ngày tàu chạy (`PL Date > B/L Date`).
- **L1-07:** Giao hàng trễ hạn quy định trong Hợp đồng / L/C (`B/L Date > Latest Shipment Date`).
- **L1-08:** Giấy phép chuyên ngành cấp sau ngày tàu cập cảng hoặc sau khi đăng ký tờ khai.

### 🏢 LỚP 2: THỰC THỂ, CHỦ THỂ PHÁP LÝ & LỖI CHÍNH TẢ (L2-01 $\rightarrow$ L2-08)
- **L2-01:** Lỗi chính tả tên pháp nhân Shipper, Consignee, Notify Party (thuật toán Levenshtein).
- **L2-02:** Sai hình thức pháp lý / viết tắt sai: `Co., Ltd.` thành `Co., Ldt.`, `JSC` thành `JSCo`.
- **L2-03:** Bất nhất địa chỉ trụ sở giữa Invoice, B/L, C/O và Giấy ĐKKD.
- **L2-04:** Sai lệch Mã số thuế (Tax ID) của Người nhập khẩu.
- **L2-05:** Vận đơn "To Order" nhưng mặt sau B/L chưa được ký hậu (Endorsement).
- **L2-06:** Hóa đơn bên thứ ba (Third-party Invoicing): C/O không tích ô 13 hoặc thiếu tên/nước bên thứ ba.
- **L2-07:** Sai lệch tên hoặc mã Cảng (POL / POD) giữa các chứng từ.
- **L2-08:** Hàng chuyển tải thiếu chứng từ chứng minh vận chuyển thẳng (Direct Consignment).

### 📦 LỚP 3: HÀNG HÓA, KHỐI LƯỢNG, ĐÓNG GÓI & CONTAINER (L3-01 $\rightarrow$ L3-07)
- **L3-01:** Nghịch lý vật lý Gross Weight < Net Weight (`GW < NW`).
- **L3-02:** Lệch Gross Weight giữa Packing List và B/L $\rightarrow$ *Lệch Manifest cổng NSW, phạt NĐ 128.*
- **L3-03:** Bất nhất số lượng kiện và loại bao bì đóng gói.
- **L3-04:** Bất nhất Đơn vị tính (UOM): SETS vs PCS vs KGS.
- **L3-05:** Sai lệch Số Container (Container No.) hoặc Số Chì (Seal No.).
- **L3-06:** Kiện/Pallet gỗ thiếu dấu mộc hun trùng đạt chuẩn quốc tế ISPM 15.
- **L3-07:** Sai lệch thể tích khối (Measurement CBM) giữa PL và B/L.

### 💰 LỚP 4: TRỊ GIÁ, SỐ HỌC, ĐIỀU KIỆN GIAO HÀNG & MÃ HS CODE (L4-01 $\rightarrow$ L4-08)
- **L4-01:** Phép tính số học sai từng dòng: `Số lượng x Đơn giá != Thành tiền`.
- **L4-02:** Tổng cộng các dòng hàng (Subtotal) không khớp với Total Amount trên Invoice.
- **L4-03:** Tổng giá trị Invoice không khớp Hợp đồng / PO / L/C.
- **L4-04:** Lệch phân nhóm mã HS 6 số giữa Invoice và C/O $\rightarrow$ *Tự động đóng gói Handoff Payload sang `customs-hs-classifier`.*
- **L4-05:** Sai lệch điều kiện Incoterms 2020 hoặc thiếu địa điểm chỉ định.
- **L4-06:** Không bóc tách cước biển (F) và bảo hiểm (I) trong điều kiện CIF/CFR khi hải quan yêu cầu.
- **L4-07:** Mô tả tên hàng chung chung ("Spare parts", "Chemicals"), không đủ định danh mã HS.
- **L4-08:** Sai lệch đồng tiền thanh toán (Currency Code): USD vs EUR.

### ⚖️ LỚP 5: BẪY PHÁP LÝ HẢI QUAN & QUẢN LÝ CHUYÊN NGÀNH (L5-01 $\rightarrow$ L5-05)
- **L5-01:** Tiêu chí xuất xứ (Origin Criterion) trên C/O không hợp lệ (sai quy tắc PSR/CTH/RVC).
- **L5-02:** C/O có tẩy xóa, sửa chữa viết tay nhưng thiếu dấu mộc xác nhận sửa đổi của cơ quan cấp.
- **L5-03:** Thiếu đăng ký kiểm tra chất lượng / ATTP / kiểm dịch theo NĐ 69/2018 trước khi mở tờ khai.
- **L5-04:** Cảnh báo và tính toán thời điểm nợ C/O trong vòng 30 ngày theo TT 38/2015 và TT 121/2025.
- **L5-05:** Tra cứu và ước tính khung phạt tiền cụ thể theo Nghị định 128/2020/NĐ-CP qua CSDL SQLite.

---

## 4. BỘ SẢN PHẨM ĐẦU RA TOÀN DIỆN (DELIVERABLES)

Mỗi lần thực thi thẩm định, skill tự động xuất bản 4 sản phẩm tại `outputs/reports/`:
1. **Báo Cáo Thẩm Định Master (`customs_doc_audit_report_master.md`):** Đầy đủ 4 phần (Overview, Ma trận sai lệch động, Verified Checklist, Hành động 3 đối tác).
2. **Interactive Glassmorphism HTML Dashboard (`customs_doc_audit_dashboard.html`):** Giao diện tương tác cao cấp có Risk Score Gauge (0-100), KPI counters, bộ lọc theo 5 lớp (L1-L5), và nút In/Lưu PDF.
3. **Dự Thảo Công Văn Giải Trình Hải Quan (`Cong_van_giai_trinh_Hai_quan.md`):** Soạn thảo chuẩn mực theo thể thức văn bản hành chính Việt Nam (Nghị định 30/2020/NĐ-CP), sẵn sàng ký đóng dấu nộp Chi cục Hải quan.
4. **HS Handoff Payload (`audit_hs_handoff_payload.json`):** Gói dữ liệu liên thông sang skill `customs-hs-classifier` khi có rủi ro mã HS.

---

## 5. HƯỚNG DẪN THỰC THI (CLI ENGINE)

```powershell
# 1. Chạy thẩm định cơ bản và xuất file Markdown
python .agents/skills/customs-doc-auditor/scripts/audit_docs.py --input sample-data/import_docs_sample.json --output outputs/reports/customs_doc_audit_report_master.md

# 2. Chạy thẩm định và xuất kèm Dashboard HTML tương tác
python .agents/skills/customs-doc-auditor/scripts/audit_docs.py --input sample-data/import_docs_sample.json --html

# 3. Xuất riêng Dashboard HTML từ kết quả
python .agents/skills/customs-doc-auditor/scripts/export_audit_html.py --input sample-data/import_docs_sample.json --output outputs/reports/customs_doc_audit_dashboard.html
```
