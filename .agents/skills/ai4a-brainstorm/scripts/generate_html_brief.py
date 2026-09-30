#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_html_brief.py — AI4A Brainstorm Interactive HTML Brief Generator
Tác giả: MT Đức Thuận & Antigravity Agent
Mô tả: Tự động hóa tạo báo cáo trực quan single-file HTML từ dữ liệu Brainstorm Contract.
Không phụ thuộc thư viện ngoài (Zero external dependencies).
"""

import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT_DEMO_DATA = {
    "project_name": "Tự động hóa Phân tích & Xếp hạng Quán Cafe Quận 1 cho Remote Workers",
    "date": "2026-09-09",
    "author": "Học viên AI4A (Minh Hoàng)",
    "mentor": "MT Đức Thuận",
    "version": "1.1.0",
    "contract": {
        "outcome": {
            "title": "Outcome (Kết quả đầu ra)",
            "desc": "File Excel chuẩn hóa (22 quán cafe) có Dashboard KPI, phân loại theo 3 phân khúc giá và mức độ phù hợp làm việc, kèm báo cáo insights kinh doanh.",
            "artifact": "outputs/reports/Quan_Cafe_Quan_1_Cleaned.xlsx"
        },
        "constraints": {
            "title": "Constraints (Ràng buộc & Ranh giới)",
            "desc": "Chỉ khảo sát địa bàn Quận 1 (TP.HCM); không lưu trữ thông tin cá nhân khách hàng; giá tiền phải được tách thành số nguyên VNĐ; điểm Google Rating chỉ lấy từ 4.0★ trở lên.",
            "rule": "Bảo mật thông tin, schema chuẩn 16 trường"
        },
        "non_goals": {
            "title": "Non-goals (Những thứ KHÔNG làm)",
            "desc": "Không xây dựng ứng dụng đặt bàn trực tuyến; không crawl bình luận thời gian thực; không mở rộng ra các quận lân cận (Quận 3, Bình Thạnh) trong chu kỳ này.",
            "boundary": "Chỉ tập trung vào dữ liệu tĩnh và phân tích tĩnh"
        },
        "acceptance_criteria": {
            "title": "Acceptance Criteria (Tiêu chí nghiệm thu)",
            "desc": "Tối thiểu 15-20 quán (thực tế 22 quán); 0 bản ghi trùng lặp; 100% cột giá tính toán được; dashboard tự động hiển thị đúng không bị lỗi 0 trên mọi bản Excel.",
            "metric": "100% pass kiểm thử dữ liệu và hiển thị"
        }
    },
    "approaches": [
        {
            "id": "app_1",
            "name": "Approach 1: Lean / Direct",
            "badge": "Khuyên dùng (Recommended)",
            "badge_type": "recommended",
            "concept": "Script Python thuần (openpyxl) kết hợp tiền xử lý dữ liệu và tạo trực tiếp workbook Excel đa sheet.",
            "pros": ["Triển khai cực nhanh trong 1-2 giờ", "Hoàn toàn kiểm soát mã nguồn, không tốn phí API", "Dễ debug và bảo trì trực tiếp trên máy"],
            "cons": ["Không tự động lấy dữ liệu thời gian thực nếu dữ liệu mạng thay đổi"],
            "key_assumption": "Dữ liệu mẫu 22 quán đã được thu thập và thẩm định cấu trúc trước khi sinh file.",
            "first_failure_point": "Nếu cấu trúc nguồn thay đổi đột ngột hoặc schema bị thiếu trường bắt buộc."
        },
        {
            "id": "app_2",
            "name": "Approach 2: Workflow / Agentic",
            "badge": "Khả thi cao",
            "badge_type": "viable",
            "concept": "Pipeline tác tử 2 tầng: Agent 1 làm sạch & xác thực schema -> Agent 2 phân tích kinh doanh và tạo dashboard.",
            "pros": ["Có thể xử lý thêm nhiều nguồn dữ liệu mới", "Có trạm kiểm soát (Human Checkpoint) trước khi xuất file"],
            "cons": ["Phức tạp hơn, cần kiểm soát token và context handoff giữa các agents"],
            "key_assumption": "Khuôn mẫu dữ liệu trung gian giữa 2 Agent được giữ nhất quán tuyệt đối.",
            "first_failure_point": "Agent 1 xuất sai định dạng schema khiến Agent 2 không thể sinh công thức Excel."
        },
        {
            "id": "app_3",
            "name": "Approach 3: Scalable / Tool-Augmented",
            "badge": "Quá tải (Overkill)",
            "badge_type": "overkill",
            "concept": "Xây dựng microservice crawl tự động từ Google Places API, lưu vào PostgreSQL và vẽ dashboard qua Web App.",
            "pros": ["Khả năng mở rộng toàn quốc cho hàng nghìn quán", "Cập nhật dữ liệu real-time"],
            "cons": ["Thời gian dựng 1-2 tuần, tốn chi phí API key và hạ tầng hosting", "Vi phạm nguyên tắc YAGNI/Lean cho quy mô bài tập"],
            "key_assumption": "Cần nguồn ngân sách duy trì API và có đội ngũ vận hành hạ tầng backend.",
            "first_failure_point": "Hết hạn mức chi phí Google API hoặc tài khoản thẻ ngân hàng bị chặn."
        }
    ],
    "recommendation": {
        "chosen": "Approach 1 (Lean / Direct)",
        "rationale": "Với tập dữ liệu 22 quán cafe Quận 1, kịch bản Python đơn lẻ kết hợp tính toán sẵn các giá trị số thực (pre-calculated values) là phương án tối ưu nhất: vừa loại bỏ triệt để lỗi hiển thị số 0 trên Excel, vừa không phụ thuộc chi phí bên thứ 3.",
        "next_step": "Cập nhật kết quả vào docs/project-brief.md và ghi log kiểm nghiệm vào docs/pdca-log.md."
    },
    "workflow_nodes": [
        {"step": "1. Input", "name": "Dữ liệu thô", "detail": "Thu thập 22 quán cafe tại Q1", "icon": "📥"},
        {"step": "2. Cleanse", "name": "Làm sạch số học", "detail": "Tách min/max/avg VNĐ, khử trùng lặp", "icon": "🧹"},
        {"step": "3. Checkpoint", "name": "Human Review", "detail": "Duyệt schema & phân khúc giá", "icon": "👁️"},
        {"step": "4. Generate", "name": "Engine Excel", "detail": "openpyxl sinh Dashboard & Data", "icon": "⚙️"},
        {"step": "5. Output", "name": "Báo cáo Hoàn Chỉnh", "detail": "Excel + Report + PDCA Log", "icon": "📊"}
    ]
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brainstorm Decision Brief — {project_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(51, 65, 85, 0.8);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent-primary: #38bdf8;
      --accent-success: #34d399;
      --accent-warning: #fbbf24;
      --accent-danger: #f87171;
      --accent-purple: #a78bfa;
      --gradient-blue: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
      --gradient-card: linear-gradient(180deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 40px 20px;
      min-height: 100vh;
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.1) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(167, 139, 250, 0.1) 0%, transparent 40%);
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}

    /* Header */
    header {{
      text-align: center;
      margin-bottom: 48px;
      padding-bottom: 32px;
      border-bottom: 1px solid var(--card-border);
    }}

    .badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 9999px;
      color: var(--accent-primary);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.5px;
      margin-bottom: 16px;
      text-transform: uppercase;
    }}

    h1 {{
      font-size: 2.25rem;
      font-weight: 800;
      line-height: 1.25;
      margin-bottom: 16px;
      background: linear-gradient(to right, #f8fafc, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .meta-bar {{
      display: flex;
      justify-content: center;
      gap: 24px;
      flex-wrap: wrap;
      color: var(--text-muted);
      font-size: 14px;
    }}

    .meta-bar strong {{
      color: var(--text);
    }}

    /* Section Headings */
    .section-title {{
      font-size: 1.4rem;
      font-weight: 700;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--text);
    }}

    .section-title span {{
      color: var(--accent-primary);
    }}

    /* The 4-Field Contract Grid */
    .contract-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
      margin-bottom: 56px;
    }}

    .contract-card {{
      background: var(--gradient-card);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(12px);
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }}

    .contract-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(56, 189, 248, 0.4);
      box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.5);
    }}

    .contract-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
    }}

    .card-outcome::before {{ background: var(--accent-primary); }}
    .card-constraints::before {{ background: var(--accent-warning); }}
    .card-nongoals::before {{ background: var(--accent-danger); }}
    .card-acceptance::before {{ background: var(--accent-success); }}

    .card-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .card-icon {{
      width: 36px;
      height: 36px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }}

    .card-outcome .card-icon {{ background: rgba(56, 189, 248, 0.15); }}
    .card-constraints .card-icon {{ background: rgba(251, 191, 36, 0.15); }}
    .card-nongoals .card-icon {{ background: rgba(248, 113, 113, 0.15); }}
    .card-acceptance .card-icon {{ background: rgba(52, 211, 153, 0.15); }}

    .card-title {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--text);
    }}

    .card-body {{
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 16px;
      min-height: 72px;
    }}

    .card-tag {{
      display: inline-block;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      word-break: break-all;
    }}

    /* Workflow Pipeline (Flowchart) */
    .pipeline-container {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 32px 24px;
      margin-bottom: 56px;
      backdrop-filter: blur(8px);
    }}

    .pipeline-steps {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .step-item {{
      flex: 1;
      min-width: 170px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      text-align: center;
      transition: all 0.2s;
    }}

    .step-item:hover {{
      border-color: var(--accent-primary);
      transform: translateY(-2px);
    }}

    .step-icon {{
      font-size: 24px;
      margin-bottom: 8px;
    }}

    .step-badge {{
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--accent-primary);
      margin-bottom: 4px;
    }}

    .step-name {{
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 6px;
    }}

    .step-detail {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .step-arrow {{
      color: var(--text-muted);
      font-size: 18px;
      font-weight: bold;
    }}

    /* Approaches Comparison Matrix */
    .approaches-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
      margin-bottom: 56px;
    }}

    .approach-card {{
      background: var(--gradient-card);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }}

    .approach-card.is-recommended {{
      border-color: rgba(56, 189, 248, 0.6);
      box-shadow: 0 0 24px -6px rgba(56, 189, 248, 0.25);
    }}

    .approach-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
    }}

    .approach-name {{
      font-size: 1.15rem;
      font-weight: 700;
    }}

    .tag-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
    }}

    .badge-recommended {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-primary);
      border: 1px solid rgba(56, 189, 248, 0.4);
    }}

    .badge-viable {{
      background: rgba(52, 211, 153, 0.15);
      color: var(--accent-success);
      border: 1px solid rgba(52, 211, 153, 0.4);
    }}

    .badge-overkill {{
      background: rgba(248, 113, 113, 0.15);
      color: var(--accent-danger);
      border: 1px solid rgba(248, 113, 113, 0.4);
    }}

    .approach-concept {{
      font-size: 14px;
      color: var(--text);
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--card-border);
    }}

    .list-block {{
      margin-bottom: 16px;
    }}

    .list-title {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    .list-pros {{ color: var(--accent-success); }}
    .list-cons {{ color: var(--accent-danger); }}

    .list-items {{
      list-style: none;
      font-size: 13px;
      color: var(--text-muted);
    }}

    .list-items li {{
      margin-bottom: 6px;
      position: relative;
      padding-left: 18px;
    }}

    .list-items li::before {{
      position: absolute;
      left: 0;
    }}

    .list-pros-items li::before {{ content: '✓'; color: var(--accent-success); }}
    .list-cons-items li::before {{ content: '✕'; color: var(--accent-danger); }}

    .triad-box {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px;
      margin-top: 16px;
      font-size: 12px;
    }}

    .triad-item {{
      margin-bottom: 8px;
    }}

    .triad-item:last-child {{
      margin-bottom: 0;
    }}

    .triad-label {{
      font-weight: 700;
      color: var(--text);
      display: block;
      margin-bottom: 2px;
    }}

    .triad-text {{
      color: var(--text-muted);
    }}

    /* Recommendation Banner */
    .recommendation-banner {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(59, 130, 246, 0.08) 100%);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 16px;
      padding: 32px;
      display: flex;
      gap: 24px;
      align-items: center;
      margin-bottom: 56px;
    }}

    .banner-icon {{
      font-size: 42px;
    }}

    .banner-content h3 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--accent-primary);
      margin-bottom: 8px;
    }}

    .banner-content p {{
      font-size: 14px;
      color: var(--text);
      margin-bottom: 12px;
    }}

    .banner-next {{
      font-size: 13px;
      color: var(--accent-warning);
      font-weight: 600;
    }}

    /* Footer */
    footer {{
      text-align: center;
      color: var(--text-muted);
      font-size: 13px;
      padding-top: 24px;
      border-top: 1px solid var(--card-border);
    }}

    @media (max-width: 768px) {{
      .pipeline-steps {{
        flex-direction: column;
      }}
      .step-arrow {{
        transform: rotate(90deg);
        margin: 4px 0;
      }}
      .recommendation-banner {{
        flex-direction: column;
        text-align: center;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge-pill">⚡ AI4A Brainstorm Contract v{version}</div>
      <h1>{project_name}</h1>
      <div class="meta-bar">
        <div>Học viên: <strong>{author}</strong></div>
        <div>Mentor: <strong>{mentor}</strong></div>
        <div>Ngày lập: <strong>{date}</strong></div>
      </div>
    </header>

    <!-- 1. The 4-Field Contract -->
    <section>
      <h2 class="section-title"><span>01.</span> Bản Hợp Đồng Thực Thi (Core Contract)</h2>
      <div class="contract-grid">
        <div class="contract-card card-outcome">
          <div class="card-header">
            <div class="card-icon">🎯</div>
            <div class="card-title">Outcome</div>
          </div>
          <div class="card-body">{contract_outcome_desc}</div>
          <div class="card-tag">Artifact: {contract_outcome_artifact}</div>
        </div>

        <div class="contract-card card-constraints">
          <div class="card-header">
            <div class="card-icon">🛡️</div>
            <div class="card-title">Constraints</div>
          </div>
          <div class="card-body">{contract_constraints_desc}</div>
          <div class="card-tag">Rule: {contract_constraints_rule}</div>
        </div>

        <div class="contract-card card-nongoals">
          <div class="card-header">
            <div class="card-icon">🚫</div>
            <div class="card-title">Non-goals</div>
          </div>
          <div class="card-body">{contract_nongoals_desc}</div>
          <div class="card-tag">Boundary: {contract_nongoals_boundary}</div>
        </div>

        <div class="contract-card card-acceptance">
          <div class="card-header">
            <div class="card-icon">✅</div>
            <div class="card-title">Acceptance Criteria</div>
          </div>
          <div class="card-body">{contract_acceptance_desc}</div>
          <div class="card-tag">Metric: {contract_acceptance_metric}</div>
        </div>
      </div>
    </section>

    <!-- 2. Workflow OIPO Flowchart -->
    <section>
      <h2 class="section-title"><span>02.</span> Quy Trình Đề Xuất (OIPO Pipeline)</h2>
      <div class="pipeline-container">
        <div class="pipeline-steps">
          {workflow_html}
        </div>
      </div>
    </section>

    <!-- 3. Approach Exploration -->
    <section>
      <h2 class="section-title"><span>03.</span> So Sánh Các Phương Án Kỹ Thuật (Trade-off Matrix)</h2>
      <div class="approaches-grid">
        {approaches_html}
      </div>
    </section>

    <!-- 4. Recommendation & Next Action -->
    <section>
      <div class="recommendation-banner">
        <div class="banner-icon">🏆</div>
        <div class="banner-content">
          <h3>Quyết Định Chọn: {recommendation_chosen}</h3>
          <p>{recommendation_rationale}</p>
          <div class="banner-next">👉 Bước tiếp theo: {recommendation_next_step}</div>
        </div>
      </div>
    </section>

    <footer>
      Đóng gói theo chuẩn Antigravity Customization System & AI4A Course Framework • Mentor: MT Đức Thuận
    </footer>
  </div>
</body>
</html>
"""

def render_workflow_steps(nodes):
    steps_html = []
    for idx, node in enumerate(nodes):
        steps_html.append(f"""
          <div class="step-item">
            <div class="step-icon">{node.get('icon', '📌')}</div>
            <div class="step-badge">{node.get('step', f'Step {idx+1}')}</div>
            <div class="step-name">{node.get('name', '')}</div>
            <div class="step-detail">{node.get('detail', '')}</div>
          </div>
        """)
        if idx < len(nodes) - 1:
            steps_html.append('<div class="step-arrow">➔</div>')
    return "".join(steps_html)

def render_approaches(approaches):
    cards_html = []
    for app in approaches:
        is_rec = app.get("badge_type") == "recommended"
        card_class = "approach-card is-recommended" if is_rec else "approach-card"
        badge_class = f"tag-badge badge-{app.get('badge_type', 'viable')}"

        pros_li = "".join([f"<li>{p}</li>" for p in app.get("pros", [])])
        cons_li = "".join([f"<li>{c}</li>" for c in app.get("cons", [])])

        cards_html.append(f"""
          <div class="{card_class}">
            <div>
              <div class="approach-header">
                <div class="approach-name">{app.get('name')}</div>
                <div class="{badge_class}">{app.get('badge', '')}</div>
              </div>
              <div class="approach-concept">{app.get('concept')}</div>

              <div class="list-block">
                <div class="list-title list-pros">Ưu điểm (Pros)</div>
                <ul class="list-items list-pros-items">{pros_li}</ul>
              </div>

              <div class="list-block">
                <div class="list-title list-cons">Nhược điểm (Cons)</div>
                <ul class="list-items list-cons-items">{cons_li}</ul>
              </div>
            </div>

            <div class="triad-box">
              <div class="triad-item">
                <span class="triad-label">Giả định chịu lực cốt lõi:</span>
                <span class="triad-text">{app.get('key_assumption', '')}</span>
              </div>
              <div class="triad-item">
                <span class="triad-label">Điểm gãy đầu tiên (First failure):</span>
                <span class="triad-text">{app.get('first_failure_point', '')}</span>
              </div>
            </div>
          </div>
        """)
    return "".join(cards_html)

def generate_html(data, output_path):
    contract = data.get("contract", {})
    workflow_nodes = data.get("workflow_nodes", [])
    approaches = data.get("approaches", [])
    recommendation = data.get("recommendation", {})

    rendered_html = HTML_TEMPLATE.format(
        version=data.get("version", "1.1.0"),
        project_name=data.get("project_name", "Brainstorm Brief"),
        author=data.get("author", "Học viên AI4A"),
        mentor=data.get("mentor", "MT Đức Thuận"),
        date=data.get("date", "2026-09-09"),
        contract_outcome_desc=contract.get("outcome", {}).get("desc", ""),
        contract_outcome_artifact=contract.get("outcome", {}).get("artifact", ""),
        contract_constraints_desc=contract.get("constraints", {}).get("desc", ""),
        contract_constraints_rule=contract.get("constraints", {}).get("rule", ""),
        contract_nongoals_desc=contract.get("non_goals", {}).get("desc", ""),
        contract_nongoals_boundary=contract.get("non_goals", {}).get("boundary", ""),
        contract_acceptance_desc=contract.get("acceptance_criteria", {}).get("desc", ""),
        contract_acceptance_metric=contract.get("acceptance_criteria", {}).get("metric", ""),
        workflow_html=render_workflow_steps(workflow_nodes),
        approaches_html=render_approaches(approaches),
        recommendation_chosen=recommendation.get("chosen", ""),
        recommendation_rationale=recommendation.get("rationale", ""),
        recommendation_next_step=recommendation.get("next_step", "")
    )

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(rendered_html, encoding="utf-8")
    print(f"[OK] Generated HTML brainstorm brief: {out_file.resolve()}")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Generate interactive HTML Brainstorm Brief for ai4a:brainstorm")
    parser.add_argument("--demo", action="store_true", help="Generate brief using sample District 1 Cafe dataset")
    parser.add_argument("--input", type=str, help="Path to JSON file containing brief data")
    parser.add_argument("--output", type=str, default="outputs/brainstorm-brief.html", help="Target output HTML file path")

    args = parser.parse_args()

    if args.demo or not args.input:
        data = DEFAULT_DEMO_DATA
    else:
        in_path = Path(args.input)
        if not in_path.exists():
            print(f"[ERROR] Input file not found: {in_path}", file=sys.stderr)
            sys.exit(1)
        with open(in_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    generate_html(data, args.output)

if __name__ == "__main__":
    main()
