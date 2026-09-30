# Báo Cáo Phân Tích Chất Lượng Đào Tạo & Đánh Giá Giảng Viên (AI4A)

**Kỳ báo cáo:** `{{period}}`  
**Đơn vị:** Phòng Đào Tạo & Quản Lý Học Vụ (Academic Department)  
**Người lập:** `{{author}}` (Nhân viên Đào tạo)  
**Kính gửi:** Ban Giám Đốc & Hội Đồng Sư Phạm  
**Tập dữ liệu chuẩn hóa:** `{{master_excel_path}}`  

---

## 1. Tổng Quan Hiệu Suất Đào Tạo (Executive KPI Overview)

| Chỉ Số Vận Hành | Giá Trị Tổng Thể | Đánh Giá Chuẩn Sư Phạm |
|---|---|---|
| **Tổng số lớp đào tạo** | `{{total_classes}}` lớp | Hoàn thành tiến độ |
| **Tổng số học viên (Hợp lệ)** | `{{total_students}}` học viên | Tỷ lệ dữ liệu sạch 100% |
| **Bản ghi rác đã lọc sạch** | `{{purged_records}}` bản ghi | Gồm ghost rows, duplicate, lỗi text |
| **Tỷ lệ Đạt Môn chung (Pass Rate)** | `{{overall_pass_rate}}%` | `{{pass_rate_assessment}}` |
| **Điểm Trung Bình toàn trung tâm** | `{{overall_avg_score}}` / 10 | Phân phối chuẩn Gauss |
| **Tỷ lệ học viên Khá - Giỏi - Xuất sắc** | `{{good_excellent_rate}}%` | Phản ánh chất lượng chuẩn đầu ra |

---

## 2. Bảng Xếp Hạng & Chỉ Số Chi Tiết Từng Giảng Viên

| Giảng Viên Phụ Trách | Khóa Học / Lớp | Sĩ Số | Điểm TB Lớp | Tỷ Lệ Pass (%) | Tỷ Lệ Giỏi/XS (%) | Độ Phân Hóa (Std Dev) | Nhận Định Sư Phạm |
|---|---|---|---|---|---|---|---|
{{teacher_table_rows}}

---

## 3. Phân Tích Chuyên Sâu & Phát Hiện Bất Thường (Outlier Detection)

### 3.1. Giảng viên có hiệu suất đào tạo xuất sắc & độ phân hóa chuẩn
{{outstanding_teachers_analysis}}

### 3.2. Cảnh báo lớp học có tỷ lệ rớt cao / phân hóa phân cực (Cần can thiệp)
{{at_risk_classes_analysis}}

### 3.3. Cảnh báo lạm phát điểm số (Grade Inflation Alert)
{{grade_inflation_analysis}}

---

## 4. Đề Xuất Hành Động Thực Tiễn (Actionable Recommendations)

1. **Đối với Giảng viên:**
   - `{{rec_for_teachers}}`
2. **Đối với Học viên có nguy cơ:**
   - `{{rec_for_students}}`
3. **Đối với Phòng Đào tạo & Ban Giám đốc:**
   - `{{rec_for_board}}`

---

*Báo cáo được khởi tạo tự động bởi Custom Skill `academic:training-ops` (AI4A Framework).*
