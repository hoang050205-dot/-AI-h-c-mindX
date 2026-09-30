import matplotlib.pyplot as plt
import numpy as np
import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice


# -------------------------------------------------------------
# 1. DATA PREPARATION
# -------------------------------------------------------------
markets = ['Singapore', 'EU', 'China']
products = [
    'Karaage',
    'Crispy fried thigh',
    'Fried wings',
    'Nuggets',
    'Grilled skewers',
    'Chicken breast',
    'Other'
]

# Exact Hex colors from the prompt and reference image
colors_hex = [
    '#2774CB',  # Karaage - Xanh dương
    '#E36531',  # Crispy fried thigh - Cam
    '#1DB078',  # Fried wings - Xanh ngọc
    '#EAA100',  # Nuggets - Vàng cam
    '#E277A6',  # Grilled skewers - Hồng
    '#007F00',  # Chicken breast - Xanh lá cây đậm
    '#6050DC'   # Other - Tím
]

data_matrix = {
    'Singapore': [12, 18, 18, 20, 12, 15, 5],
    'EU':        [10, 10, 10, 25,  5, 35, 5],
    'China':     [10, 20, 25, 15,  5, 10, 15]
}

# -------------------------------------------------------------
# 2. GENERATE ULTRA-HIGH QUALITY CHART (MATPLOTLIB)
# -------------------------------------------------------------
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)

x = np.arange(len(markets))
n_products = len(products)
cluster_width = 0.70  # Width occupied by the 7 bars
bar_width = cluster_width / n_products

# Calculate center positions for each bar in cluster
offsets = np.linspace(-cluster_width/2 + bar_width/2, cluster_width/2 - bar_width/2, n_products)

# Draw bars with slight edge color matching fill for crispness, touching each other like the reference
for i, prod in enumerate(products):
    color = colors_hex[i]
    values = [data_matrix[m][i] for m in markets]
    
    # Bars touch side by side within each cluster
    rects = ax.bar(
        x + offsets[i],
        values,
        width=bar_width * 0.96,  # 4% hairline gap for clean definition
        label=prod,
        color=color,
        edgecolor='none',
        zorder=3
    )
    
    # Value labels on top of bars
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f'{int(height)}',
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3.5),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=8.5,
            color='#4A4A4A',
            fontfamily='sans-serif'
        )

# Y-Axis Formatting (0% to 35% or 40%)
ax.set_ylim(0, 40)
y_ticks = np.arange(0, 41, 5)
ax.set_yticks(y_ticks)
ax.set_yticklabels([f'{y}%' for y in y_ticks], color='#5A5A5A', fontsize=9.5)
ax.set_ylabel('Share of product mix (%)', color='#5A5A5A', fontsize=10.5, labelpad=12)

# X-Axis Formatting
ax.set_xticks(x)
ax.set_xticklabels(markets, color='#4A4A4A', fontsize=10.5)
ax.set_xlabel('Market', color='#5A5A5A', fontsize=10.5, labelpad=10)

# Gridlines (horizontal subtle light grey, behind bars)
ax.yaxis.grid(True, linestyle='-', color='#E4E4E4', linewidth=0.9, zorder=1)
ax.xaxis.grid(False)

# Clean Spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#D0D0D0')
ax.spines['bottom'].set_linewidth(1.0)

# Hide ticks
ax.tick_params(axis='both', which='both', length=0, pad=6)

# Legend on the right
legend = ax.legend(
    loc='center left',
    bbox_to_anchor=(1.02, 0.5),
    frameon=False,
    fontsize=9.5,
    labelcolor='#404040',
    handletextpad=0.7,
    borderaxespad=0.,
    handlelength=1.1,
    handleheight=1.1,
    labelspacing=0.85
)

plt.tight_layout()

os.makedirs('outputs/reports', exist_ok=True)
png_path = 'outputs/reports/CP_Product_Mix_Singapore_EU_China.png'
svg_path = 'outputs/reports/CP_Product_Mix_Singapore_EU_China.svg'

plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(svg_path, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Generated chart image: {png_path}")

# -------------------------------------------------------------
# 3. CREATE STANDARDIZED EXCEL WORKBOOK WITH EMBEDDED NATIVE CHART
# -------------------------------------------------------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Product Mix"

# Sheet Title
ws['A1'] = "C.P. GROUP - PRODUCT MIX SHARE BY MARKET (%)"
ws['A1'].font = Font(name='Segoe UI', size=13, bold=True, color='1F4E79')
ws.merge_cells('A1:H1')

# Table Headers
headers = ['Market'] + products
for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=3, column=col_idx, value=h)
    cell.font = Font(name='Segoe UI', size=10, bold=True, color='FFFFFF')
    cell.fill = PatternFill(start_color='2C3E50', end_color='2C3E50', fill_type='solid')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Data Rows
border_thin = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for row_idx, market in enumerate(markets, 4):
    c = ws.cell(row=row_idx, column=1, value=market)
    c.font = Font(name='Segoe UI', size=10, bold=True)
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = border_thin
    
    for col_idx, val in enumerate(data_matrix[market], 2):
        c_val = ws.cell(row=row_idx, column=col_idx, value=val)
        c_val.font = Font(name='Segoe UI', size=10)
        c_val.alignment = Alignment(horizontal='center', vertical='center')
        c_val.border = border_thin

# Column widths
ws.column_dimensions['A'].width = 16
for c in ['B', 'C', 'D', 'E', 'F', 'G', 'H']:
    ws.column_dimensions[c].width = 18

# Add Native Excel Clustered Column Chart
chart = BarChart()
chart.type = "col"
chart.style = 10
chart.grouping = "clustered"
chart.title = "Share of product mix by Market"
chart.y_axis.title = "Share of product mix (%)"
chart.x_axis.title = "Market"
chart.width = 18
chart.height = 10
chart.legend.legendPos = "r"

# References
# Data values are in columns B to H, rows 3 to 6 (row 3 is titles of series)
data_ref = Reference(ws, min_col=2, min_row=3, max_col=8, max_row=6)
cats_ref = Reference(ws, min_col=1, min_row=4, max_row=6)

chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)

# Enable Data Labels
chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True

# Apply exact colors to series
hex_clean = [c.replace('#', '') for c in colors_hex]
for i, s in enumerate(chart.series):
    s.graphicalProperties.solidFill = hex_clean[i]

ws.add_chart(chart, "A9")

excel_path = 'outputs/reports/CP_Product_Mix_Singapore_EU_China.xlsx'
wb.save(excel_path)
print(f"Generated Excel workbook: {excel_path}")
