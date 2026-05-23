"""
Advanced analysis utilities for insurance analytics.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Optional


def temporal_analysis(
    df: pd.DataFrame,
    date_col: str,
    premium_col: str,
    claims_col: str,
    period: str = 'M'
) -> pd.DataFrame:
    """
    Analyze trends over time.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    date_col : str
        Date column name
    premium_col : str
        Premium column name
    claims_col : str
        Claims column name
    period : str
        Resampling period ('D', 'M', 'Q', 'Y')
        
    Returns
    -------
    pd.DataFrame
        Time series analysis
    """
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    df_copy = df_copy.dropna(subset=[date_col])
    
    temporal = df_copy.set_index(date_col).resample(period).agg({
        premium_col: ['sum', 'count'],
        claims_col: ['sum', 'mean']
    })
    
    # Flatten columns
    temporal.columns = [f'{col[0]}_{col[1]}' for col in temporal.columns]
    temporal['loss_ratio'] = (
        temporal[f'{claims_col}_sum'] / temporal[f'{premium_col}_sum']
    ).round(4)
    
    return temporal


def vehicle_analysis(
    df: pd.DataFrame,
    vehicle_col: str,
    claims_col: str,
    min_records: int = 10
) -> pd.DataFrame:
    """
    Analyze claims by vehicle.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    vehicle_col : str
        Vehicle column name
    claims_col : str
        Claims column name
    min_records : int
        Minimum records for inclusion
        
    Returns
    -------
    pd.DataFrame
        Vehicle analysis
    """
    vehicle_stats = df.groupby(vehicle_col, observed=True).agg({
        claims_col: ['count', 'sum', 'mean', 'median', 'std'],
        'TotalPremium': 'sum' if 'TotalPremium' in df.columns else 'first'
    }).round(2)
    
    # Flatten columns
    vehicle_stats.columns = [f'{col[0]}_{col[1]}' for col in vehicle_stats.columns]
    
    # Filter by minimum records
    if f'{claims_col}_count' in vehicle_stats.columns:
        vehicle_stats = vehicle_stats[
            vehicle_stats[f'{claims_col}_count'] >= min_records
        ]
    
    return vehicle_stats.sort_values(f'{claims_col}_mean', ascending=False)


def geographic_analysis(
    df: pd.DataFrame,
    geo_col: str,
    premium_col: str,
    claims_col: str,
    vehicle_col: Optional[str] = None
) -> pd.DataFrame:
    """
    Analyze patterns by geography.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    geo_col : str
        Geographic column name
    premium_col : str
        Premium column name
    claims_col : str
        Claims column name
    vehicle_col : str, optional
        Vehicle column for additional analysis
        
    Returns
    -------
    pd.DataFrame
        Geographic analysis
    """
    geo_stats = df.groupby(geo_col, observed=True).agg({
        premium_col: ['sum', 'count', 'mean'],
        claims_col: ['sum', 'mean']
    }).round(2)
    
    # Flatten columns
    geo_stats.columns = [f'{col[0]}_{col[1]}' for col in geo_stats.columns]
    
    # Calculate loss ratio
    geo_stats['loss_ratio'] = (
        geo_stats[f'{claims_col}_sum'] / geo_stats[f'{premium_col}_sum']
    ).round(4)
    
    return geo_stats.sort_values('loss_ratio', ascending=False)


def demographic_analysis(
    df: pd.DataFrame,
    demo_col: str,
    premium_col: str,
    claims_col: str
) -> pd.DataFrame:
    """
    Analyze patterns by demographic.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    demo_col : str
        Demographic column name
    premium_col : str
        Premium column name
    claims_col : str
        Claims column name
        
    Returns
    -------
    pd.DataFrame
        Demographic analysis
    """
    demo_stats = df.groupby(demo_col, observed=True).agg({
        premium_col: ['sum', 'count', 'mean'],
        claims_col: ['sum', 'mean']
    }).round(2)
    
    # Flatten columns
    demo_stats.columns = [f'{col[0]}_{col[1]}' for col in demo_stats.columns]
    
    # Calculate loss ratio
    demo_stats['loss_ratio'] = (
        demo_stats[f'{claims_col}_sum'] / demo_stats[f'{premium_col}_sum']
    ).round(4)
    
    return demo_stats.sort_values('loss_ratio', ascending=False)


def identify_high_risk_profiles(
    df: pd.DataFrame,
    loss_ratio_threshold: float = 0.75,
    premium_col: str = 'TotalPremium',
    claims_col: str = 'TotalClaims'
) -> Dict[str, pd.DataFrame]:
    """
    Identify high-risk profiles.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    loss_ratio_threshold : float
        Threshold for high risk
    premium_col : str
        Premium column name
    claims_col : str
        Claims column name
        
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary of high-risk profiles by dimension
    """
    high_risk = {}
    
    # By Vehicle Type if exists
    if 'VehicleType' in df.columns:
        vehicle_analysis_result = df.groupby('VehicleType', observed=True).agg({
            claims_col: 'sum',
            premium_col: 'sum',
            'VehicleType': 'count'
        }).rename(columns={'VehicleType': 'count'})
        vehicle_analysis_result['loss_ratio'] = (
            vehicle_analysis_result[claims_col] / 
            vehicle_analysis_result[premium_col]
        )
        high_risk['by_vehicle_type'] = vehicle_analysis_result[
            vehicle_analysis_result['loss_ratio'] >= loss_ratio_threshold
        ]
    
    # By Province if exists
    if 'Province' in df.columns:
        province_analysis = df.groupby('Province', observed=True).agg({
            claims_col: 'sum',
            premium_col: 'sum',
            'Province': 'count'
        }).rename(columns={'Province': 'count'})
        province_analysis['loss_ratio'] = (
            province_analysis[claims_col] / 
            province_analysis[premium_col]
        )
        high_risk['by_province'] = province_analysis[
            province_analysis['loss_ratio'] >= loss_ratio_threshold
        ]
    
    return high_risk


def create_summary_statistics(
    df: pd.DataFrame,
    numerical_cols: List[str],
    categorical_cols: List[str]
) -> Dict:
    """
    Create comprehensive summary statistics.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    numerical_cols : List[str]
        Numerical column names
    categorical_cols : List[str]
        Categorical column names
        
    Returns
    -------
    Dict
        Summary statistics dictionary
    """
    summary = {
        'dataset_shape': df.shape,
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'numerical_summary': df[numerical_cols].describe().T.to_dict(),
        'categorical_unique_counts': {col: df[col].nunique() for col in categorical_cols},
        'missing_values': df.isnull().sum().to_dict()
    }
    
    return summary
