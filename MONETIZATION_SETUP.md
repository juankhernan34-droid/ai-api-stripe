# 🚀 Complete Monetization Setup Guide

Step-by-step guide to start earning money with your AI API.

## Phase 1: Payment Provider Setup (30 mins)

### A. Stripe Setup

1. **Create Account**
   - Go to https://stripe.com
   - Sign up (Canada-friendly ✅)
   - Verify email

2. **Get API Keys**
   - Dashboard → Developers → API Keys
   - Copy "Secret Key" (sk_test_...)
   - Copy "Publishable Key" (pk_test_...)

3. **Create Products & Prices**
   ```
   Product 1: "AI API Starter"
   - Price: $4.99/month
   - Copy Price ID (price_...)
   
   Product 2: "AI API Pro"
   - Price: $14.99/month
   - Copy Price ID (price_...)
   ```

4. **Update .env**
   ```env
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
   STRIPE_STARTER_PRICE_ID=price_...
   STRIPE_PRO_PRICE_ID=price_...
   ```

### B. PayPal Setup

1. **Create Account**
   - Go to https://developer.paypal.com
   - Sign up (Canada-friendly ✅)
   - Accept business agreement

2. **Get Sandbox Credentials** (for testing)
   - Go to Apps & Credentials → Sandbox
   - Find your app
   - Copy "Client ID"
   - Copy "Secret"

3. **Update .env**
   ```env
   PAYPAL_CLIENT_ID=your_sandbox_client_id
   PAYPAL_CLIENT_SECRET=your_sandbox_secret
   PAYPAL_MODE=sandbox
   PAYPAL_ONE_TIME_PRICE=5.00
   ```

### C. Hugging Face Setup

1. **Get Token**
   - Go to https://huggingface.co/settings/tokens
   - Create new token
   - Copy token

2. **Update .env**
   ```env
   HF_TOKEN=your_hf_token_here
   ```

---

## Phase 2: Test Everything Locally (30 mins)

### Test Backend API

```bash
# 1. Navigate to backend
cd ai-api-stripe

# 2. Create .env with credentials from Phase 1
cp .env.example .env
# (Add your actual keys)

# 3. Install & Run
pip install -r requirements.txt
python app.py
```

**Test endpoints in browser or Postman:**

```
GET http://localhost:7860/
GET http://localhost:7860/pricing
GET http://localhost:7860/paypal/pricing

POST http://localhost:7860/api/generate
Body: {"prompt": "Hello"}

GET http://localhost:7860/health
```

### Test Mobile App

```bash
# 1. Navigate to mobile
cd ai-api-mobile

# 2. Create .env
cp .env.example .env

# 3. Update with API URL
EXPO_PUBLIC_API_URL=http://localhost:7860
EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
EXPO_PUBLIC_PAYPAL_CLIENT_ID=...

# 4. Install & Run
npm install
npm start

# Open on web:
# Press 'w' in terminal
```

**Test in browser:**
- Generate text in Home tab
- Check payment plans in Payment tab
- Click payment buttons (opens URLs)

---

## Phase 3: Deploy Backend (15 mins)

### Deploy to Hugging Face Spaces

1. **Push to GitHub** (already done ✅)
   ```bash
   cd ai-api-stripe
   git add .
   git commit -m "Production ready"
   git push origin main
   ```

2. **Create Hugging Face Space**
   - Go to https://huggingface.co/new-space
   - Owner: Your username
   - Space name: `ai-api-stripe`
   - License: MIT
   - Space SDK: Docker
   - Create Space

3. **Connect GitHub Repository**
   - In Space settings → Repository
   - Connect your GitHub repo
   - Auto-deploy enabled

4. **Add Secrets** (in Space settings)
   ```
   HF_TOKEN: your_token
   STRIPE_SECRET_KEY: sk_live_...
   PAYPAL_CLIENT_ID: live_id
   PAYPAL_CLIENT_SECRET: live_secret
   PAYPAL_MODE: live
   ```

5. **Space will auto-deploy!**
   - Get public URL: `https://huggingface.co/spaces/your-username/ai-api-stripe`

---

## Phase 4: Deploy Mobile App (20 mins)

### Option A: Web Deployment (Easiest)

```bash
cd ai-api-mobile
npm run web

# Share the URL with customers
```

### Option B: App Store Deployment (Requires $)

1. **iOS App Store** ($99/year)
   ```bash
   expo build:ios
   # Follow prompts
   # Wait for build
   # Upload to App Store Connect
   ```

2. **Google Play** ($25 one-time)
   ```bash
   expo build:android --type app-bundle
   # Upload to Google Play Console
   ```

3. **Timeline:** 1-2 weeks for app store review

---

## Phase 5: Switch to Live Payment Keys (IMPORTANT!)

### ⚠️ DO NOT SKIP THIS - You won't earn money without this!

**Stripe Live Keys:**
1. Go to https://dashboard.stripe.com/apikeys
2. Toggle "View test data" OFF
3. Copy live keys (start with `sk_live_`)
4. Update in Hugging Face Space secrets

**PayPal Live Keys:**
1. Go to https://developer.paypal.com/dashboard/
2. Switch from "Sandbox" to "Live"
3. Copy live credentials
4. Update `PAYPAL_MODE=live`
5. Update in Hugging Face Space secrets

---

## Phase 6: Monitor & Earn 💰

### Check Payments

**Stripe Dashboard:**
- https://dashboard.stripe.com/payments
- See all transactions
- Monitor subscription status
- Check payouts to your bank

**PayPal Dashboard:**
- https://www.paypal.com/business
- Monitor incoming payments
- Set up automatic payouts

### Track Revenue

```
Monthly Recurring Revenue (MRR):
- Starter subscribers × $4.99
- Pro subscribers × $14.99
- PayPal one-time = $5.00 each
```

---

## Phase 7: Marketing Your App 🎯

### Share Your App

1. **Web URL** (from Hugging Face Spaces)
   - Share on social media
   - Add to your portfolio
   - Get customers to try it

2. **App Store Links** (after deployment)
   - Share iOS link
   - Share Android link
   - Get app store reviews

3. **Content Marketing**
   - Blog about your AI API
   - Show demo videos
   - Highlight payment flexibility

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Stripe key invalid | Check you're using correct environment (test vs live) |
| PayPal payment fails | Ensure PAYPAL_MODE matches credentials |
| API not responding | Check HF Space logs for errors |
| Mobile app can't reach API | Verify API_URL in .env is correct |
| Payment button does nothing | Check browser console for errors |

---

## Success Checklist ✅

- [ ] Created Stripe account
- [ ] Created PayPal account  
- [ ] Got all API keys
- [ ] Updated .env files
- [ ] Tested backend locally
- [ ] Tested mobile app locally
- [ ] Deployed to Hugging Face Spaces
- [ ] Switched to LIVE payment keys
- [ ] Verified first test payment
- [ ] Shared app with first customer
- [ ] Made your first $5! 🎉

---

## Support

- **Stripe Support:** https://support.stripe.com/
- **PayPal Support:** https://developer.paypal.com/
- **Hugging Face:** https://huggingface.co/docs/hub
- **Expo:** https://docs.expo.dev/

---

**You're 3 steps away from your first payment!**
1. Get credentials
2. Deploy
3. Share
4. Profit 💰
