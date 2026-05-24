"""
EDA utility functions for insurance analytics.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional


def get_descriptive_statistics(df: pd.DataFrame, numerical_cols: List[str]) -> pd.DataFrame:
    """
    Calculate descriptive statistics for numerical columns.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    numerical_cols : List[str]
        List of numerical column names
        
    Returns
    -------
    pd.DataFrame
        Descriptive statistics
    """
    stats = df[numerical_cols].describe().T
    stats['variance'] = df[numerical_cols].var()
    stats['skewness'] = df[numerical_cols].skew()
    stats['kurtosis'] = df[numerical_cols].kurtosis()
    
    return stats


def calculate_loss_ratio(df: pd.DataFrame, premium_col: str, claims_col: str) -> float:
    """
    Calculate overall loss ratio.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    premium_col : str
        Column name for premiums
    claims_col : str
        Column name for claims
        
    Returns
    -------
    float
        Loss ratio (total claims / total premium)
    """
    total_claims = df[claims_col].sum()
    total_premium = df[premium_col].sum()
    
    if total_premium == 0:
        return 0
    
    return total_claims / total_premium


def segment_analysis(
    df: pd.DataFrame,
    group_col: str,
    premium_col: str,
    claims_col: str
) -> pd.DataFrame:
    """
    Calculate loss ratio by segment.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    group_col : str
        Column to group by
    premium_col : str
        Column name for premiums
    claims_col : str
        Column name for claims
        
    Returns
    -------
    pd.DataFrame
        Segmented analysis with loss ratios
    """
    grouped = df.groupby(group_col, observed=True).agg({
        premium_col: ['sum', 'count', 'mean'],
        claims_col: ['sum', 'mean']
    }).round(2)
    
    # Flatten column names
    grouped.columns = [f'{col[0]}_{col[1]}' for col in grouped.columns]
    
    # Calculate loss ratio
    grouped['loss_ratio'] = (
        grouped[f'{claims_col}_sum'] / grouped[f'{premium_col}_sum']
    ).round(4)
    
    return grouped.sort_values('loss_ratio', ascending=False)


def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> Tuple[pd.Series, dict]:
    """
    Detect outliers using IQR method.
    
    Parameters
    ----------
    series : pd.Series
        Input series
    multiplier : float
        IQR multiplier (default 1.5 for standard outliers)
        
    Returns
    -------
    Tuple[pd.Series, dict]
        Boolean series indicating outliers and outlier stats
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    outliers = (series < lower_bound) | (series > upper_bound)
    
    stats = {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'n_outliers': outliers.sum(),
        'pct_outliers': (outliers.sum() / len(series) * 100).round(2)
    }
    
    return outliers, stats


def calculate_correlation(df: pd.DataFrame, numerical_cols: List[str]) -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical columns.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    numerical_cols : List[str]
        List of numerical column names
        
    Returns
    -------
    pd.DataFrame
        Correlation matrix
    """
    return df[numerical_cols].corr().round(4)


def missing_value_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing values in dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
        
    Returns
    -------
    pd.DataFrame
        Missing value report
    """
    missing_data = pd.DataFrame({
        'column': df.columns,
        'missing_count': df.isnull().sum().values,
        'missing_pct': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    
    return missing_data[missing_data['missing_count'] > 0].sort_values(
        'missing_count', ascending=False
    )
