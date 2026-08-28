#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}AI API with Stripe - One Click Deploy${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
fi

echo ""
echo -e "${YELLOW}Enter your configuration:${NC}"
echo ""

# Get HF Username
read -p "$(echo -e ${BLUE})HF Username${NC} (e.g., klenz1984): " HF_USERNAME
if [ -z "$HF_USERNAME" ]; then
    HF_USERNAME="klenz1984"
fi

# Get HF Token
read -sp "$(echo -e ${BLUE})HF Token${NC}: " HF_TOKEN
echo ""

# Get Stripe Secret Key
read -sp "$(echo -e ${BLUE})Stripe Secret Key${NC} (sk_test_...): " STRIPE_SECRET_KEY
echo ""

# Get Stripe Publishable Key
read -sp "$(echo -e ${BLUE})Stripe Publishable Key${NC} (pk_test_...): " STRIPE_PUBLISHABLE_KEY
echo ""

# Get Starter Price ID
read -p "$(echo -e ${BLUE})Stripe Starter Price ID${NC} (price_...): " STRIPE_STARTER_PRICE_ID

# Get Pro Price ID
read -p "$(echo -e ${BLUE})Stripe Pro Price ID${NC} (price_...): " STRIPE_PRO_PRICE_ID

echo ""
echo -e "${YELLOW}Updating .env file...${NC}"

# Update .env file
cat > .env << EOF
HF_USERNAME=$HF_USERNAME
HF_TOKEN=$HF_TOKEN
STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY=$STRIPE_PUBLISHABLE_KEY
STRIPE_STARTER_PRICE_ID=$STRIPE_STARTER_PRICE_ID
STRIPE_PRO_PRICE_ID=$STRIPE_PRO_PRICE_ID
EOF

echo -e "${GREEN}✓ .env file updated${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Option to run locally or deploy to HF Spaces
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}What would you like to do?${NC}"
echo "1) Run API locally"
echo "2) Deploy to Hugging Face Spaces"
echo "3) Both"
echo ""
read -p "Enter your choice (1-3): " CHOICE

case $CHOICE in
    1)
        echo ""
        echo -e "${YELLOW}Starting API locally...${NC}"
        echo -e "${GREEN}✓ API will run on http://localhost:7860${NC}"
        echo ""
        python app.py
        ;;
    2)
        echo ""
        echo -e "${YELLOW}Preparing for HF Spaces deployment...${NC}"
        echo ""
        echo -e "${BLUE}Follow these steps:${NC}"
        echo "1. Go to https://huggingface.co/spaces/new"
        echo "2. Choose ${GREEN}Docker${NC} SDK"
        echo "3. Connect GitHub: ${GREEN}juankhernan34-droid/ai-api-stripe${NC}"
        echo "4. Add these secrets in Settings → Repository secrets:"
        echo ""
        echo -e "${YELLOW}Secrets to add:${NC}"
        echo -e "  HF_USERNAME: ${GREEN}$HF_USERNAME${NC}"
        echo -e "  HF_TOKEN: ${GREEN}[hidden]${NC}"
        echo -e "  STRIPE_SECRET_KEY: ${GREEN}[hidden]${NC}"
        echo -e "  STRIPE_PUBLISHABLE_KEY: ${GREEN}[hidden]${NC}"
        echo -e "  STRIPE_STARTER_PRICE_ID: ${GREEN}$STRIPE_STARTER_PRICE_ID${NC}"
        echo -e "  STRIPE_PRO_PRICE_ID: ${GREEN}$STRIPE_PRO_PRICE_ID${NC}"
        echo ""
        echo "5. Click ${GREEN}Create Space${NC}"
        echo ""
        echo -e "${GREEN}✓ Ready to deploy!${NC}"
        ;;
    3)
        echo ""
        echo -e "${YELLOW}Starting API locally...${NC}"
        echo -e "${GREEN}✓ API will run on http://localhost:7860${NC}"
        echo ""
        echo -e "${BLUE}In another terminal, deploy to HF Spaces:${NC}"
        echo "1. Go to https://huggingface.co/spaces/new"
        echo "2. Choose ${GREEN}Docker${NC} SDK"
        echo "3. Connect GitHub: ${GREEN}juankhernan34-droid/ai-api-stripe${NC}"
        echo "4. Add secrets (see above)"
        echo "5. Click ${GREEN}Create Space${NC}"
        echo ""
        python app.py
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac