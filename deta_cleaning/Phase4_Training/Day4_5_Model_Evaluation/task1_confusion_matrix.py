"""
Day 4-5 - 任务4.1: 混淆矩阵可视化
包含: 二分类和多分类混淆矩阵、归一化混淆矩阵
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 4-5 - 任务4.1: 混淆矩阵可视化")
print("=" * 60)

# ============================================================================
# 1. 二分类混淆矩阵
# ============================================================================
print("\n[1/3] 创建二分类混淆矩阵...")

# 生成二分类数据
X_binary, y_binary = make_classification(n_samples=1000, n_features=20, 
                                         n_informative=15, n_redundant=5,
                                         n_classes=2, random_state=42)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_binary, y_binary, 
                                                    test_size=0.3, random_state=42)

# 训练模型
clf_binary = RandomForestClassifier(n_estimators=100, random_state=42)
clf_binary.fit(X_train, y_train)

# 预测
y_pred = clf_binary.predict(X_test)

# 计算混淆矩阵
cm = confusion_matrix(y_test, y_pred)

# 创建图表
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 1.1 绝对数量混淆矩阵
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['负类', '正类'],
            yticklabels=['负类', '正类'],
            cbar_kws={'label': '样本数量'},
            ax=axes[0])
axes[0].set_xlabel('预测标签', fontsize=12)
axes[0].set_ylabel('真实标签', fontsize=12)
axes[0].set_title('二分类混淆矩阵（绝对数量）', fontsize=14, fontweight='bold')

# 添加性能指标
tn, fp, fn, tp = cm.ravel()
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * (precision * recall) / (precision + recall)

metrics_text = f'准确率: {accuracy:.3f}\n精确率: {precision:.3f}\n召回率: {recall:.3f}\nF1分数: {f1:.3f}'
axes[0].text(2.5, 0.5, metrics_text, fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 1.2 归一化混淆矩阵（百分比）
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_normalized, annot=True, fmt='.2%', cmap='Greens',
            xticklabels=['负类', '正类'],
            yticklabels=['负类', '正类'],
            cbar_kws={'label': '比例'},
            ax=axes[1])
axes[1].set_xlabel('预测标签', fontsize=12)
axes[1].set_ylabel('真实标签', fontsize=12)
axes[1].set_title('二分类混淆矩阵（归一化）', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_1_binary_confusion_matrix.png', 
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_binary_confusion_matrix.png")
plt.close()

# 打印分类报告
print("\n二分类模型性能报告:")
print(classification_report(y_test, y_pred, target_names=['负类', '正类']))

# ============================================================================
# 2. 多分类混淆矩阵
# ============================================================================
print("\n[2/3] 创建多分类混淆矩阵...")

# 生成多分类数据（5个类别）
X_multi, y_multi = make_classification(n_samples=1000, n_features=20,
                                       n_informative=15, n_redundant=5,
                                       n_classes=5, n_clusters_per_class=1,
                                       random_state=42)

# 划分训练集和测试集
X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(X_multi, y_multi,
                                                            test_size=0.3, random_state=42)

# 训练模型
clf_multi = RandomForestClassifier(n_estimators=100, random_state=42)
clf_multi.fit(X_train_m, y_train_m)

# 预测
y_pred_m = clf_multi.predict(X_test_m)

# 计算混淆矩阵
cm_multi = confusion_matrix(y_test_m, y_pred_m)

# 类别名称
class_names = ['类别A', '类别B', '类别C', '类别D', '类别E']

# 创建图表
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 2.1 绝对数量混淆矩阵
sns.heatmap(cm_multi, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            cbar_kws={'label': '样本数量'},
            ax=axes[0])
axes[0].set_xlabel('预测标签', fontsize=12)
axes[0].set_ylabel('真实标签', fontsize=12)
axes[0].set_title('多分类混淆矩阵（绝对数量）', fontsize=14, fontweight='bold')

# 2.2 归一化混淆矩阵
cm_multi_normalized = cm_multi.astype('float') / cm_multi.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_multi_normalized, annot=True, fmt='.2%', cmap='Greens',
            xticklabels=class_names,
            yticklabels=class_names,
            cbar_kws={'label': '比例'},
            ax=axes[1])
axes[1].set_xlabel('预测标签', fontsize=12)
axes[1].set_ylabel('真实标签', fontsize=12)
axes[1].set_title('多分类混淆矩阵（归一化）', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_2_multi_confusion_matrix.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_multi_confusion_matrix.png")
plt.close()

# 打印分类报告
print("\n多分类模型性能报告:")
print(classification_report(y_test_m, y_pred_m, target_names=class_names))

# ============================================================================
# 3. 详细的多分类性能分析
# ============================================================================
print("\n[3/3] 创建详细性能分析...")

# 计算每个类别的性能指标
from sklearn.metrics import precision_recall_fscore_support

precision, recall, f1, support = precision_recall_fscore_support(y_test_m, y_pred_m)

# 创建综合图表
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# 3.1 混淆矩阵（左上）
ax1 = fig.add_subplot(gs[0, 0])
sns.heatmap(cm_multi, annot=True, fmt='d', cmap='YlOrRd',
            xticklabels=class_names,
            yticklabels=class_names,
            cbar_kws={'label': '样本数量'},
            ax=ax1)
ax1.set_xlabel('预测标签', fontsize=11)
ax1.set_ylabel('真实标签', fontsize=11)
ax1.set_title('混淆矩阵', fontsize=13, fontweight='bold')

# 3.2 每个类别的性能指标（右上）
ax2 = fig.add_subplot(gs[0, 1])
x = np.arange(len(class_names))
width = 0.25

bars1 = ax2.bar(x - width, precision, width, label='精确率', color='#FF6B6B')
bars2 = ax2.bar(x, recall, width, label='召回率', color='#4ECDC4')
bars3 = ax2.bar(x + width, f1, width, label='F1分数', color='#45B7D1')

ax2.set_xlabel('类别', fontsize=11)
ax2.set_ylabel('分数', fontsize=11)
ax2.set_title('各类别性能指标对比', fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(class_names)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, 1.1)

# 添加数值标签
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=8)

# 3.3 样本分布（左下）
ax3 = fig.add_subplot(gs[1, 0])
true_counts = np.bincount(y_test_m)
pred_counts = np.bincount(y_pred_m)

x = np.arange(len(class_names))
width = 0.35

bars1 = ax3.bar(x - width/2, true_counts, width, label='真实分布', color='skyblue')
bars2 = ax3.bar(x + width/2, pred_counts, width, label='预测分布', color='lightcoral')

ax3.set_xlabel('类别', fontsize=11)
ax3.set_ylabel('样本数量', fontsize=11)
ax3.set_title('真实vs预测样本分布', fontsize=13, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(class_names)
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# 3.4 整体性能指标（右下）
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

# 计算整体指标
overall_accuracy = accuracy_score(y_test_m, y_pred_m)
macro_precision = np.mean(precision)
macro_recall = np.mean(recall)
macro_f1 = np.mean(f1)

metrics_table = f"""
整体性能指标
{'=' * 40}

准确率 (Accuracy):     {overall_accuracy:.4f}
宏平均精确率:          {macro_precision:.4f}
宏平均召回率:          {macro_recall:.4f}
宏平均F1分数:          {macro_f1:.4f}

{'=' * 40}

各类别详细指标:

"""

for i, name in enumerate(class_names):
    metrics_table += f"{name}:\n"
    metrics_table += f"  精确率: {precision[i]:.4f}\n"
    metrics_table += f"  召回率: {recall[i]:.4f}\n"
    metrics_table += f"  F1分数: {f1[i]:.4f}\n"
    metrics_table += f"  样本数: {support[i]}\n\n"

ax4.text(0.1, 0.95, metrics_table, fontsize=10, verticalalignment='top',
        fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.suptitle('多分类模型综合性能分析', fontsize=16, fontweight='bold', y=0.98)
plt.savefig('Day4_5_Model_Evaluation/output_3_comprehensive_analysis.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_3_comprehensive_analysis.png")
plt.close()

print("\n" + "=" * 60)
print("✅ Day 4-5 - 任务4.1 完成！")
print("已生成3个混淆矩阵可视化:")
print("  1. output_1_binary_confusion_matrix.png - 二分类")
print("  2. output_2_multi_confusion_matrix.png - 多分类")
print("  3. output_3_comprehensive_analysis.png - 综合分析")
print("=" * 60)
