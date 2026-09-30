# -*- coding: utf-8 -*-
"""
=============================================================================
ENTERPRISE EXPENSE SYNC AGENT — GOOGLE SHEETS AUTOMATION
=============================================================================
Dự án: MindX Agentic AI with Google Antigravity
Tác giả: Chuyên gia Tự động hóa (Automation Specialist)

Chức năng:
  1. Kết nối an toàn Google Cloud OAuth 2.0 qua file credential.json / token.json.
  2. Đọc dữ liệu chi tiêu mới từ file nhân viên (Data_Nhan_Vien).
  3. Ghi dữ liệu thông minh: Chèn nối tiếp (append) vào cuối file kế toán
     (Admin Expense Tracker) mà tuyệt đối không ghi đè dữ liệu cũ.
  4. Chống trùng lặp (Anti-duplication): Tự động tạo/tìm cột 'SyncStatus' trong
     file nhân viên và đánh dấu 'Done' sau khi copy thành công. Các lần chạy
     tiếp theo chỉ xử lý các dòng chưa có chữ 'Done'.
=============================================================================
"""

import sys
import os
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Cấu hình mã hóa UTF-8 cho console Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thiết lập logging chuẩn doanh nghiệp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ExpenseSyncAgent")

# Google Sheets & Drive Scopes chuẩn
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Cấu hình Spreadsheet ID và Sheet GID mặc định
DEFAULT_STAFF_SPREADSHEET_ID = "1WGy9N3QkJvEeSkr14-kVsA50JSMjclJiLJs__xI-uT4"
DEFAULT_STAFF_GID = 1177273027

DEFAULT_ADMIN_SPREADSHEET_ID = "1F8Hmnd0bLy3jJ9XSMtv78_VBamBNUUYqoWkp2MPSPd0"
DEFAULT_ADMIN_GID = 472636171

SYNC_STATUS_COLUMN_NAME = "SyncStatus"
SYNC_DONE_VALUE = "Done"


class GoogleSheetsAuthManager:
    """Quản lý kết nối và xác thực an toàn với Google Cloud theo chuẩn OAuth 2.0."""

    @staticmethod
    def authenticate(
        credential_path: str = "credential.json",
        token_path: str = "token.json"
    ) -> Any:
        """
        Xác thực Google Cloud bằng OAuth 2.0 InstalledAppFlow.
        Lưu phiên làm việc vào token_path để tái sử dụng mà không cần cấp quyền lại.
        """
        import gspread
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request

        # Tìm kiếm file credential nếu đường dẫn mặc định không tồn tại
        cred_candidates = [
            Path(credential_path),
            Path(__file__).parent / credential_path,
            Path("credentials.json"),
            Path(__file__).parent / "credentials.json",
        ]
        
        valid_cred_path = None
        for candidate in cred_candidates:
            if candidate.exists() and candidate.is_file():
                valid_cred_path = candidate
                break

        if not valid_cred_path and not Path(token_path).exists():
            raise FileNotFoundError(
                f"Không tìm thấy file credential.json tại các vị trí: {[str(p) for p in cred_candidates]}. "
                "Vui lòng tải file OAuth 2.0 Client Secrets từ Google Cloud Console và đặt vào thư mục làm việc."
            )

        creds = None
        # 1. Tải token đã cấp quyền trước đó nếu có
        token_file = Path(token_path)
        if token_file.exists():
            logger.info(f"Đang tải phiên xác thực đã lưu từ: {token_file.resolve()}")
            try:
                creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
            except Exception as e:
                logger.warning(f"File token hiện tại không hợp lệ ({e}), tiến hành cấp lại...")
                creds = None

        # 2. Nếu chưa có token hoặc token đã hết hạn
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Phiên làm việc đã hết hạn. Đang tự động làm mới (refresh token)...")
                try:
                    creds.refresh(Request())
                    logger.info("Làm mới phiên làm việc thành công!")
                except Exception as e:
                    logger.warning(f"Không thể làm mới token ({e}). Cần xác thực lại qua trình duyệt.")
                    creds = None

            if not creds:
                if not valid_cred_path:
                    raise FileNotFoundError(f"Cần file credential.json để xác thực lần đầu.")
                
                logger.info(f"Khởi động luồng xác thực Google Cloud OAuth 2.0 từ: {valid_cred_path.name}")
                logger.info("Trình duyệt web sẽ được mở để bạn đăng nhập và cấp quyền truy cập...")
                flow = InstalledAppFlow.from_client_secrets_file(str(valid_cred_path), SCOPES)
                creds = flow.run_local_server(port=0)

            # Lưu token cho các lần chạy tiếp theo
            with open(token_path, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
            logger.info(f"Đã lưu phiên làm việc an toàn vào: {token_path}")

        client = gspread.authorize(creds)
        logger.info("Xác thực Google Cloud OAuth 2.0 thành công!")
        return client


class ExpenseSyncAgent:
    """Agent chuyên gia Tự động hóa đồng bộ dữ liệu chi tiêu giữa các Google Sheets."""

    def __init__(
        self,
        gspread_client: Any,
        staff_sheet_id: str = DEFAULT_STAFF_SPREADSHEET_ID,
        staff_gid: int = DEFAULT_STAFF_GID,
        admin_sheet_id: str = DEFAULT_ADMIN_SPREADSHEET_ID,
        admin_gid: int = DEFAULT_ADMIN_GID,
        dry_run: bool = False
    ):
        self.client = gspread_client
        self.staff_sheet_id = staff_sheet_id
        self.staff_gid = staff_gid
        self.admin_sheet_id = admin_sheet_id
        self.admin_gid = admin_gid
        self.dry_run = dry_run

        self.staff_ws = None
        self.admin_ws = None

    def _get_worksheet_by_gid(self, spreadsheet_key: str, gid: int) -> Any:
        """Mở bảng tính và tìm chính xác sheet dựa trên GID (ID trang tính)."""
        spreadsheet = self.client.open_by_key(spreadsheet_key)
        for ws in spreadsheet.worksheets():
            if ws.id == int(gid):
                return ws
        logger.warning(f"Không tìm thấy sheet có GID={gid} trong '{spreadsheet.title}'. Dùng sheet đầu tiên: '{spreadsheet.sheet1.title}'")
        return spreadsheet.sheet1

    def connect(self):
        """Kết nối đến cả 2 bảng tính của Nhân viên và Kế toán."""
        logger.info("Đang kết nối đến Google Sheets...")
        
        # 1. Bảng tính Nhân viên
        logger.info(f"Mở bảng tính Nhân viên (ID: {self.staff_sheet_id}, GID: {self.staff_gid})...")
        self.staff_ws = self._get_worksheet_by_gid(self.staff_sheet_id, self.staff_gid)
        logger.info(f"-> Đã kết nối Sheet Nhân viên: '{self.staff_ws.spreadsheet.title}' > Sheet: '{self.staff_ws.title}'")

        # 2. Bảng tính Kế toán
        logger.info(f"Mở bảng tính Kế toán (ID: {self.admin_sheet_id}, GID: {self.admin_gid})...")
        self.admin_ws = self._get_worksheet_by_gid(self.admin_sheet_id, self.admin_gid)
        logger.info(f"-> Đã kết nối Sheet Kế toán: '{self.admin_ws.spreadsheet.title}' > Sheet: '{self.admin_ws.title}'")

    def ensure_sync_column(self, headers: List[str]) -> Tuple[int, bool]:
        """
        Tìm kiếm hoặc tự động tạo cột 'SyncStatus' trong sheet Nhân viên.
        Trả về (chỉ_số_cột_1_based, vừa_tạo_mới).
        """
        normalized_headers = [h.strip().lower() for h in headers]
        
        for idx, h in enumerate(normalized_headers):
            if h in ["syncstatus", "sync_status", "sync status", "trang thai dong bo", "trạng thái đồng bộ"]:
                logger.info(f"Đã phát hiện cột trạng thái đồng bộ: '{headers[idx]}' tại cột {idx + 1}")
                return idx + 1, False

        # Chưa có cột SyncStatus -> Tự động thêm vào cột tiếp theo
        new_col_idx = len(headers) + 1
        logger.info(f"Chưa có cột '{SYNC_STATUS_COLUMN_NAME}'. Đang tự động tạo tại cột {new_col_idx}...")
        
        if not self.dry_run:
            self.staff_ws.update_cell(1, new_col_idx, SYNC_STATUS_COLUMN_NAME)
            logger.info(f"-> Đã tạo thành công cột '{SYNC_STATUS_COLUMN_NAME}' tại ô (1, {new_col_idx})")
        else:
            logger.info(f"[DRY-RUN] Sẽ tạo cột '{SYNC_STATUS_COLUMN_NAME}' tại cột {new_col_idx}")

        return new_col_idx, True

    def scan_expenses(self) -> Tuple[List[Dict[str, Any]], List[str], int]:
        """
        Quét toàn bộ dữ liệu từ sheet Nhân viên và lọc ra những dòng mới chưa đồng bộ.
        """
        all_values = self.staff_ws.get_all_values()
        if not all_values:
            logger.warning("Bảng tính Nhân viên hoàn toàn trống!")
            return [], [], 0

        headers = all_values[0]
        sync_col_idx, just_created = self.ensure_sync_column(headers)
        
        if just_created:
            # Cập nhật danh sách headers nội bộ
            headers = list(headers) + [SYNC_STATUS_COLUMN_NAME]

        # Xác định cột số tiền để tính tổng chi tiêu
        amount_col_idx = None
        for idx, h in enumerate(headers):
            hl = h.strip().lower()
            if any(k in hl for k in ["amount", "tiền", "tien", "chi phi", "chi phí", "giá", "sotien"]):
                amount_col_idx = idx + 1
                break

        unprocessed_records: List[Dict[str, Any]] = []
        already_done_count = 0
        blank_rows_count = 0

        # Duyệt từ dòng 2 (bỏ qua dòng tiêu đề)
        for row_num, row in enumerate(all_values[1:], start=2):
            # Kiểm tra dòng hoàn toàn rỗng
            if not any(cell.strip() for cell in row):
                blank_rows_count += 1
                continue

            # Lấy giá trị trạng thái đồng bộ hiện tại
            status_val = ""
            if len(row) >= sync_col_idx:
                status_val = row[sync_col_idx - 1].strip()

            # Kiểm tra chống trùng lặp: Nếu đã là "Done", bỏ qua
            if status_val.lower() == SYNC_DONE_VALUE.lower():
                already_done_count += 1
                continue

            # Dòng mới chưa xử lý: Thu thập dữ liệu
            # Cắt bỏ cột SyncStatus để lấy đúng dữ liệu nghiệp vụ
            data_cells = []
            for col_i in range(len(headers)):
                if (col_i + 1) == sync_col_idx:
                    continue  # Bỏ qua cột SyncStatus
                cell_val = row[col_i] if col_i < len(row) else ""
                data_cells.append(cell_val)

            # Phân tích số tiền nếu có
            parsed_amount = 0
            if amount_col_idx and amount_col_idx <= len(row):
                raw_amt = str(row[amount_col_idx - 1])
                for char in [",", ".", "đ", "Đ", "VND", "vnd", "VNĐ", " "]:
                    raw_amt = raw_amt.replace(char, "")
                try:
                    parsed_amount = float(raw_amt)
                except ValueError:
                    parsed_amount = 0

            unprocessed_records.append({
                "row_number": row_num,
                "raw_row": row,
                "data_cells": data_cells,
                "amount": parsed_amount,
                "preview_text": " | ".join(c for c in data_cells[:4] if c)
            })

        logger.info(
            f"Tổng số dòng quét: {len(all_values) - 1} | "
            f"Đã xử lý trước đó ('Done'): {already_done_count} | "
            f"Dòng trống: {blank_rows_count} | "
            f"Dòng mới CẦN ĐỒNG BỘ: {len(unprocessed_records)}"
        )

        return unprocessed_records, headers, sync_col_idx

    def sync_to_admin(
        self,
        records: List[Dict[str, Any]],
        headers: List[str],
        sync_col_idx: int
    ) -> Dict[str, Any]:
        """
        Thực hiện đồng bộ:
        1. Ghi nối tiếp (Append) dữ liệu mới xuống cuối bảng Kế toán (KHÔNG GHI ĐÈ).
        2. Đánh dấu 'Done' vào cột SyncStatus ở bảng Nhân viên.
        """
        if not records:
            logger.info("Không có dữ liệu mới phát sinh. Không cần cập nhật bảng Kế toán.")
            return {"synced_count": 0, "status": "NO_NEW_DATA"}

        # 1. Chuẩn bị danh sách dòng cần append vào bảng Admin
        rows_to_append = [r["data_cells"] for r in records]
        
        # Đếm số dòng hiện tại của Admin trước khi chèn
        admin_existing_values = self.admin_ws.get_all_values()
        admin_row_count_before = len(admin_existing_values)
        logger.info(f"Số dòng hiện tại trong bảng Kế toán: {admin_row_count_before} dòng.")

        # Nếu bảng Kế toán hoàn toàn trống, bổ sung dòng tiêu đề sạch (không gồm SyncStatus)
        if admin_row_count_before == 0 and not self.dry_run:
            clean_headers = [h for i, h in enumerate(headers) if i + 1 != sync_col_idx]
            logger.info(f"Bảng Kế toán chưa có header. Đang khởi tạo dòng tiêu đề: {clean_headers}")
            self.admin_ws.append_rows([clean_headers], value_input_option="USER_ENTERED")
            admin_row_count_before = 1

        if self.dry_run:
            logger.info(f"[DRY-RUN] Sẽ chèn nối tiếp {len(rows_to_append)} dòng mới vào cuối bảng Kế toán.")
            logger.info(f"[DRY-RUN] Sẽ cập nhật 'Done' cho các dòng nhân viên: {[r['row_number'] for r in records]}")
            return {
                "synced_count": len(records),
                "admin_start_row": admin_row_count_before + 1,
                "admin_end_row": admin_row_count_before + len(records),
                "status": "DRY_RUN_SUCCESS"
            }

        # 2. GHI NỐI TIẾP THÔNG MINH (Smart Append)
        # Sử dụng append_rows với value_input_option='USER_ENTERED' để Google Sheet tự nhận dạng số và ngày
        logger.info(f"Đang ghi nối tiếp {len(rows_to_append)} dòng vào cuối bảng Kế toán...")
        append_res = self.admin_ws.append_rows(rows_to_append, value_input_option="USER_ENTERED")
        logger.info(f"-> Ghi nối tiếp vào bảng Kế toán thành công! Dữ liệu cũ được bảo toàn tuyệt đối.")

        # 3. ĐÁNH DẤU 'Done' VÀO CỘT SyncStatus (Anti-duplication)
        # Thực hiện cập nhật hàng loạt (Batch Update) bằng update_cells để tiết kiệm API quota
        import gspread
        logger.info(f"Đang đánh dấu '{SYNC_DONE_VALUE}' vào cột {sync_col_idx} trong bảng Nhân viên...")
        
        cells_to_update = [
            gspread.Cell(row=r["row_number"], col=sync_col_idx, value=SYNC_DONE_VALUE)
            for r in records
        ]
        self.staff_ws.update_cells(cells_to_update, value_input_option="USER_ENTERED")
        logger.info(f"-> Đã đánh dấu '{SYNC_DONE_VALUE}' thành công cho {len(cells_to_update)} dòng trong bảng Nhân viên.")

        return {
            "synced_count": len(records),
            "admin_start_row": admin_row_count_before + 1,
            "admin_end_row": admin_row_count_before + len(records),
            "status": "SUCCESS"
        }

    def print_summary_report(self, records: List[Dict[str, Any]], sync_result: Dict[str, Any]):
        """In báo cáo nghiệm thu trực quan ra màn hình console."""
        print("\n" + "=" * 90)
        print(f"{'BÁO CÁO TỔNG HỢP ĐỒNG BỘ CHI TIÊU — EXPENSE SYNC AGENT':^90}")
        print("=" * 90)
        print(f" Thời gian thực hiện : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f" Bảng Nhân viên (Nguồn): '{self.staff_ws.spreadsheet.title}' (GID: {self.staff_gid})")
        print(f" Bảng Kế toán (Đích)  : '{self.admin_ws.spreadsheet.title}' (GID: {self.admin_gid})")
        print(f" Chế độ vận hành      : {'[THỬ NGHIỆM - DRY-RUN]' if self.dry_run else '[THỰC THI TRỰC TIẾP]'}")
        print(f" Trạng thái kết quả   : {sync_result.get('status')}")
        print("-" * 90)

        if not records:
            print("  >>> Không có khoản chi mới nào cần đồng bộ. Tất cả dữ liệu đã 'Done'.")
        else:
            print(f"{'STT':^5} | {'Dòng Nguồn':^12} | {'Chi tiết khoản chi mới phát sinh':<65}")
            print("-" * 90)
            for i, r in enumerate(records, start=1):
                preview = r["preview_text"][:63]
                row_label = f"Dòng {r['row_number']}"
                print(f"{i:^5} | {row_label:^12} | {preview:<65}")

            total_amount = sum(r.get("amount", 0) for r in records)
            print("-" * 90)
            print(f"  * Tổng số bản ghi mới đồng bộ : {sync_result.get('synced_count', 0)} dòng")
            if total_amount > 0:
                print(f"  * Tổng số tiền đồng bộ        : {total_amount:,.0f} VNĐ")
            if not self.dry_run and sync_result.get('admin_start_row'):
                print(f"  * Vị trí ghi trong file Kế toán: Dòng {sync_result['admin_start_row']} -> Dòng {sync_result['admin_end_row']} (Nối tiếp)")
                print(f"  * Cơ chế chống trùng lặp       : Đã gắn cờ '{SYNC_DONE_VALUE}' vào cột SyncStatus")
        
        print("=" * 90 + "\n")


def parse_arguments():
    """Thiết lập các tham số CLI cho kịch bản tự động hóa."""
    parser = argparse.ArgumentParser(
        description="Enterprise Expense Sync Agent — Tự động đồng bộ chi tiêu giữa Google Sheets"
    )
    parser.add_argument(
        "--credentials",
        default="credential.json",
        help="Đường dẫn đến file OAuth 2.0 Client Secrets JSON (mặc định: credential.json)"
    )
    parser.add_argument(
        "--token",
        default="token.json",
        help="Đường dẫn đến file lưu phiên làm việc OAuth 2.0 (mặc định: token.json)"
    )
    parser.add_argument(
        "--staff-id",
        default=DEFAULT_STAFF_SPREADSHEET_ID,
        help="Google Spreadsheet ID của file Nhân viên"
    )
    parser.add_argument(
        "--staff-gid",
        type=int,
        default=DEFAULT_STAFF_GID,
        help="Sheet GID của file Nhân viên (mặc định: 1177273027)"
    )
    parser.add_argument(
        "--admin-id",
        default=DEFAULT_ADMIN_SPREADSHEET_ID,
        help="Google Spreadsheet ID của file Kế toán"
    )
    parser.add_argument(
        "--admin-gid",
        type=int,
        default=DEFAULT_ADMIN_GID,
        help="Sheet GID của file Kế toán (mặc định: 472636171)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chế độ chạy thử nghiệm: quét và hiển thị dữ liệu mà không ghi vào Google Sheets"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    print("\n" + "#" * 90)
    print(f"{'KHỞI ĐỘNG KỊCH BẢN TỰ ĐỘNG HÓA ĐỒNG BỘ CHI TIÊU GOOGLE SHEETS':^90}")
    print("#" * 90)

    try:
        # Bước 1: Xác thực chuẩn Google Cloud OAuth 2.0
        client = GoogleSheetsAuthManager.authenticate(
            credential_path=args.credentials,
            token_path=args.token
        )

        # Bước 2: Khởi tạo Agent
        agent = ExpenseSyncAgent(
            gspread_client=client,
            staff_sheet_id=args.staff_id,
            staff_gid=args.staff_gid,
            admin_sheet_id=args.admin_id,
            admin_gid=args.admin_gid,
            dry_run=args.dry_run
        )

        # Bước 3: Kết nối và kiểm tra bảng tính
        agent.connect()

        # Bước 4: Quét dữ liệu, kiểm tra cột SyncStatus và lọc các dòng chưa 'Done'
        unprocessed_records, headers, sync_col_idx = agent.scan_expenses()

        # Bước 5: Ghi nối tiếp thông minh vào Admin và đánh dấu 'Done' cho Nhân viên
        sync_result = agent.sync_to_admin(unprocessed_records, headers, sync_col_idx)

        # Bước 6: Xuất bảng tổng hợp trực quan
        agent.print_summary_report(unprocessed_records, sync_result)

    except KeyboardInterrupt:
        logger.warning("\nTiến trình bị hủy bởi người dùng.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"LỖI THỰC THI: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
