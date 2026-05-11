#!/bin/bash

echo "Setting up Healthcare AI Application..."

# Setup backend
echo "Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo "Setup complete!"
echo "To run backend: cd backend && source venv/bin/activate && python run.py"
echo "To run frontend: cd frontend && npm run dev"
