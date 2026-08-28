# AI API with Stripe Payment Integration

A Flask API that integrates Hugging Face AI models with Stripe for payment processing.

## Features

✨ **AI Generation**: Text generation using Hugging Face API
💳 **Stripe Integration**: Subscription billing with Starter and Pro plans
🚀 **Deployed on Hugging Face Spaces**: Easy deployment and scaling

## Pricing Plans

- **Starter**: $4.99/month - 5,000 requests/month
- **Pro**: $14.99/month - 50,000 requests/month

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/juankhernan34-droid/ai-api-stripe.git
cd ai-api-stripe
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add:
```
HF_USERNAME=klenz1984
HF_TOKEN=your_huggingface_token
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_STARTER_PRICE_ID=price_1U9FgZIcqdz5i1m1vYH1gvvL
STRIPE_PRO_PRICE_ID=price_1U9GpvIcqdz5i1m1pfGb9rXp
```

### 4. Run Locally
```bash
python app.py
```

API will be available at `http://localhost:7860`

## API Endpoints

### Health Check
```bash
GET /health
```

### Get Pricing
```bash
GET /pricing
```

### Generate Text
```bash
POST /api/generate
Content-Type: application/json

{
  "prompt": "Write a poem about AI"
}
```

### Create Checkout Session
```bash
POST /checkout
Content-Type: application/json

{
  "plan": "pro"
}
```

Response:
```json
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_test_..."
}
```

## Deploy to Hugging Face Spaces

1. Go to https://huggingface.co/spaces/new
2. Fill in:
   - **Space name**: `ai-api-stripe`
   - **License**: `MIT`
   - **Space SDK**: `Docker`
3. In **Files** tab, create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

4. Add secrets in **Settings** → **Repository secrets**:
   - `HF_TOKEN`
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PUBLISHABLE_KEY`
   - `STRIPE_STARTER_PRICE_ID`
   - `STRIPE_PRO_PRICE_ID`

## Testing

```bash
# Test health check
curl http://localhost:7860/health

# Test pricing
curl http://localhost:7860/pricing

# Test generation
curl -X POST http://localhost:7860/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello world"}'
```

## License

MIT