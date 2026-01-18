"""
B站数据二维可视化
生成各种二维图表分析B站热门视频数据
"""

import sys
import io

# 解决Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100

print("=" * 70)
print("B站数据二维可视化")
print("=" * 70)

# 创建输出目录
os.makedirs('visualizations', exist_ok=True)

# 读取数据
print("\n[1/8] 读取数据...")
try:
    df = pd.read_csv('data/bilibili_data.csv', encoding='utf-8-sig')
    print(f"  √ 成功读取 {len(df)} 条数据")
except FileNotFoundError:
    print("  × 错误: 找不到数据文件！")
    print("  请先运行 crawler.py 爬取数据")
    exit(1)

# ============================================================================
# 1. 播放量分布图
# ============================================================================
print("\n[2/8] 生成播放量分布图...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1.1 播放量直方图
axes[0, 0].hist(df['播放量'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('播放量', fontsize=12)
axes[0, 0].set_ylabel('视频数量', fontsize=12)
axes[0, 0].set_title('播放量分布直方图', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# 1.2 播放量箱线图（按分区）
df.boxplot(column='播放量', by='排行榜分区', ax=axes[0, 1])
axes[0, 1].set_xlabel('分区', fontsize=12)
axes[0, 1].set_ylabel('播放量', fontsize=12)
axes[0, 1].set_title('各分区播放量分布', fontsize=14, fontweight='bold')
plt.sca(axes[0, 1])
plt.xticks(rotation=45)

# 1.3 Top 20 视频播放量
top20 = df.nlargest(20, '播放量')
axes[1, 0].barh(range(20), top20['播放量'].values, color='coral')
axes[1, 0].set_yticks(range(20))
axes[1, 0].set_yticklabels([title[:15]+'...' if len(title)>15 else title 
                            for title in top20['标题'].values], fontsize=9)
axes[1, 0].set_xlabel('播放量', fontsize=12)
axes[1, 0].set_title('Top 20 热门视频', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3, axis='x')

# 1.4 分区播放量占比
category_views = df.groupby('排行榜分区')['播放量'].sum()
colors = plt.cm.Set3(range(len(category_views)))
axes[1, 1].pie(category_views.values, labels=category_views.index, autopct='%1.1f%%',
              colors=colors, startangle=90)
axes[1, 1].set_title('各分区播放量占比', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/01_播放量分析.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/01_播放量分析.png")
plt.close()

# ============================================================================
# 2. 互动数据分析
# ============================================================================
print("\n[3/8] 生成互动数据分析图...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2.1 点赞数 vs 播放量
axes[0, 0].scatter(df['播放量'], df['点赞数'], alpha=0.5, c=df['投币数'], 
                  cmap='viridis', s=50)
axes[0, 0].set_xlabel('播放量', fontsize=12)
axes[0, 0].set_ylabel('点赞数', fontsize=12)
axes[0, 0].set_title('播放量 vs 点赞数', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# 2.2 互动率对比
interaction_data = df[['点赞率', '投币率', '收藏率']].mean()
bars = axes[0, 1].bar(interaction_data.index, interaction_data.values, 
                     color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
axes[0, 1].set_ylabel('平均比率', fontsize=12)
axes[0, 1].set_title('平均互动率对比', fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2%}', ha='center', va='bottom', fontsize=11)

# 2.3 各分区互动数据
category_interaction = df.groupby('排行榜分区')[['点赞数', '投币数', '收藏数']].sum()
category_interaction.plot(kind='bar', ax=axes[1, 0], width=0.8)
axes[1, 0].set_xlabel('分区', fontsize=12)
axes[1, 0].set_ylabel('数量', fontsize=12)
axes[1, 0].set_title('各分区互动数据对比', fontsize=14, fontweight='bold')
axes[1, 0].legend(['点赞数', '投币数', '收藏数'], fontsize=10)
axes[1, 0].grid(True, alpha=0.3, axis='y')
plt.sca(axes[1, 0])
plt.xticks(rotation=45)

# 2.4 热力图：互动指标相关性
correlation_data = df[['播放量', '点赞数', '投币数', '收藏数', '弹幕数']].corr()
sns.heatmap(correlation_data, annot=True, fmt='.2f', cmap='coolwarm', 
           ax=axes[1, 1], cbar_kws={'label': '相关系数'})
axes[1, 1].set_title('互动指标相关性热力图', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/02_互动数据分析.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/02_互动数据分析.png")
plt.close()

# ============================================================================
# 3. UP主分析
# ============================================================================
print("\n[4/8] 生成UP主分析图...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 3.1 Top 15 UP主（按视频数量）
top_uploader = df['UP主'].value_counts().head(15)
axes[0, 0].barh(range(15), top_uploader.values, color='lightgreen')
axes[0, 0].set_yticks(range(15))
axes[0, 0].set_yticklabels(top_uploader.index, fontsize=10)
axes[0, 0].set_xlabel('视频数量', fontsize=12)
axes[0, 0].set_title('Top 15 高产UP主', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3, axis='x')

# 3.2 Top 15 UP主（按总播放量）
uploader_views = df.groupby('UP主')['播放量'].sum().nlargest(15)
axes[0, 1].barh(range(15), uploader_views.values, color='salmon')
axes[0, 1].set_yticks(range(15))
axes[0, 1].set_yticklabels(uploader_views.index, fontsize=10)
axes[0, 1].set_xlabel('总播放量', fontsize=12)
axes[0, 1].set_title('Top 15 热门UP主（按播放量）', fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 3.3 UP主平均播放量分布
uploader_avg = df.groupby('UP主')['播放量'].mean()
axes[1, 0].hist(uploader_avg, bins=30, color='plum', edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('平均播放量', fontsize=12)
axes[1, 0].set_ylabel('UP主数量', fontsize=12)
axes[1, 0].set_title('UP主平均播放量分布', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 3.4 UP主视频数量分布
video_counts = df['UP主'].value_counts()
axes[1, 1].hist(video_counts, bins=20, color='gold', edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('视频数量', fontsize=12)
axes[1, 1].set_ylabel('UP主数量', fontsize=12)
axes[1, 1].set_title('UP主视频数量分布', fontsize=14, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/03_UP主分析.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/03_UP主分析.png")
plt.close()

# ============================================================================
# 4. 分区对比雷达图
# ============================================================================
print("\n[5/8] 生成分区对比雷达图...")

# 计算各分区的平均指标
category_stats = df.groupby('排行榜分区').agg({
    '播放量': 'mean',
    '点赞数': 'mean',
    '投币数': 'mean',
    '收藏数': 'mean',
    '弹幕数': 'mean'
}).reset_index()

# 归一化
for col in ['播放量', '点赞数', '投币数', '收藏数', '弹幕数']:
    max_val = category_stats[col].max()
    if max_val > 0:
        category_stats[col] = category_stats[col] / max_val

# 创建雷达图
categories = ['播放量', '点赞数', '投币数', '收藏数', '弹幕数']
n_cats = len(categories)

angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

for idx, (_, row) in enumerate(category_stats.iterrows()):
    values = [row[cat] for cat in categories]
    values += values[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, label=row['排行榜分区'], 
           color=colors[idx % len(colors)], markersize=8)
    ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylim(0, 1)
ax.set_title('各分区数据对比雷达图', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('visualizations/04_分区雷达图.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/04_分区雷达图.png")
plt.close()

# ============================================================================
# 5. 综合仪表盘
# ============================================================================
print("\n[6/8] 生成综合仪表盘...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 5.1 总体统计
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
stats_text = f"""
总体数据统计
{'='*30}

视频总数: {len(df):,}
总播放量: {df['播放量'].sum():,}
总点赞数: {df['点赞数'].sum():,}
总投币数: {df['投币数'].sum():,}
总收藏数: {df['收藏数'].sum():,}

平均播放量: {df['播放量'].mean():.0f}
平均点赞率: {df['点赞率'].mean():.2%}
平均投币率: {df['投币率'].mean():.2%}
"""
ax1.text(0.1, 0.9, stats_text, fontsize=11, verticalalignment='top',
        fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 5.2 分区视频数量
ax2 = fig.add_subplot(gs[0, 1:])
category_counts = df['排行榜分区'].value_counts()
bars = ax2.bar(category_counts.index, category_counts.values, color='skyblue', edgecolor='black')
ax2.set_ylabel('视频数量', fontsize=11)
ax2.set_title('各分区视频数量', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=10)

# 5.3 播放量Top 10
ax3 = fig.add_subplot(gs[1, :])
top10 = df.nlargest(10, '播放量')
x = range(10)
width = 0.25
ax3.bar([i-width for i in x], top10['播放量'].values, width, label='播放量', color='#FF6B6B')
ax3.bar(x, top10['点赞数'].values, width, label='点赞数', color='#4ECDC4')
ax3.bar([i+width for i in x], top10['投币数'].values, width, label='投币数', color='#45B7D1')
ax3.set_xticks(x)
ax3.set_xticklabels([title[:10]+'...' for title in top10['标题'].values], rotation=45, ha='right', fontsize=9)
ax3.set_ylabel('数量', fontsize=11)
ax3.set_title('Top 10 热门视频数据对比', fontsize=13, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, axis='y')

# 5.4 互动率分布
ax4 = fig.add_subplot(gs[2, 0])
ax4.violinplot([df['点赞率'], df['投币率'], df['收藏率']], 
              positions=[1, 2, 3], showmeans=True)
ax4.set_xticks([1, 2, 3])
ax4.set_xticklabels(['点赞率', '投币率', '收藏率'])
ax4.set_ylabel('比率', fontsize=11)
ax4.set_title('互动率分布', fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# 5.5 时长分布
ax5 = fig.add_subplot(gs[2, 1])
ax5.hist(df['时长分钟'], bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
ax5.set_xlabel('时长（分钟）', fontsize=11)
ax5.set_ylabel('视频数量', fontsize=11)
ax5.set_title('视频时长分布', fontsize=13, fontweight='bold')
ax5.grid(True, alpha=0.3)

# 5.6 分区平均播放量
ax6 = fig.add_subplot(gs[2, 2])
category_avg = df.groupby('排行榜分区')['播放量'].mean().sort_values(ascending=True)
ax6.barh(range(len(category_avg)), category_avg.values, color='lightgreen')
ax6.set_yticks(range(len(category_avg)))
ax6.set_yticklabels(category_avg.index, fontsize=10)
ax6.set_xlabel('平均播放量', fontsize=11)
ax6.set_title('各分区平均播放量', fontsize=13, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='x')

plt.suptitle('B站热门视频综合数据仪表盘', fontsize=18, fontweight='bold', y=0.995)
plt.savefig('visualizations/05_综合仪表盘.png', dpi=300, bbox_inches='tight')
print("  √ 已保存: visualizations/05_综合仪表盘.png")
plt.close()

print("\n" + "=" * 70)
print("√ 二维可视化完成！")
print("=" * 70)
print("\n已生成图表:")
print("  1. 01_播放量分析.png")
print("  2. 02_互动数据分析.png")
print("  3. 03_UP主分析.png")
print("  4. 04_分区雷达图.png")
print("  5. 05_综合仪表盘.png")
print("\n所有图表保存在 visualizations/ 目录")
