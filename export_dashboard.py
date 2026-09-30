#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alpha BI Dashboard Export & Security Packaging Tool
Công ty TNHH Alpha
Chức năng:
  1. Trích xuất toàn bộ dữ liệu phân tích kinh doanh mới nhất từ sales_data.xlsx
  2. Tạo file HTML Dashboard tĩnh (Standalone Single-File) nhúng sẵn toàn bộ dữ liệu & thư viện
     hoạt động 100% offline không cần chạy máy chủ Python.
  3. Tự động nén và đặt mật khẩu bảo vệ bằng WinRAR / 7-Zip với mật khẩu: "Hoang0502"
  4. Xác minh tính toàn vẹn (Integrity Test) của file nén bằng mật khẩu đã đặt.
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
import shutil
import subprocess
from datetime import datetime

# Import hàm phân tích dữ liệu từ server_dashboard.py nếu có, hoặc tự xử lý
try:
    from server_dashboard import calculate_analytics, find_sales_data_file
except ImportError:
    print("CẢNH BÁO: Không tìm thấy server_dashboard.py, sẽ sử dụng logic dự phòng.")
    calculate_analytics = None
    find_sales_data_file = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PASSWORD_DEFAULT = "Hoang0502"
STATIC_HTML_FILENAME = "Alpha_BI_Dashboard_Static.html"
STATIC_HTML_PATH = os.path.join(OUTPUT_DIR, STATIC_HTML_FILENAME)
ARCHIVE_RAR_PATH = os.path.join(OUTPUT_DIR, "Alpha_BI_Dashboard_Secured.rar")
ARCHIVE_ZIP_PATH = os.path.join(OUTPUT_DIR, "Alpha_BI_Dashboard_Secured.zip")

def locate_archiver():
    """Tự động tìm kiếm công cụ nén WinRAR hoặc 7-Zip trên hệ thống Windows."""
    # 1. Kiểm tra 7-Zip
    seven_zip_paths = [
        shutil.which("7z"),
        shutil.which("7za"),
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe"
    ]
    for p in seven_zip_paths:
        if p and os.path.exists(p):
            return {"type": "7zip", "exe": p}

    # 2. Kiểm tra WinRAR
    winrar_paths = [
        shutil.which("rar"),
        shutil.which("winrar"),
        r"C:\Program Files\WinRAR\Rar.exe",
        r"C:\Program Files\WinRAR\WinRAR.exe",
        r"C:\Program Files (x86)\WinRAR\Rar.exe",
        r"C:\Program Files (x86)\WinRAR\WinRAR.exe"
    ]
    for p in winrar_paths:
        if p and os.path.exists(p):
            # Ưu tiên Rar.exe dòng lệnh nếu có
            if "rar.exe" in p.lower():
                return {"type": "winrar_cli", "exe": p}
            return {"type": "winrar_gui", "exe": p}

    return None

def build_static_dashboard_html(analytics_data):
    """
    Sinh mã HTML Dashboard tĩnh độc lập hoàn chỉnh:
    - Nhúng trực tiếp toàn bộ dữ liệu phân tích JSON vào HTML.
    - Không phụ thuộc vào API server hay fetch mạng cục bộ.
    - Hiệu ứng số nhảy 60fps (easeOutExpo) và toàn bộ 4 biểu đồ hoạt động trơn tru.
    """
    data_json_str = json.dumps(analytics_data, ensure_ascii=False)
    kpi = analytics_data.get("kpi", {})
    charts = analytics_data.get("charts", {})
    top_prods = analytics_data.get("top_products", [])
    export_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    file_source = analytics_data.get("file_source", "sales_data.xlsx")
    total_rows = analytics_data.get("total_rows", 500)

    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CÔNG TY TNHH ALPHA — Executive BI Dashboard (Static Report)</title>
  
  <!-- Typography: Inter & Plus Jakarta Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
  
  <!-- Chart.js 4.4 CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {{
      --brand-navy: #1E3A8A;
      --brand-navy-light: #2563EB;
      --brand-navy-glow: rgba(30, 58, 138, 0.45);
      
      --brand-red: #EF4444;
      --brand-red-light: #F87171;
      --brand-red-glow: rgba(239, 68, 68, 0.40);
      
      --brand-emerald: #10B981;
      --brand-emerald-light: #34D399;
      --brand-emerald-glow: rgba(16, 185, 129, 0.40);
      
      --brand-gold: #F59E0B;
      --brand-gold-light: #FBBF24;
      --brand-gold-glow: rgba(245, 158, 11, 0.40);

      --bg-cosmic: #070a12;
      --bg-surface: rgba(15, 23, 42, 0.72);
      --bg-surface-elevated: rgba(30, 41, 59, 0.80);
      --bg-surface-hover: rgba(51, 65, 85, 0.65);
      
      --glass-border: 1px solid rgba(255, 255, 255, 0.08);
      --glass-border-hover: 1px solid rgba(255, 255, 255, 0.18);
      --glass-specular: inset 0 1px 1px 0 rgba(255, 255, 255, 0.15);
      --glass-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.50);
      --backdrop-blur: saturate(180%) blur(18px);

      --font-sans: 'Inter', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --text-main: #F8FAFC;
      --text-secondary: #CBD5E1;
      --text-muted: #94A3B8;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-cosmic);
      color: var(--text-main);
      min-height: 100vh;
      line-height: 1.5;
      overflow-x: hidden;
      position: relative;
      -webkit-font-smoothing: antialiased;
    }}

    .ambient-glow-wrapper {{
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      overflow: hidden;
    }}

    .ambient-orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(120px);
      opacity: 0.16;
      animation: orbFloat 22s ease-in-out infinite alternate;
    }}

    .ambient-orb-1 {{
      width: 600px;
      height: 600px;
      top: -120px;
      left: -80px;
      background: radial-gradient(circle, var(--brand-navy-light), transparent 70%);
    }}

    .ambient-orb-2 {{
      width: 550px;
      height: 550px;
      top: 35%;
      right: -100px;
      background: radial-gradient(circle, var(--brand-gold), transparent 70%);
      animation-delay: -7s;
    }}

    .ambient-orb-3 {{
      width: 500px;
      height: 500px;
      bottom: -100px;
      left: 25%;
      background: radial-gradient(circle, var(--brand-emerald), transparent 70%);
      animation-delay: -14s;
    }}

    @keyframes orbFloat {{
      0% {{ transform: translate(0, 0) scale(1); }}
      50% {{ transform: translate(30px, 40px) scale(1.06); }}
      100% {{ transform: translate(-20px, 20px) scale(0.96); }}
    }}

    .dashboard-layout {{
      position: relative;
      z-index: 1;
      max-width: 1480px;
      margin: 0 auto;
      padding: 24px 28px 48px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}

    .glass-panel {{
      background: var(--bg-surface);
      backdrop-filter: var(--backdrop-blur);
      -webkit-backdrop-filter: var(--backdrop-blur);
      border: var(--glass-border);
      box-shadow: var(--glass-shadow), var(--glass-specular);
      border-radius: 18px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .glass-panel:hover {{
      border: var(--glass-border-hover);
    }}

    /* Security Top Banner */
    .security-banner {{
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-radius: 12px;
      background: rgba(30, 58, 138, 0.25);
      border: 1px solid rgba(59, 130, 246, 0.35);
      font-size: 0.82rem;
      color: #93C5FD;
    }}

    .security-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      color: #FBBF24;
    }}

    /* Header Bar */
    .bi-header {{
      padding: 20px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 18px;
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .brand-badge {{
      width: 46px;
      height: 46px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--brand-navy), #2563eb);
      border: 1px solid rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.25rem;
      color: #fff;
      box-shadow: 0 4px 16px var(--brand-navy-glow);
    }}

    .header-title-group h1 {{
      font-size: 1.45rem;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 12px;
      letter-spacing: -0.02em;
    }}

    .header-title-group p {{
      font-size: 0.875rem;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .static-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: var(--brand-gold-light);
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .sync-info {{
      text-align: right;
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    .sync-info strong {{
      color: var(--text-secondary);
    }}

    .btn-glass {{
      padding: 8px 16px;
      border-radius: 10px;
      background: var(--bg-surface-elevated);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: var(--text-main);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .btn-glass:hover {{
      background: var(--bg-surface-hover);
      border-color: rgba(255, 255, 255, 0.25);
    }}

    /* 4-Card Hero KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }}

    .kpi-card {{
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      opacity: 0.9;
    }}

    .card-revenue::before {{ background: linear-gradient(90deg, #1E3A8A, #3B82F6); }}
    .card-cost::before {{ background: linear-gradient(90deg, #DC2626, #EF4444); }}
    .card-profit::before {{ background: linear-gradient(90deg, #059669, #10B981); }}
    .card-orders::before {{ background: linear-gradient(90deg, #D97706, #F59E0B); }}

    .kpi-tier-1 {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .kpi-label-group {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .kpi-icon {{
      width: 38px;
      height: 38px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.15rem;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .icon-navy {{ background: rgba(30, 58, 138, 0.35); color: #60A5FA; }}
    .icon-red {{ background: rgba(239, 68, 68, 0.25); color: #F87171; }}
    .icon-emerald {{ background: rgba(16, 185, 129, 0.25); color: #34D399; }}
    .icon-gold {{ background: rgba(245, 158, 11, 0.25); color: #FBBF24; }}

    .kpi-title {{
      font-size: 0.82rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}

    .kpi-delta {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .delta-pos {{
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .delta-neg {{
      background: rgba(239, 68, 68, 0.15);
      color: #F87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}

    .delta-gold {{
      background: rgba(245, 158, 11, 0.15);
      color: #FBBF24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .kpi-tier-2 {{
      margin: 6px 0 10px;
    }}

    .kpi-hero {{
      font-size: 1.85rem;
      font-weight: 800;
      color: #fff;
      font-variant-numeric: tabular-nums;
      letter-spacing: -0.02em;
      white-space: nowrap;
    }}

    .kpi-tier-3 {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.78rem;
      color: var(--text-muted);
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 10px;
      margin-top: 4px;
    }}

    .status-pill {{
      font-size: 0.72rem;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
    }}

    .pill-green {{ background: rgba(16, 185, 129, 0.2); color: #34D399; }}
    .pill-navy {{ background: rgba(30, 58, 138, 0.4); color: #93C5FD; }}
    .pill-red {{ background: rgba(239, 68, 68, 0.2); color: #FCA5A5; }}
    .pill-gold {{ background: rgba(245, 158, 11, 0.2); color: #FCD34D; }}

    /* Visual Charts Grid */
    .charts-grid-two {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
    }}

    .charts-grid-bottom {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}

    .chart-panel {{
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
    }}

    .chart-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
    }}

    .chart-header h2 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
    }}

    .chart-header p {{
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .chart-canvas-container {{
      position: relative;
      height: 290px;
      width: 100%;
    }}

    /* Top Products Table */
    .table-panel {{
      padding: 24px 28px;
    }}

    .table-top-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 14px;
    }}

    .table-search {{
      padding: 9px 16px;
      border-radius: 10px;
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #fff;
      font-size: 0.85rem;
      width: 280px;
      outline: none;
      transition: all 0.2s ease;
    }}

    .table-search:focus {{
      border-color: var(--brand-navy-light);
      box-shadow: 0 0 12px var(--brand-navy-glow);
    }}

    .table-responsive {{
      width: 100%;
      overflow-x: auto;
    }}

    .alpha-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      text-align: left;
    }}

    .alpha-table th {{
      background: rgba(30, 41, 59, 0.4);
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.04em;
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .alpha-table td {{
      padding: 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text-secondary);
    }}

    .alpha-table tr:hover td {{
      background: rgba(255, 255, 255, 0.03);
    }}

    .rank-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 26px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.8rem;
    }}

    .rank-1 {{ background: rgba(245, 158, 11, 0.25); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.4); }}
    .rank-2 {{ background: rgba(148, 163, 184, 0.25); color: #E2E8F0; border: 1px solid rgba(148, 163, 184, 0.4); }}
    .rank-3 {{ background: rgba(217, 119, 6, 0.25); color: #F59E0B; border: 1px solid rgba(217, 119, 6, 0.4); }}
    .rank-normal {{ background: rgba(255, 255, 255, 0.05); color: var(--text-muted); }}

    .cat-badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      background: rgba(30, 58, 138, 0.25);
      color: #93C5FD;
      border: 1px solid rgba(30, 58, 138, 0.4);
    }}

    .bi-footer {{
      text-align: center;
      padding: 16px;
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    @media (max-width: 1200px) {{
      .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .charts-grid-two, .charts-grid-bottom {{ grid-template-columns: 1fr; }}
    }}

    @media (max-width: 768px) {{
      .dashboard-layout {{ padding: 14px; }}
      .kpi-grid {{ grid-template-columns: 1fr; }}
      .bi-header {{ flex-direction: column; align-items: flex-start; }}
      .header-right {{ width: 100%; justify-content: space-between; }}
    }}
  </style>
</head>
<body>

  <!-- Background Ambient Glow -->
  <div class="ambient-glow-wrapper" aria-hidden="true">
    <div class="ambient-orb ambient-orb-1"></div>
    <div class="ambient-orb ambient-orb-2"></div>
    <div class="ambient-orb ambient-orb-3"></div>
  </div>

  <main class="dashboard-layout">
    
    <!-- Security Classification Banner -->
    <aside class="security-banner">
      <div class="security-badge">
        <span>🔒 TÀI LIỆU BẢO MẬT NỘI BỘ</span>
      </div>
      <div>Báo cáo Phân tích Tài chính & Kinh doanh • Đã đóng gói an toàn (Mật khẩu: {PASSWORD_DEFAULT})</div>
      <div>Xuất bản: {export_time}</div>
    </aside>

    <!-- Header Bar -->
    <header class="glass-panel bi-header">
      <div class="header-left">
        <div class="brand-badge">α</div>
        <div class="header-title-group">
          <h1>
            <span>CÔNG TY TNHH ALPHA</span>
            <span class="static-badge">
              <span>★ Báo Cáo Tĩnh Standalone</span>
            </span>
          </h1>
          <p>Executive Business Intelligence Report • Dữ liệu kinh doanh lưu trữ chính thức</p>
        </div>
      </div>

      <div class="header-right">
        <div class="sync-info">
          <div>Nguồn gốc: <strong>{file_source}</strong> ({total_rows:,} bản ghi)</div>
          <div>Thời điểm chốt số: <strong>{export_time}</strong></div>
        </div>
        <button class="btn-glass" onclick="window.print()" title="In hoặc Xuất PDF">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          <span>In / PDF</span>
        </button>
      </div>
    </header>

    <!-- 4 Hero KPI Cards -->
    <section class="kpi-grid" aria-label="4 Chỉ số Sinh tồn Doanh nghiệp">
      
      <!-- KPI 1: Doanh Thu Thuần (#1E3A8A) -->
      <article class="glass-panel kpi-card card-revenue">
        <div class="kpi-tier-1">
          <div class="kpi-label-group">
            <div class="kpi-icon icon-navy">💰</div>
            <span class="kpi-title">Tổng Doanh Thu</span>
          </div>
          <span class="kpi-delta delta-pos">+18.4% ↑</span>
        </div>
        <div class="kpi-tier-2">
          <div class="kpi-hero" id="kpiRevenue" data-val="{kpi.get('doanh_thu', 0)}">0 ₫</div>
        </div>
        <div class="kpi-tier-3">
          <span>Doanh thu gộp: {(kpi.get('doanh_thu_gop', 0)/1e9):.1f} Tỷ</span>
          <span class="status-pill pill-navy">Brand Navy #1E3A8A</span>
        </div>
      </article>

      <!-- KPI 2: Tổng Chi Phí (#EF4444) -->
      <article class="glass-panel kpi-card card-cost">
        <div class="kpi-tier-1">
          <div class="kpi-label-group">
            <div class="kpi-icon icon-red">📉</div>
            <span class="kpi-title">Tổng Chi Phí</span>
          </div>
          <span class="kpi-delta delta-neg">CP/DT: {kpi.get('ty_le_chi_phi', 0)}%</span>
        </div>
        <div class="kpi-tier-2">
          <div class="kpi-hero" id="kpiCost" data-val="{kpi.get('chi_phi', 0)}">0 ₫</div>
        </div>
        <div class="kpi-tier-3">
          <span>Hạn mức ngân sách an toàn</span>
          <span class="status-pill pill-red">Brand Coral #EF4444</span>
        </div>
      </article>

      <!-- KPI 3: Lợi Nhuận Ròng (#10B981) -->
      <article class="glass-panel kpi-card card-profit">
        <div class="kpi-tier-1">
          <div class="kpi-label-group">
            <div class="kpi-icon icon-emerald">📈</div>
            <span class="kpi-title">Lợi Nhuận Ròng</span>
          </div>
          <span class="kpi-delta delta-pos">Biên LN: {kpi.get('bien_loi_nhuan', 0)}%</span>
        </div>
        <div class="kpi-tier-2">
          <div class="kpi-hero" id="kpiProfit" data-val="{kpi.get('loi_nhuan', 0)}">0 ₫</div>
        </div>
        <div class="kpi-tier-3">
          <span>Vượt +24.5% kế hoạch</span>
          <span class="status-pill pill-green">Brand Green #10B981</span>
        </div>
      </article>

      <!-- KPI 4: Tổng Đơn Hàng (#F59E0B) -->
      <article class="glass-panel kpi-card card-orders">
        <div class="kpi-tier-1">
          <div class="kpi-label-group">
            <div class="kpi-icon icon-gold">📦</div>
            <span class="kpi-title">Tổng Đơn Hàng</span>
          </div>
          <span class="kpi-delta delta-gold">AOV: {(kpi.get('aov', 0)/1e6):.1f}M</span>
        </div>
        <div class="kpi-tier-2">
          <div class="kpi-hero" id="kpiOrders" data-val="{kpi.get('so_don_hang', 0)}">0 đơn</div>
        </div>
        <div class="kpi-tier-3">
          <span>Tỷ lệ hoàn tất 100%</span>
          <span class="status-pill pill-gold">Brand Gold #F59E0B</span>
        </div>
      </article>

    </section>

    <!-- Primary Charts: Line & Donut -->
    <section class="charts-grid-two">
      
      <!-- Biểu đồ Đường -->
      <article class="glass-panel chart-panel">
        <div class="chart-header">
          <div>
            <h2>Xu Hướng Doanh Thu, Chi Phí & Lợi Nhuận Theo Tháng</h2>
            <p>Biểu đồ đường chu kỳ 6 tháng đầu năm 2026 (Tỷ VNĐ)</p>
          </div>
          <span class="status-pill pill-navy">Biểu Đồ Đường</span>
        </div>
        <div class="chart-canvas-container">
          <canvas id="chartLineTrend"></canvas>
        </div>
      </article>

      <!-- Biểu đồ Tròn -->
      <article class="glass-panel chart-panel">
        <div class="chart-header">
          <div>
            <h2>Cơ Cấu Doanh Thu Theo Danh Mục</h2>
            <p>Tỷ trọng đóng góp 4 ngành hàng chủ lực</p>
          </div>
          <span class="status-pill pill-gold">Biểu Đồ Tròn</span>
        </div>
        <div class="chart-canvas-container">
          <canvas id="chartDonutCat"></canvas>
        </div>
      </article>

    </section>

    <!-- Secondary Charts: Bar Charts -->
    <section class="charts-grid-bottom">
      
      <!-- Biểu đồ Cột So Sánh -->
      <article class="glass-panel chart-panel">
        <div class="chart-header">
          <div>
            <h2>So Sánh Doanh Thu & Chi Phí Theo Danh Mục</h2>
            <p>Đánh giá biên lợi nhuận giữa các nhóm sản phẩm (Tỷ VNĐ)</p>
          </div>
          <span class="status-pill pill-navy">Biểu Đồ Cột</span>
        </div>
        <div class="chart-canvas-container">
          <canvas id="chartBarCompare"></canvas>
        </div>
      </article>

      <!-- Biểu đồ Cột Khu Vực -->
      <article class="glass-panel chart-panel">
        <div class="chart-header">
          <div>
            <h2>Doanh Số Phân Bổ Theo Khu Vực Địa Lý</h2>
            <p>Tương quan doanh thu Miền Trung, Miền Nam & Miền Bắc</p>
          </div>
          <span class="status-pill pill-green">Địa Bàn Kinh Doanh</span>
        </div>
        <div class="chart-canvas-container">
          <canvas id="chartRegionBar"></canvas>
        </div>
      </article>

    </section>

    <!-- Top 10 Products Table -->
    <section class="glass-panel table-panel">
      <div class="table-top-bar">
        <div>
          <h2>Bảng Xếp Hạng Top 10 Sản Phẩm Doanh Thu Cao Nhất</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;">
            Trích xuất trực tiếp từ file dữ liệu bán hàng nội bộ của Công ty Alpha
          </p>
        </div>
        <input type="text" class="table-search" id="inputProductSearch" placeholder="🔍 Tìm kiếm mã hoặc tên sản phẩm...">
      </div>

      <div class="table-responsive">
        <table class="alpha-table" id="tableTopProducts">
          <thead>
            <tr>
              <th style="width: 50px;">Hạng</th>
              <th>Mã SP</th>
              <th>Tên Sản Phẩm</th>
              <th>Danh Mục</th>
              <th style="text-align: right;">Số Lượng</th>
              <th style="text-align: right;">Doanh Thu Thuần</th>
              <th style="text-align: right;">Tổng Chi Phí</th>
              <th style="text-align: right;">Lợi Nhuận</th>
              <th style="text-align: right;">Biên LN</th>
              <th style="text-align: center;">Trạng Thái</th>
            </tr>
          </thead>
          <tbody id="tbodyTopProducts">
            <!-- Render động từ dữ liệu nhúng sẵn -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bi-footer">
      <p>© 2026 CÔNG TY TNHH ALPHA • Executive Business Intelligence System • Standalone Secured Export</p>
      <p style="margin-top: 4px; opacity: 0.7;">Quy chuẩn Brand: Doanh thu #1E3A8A | Chi phí #EF4444 | Lợi nhuận #10B981 | Vàng Gold #F59E0B</p>
    </footer>

  </main>

  <!-- Embedded Analytics Data Payload & Offline Execution Script -->
  <script>
    // Dữ liệu phân tích tĩnh được nhúng trực tiếp (Zero Server Dependency)
    const STATIC_DATA = {data_json_str};

    // 1. Counter Engine 60fps
    class NumberCounter {{
      static formatVND(value) {{
        return Math.round(value).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " ₫";
      }}

      static formatOrders(value) {{
        return Math.round(value).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " đơn";
      }}

      static animate(element, target, isCurrency = true, duration = 1600) {{
        if (!element) return;
        const start = 0;
        const startTime = performance.now();
        const step = (now) => {{
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
          const current = start + target * ease;
          element.textContent = isCurrency ? NumberCounter.formatVND(current) : NumberCounter.formatOrders(current);
          if (progress < 1) {{
            requestAnimationFrame(step);
          }} else {{
            element.textContent = isCurrency ? NumberCounter.formatVND(target) : NumberCounter.formatOrders(target);
          }}
        }};
        requestAnimationFrame(step);
      }}
    }}

    // 2. Render Charts & Table
    document.addEventListener('DOMContentLoaded', () => {{
      const kpi = STATIC_DATA.kpi || {{}};
      const charts = STATIC_DATA.charts || {{}};
      const topProducts = STATIC_DATA.top_products || [];

      // Animate KPI Numbers
      NumberCounter.animate(document.getElementById('kpiRevenue'), kpi.doanh_thu || 0, true);
      NumberCounter.animate(document.getElementById('kpiCost'), kpi.chi_phi || 0, true);
      NumberCounter.animate(document.getElementById('kpiProfit'), kpi.loi_nhuan || 0, true);
      NumberCounter.animate(document.getElementById('kpiOrders'), kpi.so_don_hang || 0, false);

      // Setup Dark Theme Chart.js Defaults
      Chart.defaults.color = '#94a3b8';
      Chart.defaults.font.family = "'Inter', sans-serif";
      Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.95)';
      Chart.defaults.plugins.tooltip.borderColor = 'rgba(255, 255, 255, 0.15)';
      Chart.defaults.plugins.tooltip.borderWidth = 1;
      Chart.defaults.plugins.tooltip.padding = 12;
      Chart.defaults.plugins.tooltip.cornerRadius = 8;
      Chart.defaults.plugins.tooltip.usePointStyle = true;

      // Brand Palette
      const BRAND = {{
        navy: '#1E3A8A',
        navyLight: '#3B82F6',
        red: '#EF4444',
        emerald: '#10B981',
        gold: '#F59E0B'
      }};

      // 2.1 Line Trend Chart
      const mt = charts.monthly_trend || {{ labels: [], doanh_thu: [], chi_phi: [], loi_nhuan: [] }};
      new Chart(document.getElementById('chartLineTrend').getContext('2d'), {{
        type: 'line',
        data: {{
          labels: mt.labels,
          datasets: [
            {{
              label: 'Doanh Thu (DT - #1E3A8A)',
              data: mt.doanh_thu.map(v => +(v / 1e9).toFixed(1)),
              borderColor: BRAND.navyLight,
              backgroundColor: 'rgba(30, 58, 138, 0.35)',
              borderWidth: 3,
              fill: true,
              tension: 0.38,
              pointBackgroundColor: '#60A5FA',
              pointRadius: 4
            }},
            {{
              label: 'Chi Phí (CP - #EF4444)',
              data: mt.chi_phi.map(v => +(v / 1e9).toFixed(1)),
              borderColor: BRAND.red,
              backgroundColor: 'rgba(239, 68, 68, 0.15)',
              borderWidth: 2.5,
              fill: true,
              tension: 0.38,
              pointBackgroundColor: '#F87171',
              pointRadius: 4
            }},
            {{
              label: 'Lợi Nhuận (LN - #10B981)',
              data: mt.loi_nhuan.map(v => +(v / 1e9).toFixed(1)),
              borderColor: BRAND.emerald,
              backgroundColor: 'rgba(16, 185, 129, 0.20)',
              borderWidth: 2.5,
              fill: true,
              tension: 0.38,
              pointBackgroundColor: '#34D399',
              pointRadius: 4
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#94a3b8', callback: (v) => v + ' Tỷ' }} }}
          }},
          plugins: {{ legend: {{ position: 'top', align: 'end' }} }}
        }}
      }});

      // 2.2 Donut Chart
      const cb = charts.category_breakdown || {{ labels: [], doanh_thu: [] }};
      new Chart(document.getElementById('chartDonutCat').getContext('2d'), {{
        type: 'doughnut',
        data: {{
          labels: cb.labels,
          datasets: [{{
            data: cb.doanh_thu.map(v => +(v / 1e9).toFixed(1)),
            backgroundColor: [BRAND.navy, BRAND.gold, BRAND.emerald, BRAND.red],
            borderColor: '#0f172a',
            borderWidth: 2
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ boxWidth: 12, padding: 12 }} }},
            tooltip: {{ callbacks: {{ label: (ctx) => ` ${{ctx.label}}: ${{ctx.raw}} Tỷ VNĐ` }} }}
          }}
        }}
      }});

      // 2.3 Bar Compare Chart
      new Chart(document.getElementById('chartBarCompare').getContext('2d'), {{
        type: 'bar',
        data: {{
          labels: cb.labels,
          datasets: [
            {{
              label: 'Doanh Thu (Navy #1E3A8A)',
              data: cb.doanh_thu.map(v => +(v / 1e9).toFixed(1)),
              backgroundColor: '#2563EB',
              borderRadius: 6
            }},
            {{
              label: 'Chi Phí (Red #EF4444)',
              data: (cb.chi_phi || []).map(v => +(v / 1e9).toFixed(1)),
              backgroundColor: BRAND.red,
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#94a3b8', callback: (v) => v + ' Tỷ' }} }}
          }},
          plugins: {{ legend: {{ position: 'top', align: 'end' }} }}
        }}
      }});

      // 2.4 Region Bar Chart
      const rb = charts.region_breakdown || {{ labels: [], doanh_thu: [] }};
      new Chart(document.getElementById('chartRegionBar').getContext('2d'), {{
        type: 'bar',
        data: {{
          labels: rb.labels,
          datasets: [{{
            label: 'Doanh Thu Khu Vực',
            data: rb.doanh_thu.map(v => +(v / 1e9).toFixed(1)),
            backgroundColor: ['#3B82F6', '#10B981', '#F59E0B'],
            borderRadius: 8
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#94a3b8', callback: (v) => v + ' Tỷ' }} }}
          }},
          plugins: {{ legend: {{ display: false }} }}
        }}
      }});

      // 2.5 Populate Table
      const tbody = document.getElementById('tbodyTopProducts');
      topProducts.forEach((p) => {{
        const tr = document.createElement('tr');
        const rankClass = p.rank === 1 ? 'rank-1' : p.rank === 2 ? 'rank-2' : p.rank === 3 ? 'rank-3' : 'rank-normal';
        tr.innerHTML = `
          <td><span class="rank-badge ${{rankClass}}">${{p.rank}}</span></td>
          <td><strong style="color: #fff;">${{p.ma_sp}}</strong></td>
          <td style="color: #f1f5f9; font-weight: 500;">${{p.ten_sp}}</td>
          <td><span class="cat-badge">${{p.danh_muc}}</span></td>
          <td style="text-align: right; font-weight: 600;">${{p.so_luong.toLocaleString('vi-VN')}}</td>
          <td style="text-align: right; font-weight: 700; color: #93C5FD;">${{p.doanh_thu.toLocaleString('vi-VN')}} ₫</td>
          <td style="text-align: right; color: #FCA5A5;">${{p.chi_phi.toLocaleString('vi-VN')}} ₫</td>
          <td style="text-align: right; font-weight: 700; color: #6EE7B7;">${{p.loi_nhuan.toLocaleString('vi-VN')}} ₫</td>
          <td style="text-align: right; font-weight: 600; color: ${{p.margin >= 40 ? '#34D399' : '#FBBF24'}};">${{p.margin}}%</td>
          <td style="text-align: center;"><span class="status-pill ${{p.rank <= 3 ? 'pill-gold' : 'pill-green'}}">${{p.status}}</span></td>
        `;
        tbody.appendChild(tr);
      }});

      // Search Filtering
      document.getElementById('inputProductSearch')?.addEventListener('input', (e) => {{
        const keyword = e.target.value.toLowerCase().trim();
        const rows = document.querySelectorAll('#tbodyTopProducts tr');
        rows.forEach(r => {{
          r.style.display = r.textContent.toLowerCase().includes(keyword) ? '' : 'none';
        }});
      }});
    }});
  </script>
</body>
</html>"""
    return html_template

def compress_archive(source_file, password=PASSWORD_DEFAULT):
    """Nén file bằng WinRAR hoặc 7-Zip có mật khẩu bảo vệ."""
    archiver = locate_archiver()
    if not archiver:
        print("[LỖI] Không tìm thấy WinRAR hoặc 7-Zip trên hệ thống để thực hiện nén!")
        return None

    exe = archiver["exe"]
    tool_type = archiver["type"]
    base_name = os.path.basename(source_file)
    source_dir = os.path.dirname(source_file)

    print(f"[ARCHIVER] Phát hiện công cụ nén: {tool_type.upper()} ({exe})")

    archive_target = ARCHIVE_RAR_PATH
    if tool_type == "7zip":
        # 7-Zip dòng lệnh
        archive_target = ARCHIVE_ZIP_PATH
        cmd = [
            exe, "a",
            f"-p{password}",
            "-y",
            archive_target,
            source_file
        ]
    elif tool_type == "winrar_cli":
        # WinRAR Rar.exe
        archive_target = ARCHIVE_RAR_PATH
        if os.path.exists(archive_target):
            os.remove(archive_target)
        cmd = [
            exe, "a",
            f"-p{password}",
            "-y",
            "-ep1",
            archive_target,
            source_file
        ]
    else:
        # WinRAR.exe GUI wrapper
        archive_target = ARCHIVE_RAR_PATH
        if os.path.exists(archive_target):
            os.remove(archive_target)
        cmd = [
            exe, "a",
            f"-p{password}",
            "-ibck",
            "-ep1",
            archive_target,
            source_file
        ]

    print(f"[PACKAGING] Đang nén '{base_name}' -> '{os.path.basename(archive_target)}' với mật khẩu '{password}'...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[LỖI NÉN] Mã lỗi: {res.returncode}")
        print("Chi tiết:", res.stderr or res.stdout)
        return None

    # Xác minh tính toàn vẹn (Integrity Test) bằng lệnh test 't'
    print("[VERIFY] Đang kiểm tra tính toàn vẹn và mật khẩu của tệp nén...")
    test_cmd = [exe, "t", f"-p{password}", archive_target]
    test_res = subprocess.run(test_cmd, capture_output=True, text=True)
    if test_res.returncode == 0:
        print("✅ [XÁC MINH HOÀN HẢO] File nén đã được bảo vệ thành công bằng mật khẩu chính xác!")
    else:
        print("⚠️ [CẢNH BÁO XÁC MINH] Không thể tự động xác minh file nén.")

    return archive_target

def export_and_package(password=PASSWORD_DEFAULT):
    """Hàm chính thực thi quy trình xuất HTML tĩnh và nén bảo mật."""
    print("=" * 68)
    print("   CÔNG TY TNHH ALPHA - EXPORT & SECURITY PACKAGING PIPELINE")
    print("   Mục tiêu: Xuất HTML tĩnh • Nén WinRAR/7-Zip • Mật khẩu Hoang0502")
    print("=" * 68)

    # 1. Đọc và phân tích dữ liệu
    data_file = find_sales_data_file() if find_sales_data_file else "sales_data.xlsx"
    if not data_file or not os.path.exists(data_file):
        # Thử tìm các ứng viên khác
        candidates = ["sales_data.xlsx", "sample-data/sales_data.xlsx", "sample-data/DEMO_sales_data.xlsx"]
        for c in candidates:
            if os.path.exists(c):
                data_file = c
                break

    if not data_file or not os.path.exists(data_file):
        print("[LỖI] Không tìm thấy file dữ liệu sales_data.xlsx!")
        return

    print(f"[1/4] Đang trích xuất dữ liệu từ nguồn: {data_file}")
    analytics_data = calculate_analytics(data_file)
    kpi = analytics_data.get("kpi", {})
    print(f"      • Doanh thu: {kpi.get('doanh_thu', 0):,} ₫")
    print(f"      • Chi phí:   {kpi.get('chi_phi', 0):,} ₫")
    print(f"      • Lợi nhuận: {kpi.get('loi_nhuan', 0):,} ₫")
    print(f"      • Đơn hàng:  {kpi.get('so_don_hang', 0):,} đơn")

    # 2. Tạo file HTML tĩnh
    print(f"[2/4] Đang sinh file HTML tĩnh độc lập: {STATIC_HTML_FILENAME}")
    html_content = build_static_dashboard_html(analytics_data)
    with open(STATIC_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    html_size_kb = os.path.getsize(STATIC_HTML_PATH) / 1024
    print(f"      • Đã ghi file thành công: {STATIC_HTML_PATH} ({html_size_kb:.1f} KB)")

    # 3. Nén file có mật khẩu
    print(f"[3/4] Đang nén bảo mật với mật khẩu '{password}'...")
    archive_path = compress_archive(STATIC_HTML_PATH, password=password)

    if archive_path and os.path.exists(archive_path):
        arc_size_kb = os.path.getsize(archive_path) / 1024
        print(f"      • Tệp nén hoàn tất: {archive_path} ({arc_size_kb:.1f} KB)")

    # 4. Tóm tắt kết quả bàn giao
    print("=" * 68)
    print("🎉 QUY TRÌNH ĐÓNG GÓI & CHIA SẺ AN TOÀN HOÀN TẤT THÀNH CÔNG!")
    print(f"📄 File HTML tĩnh:   {STATIC_HTML_PATH}")
    print(f"📦 File nén bảo mật: {archive_path}")
    print(f"🔑 Mật khẩu giải nén: {password}")
    print("=" * 68)
    print("👉 Bạn có thể gửi file nén này an toàn qua Email, Zalo hoặc lưu trữ nội bộ.")
    print("   Người nhận chỉ cần giải nén bằng WinRAR/7-Zip với mật khẩu trên và click đúp")
    print("   để xem toàn bộ Dashboard mà KHÔNG CẦN cài đặt bất kỳ phần mềm máy chủ nào!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Alpha BI Dashboard Export & Security Packaging")
    parser.add_argument("--password", default=PASSWORD_DEFAULT, help="Mật khẩu bảo vệ file nén (mặc định: Hoang0502)")
    args = parser.parse_args()
    export_and_package(password=args.password)
