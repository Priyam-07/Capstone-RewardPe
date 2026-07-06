import streamlit as st

def render_insights(insights):
    st.title("🧠 AI Loyalty Insights")
    
    st.subheader("Top Insights")
    for insight in insights:
        st.info(f"💡 {insight}")
    
    st.subheader("Suggested Actions")
    st.success("🚀 Launch 'Surprise Bonus' campaign for At-Risk customers")
    st.success("📧 Send personalized emails to Dormant segment")
    st.success("🎁 Offer early access to Loyal customers")
