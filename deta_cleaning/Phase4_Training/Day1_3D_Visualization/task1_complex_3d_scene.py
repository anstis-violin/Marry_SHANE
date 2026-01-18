"""
Day 1 - 任务1.1: 复杂三维场景构建
包含: 多对象三维场景、三维路径、等高线、体绘制
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 1 - 任务1.1: 复杂三维场景构建")
print("=" * 60)

# ============================================================================
# 1. 多对象三维场景
# ============================================================================
print("\n[1/4] 创建多对象三维场景...")

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 1.1 绘制三维曲面
x_surf = np.linspace(-5, 5, 50)
y_surf = np.linspace(-5, 5, 50)
X_surf, Y_surf = np.meshgrid(x_surf, y_surf)
Z_surf = np.sin(np.sqrt(X_surf**2 + Y_surf**2))

surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', 
                       alpha=0.6, label='曲面')

# 1.2 添加三维散点
np.random.seed(42)
x_scatter = np.random.uniform(-5, 5, 100)
y_scatter = np.random.uniform(-5, 5, 100)
z_scatter = np.random.uniform(-2, 2, 100)
colors = np.random.uniform(0, 1, 100)

scatter = ax.scatter(x_scatter, y_scatter, z_scatter, 
                    c=colors, cmap='plasma', s=50, 
                    alpha=0.8, label='散点数据')

# 1.3 添加三维线框
x_wire = np.linspace(-5, 5, 20)
y_wire = np.linspace(-5, 5, 20)
X_wire, Y_wire = np.meshgrid(x_wire, y_wire)
Z_wire = -np.sin(np.sqrt(X_wire**2 + Y_wire**2)) - 1

wire = ax.plot_wireframe(X_wire, Y_wire, Z_wire, 
                         color='red', alpha=0.3, 
                         linewidth=0.5, label='线框')

# 1.4 添加三维柱状图
x_bar = np.array([3, 3, 4, 4])
y_bar = np.array([3, 4, 3, 4])
z_bar = np.zeros(4)
dx = dy = 0.3
dz = np.array([1.5, 2.0, 1.8, 2.2])

ax.bar3d(x_bar, y_bar, z_bar, dx, dy, dz, 
         color='orange', alpha=0.7, label='柱状图')

# 美化
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_zlabel('Z轴', fontsize=12)
ax.set_title('多对象三维场景示例', fontsize=16, fontweight='bold')
ax.legend(loc='upper left')
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('Day1_3D_Visualization/output_1_multi_object_scene.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_multi_object_scene.png")
plt.close()

# ============================================================================
# 2. 三维路径和轨迹
# ============================================================================
print("\n[2/4] 创建三维路径和轨迹...")

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 创建螺旋路径
t = np.linspace(0, 4*np.pi, 200)
x_path = np.cos(t) * (1 + 0.5*t)
y_path = np.sin(t) * (1 + 0.5*t)
z_path = t

# 绘制主路径
ax.plot(x_path, y_path, z_path, 'b-', linewidth=2, label='运动轨迹')

# 标记起点
ax.scatter([x_path[0]], [y_path[0]], [z_path[0]], 
          color='green', s=200, marker='o', label='起点')

# 标记终点
ax.scatter([x_path[-1]], [y_path[-1]], [z_path[-1]], 
          color='red', s=200, marker='s', label='终点')

# 标记关键点
key_points = [50, 100, 150]
for i in key_points:
    ax.scatter([x_path[i]], [y_path[i]], [z_path[i]], 
              color='orange', s=100, marker='*')

# 添加方向箭头（每隔20个点）
for i in range(0, len(t)-20, 20):
    dx = x_path[i+10] - x_path[i]
    dy = y_path[i+10] - y_path[i]
    dz = z_path[i+10] - z_path[i]
    ax.quiver(x_path[i], y_path[i], z_path[i], 
             dx, dy, dz, 
             color='purple', alpha=0.5, arrow_length_ratio=0.3)

# 美化
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_zlabel('Z轴 (时间)', fontsize=12)
ax.set_title('三维运动轨迹示例', fontsize=16, fontweight='bold')
ax.legend(loc='upper left')
ax.view_init(elev=25, azim=45)

plt.tight_layout()
plt.savefig('Day1_3D_Visualization/output_2_3d_path.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_3d_path.png")
plt.close()

# ============================================================================
# 3. 三维等高线和向量场
# ============================================================================
print("\n[3/4] 创建三维等高线和向量场...")

fig = plt.figure(figsize=(14, 6))

# 3.1 三维等高线
ax1 = fig.add_subplot(121, projection='3d')

x_contour = np.linspace(-3, 3, 50)
y_contour = np.linspace(-3, 3, 50)
X_contour, Y_contour = np.meshgrid(x_contour, y_contour)
Z_contour = np.exp(-(X_contour**2 + Y_contour**2))

# 绘制等高线
contour = ax1.contour3D(X_contour, Y_contour, Z_contour, 50, 
                        cmap='coolwarm', alpha=0.8)
fig.colorbar(contour, ax=ax1, shrink=0.5, aspect=5)

ax1.set_xlabel('X轴')
ax1.set_ylabel('Y轴')
ax1.set_zlabel('Z轴')
ax1.set_title('三维等高线图', fontsize=14, fontweight='bold')
ax1.view_init(elev=30, azim=45)

# 3.2 三维向量场
ax2 = fig.add_subplot(122, projection='3d')

x_vec = np.linspace(-2, 2, 5)
y_vec = np.linspace(-2, 2, 5)
z_vec = np.linspace(-2, 2, 5)
X_vec, Y_vec, Z_vec = np.meshgrid(x_vec, y_vec, z_vec)

# 计算向量场（简单的旋转场）
U = -Y_vec
V = X_vec
W = Z_vec * 0.5

# 绘制向量场
ax2.quiver(X_vec, Y_vec, Z_vec, U, V, W, 
          length=0.3, normalize=True, 
          color='blue', alpha=0.6)

ax2.set_xlabel('X轴')
ax2.set_ylabel('Y轴')
ax2.set_zlabel('Z轴')
ax2.set_title('三维向量场', fontsize=14, fontweight='bold')
ax2.view_init(elev=25, azim=45)

plt.tight_layout()
plt.savefig('Day1_3D_Visualization/output_3_contour_vector.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_3_contour_vector.png")
plt.close()

# ============================================================================
# 4. 三维体绘制（Voxel）
# ============================================================================
print("\n[4/4] 创建三维体绘制...")

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 创建体素数据
n = 8
x, y, z = np.indices((n, n, n))

# 创建球体
center = n // 2
radius = 2.5
sphere = (x - center)**2 + (y - center)**2 + (z - center)**2 < radius**2

# 创建立方体
cube = (x >= 1) & (x <= 3) & (y >= 5) & (y <= 7) & (z >= 1) & (z <= 3)

# 组合形状
voxels = sphere | cube

# 设置颜色
colors = np.empty(voxels.shape, dtype=object)
colors[sphere] = 'blue'
colors[cube] = 'red'
colors[sphere & cube] = 'purple'

# 绘制体素
ax.voxels(voxels, facecolors=colors, edgecolor='k', alpha=0.7)

ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')
ax.set_title('三维体绘制示例（球体+立方体）', fontsize=16, fontweight='bold')
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('Day1_3D_Visualization/output_4_voxel.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_4_voxel.png")
plt.close()

print("\n" + "=" * 60)
print("✅ Day 1 - 任务1.1 完成！")
print("已生成4个三维可视化图表:")
print("  1. output_1_multi_object_scene.png - 多对象三维场景")
print("  2. output_2_3d_path.png - 三维路径和轨迹")
print("  3. output_3_contour_vector.png - 等高线和向量场")
print("  4. output_4_voxel.png - 三维体绘制")
print("=" * 60)
