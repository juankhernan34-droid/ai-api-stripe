from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Initialize Hugging Face
hf_client = InferenceClient(api_key=os.getenv('HF_TOKEN'))

# Price IDs
STARTER_PRICE_ID = os.getenv('STRIPE_STARTER_PRICE_ID')
PRO_PRICE_ID = os.getenv('STRIPE_PRO_PRICE_ID')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'AI API with Stripe Integration',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/generate': 'Generate text using AI',
            'GET /pricing': 'Get pricing plans',
            'POST /checkout': 'Create checkout session'
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
    """Get available pricing plans"""
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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860)