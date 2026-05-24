"""
Visualization utilities for insurance analytics.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional
import pandas as pd
import numpy as np


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def create_distribution_plot(
    data: pd.Series,
    title: str,
    xlabel: str,
    figsize: tuple = (12, 5)
) -> None:
    """
    Create histogram with KDE for numerical column.
    
    Parameters
    ----------
    data : pd.Series
        Input series
    title : str
        Plot title
    xlabel : str
        X-axis label
    figsize : tuple
        Figure size
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    axes[0].hist(data.dropna(), bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].set_title(f'{title} - Histogram')
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel('Frequency')
    axes[0].grid(True, alpha=0.3)
    
    data.dropna().plot(kind='kde', ax=axes[1], color='steelblue', linewidth=2)
    axes[1].set_title(f'{title} - KDE')
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel('Density')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def create_boxplot(
    data: pd.DataFrame,
    columns: List[str],
    title: str,
    figsize: tuple = (14, 6)
) -> None:
    """
    Create boxplot for outlier detection.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe
    columns : List[str]
        Columns to plot
    title : str
        Plot title
    figsize : tuple
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    data[columns].boxplot(ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel('Value')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig


def create_categorical_plot(
    df: pd.DataFrame,
    col: str,
    title: str,
    figsize: tuple = (12, 6)
) -> None:
    """
    Create bar chart for categorical column.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    col : str
        Column name
    title : str
        Plot title
    figsize : tuple
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    value_counts = df[col].value_counts()
    value_counts.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel('Count')
    ax.set_xlabel(col)
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    return fig


def create_heatmap(
    corr_matrix: pd.DataFrame,
    title: str,
    figsize: tuple = (10, 8)
) -> None:
    """
    Create correlation heatmap.
    
    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Correlation matrix
    title : str
        Plot title
    figsize : tuple
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        ax=ax,
        cbar_kws={'label': 'Correlation'}
    )
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    figsize: tuple = (12, 6),
    hue: Optional[str] = None
) -> None:
    """
    Create scatter plot.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    x : str
        X-axis column
    y : str
        Y-axis column
    title : str
        Plot title
    figsize : tuple
        Figure size
    hue : str, optional
        Column for color encoding
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if hue:
        for category in df[hue].unique():
            mask = df[hue] == category
            ax.scatter(
                df[mask][x],
                df[mask][y],
                label=category,
                alpha=0.6,
                s=50
            )
        ax.legend()
    else:
        ax.scatter(df[x], df[y], alpha=0.6, s=50, color='steelblue')
    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig


def create_interactive_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: Optional[str] = None,
    size: Optional[str] = None
) -> go.Figure:
    """
    Create interactive Plotly scatter plot.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    x : str
        X-axis column
    y : str
        Y-axis column
    title : str
        Plot title
    color : str, optional
        Column for color encoding
    size : str, optional
        Column for size encoding
        
    Returns
    -------
    go.Figure
        Plotly figure
    """
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_data=df.columns,
        title=title
    )
    
    fig.update_layout(
        height=600,
        font=dict(size=12),
        hovermode='closest'
    )
    
    return fig


def create_segment_analysis_plot(
    segment_data: pd.DataFrame,
    metric: str,
    title: str,
    figsize: tuple = (12, 6)
) -> None:
    """
    Create bar plot for segmented analysis.
    
    Parameters
    ----------
    segment_data : pd.DataFrame
        Segmented data with index as segment names
    metric : str
        Metric column to plot
    title : str
        Plot title
    figsize : tuple
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    segment_data[metric].plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel(metric)
    ax.set_xlabel('Segment')
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    return fig
