#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_legal_report_html.py — Xuất Bản Báo Cáo Thẩm Định Pháp Lý Hải Quan HTML Doanh Nghiệp
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / AI4A Antigravity
Mô tả: Tự động kết xuất Báo cáo Giai đoạn 2 thành tệp single-file HTML chuẩn Corporate UI,
       tích hợp bảng checklist tương tác, hộp cảnh báo chế tài NĐ 128 và nút in/lưu PDF.
Zero external dependencies.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
OUTPUTS_DIR = WORKSPACE_ROOT / "outputs" / "reports"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Báo Cáo Thẩm Định Pháp Lý Hải Quan</title>
    <style>
        :root {{
            --primary: #0f2744;
            --primary-light: #1e3a5f;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --success: #059669;
            --warning: #d97706;
            --danger: #dc2626;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --border-light: #f1f5f9;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
            padding: 30px 15px;
        }}

        .container {{
            max-width: 960px;
            margin: 0 auto;
            background: var(--card-bg);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        /* Header */
        .report-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: #ffffff;
            padding: 35px 40px;
            position: relative;
        }}

        .badge-brand {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(4px);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        .report-title {{
            font-size: 1.85rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 10px;
        }}

        .report-subtitle {{
            font-size: 1rem;
            opacity: 0.85;
            max-width: 750px;
        }}

        .header-meta {{
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 0.875rem;
            opacity: 0.9;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-top: 15px;
        }}

        .header-meta-item strong {{
            color: #93c5fd;
        }}

        /* Action Bar */
        .action-bar {{
            background: #f1f5f9;
            padding: 12px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }}

        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
            background: #dcfce7;
            color: #166534;
        }}

        .status-pill::before {{
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #22c55e;
        }}

        .btn-print {{
            background: var(--primary);
            color: #ffffff;
            border: none;
            padding: 8px 18px;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }}

        .btn-print:hover {{
            background: var(--primary-light);
            transform: translateY(-1px);
        }}

        /* Content Sections */
        .content-body {{
            padding: 40px;
        }}

        .section-block {{
            margin-bottom: 35px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border-light);
        }}

        .section-num {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: var(--primary);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.95rem;
        }}

        .section-title {{
            font-size: 1.25rem;
            color: var(--primary);
            font-weight: 700;
        }}

        /* Meta Table */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }}

        .info-row {{
            display: flex;
            flex-direction: column;
        }}

        .info-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .info-val {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-main);
        }}

        /* Checklist */
        .checklist-group {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .checklist-item {{
            display: flex;
            align-items: flex-start;
            gap: 14px;
            background: #ffffff;
            padding: 14px 18px;
            border-radius: 8px;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }}

        .checklist-item:hover {{
            border-color: var(--accent);
            background: #f8fafc;
        }}

        .checklist-item input[type="checkbox"] {{
            margin-top: 4px;
            width: 18px;
            height: 18px;
            accent-color: var(--primary);
            cursor: pointer;
        }}

        .checklist-text strong {{
            display: block;
            font-size: 0.95rem;
            color: var(--primary);
            margin-bottom: 3px;
        }}

        .checklist-text p {{
            font-size: 0.875rem;
            color: #334155;
            margin: 0;
        }}

        /* Callout Alerts */
        .alert-box {{
            border-radius: 8px;
            padding: 20px;
            margin-top: 15px;
            border-left: 5px solid;
        }}

        .alert-warning {{
            background: #fffbeb;
            border-color: var(--warning);
            color: #92400e;
        }}

        .alert-danger {{
            background: #fef2f2;
            border-color: var(--danger);
            color: #991b1b;
        }}

        .alert-title {{
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .alert-content {{
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .alert-content ul {{
            margin-left: 20px;
            margin-top: 8px;
        }}

        /* Footer */
        .report-footer {{
            background: #f8fafc;
            border-top: 1px solid var(--border);
            padding: 25px 40px;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        @media print {{
            body {{
                padding: 0;
                background: #ffffff;
            }}
            .container {{
                box-shadow: none;
                border: none;
            }}
            .action-bar {{
                display: none;
            }}
            .checklist-item input[type="checkbox"] {{
                border: 1px solid #000;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="report-header">
            <span class="badge-brand">AI4A • Antigravity Customs Legal Copilot v2.0</span>
            <h1 class="report-title">{title}</h1>
            <p class="report-subtitle">{subtitle}</p>
            <div class="header-meta">
                <div class="header-meta-item">Số hiệu: <strong>{doc_number}</strong></div>
                <div class="header-meta-item">Cơ quan: <strong>{authority}</strong></div>
                <div class="header-meta-item">Hiệu lực: <strong>{effective_date}</strong></div>
                <div class="header-meta-item">Ngày thẩm định: <strong>{audit_date}</strong></div>
            </div>
        </header>

        <!-- Action Bar -->
        <div class="action-bar">
            <div class="status-pill">{status_label}</div>
            <button class="btn-print" onclick="window.print()">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
                    <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
                </svg>
                In Báo Cáo / Lưu PDF
            </button>
        </div>

        <!-- Body -->
        <main class="content-body">
            <!-- Phần 1 -->
            <section class="section-block">
                <div class="section-header">
                    <div class="section-num">1</div>
                    <h2 class="section-title">Thông Tin Pháp Lý & Quan Hệ Phả Hệ</h2>
                </div>
                <div class="info-grid">
                    <div class="info-row">
                        <span class="info-label">Số hiệu & Loại văn bản</span>
                        <span class="info-val">{doc_number} ({doc_type})</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Cơ quan ban hành</span>
                        <span class="info-val">{authority}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Ngày ban hành & Có hiệu lực</span>
                        <span class="info-val">{issue_date} ──► {effective_date}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Văn bản sửa đổi / Thay thế</span>
                        <span class="info-val">{relations_text}</span>
                    </div>
                </div>
            </section>

            <!-- Phần 2 -->
            <section class="section-block">
                <div class="section-header">
                    <div class="section-num">2</div>
                    <h2 class="section-title">Phạm Vi Áp Dụng & Đối Tượng Điều Chỉnh</h2>
                </div>
                <p style="font-size: 0.95rem; color: #334155; margin-bottom: 12px;">{scope_text}</p>
                <div style="background: #f1f5f9; padding: 12px 18px; border-radius: 6px; font-size: 0.9rem;">
                    <strong>Đối tượng áp dụng bắt buộc:</strong> {target_audience}
                </div>
            </section>

            <!-- Phần 3 -->
            <section class="section-block">
                <div class="section-header">
                    <div class="section-num">3</div>
                    <h2 class="section-title">Checklist Tuân Thủ & Trình Tự Thực Thi Thực Tế</h2>
                </div>
                <div class="checklist-group">
                    {checklist_items}
                </div>
            </section>

            <!-- Phần 4 -->
            <section class="section-block">
                <div class="section-header">
                    <div class="section-num">4</div>
                    <h2 class="section-title">Cảnh Báo Chế Tài Xử Phạt Vi Phạm Hành Chính</h2>
                </div>
                
                <div class="alert-box alert-warning">
                    <div class="alert-title">
                        <span>⚠️ Điểm Mới Cần Lưu Ý Trong Quy Trình Vận Hành 2026:</span>
                    </div>
                    <div class="alert-content">
                        {notes_text}
                    </div>
                </div>

                <div class="alert-box alert-danger">
                    <div class="alert-title">
                        <span>🛑 Khung Chế Tài Xử Phạt Hành Chính (Căn cứ Nghị định 128/2020/NĐ-CP):</span>
                    </div>
                    <div class="alert-content">
                        {sanctions_text}
                    </div>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="report-footer">
            <p>Báo cáo được khởi tạo tự động bởi <strong>Customs Legal Copilot v2.0 Pro</strong> • Workspace Cá nhân AI4A</p>
            <p style="margin-top: 4px; font-size: 0.75rem; color: #94a3b8;">Báo cáo mang tính chất tham mưu nội bộ nhằm rà soát tuân thủ chứng từ trước khi thông quan.</p>
        </footer>
    </div>
</body>
</html>
"""

def generate_report_html(data, output_path=None):
    if output_path is None:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = data.get("doc_number", "Legal_Report").replace("/", "_").replace(".", "_")
        output_path = OUTPUTS_DIR / f"Bao_Cao_Phap_Ly_{safe_name}.html"

    # Xây dựng danh sách checklist items
    items_html = []
    for step in data.get("checklist", []):
        checked = "checked" if step.get("checked", False) else ""
        item_html = f"""
        <div class="checklist-item">
            <input type="checkbox" id="{step.get('id', '')}" {checked}>
            <div class="checklist-text">
                <label for="{step.get('id', '')}"><strong>{step.get('title', '')}</strong></label>
                <p>{step.get('desc', '')}</p>
            </div>
        </div>
        """
        items_html.append(item_html)

    rendered = HTML_TEMPLATE.format(
        title=data.get("title", "Báo Cáo Thẩm Định Pháp Lý"),
        subtitle=data.get("subtitle", "Thẩm định quy chuẩn và căn cứ thực thi thủ tục hải quan"),
        doc_number=data.get("doc_number", "N/A"),
        authority=data.get("authority", "Bộ Tài chính / Chính phủ"),
        effective_date=data.get("effective_date", "Hiện hành"),
        audit_date=datetime.now().strftime("%d/%m/%Y"),
        status_label=data.get("status_label", "Còn Hiệu Lực Thi Hành"),
        doc_type=data.get("doc_type", "Thông tư"),
        issue_date=data.get("issue_date", "N/A"),
        relations_text=data.get("relations_text", "Sửa đổi bổ sung theo lộ trình"),
        scope_text=data.get("scope_text", "Áp dụng cho toàn bộ hoạt động xuất nhập khẩu."),
        target_audience=data.get("target_audience", "Doanh nghiệp XNK, Đại lý hải quan, Hãng tàu."),
        checklist_items="\n".join(items_html),
        notes_text=data.get("notes_text", "Cần kiểm tra kỹ mã chứng từ trên Cổng thông tin một cửa quốc gia."),
        sanctions_text=data.get("sanctions_text", "Phạt vi phạm theo Nghị định 128/2020/NĐ-CP.")
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ Đã xuất bản Báo cáo Pháp lý HTML: {output_path}")
    return output_path

def get_demo_report_data():
    """Dữ liệu mẫu cho Thông tư 121/2025 và Nghị định 174/2025"""
    return {
        "title": "BÁO CÁO THẨM ĐỊNH PHÁP LÝ: THÔNG TƯ 121/2025/TT-BTC & NGHỊ ĐỊNH 174/2025/NĐ-CP",
        "subtitle": "Quy trình nộp hồ sơ hải quan số hóa toàn diện, liên thông e-C/O và giảm 2% thuế GTGT đến hết 2026",
        "doc_number": "121/2025/TT-BTC",
        "doc_type": "Thông tư",
        "authority": "Bộ Tài chính",
        "issue_date": "18/12/2025",
        "effective_date": "01/02/2026",
        "status_label": "Còn Hiệu Lực (Văn bản mới nhất 2026)",
        "relations_text": "Sửa đổi toàn diện Thông tư 38/2015/TT-BTC và Thông tư 39/2018/TT-BTC; thi hành Nghị định 167/2025/NĐ-CP",
        "scope_text": "Điều chỉnh trình tự thủ tục hải quan, kiểm tra giám sát, phương thức nộp chứng từ điện tử qua Cổng Một cửa Quốc gia (NSW) và khấu trừ/giảm thuế đối với toàn bộ hàng hóa xuất khẩu, nhập khẩu thương mại.",
        "target_audience": "Doanh nghiệp xuất nhập khẩu, đại lý làm thủ tục hải quan, doanh nghiệp chế xuất, hãng vận tải và chi cục hải quan cửa khẩu.",
        "checklist": [
            {
                "id": "step1",
                "title": "Bước 1: Rà soát tính đủ của hồ sơ điện tử trước khi khai báo",
                "desc": "Kiểm tra đối chiếu Invoice, Packing List, B/L. Nếu C/O là dạng điện tử (e-C/O Form E, Form D, EUR.1), tra cứu trạng thái đã tiếp nhận trên Cổng Một cửa Quốc gia (NSW) để lấy mã định danh chứng từ.",
                "checked": True
            },
            {
                "id": "step2",
                "title": "Bước 2: Khai báo tờ khai VNACCS & Áp mã giảm thuế GTGT 8%",
                "desc": "Khai mã số e-C/O và mã chứng thư chuyên ngành vào ô ghi chú tờ khai. Tra cứu mã HS trên Phụ lục I, II của Nghị định 174/2025; nếu không thuộc diện loại trừ, áp mã thuế suất VAT giảm (8%). Tuyệt đối không scan đính kèm chứng từ đã liên thông NSW.",
                "checked": True
            },
            {
                "id": "step3",
                "title": "Bước 3: Hậu kiểm & Khai bổ sung trong vòng 60 ngày",
                "desc": "Sau khi thông quan, tiến hành đối soát số liệu số học giữa tờ khai và hồ sơ thanh toán quốc tế trong 30 ngày. Nếu có sai lệch thuế/HS, nộp tờ khai bổ sung AMA/AMC trước mốc 60 ngày để được miễn phạt vi phạm hành chính.",
                "checked": False
            }
        ],
        "notes_text": "Thông tư 121/2025/TT-BTC chính thức bãi bỏ việc yêu cầu doanh nghiệp phải scan đính kèm các chứng từ chuyên ngành (C/O, Giấy phép, Kiểm dịch) nếu dữ liệu đã được các Bộ ngành đẩy lên Cổng NSW. Giúp giảm thiểu 80% dung lượng hồ sơ đính kèm và hạn chế nghẽn mạng VNACCS.",
        "sanctions_text": "<ul><li><strong>Khai sai mã thuế suất 8% cho hàng loại trừ (Phụ lục I & II):</strong> Phạt 20% tính trên số tiền thuế khai thiếu theo Khoản 2 Điều 9 Nghị định 128/2020/NĐ-CP + tiền chậm nộp 0.03%/ngày.</li><li><strong>Khai bổ sung quá hạn 60 ngày sau khi có quyết định kiểm tra:</strong> Mất quyền tự nguyện, bị xử phạt từ 10% đến 20% số thuế thiếu và hạ bậc tuân thủ phân luồng doanh nghiệp (Điều 9 NĐ 128).</li><li><strong>Chậm nộp Báo cáo quyết toán nguyên phụ liệu SXXK quá 30 ngày:</strong> Phạt tiền từ 5.000.000đ đến 10.000.000đ theo Khoản 4 Điều 7 NĐ 128/2020.</li></ul>"
    }

def main():
    parser = argparse.ArgumentParser(description="Xuất bản Báo cáo Thẩm định Pháp lý HTML Doanh nghiệp")
    parser.add_argument("--demo", action="store_true", help="Xuất báo cáo mẫu Thông tư 121/2025 & NĐ 174/2025")
    parser.add_argument("--input", type=str, help="Đường dẫn file JSON chứa dữ liệu báo cáo")
    parser.add_argument("--output", type=str, help="Đường dẫn file HTML đầu ra")

    args = parser.parse_args()

    if args.demo:
        data = get_demo_report_data()
        out = Path(args.output) if args.output else None
        generate_report_html(data, out)
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        out = Path(args.output) if args.output else None
        generate_report_html(data, out)
    else:
        # Mặc định chạy demo
        data = get_demo_report_data()
        generate_report_html(data)

if __name__ == "__main__":
    main()
