from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from square.client import Client
from square.api.payments_api import PaymentsApi
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Initialize Square
square_client = Client(
    access_token=os.getenv('SQUARE_ACCESS_TOKEN'),
    environment=os.getenv('SQUARE_ENVIRONMENT', 'production')
)

# Initialize Hugging Face
hf_client = InferenceClient(api_key=os.getenv('HF_TOKEN'))

# Price IDs
STARTER_PRICE_ID = os.getenv('STRIPE_STARTER_PRICE_ID')
PRO_PRICE_ID = os.getenv('STRIPE_PRO_PRICE_ID')

# Square pricing (in cents)
SQUARE_ONE_TIME_PRICE = int(os.getenv('SQUARE_ONE_TIME_PRICE', 500))  # $5.00 default

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'AI API with Stripe & Square Integration',
        'version': '2.0.0',
        'endpoints': {
            'POST /api/generate': 'Generate text using AI',
            'GET /pricing': 'Get pricing plans',
            'POST /checkout': 'Create Stripe checkout session',
            'POST /square/payment': 'Create Square one-time payment',
            'GET /square/pricing': 'Get Square pricing'
        }
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate text using Hugging Face API"""
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Generate text
        response = hf_client.text_generation(
            prompt=prompt,
            max_new_tokens=100
        )
        
        return jsonify({
            'prompt': prompt,
            'response': response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pricing', methods=['GET'])
def get_pricing():
    """Get available Stripe pricing plans"""
    return jsonify({
        'plans': [
            {
                'name': 'Starter',
                'price': 4.99,
                'interval': 'month',
                'requests_per_month': 5000,
                'price_id': STARTER_PRICE_ID
            },
            {
                'name': 'Pro',
                'price': 14.99,
                'interval': 'month',
                'requests_per_month': 50000,
                'price_id': PRO_PRICE_ID
            }
        ]
    })

@app.route('/square/pricing', methods=['GET'])
def get_square_pricing():
    """Get Square one-time payment pricing"""
    return jsonify({
        'payment_type': 'one-time',
        'price': SQUARE_ONE_TIME_PRICE / 100,  # Convert cents to dollars
        'currency': 'USD',
        'description': 'One-time payment for AI API access'
    })

@app.route('/checkout', methods=['POST'])
def create_checkout():
    """Create a Stripe checkout session"""
    try:
        data = request.json
        plan = data.get('plan', 'starter').lower()
        
        price_id = STARTER_PRICE_ID if plan == 'starter' else PRO_PRICE_ID
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1
            }],
            mode='subscription',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel'
        )
        
        return jsonify({
            'checkout_url': session.url,
            'session_id': session.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/square/payment', methods=['POST'])
def create_square_payment():
    """Create a Square one-time payment"""
    try:
        data = request.json
        source_id = data.get('source_id')  # Payment token from Square Web Payments SDK
        
        if not source_id:
            return jsonify({'error': 'source_id is required'}), 400
        
        # Create payment
        payments_api = square_client.payments
        
        payment = {
            'source_id': source_id,
            'amount_money': {
                'amount': SQUARE_ONE_TIME_PRICE,
                'currency': 'USD'
            },
            'idempotency_key': str(uuid.uuid4()),
            'receipt_number': str(uuid.uuid4())[:8].upper()
        }
        
        result = payments_api.create_payment(payment)
        
        if result.is_success():
            return jsonify({
                'status': 'success',
                'payment_id': result.result.payment.id,
                'amount': SQUARE_ONE_TIME_PRICE / 100,
                'currency': 'USD'
            }), 200
        elif result.is_client_error():
            return jsonify({
                'error': 'Invalid request',
                'details': result.errors
            }), 400
        else:
            return jsonify({
                'error': 'Payment processing failed',
                'details': result.errors
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860)
