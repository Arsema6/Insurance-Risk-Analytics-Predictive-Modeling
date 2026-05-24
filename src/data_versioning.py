"""
Data versioning utilities for creating different versions of the dataset.
This demonstrates DVC's capability to track multiple versions of data.
"""

import os
import pandas as pd
from pathlib import Path


def create_cleaned_version(input_file, output_file):
    """
    Create a cleaned version of the raw data.
    
    Args:
        input_file: Path to the raw data file
        output_file: Path to save the cleaned data
    
    Returns:
        dict: Statistics about the cleaning process
    """
    # Read the raw data
    df = pd.read_csv(input_file, sep='\t', encoding='utf-8', on_bad_lines='skip')
    
    initial_rows = len(df)
    
    # Data cleaning steps
    # 1. Remove duplicates
    df = df.drop_duplicates()
    after_dedup = len(df)
    
    # 2. Handle missing values (fill with forward fill then backward fill)
    df = df.ffill().bfill()
    after_fillna = len(df[df.isnull().any(axis=1)])
    
    # 3. Save cleaned version
    df.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
    
    stats = {
        'initial_rows': initial_rows,
        'after_deduplication': after_dedup,
        'duplicates_removed': initial_rows - after_dedup,
        'rows_with_missing_after_fill': after_fillna,
        'final_rows': len(df)
    }
    
    return stats


def create_data_versions():
    """Create raw and cleaned versions of the data for versioning."""
    base_dir = Path(__file__).parent.parent
    raw_file = base_dir / 'data' / 'MachineLearningRating_v3.txt'
    cleaned_file = base_dir / 'data' / 'MachineLearningRating_cleaned_v1.txt'
    
    if raw_file.exists():
        print(f"Creating cleaned version from {raw_file}")
        stats = create_cleaned_version(str(raw_file), str(cleaned_file))
        print(f"Cleaning stats: {stats}")
        return True
    else:
        print(f"Raw data file not found: {raw_file}")
        return False


if __name__ == '__main__':
    create_data_versions()
