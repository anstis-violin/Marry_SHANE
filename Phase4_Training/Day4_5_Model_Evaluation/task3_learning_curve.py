"""
Day 4-5 - 任务4.3: 学习曲线可视化
包含: 训练样本数学习曲线、训练迭代学习曲线
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 4-5 - 任务4.3: 学习曲线可视化")
print("=" * 60)

# ============================================================================
# 1. 训练样本数学习曲线
# ============================================================================
print("\n[1/3] 创建训练样本数学习曲线...")

# 生成数据
X, y = make_classification(n_samples=2000, n_features=20,
                          n_informative=15, n_redundant=5,
                          n_classes=2, random_state=42)

# 训练模型并计算学习曲线
train_sizes = np.linspace(0.1, 1.0, 10)
train_sizes_abs, train_scores, val_scores = learning_curve(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X, y,
    train_sizes=train_sizes,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

# 计算均值和标准差
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
val_mean = np.mean(val_scores, axis=1)
val_std = np.std(val_scores, axis=1)

# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制训练集性能
ax.plot(train_sizes_abs, train_mean, 'o-', color='#FF6B6B', 
        linewidth=2.5, markersize=8, label='训练集准确率')
ax.fill_between(train_sizes_abs, 
                train_mean - train_std,
                train_mean + train_std,
                alpha=0.2, color='#FF6B6B')

# 绘制验证集性能
ax.plot(train_sizes_abs, val_mean, 'o-', color='#4ECDC4',
        linewidth=2.5, markersize=8, label='验证集准确率')
ax.fill_between(train_sizes_abs,
                val_mean - val_std,
                val_mean + val_std,
                alpha=0.2, color='#4ECDC4')

# 美化
ax.set_xlabel('训练样本数量', fontsize=12)
ax.set_ylabel('准确率', fontsize=12)
ax.set_title('学习曲线 - 训练样本数量的影响', fontsize=16, fontweight='bold')
ax.legend(loc='lower right', fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_ylim([0.5, 1.05])

# 添加分析文本
gap = train_mean[-1] - val_mean[-1]
if gap > 0.1:
    diagnosis = "过拟合：训练集性能远高于验证集"
    suggestion = "建议：增加训练数据或使用正则化"
elif val_mean[-1] < 0.8:
    diagnosis = "欠拟合：两者性能都较低"
    suggestion = "建议：使用更复杂的模型或增加特征"
else:
    diagnosis = "良好拟合：模型性能稳定"
    suggestion = "建议：当前模型表现良好"

info_text = f"""
模型诊断:
• {diagnosis}
• 训练集准确率: {train_mean[-1]:.4f}
• 验证集准确率: {val_mean[-1]:.4f}
• 性能差距: {gap:.4f}

{suggestion}
"""
ax.text(0.05, 0.95, info_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_1_learning_curve_samples.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_learning_curve_samples.png")
print(f"  训练集准确率: {train_mean[-1]:.4f}")
print(f"  验证集准确率: {val_mean[-1]:.4f}")
plt.close()

# ============================================================================
# 2. 训练迭代学习曲线（梯度提升）
# ============================================================================
print("\n[2/3] 创建训练迭代学习曲线...")

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练梯度提升模型，记录每次迭代的性能
n_estimators = 200
train_scores_iter = []
test_scores_iter = []

print("训练梯度提升模型...")
clf = GradientBoostingClassifier(n_estimators=n_estimators, 
                                learning_rate=0.1,
                                max_depth=3,
                                random_state=42,
                                warm_start=True)

for i in range(1, n_estimators + 1):
    clf.n_estimators = i
    clf.fit(X_train, y_train)
    
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    
    train_scores_iter.append(train_score)
    test_scores_iter.append(test_score)
    
    if i % 50 == 0:
        print(f"  迭代 {i}/{n_estimators}: 训练={train_score:.4f}, 测试={test_score:.4f}")

# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))

iterations = range(1, n_estimators + 1)

# 绘制训练集性能
ax.plot(iterations, train_scores_iter, '-', color='#FF6B6B',
        linewidth=2, label='训练集准确率')

# 绘制测试集性能
ax.plot(iterations, test_scores_iter, '-', color='#4ECDC4',
        linewidth=2, label='测试集准确率')

# 标记最佳迭代次数
best_iter = np.argmax(test_scores_iter) + 1
best_score = test_scores_iter[best_iter - 1]
ax.axvline(best_iter, color='green', linestyle='--', linewidth=2,
          label=f'最佳迭代次数 = {best_iter}')
ax.plot(best_iter, best_score, 'go', markersize=12)

# 美化
ax.set_xlabel('迭代次数（树的数量）', fontsize=12)
ax.set_ylabel('准确率', fontsize=12)
ax.set_title('学习曲线 - 训练迭代次数的影响（梯度提升）', fontsize=16, fontweight='bold')
ax.legend(loc='lower right', fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_ylim([0.5, 1.05])

# 添加分析文本
final_train = train_scores_iter[-1]
final_test = test_scores_iter[-1]
overfitting_start = 0

# 检测过拟合开始的位置
for i in range(len(test_scores_iter) - 1):
    if test_scores_iter[i+1] < test_scores_iter[i]:
        overfitting_start = i + 1
        break

info_text = f"""
训练分析:
• 最佳迭代次数: {best_iter}
• 最佳测试准确率: {best_score:.4f}
• 最终训练准确率: {final_train:.4f}
• 最终测试准确率: {final_test:.4f}

"""

if overfitting_start > 0:
    info_text += f"⚠️ 过拟合开始于第 {overfitting_start} 次迭代\n建议：使用早停法或减少迭代次数"
else:
    info_text += "✓ 模型训练稳定，未出现明显过拟合"

ax.text(0.05, 0.95, info_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_2_learning_curve_iterations.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_learning_curve_iterations.png")
print(f"  最佳迭代次数: {best_iter}")
print(f"  最佳测试准确率: {best_score:.4f}")
plt.close()

# ============================================================================
# 3. 多模型学习曲线对比
# ============================================================================
print("\n[3/3] 创建多模型学习曲线对比...")

# 定义多个模型
models = {
    '随机森林': RandomForestClassifier(n_estimators=100, random_state=42),
    '梯度提升': GradientBoostingClassifier(n_estimators=100, random_state=42),
    '逻辑回归': LogisticRegression(random_state=42, max_iter=1000)
}

# 创建图表
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

for idx, ((name, model), color) in enumerate(zip(models.items(), colors)):
    print(f"\n计算 {name} 的学习曲线...")
    
    # 计算学习曲线
    train_sizes_abs, train_scores, val_scores = learning_curve(
        model, X, y,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        random_state=42
    )
    
    # 计算均值和标准差
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    # 绘制
    ax = axes[idx]
    
    ax.plot(train_sizes_abs, train_mean, 'o-', color=color,
            linewidth=2, markersize=6, label='训练集', alpha=0.8)
    ax.fill_between(train_sizes_abs,
                    train_mean - train_std,
                    train_mean + train_std,
                    alpha=0.15, color=color)
    
    ax.plot(train_sizes_abs, val_mean, 's-', color=color,
            linewidth=2, markersize=6, label='验证集', linestyle='--')
    ax.fill_between(train_sizes_abs,
                    val_mean - val_std,
                    val_mean + val_std,
                    alpha=0.15, color=color)
    
    # 美化
    ax.set_xlabel('训练样本数量', fontsize=11)
    ax.set_ylabel('准确率', fontsize=11)
    ax.set_title(f'{name}', fontsize=13, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0.5, 1.05])
    
    # 添加最终性能
    final_val = val_mean[-1]
    ax.text(0.05, 0.95, f'验证集准确率:\n{final_val:.4f}',
            transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    print(f"  {name} 验证集准确率: {final_val:.4f}")

plt.suptitle('多模型学习曲线对比', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_3_multi_model_learning_curves.png',
            dpi=300, bbox_inches='tight')
print("\n✓ 已保存: output_3_multi_model_learning_curves.png")
plt.close()

# ============================================================================
# 4. 综合学习曲线分析
# ============================================================================
print("\n[4/4] 创建综合学习曲线分析...")

# 使用随机森林模型
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 计算学习曲线
train_sizes_abs, train_scores, val_scores = learning_curve(
    model, X, y,
    train_sizes=np.linspace(0.1, 1.0, 15),
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
val_mean = np.mean(val_scores, axis=1)
val_std = np.std(val_scores, axis=1)

# 创建综合图表
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# 4.1 学习曲线（左上）
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(train_sizes_abs, train_mean, 'o-', color='#FF6B6B',
        linewidth=2.5, markersize=8, label='训练集准确率')
ax1.fill_between(train_sizes_abs,
                train_mean - train_std,
                train_mean + train_std,
                alpha=0.2, color='#FF6B6B')

ax1.plot(train_sizes_abs, val_mean, 'o-', color='#4ECDC4',
        linewidth=2.5, markersize=8, label='验证集准确率')
ax1.fill_between(train_sizes_abs,
                val_mean - val_std,
                val_mean + val_std,
                alpha=0.2, color='#4ECDC4')

ax1.set_xlabel('训练样本数量', fontsize=12)
ax1.set_ylabel('准确率', fontsize=12)
ax1.set_title('学习曲线', fontsize=14, fontweight='bold')
ax1.legend(loc='lower right', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0.5, 1.05])

# 4.2 性能差距分析（左下）
ax2 = fig.add_subplot(gs[1, 0])
gap = train_mean - val_mean
ax2.plot(train_sizes_abs, gap, 'o-', color='purple', linewidth=2, markersize=6)
ax2.axhline(y=0.1, color='red', linestyle='--', label='过拟合阈值 (0.1)')
ax2.fill_between(train_sizes_abs, 0, gap, alpha=0.3, color='purple')

ax2.set_xlabel('训练样本数量', fontsize=11)
ax2.set_ylabel('性能差距（训练-验证）', fontsize=11)
ax2.set_title('过拟合程度分析', fontsize=13, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)

# 4.3 方差分析（右下）
ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(train_sizes_abs, train_std, 'o-', color='#FF6B6B',
        linewidth=2, markersize=6, label='训练集标准差')
ax3.plot(train_sizes_abs, val_std, 'o-', color='#4ECDC4',
        linewidth=2, markersize=6, label='验证集标准差')

ax3.set_xlabel('训练样本数量', fontsize=11)
ax3.set_ylabel('标准差', fontsize=11)
ax3.set_title('模型稳定性分析', fontsize=13, fontweight='bold')
ax3.legend(loc='upper right', fontsize=10)
ax3.grid(True, alpha=0.3)

plt.suptitle('学习曲线综合分析', fontsize=16, fontweight='bold', y=0.995)
plt.savefig('Day4_5_Model_Evaluation/output_4_comprehensive_learning_analysis.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_4_comprehensive_learning_analysis.png")
plt.close()

print("\n" + "=" * 60)
print("✅ Day 4-5 - 任务4.3 完成！")
print("已生成4个学习曲线可视化:")
print("  1. output_1_learning_curve_samples.png - 训练样本数影响")
print("  2. output_2_learning_curve_iterations.png - 迭代次数影响")
print("  3. output_3_multi_model_learning_curves.png - 多模型对比")
print("  4. output_4_comprehensive_learning_analysis.png - 综合分析")
print("=" * 60)
