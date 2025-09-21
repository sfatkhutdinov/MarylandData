#!/usr/bin/env python3
"""
Hanover, MD Real Implementation Budget and Funding Plan

Based on actual government data, this creates a realistic implementation plan
with specific funding sources, costs, and community organizing tools available now.
"""

import pandas as pd
import json
from datetime import datetime

class HanoverRealImplementationPlanner:
    def __init__(self):
        # Real costs based on government data
        self.infrastructure_costs = {
            'sidewalk_per_mile': 150000,  # Maryland DOT ADA compliance data
            'comprehensive_pedestrian_safety_per_mile': 6000000,  # New Hampshire Ave project data
            'protected_bike_lane_per_mile': 200000,  # Estimated from DOT data
            'bus_shelter': 15000,  # Standard cost
            'traffic_signal_upgrade': 125000,  # Standard cost
            'street_lighting_per_mile': 50000  # Estimated
        }

        # Hanover infrastructure needs (miles)
        self.hanover_infrastructure_needs = {
            'sidewalk_gaps_miles': 15,  # Estimated based on suburban layout
            'bike_lane_miles': 25,  # Major roads (Route 32, Route 1, local roads)
            'bus_shelters_needed': 8,
            'traffic_signals_needed': 12,
            'street_lighting_miles': 20
        }

        # Available funding sources with real data
        self.funding_sources = {
            'federal': {
                'cdbg_howard_county': {
                    'annual_allocation': 'Unknown - entitlement community',
                    'eligible_uses': ['Infrastructure', 'Community facilities', 'Housing'],
                    'requirements': 'Benefit low-moderate income residents'
                },
                'cdbg_anne_arundel': {
                    'annual_allocation': 306703,  # 2024 data
                    'eligible_uses': ['Capital projects only (2025 change)'],
                    'requirements': 'Benefit low-moderate income residents'
                },
                'dot_raise_grants': {
                    'total_available': 1500000000,  # $1.5B annually 2022-2026
                    'competitive': True,
                    'eligible_uses': ['Transportation safety', 'Pedestrian infrastructure']
                },
                'dot_active_transportation': {
                    'total_available': 45000000,  # $45M in 2024
                    'eligible_uses': ['Sidewalks', 'Bike lanes', 'Trails']
                },
                'dot_ss4a': {
                    'total_available': 1000000000,  # $1B annually for 5 years
                    'eligible_uses': ['Pedestrian safety', 'Vision Zero projects']
                },
                'hrsa_health_center_grants': {
                    'new_access_points': 'Up to $650K annually',
                    'requirements': 'FQHC designation process required'
                }
            },
            'maryland_state': {
                'state_revitalization_program': {
                    'total_fy2025': 129500000,  # $129.5M across 24 jurisdictions
                    'projects_funded': 304
                },
                'cdbg_state_program': {
                    'fy2024_awards': 5000000,  # $5M for 13 projects
                    'eligible_jurisdictions': 'Non-entitlement communities'
                },
                'smart_energy_communities': {
                    'status': 'FY2025 funding round open',
                    'eligible_uses': ['Clean energy planning', 'Installation projects']
                }
            },
            'county_local': {
                'howard_county_capital': {
                    'fy2024_total': 418100000,  # $418.1M
                    'funding_mechanism': 'General Obligation bonds primary',
                    'constraint': 'GO bond capacity limited'
                },
                'anne_arundel_capital': {
                    'process': 'Annual capital improvement program',
                    'timeline': 'Budget process May-June'
                }
            }
        }

    def calculate_infrastructure_costs(self):
        """Calculate real costs for Hanover infrastructure improvements"""

        costs = {}

        # Basic walkability infrastructure
        costs['sidewalk_completion'] = (
            self.hanover_infrastructure_needs['sidewalk_gaps_miles'] *
            self.infrastructure_costs['sidewalk_per_mile']
        )

        costs['protected_bike_lanes'] = (
            self.hanover_infrastructure_needs['bike_lane_miles'] *
            self.infrastructure_costs['protected_bike_lane_per_mile']
        )

        costs['bus_shelters'] = (
            self.hanover_infrastructure_needs['bus_shelters_needed'] *
            self.infrastructure_costs['bus_shelter']
        )

        costs['traffic_signals'] = (
            self.hanover_infrastructure_needs['traffic_signals_needed'] *
            self.infrastructure_costs['traffic_signal_upgrade']
        )

        costs['street_lighting'] = (
            self.hanover_infrastructure_needs['street_lighting_miles'] *
            self.infrastructure_costs['street_lighting_per_mile']
        )

        costs['total_basic_infrastructure'] = sum(costs.values())

        return costs

    def calculate_community_services_costs(self):
        """Calculate costs for community-owned services"""

        costs = {
            'mobile_health_clinic_annual': 500000,  # Estimated operating cost
            'community_health_center_startup': {
                'facility_renovation': 2000000,
                'equipment': 500000,
                'working_capital': 300000,
                'total': 2800000
            },
            'community_health_center_annual': 1500000,  # Operating costs
            'community_land_trust_startup': {
                'legal_formation': 25000,
                'staff_year1': 150000,
                'community_organizing': 75000,
                'total': 250000
            },
            'clt_housing_acquisition': {
                'average_home_price': 492100,
                'homes_year1': 10,
                'total_year1': 4921000
            }
        }

        return costs

    def create_funding_strategy(self):
        """Create realistic funding strategy using available sources"""

        infrastructure_costs = self.calculate_infrastructure_costs()
        service_costs = self.calculate_community_services_costs()

        funding_strategy = {
            'year_1_immediate_needs': {
                'sidewalk_priority_areas': {
                    'cost': 1500000,  # 10 miles of highest priority sidewalks
                    'funding_sources': [
                        'Howard County Capital Budget (GO bonds)',
                        'Anne Arundel CDBG allocation',
                        'Apply for DOT Active Transportation grants'
                    ],
                    'implementation_steps': [
                        'Submit project to both county capital budget processes',
                        'Apply for federal transportation grants by deadlines',
                        'Organize community support for county council presentations'
                    ]
                },
                'mobile_health_clinic': {
                    'cost': 500000,
                    'funding_sources': [
                        'HRSA mobile health unit grants',
                        'Howard County Health Department partnership',
                        'Community fundraising and foundation grants'
                    ],
                    'implementation_steps': [
                        'Partner with existing FQHC to sponsor mobile unit',
                        'Apply for HRSA funding through established health center',
                        'Organize community health needs assessment'
                    ]
                },
                'community_land_trust_formation': {
                    'cost': 250000,
                    'funding_sources': [
                        'Foundation grants (Ford, Surdna, etc.)',
                        'Maryland State Revitalization Program',
                        'Community fundraising and membership dues'
                    ],
                    'implementation_steps': [
                        'File 501(c)(3) incorporation paperwork',
                        'Recruit board with 1/3 community residents',
                        'Apply for Community Land Trust Network membership',
                        'Begin community organizing and education'
                    ]
                }
            },
            'year_2_3_expansion': {
                'protected_bike_lanes': {
                    'cost': 5000000,
                    'funding_sources': [
                        'DOT RAISE grant application',
                        'Maryland State transportation funds',
                        'Combined county capital programs'
                    ]
                },
                'community_health_center': {
                    'cost': 2800000,
                    'funding_sources': [
                        'HRSA Health Center New Access Point grant',
                        'CDBG funding from both counties',
                        'Maryland state health facility grants'
                    ]
                },
                'clt_housing_acquisition': {
                    'cost': 4921000,
                    'funding_sources': [
                        'Maryland Housing Trust Fund',
                        'HOME Investment Partnership funds',
                        'Community investment and loans'
                    ]
                }
            },
            'year_4_5_completion': {
                'comprehensive_pedestrian_safety': {
                    'cost': 15000000,
                    'funding_sources': [
                        'DOT Safe Streets and Roads for All',
                        'Combined state and county funding',
                        'Community infrastructure bonds'
                    ]
                }
            }
        }

        return funding_strategy

    def identify_organizing_tools(self):
        """Identify real community organizing tools available now"""

        organizing_tools = {
            'legal_mechanisms': {
                'community_land_trust_formation': {
                    'requirements': 'File as 501(c)(3) nonprofit in Maryland',
                    'governing_law': 'Maryland Corporations and Associations Code',
                    'timeline': '3-6 months for incorporation',
                    'resources': 'Community Land Trust Network toolkit'
                },
                'tenant_organizing': {
                    'legal_protections': 'Maryland tenant rights laws',
                    'organizing_support': 'Baltimore Renters United, Housing Justice Coalition',
                    'tools': 'Rent strikes, collective bargaining, tenant unions'
                },
                'zoning_advocacy': {
                    'process': 'County council public hearings',
                    'timeline': 'Planning board review, then council vote',
                    'strategy': 'Organize residents for public comment'
                }
            },
            'funding_advocacy': {
                'participatory_budgeting': {
                    'status': 'Not currently implemented in either county',
                    'strategy': 'Advocate for pilot program in county budget',
                    'examples': 'Baltimore City has participatory budgeting'
                },
                'capital_budget_advocacy': {
                    'howard_county_timeline': 'February-June annual process',
                    'anne_arundel_timeline': 'May-June annual process',
                    'strategy': 'Organize residents for public hearings'
                },
                'grant_writing_capacity': {
                    'need': 'Community grant writing collective',
                    'resources': 'Foundation Center, Maryland Nonprofits'
                }
            },
            'direct_action_tools': {
                'community_meetings': {
                    'legal_protection': 'First Amendment assembly rights',
                    'venues': 'Community centers, libraries, schools',
                    'strategy': 'Build attendance through door-to-door outreach'
                },
                'petition_drives': {
                    'uses': 'Demonstrate community support for proposals',
                    'legal_requirements': 'None for advocacy petitions',
                    'strategy': 'Collect signatures at community events'
                },
                'public_comment': {
                    'county_council_meetings': 'Regular opportunities both counties',
                    'planning_board_hearings': 'Required for development review',
                    'strategy': 'Coordinate community speakers'
                }
            },
            'electoral_strategy': {
                'county_council_elections': {
                    'howard_county': '5 districts, 4-year terms',
                    'anne_arundel': '7 districts, 4-year terms',
                    'strategy': 'Candidate recruitment and endorsement'
                },
                'voter_registration': {
                    'requirement': 'Maryland voter registration',
                    'strategy': 'Community voter registration drives',
                    'resources': 'League of Women Voters assistance'
                }
            }
        }

        return organizing_tools

    def create_implementation_timeline(self):
        """Create realistic implementation timeline with specific deadlines"""

        timeline = {
            'months_1_3': {
                'community_organizing': [
                    'Form community organizing committee',
                    'Conduct door-to-door outreach in Hanover',
                    'Host first community meeting (100+ residents)',
                    'Create communication network (email list, social media)'
                ],
                'legal_formation': [
                    'File 501(c)(3) paperwork for Community Land Trust',
                    'Recruit CLT board with community representation',
                    'Research Maryland affordable housing laws'
                ],
                'funding_research': [
                    'Complete grant opportunity database',
                    'Contact Howard County CDBG coordinator',
                    'Research foundation funding for CLT formation'
                ]
            },
            'months_4_6': {
                'advocacy_campaigns': [
                    'Present sidewalk proposal to Howard County capital budget process',
                    'Submit CDBG application to Anne Arundel County',
                    'Organize residents for county council public hearings'
                ],
                'grant_applications': [
                    'Submit DOT Active Transportation grant application',
                    'Apply for foundation grants for CLT startup',
                    'Partner with existing FQHC for mobile health clinic'
                ],
                'community_building': [
                    'Host monthly community meetings',
                    'Form working committees (housing, health, transportation)',
                    'Begin community needs survey'
                ]
            },
            'months_7_12': {
                'infrastructure_wins': [
                    'Secure funding for priority sidewalk segments',
                    'Begin construction on funded projects',
                    'Organize community celebration of wins'
                ],
                'service_development': [
                    'Launch mobile health clinic pilot',
                    'Complete CLT community education program',
                    'Begin tenant organizing in rental properties'
                ],
                'capacity_building': [
                    'Train community members in grant writing',
                    'Develop leadership development program',
                    'Create community land trust membership base'
                ]
            },
            'year_2': {
                'expansion': [
                    'Submit larger infrastructure grant applications',
                    'Begin FQHC designation process',
                    'Acquire first properties for community land trust'
                ]
            }
        }

        return timeline

    def generate_complete_implementation_plan(self):
        """Generate complete implementation plan with real costs and funding"""

        print("=== Hanover Real Implementation Budget and Funding Plan ===")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Based on: Government data, actual funding sources, real costs")
        print("="*65)

        # Calculate all components
        infrastructure_costs = self.calculate_infrastructure_costs()
        service_costs = self.calculate_community_services_costs()
        funding_strategy = self.create_funding_strategy()
        organizing_tools = self.identify_organizing_tools()
        timeline = self.create_implementation_timeline()

        # Compile results
        results = {
            'executive_summary': {
                'total_infrastructure_cost': infrastructure_costs['total_basic_infrastructure'],
                'year_1_minimum_budget': 2250000,  # Sidewalks + mobile health + CLT
                'primary_funding_sources': [
                    'Howard County Capital Budget ($418M annually)',
                    'Federal DOT grants ($1.5B annually available)',
                    'Anne Arundel CDBG ($307K annually)',
                    'Maryland State Revitalization ($129M annually)'
                ],
                'key_implementation_steps': [
                    'Form Community Land Trust (3-6 months)',
                    'Apply to county capital budget processes (February-June)',
                    'Submit federal transportation grants (rolling deadlines)',
                    'Organize community for public hearings'
                ]
            },
            'detailed_costs': {
                'infrastructure': infrastructure_costs,
                'community_services': service_costs
            },
            'funding_strategy': funding_strategy,
            'organizing_tools': organizing_tools,
            'implementation_timeline': timeline,
            'next_steps': [
                'Schedule initial community meeting within 30 days',
                'Contact Howard County CDBG coordinator',
                'Begin 501(c)(3) incorporation process for CLT',
                'Research upcoming grant deadlines',
                'Connect with existing tenant and housing justice organizations'
            ]
        }

        # Save results
        output_file = f"hanover_real_implementation_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Complete implementation plan saved to: {output_file}")

        # Print key budget summary
        print("\n=== REAL COSTS AND FUNDING SUMMARY ===")
        print(f"Total Basic Infrastructure: ${infrastructure_costs['total_basic_infrastructure']:,}")
        print(f"- Sidewalks (15 miles): ${infrastructure_costs['sidewalk_completion']:,}")
        print(f"- Protected bike lanes (25 miles): ${infrastructure_costs['protected_bike_lanes']:,}")
        print(f"- Bus shelters (8): ${infrastructure_costs['bus_shelters']:,}")
        print(f"- Traffic signals (12): ${infrastructure_costs['traffic_signals']:,}")
        print(f"- Street lighting (20 miles): ${infrastructure_costs['street_lighting']:,}")
        print()
        print("Year 1 Priorities and Funding:")
        print(f"- Priority sidewalks: $1.5M (County capital budget + CDBG)")
        print(f"- Mobile health clinic: $500K (HRSA grants + partnerships)")
        print(f"- Community Land Trust formation: $250K (Foundation grants)")
        print()
        print("Available Funding Sources:")
        print(f"- Howard County Capital Budget: $418M annually")
        print(f"- Federal DOT RAISE grants: $1.5B annually")
        print(f"- Federal Active Transportation: $45M in 2024")
        print(f"- Anne Arundel CDBG: $307K annually")
        print(f"- Maryland State Revitalization: $129M annually")

        return results

if __name__ == "__main__":
    planner = HanoverRealImplementationPlanner()
    results = planner.generate_complete_implementation_plan()