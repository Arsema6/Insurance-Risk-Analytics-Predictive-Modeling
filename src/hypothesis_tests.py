"""
Statistical Hypothesis Testing Module

Provides reusable functions for performing A/B hypothesis tests
on insurance data, including chi-squared tests, t-tests, and z-tests.
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Dict, Any


def chi_squared_test(
    contingency_table: pd.DataFrame,
    feature_name: str = "Feature"
) -> Dict[str, Any]:
    """
    Perform chi-squared test for independence.
    
    Args:
        contingency_table: Contingency table (pd.DataFrame or pd.crosstab result)
        feature_name: Name of the feature being tested
        
    Returns:
        Dictionary with chi2, p_value, dof, and decision
    """
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    decision = "Reject H₀" if p_value < 0.05 else "Fail to reject H₀"
    
    return {
        "test": "Chi-Squared",
        "feature": feature_name,
        "chi2_statistic": chi2,
        "p_value": p_value,
        "dof": dof,
        "decision": decision,
        "significant": p_value < 0.05
    }


def t_test_independent(
    group_a: pd.Series,
    group_b: pd.Series,
    feature_name: str = "Feature"
) -> Dict[str, Any]:
    """
    Perform independent samples t-test.
    
    Args:
        group_a: First group data (Series)
        group_b: Second group data (Series)
        feature_name: Name of the feature being tested
        
    Returns:
        Dictionary with t-statistic, p_value, and decision
    """
    # Remove NaN values
    group_a_clean = group_a.dropna()
    group_b_clean = group_b.dropna()
    
    # Perform t-test
    t_stat, p_value = stats.ttest_ind(group_a_clean, group_b_clean)
    
    # Calculate effect size (Cohen's d)
    pooled_std = np.sqrt(((len(group_a_clean) - 1) * group_a_clean.std() ** 2 +
                          (len(group_b_clean) - 1) * group_b_clean.std() ** 2) /
                         (len(group_a_clean) + len(group_b_clean) - 2))
    cohens_d = (group_a_clean.mean() - group_b_clean.mean()) / pooled_std
    
    decision = "Reject H₀" if p_value < 0.05 else "Fail to reject H₀"
    
    return {
        "test": "Independent t-test",
        "feature": feature_name,
        "t_statistic": t_stat,
        "p_value": p_value,
        "cohens_d": cohens_d,
        "group_a_mean": group_a_clean.mean(),
        "group_b_mean": group_b_clean.mean(),
        "group_a_std": group_a_clean.std(),
        "group_b_std": group_b_clean.std(),
        "decision": decision,
        "significant": p_value < 0.05
    }


def z_test_proportion(
    successes_a: int,
    n_a: int,
    successes_b: int,
    n_b: int,
    feature_name: str = "Feature"
) -> Dict[str, Any]:
    """
    Perform two-proportion z-test for claim frequency.
    
    Args:
        successes_a: Number of successes (claims) in group A
        n_a: Total observations in group A
        successes_b: Number of successes (claims) in group B
        n_b: Total observations in group B
        feature_name: Name of the feature being tested
        
    Returns:
        Dictionary with z-statistic, p_value, and decision
    """
    p_a = successes_a / n_a
    p_b = successes_b / n_b
    p_pooled = (successes_a + successes_b) / (n_a + n_b)
    
    # Calculate standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))
    
    # Calculate z-statistic
    z_stat = (p_a - p_b) / se if se > 0 else 0
    
    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    decision = "Reject H₀" if p_value < 0.05 else "Fail to reject H₀"
    
    return {
        "test": "Two-proportion z-test",
        "feature": feature_name,
        "z_statistic": z_stat,
        "p_value": p_value,
        "proportion_a": p_a,
        "proportion_b": p_b,
        "decision": decision,
        "significant": p_value < 0.05
    }


def test_claim_frequency_hypothesis(
    df: pd.DataFrame,
    group_col: str,
    group_a_value: Any,
    group_b_value: Any
) -> Dict[str, Any]:
    """
    Test hypothesis about claim frequency (H₀: No difference in claim frequency).
    
    Args:
        df: DataFrame with claim data
        group_col: Column name for grouping variable
        group_a_value: Value for group A (control)
        group_b_value: Value for group B (test)
        
    Returns:
        Test results dictionary
    """
    # Segment data
    group_a_data = df[df[group_col] == group_a_value]
    group_b_data = df[df[group_col] == group_b_value]
    
    # Calculate claim frequency (any claim > 0)
    claim_a = (group_a_data['TotalClaims'] > 0).sum()
    claim_b = (group_b_data['TotalClaims'] > 0).sum()
    
    # Perform z-test
    result = z_test_proportion(
        claim_a, len(group_a_data),
        claim_b, len(group_b_data),
        f"{group_col}: {group_a_value} vs {group_b_value}"
    )
    
    result['group_a_label'] = str(group_a_value)
    result['group_b_label'] = str(group_b_value)
    result['kpi'] = "Claim Frequency"
    
    return result


def test_claim_severity_hypothesis(
    df: pd.DataFrame,
    group_col: str,
    group_a_value: Any,
    group_b_value: Any
) -> Dict[str, Any]:
    """
    Test hypothesis about claim severity (H₀: No difference in average claim amount).
    
    Args:
        df: DataFrame with claim data
        group_col: Column name for grouping variable
        group_a_value: Value for group A (control)
        group_b_value: Value for group B (test)
        
    Returns:
        Test results dictionary
    """
    # Segment data
    group_a_data = df[df[group_col] == group_a_value]
    group_b_data = df[df[group_col] == group_b_value]
    
    # Filter for policies with claims
    group_a_claims = group_a_data[group_a_data['TotalClaims'] > 0]['TotalClaims']
    group_b_claims = group_b_data[group_b_data['TotalClaims'] > 0]['TotalClaims']
    
    # Perform t-test
    result = t_test_independent(
        group_a_claims,
        group_b_claims,
        f"{group_col}: {group_a_value} vs {group_b_value}"
    )
    
    result['group_a_label'] = str(group_a_value)
    result['group_b_label'] = str(group_b_value)
    result['kpi'] = "Claim Severity"
    
    return result


def test_margin_hypothesis(
    df: pd.DataFrame,
    group_col: str,
    group_a_value: Any,
    group_b_value: Any
) -> Dict[str, Any]:
    """
    Test hypothesis about profit margin (H₀: No difference in margin).
    Margin = TotalPremium - TotalClaims
    
    Args:
        df: DataFrame with premium and claims data
        group_col: Column name for grouping variable
        group_a_value: Value for group A (control)
        group_b_value: Value for group B (test)
        
    Returns:
        Test results dictionary
    """
    # Segment data
    group_a_data = df[df[group_col] == group_a_value].copy()
    group_b_data = df[df[group_col] == group_b_value].copy()
    
    # Calculate margin
    group_a_data['Margin'] = group_a_data['TotalPremium'] - group_a_data['TotalClaims']
    group_b_data['Margin'] = group_b_data['TotalPremium'] - group_b_data['TotalClaims']
    
    # Perform t-test
    result = t_test_independent(
        group_a_data['Margin'],
        group_b_data['Margin'],
        f"{group_col}: {group_a_value} vs {group_b_value}"
    )
    
    result['group_a_label'] = str(group_a_value)
    result['group_b_label'] = str(group_b_value)
    result['kpi'] = "Margin"
    
    return result


def test_loss_ratio_hypothesis(
    df: pd.DataFrame,
    group_col: str,
    group_a_value: Any,
    group_b_value: Any
) -> Dict[str, Any]:
    """
    Test hypothesis about loss ratio (H₀: No difference in loss ratio).
    Loss Ratio = TotalClaims / TotalPremium
    
    Args:
        df: DataFrame with premium and claims data
        group_col: Column name for grouping variable
        group_a_value: Value for group A (control)
        group_b_value: Value for group B (test)
        
    Returns:
        Test results dictionary
    """
    # Segment data
    group_a_data = df[df[group_col] == group_a_value].copy()
    group_b_data = df[df[group_col] == group_b_value].copy()
    
    # Calculate loss ratio
    group_a_data['LossRatio'] = group_a_data['TotalClaims'] / group_a_data['TotalPremium']
    group_b_data['LossRatio'] = group_b_data['TotalClaims'] / group_b_data['TotalPremium']
    
    # Perform t-test
    result = t_test_independent(
        group_a_data['LossRatio'],
        group_b_data['LossRatio'],
        f"{group_col}: {group_a_value} vs {group_b_value}"
    )
    
    result['group_a_label'] = str(group_a_value)
    result['group_b_label'] = str(group_b_value)
    result['kpi'] = "Loss Ratio"
    
    return result


def create_hypothesis_summary(results: list) -> pd.DataFrame:
    """
    Create summary table from hypothesis test results.
    
    Args:
        results: List of result dictionaries from test functions
        
    Returns:
        Summary DataFrame with key columns
    """
    summary_data = []
    
    for result in results:
        summary_data.append({
            'Hypothesis': result['feature'],
            'KPI': result.get('kpi', 'N/A'),
            'Test': result['test'],
            'Group A': result.get('group_a_label', 'Group A'),
            'Group B': result.get('group_b_label', 'Group B'),
            'Statistic': result.get('t_statistic') or result.get('z_statistic') or result.get('chi2_statistic'),
            'p-value': result['p_value'],
            'Decision': result['decision'],
            'Significant': result['significant']
        })
    
    return pd.DataFrame(summary_data)
