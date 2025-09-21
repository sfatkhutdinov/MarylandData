#!/usr/bin/env python3
"""
Hanover, MD Human-Centered Visualization Generator

Creates charts focused on community wellbeing, cooperative ownership,
and human-centered development metrics rather than profit-driven indicators.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.patches as patches

# Set style for community-focused charts
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")  # More community-friendly colors

class HumanCenteredVisualizer:
    def __init__(self):
        # Community wellbeing data
        self.current_state = {
            'walkability_score': 2,  # Out of 10
            'healthcare_access': 3,  # Out of 10
            'housing_security': 4,  # Out of 10
            'community_ownership': 1,  # Out of 10
            'democratic_participation': 2,  # Out of 10
            'food_security': 6,  # Out of 10
            'social_connection': 5,  # Out of 10
            'environmental_health': 6  # Out of 10
        }

        self.target_state = {
            'walkability_score': 9,
            'healthcare_access': 10,
            'housing_security': 9,
            'community_ownership': 8,
            'democratic_participation': 9,
            'food_security': 9,
            'social_connection': 9,
            'environmental_health': 8
        }

    def create_community_wellbeing_assessment(self):
        """Create current vs target community wellbeing radar chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), subplot_kw=dict(projection='polar'))
        fig.suptitle('Hanover Community Wellbeing: Current State vs Human-Centered Vision',
                     fontsize=16, fontweight='bold', y=0.95)

        # Categories for radar chart
        categories = list(self.current_state.keys())
        categories_clean = [cat.replace('_', ' ').title() for cat in categories]

        # Current state radar
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        current_values = list(self.current_state.values()) + [list(self.current_state.values())[0]]
        target_values = list(self.target_state.values()) + [list(self.target_state.values())[0]]

        # Plot current state
        ax1.plot(angles, current_values, 'o-', linewidth=2, label='Current State', color='#FF6B6B')
        ax1.fill(angles, current_values, alpha=0.25, color='#FF6B6B')
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories_clean, fontsize=10)
        ax1.set_ylim(0, 10)
        ax1.set_title('Current Community Wellbeing\n(Out of 10)', fontweight='bold', pad=20)
        ax1.grid(True)

        # Plot target state
        ax2.plot(angles, target_values, 'o-', linewidth=2, label='Human-Centered Vision', color='#4ECDC4')
        ax2.fill(angles, target_values, alpha=0.25, color='#4ECDC4')
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories_clean, fontsize=10)
        ax2.set_ylim(0, 10)
        ax2.set_title('Human-Centered Vision\n(Target State)', fontweight='bold', pad=20)
        ax2.grid(True)

        plt.tight_layout()
        plt.savefig('hanover_community_wellbeing_assessment.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_cooperative_ownership_progression(self):
        """Show progression from corporate to community ownership"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover: Transition to Community Ownership Economy', fontsize=16, fontweight='bold')

        # 1. Current vs Cooperative Ownership
        sectors = ['Healthcare', 'Housing', 'Food/Grocery', 'Childcare', 'Transportation',
                  'Banking', 'Utilities', 'Internet']
        current_ownership = [10, 5, 15, 20, 5, 0, 0, 0]  # % community owned
        target_ownership = [90, 70, 80, 85, 60, 75, 50, 40]  # % community owned target

        x = np.arange(len(sectors))
        width = 0.35

        bars1 = ax1.bar(x - width/2, current_ownership, width, label='Current Community Ownership',
                       color='#FF6B6B', alpha=0.7)
        bars2 = ax1.bar(x + width/2, target_ownership, width, label='Human-Centered Target',
                       color='#4ECDC4', alpha=0.7)

        ax1.set_title('Community vs Corporate Ownership by Sector', fontweight='bold')
        ax1.set_ylabel('Percentage Community Owned')
        ax1.set_xlabel('Essential Services')
        ax1.set_xticks(x)
        ax1.set_xticklabels(sectors, rotation=45, ha='right')
        ax1.legend()
        ax1.set_ylim(0, 100)

        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'{height}%', ha='center', va='bottom', fontsize=9)

        # 2. Housing Security Progression
        years = ['Current', 'Year 2', 'Year 4', 'Year 6']
        community_land_trust = [0, 100, 400, 800]  # number of homes
        cooperative_housing = [0, 50, 200, 500]
        affordable_rental = [200, 300, 400, 500]

        ax2.bar(years, community_land_trust, label='Community Land Trust', color='#4ECDC4')
        ax2.bar(years, cooperative_housing, bottom=community_land_trust,
               label='Housing Cooperatives', color='#45B7D1')
        ax2.bar(years, affordable_rental,
               bottom=np.array(community_land_trust) + np.array(cooperative_housing),
               label='Protected Affordable Rental', color='#96CEB4')

        ax2.set_title('Community-Controlled Housing Development', fontweight='bold')
        ax2.set_ylabel('Number of Homes')
        ax2.legend()

        # 3. Healthcare Access Model
        healthcare_models = ['Current\n(Private/Insurance)', 'Mobile Clinics\n(Year 1)',
                           'Community Health Center\n(Year 3)', 'Universal Access\n(Year 5)']
        access_percentage = [65, 85, 95, 100]  # % of residents with access
        cost_burden = [25, 15, 5, 0]  # % income spent on healthcare

        # Create twin axis
        ax3_twin = ax3.twinx()

        bars1 = ax3.bar(healthcare_models, access_percentage, color='#4ECDC4', alpha=0.7,
                       label='Healthcare Access %')
        bars2 = ax3_twin.bar(healthcare_models, cost_burden, color='#FF6B6B', alpha=0.7,
                            width=0.5, label='Cost Burden %')

        ax3.set_title('Universal Healthcare Access Progression', fontweight='bold')
        ax3.set_ylabel('Percentage with Healthcare Access', color='#4ECDC4')
        ax3_twin.set_ylabel('Healthcare Cost Burden (% of income)', color='#FF6B6B')
        ax3.set_ylim(0, 105)
        ax3_twin.set_ylim(0, 30)

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height}%', ha='center', va='bottom', fontweight='bold')

        # 4. Democratic Participation Growth
        participation_metrics = ['Community\nMeetings', 'Participatory\nBudgeting',
                               'Cooperative\nMembership', 'Community\nOrganizing']
        current_participation = [5, 0, 2, 8]  # % of residents participating
        target_participation = [40, 25, 35, 30]

        x = np.arange(len(participation_metrics))
        bars1 = ax4.bar(x - width/2, current_participation, width, label='Current Participation',
                       color='#FF6B6B', alpha=0.7)
        bars2 = ax4.bar(x + width/2, target_participation, width, label='Human-Centered Target',
                       color='#4ECDC4', alpha=0.7)

        ax4.set_title('Democratic Participation Growth', fontweight='bold')
        ax4.set_ylabel('Percentage of Residents Participating')
        ax4.set_xticks(x)
        ax4.set_xticklabels(participation_metrics)
        ax4.legend()

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height}%', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.savefig('hanover_cooperative_ownership_progression.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_walkability_and_access_maps(self):
        """Create walkability access analysis"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover: Universal Access and Walkability Analysis', fontsize=16, fontweight='bold')

        # 1. Current vs Target Walking Times to Essential Services
        services = ['Grocery Store', 'Health Center', 'Community Center', 'Public Transit',
                   'School', 'Pharmacy', 'Bank/Credit Union', 'Park/Green Space']
        current_walk_times = [25, 45, 30, 20, 15, 20, 18, 12]  # minutes walking
        target_walk_times = [8, 10, 5, 8, 10, 8, 10, 5]  # 15-minute neighborhood target

        x = np.arange(len(services))
        width = 0.35

        bars1 = ax1.barh(x - width/2, current_walk_times, width, label='Current Walk Time',
                        color='#FF6B6B', alpha=0.7)
        bars2 = ax1.barh(x + width/2, target_walk_times, width, label='15-Minute Target',
                        color='#4ECDC4', alpha=0.7)

        ax1.set_title('Walking Time to Essential Services', fontweight='bold')
        ax1.set_xlabel('Walking Time (Minutes)')
        ax1.set_yticks(x)
        ax1.set_yticklabels(services)
        ax1.legend()
        ax1.axvline(x=15, color='green', linestyle='--', alpha=0.7, label='15-Min Target')

        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                width_val = bar.get_width()
                ax1.text(width_val + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{width_val}m', ha='left', va='center', fontsize=9)

        # 2. Transportation Mode Shift
        transport_modes = ['Drive Alone', 'Walking', 'Cycling', 'Public Transit', 'Carpooling']
        current_modal_split = [78, 5, 2, 8, 7]
        target_modal_split = [35, 25, 20, 15, 5]

        x = np.arange(len(transport_modes))
        bars1 = ax2.bar(x - width/2, current_modal_split, width, label='Current Mode Share',
                       color='#FF6B6B', alpha=0.7)
        bars2 = ax2.bar(x + width/2, target_modal_split, width, label='Human-Centered Target',
                       color='#4ECDC4', alpha=0.7)

        ax2.set_title('Transportation Mode Shift to Sustainable Options', fontweight='bold')
        ax2.set_ylabel('Percentage of Trips')
        ax2.set_xlabel('Transportation Mode')
        ax2.set_xticks(x)
        ax2.set_xticklabels(transport_modes, rotation=45, ha='right')
        ax2.legend()

        # 3. Housing Affordability Burden
        income_groups = ['Very Low Income\n(<50% AMI)', 'Low Income\n(50-80% AMI)',
                        'Moderate Income\n(80-120% AMI)', 'Above Moderate\n(>120% AMI)']
        current_housing_burden = [65, 45, 35, 20]  # % of income spent on housing
        target_housing_burden = [25, 25, 25, 25]  # 30% or less target

        x = np.arange(len(income_groups))
        bars1 = ax3.bar(x - width/2, current_housing_burden, width, label='Current Housing Burden',
                       color='#FF6B6B', alpha=0.7)
        bars2 = ax3.bar(x + width/2, target_housing_burden, width, label='Community Ownership Target',
                       color='#4ECDC4', alpha=0.7)

        ax3.set_title('Housing Affordability: Community Ownership Impact', fontweight='bold')
        ax3.set_ylabel('Percentage of Income Spent on Housing')
        ax3.set_xlabel('Income Level')
        ax3.set_xticks(x)
        ax3.set_xticklabels(income_groups, fontsize=9)
        ax3.legend()
        ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Affordable Threshold')

        # 4. Community Wealth vs Extraction
        wealth_categories = ['Housing\nAppreciation', 'Local Business\nProfits', 'Healthcare\nSavings',
                           'Financial\nServices', 'Utility\nSavings']
        wealth_extracted = [15, 8, 12, 5, 3]  # millions extracted annually
        wealth_retained = [2, 12, 18, 8, 6]   # millions retained with community ownership

        x = np.arange(len(wealth_categories))
        bars1 = ax4.bar(x - width/2, wealth_extracted, width, label='Current: Wealth Extracted',
                       color='#FF6B6B', alpha=0.7)
        bars2 = ax4.bar(x + width/2, wealth_retained, width, label='Community Ownership: Wealth Retained',
                       color='#4ECDC4', alpha=0.7)

        ax4.set_title('Community Wealth: Extraction vs Retention', fontweight='bold')
        ax4.set_ylabel('Annual Amount ($ Millions)')
        ax4.set_xlabel('Wealth Category')
        ax4.set_xticks(x)
        ax4.set_xticklabels(wealth_categories, fontsize=9)
        ax4.legend()

        plt.tight_layout()
        plt.savefig('hanover_walkability_and_access.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_implementation_timeline_human_centered(self):
        """Create human-centered implementation timeline"""
        fig, ax = plt.subplots(figsize=(16, 10))

        # Human-centered projects
        projects = [
            'Complete Sidewalk Network',
            'Mobile Health Clinics Launch',
            'Community Organizing Infrastructure',
            'Tenant Protection Ordinances',
            'Community Land Trust Formation',
            'Community Health Center (FQHC)',
            'Protected Bike Lane Network',
            'Community-Owned Grocery Cooperative',
            'Public Banking Option',
            'Universal Healthcare Access',
            'Participatory Budgeting',
            'Community-Owned Utilities'
        ]

        # Timeline data (start month, duration in months)
        timeline_data = [
            (0, 12),   # Sidewalk network
            (3, 6),    # Mobile health
            (0, 18),   # Community organizing
            (6, 6),    # Tenant protections
            (9, 18),   # Land trust
            (12, 24),  # Health center
            (15, 18),  # Bike lanes
            (18, 12),  # Grocery coop
            (24, 18),  # Public banking
            (30, 18),  # Universal healthcare
            (18, 24),  # Participatory budgeting
            (36, 24)   # Community utilities
        ]

        # Colors for different project types
        colors = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD',
                 '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#82E0AA',
                 '#F8C471', '#D7BDE2']

        # Create horizontal bars
        for i, (project, (start, duration), color) in enumerate(zip(projects, timeline_data, colors)):
            ax.barh(i, duration, left=start, height=0.6, color=color, alpha=0.8)

            # Add project labels
            ax.text(start + duration/2, i, f'{project}\n({duration}mo)',
                   ha='center', va='center', fontweight='bold', fontsize=9)

        # Customize chart
        ax.set_yticks(range(len(projects)))
        ax.set_yticklabels(projects)
        ax.set_xlabel('Timeline (Months from Start)')
        ax.set_title('Hanover Human-Centered Implementation Timeline\nPrioritizing Community Wellbeing Over Profit',
                     fontsize=16, fontweight='bold', pad=20)

        # Add phase markers
        phase_markers = [0, 12, 24, 36, 48, 60]
        phase_labels = ['Start', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
        ax.set_xticks(phase_markers)
        ax.set_xticklabels(phase_labels)

        # Add phase background colors
        ax.axvspan(0, 12, alpha=0.1, color='red', label='Foundation (Year 1)')
        ax.axvspan(12, 24, alpha=0.1, color='orange', label='Service Development (Year 2)')
        ax.axvspan(24, 36, alpha=0.1, color='yellow', label='Ownership Transition (Year 3)')
        ax.axvspan(36, 48, alpha=0.1, color='green', label='System Integration (Year 4)')
        ax.axvspan(48, 60, alpha=0.1, color='blue', label='Model Community (Year 5)')

        ax.grid(True, axis='x', alpha=0.3)
        ax.set_xlim(0, 60)
        ax.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig('hanover_human_centered_timeline.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_community_power_dashboard(self):
        """Create dashboard showing community power and democratic participation"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Hanover Community Power and Democratic Participation Dashboard',
                     fontsize=16, fontweight='bold')

        # 1. Community Control vs Corporate Control
        sectors = ['Housing', 'Healthcare', 'Food', 'Banking', 'Utilities', 'Transportation']
        current_community_control = [5, 10, 15, 0, 0, 5]
        target_community_control = [70, 90, 80, 75, 50, 60]

        x = np.arange(len(sectors))
        width = 0.35

        bars1 = ax1.bar(x - width/2, current_community_control, width,
                       label='Current Community Control', color='#FF6B6B', alpha=0.7)
        bars2 = ax1.bar(x + width/2, target_community_control, width,
                       label='Democratic Ownership Target', color='#4ECDC4', alpha=0.7)

        ax1.set_title('Community vs Corporate Control by Sector', fontweight='bold')
        ax1.set_ylabel('Percentage Under Community Control')
        ax1.set_xlabel('Essential Services')
        ax1.set_xticks(x)
        ax1.set_xticklabels(sectors)
        ax1.legend()
        ax1.set_ylim(0, 100)

        # 2. Democratic Participation Growth Over Time
        years = ['Current', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
        community_meetings = [5, 15, 25, 35, 40, 45]
        cooperative_membership = [2, 8, 18, 28, 35, 40]
        participatory_budgeting = [0, 0, 10, 20, 25, 30]

        ax2.plot(years, community_meetings, marker='o', linewidth=3, label='Community Meeting Attendance', color='#4ECDC4')
        ax2.plot(years, cooperative_membership, marker='s', linewidth=3, label='Cooperative Membership', color='#45B7D1')
        ax2.plot(years, participatory_budgeting, marker='^', linewidth=3, label='Participatory Budgeting', color='#96CEB4')

        ax2.set_title('Democratic Participation Growth', fontweight='bold')
        ax2.set_ylabel('Percentage of Residents Participating')
        ax2.set_xlabel('Timeline')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 50)

        # 3. Community Wellbeing vs Income Levels
        wellbeing_indicators = ['Healthcare\nAccess', 'Housing\nSecurity', 'Food\nSecurity',
                              'Transportation\nAccess', 'Community\nConnection']
        low_income_current = [40, 30, 60, 45, 55]
        low_income_target = [100, 90, 95, 90, 85]
        high_income_current = [85, 90, 95, 90, 70]

        x = np.arange(len(wellbeing_indicators))
        width = 0.25

        bars1 = ax3.bar(x - width, low_income_current, width, label='Low Income (Current)',
                       color='#FF6B6B', alpha=0.7)
        bars2 = ax3.bar(x, low_income_target, width, label='Low Income (With Universal Services)',
                       color='#4ECDC4', alpha=0.7)
        bars3 = ax3.bar(x + width, high_income_current, width, label='High Income (Current)',
                       color='#96CEB4', alpha=0.7)

        ax3.set_title('Universal Access: Eliminating Income-Based Wellbeing Gaps', fontweight='bold')
        ax3.set_ylabel('Access Score (0-100)')
        ax3.set_xlabel('Wellbeing Indicators')
        ax3.set_xticks(x)
        ax3.set_xticklabels(wellbeing_indicators, fontsize=9)
        ax3.legend()
        ax3.set_ylim(0, 105)

        # 4. Community Wealth Building vs Extraction
        wealth_flows = ['Housing\nEquity', 'Business\nProfits', 'Healthcare\nSavings',
                       'Banking\nReturns', 'Energy\nSavings']
        extracted_current = [15, 8, 12, 5, 3]  # millions leaving community
        retained_target = [25, 18, 22, 12, 8]  # millions staying in community

        x = np.arange(len(wealth_flows))
        bars1 = ax4.bar(x - width/2, [-x for x in extracted_current], width,
                       label='Current: Wealth Extracted', color='#FF6B6B', alpha=0.7)
        bars2 = ax4.bar(x + width/2, retained_target, width,
                       label='Target: Community Wealth Retained', color='#4ECDC4', alpha=0.7)

        ax4.set_title('Community Wealth: From Extraction to Retention', fontweight='bold')
        ax4.set_ylabel('Annual Wealth Flow ($ Millions)')
        ax4.set_xlabel('Wealth Categories')
        ax4.set_xticks(x)
        ax4.set_xticklabels(wealth_flows, fontsize=9)
        ax4.legend()
        ax4.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax4.text(2, -8, 'Wealth Leaving\nCommunity', ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#FF6B6B', alpha=0.3))
        ax4.text(2, 15, 'Wealth Staying in\nCommunity', ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#4ECDC4', alpha=0.3))

        plt.tight_layout()
        plt.savefig('hanover_community_power_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()

    def generate_all_human_centered_visualizations(self):
        """Generate all human-centered visualization charts"""
        print("=== Generating Hanover Human-Centered Community Visualizations ===")
        print(f"Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Focus: Community wellbeing, cooperative ownership, and democratic participation")
        print("="*75)

        print("Creating community wellbeing assessment...")
        self.create_community_wellbeing_assessment()

        print("Creating cooperative ownership progression charts...")
        self.create_cooperative_ownership_progression()

        print("Creating walkability and universal access analysis...")
        self.create_walkability_and_access_maps()

        print("Creating human-centered implementation timeline...")
        self.create_implementation_timeline_human_centered()

        print("Creating community power dashboard...")
        self.create_community_power_dashboard()

        print("\n=== Human-Centered Visualization Generation Complete! ===")
        print("Generated files:")
        print("- hanover_community_wellbeing_assessment.png")
        print("- hanover_cooperative_ownership_progression.png")
        print("- hanover_walkability_and_access.png")
        print("- hanover_human_centered_timeline.png")
        print("- hanover_community_power_dashboard.png")
        print("\nThese charts focus on:")
        print("✓ Community wellbeing over profit margins")
        print("✓ Cooperative ownership over corporate control")
        print("✓ Universal access over market-based exclusion")
        print("✓ Democratic participation over top-down planning")
        print("✓ Community wealth building over extraction")

if __name__ == "__main__":
    visualizer = HumanCenteredVisualizer()
    visualizer.generate_all_human_centered_visualizations()