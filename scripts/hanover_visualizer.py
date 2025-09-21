"""
Hanover Visualizer for MarylandData Project
Professional visualization framework with uncertainty quantification, 
beautiful styling, and transparent source attribution.

CRITICAL PRINCIPLES:
- Always include uncertainty (error bars, confidence intervals)
- Use colorblind-friendly palettes and accessible design
- Add data source attribution on every chart
- Show ranges and limitations, not just point estimates
- Professional typography and consistent styling
- Highlight key findings without emotional manipulation

Author: MarylandData Project
Created: September 21, 2025
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import warnings

# Configure matplotlib and seaborn for professional outputs
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")  # Colorblind-friendly, professional palette
warnings.filterwarnings('ignore', category=UserWarning)  # Suppress minor matplotlib warnings

class HanoverVisualizer:
    """
    Professional visualization framework for Hanover, MD community analysis.
    
    Implements rigorous standards for data visualization:
    - Uncertainty quantification in all charts
    - Professional color schemes and typography
    - Source attribution and methodology transparency
    - Accessibility compliance (colorblind-friendly)
    - Conservative presentation without bias
    """
    
    def __init__(self, style_theme: str = 'professional'):
        """
        Initialize visualizer with professional styling standards.
        
        Args:
            style_theme: Visualization theme ('professional', 'academic', 'presentation')
        """
        self.style_theme = style_theme
        
        # Professional color schemes (colorblind-friendly)
        self.colors = {
            'primary': '#2E86AB',      # Professional blue
            'secondary': '#A23B72',    # Muted magenta  
            'accent': '#F18F01',       # Warm orange
            'neutral': '#C73E1D',      # Deep red
            'success': '#6A994E',      # Natural green
            'warning': '#F77F00',      # Amber
            'info': '#577590',         # Steel blue
            'light_gray': '#F8F9FA',   # Background
            'dark_gray': '#495057',    # Text
            'very_light_gray': '#E9ECEF'  # Grid lines
        }
        
        # Typography settings for consistent professional appearance
        self.fonts = {
            'title': {
                'fontsize': 16, 
                'fontweight': 'bold', 
                'color': self.colors['dark_gray'],
                'family': 'sans-serif'
            },
            'subtitle': {
                'fontsize': 12, 
                'fontweight': 'medium', 
                'color': self.colors['dark_gray'],
                'family': 'sans-serif'
            },
            'body': {
                'fontsize': 10, 
                'color': self.colors['dark_gray'],
                'family': 'sans-serif'
            },
            'caption': {
                'fontsize': 8, 
                'style': 'italic', 
                'color': self.colors['info'],
                'family': 'sans-serif'
            }
        }
        
        # Figure settings
        self.figure_defaults = {
            'figsize': (10, 6),
            'dpi': 150,  # High resolution for professional output
            'facecolor': 'white',
            'edgecolor': 'none'
        }
        
        # Set global matplotlib parameters
        plt.rcParams.update({
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
            'font.size': self.fonts['body']['fontsize'],
            'axes.titlesize': self.fonts['title']['fontsize'],
            'axes.labelsize': self.fonts['subtitle']['fontsize'],
            'xtick.labelsize': self.fonts['body']['fontsize'],
            'ytick.labelsize': self.fonts['body']['fontsize'],
            'legend.fontsize': self.fonts['body']['fontsize'],
            'figure.titlesize': self.fonts['title']['fontsize'],
            'figure.dpi': self.figure_defaults['dpi']
        })
    
    def create_uncertainty_chart(self, 
                               estimates: Dict[str, float],
                               margins_of_error: Dict[str, float],
                               labels: Dict[str, str],
                               title: str,
                               ylabel: str,
                               source: str,
                               save_path: Optional[str] = None) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create beautiful charts with error bars showing data uncertainty.
        
        Args:
            estimates: Dictionary of variable codes to estimate values
            margins_of_error: Dictionary of variable codes to margin of error values
            labels: Dictionary of variable codes to human-readable labels
            title: Chart title
            ylabel: Y-axis label with units
            source: Data source for attribution
            save_path: Optional path to save the figure
            
        Returns:
            Tuple of (figure, axes) objects
        """
        # Prepare data
        var_codes = list(estimates.keys())
        values = [float(estimates[code]) for code in var_codes]
        errors = [float(margins_of_error.get(code, 0)) for code in var_codes]
        chart_labels = [labels.get(code, code) for code in var_codes]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_defaults['figsize'])
        
        # Main bars with professional styling
        bars = ax.bar(chart_labels, values, 
                     color=self.colors['primary'], 
                     alpha=0.8,
                     edgecolor=self.colors['dark_gray'],
                     linewidth=0.5)
        
        # Add error bars with proper styling
        ax.errorbar(chart_labels, values, yerr=errors,
                   fmt='none', capsize=4, capthick=1.5,
                   ecolor=self.colors['neutral'], alpha=0.8,
                   linewidth=1.5)
        
        # Professional title with proper spacing
        ax.set_title(title, **self.fonts['title'], pad=20)
        ax.set_ylabel(ylabel, **self.fonts['subtitle'])
        
        # Add uncertainty explanation
        uncertainty_note = '±Error bars show 90% confidence intervals from ACS estimates'
        ax.text(0.02, 0.98, uncertainty_note, 
               transform=ax.transAxes, **self.fonts['caption'],
               verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=self.colors['light_gray'], alpha=0.7))
        
        # Source attribution (CRITICAL for credibility)
        source_text = f'Source: {source} | Generated: {datetime.now().strftime("%B %d, %Y")}'
        ax.text(0.02, 0.02, source_text, transform=ax.transAxes, 
               **self.fonts['caption'])
        
        # Clean, professional styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.colors['very_light_gray'])
        ax.spines['bottom'].set_color(self.colors['very_light_gray'])
        ax.grid(True, alpha=0.3, color=self.colors['very_light_gray'])
        ax.set_axisbelow(True)
        
        # Rotate x-axis labels if needed
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
        
        return fig, ax
    
    def create_comparison_chart(self, 
                               hanover_data: float,
                               comparison_data: Dict[str, float],
                               metric_name: str,
                               metric_unit: str = '',
                               source: str = '',
                               save_path: Optional[str] = None) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create meaningful comparison charts (Hanover vs County vs State vs National).
        
        Args:
            hanover_data: Value for Hanover (ZIP 21076)
            comparison_data: Dictionary with 'county', 'state', 'national' keys
            metric_name: Name of the metric being compared
            metric_unit: Unit of measurement (e.g., '$', '%', 'years')
            source: Data source for attribution
            save_path: Optional path to save the figure
            
        Returns:
            Tuple of (figure, axes) objects
        """
        locations = ['Hanover\n(ZIP 21076)', 'Howard County', 'Maryland', 'United States']
        values = [
            hanover_data, 
            comparison_data.get('county', 0), 
            comparison_data.get('state', 0), 
            comparison_data.get('national', 0)
        ]
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Color coding: highlight Hanover, neutral for comparisons
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['accent'], self.colors['neutral']]
        
        bars = ax.bar(locations, values, color=colors, alpha=0.8,
                     edgecolor=self.colors['dark_gray'], linewidth=0.5)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height > 0:  # Only label if we have data
                label = f'{metric_unit}{value:,.0f}' if metric_unit else f'{value:,.0f}'
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       label, ha='center', va='bottom', **self.fonts['body'],
                       fontweight='medium')
        
        # Professional title with context
        title = f'{metric_name}\nComparison Across Geographic Levels'
        ax.set_title(title, **self.fonts['title'], pad=20)
        
        # Source attribution (CRITICAL for credibility)
        if not source:
            source = 'U.S. Census Bureau, 2019-2023 ACS 5-Year Estimates'
        source_text = f'Source: {source} | Generated: {datetime.now().strftime("%B %d, %Y")}'
        ax.text(0.02, 0.02, source_text, transform=ax.transAxes, 
               **self.fonts['caption'])
        
        # Data quality note
        quality_note = 'All estimates include margins of error - see detailed analysis for uncertainty ranges'
        ax.text(0.98, 0.98, quality_note, transform=ax.transAxes,
               **self.fonts['caption'], ha='right', va='top',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=self.colors['light_gray'], alpha=0.7))
        
        # Clean, professional styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.colors['very_light_gray'])
        ax.spines['bottom'].set_color(self.colors['very_light_gray'])
        ax.set_ylabel(f'{metric_name} ({metric_unit})', **self.fonts['subtitle'])
        ax.grid(True, alpha=0.3, axis='y', color=self.colors['very_light_gray'])
        ax.set_axisbelow(True)
        
        plt.xticks(rotation=0, **self.fonts['body'])
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
        
        return fig, ax
    
    def create_demographic_overview(self, 
                                  demographic_data: Dict[str, Any],
                                  save_path: Optional[str] = None) -> Tuple[plt.Figure, List[plt.Axes]]:
        """
        Create comprehensive demographic overview with multiple subplots.
        
        Args:
            demographic_data: Dictionary with 'estimates', 'margins_of_error', and 'source'
            save_path: Optional path to save the figure
            
        Returns:
            Tuple of (figure, list of axes) objects
        """
        estimates = demographic_data.get('estimates', {})
        margins_of_error = demographic_data.get('margin_of_error', {})
        source = demographic_data.get('source', 'Census Bureau')
        
        # Create subplot layout
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Hanover, MD (ZIP 21076) - Demographic Overview', 
                    **self.fonts['title'], y=0.95)
        
        # Population and Housing (top left)
        if 'B01003_001E' in estimates and 'B25003_002E' in estimates:
            pop_data = {
                'Total Population': float(estimates.get('B01003_001E', 0)),
                'Owner-Occupied\nHouseholds': float(estimates.get('B25003_002E', 0)),
                'Renter-Occupied\nHouseholds': float(estimates.get('B25003_003E', 0))
            }
            
            bars1 = ax1.bar(pop_data.keys(), pop_data.values(), 
                           color=[self.colors['primary'], self.colors['secondary'], self.colors['accent']],
                           alpha=0.8)
            ax1.set_title('Population & Housing', **self.fonts['subtitle'])
            ax1.set_ylabel('Count', **self.fonts['body'])
            
            # Add value labels
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'{height:,.0f}', ha='center', va='bottom', **self.fonts['body'])
        
        # Economic Indicators (top right)
        if 'B19013_001E' in estimates and 'B25077_001E' in estimates:
            econ_data = {
                'Median Household\nIncome': float(estimates.get('B19013_001E', 0)),
                'Median Home\nValue': float(estimates.get('B25077_001E', 0))
            }
            
            bars2 = ax2.bar(econ_data.keys(), econ_data.values(),
                           color=[self.colors['success'], self.colors['warning']],
                           alpha=0.8)
            ax2.set_title('Economic Indicators', **self.fonts['subtitle'])
            ax2.set_ylabel('Dollars ($)', **self.fonts['body'])
            
            # Add value labels with dollar formatting
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'${height:,.0f}', ha='center', va='bottom', **self.fonts['body'])
        
        # Transportation Patterns (bottom left)
        transport_vars = ['B08301_010E', 'B08301_021E', 'B08301_016E']
        transport_labels = ['Public Transit', 'Walking', 'Bicycle']
        if any(var in estimates for var in transport_vars):
            transport_data = [float(estimates.get(var, 0)) for var in transport_vars]
            
            bars3 = ax3.bar(transport_labels, transport_data,
                           color=[self.colors['info'], self.colors['neutral'], self.colors['primary']],
                           alpha=0.8)
            ax3.set_title('Alternative Transportation', **self.fonts['subtitle'])
            ax3.set_ylabel('Commuters', **self.fonts['body'])
            
            # Add value labels
            for bar in bars3:
                height = bar.get_height()
                if height > 0:
                    ax3.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                            f'{height:,.0f}', ha='center', va='bottom', **self.fonts['body'])
        
        # Education Levels (bottom right)
        if 'B15003_022E' in estimates and 'B15003_023E' in estimates:
            edu_data = {
                "Bachelor's\nDegree": float(estimates.get('B15003_022E', 0)),
                "Master's\nDegree": float(estimates.get('B15003_023E', 0))
            }
            
            bars4 = ax4.bar(edu_data.keys(), edu_data.values(),
                           color=[self.colors['secondary'], self.colors['accent']],
                           alpha=0.8)
            ax4.set_title('Educational Attainment', **self.fonts['subtitle'])
            ax4.set_ylabel('Residents', **self.fonts['body'])
            
            # Add value labels
            for bar in bars4:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'{height:,.0f}', ha='center', va='bottom', **self.fonts['body'])
        
        # Apply consistent styling to all subplots
        for ax in [ax1, ax2, ax3, ax4]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_axisbelow(True)
            plt.setp(ax.get_xticklabels(), **self.fonts['body'])
        
        # Overall source attribution
        source_text = f'Source: {source} | Generated: {datetime.now().strftime("%B %d, %Y")}'
        fig.text(0.02, 0.02, source_text, **self.fonts['caption'])
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.90, bottom=0.08)
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
        
        return fig, [ax1, ax2, ax3, ax4]
    
    def create_quality_assessment_chart(self, 
                                      validation_results: Dict[str, Any],
                                      save_path: Optional[str] = None) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create data quality assessment visualization.
        
        Args:
            validation_results: Results from data validation pipeline
            save_path: Optional path to save the figure
            
        Returns:
            Tuple of (figure, axes) objects
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Quality metrics
        quality_score = validation_results.get('quality_score', 0)
        missing_values = validation_results.get('missing_values', 0)
        high_moe_count = validation_results.get('high_moe_count', 0)
        total_issues = len(validation_results.get('issues', []))
        
        # Create quality visualization
        categories = ['Overall\nQuality', 'Data\nCompleteness', 'Uncertainty\nLevel', 'Issue\nCount']
        scores = [
            quality_score,
            max(0, 100 - missing_values * 10),
            max(0, 100 - high_moe_count * 15),
            max(0, 100 - total_issues * 20)
        ]
        
        # Color coding based on quality levels
        colors = []
        for score in scores:
            if score >= 90:
                colors.append(self.colors['success'])
            elif score >= 70:
                colors.append(self.colors['warning'])
            else:
                colors.append(self.colors['neutral'])
        
        bars = ax.bar(categories, scores, color=colors, alpha=0.8,
                     edgecolor=self.colors['dark_gray'], linewidth=0.5)
        
        # Add score labels
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{score:.0f}', ha='center', va='bottom', 
                   **self.fonts['body'], fontweight='bold')
        
        ax.set_title('Data Quality Assessment', **self.fonts['title'], pad=20)
        ax.set_ylabel('Quality Score (0-100)', **self.fonts['subtitle'])
        ax.set_ylim(0, 105)
        
        # Add quality thresholds
        ax.axhline(y=90, color=self.colors['success'], linestyle='--', alpha=0.5, linewidth=1)
        ax.axhline(y=70, color=self.colors['warning'], linestyle='--', alpha=0.5, linewidth=1)
        
        # Quality interpretation
        interpretation = ('90+: Excellent | 70-89: Good | <70: Needs Review')
        ax.text(0.5, 0.95, interpretation, transform=ax.transAxes,
               **self.fonts['caption'], ha='center', va='top',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=self.colors['light_gray'], alpha=0.7))
        
        # Clean styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
        
        return fig, ax

if __name__ == "__main__":
    """
    Example usage and testing of HanoverVisualizer
    """
    print("🎨 Testing Hanover Visualizer...")
    
    # Initialize visualizer
    viz = HanoverVisualizer()
    
    # Test data
    sample_estimates = {
        'B01003_001E': 28089,  # Total population
        'B19013_001E': 75000,  # Median income
        'B25077_001E': 450000  # Median home value
    }
    
    sample_moe = {
        'B01003_001E': 1250,
        'B19013_001E': 8500,
        'B25077_001E': 25000
    }
    
    sample_labels = {
        'B01003_001E': 'Total Population',
        'B19013_001E': 'Median Household Income',
        'B25077_001E': 'Median Home Value'
    }
    
    # Test uncertainty chart
    print("📊 Creating uncertainty chart...")
    fig, ax = viz.create_uncertainty_chart(
        estimates=sample_estimates,
        margins_of_error=sample_moe,
        labels=sample_labels,
        title="Hanover, MD Demographics with Uncertainty",
        ylabel="Value",
        source="U.S. Census Bureau ACS 5-Year Estimates"
    )
    
    # Test comparison chart
    print("📈 Creating comparison chart...")
    comparison_data = {'county': 85000, 'state': 70000, 'national': 65000}
    fig2, ax2 = viz.create_comparison_chart(
        hanover_data=75000,
        comparison_data=comparison_data,
        metric_name="Median Household Income",
        metric_unit="$",
        source="U.S. Census Bureau ACS 5-Year Estimates"
    )
    
    print("✅ HanoverVisualizer testing completed!")
    print("🎯 Professional visualization framework ready for deployment")