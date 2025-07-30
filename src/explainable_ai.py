"""
Explainable AI module for the Ethical AI Bias Audit Dashboard.
Provides explanations for bias detection and model predictions using SHAP and LIME.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
import warnings
warnings.filterwarnings('ignore')

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

try:
    import lime
    from lime.lime_tabular import LimeTabularExplainer
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class ExplainableAI:
    """
    Class for generating explanations using SHAP and LIME for bias analysis.
    """
    
    def __init__(self):
        self.shap_explainer = None
        self.lime_explainer = None
        self.feature_names = None
        self.model = None
        
    def setup_explainers(self, X_train: pd.DataFrame, 
                        model: Any = None,
                        explainer_type: str = 'auto') -> Dict[str, bool]:
        """
        Set up SHAP and LIME explainers for the given dataset and model.
        
        Args:
            X_train: Training data for setting up explainers
            model: Trained model (optional, will train a default RF if not provided)
            explainer_type: Type of explainer ('shap', 'lime', 'auto')
            
        Returns:
            Dictionary indicating which explainers were successfully set up
        """
        setup_status = {'shap': False, 'lime': False}
        self.feature_names = X_train.columns.tolist()
        
        # Set up or train model
        if model is None:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            # We'll train this when we have target data
        else:
            self.model = model
        
        # Set up SHAP explainer
        if (explainer_type in ['shap', 'auto']) and SHAP_AVAILABLE:
            try:
                if hasattr(self.model, 'predict_proba'):
                    # For tree-based models
                    if hasattr(self.model, 'estimators_'):
                        self.shap_explainer = shap.TreeExplainer(self.model)
                    else:
                        # For other models, use KernelExplainer with a sample
                        background = shap.kmeans(X_train, min(100, len(X_train)))
                        self.shap_explainer = shap.KernelExplainer(self.model.predict_proba, background)
                setup_status['shap'] = True
            except Exception as e:
                print(f"SHAP setup failed: {e}")
        
        # Set up LIME explainer
        if (explainer_type in ['lime', 'auto']) and LIME_AVAILABLE:
            try:
                self.lime_explainer = LimeTabularExplainer(
                    X_train.values,
                    feature_names=self.feature_names,
                    class_names=['Class 0', 'Class 1'],
                    mode='classification',
                    discretize_continuous=True
                )
                setup_status['lime'] = True
            except Exception as e:
                print(f"LIME setup failed: {e}")
        
        return setup_status
    
    def explain_bias_predictions(self, X: pd.DataFrame, 
                               y_pred: np.ndarray,
                               protected_attributes: List[str],
                               num_samples: int = 10) -> Dict[str, Any]:
        """
        Generate explanations for bias in model predictions.
        
        Args:
            X: Feature data
            y_pred: Model predictions
            protected_attributes: List of protected attribute names
            num_samples: Number of samples to explain
            
        Returns:
            Dictionary containing explanation results
        """
        explanations = {
            'feature_importance': {},
            'bias_explanations': {},
            'sample_explanations': []
        }
        
        # Select samples for explanation
        sample_indices = np.random.choice(len(X), min(num_samples, len(X)), replace=False)
        
        # Generate SHAP explanations if available
        if self.shap_explainer is not None:
            shap_explanations = self._generate_shap_explanations(X, sample_indices)
            explanations['shap_explanations'] = shap_explanations
            
            # Analyze feature importance for bias
            explanations['feature_importance']['shap'] = self._analyze_shap_feature_importance(
                shap_explanations, protected_attributes
            )
        
        # Generate LIME explanations if available
        if self.lime_explainer is not None:
            lime_explanations = self._generate_lime_explanations(X, sample_indices)
            explanations['lime_explanations'] = lime_explanations
            
            # Analyze feature importance for bias
            explanations['feature_importance']['lime'] = self._analyze_lime_feature_importance(
                lime_explanations, protected_attributes
            )
        
        # Generate bias-specific explanations
        explanations['bias_explanations'] = self._generate_bias_explanations(
            X, y_pred, protected_attributes, sample_indices
        )
        
        return explanations
    
    def explain_fairness_violations(self, X: pd.DataFrame,
                                  y_true: np.ndarray,
                                  y_pred: np.ndarray,
                                  protected_attributes: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate explanations for fairness violations.
        
        Args:
            X: Feature data
            y_true: True labels
            y_pred: Predicted labels
            protected_attributes: Protected attribute data
            
        Returns:
            Dictionary containing fairness violation explanations
        """
        explanations = {
            'group_explanations': {},
            'discriminatory_features': {},
            'fairness_insights': []
        }
        
        # Analyze each protected attribute
        for attr in protected_attributes.columns:
            groups = protected_attributes[attr].unique()
            group_explanations = {}
            
            for group in groups:
                # Get samples for this group
                group_mask = protected_attributes[attr] == group
                X_group = X[group_mask]
                
                if len(X_group) > 0:
                    # Generate explanations for this group
                    group_exp = self._explain_group_predictions(X_group, attr, group)
                    group_explanations[str(group)] = group_exp
            
            explanations['group_explanations'][attr] = group_explanations
            
            # Identify discriminatory features
            discriminatory_features = self._identify_discriminatory_features(
                X, y_pred, protected_attributes[attr]
            )
            explanations['discriminatory_features'][attr] = discriminatory_features
        
        # Generate fairness insights
        explanations['fairness_insights'] = self._generate_fairness_insights(
            explanations['discriminatory_features']
        )
        
        return explanations
    
    def get_feature_bias_scores(self, X: pd.DataFrame,
                              protected_attributes: List[str]) -> Dict[str, float]:
        """
        Calculate bias scores for each feature based on correlation with protected attributes.
        
        Args:
            X: Feature data
            protected_attributes: List of protected attribute names
            
        Returns:
            Dictionary of feature bias scores
        """
        bias_scores = {}
        
        for feature in X.columns:
            if feature not in protected_attributes:
                max_bias = 0.0
                
                for protected_attr in protected_attributes:
                    if protected_attr in X.columns:
                        # Calculate correlation-based bias score
                        if X[feature].dtype in ['object', 'category']:
                            # For categorical features, use chi-square based association
                            bias_score = self._calculate_categorical_bias(X[feature], X[protected_attr])
                        else:
                            # For numerical features, use correlation
                            bias_score = abs(X[feature].corr(pd.get_dummies(X[protected_attr]).iloc[:, 0]))
                            if np.isnan(bias_score):
                                bias_score = 0.0
                        
                        max_bias = max(max_bias, bias_score)
                
                bias_scores[feature] = max_bias
        
        return bias_scores
    
    def _generate_shap_explanations(self, X: pd.DataFrame, 
                                  sample_indices: np.ndarray) -> Dict[str, Any]:
        """Generate SHAP explanations for selected samples."""
        if self.shap_explainer is None:
            return {}
        
        try:
            # Get SHAP values for samples
            X_sample = X.iloc[sample_indices]
            shap_values = self.shap_explainer.shap_values(X_sample)
            
            # Handle different SHAP value formats
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Use positive class for binary classification
            
            return {
                'shap_values': shap_values,
                'feature_names': self.feature_names,
                'sample_indices': sample_indices.tolist(),
                'expected_value': getattr(self.shap_explainer, 'expected_value', 0)
            }
        except Exception as e:
            print(f"Error generating SHAP explanations: {e}")
            return {}
    
    def _generate_lime_explanations(self, X: pd.DataFrame,
                                  sample_indices: np.ndarray) -> List[Dict[str, Any]]:
        """Generate LIME explanations for selected samples."""
        if self.lime_explainer is None or self.model is None:
            return []
        
        explanations = []
        
        try:
            for idx in sample_indices:
                # Generate LIME explanation for this sample
                explanation = self.lime_explainer.explain_instance(
                    X.iloc[idx].values,
                    self.model.predict_proba,
                    num_features=min(10, len(X.columns))
                )
                
                # Extract feature importance
                feature_importance = {}
                for feature, importance in explanation.as_list():
                    feature_importance[feature] = importance
                
                explanations.append({
                    'sample_index': int(idx),
                    'feature_importance': feature_importance,
                    'prediction_probability': self.model.predict_proba([X.iloc[idx].values])[0].tolist()
                })
                
        except Exception as e:
            print(f"Error generating LIME explanations: {e}")
        
        return explanations
    
    def _analyze_shap_feature_importance(self, shap_explanations: Dict[str, Any],
                                       protected_attributes: List[str]) -> Dict[str, Any]:
        """Analyze SHAP feature importance for bias indicators."""
        if not shap_explanations or 'shap_values' not in shap_explanations:
            return {}
        
        shap_values = shap_explanations['shap_values']
        feature_names = shap_explanations['feature_names']
        
        # Calculate average absolute SHAP values
        avg_importance = np.mean(np.abs(shap_values), axis=0)
        
        # Create importance dictionary
        importance_dict = dict(zip(feature_names, avg_importance))
        
        # Identify protected attribute importance
        protected_importance = {}
        for attr in protected_attributes:
            if attr in importance_dict:
                protected_importance[attr] = importance_dict[attr]
        
        return {
            'overall_importance': importance_dict,
            'protected_attribute_importance': protected_importance,
            'bias_risk_features': [feat for feat, imp in importance_dict.items() 
                                 if feat in protected_attributes and imp > np.mean(avg_importance)]
        }
    
    def _analyze_lime_feature_importance(self, lime_explanations: List[Dict[str, Any]],
                                       protected_attributes: List[str]) -> Dict[str, Any]:
        """Analyze LIME feature importance for bias indicators."""
        if not lime_explanations:
            return {}
        
        # Aggregate feature importance across samples
        all_importance = {}
        for explanation in lime_explanations:
            for feature, importance in explanation['feature_importance'].items():
                if feature not in all_importance:
                    all_importance[feature] = []
                all_importance[feature].append(abs(importance))
        
        # Calculate average importance
        avg_importance = {feat: np.mean(values) for feat, values in all_importance.items()}
        
        # Identify protected attribute importance
        protected_importance = {}
        for attr in protected_attributes:
            # LIME might use feature descriptions instead of exact names
            for feat, imp in avg_importance.items():
                if attr in feat:
                    protected_importance[attr] = imp
                    break
        
        return {
            'overall_importance': avg_importance,
            'protected_attribute_importance': protected_importance,
            'bias_risk_features': [feat for feat, imp in avg_importance.items() 
                                 if any(attr in feat for attr in protected_attributes)]
        }
    
    def _generate_bias_explanations(self, X: pd.DataFrame,
                                  y_pred: np.ndarray,
                                  protected_attributes: List[str],
                                  sample_indices: np.ndarray) -> Dict[str, Any]:
        """Generate bias-specific explanations."""
        explanations = {
            'protected_attribute_influence': {},
            'potential_proxies': {},
            'bias_patterns': []
        }
        
        # Analyze protected attribute influence
        for attr in protected_attributes:
            if attr in X.columns:
                # Calculate correlation between predictions and protected attribute
                attr_values = X[attr].iloc[sample_indices]
                pred_values = y_pred[sample_indices]
                
                # For categorical attributes, calculate group-wise prediction rates
                if attr_values.dtype in ['object', 'category']:
                    group_rates = {}
                    for group in attr_values.unique():
                        group_mask = attr_values == group
                        if group_mask.sum() > 0:
                            group_rates[str(group)] = pred_values[group_mask].mean()
                    
                    explanations['protected_attribute_influence'][attr] = {
                        'type': 'categorical',
                        'group_prediction_rates': group_rates,
                        'variation': max(group_rates.values()) - min(group_rates.values()) if group_rates else 0
                    }
        
        return explanations
    
    def _explain_group_predictions(self, X_group: pd.DataFrame,
                                 protected_attr: str,
                                 group_value: Any) -> Dict[str, Any]:
        """Generate explanations for a specific group's predictions."""
        if len(X_group) == 0:
            return {}
        
        # Sample a few instances from this group for explanation
        sample_size = min(5, len(X_group))
        sample_indices = np.random.choice(len(X_group), sample_size, replace=False)
        
        group_explanation = {
            'group_size': len(X_group),
            'sample_explanations': [],
            'average_feature_values': X_group.mean().to_dict() if len(X_group) > 0 else {}
        }
        
        # Generate explanations for samples from this group
        if self.lime_explainer is not None and self.model is not None:
            try:
                for idx in sample_indices:
                    explanation = self.lime_explainer.explain_instance(
                        X_group.iloc[idx].values,
                        self.model.predict_proba,
                        num_features=5
                    )
                    
                    group_explanation['sample_explanations'].append({
                        'local_index': int(idx),
                        'explanation': explanation.as_list()
                    })
            except Exception as e:
                print(f"Error explaining group {group_value}: {e}")
        
        return group_explanation
    
    def _identify_discriminatory_features(self, X: pd.DataFrame,
                                        y_pred: np.ndarray,
                                        protected_attr: pd.Series) -> Dict[str, float]:
        """Identify features that may be discriminatory."""
        discriminatory_scores = {}
        
        # Calculate how much each feature differs between protected groups
        groups = protected_attr.unique()
        
        for feature in X.columns:
            if feature != protected_attr.name:
                group_differences = []
                
                for i, group1 in enumerate(groups):
                    for group2 in groups[i+1:]:
                        mask1 = protected_attr == group1
                        mask2 = protected_attr == group2
                        
                        if mask1.sum() > 0 and mask2.sum() > 0:
                            if X[feature].dtype in ['object', 'category']:
                                # For categorical features, use distribution comparison
                                diff = self._calculate_categorical_difference(
                                    X[feature][mask1], X[feature][mask2]
                                )
                            else:
                                # For numerical features, use mean difference
                                diff = abs(X[feature][mask1].mean() - X[feature][mask2].mean())
                                # Normalize by standard deviation
                                std_dev = X[feature].std()
                                if std_dev > 0:
                                    diff = diff / std_dev
                            
                            group_differences.append(diff)
                
                discriminatory_scores[feature] = np.mean(group_differences) if group_differences else 0.0
        
        return discriminatory_scores
    
    def _generate_fairness_insights(self, discriminatory_features: Dict[str, Dict[str, float]]) -> List[str]:
        """Generate actionable fairness insights."""
        insights = []
        
        for attr, feature_scores in discriminatory_features.items():
            # Find top discriminatory features
            sorted_features = sorted(feature_scores.items(), key=lambda x: x[1], reverse=True)
            top_features = sorted_features[:3]
            
            for feature, score in top_features:
                if score > 0.5:  # Threshold for significant discrimination
                    insights.append(
                        f"Feature '{feature}' shows significant variation across {attr} groups (score: {score:.2f}). "
                        f"Consider reviewing this feature for potential bias."
                    )
        
        if not insights:
            insights.append("No significant discriminatory features detected based on current analysis.")
        
        return insights
    
    def _calculate_categorical_bias(self, feature: pd.Series, protected_attr: pd.Series) -> float:
        """Calculate bias score for categorical features."""
        try:
            # Use Cramér's V for categorical association
            confusion_matrix = pd.crosstab(feature, protected_attr)
            chi2 = self._chi_square_test(confusion_matrix)
            n = confusion_matrix.sum().sum()
            cramers_v = np.sqrt(chi2 / (n * (min(confusion_matrix.shape) - 1)))
            return cramers_v
        except:
            return 0.0
    
    def _chi_square_test(self, confusion_matrix: pd.DataFrame) -> float:
        """Calculate chi-square statistic."""
        # Calculate expected frequencies
        row_totals = confusion_matrix.sum(axis=1)
        col_totals = confusion_matrix.sum(axis=0)
        total = confusion_matrix.sum().sum()
        
        expected = np.outer(row_totals, col_totals) / total
        
        # Calculate chi-square statistic
        chi2 = ((confusion_matrix - expected) ** 2 / expected).sum().sum()
        return chi2
    
    def _calculate_categorical_difference(self, series1: pd.Series, series2: pd.Series) -> float:
        """Calculate difference between two categorical distributions."""
        # Get value counts as proportions
        dist1 = series1.value_counts(normalize=True)
        dist2 = series2.value_counts(normalize=True)
        
        # Align indices
        all_values = set(dist1.index) | set(dist2.index)
        dist1 = dist1.reindex(all_values, fill_value=0)
        dist2 = dist2.reindex(all_values, fill_value=0)
        
        # Calculate total variation distance
        return 0.5 * np.sum(np.abs(dist1 - dist2))