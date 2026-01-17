# -*- coding: utf-8 -*-
"""
Douban Top250 Movies Visualization (Mock Data Version)
If crawler fails, use mock data for visualization demo
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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

sns.set_style("whitegrid")

print("=" * 70)
print("Douban Top250 Movies Visualization (Mock Data)")
print("=" * 70)

# ============================================================================
# Generate Mock Data
# ============================================================================

def generate_mock_data():
    """Generate mock Douban Top250 data"""
    print("\n[1/2] Generating mock data...")
    
    np.random.seed(42)
    
    movies = []
    
    movie_names = [
        'The Shawshank Redemption', 'Farewell My Concubine', 'Forrest Gump', 
        'Titanic', 'Leon: The Professional', 'Life Is Beautiful', 
        'Spirited Away', "Schindler's List", 'Inception', 'Hachi',
        'The Legend of 1900', 'The Truman Show', '3 Idiots', 'WALL-E',
        'The Chorus', 'A Chinese Odyssey', 'Silenced', 'Zootopia',
        'Infernal Affairs', 'The Godfather', 'The Pursuit of Happyness',
        'Flipped', 'My Neighbor Totoro', 'The Intouchables', 'Coco'
    ]
    
    for i in range(250):
        # Rating: 8.0-9.7, normal distribution
        rating = np.random.normal(8.8, 0.4)
        rating = np.clip(rating, 8.0, 9.7)
        
        # Votes: 10K-2M, log-normal distribution
        rating_people = int(np.random.lognormal(12.5, 1.0))
        rating_people = np.clip(rating_people, 10000, 2000000)
        
        if i < len(movie_names):
            name = movie_names[i]
        else:
            name = f'Movie {i+1}'
        
        movies.append({
            'Rank': i + 1,
            'Title': name,
            'Rating': round(rating, 1),
            'Votes': rating_people,
            'Director': f'Director {i+1}',
            'Details': f'2020 / USA / Drama',
            'Quote': f'An excellent movie'
        })
    
    df = pd.DataFrame(movies)
    
    # Add rating ranges
    df['Rating_Range'] = pd.cut(df['Rating'], 
                                bins=[0, 8.0, 8.5, 9.0, 10.0],
                                labels=['<8.0', '8.0-8.5', '8.5-9.0', '>9.0'])
    
    # Add votes ranges
    df['Votes_Range'] = pd.cut(df['Votes'],
                               bins=[0, 100000, 500000, 1000000, float('inf')],
                               labels=['<100K', '100-500K', '500K-1M', '>1M'])
    
    # Save data
    output_file = 'e:/anstis/phase3_training/douban_top250_mock.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"   Mock data saved: {output_file}")
    
    print(f"\n   Statistics:")
    print(f"   - Total movies: {len(df)}")
    print(f"   - Average rating: {df['Rating'].mean():.2f}")
    print(f"   - Max rating: {df['Rating'].max()}")
    print(f"   - Min rating: {df['Rating'].min()}")
    
    return df


# ============================================================================
# Data Visualization
# ============================================================================

def create_visualizations(df):
    """Create visualization charts"""
    print("\n[2/2] Creating visualizations...")
    
    output_dir = 'e:/anstis/phase3_training'
    
    # ========== 1. Boxplot (Detailed) ==========
    print("   [1/3] Creating boxplot...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bp = ax.boxplot([df['Rating']], labels=['Douban Top250'], 
                    patch_artist=True, widths=0.5,
                    boxprops=dict(facecolor='lightblue', alpha=0.7, linewidth=2),
                    medianprops=dict(color='red', linewidth=3),
                    whiskerprops=dict(color='blue', linewidth=2),
                    capprops=dict(color='blue', linewidth=2),
                    flierprops=dict(marker='o', markerfacecolor='red', 
                                   markersize=8, alpha=0.5))
    
    # Add detailed statistics
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
           fontsize=11, family='monospace',
           verticalalignment='center')
    
    ax.set_ylabel('Rating', fontsize=14, fontweight='bold')
    ax.set_title('Douban Top250 Rating Boxplot', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(7.5, 10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/douban_boxplot.png', dpi=300, bbox_inches='tight')
    print(f"      Saved: douban_boxplot.png")
    plt.close()
    
    # ========== 2. Histogram (Detailed) ==========
    print("   [2/3] Creating histogram...")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    n, bins, patches = ax.hist(df['Rating'], bins=30, color='skyblue', 
                               edgecolor='black', alpha=0.7, linewidth=1.5)
    
    # Color by frequency
    cm = plt.cm.get_cmap('RdYlGn_r')
    for i, patch in enumerate(patches):
        patch.set_facecolor(cm(n[i]/n.max()))
    
    # Add kernel density estimation
    from scipy import stats
    density = stats.gaussian_kde(df['Rating'])
    xs = np.linspace(df['Rating'].min(), df['Rating'].max(), 200)
    ax_twin = ax.twinx()
    ax_twin.plot(xs, density(xs), 'r-', linewidth=3, label='Density', alpha=0.8)
    ax_twin.set_ylabel('Density', fontsize=13, fontweight='bold')
    ax_twin.legend(loc='upper left', fontsize=11)
    
    # Add statistical lines
    mean_val = df['Rating'].mean()
    median_val = df['Rating'].median()
    
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2.5, 
              label=f'Mean: {mean_val:.2f}', alpha=0.8)
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2.5,
              label=f'Median: {median_val:.2f}', alpha=0.8)
    
    ax.set_xlabel('Rating', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax.set_title('Douban Top250 Rating Distribution', fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add statistics text box
    stats_text = f'Total: {len(df)}\n'
    stats_text += f'Mean: {mean_val:.3f}\n'
    stats_text += f'Std: {df["Rating"].std():.3f}\n'
    stats_text += f'Max: {df["Rating"].max()}\n'
    stats_text += f'Min: {df["Rating"].min()}'
    
    ax.text(0.02, 0.98, stats_text,
           transform=ax.transAxes,
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
           fontsize=11, verticalalignment='top',
           family='monospace')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/douban_histogram.png', dpi=300, bbox_inches='tight')
    print(f"      Saved: douban_histogram.png")
    plt.close()
    
    # ========== 3. Comprehensive Analysis (6-in-1) ==========
    print("   [3/3] Creating comprehensive chart...")
    
    fig = plt.figure(figsize=(20, 12))
    
    # Subplot 1: Boxplot
    ax1 = plt.subplot(2, 3, 1)
    bp = ax1.boxplot([df['Rating']], labels=['Top250'], patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2))
    ax1.set_ylabel('Rating', fontsize=12, fontweight='bold')
    ax1.set_title('Rating Boxplot', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Histogram
    ax2 = plt.subplot(2, 3, 2)
    ax2.hist(df['Rating'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    ax2.axvline(df['Rating'].mean(), color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel('Rating', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    ax2.set_title('Rating Distribution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Subplot 3: Rating ranges
    ax3 = plt.subplot(2, 3, 3)
    rating_counts = df['Rating_Range'].value_counts().sort_index()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = ax3.bar(range(len(rating_counts)), rating_counts.values, 
                   color=colors, alpha=0.7, edgecolor='black')
    for bar, count in zip(bars, rating_counts.values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({count/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax3.set_xticks(range(len(rating_counts)))
    ax3.set_xticklabels(rating_counts.index, rotation=0)
    ax3.set_ylabel('Count', fontsize=12)
    ax3.set_title('Rating Ranges', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Subplot 4: Top20 movies
    ax4 = plt.subplot(2, 3, 4)
    top20 = df.head(20)
    y_pos = np.arange(len(top20))
    bars = ax4.barh(y_pos, top20['Rating'], color='coral', alpha=0.7)
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels([f"{row['Rank']}. {row['Title'][:15]}" 
                         for _, row in top20.iterrows()], fontsize=8)
    ax4.set_xlabel('Rating', fontsize=12)
    ax4.set_title('Top20 Movies', fontsize=14, fontweight='bold')
    ax4.invert_yaxis()
    ax4.grid(True, alpha=0.3, axis='x')
    
    # Subplot 5: Votes distribution
    ax5 = plt.subplot(2, 3, 5)
    people_counts = df['Votes_Range'].value_counts().sort_index()
    colors_people = ['#98D8C8', '#6BCF7F', '#F7DC6F', '#BB8FCE']
    ax5.pie(people_counts.values, labels=people_counts.index,
           colors=colors_people, autopct='%1.1f%%', startangle=90)
    ax5.set_title('Votes Distribution', fontsize=14, fontweight='bold')
    
    # Subplot 6: Rating vs Votes
    ax6 = plt.subplot(2, 3, 6)
    scatter = ax6.scatter(df['Votes']/10000, df['Rating'], 
                         c=df['Rank'], cmap='viridis_r', 
                         s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
    ax6.set_xlabel('Votes (10K)', fontsize=12)
    ax6.set_ylabel('Rating', fontsize=12)
    ax6.set_title('Rating vs Votes', fontsize=14, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    cbar = plt.colorbar(scatter, ax=ax6)
    cbar.set_label('Rank', fontsize=10)
    
    fig.suptitle('Douban Top250 Movies Analysis Report', 
                fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/douban_comprehensive.png', dpi=300, bbox_inches='tight')
    print(f"      Saved: douban_comprehensive.png")
    plt.close()


# ============================================================================
# Main Function
# ============================================================================

def main():
    """Main function"""
    try:
        # Generate mock data
        df = generate_mock_data()
        
        # Create visualizations
        create_visualizations(df)
        
        print("\n" + "=" * 70)
        print("Visualization completed!")
        print("=" * 70)
        print("\nGenerated files:")
        print("  1. douban_top250_mock.csv - Mock data")
        print("  2. douban_boxplot.png - Rating boxplot")
        print("  3. douban_histogram.png - Rating distribution")
        print("  4. douban_comprehensive.png - Comprehensive chart (6-in-1)")
        print("\nLocation: e:/anstis/phase3_training/")
        print("\nNote: This uses mock data for demonstration")
        print("      For real data, run douban_movie_crawler.py with network access")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
