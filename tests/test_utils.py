"""
Unit tests for insurance analytics modules.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_loader import infer_column_types, validate_data
from src.eda_utils import (
    get_descriptive_statistics,
    calculate_loss_ratio,
    detect_outliers_iqr,
    missing_value_analysis
)


class TestDataLoader:
    """Test data loading utilities."""
    
    def test_infer_column_types(self):
        """Test column type inference."""
        df = pd.DataFrame({
            'numerical': [1, 2, 3, 4, 5],
            'categorical': ['A', 'B', 'A', 'C', 'B'],
            'dates': pd.date_range('2023-01-01', periods=5)
        })
        
        types = infer_column_types(df)
        assert types['numerical'] == 'numerical'
        assert types['categorical'] == 'categorical'
    
    def test_validate_data(self):
        """Test data validation."""
        df = pd.DataFrame({
            'col1': [1, 2, None, 4, 5],
            'col2': ['A', 'B', 'A', 'B', 'A']
        })
        
        report = validate_data(df)
        assert report['total_rows'] == 5
        assert report['total_columns'] == 2
        assert report['missing_values']['col1'] == 1


class TestEDAUtils:
    """Test EDA utility functions."""
    
    def test_descriptive_statistics(self):
        """Test descriptive statistics calculation."""
        df = pd.DataFrame({
            'premium': [100, 200, 300, 400, 500],
            'claims': [50, 100, 150, 200, 250]
        })
        
        stats = get_descriptive_statistics(df, ['premium', 'claims'])
        assert 'mean' in stats.columns
        assert 'variance' in stats.columns
        assert 'skewness' in stats.columns
    
    def test_calculate_loss_ratio(self):
        """Test loss ratio calculation."""
        df = pd.DataFrame({
            'premium': [100, 200, 300],
            'claims': [50, 100, 150]
        })
        
        ratio = calculate_loss_ratio(df, 'premium', 'claims')
        assert ratio == pytest.approx(0.5)
    
    def test_detect_outliers_iqr(self):
        """Test outlier detection."""
        series = pd.Series([1, 2, 3, 4, 5, 100])  # 100 is outlier
        
        outliers, stats = detect_outliers_iqr(series)
        assert outliers.sum() >= 1
        assert stats['n_outliers'] >= 1
    
    def test_missing_value_analysis(self):
        """Test missing value analysis."""
        df = pd.DataFrame({
            'col1': [1, None, 3, None, 5],
            'col2': [1, 2, 3, 4, 5],
            'col3': [None, None, None, None, None]
        })
        
        missing = missing_value_analysis(df)
        assert len(missing) > 0
        assert 'missing_pct' in missing.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
