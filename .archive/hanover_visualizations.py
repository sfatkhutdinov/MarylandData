#!/usr/bin/env python3
"""
Hanover, MD Data Visualization Generator

Creates comprehensive charts and graphs for the Hanover community improvement analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Set style for professional-looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class HanoverVisualizer:
    def __init__(self):
        # Hanover demographic data
        self.hanover_data = {
            'population': 28089,
            'median_income': 143409,
            'median_home_value': 492100,
            'median_age': 35.9,
            'poverty_rate': 2.3,
            'racial_breakdown': {
                'White': 38.24,
                'Black': 30.70,
                'Asian': 17.01,
                'Hispanic': 9.51,
                'Other': 4.54
            }
        }

        # Comparison data (Maryland and national averages)
        self.comparison_data = {
            'maryland': {
                'median_income': 95999,
                'median_home_value': 374900,
                'median_age': 39.0,
                'poverty_rate': 9.0
            },
            'national': {
                'median_income': 70784,
                'median_home_value': 348079,
                'median_age': 38.1,
                'poverty_rate': 11.6
            }
        }

    def create_demographic_overview(self):
        """Create comprehensive demographic overview charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover, MD - Demographic Overview', fontsize=16, fontweight='bold')

        # 1. Racial/Ethnic Diversity Pie Chart
        racial_data = self.hanover_data['racial_breakdown']
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
        wedges, texts, autotexts = ax1.pie(racial_data.values(), labels=racial_data.keys(),
                                          autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_title('Racial/Ethnic Composition\n(Diversity Score: 0.72)', fontweight='bold')

        # 2. Income Comparison Bar Chart
        locations = ['Hanover', 'Maryland', 'National']
        incomes = [self.hanover_data['median_income'],
                  self.comparison_data['maryland']['median_income'],
                  self.comparison_data['national']['median_income']]

        bars = ax2.bar(locations, incomes, color=['#4CAF50', '#2196F3', '#FF9800'])
        ax2.set_title('Median Household Income Comparison', fontweight='bold')
        ax2.set_ylabel('Income ($)')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom')

        # 3. Housing Values Comparison
        home_values = [self.hanover_data['median_home_value'],
                      self.comparison_data['maryland']['median_home_value'],
                      self.comparison_data['national']['median_home_value']]

        bars = ax3.bar(locations, home_values, color=['#9C27B0', '#607D8B', '#795548'])
        ax3.set_title('Median Home Value Comparison', fontweight='bold')
        ax3.set_ylabel('Home Value ($)')
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom')

        # 4. Poverty Rate Comparison
        poverty_rates = [self.hanover_data['poverty_rate'],
                        self.comparison_data['maryland']['poverty_rate'],
                        self.comparison_data['national']['poverty_rate']]

        bars = ax4.bar(locations, poverty_rates, color=['#4CAF50', '#FF5722', '#F44336'])
        ax4.set_title('Poverty Rate Comparison', fontweight='bold')
        ax4.set_ylabel('Poverty Rate (%)')

        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}%', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('hanover_demographics_overview.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_transportation_analysis(self):
        """Create transportation and connectivity analysis charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover, MD - Transportation Analysis', fontsize=16, fontweight='bold')

        # 1. MARC Ridership Trend (Pre/Post COVID)
        years = ['2019', '2020', '2021', '2022', '2023', '2024']
        ridership = [40000, 15000, 12000, 18000, 25000, 19300]

        ax1.plot(years, ridership, marker='o', linewidth=3, markersize=8, color='#2196F3')
        ax1.fill_between(years, ridership, alpha=0.3, color='#2196F3')
        ax1.set_title('MARC System Daily Ridership Trend', fontweight='bold')
        ax1.set_ylabel('Daily Ridership')
        ax1.grid(True, alpha=0.3)
        ax1.axvline(x=1, color='red', linestyle='--', alpha=0.7, label='COVID Impact')
        ax1.legend()

        # 2. Transportation Mode Analysis (Estimated)
        transport_modes = ['Drive Alone', 'Carpool', 'Public Transit', 'Work from Home', 'Other']
        percentages = [75, 12, 8, 4, 1]

        bars = ax2.barh(transport_modes, percentages, color=['#FF9800', '#4CAF50', '#2196F3', '#9C27B0', '#607D8B'])
        ax2.set_title('Commuting Patterns (Estimated)', fontweight='bold')
        ax2.set_xlabel('Percentage of Commuters')

        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{width}%', ha='left', va='center')

        # 3. Distance to Key Destinations
        destinations = ['Savage MARC', 'BWI Airport', 'Downtown Baltimore', 'Downtown DC', 'Arundel Mills']
        distances = [3, 15, 25, 35, 2]

        bars = ax3.bar(destinations, distances, color=['#F44336', '#FF9800', '#2196F3', '#4CAF50', '#9C27B0'])
        ax3.set_title('Distance to Key Destinations', fontweight='bold')
        ax3.set_ylabel('Miles')
        ax3.tick_params(axis='x', rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height} mi', ha='center', va='bottom')

        # 4. Traffic Volume on Major Roads (Estimated Daily Counts)
        roads = ['Route 32', 'Route 1', 'Route 100', 'Local Roads']
        traffic_volumes = [65000, 45000, 55000, 15000]

        bars = ax4.bar(roads, traffic_volumes, color=['#F44336', '#FF9800', '#4CAF50', '#2196F3'])
        ax4.set_title('Daily Traffic Volume (Estimated)', fontweight='bold')
        ax4.set_ylabel('Vehicles per Day')
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1000,
                    f'{height:,}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('hanover_transportation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_economic_opportunities_chart(self):
        """Create economic development opportunities visualization"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover, MD - Economic Development Opportunities', fontsize=16, fontweight='bold')

        # 1. Industry Opportunity Score
        industries = ['Technology', 'Professional Services', 'Healthcare', 'Retail/Dining',
                     'Logistics', 'Tourism', 'Manufacturing', 'Education']
        opportunity_scores = [9.2, 8.8, 7.5, 8.0, 7.8, 6.5, 5.2, 7.0]

        bars = ax1.barh(industries, opportunity_scores, color=plt.cm.RdYlGn(np.array(opportunity_scores)/10))
        ax1.set_title('Industry Development Opportunity Scores', fontweight='bold')
        ax1.set_xlabel('Opportunity Score (1-10)')
        ax1.set_xlim(0, 10)

        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{width}', ha='left', va='center', fontweight='bold')

        # 2. Projected Job Creation by Sector
        sectors = ['Tech', 'Prof Svc', 'Retail', 'Healthcare', 'Other']
        job_projections = [500, 300, 200, 150, 100]

        bars = ax2.bar(sectors, job_projections, color=['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0'])
        ax2.set_title('5-Year Job Creation Projections', fontweight='bold')
        ax2.set_ylabel('New Jobs')

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                    f'{height}', ha='center', va='bottom', fontweight='bold')

        # 3. Investment Requirements by Priority
        priorities = ['Transportation', 'Tech Development', 'Mixed-Use', 'Recreation', 'Education']
        investments = [15, 25, 40, 20, 10]  # in millions

        bars = ax3.bar(priorities, investments, color=['#F44336', '#2196F3', '#4CAF50', '#FF9800', '#9C27B0'])
        ax3.set_title('Investment Requirements by Priority ($M)', fontweight='bold')
        ax3.set_ylabel('Investment ($ Millions)')
        ax3.tick_params(axis='x', rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'${height}M', ha='center', va='bottom', fontweight='bold')

        # 4. Economic Impact Timeline
        years = list(range(2025, 2031))
        tax_revenue_increase = [0, 2, 5, 12, 20, 30]  # cumulative % increase

        ax4.plot(years, tax_revenue_increase, marker='o', linewidth=3, markersize=8, color='#4CAF50')
        ax4.fill_between(years, tax_revenue_increase, alpha=0.3, color='#4CAF50')
        ax4.set_title('Projected Tax Revenue Increase', fontweight='bold')
        ax4.set_ylabel('Cumulative Increase (%)')
        ax4.set_xlabel('Year')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('hanover_economic_opportunities.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_implementation_timeline(self):
        """Create implementation timeline Gantt chart"""
        fig, ax = plt.subplots(figsize=(15, 10))

        # Project data
        projects = [
            'Inter-County Coordination',
            'MARC Shuttle Service',
            'Smart Traffic Systems',
            'Tech Business District',
            'Mixed-Use Development',
            'Recreation Facilities',
            'Education Programs',
            'Cultural District'
        ]

        # Start dates and durations (in months from start)
        start_dates = [0, 3, 6, 6, 12, 18, 12, 36]
        durations = [6, 9, 18, 24, 36, 24, 18, 24]

        # Colors for different project types
        colors = ['#F44336', '#2196F3', '#FF9800', '#4CAF50', '#9C27B0', '#607D8B', '#795548', '#E91E63']

        # Create horizontal bars
        for i, (project, start, duration, color) in enumerate(zip(projects, start_dates, durations, colors)):
            ax.barh(i, duration, left=start, height=0.6, color=color, alpha=0.8)

            # Add project labels
            ax.text(start + duration/2, i, f'{project}\n({duration}mo)',
                   ha='center', va='center', fontweight='bold', fontsize=9)

        # Customize chart
        ax.set_yticks(range(len(projects)))
        ax.set_yticklabels(projects)
        ax.set_xlabel('Timeline (Months from Start)')
        ax.set_title('Hanover Improvement Implementation Timeline', fontsize=16, fontweight='bold', pad=20)

        # Add year markers
        year_marks = [0, 12, 24, 36, 48, 60]
        year_labels = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6']
        ax.set_xticks(year_marks)
        ax.set_xticklabels(year_labels)

        # Add grid
        ax.grid(True, axis='x', alpha=0.3)
        ax.set_xlim(0, 60)

        plt.tight_layout()
        plt.savefig('hanover_implementation_timeline.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_success_metrics_dashboard(self):
        """Create success metrics tracking dashboard"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover Improvement Success Metrics Dashboard', fontsize=16, fontweight='bold')

        # 1. Economic Indicators Progress
        metrics = ['Business\nRegistrations', 'Tech Jobs\nCreated', 'Tax Base\nIncrease', 'Commute Time\nReduction']
        targets = [25, 500, 30, 15]  # percentage targets
        current = [0, 0, 0, 0]  # starting at zero

        x = np.arange(len(metrics))
        width = 0.35

        bars1 = ax1.bar(x - width/2, current, width, label='Current', color='#FF9800', alpha=0.7)
        bars2 = ax1.bar(x + width/2, targets, width, label='5-Year Target', color='#4CAF50', alpha=0.7)

        ax1.set_title('Economic Development Targets', fontweight='bold')
        ax1.set_ylabel('Percentage Increase')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()

        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height}%', ha='center', va='bottom')

        # 2. Transportation Metrics
        transport_metrics = ['MARC\nRidership', 'New Transit\nRoutes', 'Traffic\nReduction', 'Bike/Walk\nInfra (mi)']
        transport_targets = [100, 3, 20, 10]  # percentage or absolute targets
        transport_current = [0, 0, 0, 0]

        x = np.arange(len(transport_metrics))
        bars1 = ax2.bar(x - width/2, transport_current, width, label='Current', color='#2196F3', alpha=0.7)
        bars2 = ax2.bar(x + width/2, transport_targets, width, label='5-Year Target', color='#F44336', alpha=0.7)

        ax2.set_title('Transportation Improvement Targets', fontweight='bold')
        ax2.set_ylabel('Percentage Increase / Units')
        ax2.set_xticks(x)
        ax2.set_xticklabels(transport_metrics)
        ax2.legend()

        # 3. Community Development Progress
        years = list(range(2025, 2031))
        community_centers = [0, 0, 1, 1, 2, 2]
        mixed_use_projects = [0, 1, 2, 3, 4, 5]

        ax3.plot(years, community_centers, marker='o', linewidth=3, label='Community Centers', color='#4CAF50')
        ax3.plot(years, mixed_use_projects, marker='s', linewidth=3, label='Mixed-Use Projects', color='#2196F3')
        ax3.set_title('Community Development Timeline', fontweight='bold')
        ax3.set_ylabel('Number of Projects')
        ax3.set_xlabel('Year')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Resident Satisfaction Gauge
        satisfaction_categories = ['Transportation', 'Recreation', 'Economic Opportunities', 'Overall Quality']
        current_satisfaction = [60, 70, 65, 72]  # percentage
        target_satisfaction = [85, 90, 85, 90]

        x = np.arange(len(satisfaction_categories))
        bars1 = ax4.barh(x - width/2, current_satisfaction, width, label='Current', color='#FF9800', alpha=0.7)
        bars2 = ax4.barh(x + width/2, target_satisfaction, width, label='Target', color='#4CAF50', alpha=0.7)

        ax4.set_title('Resident Satisfaction Metrics', fontweight='bold')
        ax4.set_xlabel('Satisfaction Score (%)')
        ax4.set_yticks(x)
        ax4.set_yticklabels(satisfaction_categories)
        ax4.legend()
        ax4.set_xlim(0, 100)

        plt.tight_layout()
        plt.savefig('hanover_success_metrics.png', dpi=300, bbox_inches='tight')
        plt.show()

    def generate_all_visualizations(self):
        """Generate all visualization charts"""
        print("=== Generating Hanover Community Improvement Visualizations ===")
        print(f"Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        print("Creating demographic overview charts...")
        self.create_demographic_overview()

        print("Creating transportation analysis charts...")
        self.create_transportation_analysis()

        print("Creating economic opportunities charts...")
        self.create_economic_opportunities_chart()

        print("Creating implementation timeline...")
        self.create_implementation_timeline()

        print("Creating success metrics dashboard...")
        self.create_success_metrics_dashboard()

        print("\n=== Visualization Generation Complete! ===")
        print("Generated files:")
        print("- hanover_demographics_overview.png")
        print("- hanover_transportation_analysis.png")
        print("- hanover_economic_opportunities.png")
        print("- hanover_implementation_timeline.png")
        print("- hanover_success_metrics.png")

if __name__ == "__main__":
    visualizer = HanoverVisualizer()
    visualizer.generate_all_visualizations()