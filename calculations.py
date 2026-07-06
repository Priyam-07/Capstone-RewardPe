import pandas as pd
import numpy as np

def calculate_eli(row):
    """Calculate Emotional Loyalty Index"""
    eli = (0.35 * row['purchase_frequency'] / 12 * 100 +
           0.25 * row['engagement_score'] +
           0.20 * row['sentiment_score'] +
           0.20 * row['brand_interaction'])
    return min(100, eli)

def predict_churn(row):
    """Predict churn probability"""
    risk = (row['last_purchase_days'] * 0.4 +
            (100 - row['engagement_score']) * 0.3 +
            (100 - row['sentiment_score']) * 0.3)
    return min(100, max(0, risk))

def segment_customer(eli, churn_prob):
    """Segment customer based on ELI and churn"""
    if eli >= 70 and churn_prob < 30:
        return "Loyal"
    elif churn_prob >= 50:
        return "At Risk"
    else:
        return "Dormant"

def recommend_reward(segment, preference):
    """Recommend reward based on segment"""
    rewards = {
        "Loyal": "Early Access Offer",
        "At Risk": f"Cashback ₹200",
        "Dormant": "Surprise Bonus ₹150"
    }
    return rewards.get(segment, "Standard Reward")
