"""
高级可视化示例代码
包含：三维柱状图、三维折线图、三维散点图、阶梯图、局部放大图、多色填充图、桑基图
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# 设置中文字体（如果需要）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ==================== 三维柱状图 ====================
def create_3d_bar_chart():
    """创建三维柱状图"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 准备数据
    x = np.arange(5)
    y = np.arange(4)
    xpos, ypos = np.meshgrid(x, y)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros_like(xpos)
    
    # 柱子的高度（随机数据，实际使用时替换为真实数据）
    dz = np.random.rand(20) * 10
    
    # 柱子的宽度和深度
    dx = dy = 0.8
    
    # 根据高度设置颜色
    colors = plt.cm.viridis(dz / dz.max())
    
    # 绘制3D柱状图
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, alpha=0.8)
    
    # 设置标签和标题
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    ax.set_zlabel('Z轴（高度）', fontsize=12)
    ax.set_title('三维柱状图示例', fontsize=14, fontweight='bold')
    
    # 设置视角
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('3d_bar_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 三维折线图 ====================
def create_3d_line_chart():
    """创建三维折线图"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 准备数据（螺旋线示例）
    t = np.linspace(0, 4*np.pi, 100)
    x = np.sin(t)
    y = np.cos(t)
    z = t
    
    # 绘制3D折线图
    ax.plot(x, y, z, linewidth=2, color='blue', label='3D曲线')
    
    # 添加散点标记关键点
    key_points = [0, 25, 50, 75, 99]
    ax.scatter(x[key_points], y[key_points], z[key_points], 
               c='red', s=100, marker='o', label='关键点')
    
    # 设置标签和标题
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    ax.set_zlabel('Z轴（时间）', fontsize=12)
    ax.set_title('三维折线图示例', fontsize=14, fontweight='bold')
    ax.legend()
    
    # 设置视角
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('3d_line_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 三维散点图 ====================
def create_3d_scatter_chart():
    """创建三维散点图"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 准备数据
    np.random.seed(42)
    n = 100
    x = np.random.randn(n)
    y = np.random.randn(n)
    z = np.random.randn(n)
    colors = np.random.rand(n)
    sizes = 100 * np.random.rand(n)
    
    # 绘制3D散点图
    scatter = ax.scatter(x, y, z, c=colors, s=sizes, 
                        alpha=0.6, cmap='viridis', edgecolors='black', linewidth=0.5)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('颜色值', fontsize=12)
    
    # 设置标签和标题
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    ax.set_zlabel('Z轴', fontsize=12)
    ax.set_title('三维散点图示例', fontsize=14, fontweight='bold')
    
    # 设置视角
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('3d_scatter_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 三维曲面图 ====================
def create_3d_surface_chart():
    """创建三维曲面图"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 准备数据
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    # 绘制3D曲面图
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, 
                           linewidth=0, antialiased=True)
    
    # 添加等高线投影
    contour = ax.contour(X, Y, Z, zdir='z', offset=Z.min(), cmap='viridis', alpha=0.5)
    
    # 添加颜色条
    fig.colorbar(surf, ax=ax, pad=0.1, shrink=0.8)
    
    # 设置标签和标题
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    ax.set_zlabel('Z轴', fontsize=12)
    ax.set_title('三维曲面图示例', fontsize=14, fontweight='bold')
    
    # 设置视角
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.savefig('3d_surface_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 阶梯图 ====================
def create_step_plot():
    """创建阶梯图"""
    # 准备数据
    x = np.linspace(0, 10, 20)
    y = np.sin(x) + np.random.normal(0, 0.1, len(x))
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 默认阶梯图（post）
    axes[0, 0].step(x, y, where='post', linewidth=2, label='post')
    axes[0, 0].plot(x, y, 'o--', alpha=0.5, label='原始数据')
    axes[0, 0].set_title('阶梯图 (where="post")', fontsize=12, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. pre阶梯图
    axes[0, 1].step(x, y, where='pre', linewidth=2, color='green', label='pre')
    axes[0, 1].plot(x, y, 'o--', alpha=0.5, label='原始数据')
    axes[0, 1].set_title('阶梯图 (where="pre")', fontsize=12, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. mid阶梯图
    axes[1, 0].step(x, y, where='mid', linewidth=2, color='red', label='mid')
    axes[1, 0].plot(x, y, 'o--', alpha=0.5, label='原始数据')
    axes[1, 0].set_title('阶梯图 (where="mid")', fontsize=12, fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. 填充阶梯图
    axes[1, 1].step(x, y, where='post', linewidth=2, color='purple')
    axes[1, 1].fill_between(x, 0, y, step='post', alpha=0.3, color='purple')
    axes[1, 1].set_title('填充阶梯图', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('step_plots.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 局部放大图 ====================
def create_inset_plot():
    """创建带局部放大的图表"""
    # 准备数据
    x = np.linspace(0, 10, 1000)
    y = np.sin(x) + 0.1 * np.random.randn(len(x))
    
    # 创建主图
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, linewidth=1.5, color='blue', label='完整数据')
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    ax.set_title('带局部放大图的折线图', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 定义放大区域
    x1, x2 = 2, 4  # 放大区域范围
    y1, y2 = -0.5, 0.5
    
    # 创建局部放大图
    axins = inset_axes(ax, width="40%", height="30%", loc='upper right',
                       bbox_to_anchor=(0.5, 0.5, 1, 1), bbox_transform=ax.transAxes)
    
    # 在放大图中绘制数据
    axins.plot(x, y, linewidth=1.5, color='red')
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_xlabel('X (放大)', fontsize=10)
    axins.set_ylabel('Y (放大)', fontsize=10)
    axins.grid(True, alpha=0.3)
    
    # 标记放大区域
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", linestyle='--')
    
    # 在主图上标记放大区域
    ax.axvspan(x1, x2, alpha=0.2, color='yellow', label='放大区域')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('inset_plot.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 多色填充图 ====================
def create_multicolor_fill():
    """创建多色填充图"""
    # 准备数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x)
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 基础多色填充
    ax = axes[0, 0]
    ax.fill_between(x, 0, y1, alpha=0.5, color='blue', label='sin(x)')
    ax.fill_between(x, 0, y2, alpha=0.5, color='red', label='cos(x)')
    ax.plot(x, y1, 'b-', linewidth=2)
    ax.plot(x, y2, 'r-', linewidth=2)
    ax.set_title('基础多色填充', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 条件填充
    ax = axes[0, 1]
    ax.fill_between(x, y1, y2, where=(y1 > y2), alpha=0.5, color='green', label='y1 > y2')
    ax.fill_between(x, y1, y2, where=(y1 <= y2), alpha=0.5, color='orange', label='y1 <= y2')
    ax.plot(x, y1, 'b-', linewidth=2, label='y1')
    ax.plot(x, y2, 'r-', linewidth=2, label='y2')
    ax.set_title('条件多色填充', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. 渐变填充
    ax = axes[1, 0]
    for i in range(len(x)-1):
        ax.fill_between([x[i], x[i+1]], 0, y1[i:i+2], 
                        color=plt.cm.viridis(i/len(x)), alpha=0.7)
    ax.plot(x, y1, 'k-', linewidth=2)
    ax.set_title('渐变填充', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # 4. 堆叠多色填充
    ax = axes[1, 1]
    ax.fill_between(x, 0, y1, alpha=0.6, color='blue', label='sin(x)')
    ax.fill_between(x, y1, y1+y2, alpha=0.6, color='red', label='cos(x)')
    ax.fill_between(x, y1+y2, y1+y2+y3, alpha=0.6, color='green', label='sin(x)*cos(x)')
    ax.plot(x, y1, 'b-', linewidth=1)
    ax.plot(x, y1+y2, 'r-', linewidth=1)
    ax.plot(x, y1+y2+y3, 'g-', linewidth=1)
    ax.set_title('堆叠多色填充', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('multicolor_fill.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==================== 桑基图（使用Plotly） ====================
def create_sankey_diagram():
    """创建桑基图"""
    # 定义节点和连接
    labels = ['源1', '源2', '源3', '中间1', '中间2', '目标1', '目标2', '目标3']
    
    # 源节点索引
    source = [0, 0, 1, 1, 2, 3, 3, 4, 4]
    # 目标节点索引
    target = [3, 4, 3, 4, 4, 5, 6, 6, 7]
    # 流量值
    value = [8, 4, 2, 2, 6, 4, 6, 2, 8]
    
    # 节点颜色
    node_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                   '#F7DC6F', '#BB8FCE', '#85C1E2']
    
    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=['rgba(255,0,0,0.4)' if i < 3 else 'rgba(0,255,0,0.4)' 
                   for i in range(len(source))]
        )
    )])
    
    fig.update_layout(
        title_text="桑基图示例：数据流动可视化",
        font_size=14,
        width=1000,
        height=600
    )
    
    # 保存图片（需要安装kaleido）
    try:
        fig.write_image("sankey_diagram.png", width=1000, height=600, scale=3)
    except:
        print("提示：保存图片需要安装kaleido: pip install kaleido")
    
    fig.show()


# ==================== 复杂桑基图（多层级） ====================
def create_complex_sankey():
    """创建复杂多层级桑基图"""
    # 定义节点和连接
    labels = [
        # 第一层：能源来源
        '煤炭', '石油', '天然气', '核能', '可再生能源',
        # 第二层：转换过程
        '发电', '工业', '交通', '建筑',
        # 第三层：最终用途
        '电力', '热力', '动力'
    ]
    
    # 定义连接
    source = [
        # 能源来源 -> 转换过程
        0, 0, 0,  # 煤炭 -> 发电、工业、建筑
        1, 1,     # 石油 -> 工业、交通
        2, 2, 2,  # 天然气 -> 发电、工业、建筑
        3,        # 核能 -> 发电
        4, 4,     # 可再生能源 -> 发电、建筑
        # 转换过程 -> 最终用途
        5, 5,     # 发电 -> 电力、热力
        6, 6,     # 工业 -> 电力、热力
        7,        # 交通 -> 动力
        8, 8      # 建筑 -> 电力、热力
    ]
    
    target = [
        # 能源来源 -> 转换过程
        5, 6, 8,
        6, 7,
        5, 6, 8,
        5,
        5, 8,
        # 转换过程 -> 最终用途
        9, 10,
        9, 10,
        11,
        9, 10
    ]
    
    value = [
        # 能源来源 -> 转换过程
        30, 20, 10,
        15, 25,
        20, 15, 10,
        15,
        10, 5,
        # 转换过程 -> 最终用途
        50, 20,
        30, 20,
        25,
        15, 10
    ]
    
    # 节点颜色（按层级）
    node_colors = [
        '#FF6B6B', '#FF8E53', '#FFA07A', '#FFB347', '#FFD700',  # 能源来源
        '#4ECDC4', '#45B7D1', '#87CEEB', '#98D8C8',              # 转换过程
        '#90EE90', '#98FB98', '#ADFF2F'                          # 最终用途
    ]
    
    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="black", width=1),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(0,0,255,0.3)'
        )
    )])
    
    fig.update_layout(
        title_text="能源流动桑基图（多层级）",
        font_size=12,
        width=1200,
        height=700
    )
    
    # 保存图片
    try:
        fig.write_image("complex_sankey.png", width=1200, height=700, scale=3)
    except:
        print("提示：保存图片需要安装kaleido: pip install kaleido")
    
    fig.show()


# ==================== 主函数 ====================
if __name__ == "__main__":
    print("高级可视化示例代码")
    print("=" * 50)
    print("1. 三维柱状图")
    print("2. 三维折线图")
    print("3. 三维散点图")
    print("4. 三维曲面图")
    print("5. 阶梯图")
    print("6. 局部放大图")
    print("7. 多色填充图")
    print("8. 桑基图")
    print("9. 复杂桑基图")
    print("0. 运行所有示例")
    print("=" * 50)
    
    choice = input("请选择要运行的示例（输入数字）: ")
    
    if choice == "1":
        create_3d_bar_chart()
    elif choice == "2":
        create_3d_line_chart()
    elif choice == "3":
        create_3d_scatter_chart()
    elif choice == "4":
        create_3d_surface_chart()
    elif choice == "5":
        create_step_plot()
    elif choice == "6":
        create_inset_plot()
    elif choice == "7":
        create_multicolor_fill()
    elif choice == "8":
        create_sankey_diagram()
    elif choice == "9":
        create_complex_sankey()
    elif choice == "0":
        print("运行所有示例...")
        create_3d_bar_chart()
        create_3d_line_chart()
        create_3d_scatter_chart()
        create_3d_surface_chart()
        create_step_plot()
        create_inset_plot()
        create_multicolor_fill()
        create_sankey_diagram()
        create_complex_sankey()
        print("所有示例运行完成！")
    else:
        print("无效选择！")

