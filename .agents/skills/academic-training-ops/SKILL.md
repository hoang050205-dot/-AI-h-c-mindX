---
name: academic-training-ops
description: "Tự động hóa quy trình quản trị dữ liệu học vụ: tự tìm kiếm/thu thập dữ liệu học viên phân tán, quét sạch bản ghi rác & trùng lặp, chuẩn hóa thang điểm số học 0-10, bảo mật PII, tạo bảng tính Master Excel đa sheet và xuất báo cáo phân tích hiệu suất sư phạm theo từng Giảng viên gửi Ban Giám Đốc. Hỗ trợ lệnh /academic-training-ops hoặc /academic:training-ops."
user-invocable: true
when_to_use: "Sử dụng khi nhân viên đào tạo (Training/Academic) cần tổng hợp điểm học viên từ nhiều nguồn khác nhau (web, link khảo sát, form, file rải rác), cần làm sạch dữ liệu, lập bảng điểm chuẩn hóa và xuất báo cáo đánh giá chất lượng giảng dạy theo từng giảng viên."
category: workflow
keywords: [academic-training-ops, academic:training-ops, student-grades, teacher-kpi, academic-report, data-cleaning, grade-analytics, ai4a]
argument-hint: "[path-to-raw-data.json] [--teachers] [--report] [--dry-run]"
metadata:
  author: "Academic Training Officer / Antigravity AI"
  course: "Agentic AI with Google Antigravity (AI4A)"
  version: "1.0.0"
---

# ACADEMIC: Training Operations — Quản Trị Dữ Liệu Học Vụ & Báo Cáo Giảng Viên

> **Đóng gói chuẩn Antigravity Customization System**  
> *Hỗ trợ Nhân viên Đào tạo (Academic/Training Officer) tự động hóa 90% thời gian thu thập, làm sạch điểm số và lập báo cáo chất lượng giảng dạy.*

---

## 1. Bản Hợp Đồng Thực Thi (Core Contract)

1. **🎯 Outcome:**
   - 1 tệp Master Cleaned Excel lưu tại `outputs/reports/Academic_Student_Grades_Master.xlsx` (2 sheet: Bảng điểm học viên sạch 100% và Bảng tổng hợp KPI giảng viên).
   - 1 tệp JSON chỉ số phân tích lưu tại `outputs/reports/academic_summary_metrics.json`.
   - 1 bản báo cáo phân tích sư phạm điều hành tại `outputs/reports/Academic_Teacher_Performance_Report.md`.
2. **🛡️ Constraints:**
   - **Bảo mật PII:** Ẩn hoặc loại bỏ SĐT cá nhân, Email cá nhân của học viên; chỉ giữ `Student_ID` và Họ tên hiển thị.
   - **Toàn vẹn số học (Deterministic Scoring):** Điểm số bắt buộc ép kiểu float (0.0 - 10.0). Xử lý vắng thi quy về 0.0 theo quy chế.
   - **Không phụ thuộc thư viện ngoài:** Script PowerShell chạy offline trên Windows, tương thích OpenXML native qua `System.IO.Compression`.
3. **🚫 Non-goals:**
   - Không tự ý gửi email cảnh báo điểm trực tiếp cho học viên/phụ huynh nếu chưa có phê duyệt (Human Checkpoint).
   - Không ghi đè trực tiếp vào cơ sở dữ liệu core LMS/ERP của trung tâm.
   - Không sử dụng AI tự động chấm bài luận.
4. **✅ Acceptance Criteria:**
   - Tỷ lệ trùng lặp: **0%** (khử trùng theo `Student_ID` + `Class_ID`).
   - Loại bỏ 100% ghost rows và điểm ngoài thang (0-10).
   - 100% giảng viên có đủ chỉ số KPI: Sĩ số, Tỷ lệ Đạt (Pass Rate %), Điểm TB, Tỷ lệ Khá/Giỏi, Độ lệch chuẩn phân phối điểm (Std Dev).
   - File Excel mở mượt mà trên Excel Desktop, WPS Office với **0% lỗi công thức** (`#DIV/0!`, `#REF!`).

---

## 2. Quy Trình Vận Hành 5 Bước (SOP)

Khi người dùng kích hoạt lệnh `/academic-training-ops` (hoặc `/academic:training-ops`), Agent thực hiện tuần tự:

```text
[B1: Tiếp nhận/Thu thập] -> [B2: Kích hoạt Engine] -> [B3: Kiểm tra Đối soát] -> [B4: Soạn Executive Brief] -> [B5: Ghi nhật ký PDCA]
```

### Bước 1: Tiếp Nhận và Thu Thập Dữ Liệu Nguồn (Harvesting)
- Kiểm tra đường dẫn do người dùng chỉ định hoặc tự động dò tìm file `*raw_student*.json` trong `sample-data/`.
- Nếu dữ liệu chưa có sẵn, kích hoạt cơ chế thu thập web hoặc nạp bộ giả lập dữ liệu chuẩn hóa của trung tâm.

### Bước 2: Kích Hoạt Engine Làm Sạch & Xuất Excel
- Thực thi script tự động hóa:
  ```powershell
  powershell -ExecutionPolicy Bypass -File ".agents/skills/academic-training-ops/scripts/process_academic.ps1" -InputPath "sample-data/raw_student_scores.json"
  ```
- Script sẽ tự động:
  1. Loại bỏ các dòng rác (ghost rows) không có mã học viên/lớp.
  2. Khử trùng lặp bản ghi theo khóa kết hợp (`Student_ID` + `Class_ID`).
  3. Chuẩn hóa chuỗi text điểm ("8.5 điểm", "9,0", "Vắng") thành số thực chuẩn (float).
  4. Tính điểm Tổng kết: $\text{TK} = \text{Round}(\text{Chuyên cần}\times 10\% + \text{Giữa kỳ}\times 30\% + \text{Cuối kỳ}\times 60\%, 2)$.
  5. Xếp loại học lực (Xuất sắc, Giỏi, Khá, Trung bình, Yếu) và trạng thái Pass/Fail (Pass $\ge 5.0$).
  6. Masking dữ liệu cá nhân nhạy cảm (PII).
  7. Sinh file Master Excel 2 sheet với format bảng biểu chuẩn tại `outputs/reports/Academic_Student_Grades_Master.xlsx`.
  8. Trích xuất chỉ số tổng hợp ra tệp `outputs/reports/academic_summary_metrics.json`.

### Bước 3: Kiểm Tra Tính Toàn Vẹn Số Học (Zero-Reconciliation Audit)
- Đọc tệp `outputs/reports/academic_summary_metrics.json`.
- Xác nhận:
  - Tổng số học viên ở các lớp cộng lại bằng đúng `Valid_Student_Count`.
  - Không có học viên nào có điểm tổng kết $< 0.0$ hoặc $> 10.0$.
  - Tỷ lệ trùng lặp $= 0\%$.

### Bước 4: Soạn Thảo Báo Cáo Sư Phạm Điều Hành (Executive Brief)
- Áp dụng khung mẫu tại `resources/report_template.md` kết hợp dữ liệu trong `academic_summary_metrics.json`:
  - Đánh giá tổng quan: Tổng số học viên hợp lệ, Pass Rate chung, Điểm TB toàn trung tâm.
  - Xếp hạng hiệu suất đào tạo theo từng Giảng viên.
  - Phân tích hiện tượng phân cực và cảnh báo nguy cơ:
    - Nhận diện giảng viên có tỷ lệ rớt cao / bài tập quá nặng cần phụ đạo.
    - Nhận diện giảng viên có nguy cơ lạm phát điểm (Grade Inflation: tỷ lệ Giỏi/XS > 70%, độ lệch chuẩn < 0.5).
  - Đề xuất 3 nhóm hành động cụ thể cho Giảng viên, Học viên và Ban Giám Đốc.

### Bước 5: Cập Nhật Hồ Sơ Dự Án (PDCA Log)
- Ghi nhận đầy đủ vòng lặp PDCA vào `docs/pdca-log.md`.
