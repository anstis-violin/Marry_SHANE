"""
高质量数据可视化脚本 - 美赛第二阶段
Advanced Data Visualization for MCM Training Phase 2

功能：
1. 添加数值标注和统计信息
2. 10+种图表类型
3. 趋势线和相关性分析
4. 300 DPI高清输出
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import os

# 设置中文显示 - 强制使用微软雅黑
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'KaiTi', 'FangSong']
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'KaiTi', 'FangSong']
plt.rcParams['axes.unicode_minus'] = False

# 设置seaborn样式
sns.set_style("whitegrid")
sns.set_palette("husl")


class AdvancedVisualizer:
    """高级可视化类"""
    
    def __init__(self, df, output_dir='./figures/'):
        """
        初始化
        
        参数:
            df: 清洗后的数据DataFrame
            output_dir: 图表输出目录
        """
        self.df = df
        self.output_dir = output_dir
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        # 获取数值列
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        print(f"数据形状: {df.shape}")
        print(f"数值列数量: {len(self.numeric_cols)}")
    
    def plot_bar_with_annotations(self, column, top_n=10):
        """
        图表1: 带数值标注和平均线的柱状图
        """
        print("\n[1/10] 生成带标注的柱状图...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 计算平均值（按天或按小时）
        if isinstance(self.df.index, pd.DatetimeIndex):
            data = self.df[column].resample('D').mean().dropna().head(top_n)
        else:
            data = self.df[column].dropna().head(top_n)
        
        # 绘制柱状图
        bars = ax.bar(range(len(data)), data.values, color='steelblue', alpha=0.8, edgecolor='black')
        
        # 添加数值标注
        for i, (bar, value) in enumerate(zip(bars, data.values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 添加平均线
        mean_value = data.mean()
        ax.axhline(y=mean_value, color='red', linestyle='--', linewidth=2, 
                   label=f'平均值: {mean_value:.2f}')
        
        # 添加统计信息框
        stats_text = f'统计信息:\n'
        stats_text += f'均值: {data.mean():.2f}\n'
        stats_text += f'中位数: {data.median():.2f}\n'
        stats_text += f'标准差: {data.std():.2f}\n'
        stats_text += f'最大值: {data.max():.2f}\n'
        stats_text += f'最小值: {data.min():.2f}'
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # 设置标签
        ax.set_xlabel('时间/索引', fontsize=12, fontweight='bold')
        ax.set_ylabel(column, fontsize=12, fontweight='bold')
        ax.set_title(f'{column} - 柱状图（带数值标注）', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}01_bar_with_annotations.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 01_bar_with_annotations.png")
    
    def plot_scatter_with_trendline(self, col_x, col_y):
        """
        图表2: 带趋势线和统计信息的散点图
        """
        print("\n[2/10] 生成带趋势线的散点图...")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 准备数据（去除缺失值）
        data = self.df[[col_x, col_y]].dropna()
        x = data[col_x].values
        y = data[col_y].values
        
        # 绘制散点图
        scatter = ax.scatter(x, y, alpha=0.6, s=30, c='steelblue', edgecolors='black', linewidth=0.5)
        
        # 计算并绘制趋势线
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", linewidth=2, label=f'趋势线: y={z[0]:.4f}x+{z[1]:.4f}')
        
        # 计算统计指标
        correlation = np.corrcoef(x, y)[0, 1]
        r_squared = correlation ** 2
        
        # 添加统计信息框
        stats_text = f'统计信息:\n'
        stats_text += f'相关系数 (r): {correlation:.4f}\n'
        stats_text += f'R²: {r_squared:.4f}\n'
        stats_text += f'{col_x} 均值: {x.mean():.2f}\n'
        stats_text += f'{col_y} 均值: {y.mean():.2f}\n'
        stats_text += f'{col_x} 标准差: {x.std():.2f}\n'
        stats_text += f'{col_y} 标准差: {y.std():.2f}\n'
        stats_text += f'样本数: {len(x)}'
        
        ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 设置标签
        ax.set_xlabel(col_x, fontsize=12, fontweight='bold')
        ax.set_ylabel(col_y, fontsize=12, fontweight='bold')
        ax.set_title(f'{col_x} vs {col_y} - 散点图（带趋势线）', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}02_scatter_with_trendline.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 02_scatter_with_trendline.png")
    
    def plot_timeseries_with_annotations(self, column):
        """
        图表3: 带关键点标注的时间序列图
        """
        print("\n[3/10] 生成带标注的时间序列图...")
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # 准备数据
        if isinstance(self.df.index, pd.DatetimeIndex):
            data = self.df[column].dropna()
        else:
            data = self.df[column].dropna()
        
        # 绘制时间序列
        ax.plot(data.index, data.values, linewidth=1.5, color='steelblue', label=column)
        
        # 标注最大值
        max_idx = data.idxmax()
        max_val = data.max()
        ax.annotate(f'最大值: {max_val:.2f}',
                   xy=(max_idx, max_val),
                   xytext=(10, 20), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='red', lw=2))
        
        # 标注最小值
        min_idx = data.idxmin()
        min_val = data.min()
        ax.annotate(f'最小值: {min_val:.2f}',
                   xy=(min_idx, min_val),
                   xytext=(10, -30), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='green', lw=2))
        
        # 添加平均线
        mean_val = data.mean()
        ax.axhline(y=mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'平均值: {mean_val:.2f}')
        
        # 添加统计信息框
        stats_text = f'统计信息:\n'
        stats_text += f'均值: {data.mean():.2f}\n'
        stats_text += f'标准差: {data.std():.2f}\n'
        stats_text += f'最大值: {max_val:.2f}\n'
        stats_text += f'最小值: {min_val:.2f}\n'
        stats_text += f'数据点数: {len(data)}'
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # 设置标签
        ax.set_xlabel('时间', fontsize=12, fontweight='bold')
        ax.set_ylabel(column, fontsize=12, fontweight='bold')
        ax.set_title(f'{column} - 时间序列图（带关键点标注）', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}03_timeseries_with_annotations.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 03_timeseries_with_annotations.png")
    
    def plot_correlation_heatmap(self):
        """
        图表4: 相关性热力图
        """
        print("\n[4/10] 生成相关性热力图...")
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 计算相关性矩阵
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # 绘制热力图
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax)
        
        ax.set_title('特征相关性热力图', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}04_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 04_correlation_heatmap.png")
    
    def plot_boxplot_comparison(self, columns=None):
        """
        图表5: 箱线图对比（数据分布）
        """
        print("\n[5/10] 生成箱线图...")
        
        if columns is None:
            columns = self.numeric_cols[:6]  # 选择前6个数值列
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 准备数据
        data_to_plot = [self.df[col].dropna().values for col in columns]
        
        # 绘制箱线图
        bp = ax.boxplot(data_to_plot, labels=columns, patch_artist=True,
                       notch=True, showmeans=True)
        
        # 美化箱线图
        colors = plt.cm.Set3(np.linspace(0, 1, len(columns)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # 添加统计信息
        for i, col in enumerate(columns):
            data = self.df[col].dropna()
            median = data.median()
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            
            # 在箱线图上方添加统计信息
            ax.text(i+1, q3, f'Q3:{q3:.1f}', ha='center', va='bottom', fontsize=8)
            ax.text(i+1, median, f'中位:{median:.1f}', ha='center', va='center', 
                   fontsize=8, fontweight='bold', color='red')
            ax.text(i+1, q1, f'Q1:{q1:.1f}', ha='center', va='top', fontsize=8)
        
        ax.set_xlabel('特征', fontsize=12, fontweight='bold')
        ax.set_ylabel('数值', fontsize=12, fontweight='bold')
        ax.set_title('各特征箱线图对比', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}05_boxplot_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 05_boxplot_comparison.png")
    
    def plot_violin_plot(self, columns=None):
        """
        图表6: 小提琴图（分布形状）
        """
        print("\n[6/10] 生成小提琴图...")
        
        if columns is None:
            columns = self.numeric_cols[:4]  # 选择前4个数值列
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 准备数据（转换为长格式）
        data_list = []
        for col in columns:
            temp_df = pd.DataFrame({
                'value': self.df[col].dropna().values,
                'variable': col
            })
            data_list.append(temp_df)
        
        plot_data = pd.concat(data_list, ignore_index=True)
        
        # 绘制小提琴图
        sns.violinplot(data=plot_data, x='variable', y='value', ax=ax, palette='Set2')
        
        # 添加统计信息
        for i, col in enumerate(columns):
            data = self.df[col].dropna()
            mean_val = data.mean()
            ax.plot(i, mean_val, 'ro', markersize=8, label='均值' if i == 0 else '')
        
        ax.set_xlabel('特征', fontsize=12, fontweight='bold')
        ax.set_ylabel('数值', fontsize=12, fontweight='bold')
        ax.set_title('各特征小提琴图（分布密度）', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}06_violin_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 06_violin_plot.png")
    
    def plot_stacked_area(self, columns=None, resample='D'):
        """
        图表7: 堆叠面积图（时间序列多变量）
        """
        print("\n[7/10] 生成堆叠面积图...")
        
        if not isinstance(self.df.index, pd.DatetimeIndex):
            print("  [!] 警告: 数据没有时间索引，跳过堆叠面积图")
            return
        
        if columns is None:
            columns = self.numeric_cols[:4]  # 选择前4个数值列
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # 重采样数据
        data = self.df[columns].resample(resample).mean().dropna()
        
        # 绘制堆叠面积图
        ax.stackplot(data.index, *[data[col].values for col in columns],
                    labels=columns, alpha=0.7)
        
        ax.set_xlabel('时间', fontsize=12, fontweight='bold')
        ax.set_ylabel('数值', fontsize=12, fontweight='bold')
        ax.set_title('时间序列堆叠面积图', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}07_stacked_area.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 07_stacked_area.png")
    
    def plot_histogram_with_kde(self, column):
        """
        图表8: 直方图+核密度估计
        """
        print("\n[8/10] 生成直方图+KDE...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        data = self.df[column].dropna()
        
        # 绘制直方图
        n, bins, patches = ax.hist(data, bins=30, alpha=0.7, color='steelblue', 
                                   edgecolor='black', density=True, label='直方图')
        
        # 绘制KDE曲线
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 100)
        ax.plot(x_range, kde(x_range), 'r-', linewidth=2, label='核密度估计')
        
        # 添加均值线
        mean_val = data.mean()
        ax.axvline(mean_val, color='green', linestyle='--', linewidth=2, 
                  label=f'均值: {mean_val:.2f}')
        
        # 添加中位数线
        median_val = data.median()
        ax.axvline(median_val, color='orange', linestyle='--', linewidth=2,
                  label=f'中位数: {median_val:.2f}')
        
        # 添加统计信息框
        stats_text = f'统计信息:\n'
        stats_text += f'均值: {data.mean():.2f}\n'
        stats_text += f'中位数: {data.median():.2f}\n'
        stats_text += f'标准差: {data.std():.2f}\n'
        stats_text += f'偏度: {data.skew():.2f}\n'
        stats_text += f'峰度: {data.kurtosis():.2f}'
        
        ax.text(0.98, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.set_xlabel(column, fontsize=12, fontweight='bold')
        ax.set_ylabel('密度', fontsize=12, fontweight='bold')
        ax.set_title(f'{column} - 分布直方图+KDE', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}08_histogram_kde.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 08_histogram_kde.png")
    
    def plot_pairplot(self, columns=None):
        """
        图表9: 成对关系图
        """
        print("\n[9/10] 生成成对关系图...")
        
        if columns is None:
            columns = self.numeric_cols[:4]  # 选择前4个数值列
        
        # 使用seaborn的pairplot
        data_subset = self.df[columns].dropna()
        
        g = sns.pairplot(data_subset, diag_kind='kde', plot_kws={'alpha': 0.6, 's': 30},
                        diag_kws={'linewidth': 2})
        
        g.fig.suptitle('特征成对关系图', fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}09_pairplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 09_pairplot.png")
    
    def plot_radar_chart(self, columns=None):
        """
        图表10: 雷达图（多维度对比）
        """
        print("\n[10/10] 生成雷达图...")
        
        if columns is None:
            columns = self.numeric_cols[:6]  # 选择前6个数值列
        
        # 计算每列的均值并归一化
        values = []
        for col in columns:
            mean_val = self.df[col].mean()
            values.append(mean_val)
        
        # 归一化到0-1
        values = np.array(values)
        values_norm = (values - values.min()) / (values.max() - values.min())
        
        # 设置雷达图
        angles = np.linspace(0, 2 * np.pi, len(columns), endpoint=False).tolist()
        values_norm = values_norm.tolist()
        
        # 闭合图形
        angles += angles[:1]
        values_norm += values_norm[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # 绘制雷达图
        ax.plot(angles, values_norm, 'o-', linewidth=2, color='steelblue', label='归一化均值')
        ax.fill(angles, values_norm, alpha=0.25, color='steelblue')
        
        # 设置标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(columns, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.grid(True)
        
        # 添加原始数值标注
        for angle, value, orig_value, col in zip(angles[:-1], values_norm[:-1], values, columns):
            ax.text(angle, value + 0.1, f'{orig_value:.1f}', 
                   ha='center', va='center', fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        ax.set_title('特征雷达图（多维度对比）', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}10_radar_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[OK] 保存: 10_radar_chart.png")
    
    def generate_statistics_report(self):
        """
        生成统计报告
        """
        print("\n" + "="*50)
        print("生成统计报告...")
        print("="*50)
        
        # 计算关键统计指标
        stats_dict = {
            '计数': self.df[self.numeric_cols].count(),
            '均值': self.df[self.numeric_cols].mean(),
            '中位数': self.df[self.numeric_cols].median(),
            '标准差': self.df[self.numeric_cols].std(),
            '最小值': self.df[self.numeric_cols].min(),
            '25%分位数': self.df[self.numeric_cols].quantile(0.25),
            '75%分位数': self.df[self.numeric_cols].quantile(0.75),
            '最大值': self.df[self.numeric_cols].max(),
            '偏度': self.df[self.numeric_cols].skew(),
            '峰度': self.df[self.numeric_cols].kurtosis()
        }
        
        stats_df = pd.DataFrame(stats_dict).T
        
        # 保存为CSV
        stats_df.to_csv(f'{self.output_dir}statistics_report.csv', encoding='utf-8-sig')
        print(f"[OK] 保存统计报告: statistics_report.csv")
        
        # 打印统计报告
        print("\n统计报告预览:")
        print(stats_df.round(2))
        
        return stats_df
    
    def generate_all_visualizations(self):
        """
        生成所有可视化图表
        """
        print("\n" + "="*60)
        print("开始生成高质量可视化图表")
        print("="*60)
        
        # 选择合适的列进行可视化
        if len(self.numeric_cols) >= 2:
            col1 = self.numeric_cols[0]
            col2 = self.numeric_cols[1]
        else:
            print("错误: 数值列不足，无法生成可视化")
            return
        
        # 生成10种图表
        self.plot_bar_with_annotations(col1)
        self.plot_scatter_with_trendline(col1, col2)
        self.plot_timeseries_with_annotations(col1)
        self.plot_correlation_heatmap()
        self.plot_boxplot_comparison()
        self.plot_violin_plot()
        self.plot_stacked_area()
        self.plot_histogram_with_kde(col1)
        self.plot_pairplot()
        self.plot_radar_chart()
        
        # 生成统计报告
        self.generate_statistics_report()
        
        print("\n" + "="*60)
        print("[SUCCESS] 所有可视化图表生成完成！")
        print(f"输出目录: {self.output_dir}")
        print("="*60)


def main():
    """
    主函数
    """
    print("="*60)
    print("高质量数据可视化 - 美赛第二阶段训练")
    print("="*60)
    
    # ========== 配置区域 - 修改这里来使用不同的数据 ==========
    
    # 数据文件路径（修改这里！）
    data_file = r'C:\Users\ASUS\Desktop\Marry_SHANE\deta_cleaning\Metro_Interstate_Traffic_Volume\cleaned_data.csv'
    
    # 输出目录（修改这里！）
    output_dir = r'C:\Users\ASUS\Desktop\Marry_SHANE\deta_cleaning\Metro_Interstate_Traffic_Volume\figures\\'
    
    # 是否有时间索引（如果数据第一列是日期时间，设为True）
    has_time_index = False  # 交通数据的时间列不在第一列
    
    # 时间列的索引位置（如果has_time_index=True，指定哪一列是时间）
    time_column = 0  # 0表示第一列
    
    # =====================================================
    
    if not os.path.exists(data_file):
        print(f"\n错误: 找不到数据文件 {data_file}")
        print("请检查文件路径是否正确")
        return
    
    print(f"\n加载数据: {data_file}")
    
    # 根据配置加载数据
    if has_time_index:
        df = pd.read_csv(data_file, index_col=time_column, parse_dates=True)
    else:
        df = pd.read_csv(data_file)
    
    print(f"数据形状: {df.shape}")
    print(f"数据列: {df.columns.tolist()}")
    
    # 2. 创建可视化器
    visualizer = AdvancedVisualizer(df, output_dir=output_dir)
    
    # 3. 生成所有可视化
    visualizer.generate_all_visualizations()
    
    print("\n" + "="*60)
    print("程序执行完成！")
    print("="*60)


if __name__ == "__main__":
    main()
