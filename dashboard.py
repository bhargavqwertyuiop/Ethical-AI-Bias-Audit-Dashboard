"""
Main Streamlit Dashboard for the Ethical AI Bias Audit Tool.
Provides a comprehensive interface for bias detection, analysis, and mitigation recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import io
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from src.bias_detector import BiasDetector
from src.mitigation_engine import MitigationEngine
from src.explainable_ai import ExplainableAI

# Page configuration
st.set_page_config(
    page_title="Ethical AI Bias Audit Dashboard",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .warning-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .critical-card {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .success-card {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .code-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Ethical AI Bias Audit Dashboard</h1>
        <p>Proactive bias detection with actionable mitigation recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'bias_results' not in st.session_state:
        st.session_state.bias_results = None
    if 'mitigation_recommendations' not in st.session_state:
        st.session_state.mitigation_recommendations = None
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "📊 Data Upload & Analysis", "🔍 Bias Detection", "🎯 Mitigation Strategies", "🧠 Explainable AI", "📚 Documentation"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📊 Data Upload & Analysis":
        show_data_upload_page()
    elif page == "🔍 Bias Detection":
        show_bias_detection_page()
    elif page == "🎯 Mitigation Strategies":
        show_mitigation_page()
    elif page == "🧠 Explainable AI":
        show_explainable_ai_page()
    elif page == "📚 Documentation":
        show_documentation_page()

def show_home_page():
    """Display the home page with overview and features."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 What is Bias Audit Dashboard?")
        st.markdown("""
        The Ethical AI Bias Audit Dashboard is a comprehensive tool designed to help developers and data scientists 
        identify, understand, and mitigate bias in AI systems. Our tool provides:
        
        - **🔍 Automated Bias Detection**: Multi-dimensional bias analysis across protected attributes
        - **📊 Interactive Visualizations**: Clear, actionable insights through modern data visualization
        - **💡 Mitigation Recommendations**: Specific, code-level suggestions for bias reduction
        - **🧠 Explainable AI**: SHAP and LIME explanations for model decisions
        - **📈 Fairness Metrics**: Comprehensive fairness evaluation using industry standards
        """)
        
        st.markdown("## 🚀 Getting Started")
        st.markdown("""
        1. **Upload your dataset** in the Data Upload & Analysis section
        2. **Specify protected attributes** (gender, race, age, etc.)
        3. **Run bias detection** to identify potential fairness issues
        4. **Review mitigation strategies** with actionable recommendations
        5. **Implement suggested solutions** using our code templates
        """)
    
    with col2:
        st.markdown("## 📈 Key Features")
        
        features = [
            {"icon": "⚖️", "title": "Fairness Metrics", "desc": "Demographic parity, equalized odds, and more"},
            {"icon": "🎨", "title": "Visual Analytics", "desc": "Interactive charts and bias heatmaps"},
            {"icon": "🔧", "title": "Code Generation", "desc": "Ready-to-use mitigation code snippets"},
            {"icon": "📊", "title": "Real-time Analysis", "desc": "Instant feedback on bias detection"},
            {"icon": "🧪", "title": "XAI Integration", "desc": "SHAP and LIME explanations"},
            {"icon": "📚", "title": "Best Practices", "desc": "Industry-standard bias mitigation techniques"}
        ]
        
        for feature in features:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{feature['icon']} {feature['title']}</h4>
                <p style="margin: 0; color: #666;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_data_upload_page():
    """Display the data upload and initial analysis page."""
    
    st.markdown("## 📊 Data Upload & Initial Analysis")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=['csv', 'xlsx', 'json'],
        help="Supported formats: CSV, Excel, JSON"
    )
    
    if uploaded_file is not None:
        # Load data based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                data = pd.read_json(uploaded_file)
            else:
                st.error("❌ Unsupported file format. Please upload CSV, Excel, or JSON files.")
                return
            
            # Validate data
            if data.empty:
                st.error("❌ The uploaded file is empty.")
                return
            
            if len(data.columns) < 2:
                st.error("❌ Dataset must have at least 2 columns for bias analysis.")
                return
            
            st.session_state.data = data
            
            # Clear previous protected attributes and target column when new data is loaded
            # They will be re-selected by the user for the new dataset
            if hasattr(st.session_state, 'protected_attributes'):
                st.session_state.protected_attributes = []
            if hasattr(st.session_state, 'target_column'):
                delattr(st.session_state, 'target_column')
            
            st.success(f"✅ Successfully loaded {len(data)} rows and {len(data.columns)} columns")
            
            # Data preview
            st.markdown("### 👀 Data Preview")
            st.dataframe(data.head(10), use_container_width=True)
            
            # Data summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Total Rows", f"{len(data):,}")
            with col2:
                st.metric("📈 Total Columns", len(data.columns))
            with col3:
                missing_percentage = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
                st.metric("❌ Missing Data", f"{missing_percentage:.1f}%")
            
            # Column analysis
            st.markdown("### 🔍 Column Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Data Types")
                try:
                    dtype_counts = data.dtypes.value_counts()
                    # Convert dtype names to strings to avoid JSON serialization issues
                    dtype_names = [str(dtype) for dtype in dtype_counts.index]
                    fig = px.pie(
                        values=dtype_counts.values,
                        names=dtype_names,
                        title="Distribution of Data Types"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error displaying data types: {str(e)}")
                    # Fallback: show data types as text
                    st.write("**Data Types:**")
                    for col, dtype in data.dtypes.items():
                        st.write(f"- {col}: {str(dtype)}")
            
            with col2:
                st.markdown("#### Missing Values")
                missing_data = data.isnull().sum().sort_values(ascending=False)
                missing_data = missing_data[missing_data > 0]
                
                if len(missing_data) > 0:
                    fig = px.bar(
                        x=missing_data.values,
                        y=missing_data.index,
                        orientation='h',
                        title="Missing Values by Column"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("🎉 No missing values detected!")
            
            # Protected attributes selection
            st.markdown("### 🛡️ Protected Attributes Selection")
            st.markdown("Select columns that represent protected attributes (e.g., gender, race, age)")
            
            # Show available columns and suggest potential protected attributes
            with st.expander("💡 Need help identifying protected attributes?", expanded=False):
                st.markdown("""
                **Common protected attributes include:**
                - **Gender/Sex**: gender, sex, male_female, etc.
                - **Race/Ethnicity**: race, ethnicity, ethnic_group, etc.
                - **Age**: age, age_group, age_category, etc.
                - **Religion**: religion, religious_affiliation, etc.
                - **Disability**: disability, disabled, disability_status, etc.
                - **Sexual Orientation**: sexual_orientation, orientation, etc.
                
                **Available columns in your dataset:**
                """)
                st.write(", ".join(f"`{col}`" for col in data.columns.tolist()))
            
            # Get previously selected attributes if any
            current_protected_attrs = getattr(st.session_state, 'protected_attributes', [])
            
            # Filter current protected attributes to only include those that exist in the current dataset
            available_columns = data.columns.tolist()
            valid_current_attrs = [attr for attr in current_protected_attrs if attr in available_columns]
            
            protected_attrs = st.multiselect(
                "Protected Attributes",
                options=available_columns,
                default=valid_current_attrs,
                help="These are attributes that should not be used for discrimination (e.g., gender, race, age)"
            )
            
            # Update session state
            st.session_state.protected_attributes = protected_attrs
            
            if protected_attrs:
                st.success(f"✅ Selected {len(protected_attrs)} protected attribute(s): {', '.join(protected_attrs)}")
            else:
                st.info("ℹ️ Please select at least one protected attribute to enable bias detection.")
                
            if protected_attrs:
                # Show distribution of protected attributes
                st.markdown("#### Protected Attribute Distributions")
                
                for attr in protected_attrs:
                    if data[attr].dtype in ['object', 'category'] or data[attr].nunique() < 20:
                        fig = px.histogram(
                            data, 
                            x=attr, 
                            title=f"Distribution of {attr}",
                            color_discrete_sequence=['#667eea']
                        )
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
            
            # Target variable selection
            st.markdown("### 🎯 Target Variable Selection")
            target_col = st.selectbox(
                "Select target variable (optional)",
                options=["None"] + data.columns.tolist(),
                help="The variable you want to predict or analyze for bias"
            )
            
            if target_col != "None":
                st.session_state.target_column = target_col
                
                # Show target distribution
                if data[target_col].dtype in ['object', 'category'] or data[target_col].nunique() < 20:
                    fig = px.histogram(
                        data, 
                        x=target_col, 
                        title=f"Distribution of {target_col}",
                        color_discrete_sequence=['#764ba2']
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Cross-tabulation with protected attributes
                if protected_attrs and target_col != "None":
                    st.markdown("#### Cross-tabulation Analysis")
                    
                    for attr in protected_attrs:
                        if (data[attr].dtype in ['object', 'category'] or data[attr].nunique() < 20) and \
                           (data[target_col].dtype in ['object', 'category'] or data[target_col].nunique() < 20):
                            
                            crosstab = pd.crosstab(data[attr], data[target_col], normalize='index')
                            
                            fig = px.imshow(
                                crosstab.values,
                                labels=dict(x=target_col, y=attr, color="Proportion"),
                                x=crosstab.columns,
                                y=crosstab.index,
                                title=f"Cross-tabulation: {attr} vs {target_col}",
                                color_continuous_scale='RdYlBu_r'
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("💡 **Troubleshooting tips:**\n- Check that your file is a valid CSV, Excel, or JSON format\n- Ensure the file is not corrupted\n- Try uploading a smaller file if it's very large\n- Make sure column names don't contain special characters")
            # Clear any partially loaded data
            if hasattr(st.session_state, 'data'):
                st.session_state.data = None
    
    else:
        # Show sample data option
        st.markdown("### 🎲 Or Try with Sample Data")
        if st.button("Load Sample Dataset"):
            sample_data = generate_sample_data()
            st.session_state.data = sample_data
            # Clear previous selections when loading new data
            st.session_state.protected_attributes = []
            if hasattr(st.session_state, 'target_column'):
                delattr(st.session_state, 'target_column')
            st.success("✅ Sample dataset loaded successfully! Please select protected attributes below.")
            st.rerun()

def show_bias_detection_page():
    """Display the bias detection analysis page."""
    
    st.markdown("## 🔍 Bias Detection Analysis")
    
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first in the Data Upload & Analysis section.")
        return
    
    data = st.session_state.data
    protected_attrs = getattr(st.session_state, 'protected_attributes', [])
    target_col = getattr(st.session_state, 'target_column', None)
    
    if not protected_attrs:
        st.warning("⚠️ Please select protected attributes first in the Data Upload & Analysis section.")
        st.info("💡 **How to fix this:**\n\n1. Go to the **Data Upload & Analysis** section using the sidebar\n2. Upload your dataset\n3. Select one or more **Protected Attributes** (e.g., gender, race, age)\n4. Return to this section to run bias detection")
        
        # Show available columns if data exists
        if hasattr(st.session_state, 'data') and st.session_state.data is not None:
            st.markdown("**Available columns in your dataset:**")
            cols = st.session_state.data.columns.tolist()
            st.write(", ".join(cols))
        return
    
    # Bias detection controls
    st.markdown("### ⚙️ Analysis Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        detection_scope = st.selectbox(
            "Detection Scope",
            ["Full Analysis", "Statistical Parity Only", "Demographic Analysis Only"]
        )
    
    with col2:
        bias_threshold = st.slider(
            "Bias Detection Threshold",
            min_value=0.05,
            max_value=0.3,
            value=0.1,
            step=0.05,
            help="Lower values are more sensitive to bias"
        )
    
    with col3:
        if st.button("🚀 Run Bias Detection", type="primary"):
            with st.spinner("🔍 Analyzing data for bias..."):
                bias_detector = BiasDetector()
                bias_results = bias_detector.detect_dataset_bias(
                    data, 
                    protected_attrs, 
                    target_col
                )
                st.session_state.bias_results = bias_results
                st.success("✅ Bias detection completed!")
    
    # Display results if available
    if st.session_state.bias_results is not None:
        bias_results = st.session_state.bias_results
        
        # Bias summary
        bias_detector = BiasDetector()
        bias_detector.bias_report = bias_results
        summary = bias_detector.get_bias_summary()
        
        st.markdown("### 📋 Bias Detection Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🛡️ Protected Attributes", summary.get('total_protected_attributes', 0))
        
        with col2:
            bias_detected = summary.get('bias_detected', False)
            st.metric("⚠️ Bias Detected", "Yes" if bias_detected else "No")
        
        with col3:
            high_risk_count = len(summary.get('high_risk_attributes', []))
            st.metric("🚨 High Risk Attributes", high_risk_count)
        
        with col4:
            recommendation_count = len(summary.get('recommendations', []))
            st.metric("💡 Recommendations", recommendation_count)
        
        # Alert cards
        if summary.get('bias_detected', False):
            st.markdown("""
            <div class="critical-card">
                <h4>🚨 Bias Detected</h4>
                <p>Our analysis has identified potential bias in your dataset. Review the detailed results below and consider implementing the suggested mitigation strategies.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-card">
                <h4>✅ No Significant Bias Detected</h4>
                <p>Our analysis did not identify significant bias patterns. However, continue monitoring and consider additional fairness checks.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed results tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistical Parity", "👥 Demographics", "🔗 Correlations", "📈 Distributions"])
        
        with tab1:
            show_statistical_parity_results(bias_results.get('statistical_parity', {}))
        
        with tab2:
            show_demographic_results(bias_results.get('demographic_analysis', {}))
        
        with tab3:
            show_correlation_results(bias_results.get('correlation_analysis', {}))
        
        with tab4:
            show_distribution_results(bias_results.get('distribution_analysis', {}))

def show_mitigation_page():
    """Display the bias mitigation strategies page."""
    
    st.markdown("## 🎯 Bias Mitigation Strategies")
    
    if st.session_state.bias_results is None:
        st.warning("⚠️ Please run bias detection first.")
        return
    
    # Generate mitigation recommendations
    if st.session_state.mitigation_recommendations is None:
        with st.spinner("🧠 Generating mitigation recommendations..."):
            mitigation_engine = MitigationEngine()
            recommendations = mitigation_engine.generate_recommendations(st.session_state.bias_results)
            st.session_state.mitigation_recommendations = recommendations
    
    recommendations = st.session_state.mitigation_recommendations
    
    # Priority alert
    priority = recommendations.get('priority_level', 'low')
    priority_colors = {
        'critical': 'critical-card',
        'high': 'warning-card',
        'medium': 'warning-card',
        'low': 'success-card'
    }
    
    st.markdown(f"""
    <div class="{priority_colors.get(priority, 'success-card')}">
        <h4>📊 Priority Level: {priority.upper()}</h4>
        <p>Based on the detected bias patterns, we recommend taking action with {priority} priority.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚨 Immediate Actions", 
        "📊 Data Strategies", 
        "🤖 Modeling Strategies", 
        "💻 Code Suggestions", 
        "📈 Monitoring"
    ])
    
    with tab1:
        st.markdown("### 🚨 Immediate Actions Required")
        immediate_actions = recommendations.get('immediate_actions', [])
        
        if immediate_actions:
            for i, action in enumerate(immediate_actions, 1):
                st.markdown(f"""
                <div class="warning-card">
                    <h5>Action {i}</h5>
                    <p>{action}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No immediate critical actions required.")
    
    with tab2:
        st.markdown("### 📊 Data-Level Strategies")
        
        # Data augmentation strategies
        mitigation_engine = MitigationEngine()
        augmentation_strategies = mitigation_engine.get_data_augmentation_strategies(st.session_state.bias_results)
        
        if augmentation_strategies:
            for strategy in augmentation_strategies:
                with st.expander(f"🔄 {strategy['strategy']} - {strategy['target_attribute']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Target Group:** {strategy['target_group']}")
                        st.markdown(f"**Current Representation:** {strategy['current_representation']}")
                        st.markdown(f"**Recommended Target:** {strategy['recommended_target']}")
                    
                    with col2:
                        st.markdown("**Methods:**")
                        for method in strategy['methods']:
                            st.markdown(f"- {method}")
                    
                    st.markdown("**Implementation:**")
                    st.code(strategy['implementation'], language='python')
        
        # General data strategies
        data_strategies = recommendations.get('data_strategies', [])
        for strategy in data_strategies:
            st.markdown(f"- {strategy}")
    
    with tab3:
        st.markdown("### 🤖 Modeling Strategies")
        
        # Fairness constraints
        mitigation_engine = MitigationEngine()
        fairness_constraints = mitigation_engine.get_fairness_constraints(st.session_state.bias_results)
        
        if fairness_constraints:
            for constraint in fairness_constraints:
                with st.expander(f"⚖️ {constraint['type']}"):
                    st.markdown(f"**Description:** {constraint['description']}")
                    st.markdown(f"**Use Case:** {constraint['use_case']}")
                    st.markdown(f"**Fairlearn Method:** `{constraint['fairlearn_method']}`")
                    
                    st.markdown("**Implementation:**")
                    st.code(constraint['implementation'], language='python')
        
        # General modeling strategies
        modeling_strategies = recommendations.get('modeling_strategies', [])
        for strategy in modeling_strategies:
            st.markdown(f"- {strategy}")
    
    with tab4:
        st.markdown("### 💻 Code Suggestions")
        
        code_suggestions = recommendations.get('code_suggestions', [])
        
        for suggestion in code_suggestions:
            with st.expander(f"💻 {suggestion['title']}"):
                st.markdown(f"**Description:** {suggestion['description']}")
                st.code(suggestion['code'], language='python')
                
                # Download button for code
                st.download_button(
                    label="📥 Download Code",
                    data=suggestion['code'],
                    file_name=f"{suggestion['title'].lower().replace(' ', '_')}.py",
                    mime="text/python"
                )
    
    with tab5:
        st.markdown("### 📈 Monitoring Strategies")
        
        monitoring_strategies = recommendations.get('monitoring_strategies', [])
        for strategy in monitoring_strategies:
            st.markdown(f"- {strategy}")
        
        # Bias monitoring template
        with st.expander("📊 Bias Monitoring Template"):
            monitoring_code = '''
# Bias Monitoring System Template
import pandas as pd
import numpy as np
from datetime import datetime
from fairlearn.metrics import demographic_parity_difference

class BiasMonitor:
    def __init__(self, threshold=0.1):
        self.threshold = threshold
        self.alerts = []
        
    def monitor_predictions(self, y_true, y_pred, sensitive_features):
        """Monitor model predictions for bias."""
        
        # Calculate bias metrics
        dp_diff = demographic_parity_difference(
            y_true, y_pred, 
            sensitive_features=sensitive_features
        )
        
        # Check for violations
        if abs(dp_diff) > self.threshold:
            alert = {
                'timestamp': datetime.now(),
                'metric': 'demographic_parity',
                'value': dp_diff,
                'status': 'VIOLATION'
            }
            self.alerts.append(alert)
            return alert
        
        return None
    
    def get_alert_summary(self):
        """Get summary of bias alerts."""
        return {
            'total_alerts': len(self.alerts),
            'recent_alerts': [a for a in self.alerts 
                            if (datetime.now() - a['timestamp']).days <= 7]
        }

# Usage example
monitor = BiasMonitor(threshold=0.1)
alert = monitor.monitor_predictions(y_true, y_pred, sensitive_features)

if alert:
    print(f"BIAS ALERT: {alert}")
'''
            st.code(monitoring_code, language='python')

def show_explainable_ai_page():
    """Display the explainable AI analysis page."""
    
    st.markdown("## 🧠 Explainable AI Analysis")
    
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first.")
        return
    
    st.markdown("""
    ### 🎯 What is Explainable AI for Bias Detection?
    
    Explainable AI (XAI) helps us understand **why** bias occurs in our models and data. 
    This section uses SHAP and LIME to provide insights into:
    
    - **Feature Importance**: Which features contribute most to biased decisions
    - **Group Explanations**: How different protected groups are affected
    - **Bias Patterns**: Understanding the root causes of unfairness
    """)
    
    # XAI availability check
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            import shap
            st.success("✅ SHAP Available")
            shap_available = True
        except ImportError:
            st.error("❌ SHAP Not Available")
            shap_available = False
    
    with col2:
        try:
            import lime
            st.success("✅ LIME Available")
            lime_available = True
        except ImportError:
            st.error("❌ LIME Not Available")
            lime_available = False
    
    if not (shap_available or lime_available):
        st.warning("⚠️ Please install SHAP and/or LIME to use explainable AI features.")
        st.code("pip install shap lime")
        return
    
    # Feature bias analysis
    data = st.session_state.data
    protected_attrs = getattr(st.session_state, 'protected_attributes', [])
    
    if protected_attrs:
        st.markdown("### 🔍 Feature Bias Analysis")
        
        with st.spinner("🧠 Analyzing feature bias scores..."):
            explainer = ExplainableAI()
            bias_scores = explainer.get_feature_bias_scores(data, protected_attrs)
        
        if bias_scores:
            # Create bias scores visualization
            features = list(bias_scores.keys())
            scores = list(bias_scores.values())
            
            fig = px.bar(
                x=scores,
                y=features,
                orientation='h',
                title="Feature Bias Scores",
                labels={'x': 'Bias Score', 'y': 'Features'},
                color=scores,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=max(400, len(features) * 25))
            st.plotly_chart(fig, use_container_width=True)
            
            # High-risk features
            high_risk_features = [f for f, s in bias_scores.items() if s > 0.3]
            
            if high_risk_features:
                st.markdown("""
                <div class="warning-card">
                    <h4>⚠️ High-Risk Features Detected</h4>
                    <p>The following features show high correlation with protected attributes:</p>
                </div>
                """, unsafe_allow_html=True)
                
                for feature in high_risk_features:
                    score = bias_scores[feature]
                    st.markdown(f"- **{feature}**: {score:.3f} bias score")
            else:
                st.markdown("""
                <div class="success-card">
                    <h4>✅ Low Bias Risk Features</h4>
                    <p>Most features show low correlation with protected attributes.</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Model explanation section (if we had model predictions)
    st.markdown("### 🤖 Model Explanation Demo")
    st.markdown("""
    This section would show SHAP and LIME explanations for actual model predictions. 
    For demonstration, here's how it would work:
    """)
    
    # Demo explanation visualization
    demo_features = ['feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5']
    demo_importance = [0.3, -0.2, 0.15, -0.1, 0.05]
    
    fig = px.bar(
        x=demo_importance,
        y=demo_features,
        orientation='h',
        title="SHAP Feature Importance (Demo)",
        color=demo_importance,
        color_continuous_scale='RdBu_r',
        labels={'x': 'SHAP Value', 'y': 'Features'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Code example for XAI
    with st.expander("💻 XAI Implementation Example"):
        xai_code = '''
# Explainable AI for Bias Detection
import shap
import lime
from lime.lime_tabular import LimeTabularExplainer

# SHAP Example
def explain_with_shap(model, X_train, X_test):
    """Generate SHAP explanations for model predictions."""
    
    # Create explainer
    explainer = shap.TreeExplainer(model)
    
    # Get SHAP values
    shap_values = explainer.shap_values(X_test)
    
    # Visualize
    shap.summary_plot(shap_values, X_test)
    
    return shap_values

# LIME Example  
def explain_with_lime(model, X_train, X_test, instance_idx=0):
    """Generate LIME explanation for a single prediction."""
    
    # Create explainer
    explainer = LimeTabularExplainer(
        X_train.values,
        feature_names=X_train.columns,
        class_names=['Class 0', 'Class 1'],
        mode='classification'
    )
    
    # Explain instance
    explanation = explainer.explain_instance(
        X_test.iloc[instance_idx].values,
        model.predict_proba,
        num_features=10
    )
    
    # Show in notebook
    explanation.show_in_notebook(show_table=True)
    
    return explanation

# Bias-specific explanation
def explain_bias_patterns(model, X, protected_attr):
    """Analyze how protected attributes influence predictions."""
    
    groups = X[protected_attr].unique()
    explanations = {}
    
    for group in groups:
        group_data = X[X[protected_attr] == group]
        group_explanations = explain_with_shap(model, X, group_data)
        explanations[group] = group_explanations
    
    return explanations
'''
        st.code(xai_code, language='python')

def show_documentation_page():
    """Display comprehensive documentation."""
    
    st.markdown("## 📚 Documentation")
    
    # Documentation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Quick Start", 
        "📊 Fairness Metrics", 
        "🔧 API Reference", 
        "💡 Best Practices", 
        "🌟 Examples"
    ])
    
    with tab1:
        st.markdown("""
        ### 🚀 Quick Start Guide
        
        #### 1. Data Preparation
        - Ensure your dataset is clean and properly formatted
        - Identify protected attributes (gender, race, age, etc.)
        - Choose your target variable if applicable
        
        #### 2. Upload and Configure
        - Upload your dataset using the Data Upload page
        - Select protected attributes from the dropdown
        - Configure analysis parameters
        
        #### 3. Run Bias Detection
        - Navigate to the Bias Detection page
        - Choose your analysis scope
        - Set bias detection thresholds
        - Run the analysis
        
        #### 4. Review Results
        - Examine statistical parity metrics
        - Analyze demographic distributions
        - Check correlation patterns
        - Review feature distributions
        
        #### 5. Implement Mitigation
        - Review generated recommendations
        - Download code templates
        - Implement suggested strategies
        - Monitor ongoing bias metrics
        """)
    
    with tab2:
        st.markdown("""
        ### ⚖️ Fairness Metrics Explained
        
        #### Demographic Parity
        **Definition**: Equal positive prediction rates across groups
        **Formula**: P(Ŷ=1|A=a) = P(Ŷ=1|A=b) for groups a,b
        **Use Case**: When equal treatment is the primary goal
        
        #### Equalized Odds
        **Definition**: Equal TPR and FPR across groups
        **Formula**: P(Ŷ=1|Y=y,A=a) = P(Ŷ=1|Y=y,A=b) for y∈{0,1}
        **Use Case**: When prediction accuracy should be consistent
        
        #### Equal Opportunity
        **Definition**: Equal True Positive Rates across groups
        **Formula**: P(Ŷ=1|Y=1,A=a) = P(Ŷ=1|Y=1,A=b)
        **Use Case**: When qualified individuals should have equal opportunity
        
        #### Calibration
        **Definition**: Prediction probabilities reflect true probabilities
        **Formula**: P(Y=1|Ŷ=v,A=a) = P(Y=1|Ŷ=v,A=b) for all v
        **Use Case**: When prediction confidence should be meaningful
        """)
    
    with tab3:
        st.markdown("""
        ### 🔧 API Reference
        
        #### BiasDetector Class
        ```python
        class BiasDetector:
            def detect_dataset_bias(data, protected_attributes, target_column=None)
            def detect_model_bias(y_true, y_pred, protected_attributes)
            def get_bias_summary()
        ```
        
        #### MitigationEngine Class
        ```python
        class MitigationEngine:
            def generate_recommendations(bias_results, data_info=None)
            def get_data_augmentation_strategies(bias_results)
            def get_fairness_constraints(bias_results)
            def get_preprocessing_strategies(bias_results)
        ```
        
        #### ExplainableAI Class
        ```python
        class ExplainableAI:
            def setup_explainers(X_train, model=None, explainer_type='auto')
            def explain_bias_predictions(X, y_pred, protected_attributes)
            def explain_fairness_violations(X, y_true, y_pred, protected_attributes)
            def get_feature_bias_scores(X, protected_attributes)
        ```
        """)
    
    with tab4:
        st.markdown("""
        ### 💡 Best Practices
        
        #### Data Collection
        - Ensure representative sampling across all groups
        - Document data collection methodology
        - Regular audits of data sources
        - Implement bias-aware data collection protocols
        
        #### Model Development
        - Use fairness constraints during training
        - Implement cross-validation with stratification
        - Regular bias testing throughout development
        - Document model limitations and assumptions
        
        #### Deployment & Monitoring
        - Continuous bias monitoring in production
        - Automated alerting for fairness violations
        - Regular model retraining with updated data
        - Stakeholder reporting and transparency
        
        #### Team & Process
        - Diverse development teams
        - Ethics review boards
        - Regular bias awareness training
        - Clear escalation procedures for bias issues
        """)
    
    with tab5:
        st.markdown("""
        ### 🌟 Example Use Cases
        
        #### Hiring & Recruitment
        - **Challenge**: Ensuring fair candidate evaluation
        - **Solution**: Analyze resume screening for gender/racial bias
        - **Metrics**: Demographic parity, equal opportunity
        
        #### Credit Scoring
        - **Challenge**: Fair lending practices
        - **Solution**: Monitor approval rates across protected groups
        - **Metrics**: Equalized odds, calibration
        
        #### Healthcare AI
        - **Challenge**: Equitable treatment recommendations
        - **Solution**: Analyze diagnostic accuracy across demographics
        - **Metrics**: Equal opportunity, calibration
        
        #### Criminal Justice
        - **Challenge**: Fair risk assessment
        - **Solution**: Ensure equal accuracy across racial groups
        - **Metrics**: Equalized odds, predictive parity
        """)

# Helper functions for displaying detailed results
def show_statistical_parity_results(results):
    """Display statistical parity analysis results."""
    if not results:
        st.info("No statistical parity analysis available.")
        return
    
    for attr, metrics in results.items():
        st.markdown(f"#### {attr}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Parity Difference", 
                f"{metrics.get('parity_difference', 0):.3f}",
                delta=f"{'⚠️ Bias' if metrics.get('bias_detected', False) else '✅ OK'}"
            )
        
        with col2:
            group_rates = metrics.get('group_rates', {})
            if group_rates:
                fig = px.bar(
                    x=list(group_rates.keys()),
                    y=list(group_rates.values()),
                    title=f"Outcome Rates by {attr}",
                    color=list(group_rates.values()),
                    color_continuous_scale='RdYlBu_r'
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

def show_demographic_results(results):
    """Display demographic analysis results."""
    if not results:
        st.info("No demographic analysis available.")
        return
    
    for attr, analysis in results.items():
        st.markdown(f"#### {attr}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            percentages = analysis.get('percentages', {})
            if percentages:
                fig = px.pie(
                    values=list(percentages.values()),
                    names=list(percentages.keys()),
                    title=f"Distribution of {attr}"
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            underrepresented = analysis.get('underrepresented_groups', {})
            if underrepresented:
                st.markdown("**Underrepresented Groups:**")
                for group, percentage in underrepresented.items():
                    st.markdown(f"- {group}: {percentage}%")
            else:
                st.success("✅ No underrepresented groups detected")

def show_correlation_results(results):
    """Display correlation analysis results."""
    if not results:
        st.info("No correlation analysis available.")
        return
    
    for attr, analysis in results.items():
        st.markdown(f"#### {attr}")
        
        high_correlations = analysis.get('high_correlations', {})
        
        if high_correlations:
            st.markdown("**High Correlations (>0.3):**")
            
            features = list(high_correlations.keys())
            correlations = list(high_correlations.values())
            
            fig = px.bar(
                x=correlations,
                y=features,
                orientation='h',
                title=f"High Correlations with {attr}",
                color=correlations,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=max(200, len(features) * 30))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success(f"✅ No high correlations detected for {attr}")

def show_distribution_results(results):
    """Display distribution analysis results."""
    if not results:
        st.info("No distribution analysis available.")
        return
    
    for attr, attr_results in results.items():
        st.markdown(f"#### {attr}")
        
        high_variation_features = []
        for feature, stats in attr_results.items():
            if stats.get('high_variation', False):
                high_variation_features.append({
                    'feature': feature,
                    'cv': stats.get('coefficient_of_variation', 0)
                })
        
        if high_variation_features:
            st.markdown("**Features with High Variation Across Groups:**")
            
            features = [f['feature'] for f in high_variation_features]
            cvs = [f['cv'] for f in high_variation_features]
            
            fig = px.bar(
                x=cvs,
                y=features,
                orientation='h',
                title=f"Coefficient of Variation by {attr}",
                color=cvs,
                color_continuous_scale='Oranges'
            )
            fig.update_layout(height=max(200, len(features) * 30))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success(f"✅ No high variation features detected for {attr}")

def generate_sample_data():
    """Generate sample dataset for demonstration."""
    np.random.seed(42)
    
    n_samples = 1000
    
    # Generate synthetic data
    data = {
        'age': np.random.randint(18, 70, n_samples),
        'income': np.random.normal(50000, 20000, n_samples),
        'education_years': np.random.randint(10, 20, n_samples),
        'credit_score': np.random.randint(300, 800, n_samples),
        'gender': np.random.choice(['Male', 'Female'], n_samples, p=[0.6, 0.4]),
        'race': np.random.choice(['White', 'Black', 'Hispanic', 'Asian'], n_samples, p=[0.6, 0.2, 0.15, 0.05]),
        'employment_status': np.random.choice(['Employed', 'Unemployed', 'Self-employed'], n_samples, p=[0.8, 0.1, 0.1])
    }
    
    # Create biased target variable
    approved_prob = (
        0.3 + 
        0.0001 * data['income'] + 
        0.002 * data['credit_score'] +
        0.01 * data['education_years'] +
        0.1 * (np.array(data['gender']) == 'Male').astype(int) +
        0.05 * (np.array(data['race']) == 'White').astype(int)
    )
    
    # Add some noise and ensure probabilities are valid
    approved_prob = np.clip(approved_prob + np.random.normal(0, 0.1, n_samples), 0, 1)
    data['approved'] = np.random.binomial(1, approved_prob, n_samples)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    main()