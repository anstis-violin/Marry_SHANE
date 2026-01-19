@echo off
chcp 65001 >nul
echo ============================================================
echo 美赛第四阶段训练 - 快速启动菜单
echo ============================================================
echo.

:menu
echo 请选择要运行的任务:
echo.
echo [Day 1 - 三维可视化]
echo   1. 任务1.1 - 复杂三维场景构建
echo   2. 任务1.2 - 交互式三维可视化 (Jupyter Notebook)
echo.
echo [Day 2 - 高级二维可视化]
echo   3. 任务2.1 - 局部放大图高级应用
echo   4. 任务2.2 - 桑基图高级设计
echo   5. 任务2.3 - 其他高级二维图表
echo.
echo [Day 3 - 数据获取和处理]
echo   6. 任务3.1 - 爬虫项目实战
echo   7. 任务3.2 - 数据处理和清洗
echo.
echo [Day 4-5 - 模型评估可视化]
echo   8. 任务4.1 - 混淆矩阵可视化
echo   9. 任务4.2 - ROC曲线和AUC可视化
echo   10. 任务4.3 - 学习曲线可视化
echo   11. 任务4.4 - 模型性能综合可视化
echo.
echo [其他选项]
echo   12. 运行所有任务
echo   13. 安装依赖包
echo   0. 退出
echo.
echo ============================================================

set /p choice="请输入选项编号: "

if "%choice%"=="1" (
    echo.
    echo 正在运行任务1.1...
    python Day1_3D_Visualization\task1_complex_3d_scene.py
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 正在打开Jupyter Notebook...
    echo 请在VSCode中打开: Day1_3D_Visualization\task2_interactive_3d.ipynb
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo 正在运行任务2.1...
    python Day2_Advanced_2D\task1_zoom_inset.py
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 正在运行任务2.2...
    python Day2_Advanced_2D\task2_sankey_diagram.py
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 正在运行任务2.3...
    python Day2_Advanced_2D\task3_other_charts.py
    pause
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo 正在运行任务3.1...
    python Day3_Data_Processing\task1_web_scraper.py
    pause
    goto menu
)

if "%choice%"=="7" (
    echo.
    echo 正在运行任务3.2...
    python Day3_Data_Processing\task2_data_cleaning.py
    pause
    goto menu
)

if "%choice%"=="8" (
    echo.
    echo 正在运行任务4.1...
    python Day4_5_Model_Evaluation\task1_confusion_matrix.py
    pause
    goto menu
)

if "%choice%"=="9" (
    echo.
    echo 正在运行任务4.2...
    python Day4_5_Model_Evaluation\task2_roc_curve.py
    pause
    goto menu
)

if "%choice%"=="10" (
    echo.
    echo 正在运行任务4.3...
    python Day4_5_Model_Evaluation\task3_learning_curve.py
    pause
    goto menu
)

if "%choice%"=="11" (
    echo.
    echo 正在运行任务4.4...
    python Day4_5_Model_Evaluation\task4_comprehensive.py
    pause
    goto menu
)

if "%choice%"=="12" (
    echo.
    echo 正在运行所有任务...
    echo.
    echo [1/11] Day 1 - 任务1.1
    python Day1_3D_Visualization\task1_complex_3d_scene.py
    echo.
    echo [2/11] Day 2 - 任务2.1
    python Day2_Advanced_2D\task1_zoom_inset.py
    echo.
    echo [3/11] Day 2 - 任务2.2
    python Day2_Advanced_2D\task2_sankey_diagram.py
    echo.
    echo [4/11] Day 2 - 任务2.3
    python Day2_Advanced_2D\task3_other_charts.py
    echo.
    echo [5/11] Day 3 - 任务3.1
    python Day3_Data_Processing\task1_web_scraper.py
    echo.
    echo [6/11] Day 3 - 任务3.2
    python Day3_Data_Processing\task2_data_cleaning.py
    echo.
    echo [7/11] Day 4-5 - 任务4.1
    python Day4_5_Model_Evaluation\task1_confusion_matrix.py
    echo.
    echo [8/11] Day 4-5 - 任务4.2
    python Day4_5_Model_Evaluation\task2_roc_curve.py
    echo.
    echo [9/11] Day 4-5 - 任务4.3
    python Day4_5_Model_Evaluation\task3_learning_curve.py
    echo.
    echo [10/11] Day 4-5 - 任务4.4
    python Day4_5_Model_Evaluation\task4_comprehensive.py
    echo.
    echo ============================================================
    echo ✅ 所有任务已完成！
    echo ============================================================
    pause
    goto menu
)

if "%choice%"=="13" (
    echo.
    echo 正在安装依赖包...
    pip install -r requirements.txt
    echo.
    echo 依赖包安装完成！
    pause
    goto menu
)

if "%choice%"=="0" (
    echo.
    echo 感谢使用！再见！
    exit
)

echo.
echo 无效的选项，请重新选择！
pause
goto menu
