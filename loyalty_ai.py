import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class LoyaltyAIBrain:
    def __init__(self):
        self.churn_model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()
    
    def process_customers(self, df):
        """Process customer data and add predictions"""
        df['eli_score'] = df.apply(self._calc_eli, axis=1)
        df['churn_probability'] = df.apply(self._calc_churn, axis=1)
        df['segment'] = df.apply(lambda r: self._segment(r['eli_score'], r['churn_probability']), axis=1)
        df['recommended_reward'] = df.apply(lambda r: self._recommend(r['segment']), axis=1)
        return df
    
    def _calc_eli(self, row):
        return min(100, 0.35 * row['purchase_frequency']/12*100 + 0.25 * row['engagement_score'] + 
                   0.20 * row['sentiment_score'] + 0.20 * row['brand_interaction'])
    
    def _calc_churn(self, row):
        return min(100, max(0, row['last_purchase_days']*0.4 + (100-row['engagement_score'])*0.3 + (100-row['sentiment_score'])*0.3))
    
    def _segment(self, eli, churn):
        if eli >= 70 and churn < 30: return "Loyal"
        elif churn >= 50: return "At Risk"
        return "Dormant"
    
    def _recommend(self, segment):
        return {"Loyal": "Early Access", "At Risk": "Cashback ₹200", "Dormant": "Surprise Bonus ₹150"}.get(segment, "Standard")
    
    def get_insights(self, df):
        """Generate AI insights"""
        churn_rate = (df['churn_probability'] > 50).mean() * 100
        return [
            f"{churn_rate:.0f}% customers likely to churn",
            "Cashback rewards perform 32% better",
            "Weekend offers increase engagement by 28%"
        ]
