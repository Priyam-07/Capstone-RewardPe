"""
RewardPe x StyleKart Integration Demo
AI-Powered Loyalty Platform - CPO Capstone Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
import time

# Add project root to path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

from models.churn_model import ChurnPredictor, CustomerSegmenter, RewardRecommender
from models.ai_offer_generator import AIOfferGenerator
from sdk.stylekart_integration import StyleKartIntegration, RewardPeSDK

# Page config
st.set_page_config(
    page_title="RewardPe x StyleKart Demo",
    layout="wide",
    page_icon="👗",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Calibri:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: Calibri, 'Segoe UI', sans-serif !important;
        font-size: 18px !important;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #666;
        margin-top: 0;
    }
    .stApp > header {display: none;}
    section[data-testid="stSidebar"] > div {padding-top: 0;}
    .block-container {padding-top: 1.5rem;}
    p, li, span, div {font-size: 1.05rem;}
    h3 {font-size: 1.5rem !important;}
    .stMarkdown p {font-size: 1.05rem !important; line-height: 1.6;}
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stylekart-brand {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'demo_step' not in st.session_state:
    st.session_state.demo_step = 0
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'integration_complete' not in st.session_state:
    st.session_state.integration_complete = False

@st.cache_data
def load_stylekart_data():
    """Load StyleKart customer data"""
    data_path = os.path.join(APP_DIR, 'data', 'stylekart_customers.csv')
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        # Generate if not exists
        from data.generate_stylekart_data import generate_customer
        customers = [generate_customer(i) for i in range(1500)]
        df = pd.DataFrame(customers)
        df.to_csv(data_path, index=False)
        return df

@st.cache_resource
def get_trained_model():
    """Get trained churn prediction model"""
    df = load_stylekart_data()
    predictor = ChurnPredictor()
    metrics = predictor.train(df)
    return predictor, metrics

def render_sidebar():
    """Render sidebar navigation"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 10px 10px 10px;">
        <div style="font-size: 2.2rem; margin-bottom: 2px;">🎁</div>
        <div style="font-size: 1.6rem; font-weight: 800; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">RewardPe</div>
        <div style="font-size: 1rem; font-weight: 700; background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 2px;">× StyleKart</div>
        <div style="font-size: 0.7rem; color: #999; margin-top: 6px;">AI-Powered Loyalty Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    demo_mode = st.sidebar.checkbox("🎬 Demo Mode", value=True)
    
    if demo_mode:
        st.sidebar.markdown("<p style='font-size: 0.95rem; font-weight: 700; margin-bottom: 10px;'>📋 Demo Progress</p>", unsafe_allow_html=True)
        steps = [
            "1️⃣ Integration Setup",
            "2️⃣ Vendor Configuration",
            "3️⃣ Data Sync",
            "4️⃣ AI Analysis",
            "5️⃣ Recommendations",
            "6️⃣ AI Personalized Offers",
            "7️⃣ Dashboard"
        ]
        for i, step in enumerate(steps):
            if i < st.session_state.demo_step:
                st.sidebar.success(f"✅ {step}")
            elif i == st.session_state.demo_step:
                st.sidebar.info(f"▶️ {step}")
            else:
                st.sidebar.markdown(f"<p style='font-size: 0.85rem; color: #888; margin: 4px 0;'>{step}</p>", unsafe_allow_html=True)
    
    return demo_mode


def render_step_0_integration():
    """Step 0: SDK Integration Setup"""
    # Hero Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #FF6B6B 100%); padding: 40px; border-radius: 16px; margin-bottom: 30px; text-align: center; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: rgba(255,255,255,0.05); border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -30px; left: -30px; width: 150px; height: 150px; background: rgba(255,255,255,0.05); border-radius: 50%;"></div>
        <h1 style="color: white; font-size: 2.8rem; margin: 0; font-weight: 800; letter-spacing: -1px;">🎁 RewardPe</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin: 8px 0 4px 0; font-weight: 300;">AI-Powered Loyalty Intelligence Platform</p>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">Predict Churn · Personalize Rewards · Drive Retention</p>
        <div style="margin-top: 20px; display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.15); padding: 10px 20px; border-radius: 8px; backdrop-filter: blur(5px);">
                <span style="color: white; font-size: 1.4rem; font-weight: 700;">32%</span><br>
                <span style="color: rgba(255,255,255,0.7); font-size: 0.7rem;">Churn Reduction</span>
            </div>
            <div style="background: rgba(255,255,255,0.15); padding: 10px 20px; border-radius: 8px; backdrop-filter: blur(5px);">
                <span style="color: white; font-size: 1.4rem; font-weight: 700;">3.2x</span><br>
                <span style="color: rgba(255,255,255,0.7); font-size: 0.7rem;">ROI on Rewards</span>
            </div>
            <div style="background: rgba(255,255,255,0.15); padding: 10px 20px; border-radius: 8px; backdrop-filter: blur(5px);">
                <span style="color: white; font-size: 1.4rem; font-weight: 700;">< 2 min</span><br>
                <span style="color: rgba(255,255,255,0.7); font-size: 0.7rem;">SDK Integration</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("<h2 style='margin-bottom:5px;'>🔌 SDK Integration Setup</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Connect StyleKart with RewardPe Platform</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### About StyleKart")
        st.info("""
        **StyleKart** is India's leading fashion e-commerce platform with:
        - 🛍️ 1,500+ active customers
        - 👗 50,000+ fashion products
        - 📱 2M+ monthly app sessions
        - 💰 ₹15 Cr annual GMV
        
        **Challenge:** 25% annual customer churn costing ₹3.75 Cr in lost revenue
        """)
        
        st.markdown("### Integration Steps")
        
        if st.button("🚀 Start Integration", type="primary", use_container_width=True):
            integration = StyleKartIntegration()
            
            with st.spinner("Setting up integration..."):
                progress = st.progress(0)
                status_text = st.empty()
                
                steps = integration.setup_integration()
                
                for i, step in enumerate(steps):
                    time.sleep(0.8)
                    progress.progress((i + 1) / len(steps))
                    status_text.write(f"✅ {step['action']} - {step['status']}")
                
                time.sleep(0.5)
                st.session_state.integration_complete = True
                st.session_state.demo_step = 1
                st.rerun()
    
    with col2:
        st.markdown("### SDK Code Snippet")
        st.code("""
# Install RewardPe SDK
pip install rewardpe-sdk

# Initialize
from rewardpe import RewardPe

client = RewardPe(
    api_key='sk_live_stylekart_xxx',
    environment='production'
)

# Connect
client.connect()
        """, language="python")
        
        st.markdown("### Webhook Events")
        st.markdown("""
        - `customer.churn_risk_high`
        - `reward.recommended`
        - `campaign.triggered`
        """)


def render_step_1_vendor_config():
    """Step 1: Vendor/MarTech Stack Configuration"""
    st.markdown("<h1 class='main-header'>🔧 MarTech Stack Configuration</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Connect RewardPe with StyleKart's existing systems</p>", unsafe_allow_html=True)
    
    st.info("💡 **RewardPe integrates with your existing tools** - we're the AI brain that powers your loyalty program, not a replacement for your MarTech stack.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Customer Data Platform (CDP)")
        cdp = st.selectbox(
            "Select your CDP",
            ["Segment", "mParticle", "Rudderstack", "Tealium", "Custom API"],
            index=0
        )
        
        st.markdown("### 🗄️ CRM System")
        crm = st.selectbox(
            "Select your CRM",
            ["Salesforce", "HubSpot", "Zoho CRM", "Freshsales", "Custom CRM"],
            index=1
        )
        
        st.markdown("### 📱 Marketing Automation")
        marketing = st.selectbox(
            "Select your Marketing Platform",
            ["CleverTap", "MoEngage", "WebEngage", "Braze", "Iterable", "Custom"],
            index=0
        )
    
    with col2:
        st.markdown("### 📧 Email Provider")
        email = st.selectbox(
            "Select your Email Service",
            ["SendGrid", "Mailchimp", "Amazon SES", "Postmark", "Custom SMTP"],
            index=0
        )
        
        st.markdown("### 📱 SMS Provider")
        sms = st.selectbox(
            "Select your SMS Gateway",
            ["Twilio", "Gupshup", "MSG91", "Kaleyra", "Custom API"],
            index=0
        )
        
        st.markdown("### 💬 WhatsApp Business")
        whatsapp = st.selectbox(
            "Select your WhatsApp Provider",
            ["Gupshup", "Twilio", "Infobip", "Kaleyra", "Meta Direct", "Not Configured"],
            index=0
        )
    
    st.markdown("---")
    
    # Show integration architecture
    st.markdown("### 🏗️ Integration Architecture")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="text-align: center; font-family: monospace;">
            <div style="background: #FF6B6B; color: white; padding: 15px; border-radius: 10px; display: inline-block; margin: 10px;">
                <strong>👗 StyleKart</strong><br>
                <small>E-commerce Platform</small>
            </div>
            <div style="font-size: 24px; margin: 10px;">⬇️</div>
            <div style="background: #4CAF50; color: white; padding: 10px; border-radius: 8px; display: inline-block; margin: 5px;">
                {cdp}
            </div>
            <div style="font-size: 24px; margin: 10px;">⬇️</div>
            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; display: inline-block; margin: 10px;">
                <strong>🧠 RewardPe AI Engine</strong><br>
                <small>Churn Prediction • Segmentation • Personalization</small>
            </div>
            <div style="font-size: 24px; margin: 10px;">⬇️</div>
            <div style="background: #2196F3; color: white; padding: 10px; border-radius: 8px; display: inline-block; margin: 5px;">
                {marketing}
            </div>
            <div style="font-size: 24px; margin: 10px;">⬇️</div>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <div style="background: #9C27B0; color: white; padding: 8px 15px; border-radius: 8px;">📧 {email}</div>
                <div style="background: #FF9800; color: white; padding: 8px 15px; border-radius: 8px;">📱 {sms}</div>
                <div style="background: #25D366; color: white; padding: 8px 15px; border-radius: 8px;">💬 {whatsapp}</div>
            </div>
            <div style="font-size: 24px; margin: 10px;">⬇️</div>
            <div style="background: #607D8B; color: white; padding: 15px; border-radius: 10px; display: inline-block;">
                <strong>👥 StyleKart Customers</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Store configuration
    if 'vendor_config' not in st.session_state:
        st.session_state.vendor_config = {}
    
    st.session_state.vendor_config = {
        'cdp': cdp,
        'crm': crm,
        'marketing': marketing,
        'email': email,
        'sms': sms,
        'whatsapp': whatsapp
    }
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Confirm Configuration & Continue", type="primary", use_container_width=True):
            with st.spinner("Validating connections..."):
                progress = st.progress(0)
                
                vendors = [cdp, crm, marketing, email, sms, whatsapp]
                for i, vendor in enumerate(vendors):
                    time.sleep(0.4)
                    progress.progress((i + 1) / len(vendors))
                
                st.success("✅ All vendor connections validated!")
                time.sleep(0.5)
                st.session_state.demo_step = 2
                st.rerun()


def render_step_2_data_sync():
    """Step 1: Data Synchronization"""
    st.markdown("<h1 class='main-header'>📤 Customer Data Sync</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Syncing 1,500 StyleKart customers to RewardPe</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Data Preview")
        df = load_stylekart_data()
        
        # Show sample data
        display_cols = ['customer_id', 'name', 'city', 'total_orders', 'total_spend', 
                       'last_purchase_days', 'engagement_score']
        st.dataframe(df[display_cols].head(10), use_container_width=True)
        
        st.markdown(f"**Total Records:** {len(df):,} customers")
        
        if st.button("📤 Sync Data to RewardPe", type="primary", use_container_width=True):
            with st.spinner("Syncing customer data..."):
                progress = st.progress(0)
                
                for i in range(100):
                    time.sleep(0.02)
                    progress.progress(i + 1)
                
                st.session_state.data_loaded = True
                st.session_state.demo_step = 3
                st.success("✅ Data sync complete! 1,500 customers synced successfully.")
                time.sleep(1)
                st.rerun()
    
    with col2:
        st.markdown("### Data Quality Report")
        st.metric("Records Processed", "1,500")
        st.metric("Data Completeness", "98.5%")
        st.metric("Valid Records", "1,500")
        
        st.markdown("### Fields Mapped")
        st.markdown("""
        - ✅ Customer ID
        - ✅ Demographics
        - ✅ Transaction History
        - ✅ Engagement Metrics
        - ✅ Behavioral Data
        """)


def render_step_3_ai_analysis():
    """Step 2: AI Analysis"""
    st.markdown("<h1 class='main-header'>🤖 AI Analysis Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Real ML models analyzing customer behavior</p>", unsafe_allow_html=True)
    
    df = load_stylekart_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🧠 Run AI Analysis", type="primary", use_container_width=True):
            with st.spinner("Training ML models..."):
                progress = st.progress(0)
                status = st.empty()
                
                # Step 1: Train model
                status.write("🔄 Training Gradient Boosting model...")
                predictor, metrics = get_trained_model()
                progress.progress(33)
                time.sleep(0.5)
                
                # Step 2: Predict churn
                status.write("🔄 Predicting churn probabilities...")
                churn_probs = predictor.predict_churn_probability(df)
                progress.progress(66)
                time.sleep(0.5)
                
                # Step 3: Segment customers
                status.write("🔄 Segmenting customers...")
                segmenter = CustomerSegmenter()
                df_analyzed = segmenter.segment_customers(df, churn_probs)
                progress.progress(100)
                
                st.session_state.df_analyzed = df_analyzed
                st.session_state.model_metrics = metrics
                st.session_state.model_trained = True
                st.session_state.demo_step = 4
                
                status.empty()
                st.success(f"✅ AI Analysis Complete! Model Accuracy: {metrics['accuracy']*100:.1f}%")
                time.sleep(1)
                st.rerun()
    
    with col2:
        st.markdown("### ML Models Used")
        st.markdown("""
        **1. Churn Prediction**
        - Algorithm: Gradient Boosting
        - Features: 14 behavioral signals
        - Accuracy: ~89%
        
        **2. Customer Segmentation**
        - Emotional Loyalty Index (ELI)
        - 5 distinct segments
        
        **3. Reward Optimization**
        - Personalized recommendations
        - Expected lift prediction
        """)
    
    if st.session_state.model_trained and 'df_analyzed' in st.session_state:
        st.markdown("---")
        st.markdown("### Segmentation Results")
        
        df_analyzed = st.session_state.df_analyzed
        
        col1, col2, col3, col4, col5 = st.columns(5)
        segments = df_analyzed['segment'].value_counts()
        
        col1.metric("🏆 Champions", segments.get('Champions', 0))
        col2.metric("💚 Loyal", segments.get('Loyal', 0))
        col3.metric("🌱 Potential", segments.get('Potential', 0))
        col4.metric("⚠️ At Risk", segments.get('At Risk', 0))
        col5.metric("👀 Needs Attention", segments.get('Needs Attention', 0))
        
        # Segment distribution chart
        fig = px.pie(
            df_analyzed, names='segment',
            color='segment',
            color_discrete_map={
                'Champions': '#2E7D32',
                'Loyal': '#4CAF50',
                'Potential': '#FFC107',
                'At Risk': '#FF5722',
                'Needs Attention': '#9E9E9E'
            },
            title='Customer Segment Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_step_4_recommendations():
    """Step 3: AI Recommendations"""
    st.markdown("<h1 class='main-header'>🎁 AI Reward Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Personalized offers for each customer segment</p>", unsafe_allow_html=True)
    
    if 'df_analyzed' not in st.session_state:
        st.warning("Please complete AI Analysis first")
        return
    
    df = st.session_state.df_analyzed
    
    # Generate recommendations
    recommender = RewardRecommender()
    df_with_recs = recommender.batch_recommend(df)
    st.session_state.df_final = df_with_recs
    
    # Segment-wise recommendations
    st.markdown("### Segment-wise Reward Strategy")
    
    for segment in ['Champions', 'Loyal', 'Potential', 'At Risk', 'Needs Attention']:
        segment_df = df_with_recs[df_with_recs['segment'] == segment]
        if len(segment_df) == 0:
            continue
            
        with st.expander(f"**{segment}** ({len(segment_df)} customers)", expanded=(segment == 'At Risk')):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_cols = ['customer_id', 'name', 'eli_score', 'churn_probability', 
                               'recommended_reward', 'expected_lift']
                st.dataframe(
                    segment_df[display_cols].head(10).style.format({
                        'eli_score': '{:.1f}',
                        'churn_probability': '{:.1f}%'
                    }),
                    use_container_width=True
                )
            
            with col2:
                avg_eli = segment_df['eli_score'].mean()
                avg_churn = segment_df['churn_probability'].mean()
                st.metric("Avg ELI Score", f"{avg_eli:.1f}")
                st.metric("Avg Churn Risk", f"{avg_churn:.1f}%")
                st.metric("Customers", len(segment_df))
    
    if st.button("✨ Generate AI Offers →", type="primary", use_container_width=True):
        st.session_state.demo_step = 5
        st.rerun()


def render_step_5_ai_offers():
    """Step 4: AI-Generated Personalized Offers"""
    st.markdown("<h1 class='main-header'>✨ AI-Powered Personalized Offers</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Claude/OpenAI generates unique messages for each customer</p>", unsafe_allow_html=True)
    
    if 'df_final' not in st.session_state:
        st.warning("Please complete previous steps first")
        return
    
    df = st.session_state.df_final
    
    # API Key input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Configure AI Provider")
        
        provider = st.radio(
            "Select AI Provider",
            ["Claude (Anthropic)", "OpenAI GPT", "Demo Mode (No API)"],
            horizontal=True
        )
        
        if provider != "Demo Mode (No API)":
            api_key = st.text_input(
                "API Key",
                type="password",
                placeholder="Enter your API key...",
                help="Your API key is not stored and only used for this session"
            )
        else:
            api_key = None
        
        st.markdown("### Select Channel")
        channel = st.selectbox(
            "Message Channel",
            ["push", "whatsapp", "sms", "email"],
            format_func=lambda x: {"push": "📱 Push Notification", "whatsapp": "💬 WhatsApp", 
                                   "sms": "📝 SMS", "email": "📧 Email"}[x]
        )
        
        st.markdown("### Select Customers for Demo")
        
        # Let user pick segment to generate offers for
        segment_choice = st.selectbox(
            "Customer Segment",
            ["At Risk", "Champions", "Loyal", "Potential", "Needs Attention"]
        )
        
        num_customers = st.slider("Number of customers", 1, 10, 5)
        
        segment_df = df[df['segment'] == segment_choice].head(num_customers)
        
        st.markdown(f"**Selected {len(segment_df)} {segment_choice} customers:**")
        st.dataframe(
            segment_df[['customer_id', 'name', 'city', 'preferred_category', 'eli_score', 'churn_probability', 'recommended_reward']].style.format({
                'eli_score': '{:.1f}',
                'churn_probability': '{:.1f}%'
            }),
            use_container_width=True
        )
    
    with col2:
        st.markdown("### How It Works")
        st.info("""
        **AI Offer Generation:**
        
        1. Customer profile is sent to AI
        2. AI considers:
           - Name & demographics
           - Purchase history
           - Preferred category
           - Churn risk level
           - Recommended reward
        3. AI generates personalized message
        4. Message is tailored for channel
        """)
        
        st.markdown("### Sample Prompt")
        with st.expander("View AI Prompt"):
            st.code("""
You are a marketing copywriter for 
StyleKart. Generate a personalized 
push notification for this customer:

- Name: Priya Sharma
- Segment: At Risk
- Preferred: Western Wear
- Last Purchase: 65 days ago
- Churn Risk: 72%

Reward: Win-Back Offer ₹500

Generate a short, engaging message 
with emoji and clear CTA.
            """, language="text")
    
    st.markdown("---")
    
    # Generate offers button
    if st.button("🤖 Generate AI Personalized Offers", type="primary", use_container_width=True):
        
        # Initialize generator
        if provider == "Claude (Anthropic)":
            generator = AIOfferGenerator(provider="claude", api_key=api_key)
        elif provider == "OpenAI GPT":
            generator = AIOfferGenerator(provider="openai", api_key=api_key)
        else:
            generator = AIOfferGenerator(provider="fallback")
        
        st.markdown("### 🎯 Generated Personalized Offers")
        
        generated_offers = []
        
        progress = st.progress(0)
        
        for idx, (_, row) in enumerate(segment_df.iterrows()):
            customer = row.to_dict()
            reward = {
                'recommended_reward': row.get('recommended_reward', 'Special Offer'),
                'reward_value': row.get('reward_value', '₹500'),
                'expected_lift': row.get('expected_lift', '+25%')
            }
            
            with st.spinner(f"Generating offer for {row['name']}..."):
                offer_message = generator.generate_offer(customer, reward, channel)
                time.sleep(0.3)  # Small delay for visual effect
            
            generated_offers.append({
                'customer': row['name'],
                'segment': row['segment'],
                'message': offer_message
            })
            
            progress.progress((idx + 1) / len(segment_df))
        
        # Display generated offers
        st.session_state.generated_offers = generated_offers
        
        for offer in generated_offers:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"**{offer['customer']}**")
                    st.caption(f"Segment: {offer['segment']}")
                with col2:
                    # Style based on channel
                    if channel == "push":
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    color: white; padding: 15px; border-radius: 10px; margin: 5px 0;">
                            <strong>📱 Push Notification</strong><br>
                            {offer['message']}
                        </div>
                        """, unsafe_allow_html=True)
                    elif channel == "whatsapp":
                        st.markdown(f"""
                        <div style="background: #DCF8C6; color: #000; padding: 15px; 
                                    border-radius: 10px; margin: 5px 0; border-left: 4px solid #25D366;">
                            <strong>💬 WhatsApp</strong><br>
                            {offer['message']}
                        </div>
                        """, unsafe_allow_html=True)
                    elif channel == "sms":
                        st.markdown(f"""
                        <div style="background: #f0f0f0; color: #333; padding: 15px; 
                                    border-radius: 10px; margin: 5px 0; border: 1px solid #ccc;">
                            <strong>📝 SMS</strong><br>
                            {offer['message']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # email
                        st.markdown(f"""
                        <div style="background: #fff; color: #333; padding: 15px; 
                                    border-radius: 10px; margin: 5px 0; border: 1px solid #ddd; 
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <strong>📧 Email</strong><br>
                            <pre style="white-space: pre-wrap; font-family: inherit;">{offer['message']}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("---")
        
        # Show provider status
        status = generator.get_provider_status()
        st.caption(f"Provider: {status['provider'].upper()} | Model: {status['model'] or 'Template-based'}")
        
        st.success(f"✅ Generated {len(generated_offers)} personalized offers!")
        
        # Show delivery flow
        st.markdown("---")
        st.markdown("### 🚀 Delivery Flow")
        
        vendor_config = st.session_state.get('vendor_config', {
            'marketing': 'CleverTap',
            'email': 'SendGrid',
            'sms': 'Twilio',
            'whatsapp': 'Gupshup'
        })
        
        channel_vendor = {
            'push': vendor_config.get('marketing', 'CleverTap'),
            'email': vendor_config.get('email', 'SendGrid'),
            'sms': vendor_config.get('sms', 'Twilio'),
            'whatsapp': vendor_config.get('whatsapp', 'Gupshup')
        }
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 20px;">
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 25px; border-radius: 10px;">
                    <strong>🧠 RewardPe AI</strong><br>
                    <small>Generated {len(generated_offers)} offers</small>
                </div>
                <div style="font-size: 24px;">→</div>
                <div style="background: #2196F3; color: white; padding: 15px 25px; border-radius: 10px;">
                    <strong>📤 {vendor_config.get('marketing', 'CleverTap')}</strong><br>
                    <small>Campaign Orchestration</small>
                </div>
                <div style="font-size: 24px;">→</div>
                <div style="background: #4CAF50; color: white; padding: 15px 25px; border-radius: 10px;">
                    <strong>📨 {channel_vendor[channel]}</strong><br>
                    <small>{channel.upper()} Delivery</small>
                </div>
                <div style="font-size: 24px;">→</div>
                <div style="background: #FF6B6B; color: white; padding: 15px 25px; border-radius: 10px;">
                    <strong>👥 Customers</strong><br>
                    <small>{len(generated_offers)} recipients</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"""
        **What happens next:**
        1. RewardPe pushes personalized offers to **{vendor_config.get('marketing', 'CleverTap')}**
        2. {vendor_config.get('marketing', 'CleverTap')} triggers the campaign via **{channel_vendor[channel]}**
        3. Customers receive personalized {channel} messages
        4. Engagement data flows back to RewardPe for optimization
        """)
    
    st.markdown("---")
    
    if st.button("📊 Continue to Dashboard →", type="primary", use_container_width=True):
        st.session_state.demo_step = 6
        st.rerun()


def render_step_6_dashboard():
    """Step 4: Executive Dashboard"""
    st.markdown("<h1 class='main-header'>📊 Executive Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>StyleKart Loyalty Health Overview</p>", unsafe_allow_html=True)
    
    if 'df_final' not in st.session_state:
        df = load_stylekart_data()
        predictor, _ = get_trained_model()
        churn_probs = predictor.predict_churn_probability(df)
        segmenter = CustomerSegmenter()
        df = segmenter.segment_customers(df, churn_probs)
        recommender = RewardRecommender()
        df = recommender.batch_recommend(df)
        st.session_state.df_final = df
    
    df = st.session_state.df_final
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    avg_eli = df['eli_score'].mean()
    high_risk = (df['churn_probability'] > 50).sum()
    high_risk_pct = high_risk / len(df) * 100
    total_revenue_at_risk = df[df['churn_probability'] > 50]['total_spend'].sum()
    
    col1.metric("Loyalty Health Score", f"{avg_eli:.0f}/100", "+5 vs last month")
    col2.metric("High Churn Risk", f"{high_risk} ({high_risk_pct:.1f}%)", "-12 vs last month", delta_color="inverse")
    col3.metric("Revenue at Risk", f"₹{total_revenue_at_risk/100000:.1f}L", "-₹2.3L protected")
    col4.metric("Predicted ROI", "4.2x", "Campaign effectiveness")
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        # Loyalty Health Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_eli,
            delta={'reference': 55, 'increasing': {'color': "green"}},
            title={'text': "Overall Loyalty Health"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 40], 'color': '#ffcdd2'},
                    {'range': [40, 70], 'color': '#fff9c4'},
                    {'range': [70, 100], 'color': '#c8e6c9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Segment Distribution
        segment_counts = df['segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        fig = px.bar(
            segment_counts, x='Segment', y='Count',
            color='Segment',
            color_discrete_map={
                'Champions': '#2E7D32',
                'Loyal': '#4CAF50',
                'Potential': '#FFC107',
                'At Risk': '#FF5722',
                'Needs Attention': '#9E9E9E'
            },
            title='Customer Segments'
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Second Row
    col1, col2 = st.columns(2)
    
    with col1:
        # ELI vs Churn scatter
        fig = px.scatter(
            df.sample(min(500, len(df))),
            x='eli_score', y='churn_probability',
            color='segment',
            color_discrete_map={
                'Champions': '#2E7D32',
                'Loyal': '#4CAF50',
                'Potential': '#FFC107',
                'At Risk': '#FF5722',
                'Needs Attention': '#9E9E9E'
            },
            title='ELI Score vs Churn Probability',
            labels={'eli_score': 'Emotional Loyalty Index', 'churn_probability': 'Churn Probability (%)'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by segment
        revenue_by_segment = df.groupby('segment')['total_spend'].sum().reset_index()
        revenue_by_segment.columns = ['Segment', 'Revenue']
        revenue_by_segment['Revenue'] = revenue_by_segment['Revenue'] / 100000  # Convert to Lakhs
        
        fig = px.pie(
            revenue_by_segment, values='Revenue', names='Segment',
            color='Segment',
            color_discrete_map={
                'Champions': '#2E7D32',
                'Loyal': '#4CAF50',
                'Potential': '#FFC107',
                'At Risk': '#FF5722',
                'Needs Attention': '#9E9E9E'
            },
            title='Revenue Distribution by Segment (₹ Lakhs)'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer Table
    st.markdown("### 🔍 Customer Details")
    
    search = st.text_input("Search by name or ID")
    segment_filter = st.multiselect("Filter by Segment", df['segment'].unique(), default=df['segment'].unique())
    
    filtered_df = df[df['segment'].isin(segment_filter)]
    if search:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search, case=False) |
            filtered_df['customer_id'].str.contains(search, case=False)
        ]
    
    display_cols = ['customer_id', 'name', 'city', 'segment', 'eli_score', 
                   'churn_probability', 'total_spend', 'recommended_reward', 'expected_lift']
    
    st.dataframe(
        filtered_df[display_cols].head(50).style.format({
            'eli_score': '{:.1f}',
            'churn_probability': '{:.1f}%',
            'total_spend': '₹{:,.0f}'
        }).background_gradient(subset=['eli_score'], cmap='Greens')
         .background_gradient(subset=['churn_probability'], cmap='Reds'),
        use_container_width=True,
        height=400
    )
    
    # ROI Summary
    st.markdown("---")
    st.markdown("### 💰 Projected Impact")
    
    col1, col2, col3 = st.columns(3)
    
    at_risk_revenue = df[df['segment'].isin(['At Risk', 'Needs Attention'])]['total_spend'].sum()
    
    col1.metric("Customers at Risk", f"{(df['segment'].isin(['At Risk', 'Needs Attention'])).sum()}")
    col2.metric("Revenue at Risk", f"₹{at_risk_revenue/100000:.1f} Lakhs")
    col3.metric("Projected Savings (32% retention)", f"₹{at_risk_revenue*0.32/100000:.1f} Lakhs")
    
    st.success("""
    🎉 **Demo Complete!** 
    
    RewardPe has analyzed 1,500 StyleKart customers and identified:
    - **{}** high-risk customers requiring immediate attention
    - **₹{:.1f} Lakhs** in revenue that can be protected
    - Personalized reward recommendations for each customer
    
    Ready to transform your loyalty program?
    """.format(high_risk, at_risk_revenue*0.32/100000))
    
    if st.button("🔄 Restart Demo"):
        st.session_state.demo_step = 0
        st.session_state.data_loaded = False
        st.session_state.model_trained = False
        st.rerun()


def render_free_explore():
    """Free exploration mode - not demo"""
    st.sidebar.markdown("---")
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "AI Engine", "AI Offer Generator", "Customer Explorer", "Campaign Builder", "ROI Calculator", "API Docs"]
    )
    
    df = load_stylekart_data()
    predictor, _ = get_trained_model()
    churn_probs = predictor.predict_churn_probability(df)
    segmenter = CustomerSegmenter()
    df = segmenter.segment_customers(df, churn_probs)
    recommender = RewardRecommender()
    df = recommender.batch_recommend(df)
    
    if menu == "Dashboard":
        st.session_state.df_final = df
        render_step_6_dashboard()
    
    elif menu == "AI Engine":
        st.markdown("## 🤖 AI Loyalty Engine")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Model Performance")
            metrics = st.session_state.get('model_metrics', {'accuracy': 0.89})
            st.metric("Model Accuracy", f"{metrics['accuracy']*100:.1f}%")
            
            # Feature importance
            importance = predictor.get_feature_importance()
            fig = px.bar(importance.head(10), x='importance', y='feature', orientation='h',
                        title='Top 10 Churn Predictors')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ELI Formula")
            st.latex(r'''
            ELI = 0.30 \times PurchaseFreq + 0.25 \times Engagement + 
            0.20 \times Sentiment + 0.15 \times BrandInteraction + 0.10 \times NPS
            ''')
            
            st.markdown("### Segment Definitions")
            st.markdown("""
            | Segment | ELI | Churn Risk |
            |---------|-----|------------|
            | Champions | ≥70 | <25% |
            | Loyal | ≥55 | <35% |
            | Potential | ≥40 | <50% |
            | At Risk | Any | ≥50% |
            | Needs Attention | <40 | <50% |
            """)
    
    elif menu == "AI Offer Generator":
        st.markdown("## ✨ AI Offer Generator")
        st.markdown("Generate personalized marketing messages using Claude or OpenAI")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            provider = st.radio("AI Provider", ["Demo Mode (No API)", "Claude (Anthropic)", "OpenAI GPT"], horizontal=True)
            
            if provider != "Demo Mode (No API)":
                api_key = st.text_input("API Key", type="password")
            else:
                api_key = None
            
            channel = st.selectbox("Channel", ["push", "whatsapp", "sms", "email"])
            customer_id = st.selectbox("Select Customer", df['customer_id'].tolist())
            
            customer = df[df['customer_id'] == customer_id].iloc[0]
            
            st.markdown("**Customer Profile:**")
            st.write(f"Name: {customer['name']} | Segment: {customer['segment']} | Churn Risk: {customer['churn_probability']:.1f}%")
            
            if st.button("🤖 Generate Personalized Offer", type="primary"):
                if provider == "Claude (Anthropic)":
                    generator = AIOfferGenerator(provider="claude", api_key=api_key)
                elif provider == "OpenAI GPT":
                    generator = AIOfferGenerator(provider="openai", api_key=api_key)
                else:
                    generator = AIOfferGenerator(provider="fallback")
                
                reward = {
                    'recommended_reward': customer.get('recommended_reward', 'Special Offer'),
                    'reward_value': customer.get('reward_value', '₹500'),
                    'expected_lift': customer.get('expected_lift', '+25%')
                }
                
                with st.spinner("Generating..."):
                    offer = generator.generate_offer(customer.to_dict(), reward, channel)
                
                st.markdown("### Generated Message:")
                st.success(offer)
                
                status = generator.get_provider_status()
                st.caption(f"Provider: {status['provider']} | Model: {status['model'] or 'Template'}")
        
        with col2:
            st.markdown("### About")
            st.info("""
            The AI considers:
            - Customer name
            - Purchase history
            - Preferred category
            - Churn risk level
            - Segment type
            - Recommended reward
            
            Messages are tailored for each channel format.
            """)
    
    elif menu == "Customer Explorer":
        st.markdown("## 🔍 Customer Explorer")
        
        customer_id = st.selectbox("Select Customer", df['customer_id'].tolist())
        customer = df[df['customer_id'] == customer_id].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Profile")
            st.write(f"**Name:** {customer['name']}")
            st.write(f"**City:** {customer['city']}")
            st.write(f"**Age:** {customer['age']}")
            st.write(f"**Member Since:** {customer['registration_date']}")
        
        with col2:
            st.markdown("### Metrics")
            st.metric("ELI Score", f"{customer['eli_score']:.1f}")
            st.metric("Churn Risk", f"{customer['churn_probability']:.1f}%")
            st.metric("Total Spend", f"₹{customer['total_spend']:,}")
            st.metric("Segment", customer['segment'])
        
        with col3:
            st.markdown("### Recommendation")
            st.success(f"**{customer['recommended_reward']}**")
            st.write(f"Expected Lift: {customer['expected_lift']}")
            st.write(f"Personalization: {customer['personalization']}")
    
    elif menu == "Campaign Builder":
        st.markdown("## 🎯 Campaign Builder")
        
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input("Campaign Name", "StyleKart Summer Win-Back")
            target_segment = st.multiselect("Target Segments", df['segment'].unique(), default=['At Risk'])
            reward_type = st.selectbox("Reward Type", ["Discount", "Cashback", "Free Shipping", "Gift Card"])
            reward_value = st.slider("Reward Value (₹)", 100, 1000, 300)
        
        with col2:
            channel = st.multiselect("Channels", ["Email", "SMS", "Push", "WhatsApp"], default=["Email", "Push"])
            schedule = st.date_input("Launch Date")
            
            target_count = df[df['segment'].isin(target_segment)].shape[0]
            st.metric("Target Audience", f"{target_count:,} customers")
            
            if st.button("🚀 Launch Campaign", type="primary"):
                st.success(f"Campaign '{campaign_name}' scheduled for {schedule}!")
                st.balloons()
    
    elif menu == "ROI Calculator":
        st.markdown("## 💰 ROI Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customers = st.number_input("Total Customers", value=len(df))
            current_churn = st.slider("Current Churn Rate (%)", 5, 50, 25)
            avg_ltv = st.number_input("Avg Customer LTV (₹)", value=int(df['total_spend'].mean()))
        
        with col2:
            churn_reduction = 32  # RewardPe's claimed reduction
            customers_saved = int(customers * (current_churn/100) * (churn_reduction/100))
            revenue_saved = customers_saved * avg_ltv
            
            st.metric("Customers Saved Annually", f"{customers_saved:,}")
            st.metric("Revenue Protected", f"₹{revenue_saved/100000:.1f} Lakhs")
            st.metric("ROI (assuming ₹5L platform cost)", f"{revenue_saved/500000:.1f}x")
    
    elif menu == "API Docs":
        st.markdown("## 📚 API Documentation")
        
        st.markdown("### Authentication")
        st.code("""
curl -X POST https://api.rewardpe.com/v1/auth \\
  -H "Content-Type: application/json" \\
  -d '{"api_key": "sk_live_stylekart_xxx"}'
        """, language="bash")
        
        st.markdown("### Get Customer Insights")
        st.code("""
curl https://api.rewardpe.com/v1/customers/SK000001/insights \\
  -H "Authorization: Bearer {token}"
  
# Response
{
  "customer_id": "SK000001",
  "eli_score": 78.5,
  "churn_probability": 12.3,
  "segment": "Champions",
  "recommended_reward": {
    "type": "VIP Early Access",
    "expected_lift": "+8%"
  }
}
        """, language="json")


def main():
    demo_mode = render_sidebar()
    
    if demo_mode:
        if st.session_state.demo_step == 0:
            render_step_0_integration()
        elif st.session_state.demo_step == 1:
            render_step_1_vendor_config()
        elif st.session_state.demo_step == 2:
            render_step_2_data_sync()
        elif st.session_state.demo_step == 3:
            render_step_3_ai_analysis()
        elif st.session_state.demo_step == 4:
            render_step_4_recommendations()
        elif st.session_state.demo_step == 5:
            render_step_5_ai_offers()
        elif st.session_state.demo_step == 6:
            render_step_6_dashboard()
    else:
        render_free_explore()


if __name__ == "__main__":
    main()
