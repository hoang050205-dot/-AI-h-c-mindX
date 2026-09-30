#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generator for Beta Solutions BI Executive Web Dashboard
Strictly adheres to: knowledge-base/TH_brand_guideline_beta.txt
  - Ngân sách được duyệt: Tím Hoàng Gia (#7C3AED)
  - Chi tiêu thực tế: Xanh Ngọc (#06B6D4)
  - Vượt ngân sách: Hồng San Hô (#F43F5E)
  - Tiết kiệm / hiệu quả: Xanh Bạc Hà (#14B8A6)
  - Font: "Outfit", "Roboto", "Segoe UI"
  - Nền trang: Xám Đậm (#1E1E2E) & Dark Mode sang trọng
"""

import os
import sys

# Đảm bảo in tiếng Việt trên console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "reports", "beta_solutions_bi_dashboard.html")
SCRATCH_JSON = os.path.join(BASE_DIR, "scratch", "raw_records.json")

with open(SCRATCH_JSON, "r", encoding="utf-8") as f:
    raw_records = json.load(f)

raw_records_json_str = json.dumps(raw_records, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Beta Solutions - Realtime BI Budget Dashboard 2026</title>
  
  <!-- Brand Guideline Fonts: Outfit & Roboto -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Roboto:wght@400;500;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    /* ==========================================================================
       1. BRAND GUIDELINE DESIGN TOKENS (BETA SOLUTIONS JSC)
       ========================================================================== */
    :root {
      /* Base Dark Surfaces */
      --bg-brand-dark: #1e1e2e;          /* Xám Đậm sang trọng theo Brand Guideline */
      --bg-cosmic: #12111d;              /* Nền sâu vũ trụ */
      --bg-surface: rgba(30, 30, 46, 0.70);
      --bg-surface-elevated: rgba(43, 42, 65, 0.75);
      --bg-surface-hover: rgba(58, 56, 88, 0.65);
      
      /* Glassmorphism Borders & Highlights */
      --glass-border: 1px solid rgba(255, 255, 255, 0.09);
      --glass-specular-top: inset 0 1px 1px 0 rgba(255, 255, 255, 0.16);
      --glass-shadow: 0 10px 36px 0 rgba(0, 0, 0, 0.48);
      --glass-shadow-lg: 0 16px 48px 0 rgba(0, 0, 0, 0.60);

      /* ==========================================================================
         MÀU SẮC THƯƠNG HIỆU BẮT BUỘC (BRAND GUIDELINE):
         - Tím Hoàng Gia (Ngân sách được duyệt): #7C3AED
         - Xanh Ngọc (Chi tiêu thực tế): #06B6D4
         - Hồng San Hô (Vượt ngân sách / Cảnh báo): #F43F5E
         - Xanh Bạc Hà (Tiết kiệm / Hiệu quả): #14B8A6
         ========================================================================== */
      --brand-purple: #7C3AED;
      --brand-purple-light: #A78BFA;
      --brand-purple-glow: rgba(124, 58, 237, 0.35);
      --brand-purple-bg: rgba(124, 58, 237, 0.15);

      --brand-cyan: #06B6D4;
      --brand-cyan-light: #22D3EE;
      --brand-cyan-glow: rgba(6, 182, 212, 0.35);
      --brand-cyan-bg: rgba(6, 182, 212, 0.15);

      --brand-coral: #F43F5E;
      --brand-coral-light: #FB7185;
      --brand-coral-glow: rgba(244, 63, 94, 0.35);
      --brand-coral-bg: rgba(244, 63, 94, 0.15);

      --brand-mint: #14B8A6;
      --brand-mint-light: #2DD4BF;
      --brand-mint-glow: rgba(20, 184, 166, 0.35);
      --brand-mint-bg: rgba(20, 184, 166, 0.15);

      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;

      /* Brand Typography */
      --font-brand: 'Outfit', 'Roboto', 'Segoe UI', sans-serif;
      --font-mono: 'JetBrains Mono', Consolas, monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-brand-dark);
      background-image: radial-gradient(circle at 15% 15%, rgba(124, 58, 237, 0.12) 0%, transparent 45%),
                        radial-gradient(circle at 85% 20%, rgba(6, 182, 212, 0.10) 0%, transparent 40%),
                        radial-gradient(circle at 50% 85%, rgba(20, 184, 166, 0.08) 0%, transparent 50%);
      color: var(--text-primary);
      font-family: var(--font-brand);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.5;
      position: relative;
      padding-bottom: 50px;
    }

    /* ==========================================================================
       2. AMBIENT GLOW ORBS (BRAND TONAL HARMONY)
       ========================================================================== */
    .ambient-orb {
      position: fixed;
      border-radius: 50%;
      filter: blur(130px);
      pointer-events: none;
      z-index: 0;
      opacity: 0.42;
    }
    .orb-purple { width: 550px; height: 550px; background: rgba(124, 58, 237, 0.22); top: -100px; left: -100px; }
    .orb-cyan   { width: 520px; height: 520px; background: rgba(6, 182, 212, 0.20); top: 320px; right: -100px; }
    .orb-mint   { width: 450px; height: 450px; background: rgba(20, 184, 166, 0.16); bottom: -60px; left: 32%; }

    /* ==========================================================================
       3. LAYOUT CONTAINER & GLASSMORPHISM
       ========================================================================== */
    .app-container {
      position: relative;
      z-index: 1;
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .glass-card {
      background: var(--bg-surface);
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      border: var(--glass-border);
      border-radius: 18px;
      box-shadow: var(--glass-shadow), var(--glass-specular-top);
      transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease;
    }

    .glass-card:hover {
      box-shadow: var(--glass-shadow-lg), var(--glass-specular-top);
    }

    /* ==========================================================================
       4. HEADER SECTION
       ========================================================================== */
    .header-bar {
      padding: 20px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 18px;
    }

    .brand-icon-box {
      width: 52px;
      height: 52px;
      border-radius: 14px;
      background: linear-gradient(135deg, rgba(124, 58, 237, 0.35), rgba(6, 182, 212, 0.30));
      border: 1px solid rgba(124, 58, 237, 0.55);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 20px rgba(124, 58, 237, 0.40);
    }

    .brand-icon-box svg {
      width: 28px;
      height: 28px;
      fill: none;
      stroke: #ffffff;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .brand-text h1 {
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      background: linear-gradient(135deg, #ffffff 40%, var(--brand-purple-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .brand-subtitle {
      font-size: 0.85rem;
      color: var(--text-muted);
      font-weight: 500;
      margin-top: 2px;
    }

    .header-status-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-compliance-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(124, 58, 237, 0.15);
      border: 1px solid rgba(124, 58, 237, 0.40);
      color: var(--brand-purple-light);
    }

    .live-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 14px;
      border-radius: 9999px;
      background: rgba(20, 184, 166, 0.14);
      border: 1px solid rgba(20, 184, 166, 0.40);
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--brand-mint-light);
    }

    .live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: var(--brand-mint);
      box-shadow: 0 0 10px var(--brand-mint);
      position: relative;
    }

    .live-dot::after {
      content: '';
      position: absolute;
      top: -3px;
      left: -3px;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      border: 2px solid var(--brand-mint);
      animation: pulseRadar 2s infinite;
      opacity: 0.8;
    }

    @keyframes pulseRadar {
      0% { transform: scale(0.6); opacity: 1; }
      100% { transform: scale(2.2); opacity: 0; }
    }

    /* ==========================================================================
       5. FILTER CONTROLS BAR (DÃY NÚT BẤM LỌC SÁNG ĐẶC TRƯNG)
       ========================================================================== */
    .filter-panel {
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .filter-row {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .filter-label {
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      min-width: 170px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .filter-label svg {
      width: 16px;
      height: 16px;
      stroke: var(--brand-cyan);
    }

    .filter-btn-group {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      flex: 1;
    }

    .filter-btn {
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      background: rgba(43, 42, 65, 0.65);
      color: var(--text-secondary);
      border: 1px solid rgba(255, 255, 255, 0.10);
      transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      user-select: none;
      outline: none;
      font-family: var(--font-brand);
    }

    .filter-btn:hover {
      background: rgba(58, 56, 88, 0.80);
      border-color: rgba(255, 255, 255, 0.25);
      color: #ffffff;
      transform: translateY(-1px);
    }

    /* ACTIVE STATE - PHẢI SÁNG LÊN THEO TÍM HOÀNG GIA & XANH NGỌC */
    .filter-btn.active {
      background: linear-gradient(135deg, rgba(124, 58, 237, 0.50) 0%, rgba(6, 182, 212, 0.50) 100%) !important;
      border-color: var(--brand-purple-light) !important;
      color: #ffffff !important;
      font-weight: 700 !important;
      box-shadow: 0 0 18px rgba(124, 58, 237, 0.60), inset 0 1px 1px rgba(255, 255, 255, 0.40) !important;
      transform: translateY(-1px);
    }

    .active-indicator-dot {
      display: none;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #ffffff;
      box-shadow: 0 0 8px #ffffff;
    }

    .filter-btn.active .active-indicator-dot {
      display: inline-block;
    }

    .filter-summary-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .filter-summary-info b {
      color: var(--brand-cyan-light);
    }

    /* ==========================================================================
       6. 3 THẺ KPI 3 TẦNG (CHUẨN BRAND GUIDELINE BETA)
       ========================================================================== */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }

    .kpi-card {
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }

    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      opacity: 0.95;
    }

    /* Thẻ 1: Ngân sách -> Tím Hoàng Gia #7C3AED */
    .kpi-card.budget::before {
      background: linear-gradient(90deg, #7C3AED, #A78BFA);
    }

    /* Thẻ 2: Chi tiêu -> Xanh Ngọc #06B6D4 */
    .kpi-card.spent::before {
      background: linear-gradient(90deg, #06B6D4, #22D3EE);
    }

    /* Thẻ 3: Vượt ngân sách -> Hồng San Hô #F43F5E */
    .kpi-card.over::before {
      background: linear-gradient(90deg, #F43F5E, #FB7185);
    }

    /* Tầng 1: Icon & Tiêu đề */
    .kpi-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
    }

    .kpi-title-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .kpi-icon-box {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .kpi-card.budget .kpi-icon-box {
      background: rgba(124, 58, 237, 0.20);
      border: 1px solid rgba(124, 58, 237, 0.45);
      color: var(--brand-purple-light);
    }

    .kpi-card.spent .kpi-icon-box {
      background: rgba(6, 182, 212, 0.20);
      border: 1px solid rgba(6, 182, 212, 0.45);
      color: var(--brand-cyan);
    }

    .kpi-card.over .kpi-icon-box {
      background: rgba(244, 63, 94, 0.20);
      border: 1px solid rgba(244, 63, 94, 0.45);
      color: var(--brand-coral);
    }

    .kpi-icon-box svg {
      width: 22px;
      height: 22px;
      stroke-width: 2;
    }

    .kpi-title {
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--text-muted);
    }

    .kpi-badge {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .kpi-card.budget .kpi-badge {
      background: rgba(124, 58, 237, 0.20);
      border: 1px solid rgba(124, 58, 237, 0.45);
      color: #C4B5FD;
    }

    .kpi-card.spent .kpi-badge {
      background: rgba(6, 182, 212, 0.20);
      border: 1px solid rgba(6, 182, 212, 0.45);
      color: var(--brand-cyan-light);
    }

    .kpi-card.over .kpi-badge {
      background: rgba(244, 63, 94, 0.20);
      border: 1px solid rgba(244, 63, 94, 0.45);
      color: var(--brand-coral-light);
    }

    /* Tầng 2: Con số Hero */
    .kpi-hero {
      font-size: 2.15rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      font-family: var(--font-brand);
      font-variant-numeric: tabular-nums;
      margin-bottom: 14px;
      white-space: nowrap;
    }

    .kpi-card.budget .kpi-hero {
      color: #ffffff;
      text-shadow: 0 0 22px rgba(124, 58, 237, 0.45);
    }

    .kpi-card.spent .kpi-hero {
      color: #ffffff;
      text-shadow: 0 0 22px rgba(6, 182, 212, 0.45);
    }

    .kpi-card.over .kpi-hero {
      color: #ffffff;
      text-shadow: 0 0 22px rgba(244, 63, 94, 0.45);
    }

    /* Tầng 3: Điểm quy chiếu & Benchmark */
    .kpi-bot {
      display: flex;
      flex-direction: column;
      gap: 8px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .kpi-bot-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .kpi-progress-bar-bg {
      width: 100%;
      height: 6px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.08);
      overflow: hidden;
      margin-top: 2px;
    }

    .kpi-progress-bar-fill {
      height: 100%;
      border-radius: 9999px;
      background: linear-gradient(90deg, #06B6D4, #22D3EE);
      transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* ==========================================================================
       7. CHARTS SECTION (TUÂN THỦ TUYỆT ĐỐI BRAND COLORS)
       ========================================================================== */
    .charts-grid {
      display: grid;
      grid-template-columns: 1.6fr 1fr;
      gap: 20px;
    }

    .chart-panel {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-height: 420px;
    }

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 10px;
    }

    .chart-title-box h3 {
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.01em;
    }

    .chart-subtitle {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 3px;
    }

    .chart-legend-custom {
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 0.78rem;
      font-weight: 600;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .legend-color-dot {
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }

    .chart-body {
      flex: 1;
      position: relative;
      width: 100%;
      height: 320px;
    }

    /* ==========================================================================
       8. DATA TABLE MATRIX (BẢNG GIAO DỊCH CHI TIẾT)
       ========================================================================== */
    .table-panel {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .table-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }

    .table-title-box h3 {
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
    }

    .search-box {
      position: relative;
      min-width: 280px;
    }

    .search-box input {
      width: 100%;
      padding: 9px 16px 9px 38px;
      border-radius: 10px;
      background: rgba(43, 42, 65, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #ffffff;
      font-size: 0.85rem;
      font-family: inherit;
      outline: none;
      transition: all 0.2s ease;
    }

    .search-box input:focus {
      border-color: var(--brand-purple-light);
      box-shadow: 0 0 14px rgba(124, 58, 237, 0.40);
    }

    .search-box svg {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      width: 16px;
      height: 16px;
      stroke: var(--text-muted);
    }

    .table-container {
      width: 100%;
      overflow-x: auto;
      max-height: 480px;
      overflow-y: auto;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    table.bi-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.85rem;
    }

    table.bi-table th {
      background: rgba(30, 30, 46, 0.96);
      position: sticky;
      top: 0;
      z-index: 2;
      padding: 12px 16px;
      font-weight: 700;
      font-size: 0.75rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text-muted);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    table.bi-table td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-secondary);
      font-variant-numeric: tabular-nums;
    }

    table.bi-table tbody tr {
      transition: background 0.15s ease;
    }

    table.bi-table tbody tr:hover {
      background: rgba(255, 255, 255, 0.03);
    }

    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      white-space: nowrap;
    }

    /* Tiết kiệm: Xanh Bạc Hà #14B8A6 */
    .badge-tietkiem {
      background: rgba(20, 184, 166, 0.16);
      border: 1px solid rgba(20, 184, 166, 0.45);
      color: var(--brand-mint-light);
    }

    /* Vượt ngân sách: Hồng San Hô #F43F5E */
    .badge-vuot {
      background: rgba(244, 63, 94, 0.20);
      border: 1px solid rgba(244, 63, 94, 0.50);
      color: var(--brand-coral-light);
      font-weight: 700;
      box-shadow: 0 0 10px rgba(244, 63, 94, 0.25);
    }

    /* Responsive */
    @media (max-width: 1080px) {
      .charts-grid {
        grid-template-columns: 1fr;
      }
      .kpi-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 768px) {
      .app-container {
        padding: 16px;
      }
      .filter-label {
        min-width: 100%;
      }
      .header-bar {
        flex-direction: column;
        align-items: flex-start;
      }
    }
  </style>
</head>
<body>

  <!-- Ambient Glow Orbs -->
  <div class="ambient-orb orb-purple"></div>
  <div class="ambient-orb orb-cyan"></div>
  <div class="ambient-orb orb-mint"></div>

  <div class="app-container">

    <!-- 1. HEADER SECTION -->
    <header class="glass-card header-bar">
      <div class="brand-section">
        <div class="brand-icon-box">
          <svg viewBox="0 0 24 24">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <div class="brand-text">
          <h1>BETA SOLUTIONS <span>JSC</span></h1>
          <div class="brand-subtitle">Hệ Thống Phân Tích & Kiểm Soát Ngân Sách Doanh Nghiệp 2026</div>
        </div>
      </div>

      <div class="header-status-group">
        <div class="brand-compliance-pill" title="Tuân thủ Brand Guideline Beta Solutions">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="m9 12 2 2 4-4"></path></svg>
          Brand Guideline: Tím #7C3AED • Xanh Ngọc #06B6D4 • Hồng #F43F5E
        </div>
        <div class="live-status-pill" id="liveSyncPill" title="Tự động đồng bộ mỗi 2 giây từ file Excel gốc">
          <div class="live-dot" id="liveDot"></div>
          <span id="liveStatusText">Live Sync (2s)</span>
        </div>
      </div>
    </header>

    <!-- 2. FILTER CONTROLS BAR (DÃY NÚT BẤM LỌC SÁNG ĐẶC TRƯNG) -->
    <section class="glass-card filter-panel">
      <!-- Lọc theo Quý -->
      <div class="filter-row">
        <div class="filter-label">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
          Chu Kỳ (Quý):
        </div>
        <div class="filter-btn-group" id="quarterFilterGroup">
          <button class="filter-btn active" data-type="quy" data-value="all">
            <span class="active-indicator-dot"></span>Tất cả Quý
          </button>
          <button class="filter-btn" data-type="quy" data-value="Q1-2026">
            <span class="active-indicator-dot"></span>Q1-2026
          </button>
          <button class="filter-btn" data-type="quy" data-value="Q2-2026">
            <span class="active-indicator-dot"></span>Q2-2026
          </button>
          <button class="filter-btn" data-type="quy" data-value="Q3-2026">
            <span class="active-indicator-dot"></span>Q3-2026
          </button>
          <button class="filter-btn" data-type="quy" data-value="Q4-2026">
            <span class="active-indicator-dot"></span>Q4-2026
          </button>
        </div>
      </div>

      <!-- Lọc theo Phòng Ban -->
      <div class="filter-row">
        <div class="filter-label">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          Phòng Ban:
        </div>
        <div class="filter-btn-group" id="deptFilterGroup">
          <button class="filter-btn active" data-type="dept" data-value="all">
            <span class="active-indicator-dot"></span>Tất cả Phòng Ban
          </button>
          <button class="filter-btn" data-type="dept" data-value="Cong Nghe">
            <span class="active-indicator-dot"></span>Công Nghệ
          </button>
          <button class="filter-btn" data-type="dept" data-value="Ke Toan">
            <span class="active-indicator-dot"></span>Kế Toán
          </button>
          <button class="filter-btn" data-type="dept" data-value="Kinh Doanh">
            <span class="active-indicator-dot"></span>Kinh Doanh
          </button>
          <button class="filter-btn" data-type="dept" data-value="Marketing">
            <span class="active-indicator-dot"></span>Marketing
          </button>
          <button class="filter-btn" data-type="dept" data-value="Nhan Su">
            <span class="active-indicator-dot"></span>Nhân Sự
          </button>
          <button class="filter-btn" data-type="dept" data-value="Van Phong">
            <span class="active-indicator-dot"></span>Văn Phòng
          </button>
        </div>
      </div>

      <!-- Tóm tắt bộ lọc đang hoạt động -->
      <div class="filter-summary-info">
        <div>
          Trạng thái bộ lọc: <b id="filterSummaryText">Tất cả Quý • Tất cả Phòng Ban</b>
        </div>
        <div>
          Số lượng giao dịch khớp: <b id="matchedTxnCount">300</b> / <span id="totalTxnCount">300</span>
        </div>
      </div>
    </section>

    <!-- 3. 3 THẺ KPI 3 TẦNG (TUÂN THỦ TUYỆT ĐỐI MÀU SẮC GUIDELINE) -->
    <section class="kpi-grid">
      <!-- Thẻ KPI 1: TỔNG NGÂN SÁCH ĐƯỢC DUYỆT -> Tím Hoàng Gia #7C3AED -->
      <div class="glass-card kpi-card budget">
        <div class="kpi-top">
          <div class="kpi-title-group">
            <div class="kpi-icon-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="4" width="20" height="16" rx="2"></rect><line x1="2" y1="10" x2="22" y2="10"></line></svg>
            </div>
            <div>
              <div class="kpi-title">Tổng Ngân Sách Được Duyệt</div>
            </div>
          </div>
          <span class="kpi-badge">Tím Hoàng Gia (#7C3AED)</span>
        </div>
        <div class="kpi-hero" id="kpiBudget" data-counter="82390620999" data-suffix=" ₫">0 ₫</div>
        <div class="kpi-bot">
          <div class="kpi-bot-row">
            <span>Hạn mức phê duyệt:</span>
            <span style="color: var(--brand-purple-light); font-weight: 600;" id="kpiBudgetSub">100.0% hạn mức</span>
          </div>
          <div class="kpi-bot-row">
            <span>Chênh lệch thặng dư:</span>
            <span style="color: var(--brand-mint-light); font-weight: 600;" id="kpiSavingDelta">+4.128.535.450 ₫</span>
          </div>
        </div>
      </div>

      <!-- Thẻ KPI 2: TỔNG CHI TIÊU THỰC TẾ -> Xanh Ngọc #06B6D4 -->
      <div class="glass-card kpi-card spent">
        <div class="kpi-top">
          <div class="kpi-title-group">
            <div class="kpi-icon-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            </div>
            <div>
              <div class="kpi-title">Tổng Chi Tiêu Thực Tế</div>
            </div>
          </div>
          <span class="kpi-badge" id="spentRateBadge">Xanh Ngọc (#06B6D4)</span>
        </div>
        <div class="kpi-hero" id="kpiSpent" data-counter="78262085549" data-suffix=" ₫">0 ₫</div>
        <div class="kpi-bot">
          <div class="kpi-bot-row">
            <span>Tiến độ giải ngân ngân sách:</span>
            <span id="spentProgressText" style="font-weight: 600; color: #fff;">95.0%</span>
          </div>
          <div class="kpi-progress-bar-bg">
            <div class="kpi-progress-bar-fill" id="spentProgressBar" style="width: 95%;"></div>
          </div>
        </div>
      </div>

      <!-- Thẻ KPI 3: GIAO DỊCH VƯỢT NGÂN SÁCH -> Hồng San Hô #F43F5E -->
      <div class="glass-card kpi-card over">
        <div class="kpi-top">
          <div class="kpi-title-group">
            <div class="kpi-icon-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            </div>
            <div>
              <div class="kpi-title">Giao Dịch Vượt Ngân Sách</div>
            </div>
          </div>
          <span class="kpi-badge" id="overRatioBadge">Hồng San Hô (#F43F5E)</span>
        </div>
        <div class="kpi-hero" id="kpiOverCount" data-counter="127" data-suffix=" GD">0 GD</div>
        <div class="kpi-bot">
          <div class="kpi-bot-row">
            <span>Tình trạng cảnh báo:</span>
            <span style="color: var(--brand-coral-light); font-weight: 600;" id="kpiOverStatus">Cảnh báo rủi ro chi phí</span>
          </div>
          <div class="kpi-bot-row">
            <span>Số GD tiết kiệm chuẩn:</span>
            <span style="color: var(--brand-mint-light); font-weight: 600;" id="kpiSafeCount">173 giao dịch</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. CHARTS SECTION (BẮT BUỘC: NGÂN SÁCH #7C3AED & CHI TIÊU #06B6D4) -->
    <section class="charts-grid">
      <!-- Biểu đồ cột ghép: Ngân Sách vs Chi Tiêu -->
      <div class="glass-card chart-panel">
        <div class="chart-header">
          <div class="chart-title-box">
            <h3 id="barChartTitle">So Sánh Ngân Sách vs Chi Tiêu</h3>
            <div class="chart-subtitle" id="barChartSubtitle">Phân bổ trực quan theo từng Quý trong năm 2026</div>
          </div>
          <div class="chart-legend-custom">
            <div class="legend-item">
              <div class="legend-color-dot" style="background: #7C3AED; box-shadow: 0 0 8px rgba(124, 58, 237, 0.6);"></div>
              <span>Ngân Sách Được Duyệt (Tím #7C3AED)</span>
            </div>
            <div class="legend-item">
              <div class="legend-color-dot" style="background: #06B6D4; box-shadow: 0 0 8px rgba(6, 182, 212, 0.6);"></div>
              <span>Chi Tiêu Thực Tế (Xanh Ngọc #06B6D4)</span>
            </div>
          </div>
        </div>
        <div class="chart-body">
          <canvas id="groupedBarChart"></canvas>
        </div>
      </div>

      <!-- Biểu đồ tròn: Tỷ Trọng Phòng Ban (Bảng màu hài hòa theo Brand Guideline) -->
      <div class="glass-card chart-panel">
        <div class="chart-header">
          <div class="chart-title-box">
            <h3 id="pieChartTitle">Cơ Cấu Tỷ Trọng Chi Tiêu Phòng Ban</h3>
            <div class="chart-subtitle">Phân bổ chi tiêu thực tế giữa các khối phòng ban</div>
          </div>
        </div>
        <div class="chart-body">
          <canvas id="deptPieChart"></canvas>
        </div>
      </div>
    </section>

    <!-- 5. BẢNG GIAO DỊCH CHI TIẾT (TRANSACTION MATRIX) -->
    <section class="glass-card table-panel">
      <div class="table-header-bar">
        <div class="table-title-box">
          <h3>Bảng Tra Cứu Giao Dịch Chi Tiết</h3>
          <div class="chart-subtitle">Khoản vượt ngân sách đánh dấu Hồng San Hô (#F43F5E), Tiết kiệm dùng Xanh Bạc Hà (#14B8A6)</div>
        </div>
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="tableSearchInput" placeholder="Tìm theo Mã GD, Hạng mục, Phòng ban...">
        </div>
      </div>

      <div class="table-container">
        <table class="bi-table">
          <thead>
            <tr>
              <th>Mã Giao Dịch</th>
              <th>Quý</th>
              <th>Phòng Ban</th>
              <th>Hạng Mục Chi</th>
              <th style="text-align: right;">Ngân Sách Duyệt</th>
              <th style="text-align: right;">Chi Tiêu Thực Tế</th>
              <th style="text-align: right;">Chênh Lệch</th>
              <th style="text-align: center;">Trạng Thái</th>
            </tr>
          </thead>
          <tbody id="transactionTableBody">
            <!-- Render dynamically -->
          </tbody>
        </table>
      </div>
    </section>

  </div>

  <!-- EMBEDDED FALLBACK DATA -->
  <script id="embeddedRawData" type="application/json">
    RAW_RECORDS_PLACEHOLDER
  </script>

  <!-- JAVASCRIPT CONTROLLER -->
  <script>
    /* ==========================================================================
       1. COUNTER ANIMATION ENGINE (60fps, easeOutExpo)
       ========================================================================== */
    class CounterEngine {
      static easings = {
        easeOutExpo: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t))
      };

      static formatCurrencyVND(value) {
        return Math.round(value).toLocaleString('vi-VN') + ' ₫';
      }

      static formatCount(value, suffix = '') {
        return Math.round(value).toLocaleString('vi-VN') + suffix;
      }

      static animate(element, targetValue, isCurrency = true, suffix = '', duration = 1200) {
        if (!element) return;
        const startValue = element._currentVal || 0;
        const startTime = performance.now();

        if (element._animId) {
          cancelAnimationFrame(element._animId);
        }

        const step = (now) => {
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const eased = CounterEngine.easings.easeOutExpo(progress);
          const current = startValue + (targetValue - startValue) * eased;

          if (isCurrency) {
            element.textContent = CounterEngine.formatCurrencyVND(current);
          } else {
            element.textContent = CounterEngine.formatCount(current, suffix);
          }

          if (progress < 1) {
            element._animId = requestAnimationFrame(step);
          } else {
            element._currentVal = targetValue;
            if (isCurrency) {
              element.textContent = CounterEngine.formatCurrencyVND(targetValue);
            } else {
              element.textContent = CounterEngine.formatCount(targetValue, suffix);
            }
            element._animId = null;
          }
        };

        element._animId = requestAnimationFrame(step);
      }
    }

    /* ==========================================================================
       2. APPLICATION STATE & DATA LAYER
       ========================================================================== */
    const State = {
      rawRecords: [],
      filteredRecords: [],
      activeQuarter: 'all',
      activeDept: 'all',
      searchKeyword: '',
      lastMtime: 0,
      charts: {
        bar: null,
        pie: null
      }
    };

    // Load initial data from embedded JSON
    try {
      const embeddedScript = document.getElementById('embeddedRawData');
      if (embeddedScript && embeddedScript.textContent.trim()) {
        State.rawRecords = JSON.parse(embeddedScript.textContent);
      }
    } catch (e) {
      console.warn("Could not load embedded data:", e);
    }

    /* ==========================================================================
       3. CLIENT-SIDE FILTERING & AGGREGATION LOGIC
       ========================================================================== */
    function computeFilteredData() {
      const q = State.activeQuarter;
      const d = State.activeDept;
      const kw = State.searchKeyword.toLowerCase().trim();

      // Filter raw records
      State.filteredRecords = State.rawRecords.filter(r => {
        const matchQ = (q === 'all') || (r.Quy === q);
        const matchD = (d === 'all') || (r.Phong_Ban === d);
        let matchKw = true;
        if (kw) {
          matchKw = (r.Ma_Giao_Dich && r.Ma_Giao_Dich.toLowerCase().includes(kw)) ||
                    (r.Phong_Ban && r.Phong_Ban.toLowerCase().includes(kw)) ||
                    (r.Hang_Muc_Chi && r.Hang_Muc_Chi.toLowerCase().includes(kw)) ||
                    (r.Trang_Thai && r.Trang_Thai.toLowerCase().includes(kw));
        }
        return matchQ && matchD && matchKw;
      });

      // KPI Aggregations
      const totalBudget = State.filteredRecords.reduce((acc, r) => acc + (r.Ngan_Sach_Duyet || 0), 0);
      const totalSpent = State.filteredRecords.reduce((acc, r) => acc + (r.Chi_Tieu_Thuc_Te || 0), 0);
      const overCount = State.filteredRecords.filter(r => r.Trang_Thai === 'Vuot Ngan Sach').length;
      const safeCount = State.filteredRecords.length - overCount;
      const deltaSaving = totalBudget - totalSpent;
      const spentRatio = totalBudget > 0 ? (totalSpent / totalBudget * 100) : 0;
      const overRatio = State.filteredRecords.length > 0 ? (overCount / State.filteredRecords.length * 100) : 0;

      return {
        totalBudget,
        totalSpent,
        overCount,
        safeCount,
        deltaSaving,
        spentRatio,
        overRatio,
        count: State.filteredRecords.length
      };
    }

    /* ==========================================================================
       4. UI UPDATE & ANIMATION CONTROLLER
       ========================================================================== */
    function updateUI() {
      const metrics = computeFilteredData();

      // 1. Update KPI Hero Numbers with Counter Animation
      const budgetEl = document.getElementById('kpiBudget');
      const spentEl = document.getElementById('kpiSpent');
      const overEl = document.getElementById('kpiOverCount');

      CounterEngine.animate(budgetEl, metrics.totalBudget, true);
      CounterEngine.animate(spentEl, metrics.totalSpent, true);
      CounterEngine.animate(overEl, metrics.overCount, false, ' GD');

      // 2. Update KPI Subtexts & Badges
      const deltaFormatted = (metrics.deltaSaving >= 0 ? '+' : '') + Math.round(metrics.deltaSaving).toLocaleString('vi-VN') + ' ₫';
      document.getElementById('kpiSavingDelta').textContent = deltaFormatted;
      document.getElementById('kpiSavingDelta').style.color = metrics.deltaSaving >= 0 ? 'var(--brand-mint-light)' : 'var(--brand-coral-light)';

      const spentRateStr = metrics.spentRatio.toFixed(1) + '%';
      document.getElementById('spentRateBadge').textContent = 'Giải ngân: ' + spentRateStr;
      document.getElementById('spentProgressText').textContent = spentRateStr;
      document.getElementById('spentProgressBar').style.width = Math.min(metrics.spentRatio, 100) + '%';
      if (metrics.spentRatio > 100) {
        document.getElementById('spentProgressBar').style.background = 'linear-gradient(90deg, #F43F5E, #FB7185)';
      } else {
        document.getElementById('spentProgressBar').style.background = 'linear-gradient(90deg, #06B6D4, #22D3EE)';
      }

      document.getElementById('overRatioBadge').textContent = 'Tỷ lệ: ' + metrics.overRatio.toFixed(1) + '%';
      document.getElementById('kpiSafeCount').textContent = metrics.safeCount + ' giao dịch';
      if (metrics.overCount === 0) {
        document.getElementById('kpiOverStatus').textContent = 'Tuyệt đối an toàn (0 vi phạm)';
        document.getElementById('kpiOverStatus').style.color = 'var(--brand-mint-light)';
      } else {
        document.getElementById('kpiOverStatus').textContent = 'Cảnh báo ' + metrics.overCount + ' khoản vượt NS';
        document.getElementById('kpiOverStatus').style.color = 'var(--brand-coral-light)';
      }

      // 3. Update Filter Summary Text
      const qText = State.activeQuarter === 'all' ? 'Tất cả Quý' : State.activeQuarter;
      const deptNames = {
        'all': 'Tất cả Phòng Ban',
        'Cong Nghe': 'Công Nghệ',
        'Ke Toan': 'Kế Toán',
        'Kinh Doanh': 'Kinh Doanh',
        'Marketing': 'Marketing',
        'Nhan Su': 'Nhân Sự',
        'Van Phong': 'Văn Phòng'
      };
      const dText = deptNames[State.activeDept] || State.activeDept;
      document.getElementById('filterSummaryText').textContent = `${qText} • ${dText}`;
      document.getElementById('matchedTxnCount').textContent = metrics.count;
      document.getElementById('totalTxnCount').textContent = State.rawRecords.length;

      // 4. Update Charts
      updateGroupedBarChart();
      updateDonutChart();

      // 5. Update Table
      renderTable();
    }

    /* ==========================================================================
       5. CHART.JS VISUALIZATION (STRICT BRAND COLOR SCHEME)
       ========================================================================== */
    function initCharts() {
      // 1. Grouped Bar Chart Setup
      // BẮT BUỘC: Ngân Sách Duyệt = Tím Hoàng Gia (#7C3AED)
      // BẮT BUỘC: Chi Tiêu Thực Tế = Xanh Ngọc (#06B6D4)
      const ctxBar = document.getElementById('groupedBarChart').getContext('2d');
      State.charts.bar = new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [
            {
              label: 'Ngân Sách Được Duyệt',
              data: [],
              backgroundColor: 'rgba(124, 58, 237, 0.85)', // Tím Hoàng Gia #7C3AED
              borderColor: '#7C3AED',
              borderWidth: 1.5,
              borderRadius: 6,
              barPercentage: 0.7,
              categoryPercentage: 0.7
            },
            {
              label: 'Chi Tiêu Thực Tế',
              data: [],
              backgroundColor: 'rgba(6, 182, 212, 0.85)',  // Xanh Ngọc #06B6D4
              borderColor: '#06B6D4',
              borderWidth: 1.5,
              borderRadius: 6,
              barPercentage: 0.7,
              categoryPercentage: 0.7
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 500,
            easing: 'easeOutQuart'
          },
          plugins: {
            legend: {
              display: false // Dùng custom HTML legend để hiển thị rõ ràng hơn
            },
            tooltip: {
              backgroundColor: 'rgba(30, 30, 46, 0.96)',
              titleColor: '#f8fafc',
              bodyColor: '#cbd5e1',
              borderColor: 'rgba(255, 255, 255, 0.15)',
              borderWidth: 1,
              padding: 12,
              callbacks: {
                label: function(context) {
                  const val = context.parsed.y || 0;
                  return ` ${context.dataset.label}: ${Math.round(val).toLocaleString('vi-VN')} ₫`;
                },
                afterBody: function(contexts) {
                  if (contexts.length >= 2) {
                    const budget = contexts[0].parsed.y;
                    const spent = contexts[1].parsed.y;
                    const diff = budget - spent;
                    const sign = diff >= 0 ? '+' : '';
                    return ` Chênh lệch: ${sign}${Math.round(diff).toLocaleString('vi-VN')} ₫ (${diff >= 0 ? 'Tiết kiệm' : 'Vượt NS'})`;
                  }
                  return '';
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                color: 'rgba(255, 255, 255, 0.05)'
              },
              ticks: {
                color: '#94a3b8',
                font: { family: 'Outfit', size: 11, weight: 600 }
              }
            },
            y: {
              grid: {
                color: 'rgba(255, 255, 255, 0.05)'
              },
              ticks: {
                color: '#94a3b8',
                font: { family: 'Outfit', size: 10 },
                callback: function(value) {
                  if (value >= 1e9) return (value / 1e9).toFixed(1) + ' tỷ';
                  if (value >= 1e6) return (value / 1e6).toFixed(0) + ' tr';
                  return value;
                }
              }
            }
          }
        }
      });

      // 2. Donut Pie Chart Setup
      // Tuân thủ bảng màu Brand Guideline: Tím Hoàng Gia, Xanh Ngọc, Xanh Bạc Hà, Hồng San Hô
      const ctxPie = document.getElementById('deptPieChart').getContext('2d');
      State.charts.pie = new Chart(ctxPie, {
        type: 'doughnut',
        data: {
          labels: [],
          datasets: [{
            data: [],
            backgroundColor: [
              'rgba(124, 58, 237, 0.88)',  // Tím Hoàng Gia #7C3AED
              'rgba(6, 182, 212, 0.88)',   // Xanh Ngọc #06B6D4
              'rgba(20, 184, 166, 0.88)',  // Xanh Bạc Hà #14B8A6
              'rgba(244, 63, 94, 0.88)',   // Hồng San Hô #F43F5E
              'rgba(167, 139, 250, 0.88)', // Tím nhạt
              'rgba(34, 211, 238, 0.88)'   // Xanh ngọc sáng
            ],
            borderColor: '#1e1e2e',
            borderWidth: 2,
            hoverOffset: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '68%',
          animation: {
            duration: 600,
            easing: 'easeOutQuart'
          },
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: '#cbd5e1',
                padding: 14,
                boxWidth: 12,
                boxHeight: 12,
                borderRadius: 3,
                font: { family: 'Outfit', size: 11, weight: 500 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(30, 30, 46, 0.96)',
              titleColor: '#f8fafc',
              bodyColor: '#cbd5e1',
              borderColor: 'rgba(255, 255, 255, 0.15)',
              borderWidth: 1,
              padding: 12,
              callbacks: {
                label: function(context) {
                  const val = context.parsed || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const pct = total > 0 ? (val / total * 100).toFixed(1) : 0;
                  return ` ${context.label}: ${Math.round(val).toLocaleString('vi-VN')} ₫ (${pct}%)`;
                }
              }
            }
          }
        }
      });
    }

    function updateGroupedBarChart() {
      if (!State.charts.bar) return;

      const records = State.filteredRecords;
      const q = State.activeQuarter;
      const d = State.activeDept;

      let labels = [];
      let budgetData = [];
      let spentData = [];

      if (q === 'all') {
        // Group by Quarters
        document.getElementById('barChartTitle').textContent = 'So Sánh Ngân Sách vs Chi Tiêu Theo Quý';
        document.getElementById('barChartSubtitle').textContent = d === 'all' ? 'Tổng thể 4 quý của tất cả phòng ban' : `Phân tích 4 quý của khối ${d}`;
        const quarters = ['Q1-2026', 'Q2-2026', 'Q3-2026', 'Q4-2026'];
        labels = quarters;

        quarters.forEach(quart => {
          const subset = records.filter(r => r.Quy === quart);
          const b = subset.reduce((acc, r) => acc + (r.Ngan_Sach_Duyet || 0), 0);
          const s = subset.reduce((acc, r) => acc + (r.Chi_Tieu_Thuc_Te || 0), 0);
          budgetData.push(b);
          spentData.push(s);
        });
      } else if (d === 'all') {
        // Group by Departments in this Quarter
        document.getElementById('barChartTitle').textContent = `So Sánh Ngân Sách vs Chi Tiêu Theo Phòng Ban (${q})`;
        document.getElementById('barChartSubtitle').textContent = `Chi tiết chi tiêu của 6 khối phòng ban trong chu kỳ ${q}`;
        const depts = ['Cong Nghe', 'Ke Toan', 'Kinh Doanh', 'Marketing', 'Nhan Su', 'Van Phong'];
        const deptLabels = ['Công Nghệ', 'Kế Toán', 'Kinh Doanh', 'Marketing', 'Nhân Sự', 'Văn Phòng'];
        labels = deptLabels;

        depts.forEach(deptKey => {
          const subset = records.filter(r => r.Phong_Ban === deptKey);
          const b = subset.reduce((acc, r) => acc + (r.Ngan_Sach_Duyet || 0), 0);
          const s = subset.reduce((acc, r) => acc + (r.Chi_Tieu_Thuc_Te || 0), 0);
          budgetData.push(b);
          spentData.push(s);
        });
      } else {
        // Group by Expense Categories (Hang_Muc_Chi) for this Quarter & Department
        document.getElementById('barChartTitle').textContent = `So Sánh Ngân Sách vs Chi Tiêu Theo Hạng Mục (${q} • ${d})`;
        document.getElementById('barChartSubtitle').textContent = `Chi tiết từng khoản chi của phòng ${d} trong ${q}`;
        const categories = [...new Set(records.map(r => r.Hang_Muc_Chi))].sort();
        labels = categories;

        categories.forEach(cat => {
          const subset = records.filter(r => r.Hang_Muc_Chi === cat);
          const b = subset.reduce((acc, r) => acc + (r.Ngan_Sach_Duyet || 0), 0);
          const s = subset.reduce((acc, r) => acc + (r.Chi_Tieu_Thuc_Te || 0), 0);
          budgetData.push(b);
          spentData.push(s);
        });
      }

      State.charts.bar.data.labels = labels;
      State.charts.bar.data.datasets[0].data = budgetData;
      State.charts.bar.data.datasets[1].data = spentData;
      State.charts.bar.update();
    }

    function updateDonutChart() {
      if (!State.charts.pie) return;

      const records = State.filteredRecords;
      const d = State.activeDept;

      let labels = [];
      let data = [];

      if (d === 'all') {
        // Breakdown by 6 Departments
        document.getElementById('pieChartTitle').textContent = 'Cơ Cấu Tỷ Trọng Chi Tiêu Phòng Ban';
        const depts = [
          { key: 'Cong Nghe', name: 'Công Nghệ' },
          { key: 'Ke Toan', name: 'Kế Toán' },
          { key: 'Kinh Doanh', name: 'Kinh Doanh' },
          { key: 'Marketing', name: 'Marketing' },
          { key: 'Nhan Su', name: 'Nhân Sự' },
          { key: 'Van Phong', name: 'Văn Phòng' }
        ];

        depts.forEach(item => {
          const subset = records.filter(r => r.Phong_Ban === item.key);
          const sumSpent = subset.reduce((acc, r) => acc + (r.Chi_Tieu_Thuc_Te || 0), 0);
          if (sumSpent > 0) {
            labels.push(item.name);
            data.push(sumSpent);
          }
        });
      } else {
        // When a single department is selected: Breakdown by Hang_Muc_Chi
        document.getElementById('pieChartTitle').textContent = `Tỷ Trọng Hạng Mục Chi (${d})`;
        const categories = [...new Set(records.map(r => r.Hang_Muc_Chi))].sort();
        categories.forEach(cat => {
          const subset = records.filter(r => r.Hang_Muc_Chi === cat);
          const sumSpent = subset.reduce((acc, r) => acc + (r.Chi_Tieu_Thuc_Te || 0), 0);
          if (sumSpent > 0) {
            labels.push(cat);
            data.push(sumSpent);
          }
        });
      }

      State.charts.pie.data.labels = labels;
      State.charts.pie.data.datasets[0].data = data;
      State.charts.pie.update();
    }

    /* ==========================================================================
       6. TABLE RENDERING (VƯỢT NS: HỒNG SAN HÔ #F43F5E - TIẾT KIỆM: XANH BẠC HÀ #14B8A6)
       ========================================================================== */
    function renderTable() {
      const tbody = document.getElementById('transactionTableBody');
      const records = State.filteredRecords;

      if (!records || records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 32px; color: var(--text-muted);">Không tìm thấy giao dịch nào phù hợp với bộ lọc hiện tại.</td></tr>`;
        return;
      }

      // Display up to 50 rows for fast DOM response
      const displayRows = records.slice(0, 50);
      const rowsHtml = displayRows.map(r => {
        const isVuot = r.Trang_Thai === 'Vuot Ngan Sach';
        const badgeClass = isVuot ? 'badge-status badge-vuot' : 'badge-status badge-tietkiem';
        const badgeText = isVuot ? '● Vượt Ngân Sách' : '✓ Tiết Kiệm';
        const diffVal = r.Chenh_Lech || (r.Ngan_Sach_Duyet - r.Chi_Tieu_Thuc_Te);
        const diffColor = diffVal >= 0 ? 'var(--brand-mint-light)' : 'var(--brand-coral-light)';
        const diffSign = diffVal > 0 ? '+' : '';

        return `
          <tr>
            <td style="font-family: var(--font-mono); font-weight: 600; color: #fff;">${r.Ma_Giao_Dich || '-'}</td>
            <td><span style="background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 6px; font-size: 0.75rem;">${r.Quy || '-'}</span></td>
            <td style="font-weight: 600;">${r.Phong_Ban || '-'}</td>
            <td>${r.Hang_Muc_Chi || '-'}</td>
            <td style="text-align: right; color: var(--brand-purple-light); font-weight: 600;">${Math.round(r.Ngan_Sach_Duyet || 0).toLocaleString('vi-VN')} ₫</td>
            <td style="text-align: right; color: var(--brand-cyan-light); font-weight: 600;">${Math.round(r.Chi_Tieu_Thuc_Te || 0).toLocaleString('vi-VN')} ₫</td>
            <td style="text-align: right; color: ${diffColor}; font-weight: 600;">${diffSign}${Math.round(diffVal).toLocaleString('vi-VN')} ₫</td>
            <td style="text-align: center;"><span class="${badgeClass}">${badgeText}</span></td>
          </tr>
        `;
      }).join('');

      tbody.innerHTML = rowsHtml;
    }

    /* ==========================================================================
       7. EVENT LISTENERS (INTERACTIVE FILTER BUTTONS)
       ========================================================================== */
    function setupFilterListeners() {
      // Quarter filter buttons
      const quarterBtns = document.querySelectorAll('#quarterFilterGroup .filter-btn');
      quarterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          quarterBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          State.activeQuarter = btn.getAttribute('data-value');
          updateUI(); // Instant update
        });
      });

      // Department filter buttons
      const deptBtns = document.querySelectorAll('#deptFilterGroup .filter-btn');
      deptBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          deptBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          State.activeDept = btn.getAttribute('data-value');
          updateUI(); // Instant update
        });
      });

      // Live search input in table
      const searchInput = document.getElementById('tableSearchInput');
      searchInput.addEventListener('input', (e) => {
        State.searchKeyword = e.target.value;
        updateUI();
      });
    }

    /* ==========================================================================
       8. REALTIME POLLING ENGINE (2 SECONDS INTERVAL)
       ========================================================================== */
    function startPollingEngine() {
      const livePill = document.getElementById('liveSyncPill');
      const liveDot = document.getElementById('liveDot');
      const liveText = document.getElementById('liveStatusText');

      async function poll() {
        try {
          const res = await fetch('/api/raw_data', { cache: 'no-store' });
          if (!res.ok) throw new Error('API response not ok');
          const data = await res.json();

          if (data && data.records && Array.isArray(data.records)) {
            // Flash live pulse
            liveDot.style.boxShadow = '0 0 16px var(--brand-mint)';
            liveText.textContent = `Live Sync (${data.records.length} GD)`;
            setTimeout(() => {
              liveDot.style.boxShadow = '0 0 10px var(--brand-mint)';
            }, 600);

            // Check if file modification or record count changed
            const isFirst = (State.lastMtime === 0);
            if (isFirst || data.mtime !== State.lastMtime || data.records.length !== State.rawRecords.length) {
              console.log("[POLLING] Cập nhật dữ liệu mới từ Server:", data.timestamp);
              State.lastMtime = data.mtime;
              State.rawRecords = data.records;
              updateUI(); // Reactive auto-refresh
            }
          }
        } catch (err) {
          // If offline or opening file directly, keep functioning with fallback
          liveText.textContent = 'Chế độ Cục bộ (Offline)';
          liveDot.style.backgroundColor = 'var(--brand-purple)';
          liveDot.style.boxShadow = '0 0 8px var(--brand-purple)';
        }
      }

      // Initial poll
      poll();
      // Recurring poll every 2000ms (2s)
      setInterval(poll, 2000);
    }

    /* ==========================================================================
       9. INITIALIZATION BOOTSTRAP
       ========================================================================== */
    document.addEventListener('DOMContentLoaded', () => {
      initCharts();
      setupFilterListeners();
      updateUI();
      startPollingEngine();
    });
  </script>
</body>
</html>
"""

# Replace placeholder with actual JSON string
final_html = html_template.replace("RAW_RECORDS_PLACEHOLDER", raw_records_json_str)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Đã tạo thành công Dashboard tuân thủ Brand Guideline tại:", OUTPUT_PATH)
print("Dung lượng file:", f"{os.path.getsize(OUTPUT_PATH):,} bytes")
