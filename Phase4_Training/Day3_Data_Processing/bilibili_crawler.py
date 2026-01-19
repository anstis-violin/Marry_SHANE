"""
B站热门视频爬虫
爬取B站全站排行榜数据
"""

import sys
import io

# 解决Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime

print("=" * 60)
print("B站热门视频爬虫")
print("=" * 60)

class BilibiliCrawler:
    """B站视频爬虫类"""
    
    def __init__(self):
        # B站排行榜API（更稳定）
        self.api_url = "https://api.bilibili.com/x/web-interface/ranking/v2"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com',
            'Accept': 'application/json, text/plain, */*',
        }
        self.videos = []
        
    def get_ranking_data(self, rid=0, day=3):
        """
        获取排行榜数据
        
        参数:
            rid: 分区ID (0=全站, 1=动画, 3=音乐, 4=游戏, 等)
            day: 排行榜类型 (1=日榜, 3=三日榜, 7=周榜)
        """
        try:
            params = {
                'rid': rid,
                'type': 'all',
            }
            
            response = requests.get(self.api_url, headers=self.headers, 
                                   params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['code'] == 0:
                return data['data']['list']
            else:
                print(f"  × API返回错误: {data.get('message', '未知错误')}")
                return None
                
        except requests.RequestException as e:
            print(f"  × 请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"  × JSON解析失败: {e}")
            return None
    
    def parse_video_data(self, video_list):
        """解析视频数据"""
        parsed_videos = []
        
        for video in video_list:
            try:
                video_data = {
                    'BV号': video.get('bvid', ''),
                    '标题': video.get('title', ''),
                    'UP主': video.get('owner', {}).get('name', ''),
                    'UP主ID': video.get('owner', {}).get('mid', ''),
                    '播放量': video.get('stat', {}).get('view', 0),
                    '弹幕数': video.get('stat', {}).get('danmaku', 0),
                    '点赞数': video.get('stat', {}).get('like', 0),
                    '投币数': video.get('stat', {}).get('coin', 0),
                    '收藏数': video.get('stat', {}).get('favorite', 0),
                    '分享数': video.get('stat', {}).get('share', 0),
                    '评分': video.get('score', 0),
                    '时长': video.get('duration', 0),
                    '发布时间': video.get('pubdate', 0),
                    '分区': video.get('tname', ''),
                    '简介': video.get('desc', ''),
                    '视频链接': f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                }
                parsed_videos.append(video_data)
                
            except Exception as e:
                print(f"  × 解析视频失败: {e}")
                continue
        
        return parsed_videos
    
    def crawl(self, categories=None):
        """
        执行爬取
        
        参数:
            categories: 要爬取的分区列表，None表示只爬全站
        """
        if categories is None:
            categories = [
                {'rid': 0, 'name': '全站'},
            ]
        
        print("\n开始爬取B站排行榜数据...")
        print(f"计划爬取 {len(categories)} 个分区")
        print("=" * 60)
        
        for category in categories:
            rid = category['rid']
            name = category['name']
            
            print(f"\n正在爬取【{name}】排行榜...")
            
            # 获取数据
            video_list = self.get_ranking_data(rid=rid)
            
            if not video_list:
                print(f"  × 【{name}】获取失败，跳过")
                continue
            
            # 解析数据
            parsed_videos = self.parse_video_data(video_list)
            
            # 添加分区标签
            for video in parsed_videos:
                video['排行榜分区'] = name
            
            self.videos.extend(parsed_videos)
            print(f"  √ 成功爬取 {len(parsed_videos)} 个视频")
            
            # 礼貌性延迟
            time.sleep(1)
        
        print(f"\n√ 爬取完成！共获取 {len(self.videos)} 个视频数据")
        return self.videos
    
    def save_data(self):
        """保存数据"""
        if not self.videos:
            print("\n警告: 没有数据可保存")
            return
        
        print("\n保存数据...")
        
        # 保存为CSV
        df = pd.DataFrame(self.videos)
        csv_file = 'Day3_Data_Processing/bilibili_ranking.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"  √ 已保存CSV: {csv_file}")
        
        # 保存为JSON
        json_file = 'Day3_Data_Processing/bilibili_ranking.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.videos, f, ensure_ascii=False, indent=2)
        print(f"  √ 已保存JSON: {json_file}")
        
        # 生成报告
        self.generate_report(df)
    
    def generate_report(self, df):
        """生成数据报告"""
        print("\n生成数据报告...")
        
        # 转换时间戳
        df['发布日期'] = pd.to_datetime(df['发布时间'], unit='s')
        
        report = f"""
{'=' * 60}
B站热门视频数据报告
{'=' * 60}

爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据总量: {len(df)} 个视频

播放量统计:
  - 平均播放量: {df['播放量'].mean():.0f}
  - 最高播放量: {df['播放量'].max():,}
  - 最低播放量: {df['播放量'].min():,}

互动数据统计:
  - 平均点赞数: {df['点赞数'].mean():.0f}
  - 平均投币数: {df['投币数'].mean():.0f}
  - 平均收藏数: {df['收藏数'].mean():.0f}
  - 平均弹幕数: {df['弹幕数'].mean():.0f}

分区分布:
"""
        
        # 分区统计
        category_counts = df['分区'].value_counts()
        for category, count in category_counts.head(10).items():
            report += f"  - {category}: {count} 个视频\n"
        
        report += f"\nTop 5 热门视频:\n"
        
        # Top 5视频
        top5 = df.nlargest(5, '播放量')[['标题', 'UP主', '播放量', '点赞数']]
        for idx, row in top5.iterrows():
            report += f"  {idx+1}. {row['标题']}\n"
            report += f"     UP主: {row['UP主']} | 播放: {row['播放量']:,} | 点赞: {row['点赞数']:,}\n"
        
        report += "\n" + "=" * 60
        
        print(report)
        
        # 保存报告
        report_file = 'Day3_Data_Processing/bilibili_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n√ 报告已保存: {report_file}")


# ============================================================================
# 执行爬虫
# ============================================================================

if __name__ == "__main__":
    # 创建爬虫实例
    crawler = BilibiliCrawler()
    
    # 定义要爬取的分区
    categories = [
        {'rid': 0, 'name': '全站'},
        # 可以添加更多分区
        # {'rid': 1, 'name': '动画'},
        # {'rid': 3, 'name': '音乐'},
        # {'rid': 4, 'name': '游戏'},
        # {'rid': 5, 'name': '娱乐'},
        # {'rid': 36, 'name': '科技'},
        # {'rid': 188, 'name': '数码'},
        # {'rid': 160, 'name': '生活'},
        # {'rid': 211, 'name': '美食'},
    ]
    
    # 执行爬取
    videos = crawler.crawl(categories=categories)
    
    # 保存数据
    if videos:
        crawler.save_data()
        
        print("\n" + "=" * 60)
        print("√ B站爬虫任务完成！")
        print("已生成文件:")
        print("  1. bilibili_ranking.csv - CSV格式数据")
        print("  2. bilibili_ranking.json - JSON格式数据")
        print("  3. bilibili_report.txt - 数据分析报告")
        print("=" * 60)
        print("\n提示:")
        print("  - 可以修改 categories 列表来爬取不同分区")
        print("  - 数据来自B站官方API，更稳定可靠")
        print("  - 遵守B站使用条款，合理使用数据")
    else:
        print("\n× 爬取失败，未获取到数据")
        print("\n可能的原因:")
        print("  1. 网络连接问题")
        print("  2. B站API变更")
        print("  3. 请求频率过高")
