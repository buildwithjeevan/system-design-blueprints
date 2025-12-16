#!/bin/bash

echo "🚀 Setting up Event-Driven Architecture Example"
echo "================================================"

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed!"
    echo "Please install Redis first:"
    echo "  macOS: brew install redis"
    echo "  Linux: sudo apt-get install redis-server"
    exit 1
fi

echo "✅ Redis found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Start Redis: redis-server"
echo "2. Start Order Service: cd order_service && python main.py"
echo "3. Start Notification Service: cd notification_service && python main.py"
echo "4. Start Inventory Service: cd inventory_service && python main.py"
echo "5. Create an order:"
echo "   curl -X POST http://localhost:8001/orders \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"user_id\": 123, \"product_id\": 1, \"quantity\": 2, \"price\": 999.99}'"
