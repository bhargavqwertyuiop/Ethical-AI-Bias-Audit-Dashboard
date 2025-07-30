"""
Bias mitigation recommendation engine for the Ethical AI Bias Audit Dashboard.
Provides specific, actionable suggestions for addressing detected biases.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import json


class MitigationEngine:
    """
    Engine for generating bias mitigation recommendations and code suggestions.
    """
    
    def __init__(self):
        self.mitigation_strategies = self._load_mitigation_strategies()
        self.code_templates = self._load_code_templates()
    
    def generate_recommendations(self, bias_results: Dict[str, Any], 
                               data_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate comprehensive bias mitigation recommendations.
        
        Args:
            bias_results: Results from bias detection analysis
            data_info: Additional information about the dataset
            
        Returns:
            Dictionary containing mitigation recommendations
        """
        recommendations = {
            'immediate_actions': [],
            'data_strategies': [],
            'modeling_strategies': [],
            'code_suggestions': [],
            'monitoring_strategies': [],
            'priority_level': 'low'
        }
        
        # Analyze bias severity and generate appropriate recommendations
        severity_score = self._calculate_bias_severity(bias_results)
        recommendations['priority_level'] = self._get_priority_level(severity_score)
        
        # Generate immediate action recommendations
        recommendations['immediate_actions'] = self._generate_immediate_actions(bias_results)
        
        # Generate data-level strategies
        recommendations['data_strategies'] = self._generate_data_strategies(bias_results)
        
        # Generate modeling strategies
        recommendations['modeling_strategies'] = self._generate_modeling_strategies(bias_results)
        
        # Generate code suggestions
        recommendations['code_suggestions'] = self._generate_code_suggestions(bias_results)
        
        # Generate monitoring strategies
        recommendations['monitoring_strategies'] = self._generate_monitoring_strategies(bias_results)
        
        return recommendations
    
    def get_data_augmentation_strategies(self, bias_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get specific data augmentation strategies for addressing bias.
        
        Args:
            bias_results: Results from bias detection analysis
            
        Returns:
            List of data augmentation strategies with implementation details
        """
        strategies = []
        
        # Check for demographic imbalances
        if 'demographic_analysis' in bias_results:
            for attr, analysis in bias_results['demographic_analysis'].items():
                if analysis.get('bias_risk', False):
                    underrepresented = analysis.get('underrepresented_groups', {})
                    
                    for group, percentage in underrepresented.items():
                        strategy = {
                            'strategy': 'Synthetic Data Generation',
                            'target_attribute': attr,
                            'target_group': group,
                            'current_representation': f"{percentage}%",
                            'recommended_target': "At least 10% representation",
                            'methods': [
                                'SMOTE (Synthetic Minority Oversampling Technique)',
                                'CTGAN (Conditional Tabular GAN)',
                                'Data collection campaigns targeting underrepresented groups'
                            ],
                            'implementation': self._get_smote_implementation(attr, group)
                        }
                        strategies.append(strategy)
        
        return strategies
    
    def get_fairness_constraints(self, bias_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get fairness constraints that can be applied during model training.
        
        Args:
            bias_results: Results from bias detection analysis
            
        Returns:
            List of fairness constraints with implementation details
        """
        constraints = []
        
        # Demographic Parity Constraints
        if self._has_demographic_parity_issues(bias_results):
            constraint = {
                'type': 'Demographic Parity',
                'description': 'Ensure equal positive prediction rates across groups',
                'implementation': self._get_demographic_parity_constraint_code(),
                'fairlearn_method': 'DemographicParity()',
                'use_case': 'When equal treatment is the primary goal'
            }
            constraints.append(constraint)
        
        # Equalized Odds Constraints
        if self._has_equalized_odds_issues(bias_results):
            constraint = {
                'type': 'Equalized Odds',
                'description': 'Ensure equal TPR and FPR across groups',
                'implementation': self._get_equalized_odds_constraint_code(),
                'fairlearn_method': 'EqualizedOdds()',
                'use_case': 'When prediction accuracy should be consistent across groups'
            }
            constraints.append(constraint)
        
        # Equal Opportunity Constraints
        if self._has_equal_opportunity_issues(bias_results):
            constraint = {
                'type': 'Equal Opportunity',
                'description': 'Ensure equal True Positive Rates across groups',
                'implementation': self._get_equal_opportunity_constraint_code(),
                'fairlearn_method': 'TruePositiveRateParity()',
                'use_case': 'When it\'s important that qualified individuals have equal opportunity'
            }
            constraints.append(constraint)
        
        return constraints
    
    def get_preprocessing_strategies(self, bias_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get preprocessing strategies to mitigate bias before model training.
        
        Args:
            bias_results: Results from bias detection analysis
            
        Returns:
            List of preprocessing strategies
        """
        strategies = []
        
        # Feature selection based on correlation analysis
        if 'correlation_analysis' in bias_results:
            for attr, analysis in bias_results['correlation_analysis'].items():
                high_corr_features = analysis.get('high_correlations', {})
                
                if high_corr_features:
                    strategy = {
                        'strategy': 'Feature Selection/Engineering',
                        'target_attribute': attr,
                        'description': f'Remove or transform features highly correlated with {attr}',
                        'affected_features': list(high_corr_features.keys()),
                        'methods': [
                            'Remove proxy features',
                            'Apply feature transformation',
                            'Use fairness-aware feature selection'
                        ],
                        'implementation': self._get_feature_selection_code(high_corr_features)
                    }
                    strategies.append(strategy)
        
        # Data balancing strategies
        strategies.extend(self._get_balancing_strategies(bias_results))
        
        return strategies
    
    def _calculate_bias_severity(self, bias_results: Dict[str, Any]) -> float:
        """Calculate overall bias severity score."""
        severity_score = 0.0
        total_checks = 0
        
        # Statistical parity severity
        if 'statistical_parity' in bias_results:
            for attr, metrics in bias_results['statistical_parity'].items():
                if metrics.get('bias_detected', False):
                    parity_diff = metrics.get('parity_difference', 0)
                    severity_score += min(parity_diff * 10, 1.0)  # Cap at 1.0
                total_checks += 1
        
        # Demographic analysis severity
        if 'demographic_analysis' in bias_results:
            for attr, metrics in bias_results['demographic_analysis'].items():
                if metrics.get('bias_risk', False):
                    underrep_count = len(metrics.get('underrepresented_groups', {}))
                    severity_score += min(underrep_count * 0.2, 1.0)
                total_checks += 1
        
        return severity_score / max(total_checks, 1)
    
    def _get_priority_level(self, severity_score: float) -> str:
        """Determine priority level based on severity score."""
        if severity_score >= 0.7:
            return 'critical'
        elif severity_score >= 0.4:
            return 'high'
        elif severity_score >= 0.2:
            return 'medium'
        else:
            return 'low'
    
    def _generate_immediate_actions(self, bias_results: Dict[str, Any]) -> List[str]:
        """Generate immediate action recommendations."""
        actions = []
        
        # Check for critical biases
        if 'statistical_parity' in bias_results:
            for attr, metrics in bias_results['statistical_parity'].items():
                if metrics.get('bias_detected', False):
                    parity_diff = metrics.get('parity_difference', 0)
                    if parity_diff > 0.2:  # 20% difference is critical
                        actions.append(f"URGENT: Address {parity_diff:.1%} outcome disparity in {attr}")
        
        # Check for severe underrepresentation
        if 'demographic_analysis' in bias_results:
            for attr, analysis in bias_results['demographic_analysis'].items():
                underrep = analysis.get('underrepresented_groups', {})
                for group, percentage in underrep.items():
                    if percentage < 2.0:  # Less than 2% representation
                        actions.append(f"CRITICAL: {group} represents only {percentage:.1f}% of data in {attr}")
        
        return actions
    
    def _generate_data_strategies(self, bias_results: Dict[str, Any]) -> List[str]:
        """Generate data-level mitigation strategies."""
        strategies = [
            "Implement stratified sampling to ensure representative data collection",
            "Conduct bias audits of data collection processes",
            "Use synthetic data generation (SMOTE, CTGAN) for underrepresented groups",
            "Apply data augmentation techniques specific to minority groups",
            "Review and update data collection protocols to reduce selection bias"
        ]
        
        return strategies
    
    def _generate_modeling_strategies(self, bias_results: Dict[str, Any]) -> List[str]:
        """Generate modeling-level mitigation strategies."""
        strategies = [
            "Apply fairness constraints during model training (Fairlearn)",
            "Use adversarial debiasing techniques",
            "Implement post-processing fairness adjustments",
            "Apply re-weighting strategies to balance group representations",
            "Use ensemble methods with fairness-aware base learners"
        ]
        
        return strategies
    
    def _generate_code_suggestions(self, bias_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate specific code suggestions for bias mitigation."""
        suggestions = []
        
        # Always include basic fairness evaluation code
        suggestions.append({
            'title': 'Fairness Metrics Evaluation',
            'description': 'Add comprehensive fairness metrics to your model evaluation',
            'code': self.code_templates['fairness_evaluation']
        })
        
        # Add SMOTE if underrepresentation detected
        if self._has_underrepresentation(bias_results):
            suggestions.append({
                'title': 'SMOTE Data Balancing',
                'description': 'Use SMOTE to balance underrepresented groups',
                'code': self.code_templates['smote_balancing']
            })
        
        # Add fairness constraints if bias detected
        if self._has_statistical_parity_issues(bias_results):
            suggestions.append({
                'title': 'Fairlearn Constraints',
                'description': 'Apply fairness constraints during training',
                'code': self.code_templates['fairlearn_constraints']
            })
        
        return suggestions
    
    def _generate_monitoring_strategies(self, bias_results: Dict[str, Any]) -> List[str]:
        """Generate ongoing monitoring strategies."""
        strategies = [
            "Implement continuous bias monitoring in production",
            "Set up automated alerts for fairness metric violations",
            "Establish regular bias audit schedules (monthly/quarterly)",
            "Create bias reporting dashboards for stakeholders",
            "Implement A/B testing with fairness metrics"
        ]
        
        return strategies
    
    def _load_mitigation_strategies(self) -> Dict[str, Any]:
        """Load predefined mitigation strategies."""
        return {
            'data_level': [
                'Data augmentation for minority groups',
                'Synthetic data generation using GANs',
                'Stratified sampling strategies',
                'Bias-aware data collection protocols'
            ],
            'preprocessing': [
                'Feature selection to remove proxy variables',
                'Data reweighting and resampling',
                'Fairness-aware feature engineering',
                'Adversarial preprocessing'
            ],
            'model_level': [
                'Fairness constraints in optimization',
                'Multi-task learning with fairness objectives',
                'Adversarial debiasing',
                'Ensemble methods with fairness considerations'
            ],
            'postprocessing': [
                'Threshold optimization for fairness',
                'Calibration adjustments across groups',
                'Output redistribution methods',
                'Fairness-aware ranking'
            ]
        }
    
    def _load_code_templates(self) -> Dict[str, str]:
        """Load code templates for common mitigation strategies."""
        return {
            'fairness_evaluation': '''
# Comprehensive Fairness Evaluation
from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference

def evaluate_fairness(y_true, y_pred, sensitive_features):
    """Evaluate multiple fairness metrics."""
    
    # Create metric frame
    metric_frame = MetricFrame(
        metrics={
            'accuracy': accuracy_score,
            'precision': precision_score,
            'recall': recall_score,
            'f1': f1_score
        },
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    
    # Calculate fairness metrics
    dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_features)
    eo_diff = equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive_features)
    
    print(f"Demographic Parity Difference: {dp_diff:.3f}")
    print(f"Equalized Odds Difference: {eo_diff:.3f}")
    print("\\nMetrics by Group:")
    print(metric_frame.by_group)
    
    return metric_frame, dp_diff, eo_diff
''',
            
            'smote_balancing': '''
# SMOTE Data Balancing for Protected Attributes
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder

def balance_data_with_smote(X, y, protected_attr, random_state=42):
    """Apply SMOTE to balance data considering protected attributes."""
    
    # Combine target and protected attribute for stratified SMOTE
    le = LabelEncoder()
    combined_target = le.fit_transform(
        y.astype(str) + "_" + protected_attr.astype(str)
    )
    
    # Apply SMOTE
    smote = SMOTE(random_state=random_state, k_neighbors=3)
    X_balanced, combined_balanced = smote.fit_resample(X, combined_target)
    
    # Separate target and protected attribute
    combined_labels = le.inverse_transform(combined_balanced)
    y_balanced = np.array([label.split('_')[0] for label in combined_labels])
    protected_balanced = np.array([label.split('_')[1] for label in combined_labels])
    
    return X_balanced, y_balanced, protected_balanced
''',
            
            'fairlearn_constraints': '''
# Fairlearn Fairness Constraints
from fairlearn.reductions import ExponentiatedGradient, DemographicParity, EqualizedOdds
from sklearn.ensemble import RandomForestClassifier

def train_fair_model(X_train, y_train, sensitive_features_train, constraint_type='demographic_parity'):
    """Train a model with fairness constraints."""
    
    # Choose constraint
    if constraint_type == 'demographic_parity':
        constraint = DemographicParity()
    elif constraint_type == 'equalized_odds':
        constraint = EqualizedOdds()
    else:
        raise ValueError("Unsupported constraint type")
    
    # Base estimator
    base_estimator = RandomForestClassifier(random_state=42)
    
    # Fair estimator with constraints
    fair_estimator = ExponentiatedGradient(
        estimator=base_estimator,
        constraints=constraint,
        eps=0.01  # Fairness tolerance
    )
    
    # Train
    fair_estimator.fit(X_train, y_train, sensitive_features=sensitive_features_train)
    
    return fair_estimator
''',
            
            'bias_monitoring': '''
# Continuous Bias Monitoring
import numpy as np
from datetime import datetime

class BiasMonitor:
    def __init__(self, threshold=0.1):
        self.threshold = threshold
        self.alerts = []
    
    def check_bias(self, y_true, y_pred, sensitive_features, timestamp=None):
        """Check for bias and generate alerts if needed."""
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Calculate demographic parity
        dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_features)
        
        # Check threshold
        if abs(dp_diff) > self.threshold:
            alert = {
                'timestamp': timestamp,
                'metric': 'demographic_parity_difference',
                'value': dp_diff,
                'threshold': self.threshold,
                'status': 'VIOLATION'
            }
            self.alerts.append(alert)
            print(f"BIAS ALERT: Demographic parity difference ({dp_diff:.3f}) exceeds threshold ({self.threshold})")
        
        return dp_diff
'''
        }
    
    # Helper methods for checking specific bias types
    def _has_underrepresentation(self, bias_results: Dict[str, Any]) -> bool:
        """Check if there are underrepresented groups."""
        if 'demographic_analysis' not in bias_results:
            return False
        
        for attr, analysis in bias_results['demographic_analysis'].items():
            if analysis.get('bias_risk', False):
                return True
        return False
    
    def _has_statistical_parity_issues(self, bias_results: Dict[str, Any]) -> bool:
        """Check if there are statistical parity issues."""
        if 'statistical_parity' not in bias_results:
            return False
        
        for attr, metrics in bias_results['statistical_parity'].items():
            if metrics.get('bias_detected', False):
                return True
        return False
    
    def _has_demographic_parity_issues(self, bias_results: Dict[str, Any]) -> bool:
        """Check for demographic parity issues in model predictions."""
        return self._has_statistical_parity_issues(bias_results)
    
    def _has_equalized_odds_issues(self, bias_results: Dict[str, Any]) -> bool:
        """Check for equalized odds issues."""
        # This would be determined from model bias results
        return True  # Simplified for now
    
    def _has_equal_opportunity_issues(self, bias_results: Dict[str, Any]) -> bool:
        """Check for equal opportunity issues."""
        # This would be determined from model bias results
        return True  # Simplified for now
    
    def _get_smote_implementation(self, attr: str, group: str) -> str:
        """Get SMOTE implementation code for specific attribute and group."""
        return f'''
# SMOTE implementation for {attr} - {group}
from imblearn.over_sampling import SMOTE

# Filter data for the underrepresented group
group_mask = (data['{attr}'] == '{group}')
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X[group_mask], y[group_mask])
'''
    
    def _get_demographic_parity_constraint_code(self) -> str:
        """Get demographic parity constraint implementation."""
        return '''
from fairlearn.reductions import DemographicParity
constraint = DemographicParity()
'''
    
    def _get_equalized_odds_constraint_code(self) -> str:
        """Get equalized odds constraint implementation."""
        return '''
from fairlearn.reductions import EqualizedOdds
constraint = EqualizedOdds()
'''
    
    def _get_equal_opportunity_constraint_code(self) -> str:
        """Get equal opportunity constraint implementation."""
        return '''
from fairlearn.reductions import TruePositiveRateParity
constraint = TruePositiveRateParity()
'''
    
    def _get_feature_selection_code(self, high_corr_features: Dict[str, float]) -> str:
        """Get feature selection code for removing correlated features."""
        features_to_remove = list(high_corr_features.keys())
        return f'''
# Remove features highly correlated with protected attributes
features_to_remove = {features_to_remove}
X_debiased = X.drop(columns=features_to_remove)
'''
    
    def _get_balancing_strategies(self, bias_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get data balancing strategies."""
        strategies = []
        
        if self._has_underrepresentation(bias_results):
            strategy = {
                'strategy': 'Class Rebalancing',
                'description': 'Apply class weights or resampling to balance groups',
                'methods': [
                    'Inverse frequency weighting',
                    'Random oversampling',
                    'Random undersampling',
                    'Tomek links cleaning'
                ],
                'implementation': '''
# Class rebalancing implementation
from sklearn.utils.class_weight import compute_class_weight

# Calculate class weights
class_weights = compute_class_weight(
    'balanced', 
    classes=np.unique(y), 
    y=y
)
class_weight_dict = dict(zip(np.unique(y), class_weights))
'''
            }
            strategies.append(strategy)
        
        return strategies