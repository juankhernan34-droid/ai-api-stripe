from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import paypalrestsdk

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Initialize PayPal
paypalrestsdk.configure({
    "mode": os.getenv('PAYPAL_MODE', 'sandbox'),
    "client_id": os.getenv('PAYPAL_CLIENT_ID'),
    "client_secret": os.getenv('PAYPAL_CLIENT_SECRET')
})

# Initialize Hugging Face
hf_client = InferenceClient(api_key=os.getenv('HF_TOKEN'))

# Price IDs
STARTER_PRICE_ID = os.getenv('STRIPE_STARTER_PRICE_ID')
PRO_PRICE_ID = os.getenv('STRIPE_PRO_PRICE_ID')

# PayPal pricing
PAYPAL_ONE_TIME_PRICE = os.getenv('PAYPAL_ONE_TIME_PRICE', '5.00')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'AI API with Stripe & PayPal Integration',
        'version': '2.0.0',
        'endpoints': {
            'POST /api/generate': 'Generate text using AI',
            'GET /pricing': 'Get pricing plans',
            'POST /checkout': 'Create Stripe checkout session',
            'POST /paypal/payment': 'Create PayPal one-time payment',
            'POST /paypal/payment/execute': 'Execute PayPal payment',
            'GET /paypal/pricing': 'Get PayPal pricing'
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

@app.route('/paypal/pricing', methods=['GET'])
def get_paypal_pricing():
    """Get PayPal one-time payment pricing"""
    return jsonify({
        'payment_type': 'one-time',
        'price': float(PAYPAL_ONE_TIME_PRICE),
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

@app.route('/paypal/payment', methods=['POST'])
def create_paypal_payment():
    """Create a PayPal one-time payment"""
    try:
        data = request.json
        return_url = data.get('return_url', 'https://example.com/success')
        cancel_url = data.get('cancel_url', 'https://example.com/cancel')
        
        # Create payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "amount": {
                    "total": PAYPAL_ONE_TIME_PRICE,
                    "currency": "USD"
                },
                "description": "One-time payment for AI API access"
            }]
        })
        
        if payment.create():
            # Get approval URL
            approval_url = None
            for link in payment.links:
                if link['rel'] == 'approval_url':
                    approval_url = link['href']
            
            return jsonify({
                'status': 'success',
                'payment_id': payment.id,
                'approval_url': approval_url,
                'amount': float(PAYPAL_ONE_TIME_PRICE),
                'currency': 'USD'
            }), 200
        else:
            return jsonify({
                'error': 'Payment creation failed',
                'details': payment.error
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/paypal/payment/execute', methods=['POST'])
def execute_paypal_payment():
    """Execute a PayPal payment after user approval"""
    try:
        data = request.json
        payment_id = data.get('payment_id')
        payer_id = data.get('payer_id')
        
        if not payment_id or not payer_id:
            return jsonify({'error': 'payment_id and payer_id are required'}), 400
        
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            return jsonify({
                'status': 'success',
                'message': 'Payment completed successfully',
                'payment_id': payment.id,
                'amount': float(PAYPAL_ONE_TIME_PRICE),
                'currency': 'USD'
            }), 200
        else:
            return jsonify({
                'error': 'Payment execution failed',
                'details': payment.error
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860)
