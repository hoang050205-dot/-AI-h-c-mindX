#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alpha BI Dashboard Server - Realtime Executive Analytics
Công ty TNHH Alpha
Chức năng:
  - Phục vụ Web Dashboard Glassmorphism Dark Mode trên cổng 9090
  - Cung cấp API /api/data phản hồi dữ liệu kinh doanh tổng hợp từ sales_data.xlsx
  - Hỗ trợ Polling 2 giây từ client, tự động phát hiện file thay đổi (mtime)
  - Tự động mở trình duyệt Google Chrome khi khởi động
  - Tuân thủ tuyệt đối Brand Guideline Công ty TNHH Alpha
"""

import os
import sys

# Đảm bảo in tiếng Việt trên console Windows không bị UnicodeEncodeError
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import json
import time
import socket
import threading
import webbrowser
import subprocess
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

try:
    import pandas as pd
except ImportError:
    print("LỖI: Chưa cài đặt pandas. Vui lòng cài đặt bằng lệnh: pip install pandas openpyxl")
    sys.exit(1)

# Thiết lập thư mục làm việc cơ sở
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_HTML_PATH = os.path.join(BASE_DIR, "outputs", "reports", "alpha_bi_dashboard.html")

# Danh sách ứng viên file dữ liệu
DATA_FILE_CANDIDATES = [
    os.path.join(BASE_DIR, "sales_data.xlsx"),
    os.path.join(BASE_DIR, "sample-data", "sales_data.xlsx"),
    os.path.join(BASE_DIR, "sample-data", "DEMO_sales_data.xlsx")
]

# Biến lưu trữ Cache dữ liệu trong RAM
DATA_CACHE = {
    "file_path": None,
    "last_mtime": 0,
    "data": None
}

def find_sales_data_file():
    """Tìm file dữ liệu sales_data.xlsx theo độ ưu tiên."""
    for path in DATA_FILE_CANDIDATES:
        if os.path.exists(path):
            return path
    return None

def calculate_analytics(file_path):
    """Đọc dữ liệu Excel và tổng hợp KPI, biểu đồ, bảng Top cho Alpha BI Dashboard."""
    df = pd.read_excel(file_path)

    # 1. Bốn Chỉ Số Hero KPI Sinh Tồn
    # Doanh thu thuần (hoặc Doanh thu gộp)
    dt_thuan = int(df["Doanh_Thu_Thuan"].sum()) if "Doanh_Thu_Thuan" in df.columns else int(df["Doanh_Thu"].sum())
    dt_gop = int(df["Doanh_Thu"].sum()) if "Doanh_Thu" in df.columns else dt_thuan
    cp_tong = int(df["Tong_Chi_Phi"].sum()) if "Tong_Chi_Phi" in df.columns else 0
    loi_nhuan = int(df["Loi_Nhuan"].sum()) if "Loi_Nhuan" in df.columns else (dt_thuan - cp_tong)
    so_don_hang = int(df["Ma_Don_Hang"].nunique()) if "Ma_Don_Hang" in df.columns else len(df)
    
    aov = int(dt_thuan / so_don_hang) if so_don_hang > 0 else 0
    bien_loi_nhuan = round((loi_nhuan / dt_thuan * 100), 1) if dt_thuan > 0 else 0.0
    ty_le_chi_phi = round((cp_tong / dt_thuan * 100), 1) if dt_thuan > 0 else 0.0

    # 2. Biểu đồ Đường: Xu hướng biến động theo Tháng (Monthly Trend)
    monthly_trend = {
        "labels": [],
        "doanh_thu": [],
        "chi_phi": [],
        "loi_nhuan": []
    }
    if "Thang" in df.columns:
        df_month = df.groupby("Thang").agg({
            "Doanh_Thu_Thuan": "sum",
            "Tong_Chi_Phi": "sum",
            "Loi_Nhuan": "sum"
        }).reset_index().sort_values("Thang")
        
        for _, row in df_month.iterrows():
            month_label = str(row["Thang"])
            if "-" in month_label:
                parts = month_label.split("-")
                month_label = f"Tháng {int(parts[1])}"
            monthly_trend["labels"].append(month_label)
            monthly_trend["doanh_thu"].append(int(row["Doanh_Thu_Thuan"]))
            monthly_trend["chi_phi"].append(int(row["Tong_Chi_Phi"]))
            monthly_trend["loi_nhuan"].append(int(row["Loi_Nhuan"]))

    # 3. Biểu đồ Tròn & Cột: Cơ cấu theo Danh mục sản phẩm (Category Breakdown)
    category_breakdown = {
        "labels": [],
        "doanh_thu": [],
        "chi_phi": [],
        "loi_nhuan": [],
        "so_luong": [],
        "so_don": []
    }
    if "Danh_Muc_San_Pham" in df.columns:
        df_cat = df.groupby("Danh_Muc_San_Pham").agg({
            "Doanh_Thu_Thuan": "sum",
            "Tong_Chi_Phi": "sum",
            "Loi_Nhuan": "sum",
            "So_Luong": "sum",
            "Ma_Don_Hang": "count"
        }).reset_index().sort_values("Doanh_Thu_Thuan", ascending=False)
        
        for _, row in df_cat.iterrows():
            category_breakdown["labels"].append(str(row["Danh_Muc_San_Pham"]))
            category_breakdown["doanh_thu"].append(int(row["Doanh_Thu_Thuan"]))
            category_breakdown["chi_phi"].append(int(row["Tong_Chi_Phi"]))
            category_breakdown["loi_nhuan"].append(int(row["Loi_Nhuan"]))
            category_breakdown["so_luong"].append(int(row["So_Luong"]))
            category_breakdown["so_don"].append(int(row["Ma_Don_Hang"]))

    # 4. Phân bố Khu Vực
    region_breakdown = {
        "labels": [],
        "doanh_thu": [],
        "don_hang": []
    }
    if "Khu_Vuc" in df.columns:
        df_region = df.groupby("Khu_Vuc").agg({
            "Doanh_Thu_Thuan": "sum",
            "Ma_Don_Hang": "count"
        }).reset_index().sort_values("Doanh_Thu_Thuan", ascending=False)
        for _, row in df_region.iterrows():
            region_breakdown["labels"].append(str(row["Khu_Vuc"]))
            region_breakdown["doanh_thu"].append(int(row["Doanh_Thu_Thuan"]))
            region_breakdown["don_hang"].append(int(row["Ma_Don_Hang"]))

    # 5. Bảng Top 10 Sản Phẩm Doanh Thu Cao Nhất
    top_products = []
    if "Ma_San_Pham" in df.columns:
        df_top = df.groupby(["Ma_San_Pham", "Ten_San_Pham", "Danh_Muc_San_Pham"]).agg({
            "So_Luong": "sum",
            "Doanh_Thu_Thuan": "sum",
            "Tong_Chi_Phi": "sum",
            "Loi_Nhuan": "sum"
        }).reset_index().sort_values("Doanh_Thu_Thuan", ascending=False).head(10)

        for rank, (_, row) in enumerate(df_top.iterrows(), 1):
            dt_item = int(row["Doanh_Thu_Thuan"])
            ln_item = int(row["Loi_Nhuan"])
            margin = round((ln_item / dt_item * 100), 1) if dt_item > 0 else 0.0
            top_products.append({
                "rank": rank,
                "ma_sp": str(row["Ma_San_Pham"]),
                "ten_sp": str(row["Ten_San_Pham"]),
                "danh_muc": str(row["Danh_Muc_San_Pham"]),
                "so_luong": int(row["So_Luong"]),
                "doanh_thu": dt_item,
                "chi_phi": int(row["Tong_Chi_Phi"]),
                "loi_nhuan": ln_item,
                "margin": margin,
                "status": "Chủ lực" if rank <= 3 else "Bán chạy"
            })

    # Đóng gói dữ liệu phân tích
    return {
        "status": "success",
        "timestamp": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
        "file_source": os.path.basename(file_path),
        "total_rows": len(df),
        "kpi": {
            "doanh_thu": dt_thuan,
            "doanh_thu_gop": dt_gop,
            "chi_phi": cp_tong,
            "loi_nhuan": loi_nhuan,
            "so_don_hang": so_don_hang,
            "aov": aov,
            "bien_loi_nhuan": bien_loi_nhuan,
            "ty_le_chi_phi": ty_le_chi_phi
        },
        "charts": {
            "monthly_trend": monthly_trend,
            "category_breakdown": category_breakdown,
            "region_breakdown": region_breakdown
        },
        "top_products": top_products,
        "brand": {
            "name": "Công ty TNHH Alpha",
            "color_revenue": "#1E3A8A", # Xanh Navy
            "color_cost": "#EF4444",    # Đỏ san hô
            "color_profit": "#10B981",  # Xanh lá mạ
            "color_gold": "#F59E0B"     # Vàng Gold
        }
    }

def get_latest_analytics_data():
    """Lấy dữ liệu phân tích có cơ chế kiểm tra mtime để cache và re-parse tức thì."""
    file_path = find_sales_data_file()
    if not file_path:
        return {
            "status": "error",
            "message": "Không tìm thấy file sales_data.xlsx trong thư mục dự án.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

    current_mtime = os.path.getmtime(file_path)
    if DATA_CACHE["data"] is None or DATA_CACHE["file_path"] != file_path or DATA_CACHE["last_mtime"] != current_mtime:
        print(f"[CACHE REFRESH] Phát hiện cập nhật dữ liệu: {file_path} (mtime: {current_mtime})")
        parsed = calculate_analytics(file_path)
        DATA_CACHE["file_path"] = file_path
        DATA_CACHE["last_mtime"] = current_mtime
        DATA_CACHE["data"] = parsed

    return DATA_CACHE["data"]

class AlphaDashboardHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler phục vụ Web Dashboard và REST API cho client Polling."""

    def log_message(self, format, *args):
        # Giảm thiểu log in ra terminal khi polling 2 giây
        if "/api/data" in self.path:
            return
        super().log_message(format, *args)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # 1. API Cung Cấp Dữ Liệu Realtime (Polling endpoint)
        if path == "/api/data" or path == "/api/kpi":
            data = get_latest_analytics_data()
            json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Content-Length", str(len(json_bytes)))
            self.end_headers()
            self.wfile.write(json_bytes)
            return

        # 2. Health check
        if path == "/api/health":
            resp = json.dumps({"status": "healthy", "service": "alpha_bi_dashboard"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp)
            return

        # 3. Phục vụ Dashboard Web HTML
        if path == "/" or path == "/index.html" or path == "/dashboard":
            if os.path.exists(REPORT_HTML_PATH):
                with open(REPORT_HTML_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"Chưa tạo file dashboard tại: {REPORT_HTML_PATH}".encode("utf-8"))
                return

        # 4. Phục vụ các tài nguyên tĩnh khác nếu có
        file_target = os.path.join(BASE_DIR, path.lstrip("/"))
        if os.path.exists(file_target) and os.path.isfile(file_target):
            content_type = "text/plain"
            if file_target.endswith(".css"):
                content_type = "text/css"
            elif file_target.endswith(".js"):
                content_type = "application/javascript"
            elif file_target.endswith(".png"):
                content_type = "image/png"
            elif file_target.endswith(".svg"):
                content_type = "image/svg+xml"

            with open(file_target, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        # Mặc định 404
        self.send_response(404)
        self.end_headers()

def auto_open_chrome(url, delay_sec=1.2):
    """Tự động mở Google Chrome hoặc trình duyệt mặc định sau delay_sec giây."""
    def _launcher():
        time.sleep(delay_sec)
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        opened = False
        for cp in chrome_paths:
            if os.path.exists(cp):
                try:
                    subprocess.Popen([cp, url])
                    print(f"[BROWSER] Đã mở Google Chrome tự động tại: {url}")
                    opened = True
                    break
                except Exception as ex:
                    print(f"[BROWSER WARNING] Lỗi mở Chrome trực tiếp: {ex}")
        if not opened:
            webbrowser.open(url)
            print(f"[BROWSER] Đã mở trình duyệt mặc định tại: {url}")

    thread = threading.Thread(target=_launcher, daemon=True)
    thread.start()

def is_port_in_use(port):
    """Kiểm tra xem port đã bị chiếm dụng chưa."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_server(port=9090, auto_open=True):
    """Khởi chạy server HTTP đa luồng tại port chỉ định."""
    print("=" * 65)
    print("   CÔNG TY TNHH ALPHA - REALTIME BI DASHBOARD SERVER")
    print("   Tiêu chuẩn: Glassmorphism • Dark Mode • Polling 2s • 60fps")
    print("=" * 65)

    data_file = find_sales_data_file()
    if data_file:
        print(f"[DATA SOURCE] Đang liên kết nguồn: {data_file}")
        # Test parse ban đầu
        init_data = get_latest_analytics_data()
        kpi = init_data.get("kpi", {})
        print(f"[DATA AUDIT] Tổng đơn: {kpi.get('so_don_hang'):,} | Doanh thu: {kpi.get('doanh_thu'):,} ₫ | Chi phí: {kpi.get('chi_phi'):,} ₫ | Lợi nhuận: {kpi.get('loi_nhuan'):,} ₫")
    else:
        print("[DATA WARNING] Chưa tìm thấy file sales_data.xlsx! Vui lòng đặt file vào thư mục làm việc.")

    server_address = ('0.0.0.0', port)
    try:
        httpd = ThreadingHTTPServer(server_address, AlphaDashboardHandler)
    except OSError as e:
        print(f"[SERVER ERROR] Không thể bind port {port}: {e}")
        return

    dashboard_url = f"http://localhost:{port}"
    print(f"[SERVER ONLINE] Đang chạy tại: {dashboard_url}")
    print(f"[POLLING API]   Endpoint:   {dashboard_url}/api/data")
    print(f"[BRAND COLORS]  Doanh thu (#1E3A8A) • Chi phí (#EF4444) • Lợi nhuận (#10B981) • Vàng (#F59E0B)")
    print("=" * 65)
    print("Nhấn Ctrl+C để dừng server.")

    if auto_open:
        auto_open_chrome(dashboard_url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER SHUTDOWN] Đang dừng server...")
        httpd.server_close()
        print("[SERVER STOPPED] Đã đóng server an toàn.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Alpha Realtime BI Dashboard Server")
    parser.add_argument("--port", type=int, default=9090, help="Port lắng nghe (mặc định 9090)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự động mở trình duyệt")
    parser.add_argument("--test-data", action="store_true", help="Chỉ kiểm tra đọc và phân tích dữ liệu Excel rồi thoát")

    args = parser.parse_args()

    if args.test_data:
        data = get_latest_analytics_data()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        run_server(port=args.port, auto_open=not args.no_browser)
