/4

# Brainstorm Decision Brief: Tự Động Hóa Dữ Liệu Đào Tạo & Báo Cáo Hiệu Suất Giảng Viên

**Dự án:** Xây dựng Custom Skill Quản trị Dữ liệu Học vụ & Đánh giá Giảng viên (`academic:training-ops`)
**Vai trò:** Nhân viên Đào tạo (Academic / Training Officer)
**Học viên:** Minh Hoàng
**Mentor:** MT Đức Thuận
**Khung tham chiếu:** AI4A Brainstorm Contract (`ai4a:brainstorm`)
**Ngày thực hiện:** 11/09/2026

---

## 1. Bản Hợp Đồng Thực Thi (The 4-Field Contract)

| Trường Hợp Đồng             | Định Nghĩa & Ranh Giới Cụ Thể Nghiệp Vụ Đào Tạo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **🎯 Outcome**             | - Đóng gói Custom Skill`academic:training-ops` tại `.agents/skills/academic-training-ops/`.- Bộ kịch bản thu thập dữ liệu rải rác & chuẩn hóa số học tự động.- File bảng tính Master Excel `outputs/reports/Academic_Student_Grades_Master.xlsx` gồm 2 sheet: (1) Bảng điểm học viên sạch 100%, (2) Bảng KPI tổng hợp theo từng Giảng viên.- Báo cáo Phân tích Sư phạm Điều hành `outputs/reports/Academic_Teacher_Performance_Report.md` gửi Ban Giám Đốc.                                                  |
| **🛡️ Constraints**       | -**Bảo mật & PII:** Nghiêm cấm lưu trữ SĐT cá nhân, số CCCD, Email cá nhân của học viên; chỉ giữ `Student_ID` và Tên hiển thị.- **Toàn vẹn số học:** Ép kiểu float (0.0 - 10.0), không để dính text rác ("Vắng", "8đ", "chưa nộp"). Xử lý vắng thi bằng cờ hoặc 0 điểm theo quy chế.- **Cơ chế Fallback (Offline Mode):** Khi không có đường truyền internet hoặc nguồn cào bị chặn, tự động kích hoạt bộ Synthetic Academic Generator để quy trình không bị gián đoạn. |
| **🚫 Non-goals**           | - Không tự động gửi email thông báo điểm hoặc cảnh báo học vụ trực tiếp tới phụ huynh/học viên (cần Human Approval).- Không can thiệp ghi đè (Write-back API) vào cơ sở dữ liệu core LMS/ERP của trung tâm.- Không sử dụng AI để tự động chấm điểm bài luận học viên trong phạm vi chu kỳ này.                                                                                                                                                                                                                    |
| **✅ Acceptance Criteria** | - Khử sạch 100% bản ghi bất thường (điểm âm, điểm > 10, ký tự lạ).- Tỷ lệ trùng lặp: **0%** (khử trùng theo cặp khóa `Student_ID` + `Class_ID`).- 100% Giảng viên có đủ chỉ số KPI: Sĩ số phụ trách, Tỷ lệ Đạt môn (Pass Rate %), Điểm TB, Tỷ lệ Khá/Giỏi, Độ lệch chuẩn phân phối điểm.- Bảng tính Excel mở được mượt mà trên Excel Desktop/Web/WPS, **0% lỗi công thức** (`#DIV/0!`, `#REF!`, `#VALUE!`).                                                                  |

---

## 2. So Sánh Các Phương Án Kỹ Thuật (Option Exploration)

| Tiêu Chí So Sánh                                         | Approach 1: Lean / Direct                                                                                                         | Approach 2: Workflow / Agentic ⭐*(Khuyên dùng)*                                                                                                                                                                           | Approach 3: Scalable / Advanced                                                                                                 |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Kiến Trúc Tổng Thể**                            | 1 Script Python/PowerShell thuần quét Regex/HTML từ URL/file cố định$\rightarrow$ Làm sạch $\rightarrow$ Xuất Excel. | **Pipeline 3 Tác tử:**1. Harvester Agent (Thu thập/Mockup)2. Cleaner Engine (Chuẩn hóa số học)3. Human Checkpoint4. Academic Analyst Agent (Báo cáo BGĐ).                                                      | Headless Crawler (Playwright) chạy nền định kỳ$\rightarrow$ SQLite Database $\rightarrow$ Web App Streamlit Dashboard. |
| **Ưu Điểm**                                        | - Triển khai siêu nhanh (1-2 giờ).- 0 chi phí token AI.- Chạy offline 100%, dễ lập lịch cron.                             | -**Cân bằng hoàn hảo:** Tính toán số học chính xác tuyệt đối nhờ Code + Nhận định sư phạm sâu sắc nhờ LLM.- Có trạm kiểm duyệt dữ liệu an toàn.- Dễ mở rộng thêm nguồn dữ liệu mới. | - Theo dõi chuỗi thời gian (Time-series) nhiều học kỳ.- Dashboard tương tác lọc đa chiều.                           |
| **Nhược Điểm**                                    | - Kém linh hoạt khi web nguồn đổi giao diện DOM.- Thiếu góc nhìn phân tích định tính và đề xuất sư phạm.      | - Cần quy chuẩn Handoff Schema (JSON trung gian) rõ ràng giữa các giai đoạn.                                                                                                                                           | - Quá cồng kềnh, mất nhiều ngày cài đặt môi trường.- Chi phí vận hành cao, vi phạm nguyên tắc YAGNI/KISS.     |
| **Giả Định Cốt Lõi** *(Key Assumption)*        | Cấu trúc bảng HTML của nguồn giữ nguyên và không yêu cầu đăng nhập.                                                 | Dữ liệu sau bước Cleaner giữ được định danh`Teacher_Name` và các cột điểm chuẩn hóa.                                                                                                                        | Có máy chủ chuyên dụng và trung tâm quản lý hàng chục nghìn học viên.                                             |
| **Điểm Gãy Đầu Tiên** *(First Failure Point)* | Web nguồn đổi class CSS hoặc đổi bố cục cột làm script cào dữ liệu bị crash.                                        | Nguồn cào bị thiếu trường Tên Giảng Viên phụ trách khiến không thể nhóm dữ liệu để tính KPI.                                                                                                               | Playwright bị chặn bởi Cloudflare bot-detection hoặc thiếu thư viện đồ họa trên hệ điều hành.                    |
| **Chi Phí Từ Bỏ** *(Cheapest to Abandon)*        | Cực thấp (1 script đơn).                                                                                                      | **Thấp - Trung bình** (Module hóa độc lập, tái sử dụng được engine).                                                                                                                                         | Rất cao (Sunk cost về hạ tầng DB và giao diện web).                                                                       |

---

## 3. Quyết Định Kiến Trúc & Khuyến Nghị

- **Lựa chọn:** **Approach 2 (Workflow / Agentic Pipeline)** kết hợp Engine làm sạch dữ liệu chuẩn xác (Deterministic Code) và Trí tuệ sư phạm (Agentic Intelligence).
- **Lý do lựa chọn:**
  1. *Nguyên tắc Zero-Hallucination trong Giáo dục:* Điểm số học viên và tỷ lệ Pass/Fail là dữ liệu nhạy cảm, không được để AI tự tính nhẩm mà phải dùng code toán học chính xác 100%.
  2. *Giá trị gia tăng của AI:* LLM phát huy tối đa sức mạnh ở bước phân tích sư phạm: so sánh phổ điểm giữa các giảng viên, phát hiện giảng viên chấm quá gắt hoặc quá dễ dãi, đưa ra khuyến nghị đào tạo cho Ban Giám Đốc.
  3. *An toàn dữ liệu:* Có Human Checkpoint trước khi xuất báo cáo chính thức.
- **Tên Custom Skill đề xuất:** `academic:training-ops` (kích hoạt bằng lệnh `/academic:training-ops`).

---

## 4. Ánh Xạ Các Khung Phương Pháp Luận AI4A

### 4.1. Khung SCOPE (Định hình Dự Án cho `docs/project-brief.md`)

- **S (Situation):** Dữ liệu học viên nằm rải rác trên các bảng điểm link web, Google Form và danh sách lớp; nhân viên đào tạo mất 4-6 tiếng mỗi đợt làm báo cáo thủ công.
- **C (Constraints):** Không lộ PII học viên; chuẩn hóa thang 10; chạy mượt mà offline với Mock Data khi mất mạng.
- **O (Objective):** Tự động hóa 100% quy trình thu thập, làm sạch và xuất báo cáo chất lượng đào tạo chỉ trong < 3 phút.
- **P (Proposal / OIPO):** Pipeline 3 giai đoạn: Thu thập $\rightarrow$ Chuẩn hóa số học $\rightarrow$ Duyệt $\rightarrow$ Phân tích & Xuất báo cáo.
- **E (Evaluation):** 0 bản ghi trùng lặp, 0 lỗi công thức, 100% giảng viên được đánh giá định lượng và định tính.

### 4.2. Khung OIPO (Thiết Kế Luồng Xử Lý Chi Tiết)

- **Objective (Mục tiêu):** Chuẩn hóa bảng điểm học viên và báo cáo hiệu suất giảng dạy theo từng giảng viên.
- **Input (Đầu vào):**
  - URL bảng điểm web công khai / Mockup data: `sample-data/raw_student_scores.json` hoặc danh sách link.
  - Từ điển quy chuẩn môn học & giảng viên: `knowledge-base/academic_rubric.json`.
- **Process (Quy trình 5 trạm):**
  1. *Trạm 1 (Harvester Scout):* Thu thập dữ liệu từ nguồn hoặc kích hoạt bộ sinh Mock Data 100-200 học viên thực tế.
  2. *Trạm 2 (Cleaner Engine):* Khử trùng lặp (`Student_ID`), ép kiểu số thực (0-10), tính điểm Tổng kết theo trọng số: $\text{TK} = \text{Chuyên cần}\times 10\% + \text{Giữa kỳ}\times 30\% + \text{Cuối kỳ}\times 60\%$.
  3. *Trạm 3 (Human Checkpoint):* Nhân viên đào tạo xem lướt bảng tóm tắt chất lượng dữ liệu để bấm duyệt.
  4. *Trạm 4 (Master Excel Generator):* Xuất workbook 2 sheet với định dạng chuyên nghiệp.
  5. *Trạm 5 (Academic Lead Analyst):* Phân tích phân phối điểm (phổ điểm Gauss), đánh giá KPI từng giảng viên, lập đề xuất sư phạm.
- **Output (Đầu ra):**
  - Bảng tính: `outputs/reports/Academic_Student_Grades_Master.xlsx`
  - Báo cáo: `outputs/reports/Academic_Teacher_Performance_Report.md`
  - Dashboard tương tác: `outputs/reports/academic-training-brief.html`

### 4.3. Khung PDCA (Chu kỳ #05 cho `docs/pdca-log.md`)

- **PLAN:** Xây dựng Custom Skill `academic:training-ops` giúp nhân viên đào tạo tự động hóa trọn gói: thu thập dữ liệu rải rác $\rightarrow$ làm sạch số học $\rightarrow$ xuất Excel Master 2 sheet $\rightarrow$ viết báo cáo sư phạm theo từng giảng viên.
- **Hypothesis:** Pipeline kết hợp kịch bản chuẩn hóa số học và Agentic LLM giúp rút ngắn thời gian lập báo cáo học vụ từ 4 giờ xuống < 3 phút, bảo đảm sai số tính toán = 0 và tỷ lệ trùng lặp = 0%.

---

## 5. Câu Hỏi Làm Rõ & Các Giả Định Nghiệp Vụ (Open Questions)

1. **Về Nguồn Dữ Liệu Thực Tế:** Tại trung tâm của bạn, các nguồn dữ liệu rải rác hiện nay cụ thể là những kênh nào? (File Google Sheets của từng lớp, link form khảo sát điểm thi, trang HTML tra cứu điểm của trung tâm, hay chúng ta sẽ xây dựng kèm một bộ dữ liệu mô phỏng thực tế - Synthetic Mock Data gồm 150-200 học viên để chuẩn hóa quy trình trước?).
2. **Về Thang Điểm & Trọng Số:** Trung tâm hiện đang áp dụng công thức tính điểm tổng kết nào? (Ví dụ: Chuyên cần 10% - Giữa kỳ 30% - Cuối kỳ 60%, hay thang điểm chữ GPA 4.0?). Điểm tối thiểu để Đạt môn (Pass) là bao nhiêu? (Ví dụ: $\ge 5.0$ hay $\ge 6.0$?).
3. **Về Tiêu Chí Đánh Giá Giảng Viên:** Ban Giám Đốc quan tâm nhất đến chỉ số nào của Giảng viên? (Tỷ lệ học viên qua môn Pass Rate, Điểm trung bình lớp, Tỷ lệ học viên đạt loại Xuất sắc, hay cần phân tích độ lệch chuẩn để phát hiện giảng viên "chấm điểm quá chặt / quá nương tay"?).
