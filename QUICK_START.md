# Quick Start Guide 🚀

## Local Testing (Easy Way)

### 1. Clone & Setup
```bash
git clone https://github.com/juankhernan34-droid/ai-api-stripe
cd ai-api-stripe
pip install -r requirements.txt
```

### 2. Create `.env` file (copy and paste)
```env
HF_USERNAME=klenz1984
HF_TOKEN=your_hf_token_here
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_STARTER_PRICE_ID=price_test_starter
STRIPE_PRO_PRICE_ID=price_test_pro
PAYPAL_CLIENT_ID=test_client_id
PAYPAL_CLIENT_SECRET=test_client_secret
PAYPAL_MODE=sandbox
PAYPAL_ONE_TIME_PRICE=5.00
```

### 3. Run It!
```bash
python app.py
```

Visit: **http://localhost:7860**

---

## API Endpoints

### 🤖 AI Generation
```bash
POST http://localhost:7860/api/generate
Content-Type: application/json

{
  "prompt": "What is artificial intelligence?"
}
```

### 💰 Stripe Subscription
```bash
POST http://localhost:7860/checkout
{
  "plan": "starter"
}
```

### 💳 PayPal One-Time Payment
```bash
POST http://localhost:7860/paypal/payment
{
  "return_url": "http://localhost:7860/success",
  "cancel_url": "http://localhost:7860/cancel"
}
```

### 📊 Pricing
```bash
GET http://localhost:7860/pricing
GET http://localhost:7860/paypal/pricing
```

### ✅ Health Check
```bash
GET http://localhost:7860/health
```

---

## Getting Real Credentials

### Hugging Face Token
1. Go to [huggingface.co](https://huggingface.co/)
2. Settings → Access Tokens → New token
3. Copy and paste into `.env`

### Stripe Keys (Testing)
1. Go to [stripe.com](https://stripe.com/)
2. Sign up → Dashboard → Developers → API Keys
3. Use test keys (start with `sk_test_`)

### PayPal Credentials (Testing)
1. Go to [developer.paypal.com](https://developer.paypal.com/)
2. Sign up → Sandbox → Apps & Credentials
3. Use sandbox credentials for testing
4. Set `PAYPAL_MODE=sandbox`

---

## Ready to Deploy?

Push to Hugging Face Spaces:
```bash
git push origin main
```

Your app will auto-deploy! 🎉

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `KeyError: 'HF_TOKEN'` | Create `.env` file with all variables |
| `PayPal error` | Make sure `PAYPAL_MODE=sandbox` for testing |
| Port already in use | Change port: `app.run(port=8000)` in app.py |

---

**Questions?** Check `app.py` for the full API documentation in docstrings.

Happy coding! 🎉
