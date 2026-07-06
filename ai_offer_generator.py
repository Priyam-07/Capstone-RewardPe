"""
AI-Powered Personalized Offer Generator
Uses OpenAI/Claude API to generate personalized marketing messages
"""

import os
from typing import Optional
import json

# Try importing AI libraries
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIOfferGenerator:
    """Generate personalized offers using Claude or OpenAI"""
    
    def __init__(self, provider: str = "auto", api_key: Optional[str] = None):
        """
        Initialize the AI offer generator
        
        Args:
            provider: "claude", "openai", or "auto" (tries claude first)
            api_key: API key (or set via environment variable)
        """
        self.provider = provider
        self.client = None
        self.model = None
        
        # Auto-detect provider
        if provider == "auto":
            if ANTHROPIC_AVAILABLE and (api_key or os.getenv("ANTHROPIC_API_KEY")):
                self.provider = "claude"
            elif OPENAI_AVAILABLE and (api_key or os.getenv("OPENAI_API_KEY")):
                self.provider = "openai"
            else:
                self.provider = "fallback"
        
        # Initialize client
        if self.provider == "claude" and ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-haiku-20240307"  # Fast and cost-effective
        elif self.provider == "openai" and OPENAI_AVAILABLE:
            self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-3.5-turbo"
    
    def _build_prompt(self, customer: dict, reward: dict, channel: str = "push") -> str:
        """Build the prompt for offer generation"""
        
        prompt = f"""You are a marketing copywriter for StyleKart, a trendy Indian fashion e-commerce brand. 
Generate a personalized {channel} notification message for this customer.

CUSTOMER PROFILE:
- Name: {customer.get('name', 'Customer')}
- Segment: {customer.get('segment', 'Regular')}
- Preferred Category: {customer.get('preferred_category', 'Fashion')}
- Last Purchase: {customer.get('last_purchase_days', 30)} days ago
- Loyalty Score: {customer.get('eli_score', 50):.0f}/100
- Churn Risk: {customer.get('churn_probability', 30):.0f}%
- Total Spend: ₹{customer.get('total_spend', 10000):,}
- City: {customer.get('city', 'India')}

REWARD TO OFFER:
- Type: {reward.get('recommended_reward', 'Special Offer')}
- Value: {reward.get('reward_value', 'Exclusive')}
- Expected Impact: {reward.get('expected_lift', '+15%')} engagement lift

GUIDELINES:
1. Keep it short (max 2 sentences for push, 3-4 for email)
2. Use the customer's first name
3. Reference their preferred category if relevant
4. Create urgency but don't be pushy
5. Match tone to segment (VIP for Champions, friendly for At Risk)
6. Include 1-2 relevant emojis
7. End with a clear call-to-action

Generate ONLY the message text, nothing else."""

        return prompt
    
    def generate_offer(self, customer: dict, reward: dict, channel: str = "push") -> str:
        """
        Generate a personalized offer message
        
        Args:
            customer: Customer data dictionary
            reward: Reward recommendation dictionary
            channel: "push", "sms", "email", or "whatsapp"
        
        Returns:
            Personalized offer message string
        """
        
        prompt = self._build_prompt(customer, reward, channel)
        
        if self.provider == "claude" and self.client:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                return self._fallback_offer(customer, reward, channel)
        
        elif self.provider == "openai" and self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return self._fallback_offer(customer, reward, channel)
        
        else:
            return self._fallback_offer(customer, reward, channel)
    
    def _fallback_offer(self, customer: dict, reward: dict, channel: str) -> str:
        """Fallback template-based offer when API is unavailable"""
        
        first_name = customer.get('name', 'there').split()[0]
        segment = customer.get('segment', 'Regular')
        category = customer.get('preferred_category', 'fashion')
        reward_type = reward.get('recommended_reward', 'special offer')
        reward_value = reward.get('reward_value', 'exclusive discount')
        
        templates = {
            'Champions': {
                'push': f"👑 {first_name}, you're a StyleKart VIP! Enjoy {reward_type} - {reward_value}. Shop now!",
                'email': f"Dear {first_name},\n\nAs one of our most valued customers, we're thrilled to offer you exclusive {reward_type}! Your loyalty means everything to us.\n\n🎁 Reward: {reward_value}\n\nShop your favorite {category} today!\n\nWith love,\nTeam StyleKart",
                'sms': f"Hi {first_name}! VIP Alert: {reward_type} ({reward_value}) waiting for you at StyleKart. Shop now!",
                'whatsapp': f"Hey {first_name}! 👑\n\nYou're one of our top customers! Here's an exclusive {reward_type} just for you.\n\n🎁 {reward_value}\n\nTap to shop your fave {category}! 👗"
            },
            'Loyal': {
                'push': f"💚 {first_name}, thank you for being loyal! Here's {reward_type} for you. Tap to claim!",
                'email': f"Hi {first_name},\n\nThank you for being a loyal StyleKart shopper! We've got something special for you.\n\n🎁 {reward_type}: {reward_value}\n\nExplore the latest in {category}!\n\nCheers,\nStyleKart",
                'sms': f"{first_name}, thanks for your loyalty! Claim your {reward_type} ({reward_value}) at StyleKart today!",
                'whatsapp': f"Hi {first_name}! 💚\n\nThanks for being awesome! Here's a little thank you:\n\n🎁 {reward_type} - {reward_value}\n\nCheck out new {category} arrivals! 🛍️"
            },
            'At Risk': {
                'push': f"💝 {first_name}, we miss you! Come back for {reward_type} - {reward_value}. Limited time!",
                'email': f"Hi {first_name},\n\nWe've missed you at StyleKart! It's been a while since your last visit, and we'd love to see you back.\n\nHere's a special welcome-back offer:\n🎁 {reward_type}: {reward_value}\n\nYour favorite {category} is waiting!\n\nWarmly,\nStyleKart",
                'sms': f"{first_name}, we miss you! 💝 Here's {reward_type} ({reward_value}) to welcome you back to StyleKart!",
                'whatsapp': f"Hey {first_name}! 💝\n\nLong time no see! We've got something special to bring you back:\n\n🎁 {reward_type}\n💰 {reward_value}\n\nYour {category} picks are waiting! Come back? 🙏"
            }
        }
        
        # Default template for other segments
        default = {
            'push': f"🎁 {first_name}, special offer alert! Get {reward_type} - {reward_value}. Shop now!",
            'email': f"Hi {first_name},\n\nGreat news! You've unlocked a special offer at StyleKart.\n\n🎁 {reward_type}: {reward_value}\n\nDiscover amazing {category} today!\n\nHappy Shopping,\nStyleKart",
            'sms': f"Hi {first_name}! Your {reward_type} ({reward_value}) is ready at StyleKart. Shop now!",
            'whatsapp': f"Hi {first_name}! 🎁\n\nYou've got a special offer waiting:\n\n{reward_type} - {reward_value}\n\nShop {category} now! 🛍️"
        }
        
        segment_templates = templates.get(segment, default)
        return segment_templates.get(channel, segment_templates['push'])
    
    def generate_batch_offers(self, customers_df, channel: str = "push", limit: int = 10):
        """Generate offers for multiple customers"""
        
        results = []
        for idx, row in customers_df.head(limit).iterrows():
            customer = row.to_dict()
            reward = {
                'recommended_reward': row.get('recommended_reward', 'Special Offer'),
                'reward_value': row.get('reward_value', 'Exclusive'),
                'expected_lift': row.get('expected_lift', '+15%')
            }
            
            offer = self.generate_offer(customer, reward, channel)
            results.append({
                'customer_id': row['customer_id'],
                'name': row['name'],
                'segment': row['segment'],
                'channel': channel,
                'personalized_message': offer
            })
        
        return results
    
    def get_provider_status(self) -> dict:
        """Get current provider status"""
        return {
            'provider': self.provider,
            'model': self.model,
            'api_connected': self.client is not None,
            'anthropic_available': ANTHROPIC_AVAILABLE,
            'openai_available': OPENAI_AVAILABLE
        }
