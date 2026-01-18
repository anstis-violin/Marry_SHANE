@echo off
chcp 65001 >nul
echo ============================================================
echo B站数据分析项目 - 一键运行
echo ============================================================
echo.

echo [步骤1/3] 爬取数据...
echo.
python crawler.py
if errorlevel 1 (
    echo.
    echo × 数据爬取失败！
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [步骤2/3] 生成二维可视化图表...
echo.
python visualize_2d.py
if errorlevel 1 (
    echo.
    echo × 二维可视化失败！
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [步骤3/3] 生成三维可视化图表...
echo.
python visualize_3d.py
if errorlevel 1 (
    echo.
    echo × 三维可视化失败！
    pause
    exit /b 1
)

echo.
echo ============================================================
echo √ 所有任务完成！
echo ============================================================
echo.
echo 已生成文件:
echo   - data/bilibili_data.csv
echo   - data/bilibili_data.json
echo   - data/bilibili_report.txt
echo   - visualizations/ 目录下的10个图表
echo.
echo 请查看 visualizations 文件夹查看生成的图表
echo.
pause
