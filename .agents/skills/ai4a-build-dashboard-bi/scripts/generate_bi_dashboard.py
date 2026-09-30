#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI4A BI Dashboard Generator
CLI utility to compile structured business data into modern Glassmorphism & Dark Mode HTML Dashboards.
Supports zero-dependency standalone HTML generation with inlined CSS & JS.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output in Windows environments
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

SKILL_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = SKILL_DIR / "resources"

DEMO_DATA = {
    "dashboard_title": "AI4A Executive Business Intelligence",
    "subtitle": "Báo cáo hiệu suất kinh doanh đa kênh & Tài chính thời gian thực",
    "kpis": [
        {
            "id": "revenue",
            "title": "Tổng Doanh Thu",
            "icon": "💰",
            "icon_theme": "cyan",
            "value": 3852000000,
            "prefix": "",
            "suffix": " ₫",
            "separator": ".",
            "decimals": 0,
            "duration": 1800,
            "delta": "+18.4%",
            "delta_type": "positive",
            "benchmark": "Mục tiêu: 3.5 Tỷ",
            "status_text": "Đạt 110%",
            "status_type": "success"
        },
        {
            "id": "profit",
            "title": "Lợi Nhuận Gộp",
            "icon": "📈",
            "icon_theme": "emerald",
            "value": 1425600000,
            "prefix": "",
            "suffix": " ₫",
            "separator": ".",
            "decimals": 0,
            "duration": 1800,
            "delta": "+12.6%",
            "delta_type": "positive",
            "benchmark": "Biên LN: 37.0%",
            "status_text": "Ổn định",
            "status_type": "success"
        },
        {
            "id": "customers",
            "title": "Khách Hàng Hoạt Động",
            "icon": "👥",
            "icon_theme": "violet",
            "value": 14850,
            "prefix": "",
            "suffix": "",
            "separator": ",",
            "decimals": 0,
            "duration": 1600,
            "delta": "+8.2%",
            "delta_type": "positive",
            "benchmark": "KH Mới: 1,820",
            "status_text": "Tăng trưởng",
            "status_type": "success"
        },
        {
            "id": "conversion",
            "title": "Tỷ Lệ Chuyển Đổi",
            "icon": "⚡",
            "icon_theme": "amber",
            "value": 4.85,
            "prefix": "",
            "suffix": "%",
            "separator": ".",
            "decimals": 2,
            "duration": 1500,
            "delta": "+2.4%",
            "delta_type": "positive",
            "benchmark": "Benchmark: 3.8%",
            "status_text": "Vượt kỳ vọng",
            "status_type": "success"
        }
    ],
    "trend_chart": {
        "labels": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"],
        "revenue_data": [210, 245, 280, 260, 310, 340, 320, 365, 390, 420, 450, 485],
        "profit_data": [75, 88, 105, 95, 115, 130, 120, 140, 155, 170, 180, 195]
    },
    "channel_chart": {
        "labels": ["Thương Mại Điện Tử", "Đại Lý Phân Phối", "Bán Lẻ Trực Tiếp", "Đối Tác B2B"],
        "data": [42, 28, 18, 12]
    },
    "products_table": [
        {"code": "CAT-01", "name": "Thiết Bị Điện Tử & Phụ Kiện", "orders": "4,250 đơn", "revenue": "1,420,000,000 ₫", "margin": "42.5%", "growth": "+19.2%", "status": "Bán chạy", "status_class": "success"},
        {"code": "CAT-02", "name": "Thời Trang Công Sở & Thể Thao", "orders": "3,120 đơn", "revenue": "890,000,000 ₫", "margin": "38.0%", "growth": "+14.5%", "status": "Tăng trưởng", "status_class": "success"},
        {"code": "CAT-03", "name": "Gia Dụng & Đời Sống", "orders": "2,450 đơn", "revenue": "650,000,000 ₫", "margin": "31.2%", "growth": "+6.8%", "status": "Ổn định", "status_class": "success"},
        {"code": "CAT-04", "name": "Mỹ Phẩm & Sức Khỏe", "orders": "1,840 đơn", "revenue": "542,000,000 ₫", "margin": "45.0%", "growth": "-2.1%", "status": "Cần tối ưu", "status_class": "warning"},
        {"code": "CAT-05", "name": "Văn Phòng Phẩm & Sách", "orders": "1,190 đơn", "revenue": "350,000,000 ₫", "margin": "28.4%", "growth": "+4.1%", "status": "Bình thường", "status_class": "success"}
    ]
}


def load_file_content(path: Path) -> str:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def build_kpi_cards_html(kpis):
    html_cards = []
    for kpi in kpis:
        delta_class = "delta-" + str(kpi.get('delta_type', 'positive'))
        status_class = "status-pill-" + str(kpi.get('status_type', 'success'))
        icon_theme = "kpi-icon-" + str(kpi.get('icon_theme', 'cyan'))
        
        card = f"""
      <article class="glass-panel kpi-card">
        <div class="kpi-top-row">
          <div class="kpi-label-group">
            <div class="kpi-icon-wrapper {icon_theme}">{kpi.get('icon', '📊')}</div>
            <span class="kpi-title">{kpi.get('title')}</span>
          </div>
          <span class="kpi-delta-badge {delta_class}">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
            {kpi.get('delta', '0%')}
          </span>
        </div>
        <div class="kpi-value-row">
          <div class="kpi-hero-number"
               data-counter="{kpi.get('value', 0)}"
               data-counter-prefix="{kpi.get('prefix', '')}"
               data-counter-suffix="{kpi.get('suffix', '')}"
               data-counter-separator="{kpi.get('separator', ',')}"
               data-counter-decimals="{kpi.get('decimals', 0)}"
               data-counter-duration="{kpi.get('duration', 1600)}">
            0
          </div>
        </div>
        <div class="kpi-footer-row">
          <span class="kpi-benchmark">{kpi.get('benchmark', '')}</span>
          <span class="status-pill {status_class}">{kpi.get('status_text', 'Active')}</span>
        </div>
      </article>"""
        html_cards.append(card)
    return "\n".join(html_cards)


def build_table_rows_html(rows):
    html_rows = []
    for r in rows:
        growth_str = str(r.get("growth", "0%"))
        if growth_str.startswith("-"):
            delta_badge = f'<span class="kpi-delta-badge delta-negative">{growth_str}</span>'
        else:
            delta_badge = f'<span class="kpi-delta-badge delta-positive">{growth_str}</span>'
        
        status_pill = f'<span class="status-pill status-pill-{r.get("status_class", "success")}">{r.get("status", "Active")}</span>'
        
        row_str = f"""
            <tr>
              <td><strong>{r.get('code', '')}</strong></td>
              <td>{r.get('name', '')}</td>
              <td>{r.get('orders', '')}</td>
              <td>{r.get('revenue', '')}</td>
              <td>{r.get('margin', '')}</td>
              <td>{delta_badge}</td>
              <td>{status_pill}</td>
            </tr>"""
        html_rows.append(row_str)
    return "\n".join(html_rows)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ — Modern Glassmorphism BI</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
__CSS_CONTENT__
  </style>
</head>
<body>
  <div class="ambient-glow-wrapper" aria-hidden="true">
    <div class="ambient-orb ambient-orb-1"></div>
    <div class="ambient-orb ambient-orb-2"></div>
    <div class="ambient-orb ambient-orb-3"></div>
  </div>

  <main class="bi-dashboard-container">
    
    <header class="glass-panel bi-header">
      <div class="bi-header-left">
        <div class="bi-brand-icon" aria-hidden="true">📊</div>
        <div class="bi-title-group">
          <h1>
            <span>__TITLE__</span>
            <span class="bi-live-badge">Live Sync</span>
          </h1>
          <p class="bi-subtitle">__SUBTITLE__</p>
        </div>
      </div>

      <div class="bi-header-right">
        <nav class="filter-tabs" aria-label="Bộ lọc thời gian">
          <button class="filter-tab-btn" data-range="today">Hôm nay</button>
          <button class="filter-tab-btn" data-range="7d">7 Ngày</button>
          <button class="filter-tab-btn active" data-range="30d">30 Ngày</button>
          <button class="filter-tab-btn" data-range="quarter">Quý này</button>
          <button class="filter-tab-btn" data-range="year">Năm 2026</button>
        </nav>

        <button class="btn-glass" id="btnRefresh" title="Làm mới hiệu ứng số nhảy">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/></svg>
          <span>Refresh</span>
        </button>

        <button class="btn-glass btn-glass-primary" onclick="window.print()">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <span>In Báo Cáo</span>
        </button>
      </div>
    </header>

    <section class="bi-kpi-grid" aria-label="Chỉ số hiệu suất then chốt (KPI)">
__KPIS_HTML__
    </section>

    <section class="bi-charts-grid-primary">
      <article class="glass-panel chart-panel">
        <div class="chart-header">
          <div class="chart-title-group">
            <h2>Biểu Đồ Xu Hướng Doanh Thu & Lợi Nhuận</h2>
            <p class="chart-subtitle">Phân tích chu kỳ 12 tháng qua</p>
          </div>
          <div class="kpi-label-group">
            <span class="kpi-delta-badge delta-positive">Tăng trưởng ổn định</span>
          </div>
        </div>
        <div class="chart-container-wrapper">
          <canvas id="revenueTrendChart"></canvas>
        </div>
      </article>

      <article class="glass-panel chart-panel">
        <div class="chart-header">
          <div class="chart-title-group">
            <h2>Cơ Cấu Kênh Bán Hàng</h2>
            <p class="chart-subtitle">Tỷ trọng đóng góp doanh thu</p>
          </div>
        </div>
        <div class="chart-container-wrapper">
          <canvas id="channelDonutChart"></canvas>
        </div>
      </article>
    </section>

    <section class="glass-panel bi-table-panel">
      <div class="table-header-group">
        <div>
          <h2>Bảng Phân Tích Danh Mục Sản Phẩm Chủ Lực</h2>
          <p class="chart-subtitle">Cập nhật tự động lúc __TIMESTAMP__</p>
        </div>
        <input type="text" class="table-search-input" id="tableSearch" placeholder="Tìm kiếm nhanh danh mục...">
      </div>

      <div class="bi-responsive-table">
        <table class="bi-table">
          <thead>
            <tr>
              <th>Mã Nhóm</th>
              <th>Tên Danh Mục Hàng Hóa</th>
              <th>Số Đơn Hàng</th>
              <th>Doanh Thu Thuần</th>
              <th>Biên Lợi Nhuận</th>
              <th>Tăng Trưởng</th>
              <th>Trạng Thái</th>
            </tr>
          </thead>
          <tbody>
__TABLE_ROWS_HTML__
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <script>
__JS_COUNTER_CONTENT__
  </script>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      Chart.defaults.color = '#94a3b8';
      Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
      Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.92)';
      Chart.defaults.plugins.tooltip.borderColor = 'rgba(255, 255, 255, 0.15)';
      Chart.defaults.plugins.tooltip.borderWidth = 1;
      Chart.defaults.plugins.tooltip.padding = 12;
      Chart.defaults.plugins.tooltip.cornerRadius = 8;
      Chart.defaults.plugins.legend.labels.usePointStyle = true;

      const ctxTrend = document.getElementById('revenueTrendChart').getContext('2d');
      const gradientCyan = ctxTrend.createLinearGradient(0, 0, 0, 300);
      gradientCyan.addColorStop(0, 'rgba(6, 182, 212, 0.45)');
      gradientCyan.addColorStop(1, 'rgba(6, 182, 212, 0.00)');

      const gradientViolet = ctxTrend.createLinearGradient(0, 0, 0, 300);
      gradientViolet.addColorStop(0, 'rgba(139, 92, 246, 0.35)');
      gradientViolet.addColorStop(1, 'rgba(139, 92, 246, 0.00)');

      new Chart(ctxTrend, {
        type: 'line',
        data: {
          labels: __TREND_LABELS__,
          datasets: [
            {
              label: 'Doanh Thu (Triệu VNĐ)',
              data: __TREND_REV__,
              borderColor: '#06b6d4',
              backgroundColor: gradientCyan,
              borderWidth: 3,
              fill: true,
              tension: 0.38,
              pointBackgroundColor: '#22d3ee',
              pointBorderColor: '#070a12',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
            },
            {
              label: 'Lợi Nhuận (Triệu VNĐ)',
              data: __TREND_PROF__,
              borderColor: '#8b5cf6',
              backgroundColor: gradientViolet,
              borderWidth: 2.5,
              fill: true,
              tension: 0.38,
              pointBackgroundColor: '#a78bfa',
              pointBorderColor: '#070a12',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          scales: {
            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', callback: (v) => v + 'M' } }
          },
          plugins: { legend: { position: 'top', align: 'end' } }
        }
      });

      const ctxDonut = document.getElementById('channelDonutChart').getContext('2d');
      new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
          labels: __CHANNEL_LABELS__,
          datasets: [{
            data: __CHANNEL_DATA__,
            backgroundColor: ['#06b6d4', '#8b5cf6', '#10b981', '#f59e0b'],
            borderWidth: 0,
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '72%',
          plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 14 } } }
        }
      });

      const filterBtns = document.querySelectorAll('.filter-tab-btn');
      filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          filterBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          CounterEngine.animateAll();
        });
      });

      document.getElementById('btnRefresh')?.addEventListener('click', () => {
        CounterEngine.animateAll();
      });

      const searchInput = document.getElementById('tableSearch');
      if (searchInput) {
        searchInput.addEventListener('input', (e) => {
          const val = e.target.value.toLowerCase();
          const rows = document.querySelectorAll('.bi-table tbody tr');
          rows.forEach(r => {
            r.style.display = r.textContent.toLowerCase().includes(val) ? '' : 'none';
          });
        });
      }
    });
  </script>
</body>
</html>"""


def generate_dashboard_html(data: dict, inline: bool = True) -> str:
    css_content = load_file_content(RESOURCES_DIR / "bi-design-system.css")
    js_counter_content = load_file_content(RESOURCES_DIR / "bi-counter-engine.js")

    title = data.get("dashboard_title", "AI4A Business Intelligence Dashboard")
    subtitle = data.get("subtitle", "Báo cáo phân tích chuyên sâu")
    kpis_html = build_kpi_cards_html(data.get("kpis", []))
    table_rows_html = build_table_rows_html(data.get("products_table", []))

    trend_labels = json.dumps(data.get("trend_chart", {}).get("labels", []))
    trend_rev = json.dumps(data.get("trend_chart", {}).get("revenue_data", []))
    trend_prof = json.dumps(data.get("trend_chart", {}).get("profit_data", []))

    channel_labels = json.dumps(data.get("channel_chart", {}).get("labels", []))
    channel_data = json.dumps(data.get("channel_chart", {}).get("data", []))

    now_str = datetime.now().strftime('%H:%M • %d/%m/%Y')

    rendered = HTML_TEMPLATE
    rendered = rendered.replace("__TITLE__", title)
    rendered = rendered.replace("__SUBTITLE__", subtitle)
    rendered = rendered.replace("__CSS_CONTENT__", css_content)
    rendered = rendered.replace("__JS_COUNTER_CONTENT__", js_counter_content)
    rendered = rendered.replace("__KPIS_HTML__", kpis_html)
    rendered = rendered.replace("__TABLE_ROWS_HTML__", table_rows_html)
    rendered = rendered.replace("__TIMESTAMP__", now_str)
    rendered = rendered.replace("__TREND_LABELS__", trend_labels)
    rendered = rendered.replace("__TREND_REV__", trend_rev)
    rendered = rendered.replace("__TREND_PROF__", trend_prof)
    rendered = rendered.replace("__CHANNEL_LABELS__", channel_labels)
    rendered = rendered.replace("__CHANNEL_DATA__", channel_data)

    return rendered


def main():
    parser = argparse.ArgumentParser(description="AI4A BI Dashboard Generator")
    parser.add_argument("--demo", action="store_true", help="Generate demo executive dashboard")
    parser.add_argument("--input", type=str, help="Path to input JSON data file")
    parser.add_argument("--output", type=str, help="Path to output HTML file")
    parser.add_argument("--title", type=str, help="Custom Dashboard Title")
    args = parser.parse_args()

    data = DEMO_DATA
    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)

    if args.title:
        data["dashboard_title"] = args.title

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = args.output
    if not output_path:
        reports_dir = Path("outputs/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        output_path = reports_dir / f"bi_dashboard_{timestamp}.html"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    html_result = generate_dashboard_html(data, inline=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_result)

    print(f"✨ Dashboard generated successfully!")
    print(f"📍 Output file: {output_path.resolve()}")


if __name__ == "__main__":
    main()
