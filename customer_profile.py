import streamlit as st

def render_customer_profile(df):
    st.title("👤 Customer Loyalty Profile")
    
    customer = st.selectbox("Select Customer", df['name'].tolist())
    row = df[df['name'] == customer].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Loyalty Score", f"{row['eli_score']:.0f}")
        st.metric("Churn Probability", f"{row['churn_probability']:.0f}%")
    with col2:
        st.metric("Segment", row['segment'])
        st.metric("Preferred Reward", row['reward_preference'])
    
    st.subheader("Recommended Reward")
    st.success(f"🎁 {row['recommended_reward']}")
