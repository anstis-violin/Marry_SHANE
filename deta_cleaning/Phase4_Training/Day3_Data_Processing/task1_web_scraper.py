"""
Day 3 - 任务3.1: 爬虫项目实战
完整的爬虫项目：爬取豆瓣电影Top250
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime

print("=" * 60)
print("Day 3 - 任务3.1: 爬虫项目实战")
print("项目：爬取豆瓣电影Top250")
print("=" * 60)

# ============================================================================
# 1. 项目规划
# ============================================================================
print("\n[步骤1] 项目规划...")
print("目标网站: 豆瓣电影Top250")
print("爬取内容: 电影名称、评分、评价人数、导演、年份、类型等")
print("数据量: 250部电影")
print("存储格式: CSV和JSON")

# ============================================================================
# 2. 爬虫实现
# ============================================================================

class DoubanMovieCrawler:
    """豆瓣电影爬虫类"""
    
    def __init__(self):
        self.base_url = "https://movie.douban.com/top250"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.movies = []
        
    def get_page(self, start):
        """获取单页数据"""
        try:
            params = {'start': start, 'filter': ''}
            response = requests.get(self.base_url, headers=self.headers, 
                                   params=params, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"  ✗ 请求失败: {e}")
            return None
    
    def parse_page(self, html):
        """解析页面数据"""
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='item')
        
        page_movies = []
        for item in items:
            try:
                # 电影名称
                title = item.find('span', class_='title').text
                
                # 评分
                rating = item.find('span', class_='rating_num').text
                
                # 评价人数
                rating_people = item.find('div', class_='star').find_all('span')[-1].text
                rating_people = rating_people.replace('人评价', '')
                
                # 导演和主演
                info = item.find('div', class_='bd').find('p').text.strip()
                info_lines = [line.strip() for line in info.split('\n') if line.strip()]
                director_actors = info_lines[0] if info_lines else ''
                
                # 年份和类型
                year_type = info_lines[1] if len(info_lines) > 1 else ''
                
                # 引言
                quote_tag = item.find('span', class_='inq')
                quote = quote_tag.text if quote_tag else ''
                
                movie = {
                    '电影名称': title,
                    '评分': float(rating),
                    '评价人数': int(rating_people),
                    '导演和主演': director_actors,
                    '年份和类型': year_type,
                    '引言': quote
                }
                page_movies.append(movie)
                
            except Exception as e:
                print(f"  ✗ 解析电影信息失败: {e}")
                continue
        
        return page_movies
    
    def crawl(self):
        """执行爬取"""
        print("\n[步骤2] 开始爬取数据...")
        
        # 豆瓣Top250共10页，每页25部电影
        for page in range(10):
            start = page * 25
            print(f"\n正在爬取第 {page + 1}/10 页 (start={start})...")
            
            # 获取页面
            html = self.get_page(start)
            if not html:
                print(f"  ✗ 第{page + 1}页获取失败，跳过")
                continue
            
            # 解析数据
            page_movies = self.parse_page(html)
            self.movies.extend(page_movies)
            print(f"  ✓ 成功爬取 {len(page_movies)} 部电影")
            
            # 礼貌性延迟
            time.sleep(1)
        
        print(f"\n✓ 爬取完成！共获取 {len(self.movies)} 部电影数据")
        return self.movies
    
    def save_data(self):
        """保存数据"""
        print("\n[步骤3] 保存数据...")
        
        # 保存为CSV
        df = pd.DataFrame(self.movies)
        csv_file = 'Day3_Data_Processing/douban_top250.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"  ✓ 已保存CSV: {csv_file}")
        
        # 保存为JSON
        json_file = 'Day3_Data_Processing/douban_top250.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 已保存JSON: {json_file}")
        
        # 生成数据报告
        self.generate_report(df)
    
    def generate_report(self, df):
        """生成数据报告"""
        print("\n[步骤4] 生成数据报告...")
        
        report = f"""
{'=' * 60}
豆瓣电影Top250 数据报告
{'=' * 60}

爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据总量: {len(df)} 部电影

评分统计:
  - 平均评分: {df['评分'].mean():.2f}
  - 最高评分: {df['评分'].max():.2f}
  - 最低评分: {df['评分'].min():.2f}

评价人数统计:
  - 平均评价人数: {df['评价人数'].mean():.0f}
  - 最多评价人数: {df['评价人数'].max()}
  - 最少评价人数: {df['评价人数'].min()}

评分分布:
  - 9.0分以上: {len(df[df['评分'] >= 9.0])} 部
  - 8.5-9.0分: {len(df[(df['评分'] >= 8.5) & (df['评分'] < 9.0)])} 部
  - 8.0-8.5分: {len(df[(df['评分'] >= 8.0) & (df['评分'] < 8.5)])} 部
  - 8.0分以下: {len(df[df['评分'] < 8.0])} 部

Top 5 高分电影:
"""
        
        top5 = df.nlargest(5, '评分')[['电影名称', '评分', '评价人数']]
        for idx, row in top5.iterrows():
            report += f"  {idx+1}. {row['电影名称']} - {row['评分']}分 ({row['评价人数']}人评价)\n"
        
        report += "\n" + "=" * 60
        
        print(report)
        
        # 保存报告
        report_file = 'Day3_Data_Processing/douban_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ 报告已保存: {report_file}")

# ============================================================================
# 3. 执行爬虫
# ============================================================================

if __name__ == "__main__":
    # 创建爬虫实例
    crawler = DoubanMovieCrawler()
    
    # 执行爬取
    movies = crawler.crawl()
    
    # 保存数据
    if movies:
        crawler.save_data()
        
        print("\n" + "=" * 60)
        print("✅ Day 3 - 任务3.1 完成！")
        print("已生成文件:")
        print("  1. douban_top250.csv - CSV格式数据")
        print("  2. douban_top250.json - JSON格式数据")
        print("  3. douban_report.txt - 数据分析报告")
        print("=" * 60)
    else:
        print("\n✗ 爬取失败，未获取到数据")

# ============================================================================
# 备注：如果豆瓣网站无法访问，可以使用模拟数据
# ============================================================================

def generate_mock_data():
    """生成模拟数据（用于演示）"""
    print("\n[备用方案] 生成模拟数据...")
    
    import random
    
    movie_names = [
        '肖申克的救赎', '霸王别姬', '阿甘正传', '泰坦尼克号', '这个杀手不太冷',
        '美丽人生', '千与千寻', '辛德勒的名单', '盗梦空间', '忠犬八公的故事',
        '海上钢琴师', '三傻大闹宝莱坞', '放牛班的春天', '楚门的世界', '大话西游',
        '教父', '龙猫', '当幸福来敲门', '怦然心动', '触不可及'
    ]
    
    movies = []
    for i, name in enumerate(movie_names):
        movie = {
            '电影名称': name,
            '评分': round(random.uniform(8.5, 9.7), 1),
            '评价人数': random.randint(100000, 2000000),
            '导演和主演': f'导演{i+1} / 主演{i+1}',
            '年份和类型': f'{random.randint(1990, 2020)} / 剧情',
            '引言': f'这是一部优秀的电影{i+1}'
        }
        movies.append(movie)
    
    # 保存模拟数据
    df = pd.DataFrame(movies)
    df.to_csv('Day3_Data_Processing/douban_top250_mock.csv', index=False, encoding='utf-8-sig')
    
    with open('Day3_Data_Processing/douban_top250_mock.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已生成模拟数据: {len(movies)} 部电影")
    print("  - douban_top250_mock.csv")
    print("  - douban_top250_mock.json")

# 如果需要使用模拟数据，取消下面的注释
# generate_mock_data()
