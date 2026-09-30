# Báo Cáo Phân Tích Quản Trị Vận Hành & Quỹ Lương (Kỳ {{MONTH}})

**Thời điểm xử lý:** {{PROCESSED_AT}}  
**Tệp nguồn ERP:** `{{SOURCE_FILE}}`  
**Đơn vị lập:** Operations Department / Antigravity Agent  

---

## 1. Tổng Quan Chỉ Số Điều Hành (Executive KPI Summary)

| Chỉ Số Cốt Lõi | Giá Trị (VNĐ / Số lượng) | Tỷ Trọng / Tỷ Lệ | Ghi Chú Đánh Giá |
|---|---|---|---|
| **Tổng nhân sự hợp lệ** | {{VALID_HEADCOUNT}} nhân sự | 100% | Đã lọc sạch {{GHOST_ROWS}} dòng rác từ ERP |
| **Tổng lương cơ bản (Base)** | {{TOTAL_BASE}} VNĐ | 100% | Chi phí cố định hàng tháng |
| **Tổng tiền thưởng (Bonus)** | {{TOTAL_BONUS}} VNĐ | {{BONUS_RATE}}% | Thưởng hiệu suất công việc |
| **Tổng tiền phạt (Penalty)** | {{TOTAL_PENALTY}} VNĐ | {{PENALTY_RATE}}% | Khấu trừ vi phạm nội quy/SOP |
| **Tổng thực lĩnh (Net Salary)**| {{TOTAL_NET}} VNĐ | — | Quỹ lương giải ngân thực tế |

---

## 2. Phân Tích Cơ Cấu Chi Phí Theo Bộ Phận (Department Breakdown)

| Bộ Phận | Nhân Sự | Lương Cơ Bản (VNĐ) | Thưởng (VNĐ) | Phạt (VNĐ) | Thực Lĩnh (VNĐ) | Thu Nhập TB/Người |
|---|---|---|---|---|---|---|
{{DEPARTMENT_TABLE_ROWS}}

---

## 3. Phân Tích Hiệu Suất Theo Cấp Quản Lý (Manager Breakdown)

| Quản Lý | Số Nhân Sự | Tổng Lương Cơ Bản | Tổng Thưởng | Tổng Phạt | Tổng Thực Lĩnh | File Excel Bàn Giao |
|---|---|---|---|---|---|---|
{{MANAGER_TABLE_ROWS}}

---

## 4. Nhận Diện Bất Thường & Rủi Ro Vận Hành (Operational Outliers)

### Top 5 Nhân Sự Nhận Thưởng Cao Nhất
{{TOP_BONUS_LIST}}

### Top 5 Nhân Sự Bị Khấu Trừ Phạt Nhiều Nhất
{{TOP_PENALTY_LIST}}

---

## 5. Nhận Định Chiến Lược & Khuyến Nghị Hành Động (PDCA Act)

1. **Về cơ cấu chi phí bộ phận:**
   - {{INSIGHT_DEPT}}
2. **Về rủi ro kỷ luật & thưởng phạt:**
   - {{INSIGHT_PENALTY}}
3. **Đề xuất hành động cho Ban Giám Đốc:**
   - **Hành động 1 (COO):** {{ACTION_1}}
   - **Hành động 2 (HRD):** {{ACTION_2}}
