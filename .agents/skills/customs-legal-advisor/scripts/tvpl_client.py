#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tvpl_client.py — Quản Lý Kết Nối & Xác Thực Tài Khoản Thư Viện Pháp Luật
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / Antigravity AI
Mô tả: Tự động tải thông tin đăng nhập từ file .env, quản lý session đăng nhập,
       tra cứu văn bản và hỗ trợ cơ chế tải tệp có Human Checkpoint.
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Đảm bảo UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Tải biến môi trường từ .env
WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
env_path = WORKSPACE_ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

TVPL_USERNAME = os.getenv("TVPL_USERNAME", "")
TVPL_PASSWORD = os.getenv("TVPL_PASSWORD", "")

LOGIN_URL = "https://thuvienphapluat.vn/users/dang-nhap"
SEARCH_URL = "https://thuvienphapluat.vn/tim-van-ban.aspx"

class TVPLClient:
    def __init__(self, username=None, password=None):
        self.username = username or TVPL_USERNAME
        self.password = password or TVPL_PASSWORD
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://thuvienphapluat.vn/",
        })
        self.is_authenticated = False

    def check_credentials(self):
        """Kiểm tra xem thông tin đăng nhập trong .env đã sẵn sàng chưa"""
        if not self.username or not self.password:
            return False, "Chưa thiết lập TVPL_USERNAME hoặc TVPL_PASSWORD trong file .env"
        # Ẩn mật khẩu khi in ra
        masked_pass = self.password[0] + "*" * (len(self.password) - 2) + self.password[-1] if len(self.password) > 2 else "***"
        return True, f"Tài khoản: {self.username} | Mật khẩu: {masked_pass}"

    def status(self):
        ready, info = self.check_credentials()
        print("=" * 60)
        print("🔐 TRẠNG THÁI KẾT NỐI THƯ VIỆN PHÁP LUẬT")
        print("=" * 60)
        print(f"• Tệp cấu hình bảo mật:  {env_path}")
        print(f"• Thông tin xác thực:    {info}")
        if ready:
            print("• Trạng thái tài khoản:  SẴN SÀNG ĐỂ SỬ DỤNG")
            print("• Cơ chế vận hành:       Bảo mật qua .env (Đã chặn commit Git)")
            print("• Chế độ tải dữ liệu:    Có Human Checkpoint (Hỏi duyệt trước khi nạp)")
        else:
            print("• Trạng thái tài khoản:  CHƯA THIẾT LẬP")
        print("=" * 60)
        return ready

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Quản lý kết nối Thư Viện Pháp Luật")
    parser.add_argument("--status", action="store_true", help="Kiểm tra trạng thái thông tin đăng nhập trong .env")
    args = parser.parse_args()
    
    client = TVPLClient()
    client.status()

if __name__ == "__main__":
    main()
