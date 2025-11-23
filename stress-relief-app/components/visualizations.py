"""
Visualization components for stress data and charts.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class VisualizationManager:
    """Manages all data visualizations for the stress monitoring app."""
    
    def __init__(self):
        """Initialize the visualization manager."""
        pass
    
    def plot_stress_timeline(self, data: pd.DataFrame, stress_column: str = 'stress_level') -> go.Figure:
        """
        Create a timeline plot of stress levels over time.
        
        Args:
            data: DataFrame with timestamp and stress level data
            stress_column: Name of the column containing stress levels
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['timestamp'] if 'timestamp' in data.columns else data.index,
            y=data[stress_column],
            mode='lines+markers',
            name='Stress Level',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Stress Level Over Time',
            xaxis_title='Time',
            yaxis_title='Stress Level',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    def plot_stress_distribution(self, data: pd.DataFrame, stress_column: str = 'stress_level') -> go.Figure:
        """
        Create a histogram of stress level distribution.
        
        Args:
            data: DataFrame with stress level data
            stress_column: Name of the column containing stress levels
            
        Returns:
            Plotly figure object
        """
        fig = px.histogram(
            data,
            x=stress_column,
            nbins=20,
            title='Stress Level Distribution',
            labels={stress_column: 'Stress Level', 'count': 'Frequency'},
            color_discrete_sequence=['#ff6b6b']
        )
        
        fig.update_layout(template='plotly_white')
        return fig
    
    def plot_stress_heatmap(self, data: pd.DataFrame) -> go.Figure:
        """
        Create a heatmap showing stress patterns by time of day and day of week.
        
        Args:
            data: DataFrame with timestamp and stress level data
            
        Returns:
            Plotly figure object
        """
        # Placeholder - would require datetime processing
        st.info("Heatmap visualization would be implemented here")
        return go.Figure()
    
    def display_stress_gauge(self, current_stress: float, threshold: float = 0.7) -> go.Figure:
        """
        Display a gauge chart showing current stress level.
        
        Args:
            current_stress: Current stress level (0.0 to 1.0)
            threshold: Stress threshold for warning
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_stress * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Stress Level (%)"},
            delta={'reference': threshold * 100},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, threshold * 100], 'color': "lightgray"},
                    {'range': [threshold * 100, 100], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold * 100
                }
            }
        ))
        
        fig.update_layout(
            title="Current Stress Level",
            template='plotly_white'
        )
        
        return fig

