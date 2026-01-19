"""
B站数据三维可视化
生成三维图表分析B站热门视频数据
"""

import sys
import io

# 解决Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

# 设置中文字体和全局字体大小
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12  # 全局字体大小
plt.rcParams['axes.labelsize'] = 14  # 坐标轴标签大小
plt.rcParams['axes.titlesize'] = 16  # 子图标题大小
plt.rcParams['legend.fontsize'] = 12  # 图例字体大小

print("=" * 70)
print("B站数据三维可视化")
print("=" * 70)

# 创建输出目录
os.makedirs('visualizations', exist_ok=True)

# 读取数据
print("\n[1/5] 读取数据...")
try:
    df = pd.read_csv('data/bilibili_data.csv', encoding='utf-8-sig')
    print(f"  √ 成功读取 {len(df)} 条数据")
except FileNotFoundError:
    print("  × 错误: 找不到数据文件！")
    print("  请先运行 crawler.py 爬取数据")
    exit(1)

# ============================================================================
# 1. 三维散点图：播放量-点赞数-投币数
# ============================================================================
print("\n[2/5] 生成三维散点图...")

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 使用收藏数作为颜色映射
scatter = ax.scatter(df['播放量'], df['点赞数'], df['投币数'],
                    c=df['收藏数'], cmap='viridis', s=100, alpha=0.6,
                    edgecolors='black', linewidth=0.5)

ax.set_xlabel('播放量', fontsize=12, labelpad=10)
ax.set_ylabel('点赞数', fontsize=12, labelpad=10)
ax.set_zlabel('投币数', fontsize=12, labelpad=10)
ax.set_title('视频数据三维分布图\n（颜色表示收藏数）', fontsize=16, fontweight='bold', pad=20)

# 添加颜色条
cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
cbar.set_label('收藏数', fontsize=11)

ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('visualizations/06_三维散点图.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/06_三维散点图.png")
plt.close()

# ============================================================================
# 2. 三维柱状图：各分区数据对比
# ============================================================================
print("\n[3/5] 生成三维柱状图...")

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 准备数据
categories = df['排行榜分区'].unique()
n_categories = len(categories)

# 计算各分区的平均数据
category_data = df.groupby('排行榜分区').agg({
    '播放量': 'mean',
    '点赞数': 'mean',
    '投币数': 'mean'
}).reset_index()

# 设置位置
x_pos = np.arange(n_categories)
y_pos = np.array([0, 1, 2])  # 三个指标

# 创建网格
xpos, ypos = np.meshgrid(x_pos, y_pos)
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)

# 准备数据
dx = dy = 0.5
dz = []
colors = []

color_map = ['#FF6B6B', '#4ECDC4', '#45B7D1']

for i, category in enumerate(categories):
    cat_data = category_data[category_data['排行榜分区'] == category].iloc[0]
    dz.extend([cat_data['播放量']/1000, cat_data['点赞数']/100, cat_data['投币数']/100])
    colors.extend(color_map)

# 绘制3D柱状图
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, alpha=0.8, edgecolor='black')

# 设置标签
ax.set_xlabel('分区', fontsize=12, labelpad=10)
ax.set_ylabel('指标', fontsize=12, labelpad=10)
ax.set_zlabel('数值（已缩放）', fontsize=12, labelpad=10)
ax.set_title('各分区数据三维对比图', fontsize=16, fontweight='bold', pad=20)

ax.set_xticks(x_pos + dx/2)
ax.set_xticklabels(categories, rotation=15, ha='right')
ax.set_yticks(y_pos + dy/2)
ax.set_yticklabels(['播放量\n(×1000)', '点赞数\n(×100)', '投币数\n(×100)'])

ax.view_init(elev=25, azim=45)

plt.tight_layout()
plt.savefig('visualizations/07_三维柱状图.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/07_三维柱状图.png")
plt.close()

# ============================================================================
# 3. 三维曲面图：互动率关系
# ============================================================================
print("\n[4/5] 生成三维曲面图...")

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 创建网格数据
x = np.linspace(df['播放量'].min(), df['播放量'].max(), 50)
y = np.linspace(df['点赞数'].min(), df['点赞数'].max(), 50)
X, Y = np.meshgrid(x, y)

# 使用线性回归拟合曲面
from sklearn.linear_model import LinearRegression

# 准备训练数据
X_train = df[['播放量', '点赞数']].values
y_train = df['投币数'].values

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测曲面
Z = model.predict(np.c_[X.ravel(), Y.ravel()]).reshape(X.shape)

# 绘制曲面
surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.6, 
                       edgecolor='none', antialiased=True)

# 绘制实际数据点
ax.scatter(df['播放量'], df['点赞数'], df['投币数'], 
          c='black', s=20, alpha=0.3, label='实际数据')

ax.set_xlabel('播放量', fontsize=12, labelpad=10)
ax.set_ylabel('点赞数', fontsize=12, labelpad=10)
ax.set_zlabel('投币数', fontsize=12, labelpad=10)
ax.set_title('播放量-点赞数-投币数关系曲面', fontsize=16, fontweight='bold', pad=20)

# 添加颜色条
cbar = plt.colorbar(surf, ax=ax, pad=0.1, shrink=0.8)
cbar.set_label('投币数（预测）', fontsize=11)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('visualizations/08_三维曲面图.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/08_三维曲面图.png")
plt.close()

# ============================================================================
# 4. 三维线框图：数据分布
# ============================================================================
print("\n[5/5] 生成三维线框图...")

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 创建数据分布的网格
from scipy.stats import gaussian_kde

# 选择两个维度进行密度估计
x_data = df['播放量'].values
y_data = df['点赞数'].values

# 创建网格
x_grid = np.linspace(x_data.min(), x_data.max(), 30)
y_grid = np.linspace(y_data.min(), y_data.max(), 30)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

# 计算密度
positions = np.vstack([X_grid.ravel(), Y_grid.ravel()])
values = np.vstack([x_data, y_data])
kernel = gaussian_kde(values)
Z_grid = np.reshape(kernel(positions).T, X_grid.shape)

# 绘制线框图
wireframe = ax.plot_wireframe(X_grid, Y_grid, Z_grid, 
                              color='blue', alpha=0.6, linewidth=0.8)

# 绘制等高线投影
ax.contour(X_grid, Y_grid, Z_grid, zdir='z', offset=0, 
          cmap='viridis', alpha=0.5, linewidths=1)

ax.set_xlabel('播放量', fontsize=12, labelpad=10)
ax.set_ylabel('点赞数', fontsize=12, labelpad=10)
ax.set_zlabel('密度', fontsize=12, labelpad=10)
ax.set_title('播放量-点赞数分布密度图', fontsize=16, fontweight='bold', pad=20)

ax.view_init(elev=30, azim=45)

plt.tight_layout()
plt.savefig('visualizations/09_三维线框图.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/09_三维线框图.png")
plt.close()

# ============================================================================
# 5. 综合三维展示
# ============================================================================
print("\n[6/6] 生成综合三维展示...")

fig = plt.figure(figsize=(18, 12))

# 5.1 三维散点图（左上）
ax1 = fig.add_subplot(221, projection='3d')
scatter1 = ax1.scatter(df['播放量'], df['点赞数'], df['投币数'],
                      c=df['收藏数'], cmap='plasma', s=50, alpha=0.6)
ax1.set_xlabel('播放量', fontsize=10)
ax1.set_ylabel('点赞数', fontsize=10)
ax1.set_zlabel('投币数', fontsize=10)
ax1.set_title('数据分布', fontsize=12, fontweight='bold')
ax1.view_init(elev=20, azim=45)

# 5.2 分区对比（右上）
ax2 = fig.add_subplot(222, projection='3d')
for i, category in enumerate(categories):
    cat_df = df[df['排行榜分区'] == category]
    ax2.scatter(cat_df['播放量'], cat_df['点赞数'], cat_df['投币数'],
               label=category, s=50, alpha=0.6)
ax2.set_xlabel('播放量', fontsize=10)
ax2.set_ylabel('点赞数', fontsize=10)
ax2.set_zlabel('投币数', fontsize=10)
ax2.set_title('分区数据对比', fontsize=12, fontweight='bold')
ax2.legend(fontsize=8, loc='upper left')
ax2.view_init(elev=20, azim=45)

# 5.3 Top视频标注（左下）
ax3 = fig.add_subplot(223, projection='3d')
top10 = df.nlargest(10, '播放量')
ax3.scatter(df['播放量'], df['点赞数'], df['投币数'],
           c='lightgray', s=30, alpha=0.3)
ax3.scatter(top10['播放量'], top10['点赞数'], top10['投币数'],
           c='red', s=200, alpha=0.8, marker='*', edgecolors='black', linewidth=1)
ax3.set_xlabel('播放量', fontsize=10)
ax3.set_ylabel('点赞数', fontsize=10)
ax3.set_zlabel('投币数', fontsize=10)
ax3.set_title('Top 10 热门视频', fontsize=12, fontweight='bold')
ax3.view_init(elev=20, azim=45)

# 5.4 互动率三维展示（右下）
ax4 = fig.add_subplot(224, projection='3d')
scatter4 = ax4.scatter(df['点赞率'], df['投币率'], df['收藏率'],
                      c=df['播放量'], cmap='viridis', s=80, alpha=0.6,
                      edgecolors='black', linewidth=0.5)
ax4.set_xlabel('点赞率', fontsize=10)
ax4.set_ylabel('投币率', fontsize=10)
ax4.set_zlabel('收藏率', fontsize=10)
ax4.set_title('互动率关系（颜色=播放量）', fontsize=12, fontweight='bold')
ax4.view_init(elev=20, azim=45)

plt.suptitle('B站数据三维综合展示', fontsize=18, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('visualizations/10_三维综合展示.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/10_三维综合展示.png")
plt.close()

print("\n" + "=" * 70)
print("√ 三维可视化完成！")
print("=" * 70)
print("\n已生成图表:")
print("  6. 06_三维散点图.png")
print("  7. 07_三维柱状图.png")
print("  8. 08_三维曲面图.png")
print("  9. 09_三维线框图.png")
print("  10. 10_三维综合展示.png")
print("\n所有图表保存在 visualizations/ 目录")
