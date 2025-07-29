# 🛡️ Ethical AI Bias Audit Dashboard

A comprehensive tool for detecting, analyzing, and mitigating bias in AI systems. This dashboard provides proactive bias detection with actionable mitigation recommendations, featuring explainable AI techniques and industry-standard fairness metrics.

![Dashboard Preview](assets/dashboard_preview.png)

## 🎯 Features

- **🔍 Automated Bias Detection**: Multi-dimensional bias analysis across protected attributes
- **📊 Interactive Visualizations**: Clear, actionable insights through modern data visualization
- **💡 Mitigation Recommendations**: Specific, code-level suggestions for bias reduction
- **🧠 Explainable AI**: SHAP and LIME explanations for model decisions
- **📈 Fairness Metrics**: Comprehensive fairness evaluation using industry standards
- **⚖️ Multiple Fairness Criteria**: Demographic parity, equalized odds, equal opportunity, and calibration
- **🔧 Code Generation**: Ready-to-use mitigation code snippets
- **📚 Best Practices**: Industry-standard bias mitigation techniques

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/ethical-ai-bias-audit-dashboard.git
cd ethical-ai-bias-audit-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch the dashboard:
```bash
streamlit run dashboard.py
```

4. Open your browser to `http://localhost:8501`

### Basic Usage

1. **Upload your dataset** in CSV, Excel, or JSON format
2. **Select protected attributes** (gender, race, age, etc.)
3. **Choose target variable** (optional, for supervised learning scenarios)
4. **Run bias detection** to identify potential fairness issues
5. **Review recommendations** and implement suggested mitigation strategies

## 📊 Supported Fairness Metrics

### Statistical Parity (Demographic Parity)
- **Definition**: Equal positive prediction rates across groups
- **Formula**: P(Ŷ=1|A=a) = P(Ŷ=1|A=b) for groups a,b
- **Use Case**: When equal treatment is the primary goal

### Equalized Odds
- **Definition**: Equal TPR and FPR across groups
- **Formula**: P(Ŷ=1|Y=y,A=a) = P(Ŷ=1|Y=y,A=b) for y∈{0,1}
- **Use Case**: When prediction accuracy should be consistent

### Equal Opportunity
- **Definition**: Equal True Positive Rates across groups
- **Formula**: P(Ŷ=1|Y=1,A=a) = P(Ŷ=1|Y=1,A=b)
- **Use Case**: When qualified individuals should have equal opportunity

### Calibration
- **Definition**: Prediction probabilities reflect true probabilities
- **Formula**: P(Y=1|Ŷ=v,A=a) = P(Y=1|Ŷ=v,A=b) for all v
- **Use Case**: When prediction confidence should be meaningful

## 🔧 API Reference

### BiasDetector Class

```python
from src.bias_detector import BiasDetector

detector = BiasDetector()

# Detect dataset bias
bias_results = detector.detect_dataset_bias(
    data=df,
    protected_attributes=['gender', 'race'],
    target_column='outcome'
)

# Detect model bias
model_bias = detector.detect_model_bias(
    y_true=y_test,
    y_pred=predictions,
    protected_attributes=sensitive_features
)

# Get bias summary
summary = detector.get_bias_summary()
```

### MitigationEngine Class

```python
from src.mitigation_engine import MitigationEngine

engine = MitigationEngine()

# Generate recommendations
recommendations = engine.generate_recommendations(bias_results)

# Get data augmentation strategies
augmentation = engine.get_data_augmentation_strategies(bias_results)

# Get fairness constraints
constraints = engine.get_fairness_constraints(bias_results)
```

### ExplainableAI Class

```python
from src.explainable_ai import ExplainableAI

explainer = ExplainableAI()

# Setup explainers
explainer.setup_explainers(X_train, model)

# Get feature bias scores
bias_scores = explainer.get_feature_bias_scores(X, protected_attributes)

# Explain bias predictions
explanations = explainer.explain_bias_predictions(
    X, y_pred, protected_attributes
)
```

## 🧪 Examples

### Jupyter Notebook Demo

Check out our comprehensive demo notebook:

```bash
jupyter notebook examples/bias_audit_demo.ipynb
```

### Sample Data

Use our sample dataset to try the dashboard:

```python
# Load sample data
import pandas as pd
df = pd.read_csv('data/sample_hiring_data.csv')

# Protected attributes
protected_attrs = ['gender', 'race']
target_col = 'hired'
```

### Command Line Interface

```python
# Quick bias check
python -c "
from src.bias_detector import BiasDetector
import pandas as pd

df = pd.read_csv('data/sample_hiring_data.csv')
detector = BiasDetector()
results = detector.detect_dataset_bias(df, ['gender', 'race'], 'hired')
summary = detector.get_bias_summary()
print('Bias detected:', summary['bias_detected'])
"
```

## 🏗️ Architecture

```
ethical-ai-bias-audit-dashboard/
├── src/
│   ├── bias_detector.py       # Core bias detection engine
│   ├── mitigation_engine.py   # Bias mitigation recommendations
│   ├── explainable_ai.py      # XAI analysis using SHAP/LIME
│   └── __init__.py
├── dashboard.py               # Main Streamlit dashboard
├── examples/
│   └── bias_audit_demo.ipynb  # Comprehensive demo notebook
├── data/
│   └── sample_hiring_data.csv # Sample dataset
├── requirements.txt           # Dependencies
└── README.md
```

## 🔍 Bias Detection Methods

### Dataset-Level Analysis
- **Statistical Parity**: Outcome rate differences across groups
- **Demographic Analysis**: Group representation and underrepresentation
- **Correlation Analysis**: Feature correlation with protected attributes
- **Distribution Analysis**: Feature distribution differences across groups

### Model-Level Analysis
- **Fairness Metrics**: Comprehensive fairness evaluation
- **Performance Disparities**: Accuracy differences across groups
- **Prediction Patterns**: Systematic prediction differences

### Explainable AI Analysis
- **Feature Importance**: SHAP and LIME explanations
- **Bias Attribution**: Understanding sources of unfairness
- **Group-Specific Explanations**: How different groups are affected

## 💡 Mitigation Strategies

### Data-Level Strategies
- Synthetic data generation (SMOTE, CTGAN)
- Stratified sampling for balanced representation
- Data collection process improvements
- Feature selection to remove proxy variables

### Model-Level Strategies
- Fairness constraints during training (Fairlearn)
- Adversarial debiasing techniques
- Post-processing fairness adjustments
- Ensemble methods with fairness considerations

### Process-Level Strategies
- Continuous bias monitoring in production
- Regular bias audits and assessments
- Stakeholder training and awareness
- Documentation and transparency measures

## 🎨 Dashboard Features

### Home Page
- Project overview and key features
- Getting started guide
- Feature highlights with icons

### Data Upload & Analysis
- Support for CSV, Excel, JSON formats
- Automatic data profiling and summary
- Protected attribute selection
- Cross-tabulation analysis

### Bias Detection
- Configurable analysis parameters
- Real-time bias detection
- Interactive visualizations
- Statistical significance testing

### Mitigation Strategies
- Priority-based recommendations
- Code suggestions with download
- Data augmentation strategies
- Fairness constraints implementation

### Explainable AI
- Feature bias scoring
- SHAP/LIME integration
- Bias pattern analysis
- Discriminatory feature identification

### Documentation
- Comprehensive usage guide
- API reference
- Best practices
- Example use cases

## 🔬 Use Cases

### Hiring & Recruitment
- **Challenge**: Ensuring fair candidate evaluation
- **Solution**: Analyze resume screening for gender/racial bias
- **Metrics**: Demographic parity, equal opportunity

### Credit Scoring
- **Challenge**: Fair lending practices
- **Solution**: Monitor approval rates across protected groups
- **Metrics**: Equalized odds, calibration

### Healthcare AI
- **Challenge**: Equitable treatment recommendations
- **Solution**: Analyze diagnostic accuracy across demographics
- **Metrics**: Equal opportunity, calibration

### Criminal Justice
- **Challenge**: Fair risk assessment
- **Solution**: Ensure equal accuracy across racial groups
- **Metrics**: Equalized odds, predictive parity

## 📈 Best Practices

### Data Collection
- Ensure representative sampling across all groups
- Document data collection methodology
- Regular audits of data sources
- Implement bias-aware data collection protocols

### Model Development
- Use fairness constraints during training
- Implement cross-validation with stratification
- Regular bias testing throughout development
- Document model limitations and assumptions

### Deployment & Monitoring
- Continuous bias monitoring in production
- Automated alerting for fairness violations
- Regular model retraining with updated data
- Stakeholder reporting and transparency

### Team & Process
- Diverse development teams
- Ethics review boards
- Regular bias awareness training
- Clear escalation procedures for bias issues

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `pytest tests/`
5. Submit a pull request

### Areas for Contribution
- Additional fairness metrics
- New visualization types
- Enhanced explainability features
- Performance optimizations
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Fairlearn](https://fairlearn.org/) for fairness metrics and algorithms
- [SHAP](https://shap.readthedocs.io/) for explainable AI techniques
- [LIME](https://github.com/marcotcr/lime) for local interpretability
- [Streamlit](https://streamlit.io/) for the dashboard framework
- [Plotly](https://plotly.com/) for interactive visualizations

## 📞 Support

- 📧 Email: support@bias-audit-dashboard.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/ethical-ai-bias-audit-dashboard/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/ethical-ai-bias-audit-dashboard/discussions)
- 📖 Documentation: [Wiki](https://github.com/your-username/ethical-ai-bias-audit-dashboard/wiki)

## 🔄 Changelog

### v1.0.0 (2024-01-01)
- Initial release
- Core bias detection engine
- Streamlit dashboard interface
- Explainable AI integration
- Comprehensive documentation
- Sample datasets and examples

---

**⚠️ Disclaimer**: This tool is designed to assist in bias detection and mitigation but should not be the sole method for ensuring fairness in AI systems. Always combine automated tools with human oversight, domain expertise, and stakeholder consultation.