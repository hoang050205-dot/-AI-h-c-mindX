---
name: ops-erp-processor
description: "Tự động hóa quy trình xử lý dữ liệu vận hành ERP hàng tháng: quét sạch 799 dòng rác (ghost rows), chuẩn hóa định dạng số học, tự động phân tách bảng tính riêng biệt cho từng Quản lý (Managers) để bảo mật tiền lương, và sinh báo cáo phân tích quản trị vận hành (Executive Brief). Hỗ trợ lệnh /ops-erp-processor hoặc /ops:erp-processor."
user-invocable: true
when_to_use: "Sử dụng khi nhận được file xuất từ hệ thống ERP (chứa thông tin nhân viên, bộ phận, quản lý, lương, thưởng, phạt theo tháng) cần làm sạch dữ liệu, tách file theo từng cấp quản lý hoặc lập báo cáo tổng hợp quỹ lương."
category: workflow
keywords: [ops-erp-processor, ops:erp-processor, erp-processor, payroll, data-cleaning, ghost-rows, excel-split, manager-reports, ai4a]
argument-hint: "[path-to-erp-file.xlsx] [--managers] [--report] [--dry-run]"
metadata:
  author: "Operations Analyst / Antigravity AI"
  course: "Agentic AI with Google Antigravity (AI4A)"
  version: "1.1.0"
---

# OPS: ERP Processor — Quy Trình Tự Động Hóa Dữ Liệu Vận Hành ERP

> **Đóng gói chuẩn Antigravity Customization System**  
> *Hỗ trợ Operations Analyst tự động hóa 95% thời gian thủ công xử lý bảng tính ERP hàng tháng.*

---

## 1. Bản Hợp Đồng Thực Thi (Core Contract)

1. **Outcome:** 
   - 1 tệp Master Cleaned Excel lưu tại `outputs/reports/ERP_Operations_Master_<kỳ>.xlsx` (0 dòng rác, 100% nhân sự thực tế).
   - $N$ tệp Excel con tương ứng với từng Manager lưu tại `outputs/reports/managers/Manager_<Tên>_<kỳ>.xlsx`.
   - 1 bản báo cáo phân tích quản trị vận hành Markdown/HTML tại `outputs/reports/ERP_Executive_Operations_Report_<kỳ>.md`.
2. **Constraints:**
   - **Bảo mật tuyệt đối:** Tệp của Quản lý này không được chứa nhân sự của Quản lý khác.
   - **Toàn vẹn tài chính:** Sai số đối soát $\Delta = 0$ VNĐ giữa file Master và tổng các file con.
   - **Môi trường:** Chạy offline độc lập thông qua script PowerShell/OpenXML tích hợp sẵn trong skill.
3. **Non-goals:**
   - Không tự động gửi email hàng loạt nếu chưa qua bước rà soát (Human Checkpoint).
   - Không can thiệp sửa đổi trực tiếp vào database ERP nguồn.
4. **Acceptance Criteria:**
   - Loại bỏ 100% dòng rác trống (ghost rows).
   - Đủ danh sách nhân sự của từng Manager.
   - Có bảng xếp hạng Top Outliers (Thưởng cao nhất, Phạt nhiều nhất) kèm nhận định quản trị.

---

## 2. Quy Trình Vận Hành 5 Bước (SOP)

Khi người dùng kích hoạt lệnh `/ops-erp-processor` (hoặc `/ops:erp-processor`), Agent thực hiện tuần tự:

```text
[B1: Tiếp nhận] -> [B2: Kích hoạt Engine] -> [B3: Kiểm tra Đối soát] -> [B4: Tổng hợp Báo cáo] -> [B5: Ghi nhật ký PDCA]
```

### Bước 1: Tiếp nhận và Xác thực Tệp Nguồn
- Kiểm tra đường dẫn do người dùng cung cấp hoặc tự động dò tìm tệp `*ERP*.xlsx` mới nhất trong thư mục `sample-data/`.
- Xác thực tệp có tồn tại và đọc được.

### Bước 2: Kích hoạt Engine Làm Sạch & Tách File
- Thực thi script tự động hóa:
  ```powershell
  powershell -ExecutionPolicy Bypass -File ".agents/skills/ops-erp-processor/scripts/process_erp.ps1" -InputPath "<đường-dẫn-file>"
  ```
- Script sẽ tự động:
  1. Loại bỏ các dòng rác (ghost rows) không có `Employee_ID`.
  2. Chuẩn hóa định dạng số tiền, tính `Net_Salary = Base + Bonus - Penalty`.
  3. Xuất file Master và các file con theo từng Manager vào `outputs/reports/managers/`.
  4. Trích xuất chỉ số tổng hợp ra tệp `outputs/reports/erp_summary_metrics.json`.

### Bước 3: Kiểm Tra Tính Toàn Vẹn Số Học (Zero-Reconciliation Audit)
- Đọc tệp `outputs/reports/erp_summary_metrics.json`.
- Xác nhận:
  - Tổng số lượng nhân viên ở các file con cộng lại bằng đúng `ValidHeadcount`.
  - Tổng tiền `Net_Salary` khớp 100% không lệch 1 đồng.

### Bước 4: Soạn Thảo Executive Operations Brief
- Sử dụng khung mẫu tại `resources/report_template.md` kết hợp dữ liệu trong `erp_summary_metrics.json` để tạo báo cáo quản trị:
  - Tóm tắt KPI: Tổng quỹ lương, tỷ trọng thưởng/phạt trên lương cơ bản.
  - Phân tích cơ cấu chi phí theo 4 Bộ phận (Operations, Sales, Finance, HR).
  - Phân tích hiệu suất theo 4 Quản lý.
  - Cảnh báo bất thường: Top 5 nhân sự bị phạt nhiều nhất (Outliers > 1.5 triệu) và Top 5 nhân sự nhận thưởng cao nhất.
  - 2 đề xuất hành động thực tiễn (Actionable Recommendations) cho Giám đốc Vận hành (COO) và Trưởng phòng Nhân sự (HRD).

### Bước 5: Cập Nhật Hồ Sơ Dự Án
- Ghi nhận kết quả vào `docs/pdca-log.md` theo quy tắc PDCA bắt buộc.

---

## 3. Cấu Trúc Thư Mục Skill

```text
.agents/skills/ops-erp-processor/
├── SKILL.md                          # Trí tuệ điều phối & hướng dẫn Agent
├── scripts/
│   └── process_erp.ps1               # Engine làm sạch OpenXML, tách file & trích xuất JSON
├── resources/
│   └── report_template.md            # Khung mẫu báo cáo phân tích quản trị
└── examples/
    └── erp-sample-run.md             # Ví dụ thực thi mẫu và log đối soát
```

---

## 4. Negative Triggers (Khi nào KHÔNG dùng skill này)
- Không dùng cho việc import dữ liệu vào cơ sở dữ liệu SQL production.
- Không dùng cho việc tính toán thuế thu nhập cá nhân lũy tiến phức tạp (cần skill chuyên dụng về kế toán/thuế).
- Không dùng khi file nguồn không phải là định dạng Excel hoặc dữ liệu không có các cột định danh tối thiểu.
