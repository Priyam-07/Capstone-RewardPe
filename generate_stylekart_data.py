"""
StyleKart - Synthetic Customer Data Generator
Generates 1,500 realistic fashion e-commerce customers for RewardPe demo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)

# Indian names database
first_names_male = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan', 'Krishna', 'Ishaan',
                    'Shaurya', 'Atharva', 'Advik', 'Pranav', 'Advaith', 'Aryan', 'Dhruv', 'Kabir', 'Ritvik', 'Aarush',
                    'Karthik', 'Darsh', 'Veer', 'Yash', 'Arnav', 'Aakash', 'Rohan', 'Tanish', 'Laksh', 'Rudra',
                    'Harsh', 'Dev', 'Nikhil', 'Rahul', 'Amit', 'Vikram', 'Suresh', 'Rajesh', 'Manish', 'Deepak']

first_names_female = ['Saanvi', 'Aanya', 'Aadhya', 'Aaradhya', 'Ananya', 'Pari', 'Anika', 'Navya', 'Angel', 'Diya',
                      'Myra', 'Sara', 'Iraa', 'Ahana', 'Anvi', 'Prisha', 'Riya', 'Isha', 'Khushi', 'Pooja',
                      'Sneha', 'Priya', 'Neha', 'Kavita', 'Meera', 'Anjali', 'Shruti', 'Divya', 'Nisha', 'Swati',
                      'Kritika', 'Tanvi', 'Simran', 'Komal', 'Pallavi', 'Rashmi', 'Sonal', 'Megha', 'Jyoti', 'Preeti']

last_names = ['Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Patel', 'Shah', 'Mehta', 'Joshi', 'Agarwal',
              'Reddy', 'Nair', 'Iyer', 'Menon', 'Pillai', 'Rao', 'Desai', 'Kulkarni', 'Jain', 'Malhotra',
              'Kapoor', 'Khanna', 'Bhatia', 'Chopra', 'Bansal', 'Goel', 'Mittal', 'Saxena', 'Tiwari', 'Pandey']

cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
          'Chandigarh', 'Indore', 'Bhopal', 'Nagpur', 'Coimbatore', 'Kochi', 'Gurgaon', 'Noida', 'Surat', 'Vadodara']

preferred_categories = ['Western Wear', 'Ethnic Wear', 'Footwear', 'Accessories', 'Sportswear']

def generate_customer_id(index):
    return f"SK{str(index + 1).zfill(6)}"

def generate_name():
    gender = random.choice(['M', 'F'])
    if gender == 'M':
        first = random.choice(first_names_male)
    else:
        first = random.choice(first_names_female)
    last = random.choice(last_names)
    return f"{first} {last}", gender

def generate_email(name):
    clean_name = name.lower().replace(' ', '.')
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    return f"{clean_name}{random.randint(1, 99)}@{random.choice(domains)}"

def generate_phone():
    return f"+91-{random.randint(70000, 99999)}{random.randint(10000, 99999)}"


def generate_customer(index):
    name, gender = generate_name()
    
    # Determine customer behavior type (affects all metrics)
    behavior_type = np.random.choice(
        ['loyal', 'regular', 'occasional', 'at_risk', 'dormant'],
        p=[0.20, 0.35, 0.30, 0.10, 0.05]
    )
    
    age = int(np.random.normal(32, 10))
    age = max(18, min(65, age))
    account_age = random.randint(30, 730)
    
    if behavior_type == 'loyal':
        purchase_frequency = random.randint(8, 15)
        total_orders = random.randint(12, 40)
        avg_order_value = random.randint(2500, 8000)
        last_purchase_days = random.randint(1, 15)
        engagement_score = random.randint(75, 95)
        app_sessions_monthly = random.randint(15, 30)
        email_open_rate = random.uniform(0.4, 0.7)
        wishlist_items = random.randint(5, 20)
        reviews_written = random.randint(3, 15)
        referrals_made = random.randint(1, 5)
        support_tickets = random.randint(0, 2)
        returns_rate = random.uniform(0.02, 0.08)
        
    elif behavior_type == 'regular':
        purchase_frequency = random.randint(4, 7)
        total_orders = random.randint(6, 15)
        avg_order_value = random.randint(1500, 4000)
        last_purchase_days = random.randint(10, 35)
        engagement_score = random.randint(55, 74)
        app_sessions_monthly = random.randint(8, 15)
        email_open_rate = random.uniform(0.25, 0.45)
        wishlist_items = random.randint(2, 10)
        reviews_written = random.randint(1, 5)
        referrals_made = random.randint(0, 2)
        support_tickets = random.randint(0, 3)
        returns_rate = random.uniform(0.05, 0.12)
        
    elif behavior_type == 'occasional':
        purchase_frequency = random.randint(2, 4)
        total_orders = random.randint(2, 8)
        avg_order_value = random.randint(1000, 3000)
        last_purchase_days = random.randint(30, 60)
        engagement_score = random.randint(35, 54)
        app_sessions_monthly = random.randint(3, 8)
        email_open_rate = random.uniform(0.15, 0.30)
        wishlist_items = random.randint(0, 5)
        reviews_written = random.randint(0, 2)
        referrals_made = 0
        support_tickets = random.randint(0, 2)
        returns_rate = random.uniform(0.08, 0.15)
        
    elif behavior_type == 'at_risk':
        purchase_frequency = random.randint(1, 3)
        total_orders = random.randint(3, 10)
        avg_order_value = random.randint(1200, 3500)
        last_purchase_days = random.randint(45, 90)
        engagement_score = random.randint(20, 40)
        app_sessions_monthly = random.randint(1, 4)
        email_open_rate = random.uniform(0.05, 0.18)
        wishlist_items = random.randint(0, 3)
        reviews_written = random.randint(0, 2)
        referrals_made = 0
        support_tickets = random.randint(1, 5)
        returns_rate = random.uniform(0.15, 0.25)
        
    else:  # dormant
        purchase_frequency = random.randint(0, 1)
        total_orders = random.randint(1, 4)
        avg_order_value = random.randint(800, 2500)
        last_purchase_days = random.randint(90, 180)
        engagement_score = random.randint(5, 20)
        app_sessions_monthly = random.randint(0, 2)
        email_open_rate = random.uniform(0.0, 0.10)
        wishlist_items = random.randint(0, 2)
        reviews_written = random.randint(0, 1)
        referrals_made = 0
        support_tickets = random.randint(0, 3)
        returns_rate = random.uniform(0.10, 0.20)
    
    total_spend = total_orders * avg_order_value
    base_sentiment = 70 - (support_tickets * 8) - (returns_rate * 100) + (reviews_written * 3)
    sentiment_score = max(10, min(95, base_sentiment + random.randint(-10, 10)))
    brand_interaction = min(100, (app_sessions_monthly * 2) + (wishlist_items * 3) + (reviews_written * 5) + (referrals_made * 10))
    
    if behavior_type == 'loyal': nps = random.randint(8, 10)
    elif behavior_type == 'regular': nps = random.randint(6, 9)
    elif behavior_type == 'occasional': nps = random.randint(5, 8)
    elif behavior_type == 'at_risk': nps = random.randint(3, 6)
    else: nps = random.randint(1, 5)
    
    pref_category = random.choice(preferred_categories)
    reward_pref = random.choice(['Early Access', 'Exclusive Collections', 'Free Shipping', 'Cashback']) if behavior_type in ['loyal', 'regular'] else random.choice(['Discount', 'Cashback', 'Free Shipping', 'Gift Card'])
    
    reg_date = datetime.now() - timedelta(days=account_age)
    last_purchase_date = datetime.now() - timedelta(days=last_purchase_days)
    
    return {
        'customer_id': generate_customer_id(index),
        'name': name, 'email': generate_email(name), 'phone': generate_phone(),
        'gender': gender, 'age': age, 'city': random.choice(cities),
        'registration_date': reg_date.strftime('%Y-%m-%d'),
        'account_age_days': account_age, 'total_orders': total_orders,
        'total_spend': total_spend, 'avg_order_value': avg_order_value,
        'purchase_frequency': purchase_frequency, 'last_purchase_days': last_purchase_days,
        'last_purchase_date': last_purchase_date.strftime('%Y-%m-%d'),
        'app_sessions_monthly': app_sessions_monthly,
        'email_open_rate': round(email_open_rate, 2),
        'wishlist_items': wishlist_items,
        'cart_abandonment_rate': round(random.uniform(0.2, 0.7), 2),
        'reviews_written': reviews_written,
        'avg_rating_given': round(random.uniform(3.5, 5.0), 1) if reviews_written > 0 else None,
        'referrals_made': referrals_made, 'support_tickets': support_tickets,
        'returns_count': int(total_orders * returns_rate),
        'returns_rate': round(returns_rate, 2),
        'preferred_category': pref_category,
        'preferred_payment': random.choice(['UPI', 'Credit Card', 'Debit Card', 'COD', 'Wallet']),
        'engagement_score': engagement_score, 'sentiment_score': int(sentiment_score),
        'brand_interaction': int(brand_interaction), 'nps_score': nps,
        'reward_preference': reward_pref, 'behavior_type': behavior_type
    }

def main():
    print("Generating 1,500 StyleKart customers...")
    customers = [generate_customer(i) for i in range(1500)]
    df = pd.DataFrame(customers)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'stylekart_customers.csv')
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")
    
    print("\n=== StyleKart Customer Data Summary ===")
    print(f"Total Customers: {len(df)}")
    print(f"\nBehavior Distribution:\n{df['behavior_type'].value_counts()}")
    print(f"\nAvg Order Value: ₹{df['avg_order_value'].mean():,.0f}")
    print(f"Avg Total Spend: ₹{df['total_spend'].mean():,.0f}")
    return df

if __name__ == "__main__":
    main()
