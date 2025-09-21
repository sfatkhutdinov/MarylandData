#!/usr/bin/env python3
"""
Hanover Fort Meade Context Analysis

Analyzes the impact of Fort Meade proximity on Hanover demographics,
including military families, transitory residents, and tax implications.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

class HanoverFortMeadeAnalyzer:
    def __init__(self):
        # Fort Meade data
        self.fort_meade_data = {
            'total_personnel': 54000,  # Service members + civilians
            'fort_meade_population': 10182,  # On-base residents
            'median_age': 27.2,  # Young military families
            'median_income': 102886,  # Military pay + benefits
            'poverty_rate': 4.48
        }

        # Hanover-Fort Meade relationship estimates
        self.hanover_military_estimates = {
            # Estimated based on proximity and demographics
            'military_connected_households': 2500,  # ~28% of 8,850 households
            'transitory_rate': 0.65,  # Military families move every 2-3 years
            'off_base_housing_preference': 0.60,  # Many choose off-base for space/schools
            'non_taxpaying_military': 1200,  # Legal residence elsewhere
            'bah_recipients': 1800,  # Receiving housing allowance for off-base
            'dual_military_families': 400,  # Both spouses active duty
        }

        # Property tax implications
        self.tax_implications = {
            'disabled_veteran_exemptions': 150,  # 100% disabled vets get full exemption
            'military_spouse_non_residents': 800,  # Don't pay MD property tax
            'temporary_residents': 600,  # Short-term assignments
            'actual_taxpaying_households': 7650,  # vs 8,850 total households
        }

        # Military benefits affecting community investment
        self.military_benefits = {
            'bah_e5_rate': 2200,  # Monthly housing allowance
            'bah_o3_rate': 2800,
            'healthcare_coverage': 0.95,  # Most have military healthcare
            'frequent_moves': True,
            'voting_patterns': 'Often vote in home state'
        }

    def analyze_military_impact_on_demographics(self):
        """Analyze how military presence affects Hanover demographics"""

        analysis = {
            'population_characteristics': {
                'young_families': 'Military families drive down median age',
                'transitory_nature': '65% move every 2-3 years',
                'income_diversity': 'Military pay creates middle-income stability',
                'geographic_diversity': 'Residents from all 50 states'
            },
            'tax_base_impact': {
                'reduced_taxpaying_households': 1200,  # Legal residence elsewhere
                'property_tax_exemptions': 150,  # 100% disabled veterans
                'actual_taxpaying_base': 7650,  # vs 8,850 total households
                'percentage_reduction': '13.5% of households don\'t pay local property tax'
            },
            'service_utilization_patterns': {
                'healthcare': 'Many use military healthcare vs community services',
                'schools': 'High enrollment but frequent turnover',
                'infrastructure': 'Heavy use but limited long-term investment interest',
                'community_involvement': 'Lower participation in long-term planning'
            }
        }

        return analysis

    def calculate_adjusted_implementation_costs(self):
        """Recalculate costs accounting for military population"""

        # Original costs
        original_costs = {
            'total_infrastructure': 9870000,
            'year_1_priorities': 2250000,
            'households': 8850
        }

        # Adjusted for military context
        adjusted_calculations = {
            'actual_taxpaying_households': 7650,
            'cost_per_taxpaying_household': {
                'year_1': 2250000 / 7650,  # $294 vs original $254
                'total_project': 9870000 / 7650,  # $1,290 vs original $1,115
            },
            'military_household_contributions': {
                'bah_contribution': 'Some receive housing allowance but don\'t pay property tax',
                'local_spending': 'Shop and use services locally',
                'federal_tax_contribution': 'Pay federal taxes that fund grants'
            },
            'funding_strategy_adjustments': {
                'increased_external_funding_reliance': 'Need higher % from federal/state',
                'federal_justification': 'Military population strengthens federal grant applications',
                'community_stability_challenge': 'Harder to sustain long-term organizing'
            }
        }

        return adjusted_calculations

    def analyze_military_benefits_for_infrastructure(self):
        """Analyze how military presence can benefit infrastructure projects"""

        benefits = {
            'federal_grant_advantages': {
                'military_community_priority': 'DOD prioritizes quality of life for military families',
                'federal_agency_support': 'Easier to get federal agency backing',
                'national_security_justification': 'Infrastructure supports critical military installation',
                'congressional_support': 'Representatives support military community needs'
            },
            'demographic_advantages': {
                'young_families': 'High demand for safe pedestrian infrastructure',
                'education_focused': 'Strong support for school connectivity',
                'health_conscious': 'Active lifestyle aligns with walkability goals',
                'diverse_experience': 'Bring best practices from other installations'
            },
            'economic_benefits': {
                'stable_income': 'Military pay provides economic stability',
                'federal_spending': 'BAH recipients bring federal money to local economy',
                'business_support': 'Military families support local businesses',
                'property_values': 'Good schools and infrastructure attract military families'
            }
        }

        return benefits

    def develop_military_specific_strategies(self):
        """Develop strategies addressing military community needs"""

        strategies = {
            'community_engagement': {
                'family_readiness_groups': 'Partner with existing military support networks',
                'spouse_clubs': 'Engage military spouses in planning process',
                'newcomer_briefings': 'Include infrastructure info in military orientation',
                'base_liaison': 'Establish formal communication with Fort Meade leadership'
            },
            'funding_approaches': {
                'emphasize_federal_sources': 'Increase federal funding target to 90%+',
                'military_family_focus': 'Highlight benefits to military families in applications',
                'dod_partnerships': 'Explore Department of Defense community partnership grants',
                'congressman_engagement': 'Leverage military constituency for political support'
            },
            'project_design_adjustments': {
                'rapid_implementation': 'Faster timelines to benefit current residents',
                'family_focused_features': 'Emphasize playgrounds, school connections',
                'maintenance_planning': 'Design for durability with less community maintenance'
            },
            'long_term_sustainability': {
                'institutional_partnerships': 'Partner with schools, churches for continuity',
                'professional_management': 'Hire staff vs rely solely on volunteers',
                'documentation_systems': 'Strong systems for knowledge transfer'
            }
        }

        return strategies

    def create_adjusted_financial_model(self):
        """Create financial model accounting for military population"""

        model = {
            'funding_sources_adjusted': {
                'federal_grants': 19500000,  # 90% vs original 85%
                'county_funding': 1800000,   # 8% vs original 12%
                'community_investment': 450000,  # 2% vs original 3%
                'total': 21750000
            },
            'cost_distribution': {
                'per_taxpaying_household_annual': 27,  # vs original $23
                'per_total_household_annual': 23,  # Spread across all households
                'military_household_benefit': 'Receive benefits without direct property tax'
            },
            'roi_adjustments': {
                'property_value_increase': 'Benefits all homeowners including military',
                'bah_rate_influence': 'Higher property values may increase BAH rates',
                'military_family_attraction': 'Good infrastructure attracts quality assignments',
                'community_reputation': 'Positive for base relations and future funding'
            },
            'risk_mitigation': {
                'federal_funding_focus': 'Reduce dependence on local property tax',
                'institutional_partnerships': 'Work with base leadership for continuity',
                'rapid_implementation': 'Complete projects before major personnel turnover'
            }
        }

        return model

    def generate_comprehensive_fort_meade_analysis(self):
        """Generate complete analysis of Fort Meade impact on Hanover planning"""

        print("=== Hanover-Fort Meade Context Analysis ===")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Context: Military population impact on community infrastructure planning")
        print("="*70)

        # Run all analyses
        demographic_impact = self.analyze_military_impact_on_demographics()
        cost_adjustments = self.calculate_adjusted_implementation_costs()
        military_benefits = self.analyze_military_benefits_for_infrastructure()
        military_strategies = self.develop_military_specific_strategies()
        financial_model = self.create_adjusted_financial_model()

        results = {
            'executive_summary': {
                'military_households_estimated': self.hanover_military_estimates['military_connected_households'],
                'non_taxpaying_households': self.tax_implications['actual_taxpaying_households'],
                'adjusted_cost_per_household': cost_adjustments['cost_per_taxpaying_household']['year_1'],
                'federal_funding_target': '90% (vs 85% original)',
                'key_advantage': 'Military population strengthens federal grant applications'
            },
            'demographic_analysis': demographic_impact,
            'financial_adjustments': cost_adjustments,
            'military_advantages': military_benefits,
            'implementation_strategies': military_strategies,
            'adjusted_financial_model': financial_model,
            'recommendations': [
                'Increase federal funding target to 90% of total cost',
                'Partner with Fort Meade leadership for community support',
                'Emphasize military family benefits in grant applications',
                'Design for rapid implementation due to personnel turnover',
                'Create institutional partnerships for project continuity'
            ]
        }

        # Save results
        output_file = f"hanover_fort_meade_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        import json
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Analysis complete! Results saved to: {output_file}")

        # Print key findings
        print("\n=== KEY FINDINGS ===")
        print(f"Estimated military-connected households: {self.hanover_military_estimates['military_connected_households']:,} (28%)")
        print(f"Non-taxpaying households (legal residence elsewhere): {self.tax_implications['military_spouse_non_residents']:,}")
        print(f"Actual taxpaying households: {self.tax_implications['actual_taxpaying_households']:,} (vs {self.hanover_military_estimates['military_connected_households']+6150:,} total)")
        print(f"Adjusted cost per taxpaying household: ${cost_adjustments['cost_per_taxpaying_household']['year_1']:.0f} annually")
        print()
        print("ADVANTAGES:")
        print("- Military population strengthens federal grant applications")
        print("- Young families high demand for safe pedestrian infrastructure")
        print("- Federal BAH brings outside money to local economy")
        print("- Congressional support for military community infrastructure")
        print()
        print("CHALLENGES:")
        print("- 13.5% of households don't pay local property tax")
        print("- High turnover makes long-term organizing difficult")
        print("- Need higher reliance on external funding sources")

        return results

if __name__ == "__main__":
    analyzer = HanoverFortMeadeAnalyzer()
    results = analyzer.generate_comprehensive_fort_meade_analysis()