"""
Day 2 - 任务2.3: 其他高级二维图表
包含: 雷达图、极坐标图
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 2 - 任务2.3: 其他高级二维图表")
print("=" * 60)

# ============================================================================
# 1. 雷达图（Radar Chart）
# ============================================================================
print("\n[1/3] 创建雷达图...")

# 数据：三个产品在不同维度的评分
categories = ['性能', '价格', '设计', '续航', '相机', '系统']
n_categories = len(categories)

# 三个产品的评分
product_A = [90, 70, 85, 80, 95, 88]
product_B = [85, 90, 75, 85, 80, 82]
product_C = [75, 95, 90, 70, 85, 85]

# 使用Matplotlib创建雷达图
angles = np.linspace(0, 2 * np.pi, n_categories, endpoint=False).tolist()
# 闭合图形
product_A += product_A[:1]
product_B += product_B[:1]
product_C += product_C[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# 绘制三个产品
ax.plot(angles, product_A, 'o-', linewidth=2, label='产品A', color='#FF6B6B')
ax.fill(angles, product_A, alpha=0.25, color='#FF6B6B')

ax.plot(angles, product_B, 'o-', linewidth=2, label='产品B', color='#4ECDC4')
ax.fill(angles, product_B, alpha=0.25, color='#4ECDC4')

ax.plot(angles, product_C, 'o-', linewidth=2, label='产品C', color='#45B7D1')
ax.fill(angles, product_C, alpha=0.25, color='#45B7D1')

# 设置标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
ax.set_title('产品多维度对比雷达图', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('Day2_Advanced_2D/output_1_radar_chart.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_radar_chart.png")
plt.close()

# 使用Plotly创建交互式雷达图
categories_plotly = ['性能', '价格', '设计', '续航', '相机', '系统']

fig_plotly = go.Figure()

fig_plotly.add_trace(go.Scatterpolar(
    r=[90, 70, 85, 80, 95, 88],
    theta=categories_plotly,
    fill='toself',
    name='产品A',
    line_color='#FF6B6B'
))

fig_plotly.add_trace(go.Scatterpolar(
    r=[85, 90, 75, 85, 80, 82],
    theta=categories_plotly,
    fill='toself',
    name='产品B',
    line_color='#4ECDC4'
))

fig_plotly.add_trace(go.Scatterpolar(
    r=[75, 95, 90, 70, 85, 85],
    theta=categories_plotly,
    fill='toself',
    name='产品C',
    line_color='#45B7D1'
))

fig_plotly.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=True,
    title='产品多维度对比雷达图（交互式）',
    font=dict(family='Microsoft YaHei', size=12),
    width=800,
    height=800
)

fig_plotly.write_html('Day2_Advanced_2D/output_1_radar_chart_interactive.html')
print("✓ 已保存: output_1_radar_chart_interactive.html (交互式)")

# ============================================================================
# 2. 极坐标图（Polar Chart）
# ============================================================================
print("\n[2/3] 创建极坐标图...")

# 数据：24小时温度变化
hours = np.arange(0, 24)
temperature = 20 + 5 * np.sin((hours - 6) * np.pi / 12) + np.random.randn(24) * 0.5

# 转换为极坐标（角度）
theta = np.linspace(0, 2 * np.pi, 24, endpoint=False)

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# 绘制温度曲线
bars = ax.bar(theta, temperature, width=2*np.pi/24, bottom=15, 
              alpha=0.8, edgecolor='white', linewidth=2)

# 根据温度设置颜色
colors = plt.cm.RdYlBu_r((temperature - temperature.min()) / (temperature.max() - temperature.min()))
for bar, color in zip(bars, colors):
    bar.set_facecolor(color)

# 设置标签
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks(theta)
ax.set_xticklabels([f'{h}:00' for h in hours], fontsize=10)
ax.set_ylim(15, 30)
ax.set_title('24小时温度变化极坐标图', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, linestyle='--', alpha=0.5)

# 添加温度标注
for angle, temp, hour in zip(theta, temperature, hours):
    if hour % 3 == 0:  # 每3小时标注一次
        ax.text(angle, temp + 0.5, f'{temp:.1f}°C', 
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('Day2_Advanced_2D/output_2_polar_chart.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_polar_chart.png")
plt.close()

# ============================================================================
# 3. 极坐标散点图 - 风向风速
# ============================================================================
print("\n[3/3] 创建极坐标散点图...")

# 模拟风向风速数据
np.random.seed(42)
n_points = 100
wind_direction = np.random.uniform(0, 2*np.pi, n_points)  # 风向（角度）
wind_speed = np.random.gamma(3, 2, n_points)  # 风速（半径）
wind_frequency = np.random.randint(1, 10, n_points)  # 频率（点大小）

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))

# 绘制散点
scatter = ax.scatter(wind_direction, wind_speed, 
                    c=wind_speed, s=wind_frequency*20, 
                    cmap='YlOrRd', alpha=0.6, edgecolors='black', linewidth=0.5)

# 添加颜色条
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('风速 (m/s)', fontsize=12)

# 设置标签
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
directions = ['北', '东北', '东', '东南', '南', '西南', '西', '西北']
ax.set_xticks(np.linspace(0, 2*np.pi, 8, endpoint=False))
ax.set_xticklabels(directions, fontsize=12)
ax.set_ylim(0, wind_speed.max() * 1.1)
ax.set_title('风向风速分布图（极坐标散点图）', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, linestyle='--', alpha=0.5)

# 添加说明
ax.text(0, -wind_speed.max() * 0.15, 
        '点的大小表示频率，颜色表示风速', 
        ha='center', fontsize=11, 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('Day2_Advanced_2D/output_3_polar_scatter.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_3_polar_scatter.png")
plt.close()

# 使用Plotly创建交互式极坐标图
fig_polar = go.Figure()

fig_polar.add_trace(go.Scatterpolar(
    r=wind_speed,
    theta=np.degrees(wind_direction),
    mode='markers',
    marker=dict(
        size=wind_frequency*2,
        color=wind_speed,
        colorscale='YlOrRd',
        showscale=True,
        colorbar=dict(title="风速 (m/s)"),
        line=dict(color='black', width=0.5)
    ),
    text=[f'风向: {np.degrees(d):.0f}°<br>风速: {s:.1f} m/s<br>频率: {f}' 
          for d, s, f in zip(wind_direction, wind_speed, wind_frequency)],
    hovertemplate='%{text}<extra></extra>'
))

fig_polar.update_layout(
    title='风向风速分布图（交互式）',
    font=dict(family='Microsoft YaHei', size=12),
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, wind_speed.max() * 1.1]
        ),
        angularaxis=dict(
            direction='clockwise',
            rotation=90
        )
    ),
    width=900,
    height=900
)

fig_polar.write_html('Day2_Advanced_2D/output_3_polar_scatter_interactive.html')
print("✓ 已保存: output_3_polar_scatter_interactive.html (交互式)")

print("\n" + "=" * 60)
print("✅ Day 2 - 任务2.3 完成！")
print("已生成3个高级二维图表:")
print("  1. output_1_radar_chart.png/html - 雷达图")
print("  2. output_2_polar_chart.png - 极坐标图")
print("  3. output_3_polar_scatter.png/html - 极坐标散点图")
print("=" * 60)
