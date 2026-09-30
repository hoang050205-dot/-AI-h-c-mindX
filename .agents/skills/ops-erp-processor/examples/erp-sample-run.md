# Ví Dụ Mẫu: Thực Thi Skill `ops:erp-processor`

Tài liệu này ghi nhận nhật ký chạy thực tế của Skill `ops:erp-processor` với tập dữ liệu kỳ 2026-03.

## 1. Lệnh Kích Hoạt
```bash
powershell -ExecutionPolicy Bypass -File ".agents/skills/ops-erp-processor/scripts/process_erp.ps1" -InputPath "sample-data/THỰC HÀNH_ERP_OP_BigData_200rows B3.xlsx"
```

## 2. Nhật Ký Bàn Giao Đầu Ra (Output Manifest)

| Tệp Đầu Ra | Đường Dẫn Lưu Trữ | Số Dòng Dữ Liệu | Mục Đích Sử Dụng |
|---|---|:---:|---|
| **Master Excel** | `outputs/reports/ERP_Operations_Master_2026-03.xlsx` | 200 | Báo cáo toàn công ty cho Giám đốc Vận hành (COO) |
| **Manager A** | `outputs/reports/managers/Manager_A_2026-03.xlsx` | 62 | Gửi riêng cho Manager A (Team 62 người) |
| **Manager B** | `outputs/reports/managers/Manager_B_2026-03.xlsx` | 37 | Gửi riêng cho Manager B (Team 37 người) |
| **Manager C** | `outputs/reports/managers/Manager_C_2026-03.xlsx` | 51 | Gửi riêng cho Manager C (Team 51 người) |
| **Manager D** | `outputs/reports/managers/Manager_D_2026-03.xlsx` | 50 | Gửi riêng cho Manager D (Team 50 người) |
| **JSON Metrics** | `outputs/reports/erp_summary_metrics.json` | — | Dữ liệu cấu trúc phục vụ tạo báo cáo & AI Agent |
| **Executive Brief** | `outputs/reports/ERP_Executive_Operations_Report_2026-03.md` | — | Bản tin tóm tắt gửi Ban Giám Đốc |

## 3. Bằng Chứng Đối Soát Số Học (Audit Reconciliation)
- Tổng nhân sự file con: $62 + 37 + 51 + 50 = 200$ (Khớp 100% với file Master).
- Tổng thực lĩnh file con:
  - Manager_A: $1,259,374,500$ VNĐ
  - Manager_B: $759,692,884$ VNĐ
  - Manager_C: $1,086,189,815$ VNĐ
  - Manager_D: $964,937,808$ VNĐ
  - **Tổng cộng:** $4,070,195,007$ VNĐ (Khớp 100% với Master, sai số = 0 VNĐ).
