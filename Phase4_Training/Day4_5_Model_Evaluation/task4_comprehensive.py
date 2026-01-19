"""
Day 4-5 - 任务4.4: 模型性能综合可视化
包含: 多指标对比、多模型对比、综合仪表盘
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix)
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 4-5 - 任务4.4: 模型性能综合可视化")
print("=" * 60)

# ============================================================================
# 1. 准备数据和训练多个模型
# ============================================================================
print("\n[步骤1] 准备数据和训练模型...")

# 生成数据
X, y = make_classification(n_samples=2000, n_features=20,
                          n_informative=15, n_redundant=5,
                          n_classes=2, random_state=42)

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 定义多个模型
models = {
    '随机森林': RandomForestClassifier(n_estimators=100, random_state=42),
    '梯度提升': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
    '逻辑回归': LogisticRegression(random_state=42, max_iter=1000),
    'SVM': SVC(probability=True, random_state=42)
}

# 训练模型并收集性能指标
results = []

for name, model in models.items():
    print(f"\n训练 {name}...")
    
    # 训练模型
    model.fit(X_train, y_train)
    
    # 预测
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # 计算指标
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba) if y_proba is not None else 0
    
    # 交叉验证分数
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    results.append({
        '模型': name,
        '准确率': accuracy,
        '精确率': precision,
        '召回率': recall,
        'F1分数': f1,
        'AUC': auc,
        'CV均值': cv_mean,
        'CV标准差': cv_std
    })
    
    print(f"  准确率: {accuracy:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}")

# 转换为DataFrame
df_results = pd.DataFrame(results)
print("\n所有模型性能汇总:")
print(df_results.to_string(index=False))

# ============================================================================
# 2. 多指标对比图
# ============================================================================
print("\n[步骤2] 创建多指标对比图...")

fig, ax = plt.subplots(figsize=(14, 8))

# 准备数据
metrics = ['准确率', '精确率', '召回率', 'F1分数', 'AUC']
x = np.arange(len(models))
width = 0.15

# 绘制分组柱状图
for i, metric in enumerate(metrics):
    values = df_results[metric].values
    offset = (i - 2) * width
    bars = ax.bar(x + offset, values, width, label=metric)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=8, rotation=0)

# 美化
ax.set_xlabel('模型', fontsize=12)
ax.set_ylabel('分数', fontsize=12)
ax.set_title('多模型性能指标对比', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df_results['模型'].values, rotation=15, ha='right')
ax.legend(loc='lower right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim([0, 1.1])

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_1_multi_metric_comparison.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_1_multi_metric_comparison.png")
plt.close()

# ============================================================================
# 3. 雷达图对比
# ============================================================================
print("\n[步骤3] 创建雷达图对比...")

# 选择前3个模型进行雷达图对比
top_models = df_results.nlargest(3, 'F1分数')

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# 指标
metrics_radar = ['准确率', '精确率', '召回率', 'F1分数', 'AUC']
n_metrics = len(metrics_radar)
angles = np.linspace(0, 2 * np.pi, n_metrics, endpoint=False).tolist()
angles += angles[:1]

# 颜色
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

# 绘制每个模型
for idx, (_, row) in enumerate(top_models.iterrows()):
    values = [row[m] for m in metrics_radar]
    values += values[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, label=row['模型'], 
            color=colors[idx], markersize=8)
    ax.fill(angles, values, alpha=0.15, color=colors[idx])

# 设置标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics_radar, fontsize=12)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
ax.set_title('Top 3 模型性能雷达图', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('Day4_5_Model_Evaluation/output_2_radar_comparison.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_2_radar_comparison.png")
plt.close()

# ============================================================================
# 4. 综合性能仪表盘
# ============================================================================
print("\n[步骤4] 创建综合性能仪表盘...")

# 选择最佳模型
best_model_name = df_results.loc[df_results['F1分数'].idxmax(), '模型']
best_model = models[best_model_name]
best_model.fit(X_train, y_train)
y_pred_best = best_model.predict(X_test)
y_proba_best = best_model.predict_proba(X_test)[:, 1]

# 创建综合仪表盘
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 4.1 性能指标柱状图（左上）
ax1 = fig.add_subplot(gs[0, 0])
best_metrics = df_results[df_results['模型'] == best_model_name].iloc[0]
metrics_names = ['准确率', '精确率', '召回率', 'F1分数', 'AUC']
metrics_values = [best_metrics[m] for m in metrics_names]

bars = ax1.barh(metrics_names, metrics_values, color='skyblue', edgecolor='black')
for i, (bar, val) in enumerate(zip(bars, metrics_values)):
    ax1.text(val + 0.01, i, f'{val:.4f}', va='center', fontsize=10)

ax1.set_xlim([0, 1.1])
ax1.set_xlabel('分数', fontsize=11)
ax1.set_title(f'{best_model_name} - 性能指标', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')

# 4.2 混淆矩阵（中上）
ax2 = fig.add_subplot(gs[0, 1])
cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['负类', '正类'],
            yticklabels=['负类', '正类'],
            ax=ax2, cbar_kws={'label': '样本数'})
ax2.set_xlabel('预测标签', fontsize=11)
ax2.set_ylabel('真实标签', fontsize=11)
ax2.set_title('混淆矩阵', fontsize=13, fontweight='bold')

# 4.3 ROC曲线（右上）
ax3 = fig.add_subplot(gs[0, 2])
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_test, y_proba_best)
roc_auc = auc(fpr, tpr)

ax3.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC (AUC = {roc_auc:.3f})')
ax3.plot([0, 1], [0, 1], 'k--', lw=2)
ax3.set_xlim([0.0, 1.0])
ax3.set_ylim([0.0, 1.05])
ax3.set_xlabel('假阳性率', fontsize=11)
ax3.set_ylabel('真阳性率', fontsize=11)
ax3.set_title('ROC曲线', fontsize=13, fontweight='bold')
ax3.legend(loc="lower right")
ax3.grid(True, alpha=0.3)

# 4.4 所有模型对比（左中）
ax4 = fig.add_subplot(gs[1, :])
x = np.arange(len(models))
width = 0.15
metrics_to_plot = ['准确率', '精确率', '召回率', 'F1分数', 'AUC']
colors_bar = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

for i, (metric, color) in enumerate(zip(metrics_to_plot, colors_bar)):
    values = df_results[metric].values
    offset = (i - 2) * width
    ax4.bar(x + offset, values, width, label=metric, color=color, alpha=0.8)

ax4.set_xlabel('模型', fontsize=11)
ax4.set_ylabel('分数', fontsize=11)
ax4.set_title('所有模型性能对比', fontsize=13, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(df_results['模型'].values, rotation=15, ha='right')
ax4.legend(loc='lower right', fontsize=10, ncol=5)
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim([0, 1.1])

# 4.5 交叉验证稳定性（左下）
ax5 = fig.add_subplot(gs[2, 0])
cv_means = df_results['CV均值'].values
cv_stds = df_results['CV标准差'].values
model_names = df_results['模型'].values

ax5.errorbar(range(len(models)), cv_means, yerr=cv_stds, 
            fmt='o-', capsize=5, capthick=2, linewidth=2, markersize=8,
            color='purple', ecolor='red')
ax5.set_xticks(range(len(models)))
ax5.set_xticklabels(model_names, rotation=45, ha='right')
ax5.set_ylabel('交叉验证准确率', fontsize=11)
ax5.set_title('模型稳定性分析', fontsize=13, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.set_ylim([0.7, 1.0])

# 4.6 性能排名（中下）
ax6 = fig.add_subplot(gs[2, 1])
# 计算综合得分（各指标平均）
df_results['综合得分'] = df_results[['准确率', '精确率', '召回率', 'F1分数', 'AUC']].mean(axis=1)
df_sorted = df_results.sort_values('综合得分', ascending=True)

bars = ax6.barh(df_sorted['模型'], df_sorted['综合得分'], 
               color=plt.cm.RdYlGn(df_sorted['综合得分']))
for i, (bar, val) in enumerate(zip(bars, df_sorted['综合得分'])):
    ax6.text(val + 0.01, i, f'{val:.4f}', va='center', fontsize=10)

ax6.set_xlim([0.7, 1.0])
ax6.set_xlabel('综合得分', fontsize=11)
ax6.set_title('模型综合排名', fontsize=13, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='x')

# 4.7 性能总结表（右下）
ax7 = fig.add_subplot(gs[2, 2])
ax7.axis('off')

# 创建性能总结
summary_text = f"""
{'=' * 45}
模型评估总结报告
{'=' * 45}

最佳模型: {best_model_name}

性能指标:
  • 准确率: {best_metrics['准确率']:.4f}
  • 精确率: {best_metrics['精确率']:.4f}
  • 召回率: {best_metrics['召回率']:.4f}
  • F1分数: {best_metrics['F1分数']:.4f}
  • AUC: {best_metrics['AUC']:.4f}

交叉验证:
  • CV均值: {best_metrics['CV均值']:.4f}
  • CV标准差: {best_metrics['CV标准差']:.4f}

模型排名（按综合得分）:
"""

for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
    summary_text += f"  {idx}. {row['模型']}: {row['综合得分']:.4f}\n"

summary_text += "\n" + "=" * 45

ax7.text(0.1, 0.95, summary_text, fontsize=9, verticalalignment='top',
        fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.suptitle('模型性能综合仪表盘', fontsize=18, fontweight='bold', y=0.995)
plt.savefig('Day4_5_Model_Evaluation/output_3_comprehensive_dashboard.png',
            dpi=300, bbox_inches='tight')
print("✓ 已保存: output_3_comprehensive_dashboard.png")
plt.close()

# ============================================================================
# 5. 保存性能报告
# ============================================================================
print("\n[步骤5] 保存性能报告...")

report = f"""
{'=' * 70}
模型性能评估报告
{'=' * 70}

评估日期: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
数据集大小: 训练集 {len(X_train)} 样本, 测试集 {len(X_test)} 样本

{'=' * 70}
所有模型性能对比
{'=' * 70}

{df_results.to_string(index=False)}

{'=' * 70}
最佳模型详情
{'=' * 70}

模型名称: {best_model_name}

性能指标:
  准确率 (Accuracy):    {best_metrics['准确率']:.6f}
  精确率 (Precision):   {best_metrics['精确率']:.6f}
  召回率 (Recall):      {best_metrics['召回率']:.6f}
  F1分数 (F1-Score):    {best_metrics['F1分数']:.6f}
  AUC:                  {best_metrics['AUC']:.6f}

交叉验证结果:
  CV均值:               {best_metrics['CV均值']:.6f}
  CV标准差:             {best_metrics['CV标准差']:.6f}

混淆矩阵:
{cm}

{'=' * 70}
模型排名（按综合得分）
{'=' * 70}

"""

for idx, (_, row) in enumerate(df_sorted.iterrows(), 1):
    report += f"{idx}. {row['模型']:<15} 综合得分: {row['综合得分']:.6f}\n"

report += "\n" + "=" * 70 + "\n"

# 保存报告
with open('Day4_5_Model_Evaluation/performance_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ 已保存: performance_report.txt")

# 保存CSV
df_results.to_csv('Day4_5_Model_Evaluation/model_performance.csv', 
                  index=False, encoding='utf-8-sig')
print("✓ 已保存: model_performance.csv")

print("\n" + "=" * 60)
print("✅ Day 4-5 - 任务4.4 完成！")
print("已生成综合性能可视化:")
print("  1. output_1_multi_metric_comparison.png - 多指标对比")
print("  2. output_2_radar_comparison.png - 雷达图对比")
print("  3. output_3_comprehensive_dashboard.png - 综合仪表盘")
print("  4. performance_report.txt - 性能报告")
print("  5. model_performance.csv - 性能数据")
print("\n最佳模型: " + best_model_name)
print(f"综合得分: {df_results.loc[df_results['模型'] == best_model_name, '综合得分'].values[0]:.4f}")
print("=" * 60)
