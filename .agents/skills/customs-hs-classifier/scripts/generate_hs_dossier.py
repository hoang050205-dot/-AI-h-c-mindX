import os
import sys
import re
import json
import argparse
from classify_hs_expert import analyze_classification

sys.stdout.reconfigure(encoding='utf-8')

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_dossier_markdown(res, out_path=None):
    d = res["dissection"]
    p = res["primary_classification"]
    g = res["gri_determination"]
    b = res["borderline_analysis"]
    t = res["tariff_breakdown"]
    sim = t["simulation"]
    h = res["handoff_payload"]
    
    comm_name = d["commodity"]
    
    md_content = f"""# HỒ SƠ THẨM ĐỊNH & BIỆN LUẬN PHÂN LOẠI MÃ HS (HS CLASSIFICATION DOSSIER)
**Mặt Hàng:** {comm_name.upper()}  
**Nước Xuất Xứ (Origin):** {t['origin']} | **Chứng Nhận Xuất Xứ (C/O):** {h['commodity_dossier']['co_form_provided']}  
**Cơ Quan Phân Loại:** Chuyên Viên Thẩm Định Mã HS & Biểu Thuế XNK  
**Tiêu Chuẩn Áp Dụng:** 6 Quy tắc GRI (WCO HS Convention), Danh mục XNK Việt Nam (Thông tư 31/2022/TT-BTC) & Biểu thuế XNK 2026

---

## 1. THẨM ĐỊNH BẢN CHẤT KỸ THUẬT & BÓC TÁCH 4 CHIỀU (TECHNICAL DISSECTION)

Việc phân loại mã HS bắt buộc phải căn cứ vào bản chất kỹ thuật khách quan của hàng hóa theo 4 tiêu chí cốt lõi của Tổ chức Hải quan Thế giới (WCO):

| Tiêu Chí Thẩm Định | Thông Tin Mô Tả Thực Tế | Nhận Định Kỹ Thuật Nghiệp Vụ |
|:---|:---|:---|
| **1. Thành phần / Chất liệu (Composition)** | {d['material']} | Xác định chất liệu cấu thành cơ bản để tra cứu Chương và Nhóm vật liệu tương ứng. |
| **2. Trạng thái gia công (Processing State)** | {d['processing_state']} | Xác định mức độ hoàn thiện, sơ chế, tinh chế hoặc hàng dở dang/tháo rời. |
| **3. Chức năng chính (Principal Function)** | {d['principal_function']} | Xác định công năng và mục đích sử dụng chi phối để đối chiếu Chú giải 2 Phần XVI / Chú giải 3 Chương 84, 85. |
| **4. Quy cách thương phẩm (Presentation)** | {d['commercial_presentation']} | Xác định quy cách bao bì, hàng rời (bulk) hay bộ sản phẩm bán lẻ (retail set). |

---

## 2. KẾT QUẢ PHÂN LOẠI MÃ HS 8 CHỮ SỐ (NATIONAL TARIFF LINE)

Căn cứ Điều 16 & Điều 29 Luật Hải quan số 54/2014/QH13, việc khai báo hải quan điện tử trên hệ thống VNACCS/VCIS bắt buộc phải áp dụng **Mã HS 8 chữ số quốc gia**:

| Chỉ Tiêu Phân Loại | Kết Quả Xác Định Chuẩn Hóa |
|:---|:---|
| **Mã HS Khuyến Nghị (8 Số)** | ` {p['hs_code']} ` |
| **Mô Tả Tiếng Việt Chuẩn (TT 31/2022)** | **{p['full_desc_vn']}** |
| **Mô Tả Tiếng Anh (AHTN/WCO)** | *{p['desc_en'] or 'N/A'}* |
| **Đơn Vị Tính Tiêu Chuẩn (Unit)** | `{p['unit']}` |
| **Cấp Độ Phân Nhóm / Nhóm** | Nhóm 4 số: `{p['parent_heading']}` |

---

## 3. QUY TẮC PHÂN LOẠI ÁP DỤNG & LẬP LUẬN BIỆN LUẬN PHÁP LÝ (GRI JUSTIFICATION)

### A. Quy Tắc Phân Loại Áp Dụng (GRI Applied)
> **ÁP DỤNG: {g['rule_title']} [{g['rule_id']}]**

### B. Chuỗi Lập Luận Giải Thích Chi Tiết (Legal Rationale & Explanatory Notes)
"""

    for pt in g["rationale_points"]:
        md_content += f"{pt}\n\n"

    md_content += f"""### C. Biện Luận Bác Bỏ Các Quy Tắc Khác (Exclusion Analysis)
- **Vì sao không áp dụng các quy tắc phân loại khác:**
  - Sản phẩm đã được định danh rõ ràng hoặc bóc tách công năng/đặc tính cơ bản theo đúng điều kiện của **{g['rule_id']}**, không phát sinh xung đột mô tả không thể giải quyết để phải viện dẫn đến Quy tắc 4 (Hàng tương tự nhất).
  - Bao bì đi kèm là loại đóng gói thông thường phục vụ bảo quản vận chuyển, áp dụng Quy tắc 5(b) phân loại chung theo sản phẩm chính.

---

## 4. MA TRẬN MÃ ĐỐI TRỌNG (BORDERLINE HS), TAX DELTA & CẢNH BÁO RỦI RO THAM VẤN

Trong nghiệp vụ hải quan thực tế, cơ quan Hải quan thường kiểm tra sau thông quan (PCA) hoặc tham vấn giá/mã nếu nghi ngờ doanh nghiệp áp sai mã để hưởng thuế suất thấp:

"""

    if b:
        md_content += f"""| Tiêu Chí So Sánh | Mã Khuyến Nghị Chính Thức | Mã Đối Trọng Tiềm Ẩn (Borderline) |
|:---|:---:|:---:|
| **Mã Số HS (8 Chữ Số)** | **`{p['hs_code']}`** | **`{b['borderline_hs']}`** |
| **Mô Tả Hàng Hóa** | {p['full_desc_vn'][:80]}... | {b['borderline_desc'][:80]}... |
| **Thuế Nhập Khẩu MFN** | **{t['import_duty_rate']}** | **{b['mfn_rate']}** |
| **Chênh Lệch Thuế (Tax Delta)** | **Gốc (Baseline)** | **{b['tax_delta_mfn']}** (MFN) \| **{b['tax_delta_vat']}** (VAT) |
| **Mức Độ Rủi Ro Tranh Chấp** | — | **{b['risk_level']}** |

### ⚠️ Cảnh Báo Nghiệp Vụ & Rủi Ro Chế Tài:
{b['risk_warning']}

### 🛡️ Bộ Tiêu Chí Phân Định Cần Chuẩn Bị Để Bảo Vệ Mã:
"""
        for cr in b["discrimination_criteria"]:
            md_content += f"- {cr}\n"
    else:
        md_content += "- Không ghi nhận mã đối trọng cạnh tranh trực tiếp trong cùng phân nhóm.\n"

    md_content += f"""
---

## 5. NGHĨA VỤ THUẾ THỰC TẾ & MÔ PHỎNG CHI PHÍ THUẾ LÔ HÀNG

### A. Bảng Thuế Suất Thực Tế Theo Xuất Xứ (Origin-Based Tariff)
- **Nước xuất xứ:** {t['origin']}
- **Chế độ thuế áp dụng:** {t['duty_type']}
- **Căn cứ pháp lý Biểu thuế NK:** {t['legal_decree']}
- **Thuế suất Nhập khẩu:** **{t['import_duty_rate']}**
- **Thuế suất GTGT (VAT):** **{t['vat_rate']}** *(Căn cứ: {t['vat_decree']})*

### B. Mô Phỏng Nghĩa Vụ Thuế Phải Nộp Cho Lô Hàng
*(Giả định trị giá tính thuế CIF = **{sim['cif_val']:,.2f}**)*

```text
1. Tiền Thuế Nhập Khẩu (Import Duty):
   = Trị giá CIF x Thuế suất NK
   = {sim['cif_val']:,.2f} x {t['import_duty_rate']}
   = {sim['import_duty_amount']:,.2f}

2. Trị Giá Tính Thuế GTGT (VAT Base):
   = Trị giá CIF + Tiền Thuế NK
   = {sim['cif_val']:,.2f} + {sim['import_duty_amount']:,.2f}
   = {sim['vat_base_amount']:,.2f}

3. Tiền Thuế Giá Trị Gia Tăng (VAT):
   = Trị giá tính thuế GTGT x Thuế suất VAT
   = {sim['vat_base_amount']:,.2f} x {t['vat_rate']}
   = {sim['vat_amount']:,.2f}

────────────────────────────────────────────────────────────────
👉 TỔNG NGHĨA VỤ NỘP NGÂN SÁCH (TOTAL TAX): {sim['total_tax_amount']:,.2f}
────────────────────────────────────────────────────────────────
```

---

## 6. GIAO THỨC BÀN GIAO THỦ TỤC & PHÁP LÝ (HANDOFF PROTOCOL)

> **CHUYỂN GIAO SANG SKILL: `customs:legal-advisor`**  
> Toàn bộ thông tin phân loại kỹ thuật và mã HS đã được đóng gói thành **Handoff Payload JSON** chuẩn hóa dưới đây. Kích hoạt lệnh `/customs:legal-advisor` để tra cứu giấy phép chuyên ngành (Nghị định 69/2018/NĐ-CP) và lập danh mục bộ hồ sơ hải quan (Điều 16 TT 121/2025/TT-BTC).

```json
{json.dumps(h, ensure_ascii=False, indent=2)}
```

---
*Báo cáo được khởi tạo tự động bởi **Customs HS Classifier & Tariff Specialist v2.0** (Antigravity Workspace).*
"""

    if not out_path:
        safe_name = re.sub(r'[^a-zA-Z0-9_\u00C0-\u024F\u1E00-\u1EFF]', '_', comm_name).strip('_')
        out_path = os.path.join(skill_dir, "..", "..", "..", "outputs", "reports", f"HS_Classification_Dossier_{safe_name}.md")
        out_path = os.path.abspath(out_path)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    # Save handoff json alongside
    json_path = os.path.join(os.path.dirname(out_path), "hs_handoff_payload.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(h, f, ensure_ascii=False, indent=2)

    return out_path, json_path

def main():
    parser = argparse.ArgumentParser(description="Xuat Ban Báo Cáo Thẩm Định & Biện Luận Phân Loại Mã HS (HS Classification Dossier)")
    parser.add_argument("-c", "--commodity", required=True, help="Ten mat hang hoac mo ta thuong mai")
    parser.add_argument("-m", "--material", default="", help="Chat lieu / Thanh phan cau tao")
    parser.add_argument("-f", "--function", default="", help="Chuc nang chinh / Muc dich su dung")
    parser.add_argument("-s", "--state", default="", help="Trang thai gia cong / che bien")
    parser.add_argument("-p", "--packaging", default="", help="Quy cach dong goi / Bo ban le")
    parser.add_argument("-o", "--origin", default="Mỹ", help="Nuoc xuat xu (Origin)")
    parser.add_argument("--co", default="", help="Mau chung nhan xuat xu (Form E, Form D, EUR.1, CPTPP...)")
    parser.add_argument("--cif", type=float, default=100000.0, help="Gia tri CIF gia dinh")
    parser.add_argument("-out", "--output", default="", help="Duong dan tep Markdown xuat ra")

    args = parser.parse_args()

    res = analyze_classification(
        commodity=args.commodity,
        material=args.material,
        function=args.function,
        state=args.state,
        packaging=args.packaging,
        origin=args.origin,
        co_form=args.co,
        cif_val=args.cif
    )

    out_md, out_json = generate_dossier_markdown(res, args.output if args.output else None)

    print(f"\n{'='*95}")
    print(f" [OK] ĐÃ XUẤT BẢN THÀNH CÔNG HỒ SƠ BIỆN LUẬN PHÂN LOẠI MÃ HS:")
    print(f"   📄 Markdown Dossier : {out_md}")
    print(f"   📦 Handoff Payload  : {out_json}")
    print(f"{'='*95}\n")

if __name__ == "__main__":
    main()
