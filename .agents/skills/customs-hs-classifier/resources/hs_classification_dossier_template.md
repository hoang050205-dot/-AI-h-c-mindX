# HỒ SƠ THẨM ĐỊNH & BIỆN LUẬN PHÂN LOẠI MÃ HS (HS CLASSIFICATION DOSSIER)
**Mặt Hàng:** {{COMMODITY_NAME}}  
**Nước Xuất Xứ (Origin):** {{ORIGIN_COUNTRY}} | **Chứng Nhận Xuất Xứ (C/O):** {{CO_FORM_PROVIDED}}  
**Cơ Quan Phân Loại:** Chuyên Viên Thẩm Định Mã HS & Biểu Thuế XNK (Skill `customs-hs-classifier`)  
**Tiêu Chuẩn Áp Dụng:** 6 Quy tắc GRI (WCO HS Convention), Danh mục XNK Việt Nam (Thông tư 31/2022/TT-BTC) & Biểu thuế XNK 2026

---

## 1. THẨM ĐỊNH BẢN CHẤT KỸ THUẬT & BÓC TÁCH 4 CHIỀU (TECHNICAL DISSECTION)

Việc phân loại mã HS bắt buộc phải căn cứ vào bản chất kỹ thuật khách quan của hàng hóa theo 4 tiêu chí cốt lõi của Tổ chức Hải quan Thế giới (WCO):

| Tiêu Chí Thẩm Định | Thông Tin Mô Tả Thực Tế | Nhận Định Kỹ Thuật Nghiệp Vụ |
|:---|:---|:---|
| **1. Thành phần / Chất liệu (Composition)** | {{MATERIAL_COMPOSITION}} | Xác định chất liệu cấu thành cơ bản để tra cứu Chương và Nhóm vật liệu tương ứng. |
| **2. Trạng thái gia công (Processing State)** | {{PROCESSING_STATE}} | Xác định mức độ hoàn thiện, sơ chế, tinh chế hoặc hàng dở dang/tháo rời. |
| **3. Chức năng chính (Principal Function)** | {{PRINCIPAL_FUNCTION}} | Xác định công năng và mục đích sử dụng chi phối để đối chiếu Chú giải 2 Phần XVI / Chú giải 3 Chương 84, 85. |
| **4. Quy cách thương phẩm (Presentation)** | {{COMMERCIAL_PRESENTATION}} | Xác định quy cách bao bì, hàng rời (bulk) hay bộ sản phẩm bán lẻ (retail set). |

---

## 2. KẾT QUẢ PHÂN LOẠI MÃ HS 8 CHỮ SỐ (NATIONAL TARIFF LINE)

Căn cứ Điều 16 & Điều 29 Luật Hải quan số 54/2014/QH13, việc khai báo hải quan điện tử trên hệ thống VNACCS/VCIS bắt buộc phải áp dụng **Mã HS 8 chữ số quốc gia**:

| Chỉ Tiêu Phân Loại | Kết Quả Xác Định Chuẩn Hóa |
|:---|:---|
| **Mã HS Khuyến Nghị (8 Số)** | ` {{RECOMMENDED_HS_8_DIGITS}} ` |
| **Mô Tả Tiếng Việt Chuẩn (TT 31/2022)** | **{{FULL_DESC_VIETNAMESE}}** |
| **Mô Tả Tiếng Anh (AHTN/WCO)** | *{{FULL_DESC_ENGLISH}}* |
| **Đơn Vị Tính Tiêu Chuẩn (Unit)** | `{{UNIT_OF_MEASURE}}` |
| **Cấp Độ Phân Nhóm / Nhóm** | Nhóm 4 số: `{{PARENT_HEADING_4_DIGITS}}` |

---

## 3. QUY TẮC PHÂN LOẠI ÁP DỤNG & LẬP LUẬN BIỆN LUẬN PHÁP LÝ (GRI JUSTIFICATION)

### A. Quy Tắc Phân Loại Áp Dụng (GRI Applied)
> **ÁP DỤNG: {{GRI_RULE_TITLE}} [{{GRI_RULE_ID}}]**

### B. Chuỗi Lập Luận Giải Thích Chi Tiết (Legal Rationale & Explanatory Notes)
{{GRI_RATIONALE_PARAGRAPHS}}

### C. Biện Luận Bác Bỏ Các Quy Tắc Khác (Exclusion Analysis)
- **Vì sao không áp dụng các quy tắc phân loại khác:**
  - Sản phẩm đã được định danh rõ ràng hoặc bóc tách công năng/đặc tính cơ bản theo đúng điều kiện của **{{GRI_RULE_ID}}**, không phát sinh xung đột mô tả không thể giải quyết để phải viện dẫn đến Quy tắc 4 (Hàng tương tự nhất).
  - Bao bì đi kèm là loại đóng gói thông thường phục vụ bảo quản vận chuyển, áp dụng Quy tắc 5(b) phân loại chung theo sản phẩm chính.

---

## 4. MA TRẬN MÃ ĐỐI TRỌNG (BORDERLINE HS), TAX DELTA & CẢNH BÁO RỦI RO THAM VẤN

Trong nghiệp vụ hải quan thực tế, cơ quan Hải quan thường kiểm tra sau thông quan (PCA) hoặc tham vấn giá/mã nếu nghi ngờ doanh nghiệp áp sai mã để hưởng thuế suất thấp:

| Tiêu Chí So Sánh | Mã Khuyến Nghị Chính Thức | Mã Đối Trọng Tiềm Ẩn (Borderline) |
|:---|:---:|:---:|
| **Mã Số HS (8 Chữ Số)** | **`{{RECOMMENDED_HS_8_DIGITS}}`** | **`{{BORDERLINE_HS_CODE}}`** |
| **Mô Tả Hàng Hóa** | {{RECOMMENDED_SHORT_DESC}} | {{BORDERLINE_SHORT_DESC}} |
| **Thuế Nhập Khẩu MFN** | **{{RECOMMENDED_MFN_RATE}}** | **{{BORDERLINE_MFN_RATE}}** |
| **Chênh Lệch Thuế (Tax Delta)** | **Gốc (Baseline)** | **{{TAX_DELTA_MFN}}** (MFN) \| **{{TAX_DELTA_VAT}}** (VAT) |
| **Mức Độ Rủi Ro Tranh Chấp** | — | **{{BORDERLINE_RISK_LEVEL}}** |

### ⚠️ Cảnh Báo Nghiệp Vụ & Rủi Ro Chế Tài:
{{BORDERLINE_RISK_WARNING}}

### 🛡️ Bộ Tiêu Chí Phân Định Cần Chuẩn Bị Để Bảo Vệ Mã:
{{DISCRIMINATION_CRITERIA_LIST}}

---

## 5. NGHĨA VỤ THUẾ THỰC TẾ & MÔ PHỎNG CHI PHÍ THUẾ LÔ HÀNG

### A. Bảng Thuế Suất Thực Tế Theo Xuất Xứ (Origin-Based Tariff)
- **Nước xuất xứ:** {{ORIGIN_COUNTRY}}
- **Chế độ thuế áp dụng:** {{DUTY_SCHEME_NAME}}
- **Căn cứ pháp lý Biểu thuế NK:** {{DUTY_LEGAL_DECREE}}
- **Thuế suất Nhập khẩu:** **{{APPLICABLE_IMPORT_DUTY}}**
- **Thuế suất GTGT (VAT):** **{{APPLICABLE_VAT}}** *(Căn cứ: {{VAT_LEGAL_DECREE}})*

### B. Mô Phỏng Nghĩa Vụ Thuế Phải Nộp Cho Lô Hàng
*(Giả định trị giá tính thuế CIF = **{{CIF_SIMULATED_VALUE}}**)*

```text
1. Tiền Thuế Nhập Khẩu (Import Duty):
   = Trị giá CIF x Thuế suất NK
   = {{CIF_SIMULATED_VALUE}} x {{APPLICABLE_IMPORT_DUTY}}
   = {{IMPORT_DUTY_AMOUNT}}

2. Trị Giá Tính Thuế GTGT (VAT Base):
   = Trị giá CIF + Tiền Thuế NK
   = {{CIF_SIMULATED_VALUE}} + {{IMPORT_DUTY_AMOUNT}}
   = {{VAT_BASE_AMOUNT}}

3. Tiền Thuế Giá Trị Gia Tăng (VAT):
   = Trị giá tính thuế GTGT x Thuế suất VAT
   = {{VAT_BASE_AMOUNT}} x {{APPLICABLE_VAT}}
   = {{VAT_AMOUNT}}

────────────────────────────────────────────────────────────────
👉 TỔNG NGHĨA VỤ NỘP NGÂN SÁCH (TOTAL TAX): {{TOTAL_TAX_AMOUNT}}
────────────────────────────────────────────────────────────────
```

---

## 6. GIAO THỨC BÀN GIAO THỦ TỤC & PHÁP LÝ (HANDOFF PROTOCOL)

> **CHUYỂN GIAO SANG SKILL: `customs:legal-advisor`**  
> Toàn bộ thông tin phân loại kỹ thuật và mã HS đã được đóng gói thành **Handoff Payload JSON** chuẩn hóa dưới đây. Kích hoạt lệnh `/customs:legal-advisor` để tra cứu giấy phép chuyên ngành (Nghị định 69/2018/NĐ-CP) và lập danh mục bộ hồ sơ hải quan (Điều 16 TT 121/2025/TT-BTC).

```json
{{HANDOFF_JSON_PAYLOAD}}
```

---
*Báo cáo được khởi tạo tự động bởi **Customs HS Classifier & Tariff Specialist v2.0** (Antigravity Workspace).*
