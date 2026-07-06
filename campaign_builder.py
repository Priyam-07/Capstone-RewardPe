import streamlit as st

def render_campaign_builder():
    st.title("🎯 Create Reward Campaign")
    
    with st.form("campaign_form"):
        name = st.text_input("Campaign Name", "Summer Loyalty Boost")
        segment = st.selectbox("Target Segment", ["At-Risk Customers", "Loyal Customers", "Dormant Customers"])
        trigger = st.selectbox("Trigger Event", ["Purchase inactivity 14 days", "Birthday", "First Purchase", "Milestone"])
        reward_type = st.selectbox("Reward Type", ["Cashback ₹200", "Gift Card ₹500", "Discount 20%", "Early Access"])
        channel = st.multiselect("Channel", ["App Notification", "Email", "SMS", "WhatsApp"], default=["App Notification"])
        
        col1, col2 = st.columns(2)
        preview = col1.form_submit_button("Preview Campaign")
        launch = col2.form_submit_button("🚀 Launch", type="primary")
        
        if launch:
            st.success(f"Campaign '{name}' launched successfully!")
            st.balloons()
