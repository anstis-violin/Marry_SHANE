"""
Day 4-5 - 任务4.2: ROC曲线和AUC可视化
包含: 二分类ROC曲线、多分类ROC曲线、模型对比
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.preprocessing import label_binarize
from itertools import cycle

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 4-5 - 任务4.2: ROC曲线和AUC可视化")
print("=" * 60)

# ============================================================================
# 1. 二分类ROC曲线
# ============================================================================
print("\n[1/3] 创建二分类ROC曲线...")

# 生成二分类数据
X_binary, y_binary = make_classification(n_samples=1000, n_features=20,
                                         n_informative=15, n_redundant=5,
                                         n_classes=2, random_state=42)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_binary, y_binary,
                                                    test_size=0.3, random_state=42)

# 训练模型
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 获取预测概率
y_scores = clf.predict_proba(X_test)[:, 1]

# 计算ROC曲线
fpr, tpr, thresholds = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制ROC曲线
ax.plot(fpr, tpr, color='darkorange', lw=2,
        label=f'ROC曲线 (AUC = {roc_auc:.3f})')

# 绘制对角线（随机分类器）
ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--',
        label='随机分类器 (AUC = 0.500)')

# 标记最优阈值点
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
ax.plot(fpr[optimal_idx], tpr[optimal_idx], 'ro', markersize=10,
        label=f'最优阈值 = {optimal_threshold:.3f}')

# 美化
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('假阳性率 (FPR)', fontsize=12)
ax.set_ylabel('真阳性率 (TPR)', fontsize=12)
ax.set_title('二分类ROC曲线', fontsize=16, fontweight='bold')
ax.legend(loc="lower right", fontsize=11)
ax.grid(True, alpha=0.3)

# 添加说明文本
info_text = f"""
模型性能指标:
• AUC: {roc_auc:.4f}
• 最优阈值: {optimal_threshold:.4f}
• 最优点TPR: {tpr[optimal_idx]:.4f}
• 最优点FPR: {fpr[optimal_idx]:.4f}
"""
ax.text(0.6, 0.2, info_text, fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_1_binary_roc.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_binary_roc.png")
print(f"  AUC = {roc_auc:.4f}")
plt.close()

# ============================================================================
# 2. 多分类ROC曲线（One-vs-Rest）
# ============================================================================
print("\n[2/3] 创建多分类ROC曲线...")

# 生成多分类数据（5个类别）
X_multi, y_multi = make_classification(n_samples=1000, n_features=20,
                                       n_informative=15, n_redundant=5,
                                       n_classes=5, n_clusters_per_class=1,
                                       random_state=42)

# 划分训练集和测试集
X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(X_multi, y_multi,
                                                            test_size=0.3, random_state=42)

# 二值化标签（One-vs-Rest）
y_test_bin = label_binarize(y_test_m, classes=[0, 1, 2, 3, 4])
n_classes = y_test_bin.shape[1]

# 训练模型
clf_multi = RandomForestClassifier(n_estimators=100, random_state=42)
clf_multi.fit(X_train_m, y_train_m)

# 获取预测概率
y_scores_multi = clf_multi.predict_proba(X_test_m)

# 计算每个类别的ROC曲线和AUC
fpr_dict = dict()
tpr_dict = dict()
roc_auc_dict = dict()

for i in range(n_classes):
    fpr_dict[i], tpr_dict[i], _ = roc_curve(y_test_bin[:, i], y_scores_multi[:, i])
    roc_auc_dict[i] = auc(fpr_dict[i], tpr_dict[i])

# 计算微平均ROC曲线和AUC
fpr_dict["micro"], tpr_dict["micro"], _ = roc_curve(y_test_bin.ravel(), y_scores_multi.ravel())
roc_auc_dict["micro"] = auc(fpr_dict["micro"], tpr_dict["micro"])

# 计算宏平均ROC曲线和AUC
all_fpr = np.unique(np.concatenate([fpr_dict[i] for i in range(n_classes)]))
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += np.interp(all_fpr, fpr_dict[i], tpr_dict[i])
mean_tpr /= n_classes
fpr_dict["macro"] = all_fpr
tpr_dict["macro"] = mean_tpr
roc_auc_dict["macro"] = auc(fpr_dict["macro"], tpr_dict["macro"])

# 创建图表
fig, ax = plt.subplots(figsize=(12, 9))

# 类别名称和颜色
class_names = ['类别A', '类别B', '类别C', '类别D', '类别E']
colors = cycle(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])

# 绘制每个类别的ROC曲线
for i, color, name in zip(range(n_classes), colors, class_names):
    ax.plot(fpr_dict[i], tpr_dict[i], color=color, lw=2,
            label=f'{name} (AUC = {roc_auc_dict[i]:.3f})')

# 绘制微平均ROC曲线
ax.plot(fpr_dict["micro"], tpr_dict["micro"],
        label=f'微平均 (AUC = {roc_auc_dict["micro"]:.3f})',
        color='deeppink', linestyle=':', linewidth=3)

# 绘制宏平均ROC曲线
ax.plot(fpr_dict["macro"], tpr_dict["macro"],
        label=f'宏平均 (AUC = {roc_auc_dict["macro"]:.3f})',
        color='navy', linestyle=':', linewidth=3)

# 绘制对角线
ax.plot([0, 1], [0, 1], 'k--', lw=2, label='随机分类器 (AUC = 0.500)')

# 美化
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('假阳性率 (FPR)', fontsize=12)
ax.set_ylabel('真阳性率 (TPR)', fontsize=12)
ax.set_title('多分类ROC曲线（One-vs-Rest）', fontsize=16, fontweight='bold')
ax.legend(loc="lower right", fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_2_multi_roc.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_multi_roc.png")
print(f"  微平均AUC = {roc_auc_dict['micro']:.4f}")
print(f"  宏平均AUC = {roc_auc_dict['macro']:.4f}")
plt.close()

# ============================================================================
# 3. 多模型ROC曲线对比
# ============================================================================
print("\n[3/3] 创建多模型ROC曲线对比...")

# 使用二分类数据
X_train, X_test, y_train, y_test = train_test_split(X_binary, y_binary,
                                                    test_size=0.3, random_state=42)

# 训练多个模型
models = {
    '随机森林': RandomForestClassifier(n_estimators=100, random_state=42),
    '梯度提升': GradientBoostingClassifier(n_estimators=100, random_state=42),
    '逻辑回归': LogisticRegression(random_state=42, max_iter=1000)
}

# 创建图表
fig, ax = plt.subplots(figsize=(12, 9))

# 颜色
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

# 训练模型并绘制ROC曲线
for (name, model), color in zip(models.items(), colors):
    print(f"\n训练 {name}...")
    model.fit(X_train, y_train)
    
    # 获取预测概率
    y_scores = model.predict_proba(X_test)[:, 1]
    
    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(y_test, y_scores)
    roc_auc = auc(fpr, tpr)
    
    # 绘制ROC曲线
    ax.plot(fpr, tpr, color=color, lw=2.5,
            label=f'{name} (AUC = {roc_auc:.3f})')
    
    print(f"  {name} AUC = {roc_auc:.4f}")

# 绘制对角线
ax.plot([0, 1], [0, 1], 'k--', lw=2, label='随机分类器 (AUC = 0.500)')

# 美化
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('假阳性率 (FPR)', fontsize=12)
ax.set_ylabel('真阳性率 (TPR)', fontsize=12)
ax.set_title('多模型ROC曲线对比', fontsize=16, fontweight='bold')
ax.legend(loc="lower right", fontsize=12)
ax.grid(True, alpha=0.3)

# 添加说明
info_text = """
💡 模型选择建议:
• AUC越接近1，模型性能越好
• AUC > 0.9: 优秀
• AUC 0.8-0.9: 良好
• AUC 0.7-0.8: 一般
• AUC < 0.7: 较差
"""
ax.text(0.55, 0.15, info_text, fontsize=10,
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_3_model_comparison_roc.png',
            dpi=300, bbox_inches='tight')
print("\n✓ 已保存: output_3_model_comparison_roc.png")
plt.close()

# ============================================================================
# 4. 详细的ROC分析
# ============================================================================
print("\n[4/4] 创建详细ROC分析...")

# 使用随机森林模型
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_scores = clf.predict_proba(X_test)[:, 1]

# 计算ROC曲线
fpr, tpr, thresholds = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

# 创建综合图表
fig = plt.figure(figsize=(16, 6))

# 4.1 ROC曲线（左）
ax1 = plt.subplot(131)
ax1.plot(fpr, tpr, color='darkorange', lw=2.5,
        label=f'ROC曲线 (AUC = {roc_auc:.3f})')
ax1.plot([0, 1], [0, 1], 'k--', lw=2)

# 标记几个关键点
key_indices = [len(thresholds)//4, len(thresholds)//2, 3*len(thresholds)//4]
for idx in key_indices:
    ax1.plot(fpr[idx], tpr[idx], 'ro', markersize=8)
    ax1.annotate(f'阈值={thresholds[idx]:.2f}',
                xy=(fpr[idx], tpr[idx]),
                xytext=(fpr[idx]+0.1, tpr[idx]-0.1),
                fontsize=8,
                arrowprops=dict(arrowstyle='->', color='red'))

ax1.set_xlim([0.0, 1.0])
ax1.set_ylim([0.0, 1.05])
ax1.set_xlabel('假阳性率 (FPR)', fontsize=11)
ax1.set_ylabel('真阳性率 (TPR)', fontsize=11)
ax1.set_title('ROC曲线与阈值', fontsize=13, fontweight='bold')
ax1.legend(loc="lower right")
ax1.grid(True, alpha=0.3)

# 4.2 阈值vs TPR/FPR（中）
ax2 = plt.subplot(132)
ax2.plot(thresholds, tpr[:-1], 'b-', label='TPR (真阳性率)', linewidth=2)
ax2.plot(thresholds, fpr[:-1], 'r-', label='FPR (假阳性率)', linewidth=2)
ax2.plot(thresholds, tpr[:-1] - fpr[:-1], 'g--', label='TPR - FPR', linewidth=2)

# 标记最优阈值
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
ax2.axvline(optimal_threshold, color='purple', linestyle=':', linewidth=2,
           label=f'最优阈值 = {optimal_threshold:.3f}')

ax2.set_xlabel('分类阈值', fontsize=11)
ax2.set_ylabel('比率', fontsize=11)
ax2.set_title('阈值对TPR/FPR的影响', fontsize=13, fontweight='bold')
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3)

# 4.3 预测概率分布（右）
ax3 = plt.subplot(133)
y_scores_0 = y_scores[y_test == 0]
y_scores_1 = y_scores[y_test == 1]

ax3.hist(y_scores_0, bins=30, alpha=0.6, color='blue', label='负类', density=True)
ax3.hist(y_scores_1, bins=30, alpha=0.6, color='red', label='正类', density=True)
ax3.axvline(optimal_threshold, color='green', linestyle='--', linewidth=2,
           label=f'最优阈值 = {optimal_threshold:.3f}')

ax3.set_xlabel('预测概率', fontsize=11)
ax3.set_ylabel('密度', fontsize=11)
ax3.set_title('预测概率分布', fontsize=13, fontweight='bold')
ax3.legend(loc='best')
ax3.grid(True, alpha=0.3, axis='y')

plt.suptitle('ROC曲线详细分析', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_4_detailed_roc_analysis.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_4_detailed_roc_analysis.png")
plt.close()

print("\n" + "=" * 60)
print("✅ Day 4-5 - 任务4.2 完成！")
print("已生成4个ROC曲线可视化:")
print("  1. output_1_binary_roc.png - 二分类ROC")
print("  2. output_2_multi_roc.png - 多分类ROC")
print("  3. output_3_model_comparison_roc.png - 模型对比")
print("  4. output_4_detailed_roc_analysis.png - 详细分析")
print("=" * 60)
