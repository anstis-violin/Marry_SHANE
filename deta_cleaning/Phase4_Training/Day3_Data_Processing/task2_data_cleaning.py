"""
Day 3 - 任务3.2: 数据处理和清洗
包含: 缺失值处理、异常值处理、数据转换、数据合并
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("Day 3 - 任务3.2: 数据处理和清洗")
print("=" * 60)

# ============================================================================
# 1. 创建示例数据集（包含各种问题）
# ============================================================================
print("\n[步骤1] 创建示例数据集...")

np.random.seed(42)

# 创建包含问题的数据集
data = {
    '学号': range(1, 101),
    '姓名': [f'学生{i}' for i in range(1, 101)],
    '年龄': np.random.randint(18, 25, 100),
    '成绩': np.random.uniform(60, 100, 100),
    '出勤率': np.random.uniform(0.7, 1.0, 100),
    '家庭收入': np.random.uniform(30000, 150000, 100)
}

# 引入缺失值
data['成绩'][np.random.choice(100, 10, replace=False)] = np.nan
data['出勤率'][np.random.choice(100, 8, replace=False)] = np.nan

# 引入异常值
data['年龄'][5] = 150  # 异常年龄
data['成绩'][10] = 200  # 异常成绩
data['出勤率'][15] = 5.0  # 异常出勤率

df = pd.DataFrame(data)

print(f"✓ 创建数据集: {len(df)} 条记录")
print(f"\n原始数据预览:")
print(df.head(10))

# 保存原始数据
df.to_csv('Day3_Data_Processing/raw_data.csv', index=False, encoding='utf-8-sig')
print(f"\n✓ 已保存原始数据: raw_data.csv")

# ============================================================================
# 2. 数据质量检查
# ============================================================================
print("\n" + "=" * 60)
print("[步骤2] 数据质量检查")
print("=" * 60)

print("\n数据基本信息:")
print(df.info())

print("\n数据统计描述:")
print(df.describe())

print("\n缺失值统计:")
missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    '缺失数量': missing,
    '缺失比例(%)': missing_percent
})
print(missing_df[missing_df['缺失数量'] > 0])

# 可视化缺失值
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 缺失值热图
sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis', ax=axes[0])
axes[0].set_title('缺失值分布热图', fontsize=14, fontweight='bold')

# 缺失值柱状图
missing_data = df.isnull().sum()
missing_data = missing_data[missing_data > 0]
missing_data.plot(kind='bar', ax=axes[1], color='coral')
axes[1].set_title('各列缺失值数量', fontsize=14, fontweight='bold')
axes[1].set_xlabel('列名')
axes[1].set_ylabel('缺失数量')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('Day3_Data_Processing/output_1_missing_values.png', dpi=300, bbox_inches='tight')
print("\n✓ 已保存: output_1_missing_values.png")
plt.close()

# ============================================================================
# 3. 缺失值处理
# ============================================================================
print("\n" + "=" * 60)
print("[步骤3] 缺失值处理")
print("=" * 60)

df_cleaned = df.copy()

# 3.1 成绩缺失值：使用均值填充
mean_score = df_cleaned['成绩'].mean()
df_cleaned['成绩'].fillna(mean_score, inplace=True)
print(f"\n✓ 成绩缺失值已用均值填充: {mean_score:.2f}")

# 3.2 出勤率缺失值：使用中位数填充
median_attendance = df_cleaned['出勤率'].median()
df_cleaned['出勤率'].fillna(median_attendance, inplace=True)
print(f"✓ 出勤率缺失值已用中位数填充: {median_attendance:.2f}")

print(f"\n处理后缺失值统计:")
print(df_cleaned.isnull().sum())

# ============================================================================
# 4. 异常值检测和处理
# ============================================================================
print("\n" + "=" * 60)
print("[步骤4] 异常值检测和处理")
print("=" * 60)

# 4.1 使用箱线图检测异常值
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 年龄箱线图
axes[0, 0].boxplot(df_cleaned['年龄'].dropna())
axes[0, 0].set_title('年龄分布（处理前）', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('年龄')
axes[0, 0].grid(True, alpha=0.3)

# 成绩箱线图
axes[0, 1].boxplot(df_cleaned['成绩'].dropna())
axes[0, 1].set_title('成绩分布（处理前）', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('成绩')
axes[0, 1].grid(True, alpha=0.3)

# 出勤率箱线图
axes[1, 0].boxplot(df_cleaned['出勤率'].dropna())
axes[1, 0].set_title('出勤率分布（处理前）', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('出勤率')
axes[1, 0].grid(True, alpha=0.3)

# 家庭收入箱线图
axes[1, 1].boxplot(df_cleaned['家庭收入'].dropna())
axes[1, 1].set_title('家庭收入分布（处理前）', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('家庭收入')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Day3_Data_Processing/output_2_outliers_before.png', dpi=300, bbox_inches='tight')
print("\n✓ 已保存: output_2_outliers_before.png")
plt.close()

# 4.2 使用IQR方法检测和处理异常值
def detect_outliers_iqr(data, column):
    """使用IQR方法检测异常值"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# 检测年龄异常值
outliers_age, lower_age, upper_age = detect_outliers_iqr(df_cleaned, '年龄')
print(f"\n年龄异常值检测:")
print(f"  正常范围: [{lower_age:.2f}, {upper_age:.2f}]")
print(f"  异常值数量: {len(outliers_age)}")
if len(outliers_age) > 0:
    print(f"  异常值: {outliers_age['年龄'].values}")

# 检测成绩异常值
outliers_score, lower_score, upper_score = detect_outliers_iqr(df_cleaned, '成绩')
print(f"\n成绩异常值检测:")
print(f"  正常范围: [{lower_score:.2f}, {upper_score:.2f}]")
print(f"  异常值数量: {len(outliers_score)}")

# 检测出勤率异常值
outliers_attend, lower_attend, upper_attend = detect_outliers_iqr(df_cleaned, '出勤率')
print(f"\n出勤率异常值检测:")
print(f"  正常范围: [{lower_attend:.2f}, {upper_attend:.2f}]")
print(f"  异常值数量: {len(outliers_attend)}")

# 4.3 处理异常值
# 年龄：限制在合理范围
df_cleaned.loc[df_cleaned['年龄'] > 30, '年龄'] = df_cleaned['年龄'].median()
df_cleaned.loc[df_cleaned['年龄'] < 15, '年龄'] = df_cleaned['年龄'].median()

# 成绩：限制在0-100
df_cleaned.loc[df_cleaned['成绩'] > 100, '成绩'] = 100
df_cleaned.loc[df_cleaned['成绩'] < 0, '成绩'] = 0

# 出勤率：限制在0-1
df_cleaned.loc[df_cleaned['出勤率'] > 1, '出勤率'] = 1
df_cleaned.loc[df_cleaned['出勤率'] < 0, '出勤率'] = 0

print("\n✓ 异常值已处理")

# ============================================================================
# 5. 数据转换
# ============================================================================
print("\n" + "=" * 60)
print("[步骤5] 数据转换")
print("=" * 60)

# 5.1 添加成绩等级
def score_to_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

df_cleaned['成绩等级'] = df_cleaned['成绩'].apply(score_to_grade)
print("\n✓ 已添加成绩等级列")

# 5.2 标准化家庭收入（Z-score标准化）
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_cleaned['家庭收入_标准化'] = scaler.fit_transform(df_cleaned[['家庭收入']])
print("✓ 已标准化家庭收入")

# 5.3 归一化出勤率（Min-Max归一化，已经在0-1范围内）
print("✓ 出勤率已在0-1范围内")

print("\n转换后数据预览:")
print(df_cleaned[['学号', '姓名', '成绩', '成绩等级', '家庭收入', '家庭收入_标准化']].head(10))

# ============================================================================
# 6. 数据合并示例
# ============================================================================
print("\n" + "=" * 60)
print("[步骤6] 数据合并示例")
print("=" * 60)

# 创建额外的数据集（课外活动）
extra_data = pd.DataFrame({
    '学号': range(1, 101),
    '社团活动': np.random.choice(['是', '否'], 100),
    '志愿服务小时': np.random.randint(0, 50, 100)
})

# 合并数据
df_final = pd.merge(df_cleaned, extra_data, on='学号', how='left')
print(f"\n✓ 已合并课外活动数据")
print(f"合并后数据形状: {df_final.shape}")

# ============================================================================
# 7. 保存清洗后的数据
# ============================================================================
print("\n" + "=" * 60)
print("[步骤7] 保存清洗后的数据")
print("=" * 60)

df_final.to_csv('Day3_Data_Processing/cleaned_data.csv', index=False, encoding='utf-8-sig')
print("✓ 已保存: cleaned_data.csv")

# ============================================================================
# 8. 生成数据清洗报告
# ============================================================================
print("\n" + "=" * 60)
print("[步骤8] 生成数据清洗报告")
print("=" * 60)

report = f"""
{'=' * 60}
数据清洗报告
{'=' * 60}

1. 原始数据
   - 记录数: {len(df)}
   - 列数: {len(df.columns)}
   - 缺失值总数: {df.isnull().sum().sum()}

2. 缺失值处理
   - 成绩缺失: {df['成绩'].isnull().sum()} 条 → 使用均值填充
   - 出勤率缺失: {df['出勤率'].isnull().sum()} 条 → 使用中位数填充

3. 异常值处理
   - 年龄异常: {len(outliers_age)} 条 → 替换为中位数
   - 成绩异常: {len(outliers_score)} 条 → 限制在0-100范围
   - 出勤率异常: {len(outliers_attend)} 条 → 限制在0-1范围

4. 数据转换
   - 添加成绩等级列
   - 标准化家庭收入
   - 归一化出勤率

5. 数据合并
   - 合并课外活动数据
   - 最终记录数: {len(df_final)}
   - 最终列数: {len(df_final.columns)}

6. 清洗后数据质量
   - 缺失值: {df_final.isnull().sum().sum()}
   - 数据完整性: {(1 - df_final.isnull().sum().sum() / (len(df_final) * len(df_final.columns))) * 100:.2f}%

7. 成绩等级分布
   - A等: {len(df_final[df_final['成绩等级'] == 'A'])} 人
   - B等: {len(df_final[df_final['成绩等级'] == 'B'])} 人
   - C等: {len(df_final[df_final['成绩等级'] == 'C'])} 人
   - D等: {len(df_final[df_final['成绩等级'] == 'D'])} 人
   - F等: {len(df_final[df_final['成绩等级'] == 'F'])} 人

{'=' * 60}
"""

print(report)

with open('Day3_Data_Processing/cleaning_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
print("✓ 已保存: cleaning_report.txt")

# ============================================================================
# 9. 可视化对比
# ============================================================================
print("\n" + "=" * 60)
print("[步骤9] 生成对比可视化")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 成绩分布对比
axes[0, 0].hist(df['成绩'].dropna(), bins=20, alpha=0.7, color='red', label='处理前')
axes[0, 0].hist(df_final['成绩'], bins=20, alpha=0.7, color='green', label='处理后')
axes[0, 0].set_title('成绩分布对比', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('成绩')
axes[0, 0].set_ylabel('频数')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 年龄分布对比
axes[0, 1].hist(df['年龄'], bins=15, alpha=0.7, color='red', label='处理前')
axes[0, 1].hist(df_final['年龄'], bins=15, alpha=0.7, color='green', label='处理后')
axes[0, 1].set_title('年龄分布对比', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('年龄')
axes[0, 1].set_ylabel('频数')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 出勤率分布对比
axes[0, 2].hist(df['出勤率'].dropna(), bins=20, alpha=0.7, color='red', label='处理前')
axes[0, 2].hist(df_final['出勤率'], bins=20, alpha=0.7, color='green', label='处理后')
axes[0, 2].set_title('出勤率分布对比', fontsize=12, fontweight='bold')
axes[0, 2].set_xlabel('出勤率')
axes[0, 2].set_ylabel('频数')
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# 成绩等级分布
grade_counts = df_final['成绩等级'].value_counts().sort_index()
axes[1, 0].bar(grade_counts.index, grade_counts.values, color='skyblue', edgecolor='black')
axes[1, 0].set_title('成绩等级分布', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('等级')
axes[1, 0].set_ylabel('人数')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# 社团活动分布
activity_counts = df_final['社团活动'].value_counts()
axes[1, 1].pie(activity_counts.values, labels=activity_counts.index, autopct='%1.1f%%',
               colors=['lightcoral', 'lightblue'], startangle=90)
axes[1, 1].set_title('社团活动参与情况', fontsize=12, fontweight='bold')

# 成绩与出勤率关系
axes[1, 2].scatter(df_final['出勤率'], df_final['成绩'], alpha=0.5, color='purple')
axes[1, 2].set_title('成绩与出勤率关系', fontsize=12, fontweight='bold')
axes[1, 2].set_xlabel('出勤率')
axes[1, 2].set_ylabel('成绩')
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Day3_Data_Processing/output_3_comparison.png', dpi=300, bbox_inches='tight')
print("✓ 已保存: output_3_comparison.png")
plt.close()

print("\n" + "=" * 60)
print("✅ Day 3 - 任务3.2 完成！")
print("已生成文件:")
print("  1. raw_data.csv - 原始数据")
print("  2. cleaned_data.csv - 清洗后数据")
print("  3. cleaning_report.txt - 清洗报告")
print("  4. output_1_missing_values.png - 缺失值可视化")
print("  5. output_2_outliers_before.png - 异常值检测")
print("  6. output_3_comparison.png - 处理前后对比")
print("=" * 60)
