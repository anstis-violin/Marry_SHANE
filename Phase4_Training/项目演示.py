"""
Phase 4 训练项目 - 演示脚本
运行此脚本可以快速测试所有功能是否正常
"""

import os
import sys

print("=" * 70)
print("美赛第四阶段训练 - 项目演示")
print("=" * 70)
print()

# 检查当前目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")
print()

# 检查项目结构
print("检查项目结构...")
folders = [
    "Day1_3D_Visualization",
    "Day2_Advanced_2D", 
    "Day3_Data_Processing",
    "Day4_5_Model_Evaluation"
]

all_exist = True
for folder in folders:
    exists = os.path.exists(folder)
    status = "✓" if exists else "✗"
    print(f"  {status} {folder}")
    if not exists:
        all_exist = False

print()

if not all_exist:
    print("⚠️ 警告: 部分文件夹不存在，请检查项目结构")
    sys.exit(1)

# 检查Python库
print("检查Python库...")
required_libs = [
    "numpy",
    "pandas", 
    "matplotlib",
    "seaborn",
    "plotly",
    "sklearn",
    "requests",
    "bs4"
]

missing_libs = []
for lib in required_libs:
    try:
        __import__(lib)
        print(f"  ✓ {lib}")
    except ImportError:
        print(f"  ✗ {lib} (未安装)")
        missing_libs.append(lib)

print()

if missing_libs:
    print("⚠️ 警告: 以下库未安装:")
    for lib in missing_libs:
        print(f"  - {lib}")
    print()
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

# 显示项目信息
print("=" * 70)
print("项目信息")
print("=" * 70)
print()
print("📊 项目名称: 美赛第四阶段训练")
print("📝 任务数量: 11个")
print("📁 代码文件: 11个Python脚本 + 1个Jupyter Notebook")
print("⏱️  学习时长: 20-25小时（5天）")
print("📈 输出图表: 40+个专业图表")
print()

print("=" * 70)
print("学习路径")
print("=" * 70)
print()
print("Day 1: 三维可视化 (4-5小时)")
print("  - 任务1.1: 复杂三维场景构建")
print("  - 任务1.2: 交互式三维可视化")
print()
print("Day 2: 高级二维可视化 (4-5小时)")
print("  - 任务2.1: 局部放大图高级应用")
print("  - 任务2.2: 桑基图高级设计")
print("  - 任务2.3: 其他高级二维图表")
print()
print("Day 3: 数据获取和处理 (4-5小时)")
print("  - 任务3.1: 爬虫项目实战")
print("  - 任务3.2: 数据处理和清洗")
print()
print("Day 4-5: 模型评估可视化 (8-10小时)")
print("  - 任务4.1: 混淆矩阵可视化")
print("  - 任务4.2: ROC曲线和AUC可视化")
print("  - 任务4.3: 学习曲线可视化")
print("  - 任务4.4: 模型性能综合可视化")
print()

print("=" * 70)
print("快速开始")
print("=" * 70)
print()
print("方法1: 使用启动菜单（推荐）")
print("  双击运行: 启动菜单.bat")
print()
print("方法2: 命令行运行")
print("  python Day1_3D_Visualization/task1_complex_3d_scene.py")
print()
print("方法3: 查看文档")
print("  - README.md - 项目概述")
print("  - 使用指南.md - 详细教程")
print("  - 项目总结.md - 完成总结")
print("  - 快速参考.md - 快速参考")
print()

print("=" * 70)
print("✅ 项目检查完成！所有依赖已就绪，可以开始学习了！")
print("=" * 70)
print()
print("💡 提示: 建议按照Day 1 → Day 2 → Day 3 → Day 4-5的顺序学习")
print("🎯 目标: 掌握三维可视化、高级二维可视化、数据处理和模型评估")
print("🏆 祝您学习顺利，在美赛中取得优异成绩！")
print()
