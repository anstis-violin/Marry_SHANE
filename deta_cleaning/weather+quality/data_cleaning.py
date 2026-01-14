"""
空气质量数据集清洗脚本
Air Quality UCI Dataset Cleaning
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data(file_path):
    """
    加载原始数据
    """
    print("=" * 50)
    print("步骤 1: 加载数据")
    print("=" * 50)
    
    # 读取CSV文件，使用分号作为分隔符
    df = pd.read_csv(file_path, sep=';', decimal=',')
    
    print(f"原始数据形状: {df.shape}")
    print(f"\n前5行数据:")
    print(df.head())
    
    return df

def explore_data(df):
    """
    探索数据基本信息
    """
    print("\n" + "=" * 50)
    print("步骤 2: 数据探索")
    print("=" * 50)
    
    print("\n数据信息:")
    print(df.info())
    
    print("\n数据统计描述:")
    print(df.describe())
    
    print("\n缺失值统计:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    print("\n各列数据类型:")
    print(df.dtypes)
    
    return df

def clean_data(df):
    """
    清洗数据
    """
    print("\n" + "=" * 50)
    print("步骤 3: 数据清洗")
    print("=" * 50)
    
    # 3.1 删除空列
    print("\n3.1 删除空列...")
    df = df.dropna(axis=1, how='all')
    print(f"删除空列后形状: {df.shape}")
    
    # 3.2 删除末尾的空列（Unnamed列）
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    print(f"删除Unnamed列后形状: {df.shape}")
    
    # 3.3 合并日期和时间列
    print("\n3.2 处理日期时间...")
    if 'Date' in df.columns and 'Time' in df.columns:
        # 创建datetime列
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'], 
            format='%d/%m/%Y %H.%M.%S',
            errors='coerce'
        )
        # 删除原始的Date和Time列
        df = df.drop(['Date', 'Time'], axis=1)
        # 将DateTime设为索引
        df = df.set_index('DateTime')
        print(f"日期时间处理完成，时间范围: {df.index.min()} 到 {df.index.max()}")
    
    # 3.4 处理缺失值标记 (-200)
    print("\n3.3 处理缺失值标记 (-200)...")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    # 统计-200的数量
    missing_200_count = {}
    for col in numeric_columns:
        count = (df[col] == -200).sum()
        if count > 0:
            missing_200_count[col] = count
    
    if missing_200_count:
        print(f"发现 -200 标记的缺失值:")
        for col, count in missing_200_count.items():
            print(f"  {col}: {count} 个")
    
    # 将-200替换为NaN
    df[numeric_columns] = df[numeric_columns].replace(-200, np.nan)
    
    # 3.5 删除完全重复的行
    print("\n3.4 删除重复行...")
    duplicates = df.duplicated().sum()
    print(f"发现 {duplicates} 个重复行")
    df = df.drop_duplicates()
    
    # 3.6 删除全为NaN的行
    print("\n3.5 删除全为NaN的行...")
    before_rows = len(df)
    df = df.dropna(how='all')
    after_rows = len(df)
    print(f"删除了 {before_rows - after_rows} 行全为NaN的数据")
    
    print(f"\n清洗后数据形状: {df.shape}")
    
    return df

def handle_missing_values(df, method='interpolate'):
    """
    处理缺失值
    
    参数:
        method: 'drop' - 删除含缺失值的行
                'interpolate' - 线性插值
                'ffill' - 前向填充
                'mean' - 均值填充
    """
    print("\n" + "=" * 50)
    print(f"步骤 4: 处理缺失值 (方法: {method})")
    print("=" * 50)
    
    print("\n缺失值统计:")
    missing_stats = df.isnull().sum()
    missing_percent = (missing_stats / len(df)) * 100
    missing_df = pd.DataFrame({
        '缺失数量': missing_stats,
        '缺失百分比': missing_percent
    })
    print(missing_df[missing_df['缺失数量'] > 0])
    
    if method == 'drop':
        print("\n使用删除法处理缺失值...")
        df_cleaned = df.dropna()
        print(f"删除后剩余 {len(df_cleaned)} 行 (原有 {len(df)} 行)")
        
    elif method == 'interpolate':
        print("\n使用线性插值法处理缺失值...")
        df_cleaned = df.copy()
        numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
        df_cleaned[numeric_columns] = df_cleaned[numeric_columns].interpolate(
            method='linear', 
            limit_direction='both'
        )
        
    elif method == 'ffill':
        print("\n使用前向填充法处理缺失值...")
        df_cleaned = df.fillna(method='ffill')
        
    elif method == 'mean':
        print("\n使用均值填充法处理缺失值...")
        df_cleaned = df.copy()
        numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
    
    else:
        print(f"未知方法: {method}，返回原数据")
        df_cleaned = df
    
    print(f"\n处理后缺失值数量: {df_cleaned.isnull().sum().sum()}")
    
    return df_cleaned

def detect_outliers(df, method='iqr'):
    """
    检测异常值
    
    参数:
        method: 'iqr' - 四分位距法
                'zscore' - Z分数法
    """
    print("\n" + "=" * 50)
    print(f"步骤 5: 检测异常值 (方法: {method})")
    print("=" * 50)
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    outliers_info = {}
    
    for col in numeric_columns:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outliers_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
            
        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outliers = df[z_scores > 3]
            outliers_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100
            }
    
    print("\n异常值统计:")
    for col, info in outliers_info.items():
        if info['count'] > 0:
            print(f"{col}: {info['count']} 个 ({info['percentage']:.2f}%)")
    
    return outliers_info

def visualize_data(df, output_dir='./'):
    """
    数据可视化
    """
    print("\n" + "=" * 50)
    print("步骤 6: 数据可视化")
    print("=" * 50)
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    # 6.1 缺失值热图
    print("\n生成缺失值热图...")
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
    plt.title('缺失值分布热图', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}missing_values_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"保存: {output_dir}missing_values_heatmap.png")
    
    # 6.2 数据分布箱线图
    print("\n生成箱线图...")
    fig, axes = plt.subplots(4, 4, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_columns[:16]):
        if idx < len(axes):
            df[col].plot(kind='box', ax=axes[idx])
            axes[idx].set_title(col, fontsize=10)
            axes[idx].set_ylabel('')
    
    # 隐藏多余的子图
    for idx in range(len(numeric_columns), len(axes)):
        axes[idx].axis('off')
    
    plt.suptitle('各特征箱线图', fontsize=16, y=1.00)
    plt.tight_layout()
    plt.savefig(f'{output_dir}boxplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"保存: {output_dir}boxplots.png")
    
    # 6.3 相关性热图
    print("\n生成相关性热图...")
    plt.figure(figsize=(14, 12))
    correlation = df[numeric_columns].corr()
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('特征相关性热图', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"保存: {output_dir}correlation_heatmap.png")
    
    print("\n可视化完成！")

def save_cleaned_data(df, output_path):
    """
    保存清洗后的数据
    """
    print("\n" + "=" * 50)
    print("步骤 7: 保存清洗后的数据")
    print("=" * 50)
    
    # 保存为CSV
    df.to_csv(output_path)
    print(f"数据已保存到: {output_path}")
    print(f"最终数据形状: {df.shape}")
    
    # 显示最终数据预览
    print("\n清洗后数据预览:")
    print(df.head(10))
    
    print("\n数据统计信息:")
    print(df.describe())

def main():
    """
    主函数
    """
    # 文件路径
    input_file = r'c:\Users\ASUS\Desktop\好想娶谢恩\uci数据集\air+quality\AirQualityUCI.csv'
    output_file = r'e:\anstis\AirQualityUCI_cleaned.csv'
    output_dir = r'e:\anstis\\'
    
    print("=" * 60)
    print("空气质量数据清洗开始")
    print("=" * 60)
    print()
    
    # 1. 加载数据
    df = load_data(input_file)
    
    # 2. 探索数据
    df = explore_data(df)
    
    # 3. 清洗数据
    df = clean_data(df)
    
    # 4. 处理缺失值（可选择不同方法）
    # 方法选项: 'drop', 'interpolate', 'ffill', 'mean'
    df = handle_missing_values(df, method='interpolate')
    
    # 5. 检测异常值
    outliers_info = detect_outliers(df, method='iqr')
    
    # 6. 数据可视化
    visualize_data(df, output_dir=output_dir)
    
    # 7. 保存清洗后的数据
    save_cleaned_data(df, output_file)
    
    print("\n" + "=" * 50)
    print("数据清洗完成！")
    print("=" * 50)
    
    return df

if __name__ == "__main__":
    df_cleaned = main()
