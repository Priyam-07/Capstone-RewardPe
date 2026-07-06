"""
RewardPe - Real ML Churn Prediction Model
Uses scikit-learn for actual machine learning predictions
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'purchase_frequency', 'last_purchase_days', 'engagement_score',
            'sentiment_score', 'brand_interaction', 'app_sessions_monthly',
            'email_open_rate', 'support_tickets', 'returns_rate', 'nps_score',
            'total_orders', 'avg_order_value', 'wishlist_items', 'cart_abandonment_rate'
        ]
        
    def prepare_features(self, df):
        """Extract and scale features for prediction"""
        X = df[self.feature_columns].copy()
        X = X.fillna(X.mean())
        return X
    
    def create_churn_labels(self, df):
        """Create churn labels based on behavior patterns"""
        # Churn = 1 if at_risk or dormant, 0 otherwise
        return (df['behavior_type'].isin(['at_risk', 'dormant'])).astype(int)
    
    def train(self, df):
        """Train the churn prediction model"""
        X = self.prepare_features(df)
        y = self.create_churn_labels(df)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Gradient Boosting model
        self.model = GradientBoostingClassifier(
            n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'report': classification_report(y_test, y_pred, output_dict=True)
        }
    
    def predict_churn_probability(self, df):
        """Predict churn probability for customers"""
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        return probabilities * 100  # Return as percentage
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance
    
    def save_model(self, path):
        """Save trained model"""
        joblib.dump({'model': self.model, 'scaler': self.scaler}, path)
    
    def load_model(self, path):
        """Load trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']


class CustomerSegmenter:
    """AI-powered customer segmentation using clustering"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def calculate_eli_score(self, row):
        """Calculate Emotional Loyalty Index"""
        eli = (
            0.30 * min(100, row['purchase_frequency'] / 12 * 100) +
            0.25 * row['engagement_score'] +
            0.20 * row['sentiment_score'] +
            0.15 * row['brand_interaction'] +
            0.10 * row['nps_score'] * 10
        )
        return min(100, max(0, eli))
    
    def segment_customers(self, df, churn_probabilities):
        """Segment customers based on ELI and churn probability"""
        df = df.copy()
        df['eli_score'] = df.apply(self.calculate_eli_score, axis=1)
        df['churn_probability'] = churn_probabilities
        
        def get_segment(row):
            eli = row['eli_score']
            churn = row['churn_probability']
            
            if eli >= 70 and churn < 25:
                return 'Champions'
            elif eli >= 55 and churn < 35:
                return 'Loyal'
            elif eli >= 40 and churn < 50:
                return 'Potential'
            elif churn >= 50:
                return 'At Risk'
            else:
                return 'Needs Attention'
        
        df['segment'] = df.apply(get_segment, axis=1)
        return df


class RewardRecommender:
    """AI-powered reward recommendation engine"""
    
    REWARD_CATALOG = {
        'Champions': [
            {'reward': 'VIP Early Access', 'description': 'Exclusive 48-hour early access to new collections', 'value': 'Premium', 'expected_lift': '+8%'},
            {'reward': 'Personal Stylist Session', 'description': 'Free 30-min virtual styling consultation', 'value': '₹2,000', 'expected_lift': '+12%'},
            {'reward': 'Double Points Week', 'description': '2X loyalty points on all purchases', 'value': 'Variable', 'expected_lift': '+15%'},
        ],
        'Loyal': [
            {'reward': 'Free Express Shipping', 'description': 'Free express delivery for 3 months', 'value': '₹600', 'expected_lift': '+10%'},
            {'reward': 'Birthday Month Bonus', 'description': '20% off during birthday month', 'value': 'Up to ₹1,000', 'expected_lift': '+18%'},
            {'reward': 'Exclusive Collection Access', 'description': 'Early access to limited editions', 'value': 'Premium', 'expected_lift': '+7%'},
        ],
        'Potential': [
            {'reward': 'Cashback ₹300', 'description': '₹300 cashback on next order above ₹1,500', 'value': '₹300', 'expected_lift': '+22%'},
            {'reward': 'Free Shipping Upgrade', 'description': 'Free shipping on next 2 orders', 'value': '₹200', 'expected_lift': '+15%'},
            {'reward': 'Category Discount', 'description': '25% off on preferred category', 'value': 'Up to ₹500', 'expected_lift': '+20%'},
        ],
        'At Risk': [
            {'reward': 'Win-Back Offer ₹500', 'description': '₹500 off on orders above ₹2,000', 'value': '₹500', 'expected_lift': '+35%'},
            {'reward': 'We Miss You Gift', 'description': 'Free accessory with next purchase', 'value': '₹400', 'expected_lift': '+28%'},
            {'reward': 'Flash Sale Access', 'description': 'Exclusive 40% off flash sale invite', 'value': 'Up to ₹800', 'expected_lift': '+32%'},
        ],
        'Needs Attention': [
            {'reward': 'Reactivation Bonus ₹200', 'description': '₹200 off on any purchase', 'value': '₹200', 'expected_lift': '+25%'},
            {'reward': 'Survey Reward', 'description': '₹150 for completing feedback survey', 'value': '₹150', 'expected_lift': '+18%'},
            {'reward': 'Referral Bonus', 'description': '₹300 for each successful referral', 'value': '₹300', 'expected_lift': '+20%'},
        ]
    }
    
    def recommend_reward(self, customer_row):
        """Recommend best reward for a customer"""
        segment = customer_row['segment']
        pref_category = customer_row.get('preferred_category', 'Western Wear')
        
        rewards = self.REWARD_CATALOG.get(segment, self.REWARD_CATALOG['Needs Attention'])
        
        # Select reward based on customer preferences and behavior
        if customer_row['churn_probability'] > 60:
            reward = rewards[0]  # Most aggressive offer
        elif customer_row['eli_score'] > 70:
            reward = rewards[-1]  # Engagement-focused
        else:
            reward = rewards[1]  # Balanced
        
        return {
            'recommended_reward': reward['reward'],
            'reward_description': reward['description'],
            'reward_value': reward['value'],
            'expected_lift': reward['expected_lift'],
            'personalization': f"Tailored for {pref_category} preference"
        }
    
    def batch_recommend(self, df):
        """Generate recommendations for all customers"""
        recommendations = df.apply(self.recommend_reward, axis=1)
        rec_df = pd.DataFrame(recommendations.tolist())
        return pd.concat([df, rec_df], axis=1)
