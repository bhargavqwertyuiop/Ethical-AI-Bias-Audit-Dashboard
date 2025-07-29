"""
Core bias detection engine for the Ethical AI Bias Audit Dashboard.
Implements multiple fairness metrics and bias detection algorithms.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class BiasDetector:
    """
    Core class for detecting various types of bias in datasets and model predictions.
    """
    
    def __init__(self):
        self.protected_attributes = []
        self.fairness_metrics = {}
        self.bias_report = {}
        
    def detect_dataset_bias(self, data: pd.DataFrame, 
                          protected_attributes: List[str],
                          target_column: str = None) -> Dict[str, Any]:
        """
        Detect bias in a dataset across protected attributes.
        
        Args:
            data: Input dataset
            protected_attributes: List of protected attribute column names
            target_column: Target variable column name (optional)
            
        Returns:
            Dictionary containing bias detection results
        """
        self.protected_attributes = protected_attributes
        bias_results = {}
        
        # Statistical parity analysis
        bias_results['statistical_parity'] = self._calculate_statistical_parity(
            data, protected_attributes, target_column
        )
        
        # Demographic parity analysis
        bias_results['demographic_analysis'] = self._analyze_demographics(
            data, protected_attributes
        )
        
        # Correlation analysis
        bias_results['correlation_analysis'] = self._analyze_correlations(
            data, protected_attributes, target_column
        )
        
        # Distribution analysis
        bias_results['distribution_analysis'] = self._analyze_distributions(
            data, protected_attributes
        )
        
        self.bias_report = bias_results
        return bias_results
    
    def detect_model_bias(self, y_true: np.ndarray, y_pred: np.ndarray,
                         protected_attributes: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect bias in model predictions using various fairness metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            protected_attributes: DataFrame with protected attribute values
            
        Returns:
            Dictionary containing model bias metrics
        """
        bias_results = {}
        
        for attr in protected_attributes.columns:
            attr_values = protected_attributes[attr].unique()
            
            # Calculate fairness metrics for each protected attribute
            bias_results[attr] = {}
            
            # Demographic Parity
            bias_results[attr]['demographic_parity'] = self._calculate_demographic_parity(
                y_pred, protected_attributes[attr]
            )
            
            # Equalized Odds
            bias_results[attr]['equalized_odds'] = self._calculate_equalized_odds(
                y_true, y_pred, protected_attributes[attr]
            )
            
            # Equal Opportunity
            bias_results[attr]['equal_opportunity'] = self._calculate_equal_opportunity(
                y_true, y_pred, protected_attributes[attr]
            )
            
            # Calibration
            bias_results[attr]['calibration'] = self._calculate_calibration(
                y_true, y_pred, protected_attributes[attr]
            )
        
        return bias_results
    
    def _calculate_statistical_parity(self, data: pd.DataFrame, 
                                    protected_attributes: List[str],
                                    target_column: str = None) -> Dict[str, Any]:
        """Calculate statistical parity metrics."""
        results = {}
        
        if target_column and target_column in data.columns:
            for attr in protected_attributes:
                if attr in data.columns:
                    # Calculate positive outcome rates by group
                    group_rates = data.groupby(attr)[target_column].mean()
                    
                    # Calculate parity differences
                    max_rate = group_rates.max()
                    min_rate = group_rates.min()
                    parity_difference = max_rate - min_rate
                    
                    results[attr] = {
                        'group_rates': group_rates.to_dict(),
                        'parity_difference': parity_difference,
                        'bias_detected': parity_difference > 0.1  # 10% threshold
                    }
        
        return results
    
    def _analyze_demographics(self, data: pd.DataFrame, 
                            protected_attributes: List[str]) -> Dict[str, Any]:
        """Analyze demographic distributions."""
        results = {}
        
        for attr in protected_attributes:
            if attr in data.columns:
                value_counts = data[attr].value_counts()
                total_count = len(data)
                
                # Calculate representation percentages
                percentages = (value_counts / total_count * 100).round(2)
                
                # Check for underrepresentation (less than 5%)
                underrepresented = percentages[percentages < 5.0]
                
                results[attr] = {
                    'value_counts': value_counts.to_dict(),
                    'percentages': percentages.to_dict(),
                    'underrepresented_groups': underrepresented.to_dict(),
                    'bias_risk': len(underrepresented) > 0
                }
        
        return results
    
    def _analyze_correlations(self, data: pd.DataFrame, 
                            protected_attributes: List[str],
                            target_column: str = None) -> Dict[str, Any]:
        """Analyze correlations between protected attributes and other features."""
        results = {}
        
        # Get numeric columns only
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        for attr in protected_attributes:
            if attr in data.columns:
                attr_encoded = pd.get_dummies(data[attr], prefix=attr)
                correlations = {}
                
                for col in numeric_cols:
                    if col != attr and col in data.columns:
                        # Calculate correlation between encoded protected attribute and feature
                        corr_values = []
                        for encoded_col in attr_encoded.columns:
                            corr = attr_encoded[encoded_col].corr(data[col])
                            if not np.isnan(corr):
                                corr_values.append(abs(corr))
                        
                        if corr_values:
                            max_corr = max(corr_values)
                            correlations[col] = max_corr
                
                # Identify high correlations (> 0.3)
                high_correlations = {k: v for k, v in correlations.items() if v > 0.3}
                
                results[attr] = {
                    'correlations': correlations,
                    'high_correlations': high_correlations,
                    'bias_risk': len(high_correlations) > 0
                }
        
        return results
    
    def _analyze_distributions(self, data: pd.DataFrame, 
                             protected_attributes: List[str]) -> Dict[str, Any]:
        """Analyze feature distributions across protected groups."""
        results = {}
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        for attr in protected_attributes:
            if attr in data.columns:
                attr_results = {}
                
                for col in numeric_cols:
                    if col != attr:
                        # Calculate statistics by group
                        group_stats = data.groupby(attr)[col].agg(['mean', 'std', 'median']).round(3)
                        
                        # Calculate coefficient of variation across groups
                        means = group_stats['mean']
                        cv = means.std() / means.mean() if means.mean() != 0 else 0
                        
                        attr_results[col] = {
                            'group_statistics': group_stats.to_dict(),
                            'coefficient_of_variation': cv,
                            'high_variation': cv > 0.2  # 20% threshold
                        }
                
                results[attr] = attr_results
        
        return results
    
    def _calculate_demographic_parity(self, y_pred: np.ndarray, 
                                    protected_attr: pd.Series) -> Dict[str, float]:
        """Calculate demographic parity metric."""
        results = {}
        groups = protected_attr.unique()
        
        for group in groups:
            mask = protected_attr == group
            positive_rate = y_pred[mask].mean()
            results[str(group)] = positive_rate
        
        # Calculate parity difference
        rates = list(results.values())
        parity_diff = max(rates) - min(rates) if rates else 0
        
        return {
            'group_rates': results,
            'parity_difference': parity_diff,
            'bias_detected': parity_diff > 0.1
        }
    
    def _calculate_equalized_odds(self, y_true: np.ndarray, y_pred: np.ndarray,
                                protected_attr: pd.Series) -> Dict[str, Any]:
        """Calculate equalized odds metric."""
        results = {}
        groups = protected_attr.unique()
        
        for group in groups:
            mask = protected_attr == group
            y_true_group = y_true[mask]
            y_pred_group = y_pred[mask]
            
            # True Positive Rate
            tpr = np.sum((y_true_group == 1) & (y_pred_group == 1)) / np.sum(y_true_group == 1) if np.sum(y_true_group == 1) > 0 else 0
            
            # False Positive Rate
            fpr = np.sum((y_true_group == 0) & (y_pred_group == 1)) / np.sum(y_true_group == 0) if np.sum(y_true_group == 0) > 0 else 0
            
            results[str(group)] = {'tpr': tpr, 'fpr': fpr}
        
        return results
    
    def _calculate_equal_opportunity(self, y_true: np.ndarray, y_pred: np.ndarray,
                                   protected_attr: pd.Series) -> Dict[str, float]:
        """Calculate equal opportunity metric (TPR parity)."""
        results = {}
        groups = protected_attr.unique()
        
        for group in groups:
            mask = protected_attr == group
            y_true_group = y_true[mask]
            y_pred_group = y_pred[mask]
            
            # True Positive Rate
            tpr = np.sum((y_true_group == 1) & (y_pred_group == 1)) / np.sum(y_true_group == 1) if np.sum(y_true_group == 1) > 0 else 0
            results[str(group)] = tpr
        
        return results
    
    def _calculate_calibration(self, y_true: np.ndarray, y_pred: np.ndarray,
                             protected_attr: pd.Series) -> Dict[str, float]:
        """Calculate calibration metric."""
        results = {}
        groups = protected_attr.unique()
        
        for group in groups:
            mask = protected_attr == group
            y_true_group = y_true[mask]
            y_pred_group = y_pred[mask]
            
            if len(y_true_group) > 0:
                # For binary predictions, calculate accuracy as a proxy for calibration
                accuracy = np.mean(y_true_group == y_pred_group)
                results[str(group)] = accuracy
            else:
                results[str(group)] = 0.0
        
        return results
    
    def get_bias_summary(self) -> Dict[str, Any]:
        """Get a summary of detected biases."""
        if not self.bias_report:
            return {"error": "No bias analysis performed yet"}
        
        summary = {
            "total_protected_attributes": len(self.protected_attributes),
            "bias_detected": False,
            "high_risk_attributes": [],
            "recommendations": []
        }
        
        # Check for bias indicators
        for section, results in self.bias_report.items():
            if section == 'statistical_parity':
                for attr, metrics in results.items():
                    if metrics.get('bias_detected', False):
                        summary["bias_detected"] = True
                        summary["high_risk_attributes"].append(attr)
            
            elif section == 'demographic_analysis':
                for attr, metrics in results.items():
                    if metrics.get('bias_risk', False):
                        summary["bias_detected"] = True
                        if attr not in summary["high_risk_attributes"]:
                            summary["high_risk_attributes"].append(attr)
        
        # Generate basic recommendations
        if summary["bias_detected"]:
            summary["recommendations"] = [
                "Consider data augmentation for underrepresented groups",
                "Apply fairness-aware machine learning techniques",
                "Review data collection processes for potential bias sources",
                "Implement bias mitigation strategies during model training"
            ]
        
        return summary