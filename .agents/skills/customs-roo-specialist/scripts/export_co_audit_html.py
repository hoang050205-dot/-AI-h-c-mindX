#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROO & C/O Glassmorphism HTML Report Exporter (export_co_audit_html.py)
Chuyên viên Cao cấp Thẩm định Quy tắc Xuất xứ Hàng hóa (ROO Specialist)
Tạo Dashboard HTML Glassmorphism cao cấp: Hiển thị Ma trận Box-by-Box, Điểm Questionnaire, Cây xuất xứ và Liên kết Sổ tay Tri thức Số NotebookLM.
"""

import sys
import json
import argparse
import io
from typing import Dict, Any, Optional

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


NOTEBOOK_URL = "https://notebook.google.com/notebook/48e2c8d1-d804-484d-bc15-32f518077df6"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Thẩm Định C/O & Quy Tắc Xuất Xứ (ROO) — __CO_REF__</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #070d19;
            --card-bg: rgba(15, 23, 42, 0.75);
            --card-border: rgba(255, 255, 255, 0.08);
            --cyan-neon: #00f5d4;
            --sky-neon: #38bdf8;
            --amber-neon: #fbbf24;
            --rose-neon: #f43f5e;
            --emerald-neon: #34d399;
            --purple-neon: #a855f7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(0, 245, 212, 0.08) 0px, transparent 50%),
                radial-gradient(at 50% 50%, rgba(168, 85, 247, 0.06) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            line-height: 1.6;
            padding: 30px 20px;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
        }

        /* HEADER */
        .header-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(20px);
            margin-bottom: 25px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            position: relative;
            overflow: hidden;
        }

        .header-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--cyan-neon), var(--sky-neon), var(--purple-neon));
        }

        .header-title h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }

        .header-subtitle {
            font-size: 14px;
            color: var(--text-muted);
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }

        .tag-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .tag-form {
            background: rgba(56, 189, 248, 0.15);
            color: var(--sky-neon);
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .tag-fta {
            background: rgba(168, 85, 247, 0.15);
            color: var(--purple-neon);
            border: 1px solid rgba(168, 85, 247, 0.3);
        }

        .notebook-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 22px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(0, 245, 212, 0.2), rgba(56, 189, 248, 0.2));
            color: var(--cyan-neon);
            border: 1px solid rgba(0, 245, 212, 0.4);
            text-decoration: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 14px;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 245, 212, 0.15);
        }

        .notebook-btn:hover {
            transform: translateY(-2px);
            background: linear-gradient(135deg, rgba(0, 245, 212, 0.35), rgba(56, 189, 248, 0.35));
            box-shadow: 0 0 30px rgba(0, 245, 212, 0.3);
            color: #ffffff;
        }

        /* KPI GRID */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .kpi-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 22px;
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            position: relative;
        }

        .kpi-label {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .kpi-value {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 4px;
        }

        .kpi-status-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }

        .status-qualified {
            background: rgba(52, 211, 153, 0.15);
            color: var(--emerald-neon);
            border: 1px solid rgba(52, 211, 153, 0.3);
        }

        .status-warning {
            background: rgba(251, 191, 36, 0.15);
            color: var(--amber-neon);
            border: 1px solid rgba(251, 191, 36, 0.3);
        }

        .status-rejected {
            background: rgba(244, 63, 94, 0.15);
            color: var(--rose-neon);
            border: 1px solid rgba(244, 63, 94, 0.3);
        }

        /* SECTION CARD */
        .content-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 28px;
            backdrop-filter: blur(20px);
            margin-bottom: 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--card-border);
        }

        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 19px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-title i {
            color: var(--cyan-neon);
        }

        /* ORIGIN TREE */
        .origin-tree {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
            margin-top: 15px;
        }

        .tree-node {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 18px;
            position: relative;
        }

        .tree-node.active-branch {
            border-color: rgba(0, 245, 212, 0.4);
            background: rgba(0, 245, 212, 0.05);
        }

        .tree-node-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }

        .tree-node-desc {
            font-size: 13px;
            color: var(--text-muted);
        }

        /* TABLE */
        .table-responsive {
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid var(--card-border);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
            text-align: left;
        }

        th {
            background: rgba(30, 41, 59, 0.8);
            color: var(--text-muted);
            padding: 14px 16px;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11.5px;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--card-border);
        }

        td {
            padding: 14px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        .badge-box {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            color: var(--sky-neon);
            background: rgba(56, 189, 248, 0.1);
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }

        .badge-status-match {
            color: var(--emerald-neon);
            font-weight: 600;
        }

        .badge-status-mismatch {
            color: var(--rose-neon);
            font-weight: 700;
        }

        .badge-risk-low {
            color: var(--emerald-neon);
        }

        .badge-risk-high {
            color: var(--rose-neon);
            font-weight: 700;
        }

        /* CHECKLIST */
        .chk-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }

        .chk-item {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 14px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 13.5px;
        }

        .chk-icon-ready {
            color: var(--emerald-neon);
            font-size: 18px;
        }

        .chk-icon-missing {
            color: var(--rose-neon);
            font-size: 18px;
        }

        /* FOOTER */
        .footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 12.5px;
            margin-top: 30px;
            padding: 20px;
        }

        .footer a {
            color: var(--cyan-neon);
            text-decoration: none;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- HEADER -->
    <div class="header-card">
        <div class="header-title">
            <h1>THẨM ĐỊNH QUY TẮC XUẤT XỨ (ROO) & HỒ SƠ C/O</h1>
            <div class="header-subtitle">
                <span>Số C/O: <strong style="color: #fff;">__CO_REF__</strong></span>
                <span class="tag-badge tag-form">__FORM_TYPE__</span>
                <span class="tag-badge tag-fta">__FTA_NAME__</span>
                <span>Ngày cấp: __ISSUE_DATE__</span>
            </div>
        </div>
        <div>
            <a href="__NOTEBOOK_URL__" target="_blank" class="notebook-btn">
                <span>📖 Sổ Tay Tri Thức Số C/O ROO (NotebookLM)</span>
            </a>
        </div>
    </div>

    <!-- 4 KPI CARDS -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Kết Luận Thẩm Định</div>
            <div class="kpi-value" style="font-size: 20px; line-height: 1.3;">
                <span class="kpi-status-badge __VERDICT_CLASS__">__VERDICT_TEXT__</span>
            </div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px;">__FINDINGS_COUNT__ sai lệch & rủi ro</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Tiêu Chí Khai Báo (Box 8)</div>
            <div class="kpi-value" style="color: var(--cyan-neon); font-size: 24px;">__DECLARED_CRITERION__</div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px;">Quy tắc cụ thể mặt hàng: __PSR_RULE__</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Hàm Lượng Giá Trị Tính Toán</div>
            <div class="kpi-value" style="color: var(--sky-neon);">__CALC_VALUE__</div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px;">__VALUE_FORMULA_NOTE__</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Điểm Sẵn Sàng Xác Minh Hải Quan</div>
            <div class="kpi-value" style="color: var(--emerald-neon);">__SCORE__/100</div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px;">Checklist Questionnaire: __READINESS_STATUS__</div>
        </div>
    </div>

    <!-- CÂY XUẤT XỨ CHUẨN (ORIGIN TREE) -->
    <div class="content-card">
        <div class="section-header">
            <div class="section-title">
                <i>🌲</i> CÂY TIÊU CHÍ XUẤT XỨ CHUẨN (ORIGIN DETERMINATION TREE)
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">Phân định 3 nhánh xuất xứ độc lập theo quy định FTA</div>
        </div>
        <div class="origin-tree">
            <div class="tree-node __NODE_WO_CLASS__">
                <div class="tree-node-title">
                    <span>1. Nhánh WO (Wholly Obtained)</span>
                    <span>__NODE_WO_BADGE__</span>
                </div>
                <div class="tree-node-desc">
                    Xuất xứ thuần túy: Thu hoạch, khai thác thô hoặc sinh ra và nuôi dưỡng toàn bộ tại một nước thành viên (khoáng sản, nông sản, vật nuôi). Không dùng cho công nghiệp gia công có nguyên liệu nhập.
                </div>
            </div>
            <div class="tree-node __NODE_PE_CLASS__">
                <div class="tree-node-title">
                    <span>2. Nhánh PE (Produced Entirely)</span>
                    <span>__NODE_PE_BADGE__</span>
                </div>
                <div class="tree-node-desc">
                    Sản xuất hoàn toàn trong lãnh thổ một hoặc nhiều nước thành viên, <strong>chỉ sử dụng 100% nguyên liệu đã có sẵn xuất xứ FTA</strong> (chuỗi cung ứng nội khối hoàn toàn).
                </div>
            </div>
            <div class="tree-node __NODE_PSR_CLASS__">
                <div class="tree-node-title">
                    <span>3. Nhánh PSR (Product Specific Rules)</span>
                    <span>__NODE_PSR_BADGE__</span>
                </div>
                <div class="tree-node-desc">
                    Có sử dụng nguyên liệu không có xuất xứ (NOM): Đạt CTC (CC/CTH/CTSH) kèm ngoại trừ, RVC/VL (Hàm lượng giá trị), hoặc SP (Công đoạn sản xuất đặc trưng) và kiểm soát De Minimis (&le; 10%).
                </div>
            </div>
        </div>
    </div>

    <!-- MA TRẬN ĐỐI CHIẾU BOX-BY-BOX -->
    <div class="content-card">
        <div class="section-header">
            <div class="section-title">
                <i>📦</i> MA TRẬN ĐỐI CHIẾU CHI TIẾT TỪNG Ô (BOX-BY-BOX AUDIT)
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">Đối soát đồng nhất giữa C/O và Hóa đơn, Vận đơn, Packing List, Tờ khai</div>
        </div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th style="width: 100px;">Vị trí (Box)</th>
                        <th style="width: 160px;">Chỉ mục nghiệp vụ</th>
                        <th>Nội dung trên C/O & Dữ liệu đối chiếu</th>
                        <th style="width: 130px;">Trạng thái</th>
                        <th style="width: 110px;">Rủi ro</th>
                        <th>Căn cứ & Đánh giá chuyên sâu</th>
                    </tr>
                </thead>
                <tbody>
                    __BOX_ROWS__
                </tbody>
            </table>
        </div>
    </div>

    <!-- ĐIỀU KIỆN VẬN CHUYỂN & HỒ SƠ XÁC MINH QUESTIONNAIRE -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px;">
        <!-- Vận chuyển suốt -->
        <div class="content-card">
            <div class="section-header">
                <div class="section-title">
                    <i>🚢</i> VẬN CHUYỂN TRỰC TIẾP & HIỆU LỰC
                </div>
            </div>
            <div style="font-size: 14px; margin-bottom: 12px;">
                <strong>Hành trình:</strong> __ROUTE_DETAIL__
            </div>
            <div style="font-size: 14px; margin-bottom: 12px;">
                <strong>Loại vận đơn:</strong> <span class="badge-box">__BL_TYPE__</span>
            </div>
            <div style="font-size: 14px; margin-bottom: 12px;">
                <strong>Hiệu lực C/O:</strong> __VALIDITY_NOTE__
            </div>
            <div style="background: rgba(30, 41, 59, 0.5); padding: 14px; border-radius: 10px; font-size: 13px; border-left: 3px solid var(--cyan-neon);">
                <strong>Lưu ý nghiệp vụ:</strong> Nếu tàu chuyển tải qua cảng trung chuyển ngoài khối, bắt buộc lưu trữ Through B/L hoặc Xác nhận không can thiệp (CNM) từ Hải quan quá cảnh để tránh bị bác C/O khi kiểm tra sau thông quan.
            </div>
        </div>

        <!-- Verification Questionnaire Readiness -->
        <div class="content-card">
            <div class="section-header">
                <div class="section-title">
                    <i>🛡️</i> HỒ SƠ ỨNG PHÓ XÁC MINH HẢI QUAN (QUESTIONNAIRE)
                </div>
                <div class="badge-box">Điểm: __SCORE__/100</div>
            </div>
            <div class="chk-grid">
                __CHK_ITEMS__
            </div>
            <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--card-border); font-size: 12.5px; color: var(--text-muted);">
                <strong>Thời hạn luật định:</strong> Lưu trữ hồ sơ <strong>5 năm</strong> (Việt Nam) / <strong>3 năm</strong> (FTA). Phản hồi xác minh hồ sơ tối đa <strong>90 ngày</strong>; chấp thuận kiểm tra nhà máy trong <strong>30 ngày</strong>; tổng quy trình kết thúc trong <strong>180 ngày</strong>.
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        Báo cáo Thẩm định Chuyên sâu được khởi tạo tự động bởi <strong>ROO Specialist v1.0 (Customs Golden Suite)</strong>.<br>
        Dữ liệu tri thức nội bộ được liên thông với Sổ tay Tri thức Số: <a href="__NOTEBOOK_URL__" target="_blank">Google NotebookLM C/O ROO Master</a>.
    </div>
</div>

</body>
</html>
"""

def generate_co_audit_html(co_audit_data: Dict[str, Any], origin_calc_data: Optional[Dict[str, Any]] = None) -> str:
    co_ref = co_audit_data.get("co_reference_no", "N/A")
    form_type = co_audit_data.get("form_type", "Form D")
    fta_name = co_audit_data.get("fta", "ATIGA")
    issue_date = co_audit_data.get("validity", {}).get("issue_date", "N/A")

    badge = co_audit_data.get("verdict_badge", "QUALIFIED")
    if badge == "QUALIFIED":
        v_class = "status-qualified"
        v_text = "HỢP LỆ — ĐỦ ĐIỀU KIỆN ÁP DỤNG THUẾ FTA"
    elif badge == "WARNING":
        v_class = "status-warning"
        v_text = "CẢNH BÁO — CÓ SAI SÓT CẦN GIẢI TRÌNH"
    else:
        v_class = "status-rejected"
        v_text = "NGHIÊM TRỌNG — NGUY CƠ BÁC C/O HOẶC TRUY THU"

    findings_cnt = co_audit_data.get("findings_count", 0)

    # Calculation values
    declared_criterion = "N/A"
    psr_rule = "N/A"
    calc_value = "N/A"
    formula_note = "Chưa nạp dữ liệu định lượng BOM"

    if origin_calc_data:
        declared_criterion = origin_calc_data.get("declared_criterion", "N/A")
        psr_rule = origin_calc_data.get("psr_rule", origin_calc_data.get("checks", {}).get("ctc_analysis", {}).get("rule_type", "N/A"))
        if "rvc_build_down" in origin_calc_data.get("checks", {}):
            rb = origin_calc_data["checks"]["rvc_build_down"]
            calc_value = f"{rb['rvc_percentage']}% RVC"
            formula_note = f"Build-down (FOB) | Ngưỡng: {rb['threshold']}% (Biên an toàn: {rb['margin']}%)"
        elif "evfta_value_limit" in origin_calc_data.get("checks", {}):
            vl = origin_calc_data["checks"]["evfta_value_limit"]
            calc_value = f"{vl['vnm_ratio']}% VL"
            formula_note = f"Value Limit (EXW) | Hạn mức: &le; {vl['threshold']}%"

    vr = co_audit_data.get("verification_readiness", {})
    score = vr.get("score", 0)
    readiness_status = vr.get("status", "N/A")

    # Tree Nodes active logic
    node_wo_class = "active-branch" if "WO" in declared_criterion.upper() else ""
    node_wo_badge = '<span class="tag-badge tag-fta">ÁP DỤNG</span>' if node_wo_class else '<span style="font-size: 11px; color: var(--text-muted);">Không áp dụng</span>'

    node_pe_class = "active-branch" if "PE" in declared_criterion.upper() else ""
    node_pe_badge = '<span class="tag-badge tag-fta">ÁP DỤNG</span>' if node_pe_class else '<span style="font-size: 11px; color: var(--text-muted);">Không áp dụng</span>'

    node_psr_class = "active-branch" if not node_wo_class and not node_pe_class else ""
    node_psr_badge = '<span class="tag-badge tag-fta">ÁP DỤNG</span>' if node_psr_class else '<span style="font-size: 11px; color: var(--text-muted);">Không áp dụng</span>'

    # Box Rows
    box_rows_html = []
    for b in co_audit_data.get("box_matrix", []):
        is_mismatch = b.get("status") in ["LỆCH", "THIẾU TICK", "LỖI QUY CÁCH", "THIẾU FOB", "THIẾU TÊN"]
        stat_class = "badge-status-mismatch" if is_mismatch else "badge-status-match"
        risk_class = "badge-risk-high" if b.get("risk") in ["Rất cao", "Cao"] else "badge-risk-low"

        row = f"""
        <tr>
            <td><span class="badge-box">{b.get('box')}</span></td>
            <td><strong>{b.get('field')}</strong></td>
            <td>{b.get('note', '')}</td>
            <td><span class="{stat_class}">{b.get('status')}</span></td>
            <td><span class="{risk_class}">{b.get('risk')}</span></td>
            <td style="font-size: 12.5px; color: var(--text-muted);">{b.get('note', '')}</td>
        </tr>
        """
        box_rows_html.append(row)

    # Checklist Items
    chk_items_html = []
    ready_docs = vr.get("ready_docs", [])
    missing_docs = vr.get("missing_docs", [])

    for doc in ready_docs:
        chk_items_html.append(f"""
        <div class="chk-item">
            <span class="chk-icon-ready">✅</span>
            <span>{doc}</span>
        </div>
        """)
    for doc in missing_docs:
        chk_items_html.append(f"""
        <div class="chk-item" style="border-color: rgba(244, 63, 94, 0.2); background: rgba(244, 63, 94, 0.05);">
            <span class="chk-icon-missing">⚠️</span>
            <span style="color: var(--rose-neon); font-weight: 500;">Thiếu: {doc}</span>
        </div>
        """)

    dc = co_audit_data.get("direct_consignment", {})
    route_detail = dc.get("route_detail", "N/A")
    bl_type = dc.get("bl_type", "Through B/L")

    val_info = co_audit_data.get("validity", {})
    val_note = "Còn trong hạn 12 tháng (Hợp lệ)" if val_info.get("passed", True) else f"Hết hạn hiệu lực (Đã vượt quá 12 tháng)"

    html = HTML_TEMPLATE
    html = html.replace("__CO_REF__", co_ref)
    html = html.replace("__FORM_TYPE__", form_type)
    html = html.replace("__FTA_NAME__", fta_name)
    html = html.replace("__ISSUE_DATE__", issue_date)
    html = html.replace("__NOTEBOOK_URL__", NOTEBOOK_URL)

    html = html.replace("__VERDICT_CLASS__", v_class)
    html = html.replace("__VERDICT_TEXT__", v_text)
    html = html.replace("__FINDINGS_COUNT__", str(findings_cnt))

    html = html.replace("__DECLARED_CRITERION__", declared_criterion)
    html = html.replace("__PSR_RULE__", psr_rule)
    html = html.replace("__CALC_VALUE__", calc_value)
    html = html.replace("__VALUE_FORMULA_NOTE__", formula_note)

    html = html.replace("__SCORE__", str(score))
    html = html.replace("__READINESS_STATUS__", readiness_status)

    html = html.replace("__NODE_WO_CLASS__", node_wo_class)
    html = html.replace("__NODE_WO_BADGE__", node_wo_badge)
    html = html.replace("__NODE_PE_CLASS__", node_pe_class)
    html = html.replace("__NODE_PE_BADGE__", node_pe_badge)
    html = html.replace("__NODE_PSR_CLASS__", node_psr_class)
    html = html.replace("__NODE_PSR_BADGE__", node_psr_badge)

    html = html.replace("__BOX_ROWS__", "\n".join(box_rows_html))
    html = html.replace("__CHK_ITEMS__", "\n".join(chk_items_html))

    html = html.replace("__ROUTE_DETAIL__", route_detail)
    html = html.replace("__BL_TYPE__", bl_type)
    html = html.replace("__VALIDITY_NOTE__", val_note)

    return html

def load_json_file(filepath: str) -> Dict[str, Any]:
    for enc in ["utf-8-sig", "utf-8", "utf-16", "cp1252"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return json.load(f)
        except Exception:
            continue
    raise ValueError(f"Không thể giải mã file JSON: {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Export ROO & C/O Audit HTML Dashboard")
    parser.add_argument("--audit-file", "-a", type=str, required=True, help="File JSON kết quả từ audit_co_box.py")
    parser.add_argument("--calc-file", "-c", type=str, help="File JSON kết quả từ calculate_origin.py")
    parser.add_argument("--output", "-o", type=str, default="co_roo_audit_dashboard.html", help="Đường dẫn file HTML kết xuất")

    args = parser.parse_args()

    audit_data = load_json_file(args.audit_file)

    calc_data = None
    if args.calc_file:
        calc_data = load_json_file(args.calc_file)

    html_content = generate_co_audit_html(audit_data, calc_data)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Đã kết xuất thành công Dashboard HTML Glassmorphism tại: {args.output}")


if __name__ == "__main__":
    main()
