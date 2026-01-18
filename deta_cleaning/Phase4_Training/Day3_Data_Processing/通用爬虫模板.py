"""
通用爬虫模板 - 可以修改为爬取任何网站
使用说明：
1. 修改 base_url 为目标网站
2. 修改 parse_page 方法中的选择器
3. 修改 crawl 方法中的分页逻辑
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime

class GenericWebCrawler:
    """通用网页爬虫类"""
    
    def __init__(self, base_url, target_name="数据"):
        """
        初始化爬虫
        
        参数:
            base_url: 目标网站的URL
            target_name: 爬取目标的名称（用于显示）
        """
        # ========== 在这里修改目标网站 ==========
        self.base_url = base_url
        self.target_name = target_name
        # =======================================
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.data_list = []
        
    def get_page(self, url):
        """获取页面内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except requests.RequestException as e:
            print(f"  ✗ 请求失败: {e}")
            return None
    
    def parse_page(self, html):
        """
        解析页面数据
        
        ========== 重要：根据目标网站修改这里 ==========
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # 示例1: 爬取列表项
        # items = soup.find_all('div', class_='item-class')
        
        # 示例2: 爬取表格
        # items = soup.find('table').find_all('tr')[1:]  # 跳过表头
        
        # 示例3: 爬取文章
        # items = soup.find_all('article')
        
        # ========== 修改选择器 ==========
        items = soup.find_all('div', class_='your-target-class')
        # ================================
        
        page_data = []
        for item in items:
            try:
                # ========== 根据需要提取的字段修改 ==========
                data = {
                    '标题': item.find('h2').text.strip() if item.find('h2') else '',
                    '内容': item.find('p').text.strip() if item.find('p') else '',
                    '链接': item.find('a')['href'] if item.find('a') else '',
                    # 添加更多字段...
                }
                # ==========================================
                
                page_data.append(data)
                
            except Exception as e:
                print(f"  ✗ 解析项目失败: {e}")
                continue
        
        return page_data
    
    def crawl(self, num_pages=5, delay=1):
        """
        执行爬取
        
        参数:
            num_pages: 要爬取的页数
            delay: 每次请求之间的延迟（秒）
        """
        print(f"\n开始爬取 {self.target_name}...")
        print(f"目标网站: {self.base_url}")
        print(f"计划爬取: {num_pages} 页")
        print("=" * 60)
        
        for page in range(num_pages):
            # ========== 根据网站的分页方式修改 ==========
            
            # 方式1: 使用start参数（如豆瓣）
            # url = f"{self.base_url}?start={page * 25}"
            
            # 方式2: 使用page参数
            # url = f"{self.base_url}?page={page + 1}"
            
            # 方式3: 使用路径参数
            # url = f"{self.base_url}/page/{page + 1}"
            
            # 方式4: 固定URL（不分页）
            url = self.base_url
            # ===========================================
            
            print(f"\n正在爬取第 {page + 1}/{num_pages} 页...")
            print(f"URL: {url}")
            
            # 获取页面
            html = self.get_page(url)
            if not html:
                print(f"  ✗ 第{page + 1}页获取失败，跳过")
                continue
            
            # 解析数据
            page_data = self.parse_page(html)
            self.data_list.extend(page_data)
            print(f"  ✓ 成功爬取 {len(page_data)} 条数据")
            
            # 礼貌性延迟
            if page < num_pages - 1:
                time.sleep(delay)
        
        print(f"\n✓ 爬取完成！共获取 {len(self.data_list)} 条数据")
        return self.data_list
    
    def save_data(self, output_dir='Day3_Data_Processing', filename='crawled_data'):
        """保存数据"""
        if not self.data_list:
            print("⚠️ 没有数据可保存")
            return
        
        print("\n保存数据...")
        
        # 保存为CSV
        df = pd.DataFrame(self.data_list)
        csv_file = f'{output_dir}/{filename}.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"  ✓ 已保存CSV: {csv_file}")
        
        # 保存为JSON
        json_file = f'{output_dir}/{filename}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data_list, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 已保存JSON: {json_file}")
        
        # 生成简单报告
        self.generate_report(df, output_dir, filename)
    
    def generate_report(self, df, output_dir, filename):
        """生成数据报告"""
        report = f"""
{'=' * 60}
{self.target_name} 爬取报告
{'=' * 60}

爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
目标网站: {self.base_url}
数据总量: {len(df)} 条

数据字段: {', '.join(df.columns.tolist())}

{'=' * 60}
"""
        
        print(report)
        
        # 保存报告
        report_file = f'{output_dir}/{filename}_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"  ✓ 报告已保存: {report_file}")


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("通用爬虫模板 - 使用示例")
    print("=" * 60)
    
    # ========== 在这里配置您的爬虫 ==========
    
    # 示例1: 爬取豆瓣电影
    crawler = GenericWebCrawler(
        base_url="https://www.bilibili.com/v/popular/rank/all",
        target_name="哔哩哔哩排行榜"
    )
    
    # 示例2: 爬取其他网站（取消注释使用）
    # crawler = GenericWebCrawler(
    #     base_url="https://你的目标网站.com",
    #     target_name="网站名称"
    # )
    
    # =======================================
    
    # 执行爬取
    data = crawler.crawl(
        num_pages=3,    # 爬取页数
        delay=1         # 延迟秒数
    )
    
    # 保存数据
    if data:
        crawler.save_data(
            output_dir='Day3_Data_Processing',
            filename='my_crawled_data'
        )
        print("\n✅ 爬虫任务完成！")
    else:
        print("\n✗ 爬取失败，未获取到数据")
    
    print("\n" + "=" * 60)
    print("💡 提示：")
    print("1. 修改 base_url 为您的目标网站")
    print("2. 修改 parse_page 方法中的选择器")
    print("3. 修改 crawl 方法中的URL构建方式")
    print("4. 运行脚本开始爬取")
    print("=" * 60)
