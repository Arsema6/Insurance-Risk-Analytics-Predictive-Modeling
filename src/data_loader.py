"""
Data loading utilities for insurance analytics.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


def load_insurance_data(
    filepath: str,
    sample_size: Optional[int] = None,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Load insurance data from text file.
    
    Parameters
    ----------
    filepath : str
        Path to the data file
    sample_size : int, optional
        If specified, returns a random sample of this size
    random_state : int
        Random state for reproducibility
        
    Returns
    -------
    pd.DataFrame
        Loaded data
    """
    df = pd.read_csv(filepath, sep='\t')
    
    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=random_state)
    
    return df


def infer_column_types(df: pd.DataFrame) -> dict:
    """
    Infer and return column data types.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
        
    Returns
    -------
    dict
        Dictionary mapping column names to inferred types
    """
    type_mapping = {}
    
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if it's a date
            try:
                pd.to_datetime(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.8:
                    type_mapping[col] = 'datetime'
                else:
                    type_mapping[col] = 'categorical'
            except:
                type_mapping[col] = 'categorical'
        elif np.issubdtype(df[col].dtype, np.number):
            type_mapping[col] = 'numerical'
        else:
            type_mapping[col] = df[col].dtype.name
    
    return type_mapping


def validate_data(df: pd.DataFrame) -> dict:
    """
    Validate data quality.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
        
    Returns
    -------
    dict
        Validation report
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'duplicate_rows': df.duplicated().sum(),
        'missing_values': df.isnull().sum().to_dict(),
        'column_dtypes': df.dtypes.to_dict()
    }
    
    return report
