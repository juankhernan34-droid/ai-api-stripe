# 💳 Payment Testing Guide

How to test payments BEFORE going live and charging real customers.

## Stripe Test Payments

### Test Card Numbers

**Successful Payment:**
```
Card Number: 4242 4242 4242 4242
Expiry: 12/25
CVC: 123
```

**Declined Payment:**
```
Card Number: 4000 0000 0000 0002
Expiry: 12/25
CVC: 123
```

**Requires Authentication:**
```
Card Number: 4000 0025 0000 3155
Expiry: 12/25
CVC: 123
```

### How to Test

1. Make sure you're in **Stripe Test Mode**
   - Dashboard shows "Test" label
   - Keys start with `pk_test_` and `sk_test_`

2. Create a checkout session:
   ```bash
   curl -X POST http://localhost:7860/checkout \
     -H "Content-Type: application/json" \
     -d '{"plan": "starter"}'
   ```

3. Go to Stripe checkout URL
4. Enter test card number
5. Complete payment
6. Check Stripe dashboard for transaction

---

## PayPal Sandbox Testing

### Test Accounts (Auto-created)

**Buyer Account:**
```
Email: sb-xxxxx@personal.example.com
Password: Check your PayPal sandbox
```

**Business Account:**
```
Email: sb-xxxxx@business.example.com
Password: Check your PayPal sandbox
```

### How to Test

1. Make sure `PAYPAL_MODE=sandbox`

2. Create payment:
   ```bash
   curl -X POST http://localhost:7860/paypal/payment \
     -H "Content-Type: application/json" \
     -d '{
       "return_url": "http://localhost:7860/success",
       "cancel_url": "http://localhost:7860/cancel"
     }'
   ```

3. Go to approval URL
4. Log in with sandbox buyer account
5. Approve payment
6. Confirm payment
7. Check PayPal sandbox for transaction

---

## Mobile App Testing

### Test on Web First

```bash
cd ai-api-mobile
npm start
# Press 'w'
```

### Test Payments in Mobile App

1. **Test AI Generation**
   - Enter prompt
   - Click Generate
   - Should get response from your API

2. **Test Stripe Payment**
   - Go to Payment tab
   - Click "Subscribe Now"
   - Opens Stripe checkout
   - Use test card 4242 4242 4242 4242

3. **Test PayPal Payment**
   - Go to Payment tab
   - Click "Pay with PayPal"
   - Opens PayPal approval
   - Log in with sandbox account
   - Approve payment

---

## Checklist Before Going Live

- [ ] Test Stripe payment with test card
- [ ] Verify transaction in Stripe dashboard
- [ ] Test PayPal payment with sandbox
- [ ] Verify payment in PayPal sandbox
- [ ] Test on mobile device (iOS simulator or Android emulator)
- [ ] Test payment on deployed Hugging Face Space
- [ ] Verify error handling (invalid card, etc.)
- [ ] Test refund process (Stripe dashboard)
- [ ] Check payment receipts sent to customer

---

## Going Live Safely

### Step 1: Get Live Keys

**Stripe:**
1. Dashboard → Developers → API Keys
2. Toggle "View test data" OFF
3. Copy live keys (sk_live_...)

**PayPal:**
1. Dashboard → Sandbox/Live toggle
2. Switch to Live
3. Copy live credentials

### Step 2: Deploy Live Keys

**Option A: Local Testing**
```bash
# Update .env
STRIPE_SECRET_KEY=sk_live_...
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=live_id

# Test locally
python app.py

# Make test payment with real card
```

**Option B: Production Deploy**
```bash
# Update Hugging Face Space secrets
STRIPE_SECRET_KEY=sk_live_...
PAYPAL_MODE=live

# Space auto-redeploys
# Wait 2-3 minutes

# Test payment
```

### Step 3: Verify First Payment

1. Make a real payment with your personal card
2. Check Stripe/PayPal dashboard
3. Verify funds transferred to your bank
4. Process refund to verify refund flow

### Step 4: Monitor

- **Daily:** Check for failed payments
- **Weekly:** Review transaction history
- **Monthly:** Analyze revenue trends

---

## Common Issues & Fixes

### Payment Fails Immediately
**Cause:** Invalid API keys
**Fix:** Double-check keys, ensure correct test/live mode

### Payment Succeeds but No Email Sent
**Cause:** Email provider not configured
**Fix:** Add email service (SendGrid, AWS SES, etc.)

### Customer Gets Charged but App Not Updated
**Cause:** Webhook not received
**Fix:** Set up webhook endpoints for payment confirmations

### Cannot Switch to Live Mode
**Cause:** Account not verified
**Fix:** Complete account verification with payment provider

---

## Next: Email Receipts

Add email receipts to increase trust:

```python
# In app.py after successful payment
import smtplib
from email.mime.text import MIMEText

def send_receipt(email, amount):
    # Send payment receipt
    pass
```

---

**You're now ready to accept real payments!** 💰
