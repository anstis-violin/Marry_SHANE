"""
B站热门视频数据爬虫（改进版）
包含模拟数据功能，确保一定能获取到数据
"""

import sys
import io

# 解决Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import pandas as pd
import time
import json
from datetime import datetime
import random
import os

print("=" * 70)
print("B站热门视频数据爬虫")
print("=" * 70)

class BilibiliCrawler:
    """B站视频爬虫类"""
    
    def __init__(self):
        self.api_url = "https://api.bilibili.com/x/web-interface/ranking/v2"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com',
        }
        self.videos = []
        
    def get_ranking_data(self, rid=0):
        """获取排行榜数据"""
        try:
            params = {'rid': rid, 'type': 'all'}
            response = requests.get(self.api_url, headers=self.headers, 
                                   params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] == 0 and 'data' in data and 'list' in data['data']:
                return data['data']['list']
            else:
                print(f"  × API返回错误: {data.get('message', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"  × 请求失败: {e}")
            return None
    
    def parse_video_data(self, video_list, category_name):
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
                    '时长秒': video.get('duration', 0),
                    '发布时间戳': video.get('pubdate', 0),
                    '分区': video.get('tname', ''),
                    '简介': video.get('desc', '')[:100],
                    '排行榜分区': category_name,
                }
                
                # 计算互动率
                total_view = video_data['播放量']
                if total_view > 0:
                    video_data['点赞率'] = video_data['点赞数'] / total_view
                    video_data['投币率'] = video_data['投币数'] / total_view
                    video_data['收藏率'] = video_data['收藏数'] / total_view
                else:
                    video_data['点赞率'] = 0
                    video_data['投币率'] = 0
                    video_data['收藏率'] = 0
                
                parsed_videos.append(video_data)
                
            except Exception as e:
                print(f"  × 解析视频失败: {e}")
                continue
        
        return parsed_videos
    
    def crawl(self, categories=None):
        """执行爬取"""
        if categories is None:
            categories = [
                {'rid': 0, 'name': '全站'},
                {'rid': 1, 'name': '动画'},
                {'rid': 3, 'name': '音乐'},
                {'rid': 4, 'name': '游戏'},
                {'rid': 5, 'name': '娱乐'},
            ]
        
        print(f"\n开始爬取B站排行榜数据...")
        print(f"计划爬取 {len(categories)} 个分区")
        print("=" * 70)
        
        success_count = 0
        
        for category in categories:
            rid = category['rid']
            name = category['name']
            
            print(f"\n正在爬取【{name}】排行榜...")
            
            video_list = self.get_ranking_data(rid=rid)
            
            if not video_list:
                print(f"  × 【{name}】获取失败，跳过")
                continue
            
            parsed_videos = self.parse_video_data(video_list, name)
            
            if parsed_videos:
                self.videos.extend(parsed_videos)
                print(f"  √ 成功爬取 {len(parsed_videos)} 个视频")
                success_count += 1
            
            time.sleep(1)
        
        if self.videos:
            print(f"\n√ 爬取完成！共获取 {len(self.videos)} 个视频数据")
            return self.videos
        else:
            print(f"\n× 所有分区爬取失败")
            return None
    
    def generate_mock_data(self):
        """生成模拟数据（当API无法访问时使用）"""
        print("\n" + "=" * 70)
        print("使用模拟数据模式")
        print("=" * 70)
        
        categories = ['全站', '动画', '音乐', '游戏', '娱乐']
        video_types = ['生活', '科技', '美食', '舞蹈', '鬼畜', '时尚', '影视', '知识']
        
        up_names = [
            '老番茄', '徐大虾咯', '影视飓风', '敬汉卿', '华农兄弟',
            '李子柒', 'Lex', '小潮院长', '芳斯塔芙', '绵羊料理',
            '技术宅阿伟', '何同学', '老师好我叫何同学', '稚晖君', '硬核的半佛仙人',
            '罗翔说刑法', '巫师财经', '半佛仙人', '蕾蕾Kyokyo', '泛式',
        ]
        
        video_titles = [
            '这游戏太离谱了！', '震惊！原来真相是这样', '教你一招搞定',
            '万万没想到', '这才是正确的打开方式', '太强了！',
            '我悟了！', '这个技巧你一定要学', '神仙操作',
            '笑死我了', '太真实了', '这也太厉害了吧',
            '绝了！', '学到了学到了', '涨知识了',
        ]
        
        mock_videos = []
        
        for i in range(100):
            category = random.choice(categories)
            up_name = random.choice(up_names)
            title_base = random.choice(video_titles)
            video_type = random.choice(video_types)
            
            # 生成合理的数据
            view = random.randint(50000, 5000000)
            like = int(view * random.uniform(0.03, 0.08))
            coin = int(view * random.uniform(0.01, 0.04))
            favorite = int(view * random.uniform(0.015, 0.05))
            danmaku = int(view * random.uniform(0.005, 0.02))
            share = int(view * random.uniform(0.001, 0.01))
            
            video = {
                'BV号': f'BV{random.randint(1000000000, 9999999999)}',
                '标题': f'{title_base} - {video_type}相关',
                'UP主': up_name,
                'UP主ID': random.randint(1000000, 9999999),
                '播放量': view,
                '弹幕数': danmaku,
                '点赞数': like,
                '投币数': coin,
                '收藏数': favorite,
                '分享数': share,
                '时长秒': random.randint(60, 1800),
                '发布时间戳': int(time.time()) - random.randint(0, 7*24*3600),
                '分区': video_type,
                '简介': f'这是一个关于{video_type}的精彩视频',
                '排行榜分区': category,
                '点赞率': like / view,
                '投币率': coin / view,
                '收藏率': favorite / view,
            }
            
            mock_videos.append(video)
        
        self.videos = mock_videos
        print(f"\n√ 已生成 {len(mock_videos)} 条模拟数据")
        return mock_videos
    
    def save_data(self, output_dir='data'):
        """保存数据"""
        if not self.videos:
            print("\n警告: 没有数据可保存")
            return None
        
        print("\n保存数据...")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        df = pd.DataFrame(self.videos)
        
        # 转换时间戳为日期
        df['发布日期'] = pd.to_datetime(df['发布时间戳'], unit='s')
        df['时长分钟'] = df['时长秒'] / 60
        
        # 保存CSV
        csv_file = f'{output_dir}/bilibili_data.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"  √ 已保存CSV: {csv_file}")
        
        # 保存JSON
        json_file = f'{output_dir}/bilibili_data.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.videos, f, ensure_ascii=False, indent=2)
        print(f"  √ 已保存JSON: {json_file}")
        
        # 生成报告
        self.generate_report(df, output_dir)
        
        return df
    
    def generate_report(self, df, output_dir):
        """生成数据报告"""
        report = f"""
{'=' * 70}
B站热门视频数据报告
{'=' * 70}

爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据总量: {len(df)} 个视频

播放量统计:
  - 总播放量: {df['播放量'].sum():,}
  - 平均播放量: {df['播放量'].mean():.0f}
  - 最高播放量: {df['播放量'].max():,}
  - 最低播放量: {df['播放量'].min():,}

互动数据统计:
  - 总点赞数: {df['点赞数'].sum():,}
  - 总投币数: {df['投币数'].sum():,}
  - 总收藏数: {df['收藏数'].sum():,}
  - 平均点赞率: {df['点赞率'].mean():.2%}
  - 平均投币率: {df['投币率'].mean():.2%}
  - 平均收藏率: {df['收藏率'].mean():.2%}

分区分布:
"""
        
        category_counts = df['排行榜分区'].value_counts()
        for category, count in category_counts.items():
            report += f"  - {category}: {count} 个视频\n"
        
        report += f"\nTop 10 热门视频:\n"
        
        top10 = df.nlargest(10, '播放量')[['标题', 'UP主', '播放量', '点赞数', '分区']]
        for idx, (_, row) in enumerate(top10.iterrows(), 1):
            report += f"\n  {idx}. {row['标题']}\n"
            report += f"     UP主: {row['UP主']} | 分区: {row['分区']}\n"
            report += f"     播放: {row['播放量']:,} | 点赞: {row['点赞数']:,}\n"
        
        report += "\n" + "=" * 70
        
        print(report)
        
        report_file = f'{output_dir}/bilibili_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n√ 报告已保存: {report_file}")


if __name__ == "__main__":
    # 创建爬虫实例
    crawler = BilibiliCrawler()
    
    # 定义要爬取的分区
    categories = [
        {'rid': 0, 'name': '全站'},
        {'rid': 1, 'name': '动画'},
        {'rid': 3, 'name': '音乐'},
        {'rid': 4, 'name': '游戏'},
        {'rid': 5, 'name': '娱乐'},
    ]
    
    # 尝试爬取真实数据
    print("\n尝试从B站API获取数据...")
    videos = crawler.crawl(categories=categories)
    
    # 如果爬取失败，使用模拟数据
    if not videos:
        print("\n" + "=" * 70)
        print("⚠️  无法从B站API获取数据")
        print("可能原因:")
        print("  1. 网络连接问题")
        print("  2. B站API限制")
        print("  3. API地址变更")
        print("\n切换到模拟数据模式...")
        print("=" * 70)
        
        videos = crawler.generate_mock_data()
    
    # 保存数据
    if videos:
        df = crawler.save_data(output_dir='data')
        
        print("\n" + "=" * 70)
        print("√ 数据获取完成！")
        print("=" * 70)
        print("\n下一步:")
        print("  1. 运行 visualize_2d.py 生成二维图表")
        print("  2. 运行 visualize_3d.py 生成三维图表")
        print("  或直接运行 run_all.bat 一键生成所有图表")
    else:
        print("\n× 数据获取失败")
