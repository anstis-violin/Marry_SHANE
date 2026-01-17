# -*- coding: utf-8 -*-
"""
Douban Top250 Movies Crawler and Visualization
Crawl Douban Top250 movies data and create visualizations
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import random
import sys
import io

# Set output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set font - try multiple fonts
try:
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# Set seaborn style
sns.set_style("whitegrid")

print("=" * 70)
print("Douban Top250 Movies - Crawler and Visualization")
print("=" * 70)

# ============================================================================
# Part 1: Crawl Douban Top250 Data
# ============================================================================

def crawl_douban_top250():
    """Crawl Douban Top250 movies data"""
    print("\n[1/3] Crawling Douban Top250 data...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://movie.douban.com/'
    }
    
    movies = []
    
    for page in range(0, 250, 25):
        url = f'https://movie.douban.com/top250?start={page}'
        
        try:
            print(f"   Crawling page {page//25 + 1}...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            movie_list = soup.find('ol', class_='grid_view')
            
            if not movie_list:
                print(f"   Warning: Page {page//25 + 1} not found")
                continue
            
            movie_items = movie_list.find_all('li')
            
            for item in movie_items:
                try:
                    info_div = item.find('div', class_='info')
                    if not info_div:
                        continue
                    
                    rank_em = item.find('em')
                    rank = rank_em.text if rank_em else "0"
                    
                    title_span = info_div.find('span', class_='title')
                    title = title_span.text if title_span else "Unknown"
                    
                    rating_span = info_div.find('span', class_='rating_num')
                    rating = rating_span.text if rating_span else "0"
                    
                    star_div = info_div.find('div', class_='star')
                    if star_div:
                        rating_people_spans = star_div.find_all('span')
                        if len(rating_people_spans) >= 4:
                            rating_people = rating_people_spans[3].text.replace('人评价', '').strip()
                        else:
                            rating_people = "0"
                    else:
                        rating_people = "0"
                    
                    if rank != "0" and title != "Unknown":
                        movies.append({
                            'Rank': int(rank),
                            'Title': title,
                            'Rating': float(rating),
                            'Votes': int(rating_people) if rating_people.isdigit() else 0
                        })
                    
                except Exception as e:
                    continue
            
            print(f"   Page {page//25 + 1} done, got {len(movie_items)} movies")
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"   Failed to crawl page {page//25 + 1}: {e}")
            continue
    
    print(f"\n   Successfully crawled {len(movies)} movies!")
    return movies


# ============================================================================
# Part 2: Process and Save Data
# ============================================================================

def process_and_save_data(movies):
    """Process data and save"""
    print("\n[2/3] Processing and saving data...")
    
    df = pd.DataFrame(movies)
    df = df.sort_values('Rank')
    
    # Add rating ranges
    df['Rating_Range'] = pd.cut(df['Rating'], 
                                bins=[0, 8.0, 8.5, 9.0, 10.0],
                                labels=['<8.0', '8.0-8.5', '8.5-9.0', '>9.0'])
    
    # Add votes ranges (handle missing values)
    df['Votes_Range'] = pd.cut(df['Votes'],
                               bins=[0, 100000, 500000, 1000000, float('inf')],
                               labels=['<100K', '100-500K', '500K-1M', '>1M'],
                               include_lowest=True)
    # Fill any NaN values with a default category
    df['Votes_Range'] = df['Votes_Range'].fillna('<100K')
    
    output_file = 'e:/anstis/phase3_training/douban_top250.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"   Data saved to: {output_file}")
    
    print("\n   Statistics:")
    print(f"   - Total movies: {len(df)}")
    print(f"   - Average rating: {df['Rating'].mean():.2f}")
    print(f"   - Max rating: {df['Rating'].max()}")
    print(f"   - Min rating: {df['Rating'].min()}")
    
    return df


# ============================================================================
# Part 3: Data Visualization
# ============================================================================

def visualize_data(df):
    """Create visualizations"""
    print("\n[3/3] Creating visualizations...")
    
    output_dir = 'e:/anstis/phase3_training'
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Boxplot
    print("   [1/6] Creating boxplot...")
    ax1 = plt.subplot(2, 3, 1)
    bp = ax1.boxplot([df['Rating']], tick_labels=['Top250'], patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2))
    
    stats_text = f'Mean: {df["Rating"].mean():.2f}\n'
    stats_text += f'Median: {df["Rating"].median():.2f}\n'
    stats_text += f'Max: {df["Rating"].max()}\n'
    stats_text += f'Min: {df["Rating"].min()}'
    
    ax1.text(1.15, df['Rating'].mean(), stats_text, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=10)
    ax1.set_ylabel('Rating', fontsize=12, fontweight='bold')
    ax1.set_title('Rating Boxplot', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 2. Histogram
    print("   [2/6] Creating histogram...")
    ax2 = plt.subplot(2, 3, 2)
    n, bins, patches = ax2.hist(df['Rating'], bins=20, color='skyblue', 
                                 edgecolor='black', alpha=0.7)
    
    from scipy import stats
    density = stats.gaussian_kde(df['Rating'])
    xs = np.linspace(df['Rating'].min(), df['Rating'].max(), 200)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(xs, density(xs), 'r-', linewidth=2, label='Density')
    ax2_twin.set_ylabel('Density', fontsize=11)
    ax2_twin.legend(loc='upper left')
    
    ax2.axvline(df['Rating'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {df["Rating"].mean():.2f}')
    ax2.set_xlabel('Rating', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax2.set_title('Rating Distribution', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Rating ranges
    print("   [3/6] Creating rating ranges...")
    ax3 = plt.subplot(2, 3, 3)
    rating_counts = df['Rating_Range'].value_counts().sort_index()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = ax3.bar(range(len(rating_counts)), rating_counts.values, 
                   color=colors, alpha=0.7, edgecolor='black')
    
    for bar, count in zip(bars, rating_counts.values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({count/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax3.set_xticks(range(len(rating_counts)))
    ax3.set_xticklabels(rating_counts.index, rotation=0)
    ax3.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax3.set_title('Rating Ranges', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Top20 movies
    print("   [4/6] Creating Top20 chart...")
    ax4 = plt.subplot(2, 3, 4)
    top20 = df.head(20)
    y_pos = np.arange(len(top20))
    bars = ax4.barh(y_pos, top20['Rating'], color='coral', alpha=0.7)
    
    for bar, rating in zip(bars, top20['Rating']):
        if rating >= 9.5:
            bar.set_color('#FF6B6B')
        elif rating >= 9.0:
            bar.set_color('#FFA07A')
        else:
            bar.set_color('#FFD700')
    
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels([f"{row['Rank']}. {row['Title'][:10]}" 
                         for _, row in top20.iterrows()], fontsize=9)
    ax4.set_xlabel('Rating', fontsize=12, fontweight='bold')
    ax4.set_title('Top20 Movies', fontsize=14, fontweight='bold')
    ax4.invert_yaxis()
    ax4.grid(True, alpha=0.3, axis='x')
    
    for bar, rating in zip(bars, top20['Rating']):
        ax4.text(rating + 0.02, bar.get_y() + bar.get_height()/2,
                f'{rating}', va='center', fontsize=9, fontweight='bold')
    
    # 5. Votes distribution
    print("   [5/6] Creating votes distribution...")
    ax5 = plt.subplot(2, 3, 5)
    votes_counts = df['Votes_Range'].value_counts().sort_index()
    
    # Only create pie chart if we have valid data
    if len(votes_counts) > 0 and votes_counts.sum() > 0:
        colors_votes = ['#98D8C8', '#6BCF7F', '#F7DC6F', '#BB8FCE']
        # Use only as many colors as we have categories
        colors_to_use = colors_votes[:len(votes_counts)]
        
        wedges, texts, autotexts = ax5.pie(votes_counts.values, 
                                            labels=votes_counts.index,
                                            colors=colors_to_use,
                                            autopct='%1.1f%%',
                                            startangle=90)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
    else:
        ax5.text(0.5, 0.5, 'No data available', 
                ha='center', va='center', transform=ax5.transAxes)
    
    ax5.set_title('Votes Distribution', fontsize=14, fontweight='bold')
    
    # 6. Rating vs Votes
    print("   [6/6] Creating scatter plot...")
    ax6 = plt.subplot(2, 3, 6)
    
    # Filter out movies with 0 votes for better visualization
    df_valid = df[df['Votes'] > 0].copy()
    
    if len(df_valid) > 0:
        scatter = ax6.scatter(df_valid['Votes']/10000, df_valid['Rating'], 
                             c=df_valid['Rank'], cmap='viridis_r', 
                             s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Try to add trend line, skip if data is problematic
        try:
            if len(df_valid) > 1:
                z = np.polyfit(df_valid['Votes'], df_valid['Rating'], 1)
                p = np.poly1d(z)
                ax6.plot(df_valid['Votes']/10000, p(df_valid['Votes']), 
                        "r--", linewidth=2, alpha=0.8, label='Trend')
                ax6.legend()
        except:
            pass  # Skip trend line if calculation fails
        
        cbar = plt.colorbar(scatter, ax=ax6)
        cbar.set_label('Rank', fontsize=11)
    else:
        ax6.text(0.5, 0.5, 'No valid data', 
                ha='center', va='center', transform=ax6.transAxes)
    
    ax6.set_xlabel('Votes (10K)', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Rating', fontsize=12, fontweight='bold')
    ax6.set_title('Rating vs Votes', fontsize=14, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    fig.suptitle('Douban Top250 Movies Analysis', 
                fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    output_file = f'{output_dir}/douban_top250_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n   Comprehensive chart saved: {output_file}")
    plt.close()
    
    create_detailed_boxplot(df, output_dir)
    create_detailed_histogram(df, output_dir)


def create_detailed_boxplot(df, output_dir):
    """Create detailed boxplot"""
    print("\n   Creating detailed boxplot...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bp = ax.boxplot([df['Rating']], tick_labels=['Douban Top250'], 
                    patch_artist=True, widths=0.5,
                    boxprops=dict(facecolor='lightblue', alpha=0.7, linewidth=2),
                    medianprops=dict(color='red', linewidth=3),
                    whiskerprops=dict(color='blue', linewidth=2),
                    capprops=dict(color='blue', linewidth=2))
    
    stats = df['Rating'].describe()
    stats_text = f"""Statistics:
    
Count: {int(stats['count'])}
Mean: {stats['mean']:.3f}
Std: {stats['std']:.3f}
    
Min: {stats['min']:.1f}
25%: {stats['25%']:.1f}
Median: {stats['50%']:.1f}
75%: {stats['75%']:.1f}
Max: {stats['max']:.1f}
    
IQR: {stats['75%'] - stats['25%']:.2f}
    """
    
    ax.text(1.3, df['Rating'].mean(), stats_text,
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
           fontsize=11, family='monospace', verticalalignment='center')
    
    ax.set_ylabel('Rating', fontsize=14, fontweight='bold')
    ax.set_title('Rating Boxplot (Detailed)', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(7.5, 10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/douban_boxplot_detailed.png', dpi=300, bbox_inches='tight')
    print(f"   Detailed boxplot saved")
    plt.close()


def create_detailed_histogram(df, output_dir):
    """Create detailed histogram"""
    print("   Creating detailed histogram...")
    fig, ax = plt.subplots(figsize=(14, 8))
    
    n, bins, patches = ax.hist(df['Rating'], bins=30, color='skyblue', 
                               edgecolor='black', alpha=0.7, linewidth=1.5)
    
    cm = plt.colormaps.get_cmap('RdYlGn_r')
    for i, patch in enumerate(patches):
        patch.set_facecolor(cm(n[i]/n.max()))
    
    from scipy import stats
    density = stats.gaussian_kde(df['Rating'])
    xs = np.linspace(df['Rating'].min(), df['Rating'].max(), 200)
    ax_twin = ax.twinx()
    ax_twin.plot(xs, density(xs), 'r-', linewidth=3, label='Density', alpha=0.8)
    ax_twin.set_ylabel('Density', fontsize=13, fontweight='bold')
    ax_twin.legend(loc='upper left', fontsize=11)
    
    mean_val = df['Rating'].mean()
    median_val = df['Rating'].median()
    
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2.5, 
              label=f'Mean: {mean_val:.2f}', alpha=0.8)
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2.5,
              label=f'Median: {median_val:.2f}', alpha=0.8)
    
    ax.set_xlabel('Rating', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Rating Distribution (Detailed)', fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    stats_text = f'Total: {len(df)}\n'
    stats_text += f'Mean: {mean_val:.3f}\n'
    stats_text += f'Std: {df["Rating"].std():.3f}\n'
    stats_text += f'Max: {df["Rating"].max()}\n'
    stats_text += f'Min: {df["Rating"].min()}'
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
           fontsize=11, verticalalignment='top', family='monospace')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/douban_histogram_detailed.png', dpi=300, bbox_inches='tight')
    print(f"   Detailed histogram saved")
    plt.close()


# ============================================================================
# Main Function
# ============================================================================

def main():
    """Main function"""
    try:
        movies = crawl_douban_top250()
        
        if not movies:
            print("\nNo data crawled, please check network")
            return
        
        df = process_and_save_data(movies)
        visualize_data(df)
        
        print("\n" + "=" * 70)
        print("Project completed!")
        print("=" * 70)
        print("\nGenerated files:")
        print("  1. douban_top250.csv - Movie data")
        print("  2. douban_top250_analysis.png - Comprehensive chart (6-in-1)")
        print("  3. douban_boxplot_detailed.png - Detailed boxplot")
        print("  4. douban_histogram_detailed.png - Detailed histogram")
        print("\nLocation: e:/anstis/phase3_training/")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
