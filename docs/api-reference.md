# 📚 API Reference - Ethical AI Bias Audit Dashboard

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [BiasDetector API](#biasdetector-api)
4. [MitigationEngine API](#mitigationengine-api)
5. [ExplainableAI API](#explainableai-api)
6. [Usage Examples](#usage-examples)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

## 🎯 Overview

The Ethical AI Bias Audit Dashboard provides a comprehensive Python API for programmatic bias detection and mitigation. This reference covers all public methods, parameters, and return values for seamless integration into your ML pipelines.

### Core Components

```python
from src.bias_detector import BiasDetector
from src.mitigation_engine import MitigationEngine
from src.explainable_ai import ExplainableAI
```

### Quick Example

```python
import pandas as pd
from src.bias_detector import BiasDetector

# Load your data
data = pd.read_csv('your_dataset.csv')

# Initialize detector
detector = BiasDetector()

# Detect bias
results = detector.detect_dataset_bias(
    data=data,
    protected_attributes=['gender', 'race'],
    target_column='outcome'
)

print(f"Bias detected: {results['summary']['bias_detected']}")
```

## 📦 Installation

```bash
# Install from requirements
pip install -r requirements.txt

# Core dependencies for API usage
pip install pandas numpy scikit-learn fairlearn aif360 shap lime
```

## 🔍 BiasDetector API

### Class: `BiasDetector`

The core class for detecting bias in datasets and model predictions.

#### Constructor

```python
BiasDetector()
```

**Description**: Initializes a new BiasDetector instance.

**Parameters**: None

**Returns**: BiasDetector instance

**Example**:
```python
detector = BiasDetector()
```

---

#### Method: `detect_dataset_bias`

```python
detect_dataset_bias(
    data: pd.DataFrame,
    protected_attributes: List[str],
    target_column: str = None
) -> Dict[str, Any]
```

**Description**: Detects bias patterns in a dataset across specified protected attributes.

**Parameters**:
- `data` (pd.DataFrame): Input dataset for bias analysis
- `protected_attributes` (List[str]): List of protected attribute column names
- `target_column` (str, optional): Target variable column name

**Returns**: Dictionary containing comprehensive bias detection results

**Return Structure**:
```python
{
    'statistical_parity': {
        'attribute_name': {
            'group_rates': Dict[str, float],      # Positive rates by group
            'parity_difference': float,           # Max difference between groups
            'bias_detected': bool                 # True if difference > threshold
        }
    },
    'demographic_analysis': {
        'attribute_name': {
            'value_counts': Dict[str, int],       # Count by group
            'percentages': Dict[str, float],      # Percentage by group
            'underrepresented_groups': List[str], # Groups < 5% representation
            'bias_risk': bool                     # True if underrepresentation detected
        }
    },
    'correlation_analysis': {
        'attribute_name': {
            'correlations': Dict[str, float],     # Feature correlations
            'high_correlations': Dict[str, float], # Correlations > 0.3
            'bias_risk': bool                     # True if high correlations found
        }
    },
    'distribution_analysis': {
        'attribute_name': {
            'feature_name': {
                'group_statistics': Dict[str, Dict[str, float]], # Mean, std by group
                'coefficient_of_variation': float,    # Measure of variance
                'high_variation': bool                # True if CV > threshold
            }
        }
    },
    'summary': {
        'total_protected_attributes': int,
        'bias_detected': bool,
        'high_risk_attributes': List[str],
        'severity_level': str                     # 'low', 'medium', 'high', 'critical'
    }
}
```

**Example**:
```python
detector = BiasDetector()
results = detector.detect_dataset_bias(
    data=df,
    protected_attributes=['gender', 'race'],
    target_column='hired'
)

# Check for bias
if results['summary']['bias_detected']:
    print(f"Bias detected in: {results['summary']['high_risk_attributes']}")
    
# Examine specific metrics
gender_parity = results['statistical_parity']['gender']['parity_difference']
print(f"Gender parity difference: {gender_parity:.3f}")
```

---

#### Method: `detect_model_bias`

```python
detect_model_bias(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    protected_attributes: pd.DataFrame
) -> Dict[str, Any]
```

**Description**: Detects bias in model predictions using various fairness metrics.

**Parameters**:
- `y_true` (np.ndarray): True labels
- `y_pred` (np.ndarray): Predicted labels
- `protected_attributes` (pd.DataFrame): DataFrame with protected attribute values

**Returns**: Dictionary containing model bias metrics

**Return Structure**:
```python
{
    'attribute_name': {
        'demographic_parity': {
            'group_rates': Dict[str, float],
            'parity_difference': float,
            'bias_detected': bool
        },
        'equalized_odds': {
            'group_name': {
                'tpr': float,    # True Positive Rate
                'fpr': float     # False Positive Rate
            }
        },
        'equal_opportunity': Dict[str, float],  # TPR by group
        'calibration': Dict[str, float]         # Calibration by group
    }
}
```

**Example**:
```python
# Train your model
model = RandomForestClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Detect model bias
model_bias = detector.detect_model_bias(
    y_true=y_test,
    y_pred=predictions,
    protected_attributes=sensitive_features
)

# Check demographic parity
for attr, metrics in model_bias.items():
    dp_diff = metrics['demographic_parity']['parity_difference']
    if dp_diff > 0.1:
        print(f"Bias detected in {attr}: {dp_diff:.3f}")
```

---

#### Method: `get_bias_summary`

```python
get_bias_summary() -> Dict[str, Any]
```

**Description**: Returns a summary of detected biases from the last analysis.

**Parameters**: None

**Returns**: Summary dictionary

**Return Structure**:
```python
{
    'total_protected_attributes': int,
    'bias_detected': bool,
    'high_risk_attributes': List[str],
    'severity_level': str,
    'recommendations': List[str],
    'next_steps': List[str]
}
```

**Example**:
```python
summary = detector.get_bias_summary()
print(f"Bias detected: {summary['bias_detected']}")
print(f"Severity: {summary['severity_level']}")
for rec in summary['recommendations']:
    print(f"- {rec}")
```

## 🎯 MitigationEngine API

### Class: `MitigationEngine`

Generates actionable bias mitigation recommendations and code suggestions.

#### Constructor

```python
MitigationEngine()
```

**Description**: Initializes a new MitigationEngine instance.

---

#### Method: `generate_recommendations`

```python
generate_recommendations(
    bias_results: Dict[str, Any],
    data_info: Dict[str, Any] = None
) -> Dict[str, Any]
```

**Description**: Generates comprehensive bias mitigation recommendations based on detected bias patterns.

**Parameters**:
- `bias_results` (Dict): Results from bias detection analysis
- `data_info` (Dict, optional): Additional dataset information (size, domain, etc.)

**Returns**: Dictionary containing mitigation recommendations

**Return Structure**:
```python
{
    'immediate_actions': List[str],           # Actions to take right now
    'data_strategies': List[str],            # Data-level improvements
    'modeling_strategies': List[str],         # Model-level improvements
    'code_suggestions': List[Dict[str, str]], # Ready-to-implement code
    'monitoring_strategies': List[str],       # Ongoing monitoring recommendations
    'priority_level': str,                   # 'low', 'medium', 'high', 'critical'
    'estimated_effort': Dict[str, str],      # Time/resource estimates
    'expected_impact': Dict[str, str]        # Expected bias reduction
}
```

**Example**:
```python
engine = MitigationEngine()
recommendations = engine.generate_recommendations(bias_results)

print(f"Priority: {recommendations['priority_level']}")
print("Immediate actions:")
for action in recommendations['immediate_actions']:
    print(f"- {action}")

print("Code suggestions:")
for suggestion in recommendations['code_suggestions']:
    print(f"- {suggestion['description']}")
    print(f"  Code: {suggestion['code']}")
```

---

#### Method: `get_data_augmentation_strategies`

```python
get_data_augmentation_strategies(
    bias_results: Dict[str, Any]
) -> List[Dict[str, Any]]
```

**Description**: Returns specific data augmentation strategies for addressing bias.

**Parameters**:
- `bias_results` (Dict): Results from bias detection analysis

**Returns**: List of data augmentation strategies

**Return Structure**:
```python
[
    {
        'strategy': str,                    # Strategy name
        'target_attribute': str,            # Which attribute to balance
        'target_group': str,               # Which group needs augmentation
        'current_representation': str,      # Current percentage
        'recommended_target': str,         # Target percentage
        'methods': List[str],              # Available methods
        'implementation': str,             # Code snippet
        'expected_improvement': str,       # Expected bias reduction
        'effort_level': str               # 'low', 'medium', 'high'
    }
]
```

**Example**:
```python
strategies = engine.get_data_augmentation_strategies(bias_results)

for strategy in strategies:
    print(f"Strategy: {strategy['strategy']}")
    print(f"Target: {strategy['target_group']} in {strategy['target_attribute']}")
    print(f"Implementation:\n{strategy['implementation']}")
```

---

#### Method: `get_fairness_constraints`

```python
get_fairness_constraints(
    bias_results: Dict[str, Any]
) -> List[Dict[str, Any]]
```

**Description**: Returns fairness constraints that can be applied during model training.

**Parameters**:
- `bias_results` (Dict): Results from bias detection analysis

**Returns**: List of fairness constraints

**Return Structure**:
```python
[
    {
        'type': str,                      # Constraint type
        'description': str,               # What it does
        'implementation': str,            # Code implementation
        'fairlearn_method': str,          # Fairlearn class to use
        'use_case': str,                 # When to use this constraint
        'trade_offs': str,               # Performance vs fairness trade-offs
        'example_code': str              # Complete example
    }
]
```

**Example**:
```python
constraints = engine.get_fairness_constraints(bias_results)

for constraint in constraints:
    if constraint['type'] == 'DemographicParity':
        print(f"Use: {constraint['use_case']}")
        print(f"Implementation:\n{constraint['example_code']}")
```

## 🧠 ExplainableAI API

### Class: `ExplainableAI`

Provides model explanations using SHAP and LIME for bias analysis.

#### Constructor

```python
ExplainableAI()
```

**Description**: Initializes a new ExplainableAI instance.

---

#### Method: `setup_explainers`

```python
setup_explainers(
    X_train: pd.DataFrame,
    model: Any = None,
    explainer_type: str = 'auto'
) -> Dict[str, bool]
```

**Description**: Sets up SHAP and LIME explainers for the given dataset and model.

**Parameters**:
- `X_train` (pd.DataFrame): Training data for setting up explainers
- `model` (Any, optional): Trained model
- `explainer_type` (str): Type of explainer ('shap', 'lime', 'auto')

**Returns**: Dictionary indicating which explainers were successfully set up

**Example**:
```python
explainer = ExplainableAI()
setup_result = explainer.setup_explainers(X_train, model)
print(f"SHAP ready: {setup_result['shap']}")
print(f"LIME ready: {setup_result['lime']}")
```

---

#### Method: `explain_bias_predictions`

```python
explain_bias_predictions(
    X: pd.DataFrame,
    y_pred: np.ndarray,
    protected_attributes: List[str],
    num_samples: int = 10
) -> Dict[str, Any]
```

**Description**: Generates explanations for bias in model predictions.

**Parameters**:
- `X` (pd.DataFrame): Feature data
- `y_pred` (np.ndarray): Model predictions
- `protected_attributes` (List[str]): List of protected attribute names
- `num_samples` (int): Number of samples to explain

**Returns**: Dictionary containing explanation results

**Return Structure**:
```python
{
    'shap_explanations': {
        'global_importance': Dict[str, float],     # Feature importance scores
        'bias_attribution': Dict[str, float],      # Bias contribution by feature
        'protected_feature_impact': Dict[str, float] # Impact of protected attributes
    },
    'lime_explanations': {
        'sample_explanations': List[Dict],         # Individual explanations
        'common_patterns': List[str],              # Common bias patterns
        'discriminatory_features': List[str]       # Features causing bias
    },
    'summary': {
        'primary_bias_sources': List[str],         # Main sources of bias
        'explanation_confidence': float,           # Confidence in explanations
        'actionable_insights': List[str]           # What to do about it
    }
}
```

**Example**:
```python
explanations = explainer.explain_bias_predictions(
    X=X_test,
    y_pred=predictions,
    protected_attributes=['gender', 'race'],
    num_samples=20
)

print("Primary bias sources:")
for source in explanations['summary']['primary_bias_sources']:
    print(f"- {source}")

print("Actionable insights:")
for insight in explanations['summary']['actionable_insights']:
    print(f"- {insight}")
```

---

#### Method: `get_feature_bias_scores`

```python
get_feature_bias_scores(
    X: pd.DataFrame,
    protected_attributes: List[str]
) -> Dict[str, float]
```

**Description**: Calculates bias scores for each feature based on correlation with protected attributes.

**Parameters**:
- `X` (pd.DataFrame): Feature data
- `protected_attributes` (List[str]): List of protected attribute names

**Returns**: Dictionary of feature bias scores (0-1, where 1 is highest bias risk)

**Example**:
```python
bias_scores = explainer.get_feature_bias_scores(
    X=features_df,
    protected_attributes=['gender', 'race']
)

# Sort by bias score
sorted_features = sorted(bias_scores.items(), key=lambda x: x[1], reverse=True)

print("Features with highest bias risk:")
for feature, score in sorted_features[:5]:
    print(f"- {feature}: {score:.3f}")
```

## 💡 Usage Examples

### Complete Bias Audit Workflow

```python
import pandas as pd
import numpy as np
from src.bias_detector import BiasDetector
from src.mitigation_engine import MitigationEngine
from src.explainable_ai import ExplainableAI

# Load data
data = pd.read_csv('dataset.csv')

# Step 1: Detect bias
detector = BiasDetector()
bias_results = detector.detect_dataset_bias(
    data=data,
    protected_attributes=['gender', 'race'],
    target_column='outcome'
)

# Step 2: Get bias summary
summary = detector.get_bias_summary()
print(f"Bias detected: {summary['bias_detected']}")
print(f"Severity: {summary['severity_level']}")

# Step 3: Generate mitigation recommendations
mitigation_engine = MitigationEngine()
recommendations = mitigation_engine.generate_recommendations(bias_results)

print(f"Priority: {recommendations['priority_level']}")
for action in recommendations['immediate_actions']:
    print(f"- {action}")

# Step 4: Explainable AI analysis (if model available)
if 'model' in locals():
    explainer = ExplainableAI()
    explainer.setup_explainers(X_train, model)
    
    feature_bias_scores = explainer.get_feature_bias_scores(
        X=data.drop(['outcome'], axis=1),
        protected_attributes=['gender', 'race']
    )
    
    print("High-risk features:")
    for feature, score in sorted(feature_bias_scores.items(), 
                                key=lambda x: x[1], reverse=True)[:3]:
        print(f"- {feature}: {score:.3f}")

# Step 5: Implement fairness constraints
fairness_constraints = mitigation_engine.get_fairness_constraints(bias_results)
for constraint in fairness_constraints:
    if constraint['type'] == 'DemographicParity':
        print(f"Recommended constraint: {constraint['description']}")
        print(f"Implementation:\n{constraint['implementation']}")
```

### Model Bias Detection Pipeline

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Prepare data
X = data.drop(['outcome', 'gender', 'race'], axis=1)
y = data['outcome']
sensitive_features = data[['gender', 'race']]

X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
    X, y, sensitive_features, test_size=0.3, random_state=42
)

# Train baseline model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f"Baseline accuracy: {accuracy_score(y_test, predictions):.3f}")

# Detect model bias
detector = BiasDetector()
model_bias = detector.detect_model_bias(
    y_true=y_test,
    y_pred=predictions,
    protected_attributes=s_test
)

# Check each protected attribute
for attr, metrics in model_bias.items():
    dp_diff = metrics['demographic_parity']['parity_difference']
    print(f"{attr} demographic parity difference: {dp_diff:.3f}")
    
    if dp_diff > 0.1:
        print(f"⚠️  Bias detected in {attr}")

# Generate explanations
explainer = ExplainableAI()
explainer.setup_explainers(X_train, model)

explanations = explainer.explain_bias_predictions(
    X=X_test,
    y_pred=predictions,
    protected_attributes=['gender', 'race'],
    num_samples=20
)

print("Primary bias sources:")
for source in explanations['summary']['primary_bias_sources']:
    print(f"- {source}")
```

### Automated Fairness Pipeline

```python
def create_fair_model_pipeline(data, protected_attrs, target_col):
    """Complete pipeline for fair model development"""
    
    # Step 1: Bias detection
    detector = BiasDetector()
    bias_results = detector.detect_dataset_bias(
        data=data,
        protected_attributes=protected_attrs,
        target_column=target_col
    )
    
    # Step 2: Data preparation
    mitigation_engine = MitigationEngine()
    augmentation_strategies = mitigation_engine.get_data_augmentation_strategies(bias_results)
    
    # Apply SMOTE if recommended
    X = data.drop([target_col] + protected_attrs, axis=1)
    y = data[target_col]
    sensitive_features = data[protected_attrs]
    
    for strategy in augmentation_strategies:
        if strategy['strategy'] == 'Synthetic Data Generation':
            from imblearn.over_sampling import SMOTE
            smote = SMOTE(random_state=42)
            X, y = smote.fit_resample(X, y)
            break
    
    # Step 3: Train fair model
    fairness_constraints = mitigation_engine.get_fairness_constraints(bias_results)
    
    for constraint in fairness_constraints:
        if constraint['type'] == 'DemographicParity':
            from fairlearn.reductions import ExponentiatedGradient, DemographicParity
            
            constraint_obj = DemographicParity()
            fair_model = ExponentiatedGradient(
                estimator=RandomForestClassifier(),
                constraints=constraint_obj,
                eps=0.01
            )
            
            fair_model.fit(X, y, sensitive_features=sensitive_features.iloc[:, 0])
            break
    
    return fair_model, bias_results

# Usage
fair_model, original_bias = create_fair_model_pipeline(
    data=data,
    protected_attrs=['gender', 'race'],
    target_col='outcome'
)
```

## ⚠️ Error Handling

### Common Exceptions

```python
from src.bias_detector import BiasDetector

try:
    detector = BiasDetector()
    results = detector.detect_dataset_bias(
        data=invalid_data,
        protected_attributes=['invalid_column'],
        target_column='missing_target'
    )
except ValueError as e:
    print(f"Invalid input: {e}")
except KeyError as e:
    print(f"Missing column: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Input Validation

```python
def validate_bias_detection_inputs(data, protected_attributes, target_column=None):
    """Validate inputs before bias detection"""
    
    # Check data type
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data must be a pandas DataFrame")
    
    # Check protected attributes exist
    missing_attrs = [attr for attr in protected_attributes if attr not in data.columns]
    if missing_attrs:
        raise KeyError(f"Missing protected attributes: {missing_attrs}")
    
    # Check target column if provided
    if target_column and target_column not in data.columns:
        raise KeyError(f"Missing target column: {target_column}")
    
    # Check minimum data size
    if len(data) < 10:
        raise ValueError("Dataset too small for reliable bias detection (minimum 10 rows)")
    
    # Check for null values in protected attributes
    for attr in protected_attributes:
        if data[attr].isnull().any():
            raise ValueError(f"Null values found in protected attribute: {attr}")
    
    return True

# Usage
try:
    validate_bias_detection_inputs(data, ['gender', 'race'], 'outcome')
    # Proceed with bias detection
except (TypeError, KeyError, ValueError) as e:
    print(f"Validation failed: {e}")
```

## 🎯 Best Practices

### 1. Data Preparation

```python
# Ensure proper data types
data['gender'] = data['gender'].astype('category')
data['race'] = data['race'].astype('category')

# Handle missing values appropriately
data = data.dropna(subset=['gender', 'race'])  # For protected attributes
data['target'] = data['target'].fillna(0)      # For target variable

# Validate data quality
assert data['gender'].notna().all(), "Missing values in protected attributes"
assert len(data) >= 100, "Insufficient data for reliable bias detection"
```

### 2. Bias Detection Configuration

```python
# Use appropriate thresholds for your domain
detector = BiasDetector()

# For high-stakes applications (hiring, lending), use strict thresholds
results = detector.detect_dataset_bias(
    data=data,
    protected_attributes=['gender', 'race'],
    target_column='outcome'
)

# Check bias at multiple severity levels
for attr in ['gender', 'race']:
    if attr in results['statistical_parity']:
        parity_diff = results['statistical_parity'][attr]['parity_difference']
        
        if parity_diff > 0.05:  # 5% threshold for critical applications
            print(f"⚠️  Critical bias detected in {attr}: {parity_diff:.3f}")
        elif parity_diff > 0.02:  # 2% threshold for monitoring
            print(f"⚡ Monitor bias in {attr}: {parity_diff:.3f}")
```

### 3. Model Integration

```python
# Integrate bias detection into ML pipeline
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class BiasChecker(BaseEstimator, TransformerMixin):
    def __init__(self, protected_attributes, threshold=0.1):
        self.protected_attributes = protected_attributes
        self.threshold = threshold
        self.detector = BiasDetector()
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Check for bias during pipeline execution
        data_with_target = X.copy()
        if y is not None:
            data_with_target['target'] = y
            
        bias_results = self.detector.detect_dataset_bias(
            data=data_with_target,
            protected_attributes=self.protected_attributes,
            target_column='target' if y is not None else None
        )
        
        summary = self.detector.get_bias_summary()
        if summary['bias_detected']:
            print(f"⚠️  Bias detected during pipeline execution: {summary['severity_level']}")
        
        return X

# Use in pipeline
pipeline = Pipeline([
    ('bias_check', BiasChecker(['gender', 'race'])),
    ('model', RandomForestClassifier())
])

pipeline.fit(X_train, y_train)
```

### 4. Continuous Monitoring

```python
def monitor_model_fairness(model, X_test, y_test, sensitive_features, threshold=0.1):
    """Continuous fairness monitoring function"""
    
    predictions = model.predict(X_test)
    
    detector = BiasDetector()
    bias_results = detector.detect_model_bias(
        y_true=y_test,
        y_pred=predictions,
        protected_attributes=sensitive_features
    )
    
    # Check each protected attribute
    alerts = []
    for attr, metrics in bias_results.items():
        dp_diff = metrics['demographic_parity']['parity_difference']
        if dp_diff > threshold:
            alerts.append({
                'attribute': attr,
                'metric': 'demographic_parity',
                'value': dp_diff,
                'threshold': threshold,
                'timestamp': pd.Timestamp.now()
            })
    
    return alerts

# Schedule regular monitoring
import schedule
import time

def scheduled_monitoring():
    alerts = monitor_model_fairness(
        model=production_model,
        X_test=validation_data,
        y_test=validation_labels,
        sensitive_features=validation_sensitive
    )
    
    if alerts:
        print(f"🚨 BIAS ALERT: {len(alerts)} fairness violations detected")
        for alert in alerts:
            print(f"  - {alert['attribute']}: {alert['value']:.3f} > {alert['threshold']}")

# Run every hour in production
schedule.every().hour.do(scheduled_monitoring)
```

### 5. Performance Optimization

```python
# For large datasets, process in chunks
def detect_bias_in_chunks(data, protected_attributes, chunk_size=10000):
    """Process large datasets in chunks"""
    
    detector = BiasDetector()
    chunk_results = []
    
    for chunk_start in range(0, len(data), chunk_size):
        chunk_end = min(chunk_start + chunk_size, len(data))
        chunk_data = data.iloc[chunk_start:chunk_end]
        
        chunk_result = detector.detect_dataset_bias(
            data=chunk_data,
            protected_attributes=protected_attributes
        )
        chunk_results.append(chunk_result)
    
    # Aggregate results (implementation depends on specific needs)
    return aggregate_bias_results(chunk_results)

# Parallel processing for multiple datasets
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def parallel_bias_detection(datasets, protected_attributes):
    """Run bias detection on multiple datasets in parallel"""
    
    def detect_single(data):
        detector = BiasDetector()
        return detector.detect_dataset_bias(data, protected_attributes)
    
    max_workers = min(len(datasets), multiprocessing.cpu_count())
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(detect_single, datasets))
    
    return results
```

---

For more information, see our [User Guide](user-guide.md) and [Best Practices](best-practices.md) guides.