"""
Statistical Modeling Module for Risk-Based Pricing

Provides models for claim severity prediction, claim probability classification,
and risk-based premium optimization using Linear Regression, Random Forest, and XGBoost.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb
from typing import Tuple, Dict, Any


class ClaimSeverityModel:
    """Build and evaluate predictive models for claim severity (amount)."""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def prepare_data(self, df: pd.DataFrame, test_size=0.2):
        """
        Prepare data for modeling - claims only, feature engineering.
        
        Args:
            df: Input dataframe with all features
            test_size: Proportion for test set
        """
        # Filter for claims only
        df_claims = df[df['TotalClaims'] > 0].copy()
        
        # Feature engineering
        df_claims['VehicleAge'] = 2024 - df_claims.get('RegistrationYear', 2010).astype(float)
        
        # Select features for modeling
        feature_cols = [
            'TotalPremium', 'SumInsured', 'CustomValueEstimate',
            'VehicleAge', 'Cylinders', 'Cubiccapacity'
        ]
        
        # Add categorical features (encoded)
        categorical_cols = ['Province', 'VehicleType', 'Gender']
        
        # Prepare dataframe
        X = df_claims[feature_cols + categorical_cols].copy()
        y = df_claims['TotalClaims'].copy()
        
        # Encode categorical variables
        le_dict = {}
        for col in categorical_cols:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                le_dict[col] = le
        
        # Handle missing values
        X = X.fillna(X.mean(numeric_only=True))
        
        # Remove outliers (IQR method on target)
        Q1 = y.quantile(0.25)
        Q3 = y.quantile(0.75)
        IQR = Q3 - Q1
        mask = (y >= Q1 - 1.5*IQR) & (y <= Q3 + 1.5*IQR)
        X = X[mask]
        y = y[mask]
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        
        # Scale features
        self.X_train = pd.DataFrame(
            self.scaler.fit_transform(self.X_train),
            columns=self.X_train.columns
        )
        self.X_test = pd.DataFrame(
            self.scaler.transform(self.X_test),
            columns=self.X_test.columns
        )
        
        return self.X_train, self.y_train, self.X_test, self.y_test
    
    def train_linear_regression(self):
        """Train linear regression model."""
        model = LinearRegression()
        model.fit(self.X_train, self.y_train)
        self.models['Linear Regression'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        
        self.results['Linear Regression'] = {
            'model': model,
            'y_pred': y_pred,
            'RMSE': rmse,
            'R2': r2
        }
        
        return model, rmse, r2
    
    def train_random_forest(self, n_estimators=100):
        """Train Random Forest regression model."""
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=15,
            random_state=self.random_state,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        
        self.results['Random Forest'] = {
            'model': model,
            'y_pred': y_pred,
            'RMSE': rmse,
            'R2': r2,
            'feature_importance': model.feature_importances_
        }
        
        return model, rmse, r2
    
    def train_xgboost(self, n_estimators=100):
        """Train XGBoost regression model."""
        model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            max_depth=7,
            learning_rate=0.1,
            random_state=self.random_state,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        
        self.results['XGBoost'] = {
            'model': model,
            'y_pred': y_pred,
            'RMSE': rmse,
            'R2': r2,
            'feature_importance': model.feature_importances_
        }
        
        return model, rmse, r2
    
    def get_results_summary(self) -> pd.DataFrame:
        """Get summary of all model results."""
        summary_data = []
        for model_name, result in self.results.items():
            summary_data.append({
                'Model': model_name,
                'RMSE': result['RMSE'],
                'R2': result['R2']
            })
        return pd.DataFrame(summary_data)


class ClaimProbabilityModel:
    """Build and evaluate models for claim probability (binary classification)."""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def prepare_data(self, df: pd.DataFrame, test_size=0.2):
        """
        Prepare data for binary classification.
        
        Args:
            df: Input dataframe
            test_size: Proportion for test set
        """
        df_prepared = df.copy()
        
        # Create target variable: 1 if claim, 0 otherwise
        y = (df_prepared['TotalClaims'] > 0).astype(int)
        
        # Feature engineering
        df_prepared['VehicleAge'] = 2024 - df_prepared.get('RegistrationYear', 2010).astype(float)
        
        # Select features
        feature_cols = [
            'TotalPremium', 'SumInsured', 'CustomValueEstimate',
            'VehicleAge', 'Cylinders', 'Cubiccapacity'
        ]
        
        categorical_cols = ['Province', 'VehicleType', 'Gender']
        
        # Prepare features
        X = df_prepared[feature_cols + categorical_cols].copy()
        
        # Encode categorical variables
        le_dict = {}
        for col in categorical_cols:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                le_dict[col] = le
        
        # Handle missing values
        X = X.fillna(X.mean(numeric_only=True))
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        
        # Scale features
        self.X_train = pd.DataFrame(
            self.scaler.fit_transform(self.X_train),
            columns=self.X_train.columns
        )
        self.X_test = pd.DataFrame(
            self.scaler.transform(self.X_test),
            columns=self.X_test.columns
        )
        
        return self.X_train, self.y_train, self.X_test, self.y_test
    
    def train_logistic_regression(self):
        """Train logistic regression model."""
        model = LogisticRegression(random_state=self.random_state, max_iter=1000)
        model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        y_prob = model.predict_proba(self.X_test)[:, 1]
        
        results_dict = {
            'model': model,
            'y_pred': y_pred,
            'y_prob': y_prob,
            'Accuracy': accuracy_score(self.y_test, y_pred),
            'Precision': precision_score(self.y_test, y_pred),
            'Recall': recall_score(self.y_test, y_pred),
            'F1': f1_score(self.y_test, y_pred)
        }
        self.results['Logistic Regression'] = results_dict
        
        return model, results_dict
    
    def train_random_forest(self, n_estimators=100):
        """Train Random Forest classifier."""
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=15,
            random_state=self.random_state,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        y_prob = model.predict_proba(self.X_test)[:, 1]
        
        results_dict = {
            'model': model,
            'y_pred': y_pred,
            'y_prob': y_prob,
            'Accuracy': accuracy_score(self.y_test, y_pred),
            'Precision': precision_score(self.y_test, y_pred),
            'Recall': recall_score(self.y_test, y_pred),
            'F1': f1_score(self.y_test, y_pred),
            'feature_importance': model.feature_importances_
        }
        self.results['Random Forest'] = results_dict
        
        return model, results_dict
    
    def train_xgboost(self, n_estimators=100):
        """Train XGBoost classifier."""
        model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=7,
            learning_rate=0.1,
            random_state=self.random_state,
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        
        # Evaluate
        y_pred = model.predict(self.X_test)
        y_prob = model.predict_proba(self.X_test)[:, 1]
        
        results_dict = {
            'model': model,
            'y_pred': y_pred,
            'y_prob': y_prob,
            'Accuracy': accuracy_score(self.y_test, y_pred),
            'Precision': precision_score(self.y_test, y_pred),
            'Recall': recall_score(self.y_test, y_pred),
            'F1': f1_score(self.y_test, y_pred),
            'feature_importance': model.feature_importances_
        }
        self.results['XGBoost'] = results_dict
        
        return model, results_dict
    
    def get_results_summary(self) -> pd.DataFrame:
        """Get summary of all model results."""
        summary_data = []
        for model_name, result in self.results.items():
            summary_data.append({
                'Model': model_name,
                'Accuracy': result['Accuracy'],
                'Precision': result['Precision'],
                'Recall': result['Recall'],
                'F1': result['F1']
            })
        return pd.DataFrame(summary_data)


def calculate_risk_based_premium(
    prob_claim: np.ndarray,
    severity_pred: np.ndarray,
    expense_loading: float = 0.20,
    profit_margin: float = 0.15
) -> np.ndarray:
    """
    Calculate risk-based premium.
    
    Premium = (P(claim) × Predicted Severity) + Expense Loading + Profit Margin
    
    Args:
        prob_claim: Probability of claim (0-1)
        severity_pred: Predicted claim amount
        expense_loading: Expense loading factor
        profit_margin: Desired profit margin
        
    Returns:
        Calculated premiums
    """
    base_premium = prob_claim * severity_pred
    total_premium = base_premium * (1 + expense_loading + profit_margin)
    return total_premium
