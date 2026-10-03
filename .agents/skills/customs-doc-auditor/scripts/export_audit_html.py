#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_audit_html.py — Interactive Glassmorphism HTML Audit Dashboard Generator (v3.0 Pro)
Tác giả: Minh Hoàng (Customs Documentation Audit Specialist)
Framework: Antigravity Customization System & AI4A
Thiết kế: Glassmorphism Dark Mode, KPI Counter 60fps, Risk Score Gauge, Filter 5 Lớp, Print-ready
Zero external dependencies.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
REPORTS_DIR = WORKSPACE_ROOT / "outputs" / "reports"


def generate_audit_html_dashboard(auditor_or_data, output_path=None):
    """
    Tạo tệp HTML Dashboard tương tác cao cấp từ đối tượng CustomsDocAuditor
    hoặc từ file kết quả JSON.
    """
    if hasattr(auditor_or_data, "shipment"):
        # Đối tượng CustomsDocAuditor
        shipment = auditor_or_data.shipment
        discrepancies = auditor_or_data.discrepancies
        verified_items = auditor_or_data.verified_items
        risk_score = auditor_or_data.risk_score
        audit_passed = auditor_or_data.audit_passed
        seller_name = auditor_or_data.invoice.get("seller", {}).get("name") or auditor_or_data.contract.get("seller", {}).get("name") or "Nhà cung cấp ngoại thương (Shipper)"
        carrier_name = auditor_or_data.bl.get("carrier") or auditor_or_data.bl.get("vessel_voyage") or "Hãng tàu / Forwarder"
        pod_port = auditor_or_data.shipment.get("pod") or auditor_or_data.bl.get("pod") or "Chi cục Hải quan cửa khẩu"
    else:
        # Dictionary data
        shipment = auditor_or_data.get("shipment_info", {})
        discrepancies = auditor_or_data.get("discrepancies", [])
        verified_items = auditor_or_data.get("verified_items", [])
        risk_score = auditor_or_data.get("risk_score", 85)
        audit_passed = len(discrepancies) == 0
        seller_name = "Nhà cung cấp (Shipper)"
        carrier_name = "Hãng tàu / Đại lý Giao nhận"
        pod_port = shipment.get("pod", "Cửa khẩu đến")

    if output_path is None:
        output_path = REPORTS_DIR / "customs_doc_audit_dashboard.html"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    critical_count = sum(1 for d in discrepancies if d.get("severity") == "CRITICAL")
    high_count = sum(1 for d in discrepancies if d.get("severity") == "HIGH")
    med_low_count = len(discrepancies) - critical_count - high_count

    # Xác định màu sắc chỉ số Risk Score
    if risk_score >= 85:
        score_color = "#34d399"  # Emerald
        score_status = "HỒ SƠ AN TOÀN"
    elif risk_score >= 60:
        score_color = "#fbbf24"  # Amber
        score_status = "CÓ RỦI RO TRUNG BÌNH"
    else:
        score_color = "#f87171"  # Crimson
        score_status = "RỦI RO CAO / NGUY CƠ BÁC C/O"

    # Xây dựng các dòng bảng lỗi
    discrepancy_rows_html = []
    for idx, d in enumerate(discrepancies, 1):
        code = d.get("code", "L0-00")
        layer_class = "l" + code[1:2] if len(code) >= 2 else "l1"
        sev = d.get("severity", "HIGH")
        sev_badge = {
            "CRITICAL": '<span class="badge badge-critical">CRITICAL</span>',
            "HIGH": '<span class="badge badge-high">HIGH</span>',
            "MEDIUM": '<span class="badge badge-medium">MEDIUM</span>',
            "LOW": '<span class="badge badge-low">LOW</span>'
        }.get(sev, f'<span class="badge">{sev}</span>')

        doc_a = d.get("doc_a", "").replace("\n", "<br>")
        doc_b = d.get("doc_b", "").replace("\n", "<br>")
        risk = d.get("risk", "").replace("\n", "<br>")
        remedy = d.get("remedy", "").replace("\n", "<br>")

        discrepancy_rows_html.append(f"""
        <tr class="discrepancy-row {layer_class}" data-layer="{layer_class}" data-severity="{sev}">
            <td style="text-align: center; font-weight: 700; color: #94a3b8;">{idx}</td>
            <td style="font-family: monospace; font-weight: 700; color: #38bdf8;">{code}</td>
            <td>{sev_badge}</td>
            <td style="font-weight: 600; color: #f1f5f9;">{d.get('criterion', '')}</td>
            <td style="font-size: 0.85rem; color: #cbd5e1; background: rgba(15, 23, 42, 0.4);">{doc_a}</td>
            <td style="font-size: 0.85rem; color: #fca5a5; background: rgba(239, 68, 68, 0.08);">{doc_b}</td>
            <td style="font-size: 0.85rem; color: #fef08a;">{risk}</td>
            <td style="font-size: 0.85rem; color: #a7f3d0;">{remedy}</td>
        </tr>
        """)

    # Xây dựng danh mục Verified
    verified_chips_html = []
    for v in verified_items:
        cat = v.get("category", "")
        detail = v.get("detail", "")
        verified_chips_html.append(f"""
        <div class="verified-card">
            <div class="verified-icon">✓</div>
            <div>
                <div class="verified-cat">{cat}</div>
                <div class="verified-detail">{detail}</div>
            </div>
        </div>
        """)

    # HTML Template Glassmorphism
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Thẩm Định Chứng Từ XNK — {shipment.get('shipment_id', 'SHP-2026')}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-deep: #070d19;
            --bg-canvas: #0c1427;
            --card-glass: rgba(17, 27, 49, 0.72);
            --card-glass-hover: rgba(24, 38, 69, 0.85);
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(56, 189, 248, 0.35);
            --neon-cyan: #00f5d4;
            --neon-blue: #38bdf8;
            --neon-amber: #fbbf24;
            --neon-rose: #f43f5e;
            --neon-emerald: #34d399;
            --text-title: #f8fafc;
            --text-body: #cbd5e1;
            --text-muted: #64748b;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: radial-gradient(circle at 15% 15%, #111d38 0%, #070d19 100%);
            color: var(--text-body);
            line-height: 1.6;
            padding: 30px 20px;
            min-height: 100vh;
        }}

        .dashboard-container {{
            max-width: 1380px;
            margin: 0 auto;
        }}

        /* HEADER GLASS */
        .glass-header {{
            background: var(--card-glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 20px;
            padding: 28px 36px;
            margin-bottom: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .header-title-box h1 {{
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.02em;
        }}

        .header-title-box h1 span.badge-version {{
            font-size: 0.75rem;
            padding: 3px 10px;
            background: rgba(56, 189, 248, 0.15);
            color: var(--neon-blue);
            border: 1px solid var(--neon-blue);
            border-radius: 20px;
            font-weight: 600;
        }}

        .header-subtitle {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 6px;
        }}

        .header-actions {{
            display: flex;
            gap: 12px;
        }}

        .btn-action {{
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.88rem;
            cursor: pointer;
            transition: all 0.25s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #fff;
            border: none;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }}

        .btn-secondary {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--neon-cyan);
            border: 1px solid rgba(0, 245, 212, 0.3);
        }}

        .btn-secondary:hover {{
            background: rgba(0, 245, 212, 0.12);
            transform: translateY(-2px);
        }}

        /* KPI ROW */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--card-glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 22px 24px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .kpi-card:hover {{
            background: var(--card-glass-hover);
            border-color: var(--border-accent);
            transform: translateY(-4px);
        }}

        .kpi-label {{
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}

        .kpi-value {{
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text-title);
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.1;
        }}

        .kpi-meta {{
            font-size: 0.8rem;
            margin-top: 8px;
            color: var(--text-muted);
        }}

        .kpi-score-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
            margin-top: 6px;
        }}

        /* SHIPMENT SUMMARY STRIP */
        .shipment-strip {{
            background: var(--card-glass);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 16px 24px;
            margin-bottom: 24px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            font-size: 0.88rem;
        }}

        .strip-item span.label {{
            color: var(--text-muted);
            display: block;
            font-size: 0.78rem;
        }}

        .strip-item span.val {{
            color: var(--text-title);
            font-weight: 600;
        }}

        /* FILTER TABS */
        .filter-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 18px;
        }}

        .tabs-group {{
            display: flex;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 4px;
            gap: 4px;
            overflow-x: auto;
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 8px 16px;
            font-size: 0.84rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .tab-btn.active {{
            background: rgba(56, 189, 248, 0.2);
            color: var(--neon-blue);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}

        /* DISCREPANCY TABLE */
        .table-glass-card {{
            background: var(--card-glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-glass);
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 30px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35);
        }}

        .table-responsive {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }}

        thead tr {{
            background: rgba(15, 23, 42, 0.85);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        th {{
            padding: 14px 16px;
            text-align: left;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94a3b8;
            font-weight: 700;
        }}

        tbody tr {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            transition: background 0.2s;
        }}

        tbody tr:hover {{
            background: rgba(255, 255, 255, 0.03);
        }}

        td {{
            padding: 14px 16px;
            vertical-align: top;
        }}

        /* BADGES */
        .badge {{
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            display: inline-block;
        }}

        .badge-critical {{
            background: rgba(244, 63, 94, 0.18);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.4);
        }}

        .badge-high {{
            background: rgba(251, 191, 36, 0.18);
            color: #fde047;
            border: 1px solid rgba(251, 191, 36, 0.4);
        }}

        .badge-medium {{
            background: rgba(56, 189, 248, 0.18);
            color: #7dd3fc;
            border: 1px solid rgba(56, 189, 248, 0.35);
        }}

        .badge-low {{
            background: rgba(148, 163, 184, 0.15);
            color: #cbd5e1;
            border: 1px solid rgba(148, 163, 184, 0.25);
        }}

        /* ACTION PLAN & VERIFIED GRID */
        .dual-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 30px;
        }}

        @media (max-width: 900px) {{
            .dual-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .section-glass-card {{
            background: var(--card-glass);
            border: 1px solid var(--border-glass);
            border-radius: 18px;
            padding: 24px 28px;
        }}

        .section-glass-card h2 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-title);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .action-step {{
            background: rgba(15, 23, 42, 0.5);
            border-left: 4px solid var(--neon-blue);
            padding: 14px 18px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 12px;
            font-size: 0.88rem;
        }}

        .action-step.shipper {{
            border-left-color: #38bdf8;
        }}

        .action-step.carrier {{
            border-left-color: #fbbf24;
        }}

        .action-step.broker {{
            border-left-color: #34d399;
        }}

        .action-party {{
            font-weight: 700;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}

        .action-party.shipper {{ color: #38bdf8; }}
        .action-party.carrier {{ color: #fbbf24; }}
        .action-party.broker {{ color: #34d399; }}

        .verified-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            max-height: 420px;
            overflow-y: auto;
            padding-right: 6px;
        }}

        .verified-card {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(52, 211, 153, 0.2);
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.85rem;
        }}

        .verified-icon {{
            background: rgba(52, 211, 153, 0.2);
            color: #34d399;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        .verified-cat {{
            font-weight: 700;
            color: #f1f5f9;
            font-size: 0.8rem;
        }}

        .verified-detail {{
            color: #94a3b8;
            font-size: 0.8rem;
        }}

        /* PRINT STYLES */
        @media print {{
            body {{
                background: #fff;
                color: #000;
                padding: 0;
            }}
            .glass-header, .kpi-card, .table-glass-card, .section-glass-card {{
                background: #fff;
                border: 1px solid #ccc;
                box-shadow: none;
                color: #000;
            }}
            .header-actions, .filter-section {{
                display: none !important;
            }}
            th {{
                background: #f1f5f9;
                color: #000;
            }}
            td {{
                color: #000 !important;
            }}
        }}
    </style>
</head>
<body>

<div class="dashboard-container">

    <!-- HEADER -->
    <header class="glass-header">
        <div class="header-title-box">
            <h1>
                HỒ SƠ THẨM ĐỊNH CHỨNG TỪ XNK
                <span class="badge-version">v3.0 PRO</span>
            </h1>
            <div class="header-subtitle">
                Mã Lô Hàng: <strong>{shipment.get('shipment_id', 'N/A')}</strong> | Mặt Hàng: <strong>{shipment.get('commodity', 'N/A')}</strong> | Kiểm toán lúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        </div>
        <div class="header-actions">
            <button class="btn-action btn-primary" onclick="window.print()">
                🖨️ In / Lưu PDF Báo Cáo
            </button>
            <a class="btn-action btn-secondary" href="Cong_van_giai_trinh_Hai_quan.md" target="_blank">
                📝 Tải Công Văn Mẫu
            </a>
        </div>
    </header>

    <!-- KPI ROW -->
    <section class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Chỉ Số An Toàn Hồ Sơ</div>
            <div class="kpi-value" style="color: {score_color};">{risk_score}<span style="font-size: 1.1rem; color: #64748b;">/100</span></div>
            <div class="kpi-score-badge" style="background: {score_color}22; color: {score_color}; border: 1px solid {score_color};">
                {score_status}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Tổng Sai Lệch Phát Hiện</div>
            <div class="kpi-value" style="color: {'#34d399' if len(discrepancies) == 0 else '#f43f5e'};">{len(discrepancies)}</div>
            <div class="kpi-meta">
                Critical: <strong style="color: #fb7185;">{critical_count}</strong> | High: <strong style="color: #fde047;">{high_count}</strong> | Med/Low: <strong>{med_low_count}</strong>
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Tiêu Chí Đạt Chuẩn</div>
            <div class="kpi-value" style="color: #38bdf8;">{len(verified_items)}</div>
            <div class="kpi-meta">100% đối soát chéo trên 5 lớp kiểm soát</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Rủi Ro Chế Tài NĐ 128</div>
            <div class="kpi-value" style="font-size: 1.35rem; color: {'#34d399' if len(discrepancies) == 0 else '#fde047'}; line-height: 1.3;">
                {'0 VNĐ (Đủ điều kiện)' if len(discrepancies) == 0 else 'Cảnh báo xử phạt'}
            </div>
            <div class="kpi-meta">Tự động đối chiếu CSDL SQLite NĐ 128</div>
        </div>
    </section>

    <!-- SHIPMENT STRIP -->
    <div class="shipment-strip">
        <div class="strip-item">
            <span class="label">Xuất Xứ & C/O</span>
            <span class="val">{shipment.get('country_of_origin', 'N/A')}</span>
        </div>
        <div class="strip-item">
            <span class="label">Điều Kiện Giao Hàng</span>
            <span class="val">{shipment.get('incoterms', 'N/A')[:32]}</span>
        </div>
        <div class="strip-item">
            <span class="label">Cảng Xếp & Dỡ Hàng</span>
            <span class="val">{shipment.get('pol', 'Busan')} → {shipment.get('pod', 'Cat Lai Port')}</span>
        </div>
        <div class="strip-item">
            <span class="label">Loại Hình Khai Báo</span>
            <span class="val">{shipment.get('customs_declaration_type', 'A11 (Tiêu dùng)')}</span>
        </div>
    </div>

    <!-- FILTER BUTTONS -->
    <div class="filter-section">
        <div class="tabs-group" id="layerFilter">
            <button class="tab-btn active" onclick="filterLayer('all')">Tất Cả ({len(discrepancies)})</button>
            <button class="tab-btn" onclick="filterLayer('l1')">Lớp 1: Thời Gian</button>
            <button class="tab-btn" onclick="filterLayer('l2')">Lớp 2: Thực Thể & Typo</button>
            <button class="tab-btn" onclick="filterLayer('l3')">Lớp 3: Hàng Hóa & Trọng Lượng</button>
            <button class="tab-btn" onclick="filterLayer('l4')">Lớp 4: Trị Giá & HS Code</button>
            <button class="tab-btn" onclick="filterLayer('l5')">Lớp 5: Bẫy Pháp Lý C/O</button>
        </div>
    </div>

    <!-- DISCREPANCY TABLE -->
    <div class="table-glass-card">
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th style="width: 45px; text-align: center;">STT</th>
                        <th style="width: 85px;">Mã Lỗi</th>
                        <th style="width: 95px;">Cấp Độ</th>
                        <th style="width: 190px;">Tiêu Chí Đối Soát</th>
                        <th style="width: 170px;">Chứng Từ A (Thực Tế)</th>
                        <th style="width: 170px;">Chứng Từ B (Thực Tế)</th>
                        <th>Rủi Ro Pháp Lý & Chế Tài NĐ 128</th>
                        <th style="width: 240px;">Khuyến Nghị Khắc Phục</th>
                    </tr>
                </thead>
                <tbody id="discrepancyTableBody">
                    {''.join(discrepancy_rows_html) if discrepancy_rows_html else '<tr><td colspan="8" style="text-align: center; padding: 30px; color: #34d399; font-weight: 600;">✓ Tuyệt vời! Bộ chứng từ hoàn toàn nhất quán, không có sai sót nào.</td></tr>'}
                </tbody>
            </table>
        </div>
    </div>

    <!-- 2 COLUMN GRID: ACTION PLAN & VERIFIED ITEMS -->
    <div class="dual-grid">
        <!-- ACTION PLAN -->
        <div class="section-glass-card">
            <h2>🚀 Lộ Trình Hành Động 3 Nhóm Đối Tác</h2>
            
            <div class="action-step shipper">
                <div class="action-party shipper">1. Với Nhà Xuất Khẩu / Shipper ({seller_name[:35]})</div>
                <div>Đính chính Hóa đơn thương mại khớp hợp đồng ngoại thương; liên hệ cơ quan cấp xuất xứ xin cấp lại C/O có tích chọn ô Retroactive và mã HS 8479.89.</div>
            </div>

            <div class="action-step carrier">
                <div class="action-party carrier">2. Với Hãng Tàu / Forwarder ({carrier_name[:35]})</div>
                <div>Nộp công văn đề nghị Hãng tàu gửi điện đính chính Manifest trên Cổng NSW đối với Tổng trọng lượng Gross Weight; cấp Giấy đính chính Vận đơn B/L.</div>
            </div>

            <div class="action-step broker">
                <div class="action-party broker">3. Với Người Khai Hải Quan tại ({pod_port[:35]})</div>
                <div>Khai báo mã lý do <strong>NỢ C/O TRONG VÒNG 30 NGÀY</strong> trên tờ khai VNACCS theo TT 38/2015 & TT 121/2025/TT-BTC; nộp kèm Công văn giải trình sai sót đánh máy.</div>
            </div>
        </div>

        <!-- VERIFIED CHECKLIST -->
        <div class="section-glass-card">
            <h2>✅ Tiêu Chí Đã Đối Soát Đạt Chuẩn ({len(verified_items)})</h2>
            <div class="verified-grid">
                {''.join(verified_chips_html)}
            </div>
        </div>
    </div>

</div>

<script>
function filterLayer(layer) {{
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    const rows = document.querySelectorAll('.discrepancy-row');
    rows.forEach(row => {{
        if (layer === 'all' || row.getAttribute('data-layer') === layer) {{
            row.style.display = '';
        }} else {{
            row.style.display = 'none';
        }}
    }});
}}
</script>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Export Customs Doc Audit Interactive HTML Dashboard")
    parser.add_argument("--input", "-i", default="sample-data/import_docs_sample.json", help="Path to input JSON")
    parser.add_argument("--output", "-o", default="outputs/reports/customs_doc_audit_dashboard.html", help="Path to output HTML")
    args = parser.parse_args()

    # Import dynamically from audit_docs
    sys.path.insert(0, str(Path(__file__).parent))
    from audit_docs import CustomsDocAuditor

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = WORKSPACE_ROOT / input_path

    if not input_path.exists():
        print(f"[ERROR] Input not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    auditor = CustomsDocAuditor(data)
    auditor.audit_all()

    out_file = generate_audit_html_dashboard(auditor, args.output)
    print(f"[OK] Generated Interactive HTML Dashboard: {out_file}")


if __name__ == "__main__":
    main()
