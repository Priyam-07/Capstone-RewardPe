# RewardPe SDK Integration Guide

## Quick Start for StyleKart Integration

### 1. Install SDK
```bash
npm install @rewardpe/sdk
# or
pip install rewardpe-sdk
```

### 2. Initialize
```javascript
import RewardPe from '@rewardpe/sdk';

const rewardpe = new RewardPe({
  apiKey: 'sk_live_stylekart_xxxxx',
  environment: 'production'
});
```

### 3. Sync Customers
```javascript
// Push customer data to RewardPe
await rewardpe.customers.sync({
  source: 'stylekart_db',
  batchSize: 1000
});
```

### 4. Get Recommendations
```javascript
const recommendation = await rewardpe.rewards.getRecommendation({
  customerId: 'SK000001'
});
```

## Webhook Events
- `customer.churn_risk_high` - Customer churn probability > 50%
- `reward.recommended` - New reward recommendation generated
- `campaign.triggered` - Automated campaign triggered
