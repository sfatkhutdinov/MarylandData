#!/usr/bin/env python3
"""
Fix the dashboard chart - matplotlib was choking on dollar signs
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

plt.style.use('default')
sns.set_palette("Set2")

COLORS = {
    'struggling': '#C73E1D',
    'comfortable': '#5E8C31',
    'service': '#F18F01',
    'professional': '#2E86AB',
    'wealthy': '#A23B72'
}

def load_real_data():
    """Load all our real data"""
    with open('data/hanover_real_data.json', 'r') as f:
        baseline_data = json.load(f)

    with open('data/real_employment_income.json', 'r') as f:
        detailed_data = json.load(f)

    return baseline_data, detailed_data

def create_honest_summary_dashboard(baseline_data, detailed_data):
    """Fixed dashboard without problematic characters"""
    fig = plt.figure(figsize=(18, 14))

    fig.suptitle('HANOVER, MD: REAL DATA FOR REAL PEOPLE\nFocus on Working Families, Not Defense Contractors',
                 fontsize=20, fontweight='bold', y=0.95)

    gs = fig.add_gridspec(4, 4, hspace=0.4, wspace=0.3)

    # Key numbers
    metrics = baseline_data['calculated_metrics']
    affordability = detailed_data['affordability_analysis']
    employment = detailed_data['employment_by_industry']

    # Population
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.text(0.5, 0.6, f"{metrics['population_2023']:,}", ha='center', va='center',
             fontsize=28, fontweight='bold', color=COLORS['professional'])
    ax1.text(0.5, 0.3, 'Total\nPopulation', ha='center', va='center',
             fontsize=11, fontweight='bold')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')

    # Service workers
    service_workers = employment['C24010_003E']['value']
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.text(0.5, 0.6, f"{service_workers:,}", ha='center', va='center',
             fontsize=28, fontweight='bold', color=COLORS['service'])
    ax2.text(0.5, 0.3, 'Service\nWorkers', ha='center', va='center',
             fontsize=11, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')

    # Households priced out
    priced_out = affordability['cannot_afford']
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.text(0.5, 0.6, f"{priced_out:,}", ha='center', va='center',
             fontsize=28, fontweight='bold', color=COLORS['struggling'])
    ax3.text(0.5, 0.3, 'Households\nPriced Out', ha='center', va='center',
             fontsize=11, fontweight='bold')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')

    # Transit usage
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.text(0.5, 0.6, f"{metrics['public_transit_rate']:.1f}%", ha='center', va='center',
             fontsize=28, fontweight='bold', color=COLORS['struggling'])
    ax4.text(0.5, 0.3, 'Use Public\nTransit', ha='center', va='center',
             fontsize=11, fontweight='bold')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')

    # Employment breakdown
    ax5 = fig.add_subplot(gs[1, :2])
    total_employed = employment['C24010_001E']['value']

    job_types = ['Service\nWorkers', 'Professional/\nManagement', 'Sales/\nOffice', 'Manual\nLabor']
    job_counts = [
        employment['C24010_003E']['value'],
        employment['C24010_002E']['value'],
        employment['C24010_004E']['value'],
        employment['C24010_005E']['value'] + employment['C24010_006E']['value']
    ]
    job_colors = [COLORS['service'], COLORS['professional'], COLORS['comfortable'], COLORS['struggling']]

    bars = ax5.bar(job_types, job_counts, color=job_colors, alpha=0.8)
    ax5.set_title('WHO WORKS IN HANOVER\nReal Employment Data', fontsize=14, fontweight='bold')
    ax5.set_ylabel('Number of Workers')
    ax5.grid(True, alpha=0.3)

    for bar, count in zip(bars, job_counts):
        percentage = (count / total_employed) * 100
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f'{count:,}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')

    # Housing affordability
    ax6 = fig.add_subplot(gs[1, 2:])

    afford_categories = ['Can Afford\nMedian Home', 'Cannot Afford\nMedian Home']
    afford_values = [affordability['can_afford'], affordability['cannot_afford']]
    afford_colors = [COLORS['comfortable'], COLORS['struggling']]

    bars = ax6.bar(afford_categories, afford_values, color=afford_colors, alpha=0.8)
    ax6.set_title('HOUSING AFFORDABILITY REALITY\n492K Median Home Price', fontsize=14, fontweight='bold')
    ax6.set_ylabel('Number of Households')
    ax6.grid(True, alpha=0.3)

    for bar, value in zip(bars, afford_values):
        percentage = (value / sum(afford_values)) * 100
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f'{value:,}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')

    # Key findings - removed problematic characters
    ax7 = fig.add_subplot(gs[2:, :])
    findings_text = f"""
REAL FINDINGS FROM REAL DATA:

• SERVICE WORKERS: {service_workers:,} people (32.8% of workforce) in restaurants, retail, healthcare support, cleaning, etc.
• HOUSING CRISIS: {priced_out:,} households ({affordability['cannot_afford_percentage']:.1f}%) cannot afford 492K median home
• TRANSIT DESERT: {metrics['public_transit_rate']:.1f}% use public transit - workers must own cars (650/month) to get to jobs
• INCOME REALITY: 8% earn under 50K, 26% earn 200K+ - stark inequality in same community

REAL SOLUTIONS FOR REAL PEOPLE:
• Affordable rental housing (1,200-1,800/month) for service workers
• Public transit connecting neighborhoods to job centers (save workers 450/month)
• Workforce housing (200K-350K) for teachers, nurses, firefighters
• Local job creation to reduce long commutes

THE REAL PROBLEM: Essential workers (restaurant staff, store clerks, healthcare aides) cannot afford to live where they work.
THE REAL SOLUTION: Housing and transportation that serves working families, not just high earners.
"""

    ax7.text(0.05, 0.95, findings_text, transform=ax7.transAxes,
             fontsize=12, va='top', ha='left',
             bbox=dict(boxstyle="round,pad=0.8", facecolor=COLORS['service'], alpha=0.1))
    ax7.axis('off')

    # Data source
    fig.text(0.5, 0.02,
             f'Data Sources: US Census ACS 2023 | Analysis Date: {datetime.now().strftime("%B %d, %Y")}',
             ha='center', fontsize=10, style='italic')

    plt.savefig('data/honest_hanover_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: honest_hanover_dashboard.png")

def main():
    """Fix the dashboard"""
    print("FIXING DASHBOARD CHART")
    print("=" * 30)

    # Load real data
    baseline_data, detailed_data = load_real_data()

    # Create fixed dashboard
    create_honest_summary_dashboard(baseline_data, detailed_data)

    print("\nFIXED!")
    print("Now we have all 4 charts:")
    print("- data/who_actually_lives_here.png")
    print("- data/service_worker_reality.png")
    print("- data/real_solutions.png")
    print("- data/honest_hanover_dashboard.png")

if __name__ == "__main__":
    main()