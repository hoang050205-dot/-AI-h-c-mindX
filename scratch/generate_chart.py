import matplotlib.pyplot as plt
import numpy as np
import os
import openpyxl
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice

# Define data
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

colors = [
    '#2774CB',  # Karaage - Xanh dương
    '#E36531',  # Crispy fried thigh - Cam
    '#1DB078',  # Fried wings - Xanh ngọc
    '#EAA100',  # Nuggets - Vàng cam
    '#E277A6',  # Grilled skewers - Hồng
    '#007F00',  # Chicken breast - Xanh lá cây đậm
    '#6050DC'   # Other - Tím
]

# Matrix data: rows = markets, cols = products
# Singapore: 12, 18, 18, 20, 12, 15, 5
# EU: 10, 10, 10, 25, 5, 35, 5
# China: 10, 20, 25, 15, 5, 10, 15
data = {
    'Karaage': [12, 10, 10],
    'Crispy fried thigh': [18, 10, 20],
    'Fried wings': [18, 10, 25],
    'Nuggets': [20, 25, 15],
    'Grilled skewers': [12, 5, 5],
    'Chicken breast': [15, 35, 10],
    'Other': [5, 5, 15]
}

# 1. Render High-Resolution Matplotlib Chart (matching the original style 100%)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Calibri']

fig, ax = plt.subplots(figsize=(11, 5.2), dpi=300)

x = np.arange(len(markets))
n_products = len(products)
total_group_width = 0.72
bar_width = total_group_width / n_products

# Offsets for each product bar in a group
offsets = np.linspace(-total_group_width/2 + bar_width/2, total_group_width/2 - bar_width/2, n_products)

bars_dict = {}
for i, (prod, color) in enumerate(zip(products, colors)):
    values = data[prod]
    rects = ax.bar(x + offsets[i], values, width=bar_width*0.92, label=prod, color=color, zorder=3)
    bars_dict[prod] = rects
    
    # Data labels on top of bars
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2.5),  # 2.5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=8.5, color='#4A4A4A', fontweight='medium')

# Grid and Spines
ax.yaxis.grid(True, linestyle='-', color='#E5E5E5', linewidth=1, zorder=1)
ax.xaxis.grid(False)

# Y-axis formatting (0% to 40% since Chicken breast in EU reaches 35%)
ax.set_ylim(0, 40)
y_ticks = np.arange(0, 41, 5)
ax.set_yticks(y_ticks)
ax.set_yticklabels([f'{y}%' for y in y_ticks], color='#555555', fontsize=9.5)
ax.set_ylabel('Share of product mix (%)', color='#555555', fontsize=10.5, labelpad=10)

# X-axis formatting
ax.set_xticks(x)
ax.set_xticklabels(markets, color='#555555', fontsize=10.5)
ax.set_xlabel('Market', color='#555555', fontsize=10.5, labelpad=10)

# Remove top, right, and left spines, keep bottom subtle
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')
ax.spines['bottom'].set_linewidth(1.2)

# Remove tick marks
ax.tick_params(axis='both', which='both', length=0)

# Legend on the right side
legend = ax.legend(
    loc='center left',
    bbox_to_anchor=(1.02, 0.5),
    frameon=False,
    fontsize=9.5,
    labelcolor='#444444',
    handletextpad=0.8,
    borderaxespad=0.,
    handlelength=1.0,
    handleheight=1.0
)

plt.tight_layout()

os.makedirs('outputs/reports', exist_ok=True)
png_path = 'outputs/reports/product_mix_singapore_eu_china.png'
svg_path = 'outputs/reports/product_mix_singapore_eu_china.svg'

plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(svg_path, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {png_path} and {svg_path}")
