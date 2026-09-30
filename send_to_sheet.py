# -*- coding: utf-8 -*-
"""
=============================================================================
AI FINANCE AGENT — AUTOMATED EXPENSE AUDIT & GOOGLE SHEETS SYNC
=============================================================================
Dự án: MindX Agentic AI with Google Antigravity - Buổi 12
Chức năng:
  1. Đọc dữ liệu chi tiêu thô từ data.json.
  2. Đóng vai trò AI Finance Agent:
     - Tự động phân loại danh mục (Category).
     - Kiểm tra và thực thi Rule tài chính: Khoản chi > 500.000 VNĐ bắt buộc
       phải có hóa đơn/chứng từ hợp lệ và phê duyệt cấp quản lý.
     - Đánh giá trạng thái (Status: Hop le, Can chung tu, Can xem lai).
     - Tạo ghi chú tài chính chuyên nghiệp (AI Note).
  3. Chuẩn hóa cấu trúc JSON theo chuẩn 7 trường:
     [Date, Employee, Item, Amount, Category, Status, AI Note].
  4. Đẩy dữ liệu tự động lên Google Sheets qua Google Apps Script Web App REST API.
=============================================================================
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import requests

# Cấu hình mã hóa UTF-8 cho console Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Cấu hình logging với UTF-8 stream handler
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
logger = logging.getLogger("AIFinanceAgent")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Hằng số cấu hình
DEFAULT_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwL9agmPIYTCQxYr-f1fJQT-FbL54Z5bI6Ggw4oR4MZPVB8jq3SG5nkcf7TOLMrSA9x6g/exec"
THRESHOLD_AMOUNT = 500000  # Ngưỡng quy tắc tài chính: > 500k cần chứng từ/phê duyệt

POTENTIAL_DATA_PATHS = [
    Path(r"C:\Minh Hoang\Antigravity học\data.json"),
    Path(__file__).parent / "data.json",
    Path(__file__).parent / "sample-data" / "data.json",
]


class AIFinanceAgent:
    """Agent AI Tài chính chuyên trách kiểm duyệt, phân loại chi tiêu nội bộ."""

    def __init__(self, threshold: int = THRESHOLD_AMOUNT):
        self.threshold = threshold

    def classify_category(self, item: str, current_category: str = "") -> str:
        """Chuẩn hóa phân loại danh mục chi phí nếu chưa có hoặc cần tối ưu."""
        if current_category:
            return current_category

        item_lower = item.lower()
        if any(w in item_lower for w in ["tiep khach", "khach hang", "doi tac", "an toi"]):
            return "Tiep khach"
        elif any(w in item_lower for w in ["taxi", "grab", "xe", "di lai", "di chuyen"]):
            return "Di chuyen"
        elif any(w in item_lower for w in ["ca phe", "tra sua", "com", "an uong", "snack"]):
            return "An uong"
        elif any(w in item_lower for w in ["van phong pham", "but", "giay", "in an", "van phong"]):
            return "Van phong"
        return "Chi phi khac"

    def evaluate_rule(self, item: str, amount: int, current_status: str = "", current_note: str = "") -> tuple[str, str]:
        """
        Đánh giá khoản chi theo quy chuẩn tài chính nội bộ:
        - Rule 1: Chi phí > 500k bắt buộc cần hóa đơn/chứng từ hợp lệ & phê duyệt cấp quản lý.
        - Rule 2: Chi phí liên quan trực tiếp khách hàng cần biên lai/hóa đơn dịch vụ.
        - Rule 3: Chi tiêu nội bộ dưới hạn mức được phê duyệt hợp lệ.
        """
        # Nếu đã có Status và AI Note chuẩn, giữ nguyên và tinh chỉnh nếu cần
        if current_status and current_note:
            return current_status, current_note

        item_lower = item.lower()
        if amount > self.threshold:
            status = "Can xem lai"
            note = (
                f"Khoản chi lớn hơn {self.threshold:,.0f}đ, cần phê duyệt cấp quản lý "
                f"và bổ sung đầy đủ hóa đơn/chứng từ hợp lệ."
            )
        elif any(w in item_lower for w in ["khach", "gap khach", "tiep khach"]):
            status = "Can chung tu"
            note = "Khoản chi liên quan đến khách hàng, cần cung cấp hóa đơn/biên lai dịch vụ."
        else:
            status = "Hop le"
            note = "Chi phí hoạt động nội bộ thông thường, mức chi nằm trong hạn mức cho phép."

        return status, note

    def process_records(self, raw_expenses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Duyệt qua danh sách chi phí, phân loại và sinh cấu trúc JSON chuẩn hóa."""
        processed = []
        for exp in raw_expenses:
            date_val = exp.get("Date", "")
            emp_val = exp.get("Employee", "")
            item_val = exp.get("Item", "")
            amount_val = int(exp.get("Amount", 0))

            category_val = self.classify_category(item_val, exp.get("Category", ""))
            status_val, note_val = self.evaluate_rule(
                item=item_val,
                amount=amount_val,
                current_status=exp.get("Status", ""),
                current_note=exp.get("AI Note", "")
            )

            standardized_record = {
                "Date": date_val,
                "Employee": emp_val,
                "Item": item_val,
                "Amount": amount_val,
                "Category": category_val,
                "Status": status_val,
                "AI Note": note_val
            }
            processed.append(standardized_record)

        return processed


def load_expense_data() -> tuple[Path, Dict[str, Any]]:
    """Tìm và đọc file data.json với hỗ trợ mã hóa UTF-8."""
    target_path = None
    for p in POTENTIAL_DATA_PATHS:
        if p.exists() and p.is_file():
            target_path = p
            break

    if not target_path:
        raise FileNotFoundError(
            f"Không tìm thấy file data.json tại các vị trí đã kiểm tra: {[str(p) for p in POTENTIAL_DATA_PATHS]}"
        )

    logger.info(f"Đọc dữ liệu chi tiêu từ file: {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return target_path, data


def send_to_google_sheet(payload: Dict[str, Any], webapp_url: str = DEFAULT_WEBAPP_URL) -> Dict[str, Any]:
    """Gửi payload JSON chuẩn hóa đến Google Apps Script Web App qua HTTP POST."""
    logger.info(f"Gửi dữ liệu ({len(payload.get('expenses', []))} bản ghi) đến Google Apps Script...")
    logger.info(f"Web App URL: {webapp_url}")

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.post(
            webapp_url,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        logger.info(f"Phản hồi từ Google Apps Script: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi khi gửi dữ liệu sang Google Apps Script: {e}")
        raise


def print_summary_table(expenses: List[Dict[str, Any]]):
    """In bảng tổng hợp kết quả đánh giá của AI Finance Agent ra console."""
    print("\n" + "=" * 115)
    print(f"{'BẢNG TỔNG HỢP KIỂM DUYỆT CHI TIÊU — AI FINANCE AGENT':^115}")
    print("=" * 115)
    header = f"| {'Ngày':^6} | {'Nhân viên':^10} | {'Nội dung chi tiêu':^24} | {'Số tiền (VNĐ)':^14} | {'Danh mục':^12} | {'Trạng thái':^14} | {'AI Ghi chú & Đánh giá':^20}"
    print(header)
    print("|" + "-" * 8 + "|" + "-" * 12 + "|" + "-" * 26 + "|" + "-" * 16 + "|" + "-" * 14 + "|" + "-" * 16 + "|" + "-" * 32 + "|")

    total_amount = 0
    over_threshold_count = 0

    for item in expenses:
        total_amount += item["Amount"]
        if item["Amount"] > THRESHOLD_AMOUNT:
            over_threshold_count += 1

        amt_str = f"{item['Amount']:,}"
        note_display = (item["AI Note"][:28] + "..") if len(item["AI Note"]) > 30 else item["AI Note"]
        row = f"| {item['Date']:^6} | {item['Employee']:^10} | {item['Item']:<24} | {amt_str:>14} | {item['Category']:<12} | {item['Status']:^14} | {note_display:<30} |"
        print(row)

    print("=" * 115)
    print(f"Tổng số khoản chi: {len(expenses)} | Tổng giá trị: {total_amount:,.0f} VNĐ | Số khoản chi > {THRESHOLD_AMOUNT:,.0f}đ (cần chứng từ/duyệt): {over_threshold_count}")
    print("=" * 115 + "\n")


def main():
    print("\n[AI FINANCE AGENT] KHỞI ĐỘNG HỆ THỐNG XỬ LÝ & ĐỒNG BỘ GOOGLE SHEETS...")
    
    # 1. Đọc dữ liệu chi tiêu thô
    data_file, raw_data = load_expense_data()
    raw_expenses = raw_data.get("expenses", [])
    logger.info(f"Đã nạp thành công {len(raw_expenses)} khoản chi từ {data_file.name}")

    # 2. Xử lý qua AI Finance Agent
    agent = AIFinanceAgent(threshold=THRESHOLD_AMOUNT)
    processed_expenses = agent.process_records(raw_expenses)

    # 3. Chuẩn hóa payload
    payload = {"expenses": processed_expenses}

    # In bảng trực quan
    print_summary_table(processed_expenses)

    # Xuất định dạng JSON chuẩn
    print("[JSON OUTPUT CHUẨN HÓA]:")
    print(json.dumps(payload, ensure_ascii=False, indent=4))
    print()

    # 4. Gửi đến Google Sheet qua Web App
    result = send_to_google_sheet(payload, DEFAULT_WEBAPP_URL)

    if result.get("success"):
        updated = result.get("updatedRows", len(processed_expenses))
        print(f"\n✅ ĐỒNG BỘ THÀNH CÔNG! Đã cập nhật {updated} dòng dữ liệu lên Google Sheets.")
    else:
        print(f"\n❌ ĐỒNG BỘ THẤT BẠI: {result.get('error', 'Lỗi không xác định')}")


if __name__ == "__main__":
    main()
