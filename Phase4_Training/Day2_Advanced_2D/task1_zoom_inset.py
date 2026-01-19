"""
Day 2 - 任务2.1: 局部放大图高级应用
包含: 多区域放大、嵌套放大、交互式放大
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 2 - 任务2.1: 局部放大图高级应用")
print("=" * 60)

# ============================================================================
# 1. 多个局部放大区域
# ============================================================================
print("\n[1/3] 创建多个局部放大区域...")

# 生成数据
x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-x/10) + 0.1 * np.random.randn(1000)

fig, ax = plt.subplots(figsize=(14, 8))

# 绘制主图
ax.plot(x, y, 'b-', linewidth=1, alpha=0.7, label='原始数据')
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('多区域局部放大图示例', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

# 放大区域1: 左侧峰值
axins1 = inset_axes(ax, width="30%", height="30%", loc='upper right',
                    bbox_to_anchor=(0, 0.05, 1, 1), bbox_transform=ax.transAxes)
x1, x2, y1, y2 = 1.5, 2.5, 0.5, 1.0
axins1.plot(x, y, 'b-', linewidth=1.5)
axins1.set_xlim(x1, x2)
axins1.set_ylim(y1, y2)
axins1.set_title('区域1: 第一个峰', fontsize=10)
axins1.grid(True, alpha=0.3)
mark_inset(ax, axins1, loc1=2, loc2=4, fc="none", ec="red", linewidth=2)

# 放大区域2: 中间部分
axins2 = inset_axes(ax, width="30%", height="30%", loc='center left',
                    bbox_to_anchor=(0.05, 0, 1, 1), bbox_transform=ax.transAxes)
x1, x2, y1, y2 = 4.5, 5.5, -0.3, 0.3
axins2.plot(x, y, 'b-', linewidth=1.5)
axins2.set_xlim(x1, x2)
axins2.set_ylim(y1, y2)
axins2.set_title('区域2: 中间波动', fontsize=10)
axins2.grid(True, alpha=0.3)
mark_inset(ax, axins2, loc1=2, loc2=4, fc="none", ec="green", linewidth=2)

# 放大区域3: 右侧尾部
axins3 = inset_axes(ax, width="30%", height="30%", loc='lower right',
                    bbox_to_anchor=(0, 0.05, 1, 1), bbox_transform=ax.transAxes)
x1, x2, y1, y2 = 8.5, 9.5, -0.2, 0.2
axins3.plot(x, y, 'b-', linewidth=1.5)
axins3.set_xlim(x1, x2)
axins3.set_ylim(y1, y2)
axins3.set_title('区域3: 尾部细节', fontsize=10)
axins3.grid(True, alpha=0.3)
mark_inset(ax, axins3, loc1=2, loc2=4, fc="none", ec="blue", linewidth=2)

plt.tight_layout()
plt.savefig('Day2_Advanced_2D/output_1_multi_zoom.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_multi_zoom.png")
plt.close()

# ============================================================================
# 2. 嵌套局部放大图
# ============================================================================
print("\n[2/3] 创建嵌套局部放大图...")

# 生成复杂数据
x = np.linspace(0, 20, 2000)
y = np.sin(x) + 0.5 * np.sin(5*x) + 0.1 * np.sin(20*x) + 0.05 * np.random.randn(2000)

fig, ax = plt.subplots(figsize=(14, 8))

# 主图
ax.plot(x, y, 'b-', linewidth=0.8, alpha=0.7)
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('嵌套局部放大图示例 - 多尺度观察', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)

# 第一层放大
axins1 = inset_axes(ax, width="40%", height="40%", loc='upper right',
                    bbox_to_anchor=(0, 0.05, 1, 1), bbox_transform=ax.transAxes)
x1_1, x2_1, y1_1, y2_1 = 8, 12, -1, 2
axins1.plot(x, y, 'b-', linewidth=1)
axins1.set_xlim(x1_1, x2_1)
axins1.set_ylim(y1_1, y2_1)
axins1.set_title('第一层放大', fontsize=10, fontweight='bold')
axins1.grid(True, alpha=0.3)
mark_inset(ax, axins1, loc1=2, loc2=4, fc="none", ec="red", linewidth=2)

# 第二层放大（在第一层内部）
axins2 = inset_axes(axins1, width="50%", height="50%", loc='upper right')
x1_2, x2_2, y1_2, y2_2 = 9.5, 10.5, 0.5, 1.5
axins2.plot(x, y, 'b-', linewidth=1.5)
axins2.set_xlim(x1_2, x2_2)
axins2.set_ylim(y1_2, y2_2)
axins2.set_title('第二层放大', fontsize=8, fontweight='bold')
axins2.grid(True, alpha=0.3)
mark_inset(axins1, axins2, loc1=2, loc2=4, fc="none", ec="green", linewidth=2)

plt.tight_layout()
plt.savefig('Day2_Advanced_2D/output_2_nested_zoom.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_nested_zoom.png")
plt.close()

# ============================================================================
# 3. 实际应用：时间序列数据分析
# ============================================================================
print("\n[3/3] 创建实际应用示例...")

# 模拟股票价格数据
np.random.seed(42)
days = np.arange(0, 365)
price = 100 + np.cumsum(np.random.randn(365) * 2)
# 添加一个突然的价格波动
price[180:190] += np.linspace(0, 20, 10)
price[190:200] += np.linspace(20, 0, 10)

fig, ax = plt.subplots(figsize=(14, 8))

# 主图
ax.plot(days, price, 'b-', linewidth=1.5, label='股票价格')
ax.set_xlabel('交易日', fontsize=12)
ax.set_ylabel('价格 (元)', fontsize=12)
ax.set_title('股票价格走势分析 - 局部放大观察异常波动', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left')

# 放大异常波动区域
axins = inset_axes(ax, width="40%", height="40%", loc='center right',
                   bbox_to_anchor=(0, 0, 1, 1), bbox_transform=ax.transAxes)
x1, x2 = 170, 210
y1, y2 = price[170:210].min() - 5, price[170:210].max() + 5
axins.plot(days, price, 'b-', linewidth=2)
axins.axvspan(180, 200, alpha=0.2, color='red', label='异常波动期')
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_title('异常波动详细观察', fontsize=11, fontweight='bold')
axins.grid(True, alpha=0.3)
axins.legend(fontsize=9)

# 标记异常区域
mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="red", linewidth=2.5, linestyle='--')

# 在主图上标记异常区域
ax.axvspan(180, 200, alpha=0.1, color='red')
ax.text(190, price.max() - 10, '异常波动', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.tight_layout()
plt.savefig('Day2_Advanced_2D/output_3_practical_zoom.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_3_practical_zoom.png")
plt.close()

print("\n" + "=" * 60)
print("✅ Day 2 - 任务2.1 完成！")
print("已生成3个局部放大图示例:")
print("  1. output_1_multi_zoom.png - 多区域放大")
print("  2. output_2_nested_zoom.png - 嵌套放大")
print("  3. output_3_practical_zoom.png - 实际应用示例")
print("=" * 60)
