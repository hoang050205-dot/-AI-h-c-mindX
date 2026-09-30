# Nhật Ký Thực Thi Mẫu: Academic Training Operations (AI4A)

**Kỳ thực nghiệm:** Đợt 1 — Khóa K26  
**Dữ liệu đầu vào:** `sample-data/raw_student_scores.json` (45 bản ghi thu thập từ 4 nguồn phân tán)  
**Công cụ kích hoạt:** `.agents/skills/academic-training-ops/scripts/process_academic.ps1`  
**Thời gian thực thi:** < 2 giây  

---

## 1. Nhật Ký Tiến Trình Pipeline

```text
==========================================================
[START] ACADEMIC TRAINING OPS PIPELINE DANG KHOI CHAY...
==========================================================
[INFO] Doc du lieu tu tap tin: sample-data/raw_student_scores.json
[STAGE 1 - HARVEST] Thu thap thanh cong 45 ban ghi tho.
[STAGE 2 - CLEANSE] Ket qua lam sach du lieu:
  - So ban ghi hop le: 39
  - Ghost rows da loai bo: 2
  - Ban ghi trung lap da loai bo: 3
  - Ban ghi diem ngoai pham vi (0-10): 1
  - Ho so da duoc bao mat PII: 39
[STAGE 3 - EXCEL ENGINE] Dang sinh file Excel Master da sheet...
[SUCCESS] Da tao thanh cong Excel Master da sheet tai: outputs\reports\Academic_Student_Grades_Master.xlsx
[SUCCESS] Da xuat chi so phan tich JSON tai: outputs\reports\academic_summary_metrics.json
==========================================================
[DONE] PIPELINE HOAN TAT 100% TIEN TRINH!
==========================================================
```

---

## 2. Kết Quả Đối Soát Số Học (Audit Metrics)

- **Tổng số bản ghi thô nạp vào:** 45 bản ghi
- **Bản ghi rác đã loại bỏ (Purged):** 6 bản ghi (13.3%)
  - 2 ghost rows (thiếu mã học viên hoặc thông tin rác hệ thống)
  - 3 bản ghi trùng lặp chính xác theo cặp (`Student_ID`, `Class_ID`)
  - 1 bản ghi lỗi điểm số ngoài phạm vi ($>10$ hoặc âm)
- **Số học viên thực tế sau làm sạch:** **39 học viên** (100% dữ liệu hợp lệ)
- **Tỷ lệ Pass Rate toàn trung tâm:** **84.6%** (33/39 học viên đạt môn)
- **Điểm trung bình toàn trung tâm:** **7.59 / 10.0**
- **Tỷ lệ Khá / Giỏi / Xuất sắc:** **56.4%**

---

## 3. Tổng Hợp Chỉ Số 4 Giảng Viên

| Giảng Viên | Lớp Phụ Trách | Sĩ Số | Đạt (Pass) | Rớt (Fail) | Tỷ Lệ Pass (%) | Điểm TB | Độ Phân Hóa (Std Dev) | Nhận Định Sư Phạm |
|---|---|---|---|---|---|---|---|---|
| **Thầy Nguyễn Hoàng Nam** | `PY101-K26` (Python Core) | 10 | 9 | 1 | 90.0% | 7.50 | 1.70 | Hiệu suất rất tốt; phổ điểm chuẩn Gauss |
| **Cô Trần Mai Anh** | `DA201-K26` (Data Analysis) | 9 | 8 | 1 | 88.9% | 6.72 | 1.21 | Đạt chuẩn yêu cầu; kiểm soát thi nghiêm túc |
| **Thầy Lê Quốc Bảo** | `AI301-K26` (Machine Learning) | 10 | 6 | 4 | 60.0% | 6.96 | 2.46 | Cảnh báo tỷ lệ rớt cao; phân hóa rất mạnh |
| **Cô Phạm Thùy Linh** | `FE102-K26` (Frontend Web) | 10 | 10 | 0 | 100.0% | 9.11 | 0.42 | Cảnh báo lạm phát điểm (chấm quá nương tay) |

---

## 4. Kiểm Nghiệm File Excel Master Đầu Ra

Tệp `outputs/reports/Academic_Student_Grades_Master.xlsx` được sinh ra hoàn chỉnh gồm 2 sheet:
1. `Student_Grades_Cleaned`: Bảng chi tiết 39 học viên, có định dạng màu xen kẽ (zebra striping), căn chỉnh số học và trạng thái `PASS` được tô nền xanh chuẩn mực.
2. `Teacher_KPI_Summary`: Bảng tổng hợp các chỉ số sư phạm phục vụ báo cáo nhanh cho Ban Giám Đốc.
