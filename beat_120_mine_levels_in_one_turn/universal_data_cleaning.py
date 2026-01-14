"""
通用数据清洗脚本 - 美赛第二阶段
Universal Data Cleaning Script for MCM Training Phase 2

功能：
1. 自动识别数据类型
2. 处理缺失值（多种方法）
3. 删除重复值
4. 处理异常值
5. 数据类型转换
6. 生成清洗报告
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class UniversalDataCleaner:
    """通用数据清洗类"""
    
    def __init__(self, input_file, output_dir='./cleaned_data/'):
        """
        初始化
        
        参数:
            input_file: 输入数据文件路径（CSV格式）
            output_dir: 输出目录
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.df_original = None
        self.df_cleaned = None
        self.cleaning_report = {}
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"[OK] 创建输出目录: {output_dir}")
    
    def load_data(self, encoding='utf-8', sep=','):
        """
        加载数据
        
        参数:
            encoding: 文件编码（默认utf-8，如果报错可尝试'gbk'或'latin1'）
            sep: 分隔符（默认逗号，可以是';'、'\t'等）
        """
        print("\n" + "="*60)
        print("步骤 1: 加载数据")
        print("="*60)
        
        try:
            self.df_original = pd.read_csv(self.input_file, encoding=encoding, sep=sep)
            print(f"[OK] 成功加载数据")
            print(f"  文件路径: {self.input_file}")
            print(f"  数据形状: {self.df_original.shape}")
            print(f"  行数: {self.df_original.shape[0]}")
            print(f"  列数: {self.df_original.shape[1]}")
            
            # 复制一份用于清洗
            self.df_cleaned = self.df_original.copy()
            
            # 记录原始信息
            self.cleaning_report['原始行数'] = self.df_original.shape[0]
            self.cleaning_report['原始列数'] = self.df_original.shape[1]
            
            return True
            
        except UnicodeDecodeError:
            print(f"[!] 编码错误，尝试使用 'gbk' 编码...")
            try:
                self.df_original = pd.read_csv(self.input_file, encoding='gbk', sep=sep)
                self.df_cleaned = self.df_original.copy()
                print(f"[OK] 使用 gbk 编码成功加载")
                return True
            except:
                print(f"[ERROR] 加载失败，请检查文件编码")
                return False
        except Exception as e:
            print(f"[ERROR] 加载失败: {e}")
            return False
    
    def explore_data(self):
        """
        数据探索
        """
        print("\n" + "="*60)
        print("步骤 2: 数据探索")
        print("="*60)
        
        print("\n【数据预览】")
        print(self.df_cleaned.head(10))
        
        print("\n【数据信息】")
        print(f"数据类型分布:")
        print(self.df_cleaned.dtypes.value_counts())
        
        print("\n【列名和数据类型】")
        for col in self.df_cleaned.columns:
            dtype = self.df_cleaned[col].dtype
            non_null = self.df_cleaned[col].count()
            null_count = self.df_cleaned[col].isnull().sum()
            print(f"  {col:30s} | 类型: {str(dtype):10s} | 非空: {non_null:6d} | 缺失: {null_count:6d}")
        
        print("\n【基本统计】")
        print(self.df_cleaned.describe())
        
        # 识别数值列和分类列
        self.numeric_cols = self.df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df_cleaned.select_dtypes(include=['object']).columns.tolist()
        
        print(f"\n数值列 ({len(self.numeric_cols)}): {self.numeric_cols}")
        print(f"分类列 ({len(self.categorical_cols)}): {self.categorical_cols}")
    
    def handle_missing_values(self, method='auto', threshold=0.5):
        """
        处理缺失值
        
        参数:
            method: 处理方法
                - 'auto': 自动选择（推荐）
                - 'drop': 删除含缺失值的行
                - 'interpolate': 线性插值（适合时间序列）
                - 'mean': 均值填充（数值列）
                - 'median': 中位数填充（数值列）
                - 'mode': 众数填充（分类列）
                - 'ffill': 前向填充
                - 'bfill': 后向填充
            threshold: 缺失值比例阈值，超过此比例的列将被删除（0-1之间）
        """
        print("\n" + "="*60)
        print(f"步骤 3: 处理缺失值 (方法: {method})")
        print("="*60)
        
        # 统计缺失值
        missing_stats = self.df_cleaned.isnull().sum()
        missing_percent = (missing_stats / len(self.df_cleaned)) * 100
        
        missing_df = pd.DataFrame({
            '缺失数量': missing_stats,
            '缺失百分比': missing_percent
        })
        missing_df = missing_df[missing_df['缺失数量'] > 0].sort_values('缺失数量', ascending=False)
        
        if len(missing_df) > 0:
            print("\n【缺失值统计】")
            print(missing_df)
            
            # 删除缺失值过多的列
            cols_to_drop = missing_df[missing_df['缺失百分比'] > threshold * 100].index.tolist()
            if cols_to_drop:
                print(f"\n[OK] 删除缺失值超过{threshold*100}%的列: {cols_to_drop}")
                self.df_cleaned = self.df_cleaned.drop(columns=cols_to_drop)
                self.cleaning_report['删除的列'] = cols_to_drop
            
            # 处理剩余缺失值
            if method == 'auto':
                print("\n使用自动模式处理缺失值:")
                # 数值列用中位数填充
                for col in self.numeric_cols:
                    if col in self.df_cleaned.columns and self.df_cleaned[col].isnull().sum() > 0:
                        median_val = self.df_cleaned[col].median()
                        self.df_cleaned[col].fillna(median_val, inplace=True)
                        print(f"  [OK] {col}: 用中位数 {median_val:.2f} 填充")
                
                # 分类列用众数填充
                for col in self.categorical_cols:
                    if col in self.df_cleaned.columns and self.df_cleaned[col].isnull().sum() > 0:
                        mode_val = self.df_cleaned[col].mode()[0] if len(self.df_cleaned[col].mode()) > 0 else 'Unknown'
                        self.df_cleaned[col].fillna(mode_val, inplace=True)
                        print(f"  [OK] {col}: 用众数 '{mode_val}' 填充")
            
            elif method == 'drop':
                before_rows = len(self.df_cleaned)
                self.df_cleaned = self.df_cleaned.dropna()
                after_rows = len(self.df_cleaned)
                print(f"[OK] 删除含缺失值的行: {before_rows - after_rows} 行")
            
            elif method == 'interpolate':
                self.df_cleaned[self.numeric_cols] = self.df_cleaned[self.numeric_cols].interpolate(
                    method='linear', limit_direction='both'
                )
                print(f"[OK] 使用线性插值填充数值列")
            
            elif method == 'mean':
                for col in self.numeric_cols:
                    if col in self.df_cleaned.columns:
                        self.df_cleaned[col].fillna(self.df_cleaned[col].mean(), inplace=True)
                print(f"[OK] 使用均值填充数值列")
            
            elif method == 'median':
                for col in self.numeric_cols:
                    if col in self.df_cleaned.columns:
                        self.df_cleaned[col].fillna(self.df_cleaned[col].median(), inplace=True)
                print(f"[OK] 使用中位数填充数值列")
            
            elif method == 'mode':
                for col in self.df_cleaned.columns:
                    if self.df_cleaned[col].isnull().sum() > 0:
                        mode_val = self.df_cleaned[col].mode()[0] if len(self.df_cleaned[col].mode()) > 0 else None
                        if mode_val is not None:
                            self.df_cleaned[col].fillna(mode_val, inplace=True)
                print(f"[OK] 使用众数填充所有列")
            
            elif method in ['ffill', 'bfill']:
                self.df_cleaned = self.df_cleaned.fillna(method=method)
                print(f"[OK] 使用{method}方法填充")
            
            # 检查剩余缺失值
            remaining_missing = self.df_cleaned.isnull().sum().sum()
            print(f"\n处理后剩余缺失值: {remaining_missing}")
            self.cleaning_report['处理后缺失值'] = remaining_missing
        else:
            print("\n[OK] 数据中没有缺失值")
            self.cleaning_report['处理后缺失值'] = 0
    
    def remove_duplicates(self):
        """
        删除重复值
        """
        print("\n" + "="*60)
        print("步骤 4: 删除重复值")
        print("="*60)
        
        before_rows = len(self.df_cleaned)
        duplicates = self.df_cleaned.duplicated().sum()
        
        if duplicates > 0:
            print(f"发现 {duplicates} 个重复行 ({duplicates/before_rows*100:.2f}%)")
            self.df_cleaned = self.df_cleaned.drop_duplicates()
            after_rows = len(self.df_cleaned)
            print(f"[OK] 删除了 {before_rows - after_rows} 个重复行")
            self.cleaning_report['删除的重复行'] = before_rows - after_rows
        else:
            print("[OK] 没有发现重复行")
            self.cleaning_report['删除的重复行'] = 0
    
    def handle_outliers(self, method='iqr', action='cap'):
        """
        处理异常值
        
        参数:
            method: 检测方法
                - 'iqr': 四分位距法（推荐）
                - 'zscore': Z分数法
            action: 处理方式
                - 'cap': 截断（将异常值替换为边界值）
                - 'remove': 删除异常值
                - 'none': 只检测不处理
        """
        print("\n" + "="*60)
        print(f"步骤 5: 处理异常值 (方法: {method}, 操作: {action})")
        print("="*60)
        
        outliers_info = {}
        
        for col in self.numeric_cols:
            if col not in self.df_cleaned.columns:
                continue
            
            if method == 'iqr':
                Q1 = self.df_cleaned[col].quantile(0.25)
                Q3 = self.df_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers_mask = (self.df_cleaned[col] < lower_bound) | (self.df_cleaned[col] > upper_bound)
                outliers_count = outliers_mask.sum()
                
                if outliers_count > 0:
                    outliers_info[col] = {
                        'count': outliers_count,
                        'percentage': (outliers_count / len(self.df_cleaned)) * 100,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound
                    }
                    
                    if action == 'cap':
                        self.df_cleaned.loc[self.df_cleaned[col] < lower_bound, col] = lower_bound
                        self.df_cleaned.loc[self.df_cleaned[col] > upper_bound, col] = upper_bound
                        print(f"  [OK] {col}: 截断了 {outliers_count} 个异常值")
                    elif action == 'remove':
                        self.df_cleaned = self.df_cleaned[~outliers_mask]
                        print(f"  [OK] {col}: 删除了 {outliers_count} 个异常值")
            
            elif method == 'zscore':
                z_scores = np.abs((self.df_cleaned[col] - self.df_cleaned[col].mean()) / self.df_cleaned[col].std())
                outliers_mask = z_scores > 3
                outliers_count = outliers_mask.sum()
                
                if outliers_count > 0:
                    outliers_info[col] = {
                        'count': outliers_count,
                        'percentage': (outliers_count / len(self.df_cleaned)) * 100
                    }
                    
                    if action == 'remove':
                        self.df_cleaned = self.df_cleaned[~outliers_mask]
                        print(f"  [OK] {col}: 删除了 {outliers_count} 个异常值")
        
        if outliers_info:
            print(f"\n【异常值统计】")
            for col, info in outliers_info.items():
                print(f"  {col}: {info['count']} 个 ({info['percentage']:.2f}%)")
            self.cleaning_report['异常值处理'] = outliers_info
        else:
            print("[OK] 没有发现异常值")
            self.cleaning_report['异常值处理'] = {}
    
    def convert_data_types(self, auto_detect=True):
        """
        数据类型转换
        
        参数:
            auto_detect: 是否自动检测并转换数据类型
        """
        print("\n" + "="*60)
        print("步骤 6: 数据类型转换")
        print("="*60)
        
        if auto_detect:
            print("\n自动检测数据类型...")
            
            for col in self.df_cleaned.columns:
                # 尝试转换为数值类型
                if self.df_cleaned[col].dtype == 'object':
                    try:
                        # 尝试转换为数值
                        converted = pd.to_numeric(self.df_cleaned[col], errors='coerce')
                        if converted.notna().sum() / len(converted) > 0.8:  # 80%以上可转换
                            self.df_cleaned[col] = converted
                            print(f"  [OK] {col}: object -> numeric")
                            continue
                    except:
                        pass
                    
                    # 尝试转换为日期时间
                    try:
                        converted = pd.to_datetime(self.df_cleaned[col], errors='coerce')
                        if converted.notna().sum() / len(converted) > 0.8:
                            self.df_cleaned[col] = converted
                            print(f"  [OK] {col}: object -> datetime")
                            continue
                    except:
                        pass
            
            # 更新数值列和分类列
            self.numeric_cols = self.df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
            self.categorical_cols = self.df_cleaned.select_dtypes(include=['object']).columns.tolist()
            
            print(f"\n转换后:")
            print(f"  数值列 ({len(self.numeric_cols)}): {self.numeric_cols}")
            print(f"  分类列 ({len(self.categorical_cols)}): {self.categorical_cols}")
    
    def generate_cleaning_report(self):
        """
        生成清洗报告
        """
        print("\n" + "="*60)
        print("步骤 7: 生成清洗报告")
        print("="*60)
        
        # 添加最终统计
        self.cleaning_report['清洗后行数'] = self.df_cleaned.shape[0]
        self.cleaning_report['清洗后列数'] = self.df_cleaned.shape[1]
        self.cleaning_report['保留行数比例'] = f"{self.df_cleaned.shape[0] / self.df_original.shape[0] * 100:.2f}%"
        
        # 打印报告
        print("\n【数据清洗报告】")
        print(f"原始数据: {self.cleaning_report['原始行数']} 行 x {self.cleaning_report['原始列数']} 列")
        print(f"清洗后数据: {self.cleaning_report['清洗后行数']} 行 x {self.cleaning_report['清洗后列数']} 列")
        print(f"保留比例: {self.cleaning_report['保留行数比例']}")
        print(f"删除重复行: {self.cleaning_report.get('删除的重复行', 0)} 行")
        print(f"处理后缺失值: {self.cleaning_report.get('处理后缺失值', 0)} 个")
        
        if '删除的列' in self.cleaning_report:
            print(f"删除的列: {self.cleaning_report['删除的列']}")
        
        # 保存报告为文本文件
        report_file = os.path.join(self.output_dir, 'cleaning_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("数据清洗报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"清洗时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"输入文件: {self.input_file}\n\n")
            
            for key, value in self.cleaning_report.items():
                f.write(f"{key}: {value}\n")
        
        print(f"\n[OK] 清洗报告已保存: {report_file}")
    
    def visualize_cleaning_results(self):
        """
        可视化清洗结果
        """
        print("\n" + "="*60)
        print("步骤 8: 生成可视化报告")
        print("="*60)
        
        # 创建对比图
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 数据量对比
        ax1 = axes[0, 0]
        categories = ['原始数据', '清洗后数据']
        values = [self.cleaning_report['原始行数'], self.cleaning_report['清洗后行数']]
        bars = ax1.bar(categories, values, color=['lightcoral', 'lightgreen'], edgecolor='black')
        ax1.set_ylabel('行数', fontsize=12, fontweight='bold')
        ax1.set_title('数据量对比', fontsize=14, fontweight='bold')
        
        # 添加数值标注
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # 2. 缺失值对比
        ax2 = axes[0, 1]
        missing_before = self.df_original.isnull().sum().sum()
        missing_after = self.df_cleaned.isnull().sum().sum()
        categories = ['清洗前', '清洗后']
        values = [missing_before, missing_after]
        bars = ax2.bar(categories, values, color=['lightcoral', 'lightgreen'], edgecolor='black')
        ax2.set_ylabel('缺失值数量', fontsize=12, fontweight='bold')
        ax2.set_title('缺失值对比', fontsize=14, fontweight='bold')
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # 3. 数据类型分布
        ax3 = axes[1, 0]
        dtype_counts = self.df_cleaned.dtypes.value_counts()
        ax3.pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%',
               startangle=90, colors=plt.cm.Set3.colors)
        ax3.set_title('数据类型分布', fontsize=14, fontweight='bold')
        
        # 4. 统计信息
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        stats_text = "清洗统计摘要\n" + "="*30 + "\n\n"
        stats_text += f"原始数据: {self.cleaning_report['原始行数']} 行\n"
        stats_text += f"清洗后数据: {self.cleaning_report['清洗后行数']} 行\n"
        stats_text += f"保留比例: {self.cleaning_report['保留行数比例']}\n\n"
        stats_text += f"删除重复行: {self.cleaning_report.get('删除的重复行', 0)} 行\n"
        stats_text += f"处理缺失值: {missing_before} -> {missing_after}\n\n"
        stats_text += f"数值列: {len(self.numeric_cols)} 个\n"
        stats_text += f"分类列: {len(self.categorical_cols)} 个\n"
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes,
                fontsize=11, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.suptitle('数据清洗结果可视化', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        # 保存图表
        viz_file = os.path.join(self.output_dir, 'cleaning_visualization.png')
        plt.savefig(viz_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"[OK] 可视化报告已保存: {viz_file}")
    
    def save_cleaned_data(self, filename='cleaned_data.csv'):
        """
        保存清洗后的数据
        """
        print("\n" + "="*60)
        print("步骤 9: 保存清洗后的数据")
        print("="*60)
        
        output_file = os.path.join(self.output_dir, filename)
        self.df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"[OK] 清洗后数据已保存: {output_file}")
        print(f"  最终数据形状: {self.df_cleaned.shape}")
        
        # 保存统计信息
        stats_file = os.path.join(self.output_dir, 'statistics.csv')
        stats_df = self.df_cleaned.describe()
        stats_df.to_csv(stats_file, encoding='utf-8-sig')
        print(f"[OK] 统计信息已保存: {stats_file}")
        
        # 显示数据预览
        print("\n【清洗后数据预览】")
        print(self.df_cleaned.head(10))
    
    def clean_all(self, missing_method='auto', outlier_method='iqr', outlier_action='cap'):
        """
        执行完整的清洗流程
        
        参数:
            missing_method: 缺失值处理方法
            outlier_method: 异常值检测方法
            outlier_action: 异常值处理方式
        """
        print("\n" + "="*70)
        print("通用数据清洗 - 开始执行")
        print("="*70)
        
        # 执行清洗步骤
        if not self.load_data():
            return False
        
        self.explore_data()
        self.handle_missing_values(method=missing_method)
        self.remove_duplicates()
        self.handle_outliers(method=outlier_method, action=outlier_action)
        self.convert_data_types()
        self.generate_cleaning_report()
        self.visualize_cleaning_results()
        self.save_cleaned_data()
        
        print("\n" + "="*70)
        print("[SUCCESS] 数据清洗完成！")
        print("="*70)
        
        return True


def main():
    """
    主函数 - 配置区域
    """
    print("="*70)
    print("通用数据清洗脚本 - 美赛第二阶段训练")
    print("="*70)
    
    # ========== 配置区域 - 修改这里 ==========
    
    # 输入文件路径（修改为你的数据文件）
    input_file = r'C:\Users\ASUS\Desktop\Marry_SHANE\deta_from_uci\metro+interstate+traffic+volume\Traffic_Volume.csv'
    
    # 输出目录
    output_dir = r'C:\Users\ASUS\Desktop\Marry_SHANE\deta_cleaning\Metro_Interstate_Traffic_Volume'
    
    # 缺失值处理方法
    # 可选: 'auto', 'drop', 'interpolate', 'mean', 'median', 'mode', 'ffill', 'bfill'
    missing_method = 'auto'
    
    # 异常值检测方法
    # 可选: 'iqr', 'zscore'
    outlier_method = 'iqr'
    
    # 异常值处理方式
    # 可选: 'cap'(截断), 'remove'(删除), 'none'(不处理)
    outlier_action = 'cap'
    
    # ==========================================
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"\n[ERROR] 找不到文件 {input_file}")
        print("\n请修改 input_file 变量为你的数据文件路径")
        print("\n示例:")
        print("  input_file = r'C:\\Users\\YourName\\Desktop\\data.csv'")
        return
    
    # 创建清洗器并执行清洗
    cleaner = UniversalDataCleaner(input_file, output_dir)
    cleaner.clean_all(
        missing_method=missing_method,
        outlier_method=outlier_method,
        outlier_action=outlier_action
    )


if __name__ == "__main__":
    main()
