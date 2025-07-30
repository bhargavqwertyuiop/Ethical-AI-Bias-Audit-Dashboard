# 🔧 Troubleshooting Guide - Ethical AI Bias Audit Dashboard

## 📋 Table of Contents

1. [Common Issues](#common-issues)
2. [Installation Problems](#installation-problems)
3. [Data Upload Issues](#data-upload-issues)
4. [Analysis Errors](#analysis-errors)
5. [Performance Issues](#performance-issues)
6. [Dashboard Problems](#dashboard-problems)
7. [API Integration Issues](#api-integration-issues)
8. [Frequently Asked Questions](#frequently-asked-questions)

## 🚨 Common Issues

### Issue: Streamlit AttributeError 'experimental_rerun'

**Problem**: Error when trying sample data: `AttributeError: module 'streamlit' has no attribute 'experimental_rerun'`

**Solution**:
```bash
# Quick fix - run the automated fix script
./scripts/fix-common-issues.sh streamlit

# Or manually update Streamlit
pip install --upgrade streamlit>=1.28.0

# For Docker users - rebuild the container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Explanation**: This occurs when using an older version of Streamlit. The `st.experimental_rerun()` function was deprecated and replaced with `st.rerun()` in newer versions.

---

### Issue: Import Errors for Fairness Libraries

**Problem**: `ImportError: No module named 'fairlearn'` or similar for AIF360, SHAP, LIME

**Solution**:
```bash
# Install missing libraries
pip install fairlearn>=0.10.0
pip install aif360>=0.5.0
pip install shap>=0.43.0
pip install lime>=0.2.0

# Or install all requirements
pip install -r requirements.txt

# Verify installation
python -c "import fairlearn; print('Fairlearn version:', fairlearn.__version__)"
```

---

### Issue: Memory Errors with Large Datasets

**Problem**: `MemoryError` or system freeze when analyzing large datasets

**Solution**:
```python
# Process in chunks for large datasets
def analyze_large_dataset(data, chunk_size=10000):
    results = []
    
    for i in range(0, len(data), chunk_size):
        chunk = data.iloc[i:i+chunk_size]
        chunk_results = detector.detect_dataset_bias(
            data=chunk,
            protected_attributes=['gender', 'race']
        )
        results.append(chunk_results)
    
    return aggregate_results(results)

# Or increase system memory limits
# For Docker: docker run -m 8g your-image
```

---

### Issue: Dashboard Not Loading

**Problem**: Browser shows connection refused or timeout errors

**Solution**:
```bash
# Check if application is running
curl http://localhost:8501

# For local installation
streamlit run dashboard.py --server.port 8501

# For Docker installation
docker-compose ps
docker-compose logs bias-audit-dashboard

# Check port availability
netstat -tulpn | grep 8501
```

## 🔧 Installation Problems

### Python Version Compatibility

**Problem**: Compatibility issues with older Python versions

**Solution**:
```bash
# Check Python version
python --version

# Required: Python 3.8 or higher
# Recommended: Python 3.9+

# Install compatible Python version
# Using pyenv (recommended)
pyenv install 3.9.16
pyenv local 3.9.16

# Using conda
conda create -n bias-audit python=3.9
conda activate bias-audit
```

### Virtual Environment Issues

**Problem**: Package conflicts or permission errors

**Solution**:
```bash
# Create fresh virtual environment
python -m venv venv_new
source venv_new/bin/activate  # Linux/macOS
# venv_new\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
python test_app.py
```

### Docker Installation Issues

**Problem**: Docker build failures or container startup issues

**Solution**:
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check for port conflicts
docker port bias-audit-dashboard

# View logs for errors
docker-compose logs -f

# Test with minimal setup
docker run -p 8501:8501 ethical-ai-bias-audit:latest
```

## 📊 Data Upload Issues

### File Format Problems

**Problem**: "Unsupported file format" or parsing errors

**Solution**:
```python
# Supported formats and solutions
formats = {
    'CSV': {
        'issues': ['encoding', 'separators', 'quotes'],
        'solutions': [
            'pd.read_csv(file, encoding="utf-8")',
            'pd.read_csv(file, sep=";")',
            'pd.read_csv(file, quotechar="\'")'
        ]
    },
    'Excel': {
        'issues': ['sheet selection', 'merged cells', 'formatting'],
        'solutions': [
            'pd.read_excel(file, sheet_name="Sheet1")',
            'pd.read_excel(file, header=1)',
            'Clean data before upload'
        ]
    }
}

# Debug file reading
try:
    data = pd.read_csv('your_file.csv')
    print("✅ File loaded successfully")
except Exception as e:
    print(f"❌ Error: {e}")
    # Try different encoding
    data = pd.read_csv('your_file.csv', encoding='latin1')
```

### Missing or Invalid Columns

**Problem**: "Protected attribute not found" or "Invalid target column"

**Solution**:
```python
# Check column names
print("Available columns:", data.columns.tolist())

# Check for common issues
issues = []

# Extra spaces in column names
data.columns = data.columns.str.strip()

# Case sensitivity
protected_attributes = ['Gender', 'Race']  # Original
protected_attributes = ['gender', 'race']  # Lowercase

# Check data types
print(data.dtypes)
print(data.head())

# Validate protected attributes exist
missing_cols = [col for col in protected_attributes if col not in data.columns]
if missing_cols:
    print(f"Missing columns: {missing_cols}")
    print("Available columns:", data.columns.tolist())
```

### Data Quality Issues

**Problem**: Analysis fails due to poor data quality

**Solution**:
```python
def diagnose_data_quality(data, protected_attributes, target_column):
    """Comprehensive data quality diagnosis"""
    
    issues = []
    
    # Check data size
    if len(data) < 50:
        issues.append(f"Dataset too small: {len(data)} rows (minimum: 50)")
    
    # Check missing values
    for col in protected_attributes + [target_column]:
        if col in data.columns:
            missing_pct = data[col].isnull().mean()
            if missing_pct > 0.1:
                issues.append(f"{col}: {missing_pct:.1%} missing values")
    
    # Check group sizes
    for attr in protected_attributes:
        if attr in data.columns:
            group_sizes = data[attr].value_counts()
            small_groups = group_sizes[group_sizes < 10]
            if len(small_groups) > 0:
                issues.append(f"{attr}: Groups with <10 samples: {small_groups.index.tolist()}")
    
    # Check target variable
    if target_column in data.columns:
        unique_values = data[target_column].nunique()
        if unique_values < 2:
            issues.append(f"Target column {target_column} has only {unique_values} unique values")
    
    return issues

# Usage
issues = diagnose_data_quality(data, ['gender', 'race'], 'hired')
for issue in issues:
    print(f"⚠️ {issue}")
```

## 📈 Analysis Errors

### Numerical Computation Errors

**Problem**: NaN values, division by zero, or infinite values in results

**Solution**:
```python
# Check for and handle numerical issues
import numpy as np

def safe_division(numerator, denominator):
    """Safe division that handles edge cases"""
    if denominator == 0:
        return 0.0
    result = numerator / denominator
    return result if np.isfinite(result) else 0.0

def clean_analysis_results(results):
    """Clean analysis results of invalid values"""
    
    def clean_dict(d):
        if isinstance(d, dict):
            return {k: clean_dict(v) for k, v in d.items()}
        elif isinstance(d, (int, float)):
            return 0.0 if not np.isfinite(d) else d
        else:
            return d
    
    return clean_dict(results)

# Apply to analysis results
cleaned_results = clean_analysis_results(bias_results)
```

### Statistical Significance Issues

**Problem**: Warnings about insufficient sample sizes or statistical power

**Solution**:
```python
def check_statistical_power(data, protected_attributes, target_column, alpha=0.05):
    """Check if sample sizes are sufficient for reliable analysis"""
    
    recommendations = []
    
    for attr in protected_attributes:
        if attr in data.columns:
            group_sizes = data[attr].value_counts()
            
            # Check minimum group size (rule of thumb: 30+ per group)
            min_size = group_sizes.min()
            if min_size < 30:
                recommendations.append(
                    f"Increase sample size for {attr}: smallest group has {min_size} samples "
                    f"(recommended: 30+)"
                )
            
            # Check class balance within groups
            if target_column in data.columns:
                for group in group_sizes.index:
                    group_data = data[data[attr] == group]
                    class_balance = group_data[target_column].value_counts()
                    
                    if len(class_balance) > 1:
                        minority_class_size = class_balance.min()
                        if minority_class_size < 10:
                            recommendations.append(
                                f"Low minority class size in {attr}={group}: "
                                f"{minority_class_size} samples"
                            )
    
    return recommendations

# Usage
power_recommendations = check_statistical_power(data, ['gender', 'race'], 'hired')
for rec in power_recommendations:
    print(f"📊 {rec}")
```

### Model Compatibility Issues

**Problem**: Explainable AI features fail with certain model types

**Solution**:
```python
# Check model compatibility for SHAP/LIME
def check_model_compatibility(model):
    """Check if model is compatible with explainability tools"""
    
    compatibility = {
        'shap': False,
        'lime': False,
        'issues': []
    }
    
    # SHAP compatibility
    shap_compatible_types = [
        'RandomForestClassifier',
        'XGBClassifier',
        'LGBMClassifier',
        'DecisionTreeClassifier'
    ]
    
    model_type = type(model).__name__
    
    if model_type in shap_compatible_types:
        compatibility['shap'] = True
    elif hasattr(model, 'predict_proba'):
        compatibility['shap'] = True  # Can use KernelExplainer
        compatibility['issues'].append("Using slower KernelExplainer for SHAP")
    else:
        compatibility['issues'].append("Model not compatible with SHAP")
    
    # LIME compatibility (more flexible)
    if hasattr(model, 'predict') or hasattr(model, 'predict_proba'):
        compatibility['lime'] = True
    else:
        compatibility['issues'].append("Model not compatible with LIME")
    
    return compatibility

# Usage
compatibility = check_model_compatibility(your_model)
if compatibility['issues']:
    for issue in compatibility['issues']:
        print(f"⚠️ {issue}")
```

## ⚡ Performance Issues

### Slow Analysis Times

**Problem**: Bias detection takes too long to complete

**Solution**:
```python
# Optimize for large datasets
def optimize_analysis_performance(data, protected_attributes, target_column):
    """Optimize analysis for better performance"""
    
    optimizations = []
    
    # Sample large datasets
    if len(data) > 100000:
        sample_size = min(50000, len(data))
        data_sample = data.sample(n=sample_size, random_state=42)
        optimizations.append(f"Sampled {sample_size} rows from {len(data)}")
        data = data_sample
    
    # Reduce precision for floating-point columns
    float_cols = data.select_dtypes(include=['float64']).columns
    if len(float_cols) > 0:
        data[float_cols] = data[float_cols].astype('float32')
        optimizations.append(f"Reduced precision for {len(float_cols)} float columns")
    
    # Convert strings to categories
    for col in protected_attributes:
        if data[col].dtype == 'object':
            data[col] = data[col].astype('category')
            optimizations.append(f"Converted {col} to category")
    
    return data, optimizations

# Usage
optimized_data, optimizations = optimize_analysis_performance(
    data, ['gender', 'race'], 'hired'
)

for opt in optimizations:
    print(f"🔧 {opt}")
```

### Memory Usage Optimization

**Problem**: High memory usage causing system slowdown

**Solution**:
```python
import psutil
import gc

def monitor_memory_usage():
    """Monitor and report memory usage"""
    
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"Memory usage: {memory_info.rss / 1024 / 1024:.1f} MB")
    print(f"Available memory: {psutil.virtual_memory().available / 1024 / 1024:.1f} MB")
    
    return memory_info.rss

def optimize_memory_usage(data):
    """Optimize data types for lower memory usage"""
    
    original_memory = data.memory_usage(deep=True).sum()
    
    # Optimize integer columns
    for col in data.select_dtypes(include=['int64']).columns:
        col_min = data[col].min()
        col_max = data[col].max()
        
        if col_min >= 0:
            if col_max < 255:
                data[col] = data[col].astype('uint8')
            elif col_max < 65535:
                data[col] = data[col].astype('uint16')
            else:
                data[col] = data[col].astype('uint32')
        else:
            if col_min > -128 and col_max < 127:
                data[col] = data[col].astype('int8')
            elif col_min > -32768 and col_max < 32767:
                data[col] = data[col].astype('int16')
            else:
                data[col] = data[col].astype('int32')
    
    # Optimize string columns
    for col in data.select_dtypes(include=['object']).columns:
        if data[col].nunique() < len(data) * 0.5:  # If less than 50% unique values
            data[col] = data[col].astype('category')
    
    new_memory = data.memory_usage(deep=True).sum()
    reduction = (original_memory - new_memory) / original_memory * 100
    
    print(f"Memory usage reduced by {reduction:.1f}%")
    
    # Force garbage collection
    gc.collect()
    
    return data
```

## 🖥️ Dashboard Problems

### Browser Compatibility Issues

**Problem**: Dashboard doesn't display correctly in certain browsers

**Solution**:
```bash
# Recommended browsers and versions
Supported browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

# Clear browser cache
# Chrome: Ctrl+Shift+Delete
# Firefox: Ctrl+Shift+Delete
# Safari: Cmd+Option+E

# Disable browser extensions that might interfere
# Try incognito/private browsing mode

# Check JavaScript is enabled
# Streamlit requires JavaScript to function
```

### Session State Issues

**Problem**: Dashboard loses state or behaves unexpectedly

**Solution**:
```python
# Clear Streamlit cache and session state
import streamlit as st

# Add this to your dashboard
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.experimental_rerun()  # or st.rerun() for newer versions

# Check session state
def debug_session_state():
    """Debug session state issues"""
    st.write("Current session state:")
    for key, value in st.session_state.items():
        st.write(f"- {key}: {type(value)} = {value}")

# Reset session state if needed
def reset_session_state():
    """Reset all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
```

### File Upload Widget Issues

**Problem**: File upload fails or behaves inconsistently

**Solution**:
```python
# Robust file upload handling
def handle_file_upload(uploaded_file):
    """Handle file upload with proper error checking"""
    
    if uploaded_file is not None:
        try:
            # Check file size
            file_size = uploaded_file.size
            max_size = 100 * 1024 * 1024  # 100MB
            
            if file_size > max_size:
                st.error(f"File too large: {file_size/1024/1024:.1f}MB (max: 100MB)")
                return None
            
            # Check file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            supported_extensions = ['csv', 'xlsx', 'xls', 'json']
            
            if file_extension not in supported_extensions:
                st.error(f"Unsupported file type: {file_extension}")
                return None
            
            # Try to read the file
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                data = pd.read_excel(uploaded_file)
            elif file_extension == 'json':
                data = pd.read_json(uploaded_file)
            
            # Validate data
            if len(data) == 0:
                st.error("File is empty")
                return None
            
            if len(data.columns) < 2:
                st.error("File must have at least 2 columns")
                return None
            
            st.success(f"File loaded: {len(data)} rows, {len(data.columns)} columns")
            return data
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    
    return None

# Usage in dashboard
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'json'])
data = handle_file_upload(uploaded_file)
```

## 🔌 API Integration Issues

### Authentication Problems

**Problem**: API calls fail with authentication errors

**Solution**:
```python
# Set up proper authentication for API usage
import requests
import os

def setup_api_authentication():
    """Setup authentication for API calls"""
    
    # Check for API key
    api_key = os.getenv('BIAS_AUDIT_API_KEY')
    if not api_key:
        print("Warning: No API key found. Set BIAS_AUDIT_API_KEY environment variable")
        return None
    
    # Setup headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    return headers

# Test API connection
def test_api_connection(base_url, headers):
    """Test API connection"""
    
    try:
        response = requests.get(f"{base_url}/health", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ API connection successful")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {e}")
        return False
```

### Rate Limiting Issues

**Problem**: API calls are being rate limited

**Solution**:
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """Decorator to implement rate limiting"""
    
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 60.0 / calls_per_minute - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        
        return wrapper
    return decorator

# Usage
@rate_limit(calls_per_minute=30)
def api_call_with_rate_limit(data):
    """API call with rate limiting"""
    # Your API call here
    pass
```

## ❓ Frequently Asked Questions

### General Questions

**Q: What types of bias can the dashboard detect?**

A: The dashboard can detect several types of bias:
- **Statistical bias**: Differences in positive prediction rates between groups
- **Representation bias**: Underrepresentation of certain demographic groups
- **Historical bias**: Bias inherited from historical data
- **Proxy bias**: Indirect bias through correlated features
- **Intersectional bias**: Bias affecting multiple protected attributes simultaneously

**Q: What fairness metrics are supported?**

A: Supported metrics include:
- Statistical Parity (Demographic Parity)
- Equalized Odds
- Equal Opportunity
- Calibration
- Individual Fairness
- Predictive Parity

**Q: Can I use the dashboard with my own model?**

A: Yes! The dashboard supports:
- Any scikit-learn compatible model
- Models with `predict()` and/or `predict_proba()` methods
- Tree-based models (for enhanced SHAP support)
- Custom models (with wrapper functions)

### Technical Questions

**Q: What's the maximum dataset size supported?**

A: Dataset size limits:
- **Web interface**: 100MB file upload limit
- **Local installation**: Limited by available RAM
- **API usage**: No hard limit, but performance may degrade
- **Recommended**: <1M rows for optimal performance

**Q: How accurate are the bias measurements?**

A: Accuracy depends on several factors:
- **Sample size**: Larger samples provide more reliable estimates
- **Data quality**: Clean, representative data improves accuracy
- **Statistical power**: Minimum 30 samples per group recommended
- **Confidence intervals**: 95% confidence intervals provided for key metrics

**Q: Can I export analysis results?**

A: Yes, multiple export options are available:
- **PDF reports**: Executive and technical summaries
- **CSV data**: Raw analysis results and metrics
- **JSON format**: Complete analysis data structure
- **Code snippets**: Ready-to-implement mitigation code
- **Jupyter notebooks**: Interactive analysis workflows

### Implementation Questions

**Q: How do I integrate bias detection into my ML pipeline?**

A: Integration options:
```python
# Option 1: API integration
from src.bias_detector import BiasDetector

detector = BiasDetector()
bias_results = detector.detect_dataset_bias(data, protected_attrs, target)

# Option 2: Pipeline component
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('bias_check', BiasChecker(protected_attrs)),
    ('model', YourModel())
])

# Option 3: Automated monitoring
schedule.every().week.do(automated_bias_check)
```

**Q: What mitigation strategies are recommended?**

A: The dashboard provides prioritized recommendations:
1. **Immediate actions**: Process and training improvements
2. **Data strategies**: Balancing, augmentation, feature engineering
3. **Model strategies**: Fairness constraints, ensemble methods
4. **Monitoring**: Continuous bias detection and alerting

**Q: How do I handle missing protected attribute data?**

A: Several approaches are supported:
```python
# Option 1: Remove rows with missing data
data_clean = data.dropna(subset=protected_attributes)

# Option 2: Create "Unknown" category
data['gender'] = data['gender'].fillna('Unknown')

# Option 3: Impute based on other features
# (use with caution to avoid introducing bias)
```

---

## 🆘 Getting Additional Help

### Diagnostic Tools

Run the built-in diagnostic tools:
```bash
# Test application components
python test_app.py

# Fix common issues automatically
./scripts/fix-common-issues.sh all

# Check system compatibility
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import pandas; print(f'Pandas: {pandas.__version__}')"
```

### Log Analysis

Enable detailed logging:
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or add to your analysis
logger = logging.getLogger(__name__)
logger.debug("Running bias detection analysis...")
```

### Community Support

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences  
- **Documentation**: Comprehensive guides and examples
- **Examples**: Real-world usage patterns and code samples

### Professional Support

For enterprise deployments or complex requirements:
- Custom implementation consulting
- Performance optimization services
- Training and education programs
- Compliance and audit assistance

---

**Still having issues?** Please open a GitHub issue with:
1. **Error description**: What went wrong?
2. **Steps to reproduce**: How can we recreate the issue?
3. **Environment details**: OS, Python version, installation method
4. **Error logs**: Complete error messages and stack traces
5. **Sample data**: If possible, provide a minimal example

We're here to help make AI more fair and ethical! 🌟