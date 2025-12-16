"""
Inventory Service - Event Consumer
Listens for 'order.created' events and updates inventory
"""
import sys
import os

# Add parent directory to path to import event_broker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from event_broker import EventBroker

# Mock inventory database
inventory = {
    1: {"name": "Laptop", "stock": 50},
    2: {"name": "Mouse", "stock": 200},
    3: {"name": "Keyboard", "stock": 100}
}

def update_inventory(order_data):
    """
    Handle the order.created event by updating inventory
    
    This demonstrates how multiple services can independently 
    react to the same event in different ways.
    """
    product_id = order_data.get('product_id')
    quantity = order_data.get('quantity')
    
    if product_id in inventory:
        inventory[product_id]['stock'] -= quantity
        print(f"📦 INVENTORY: Updated product {product_id}")
        print(f"   Product: {inventory[product_id]['name']}")
        print(f"   Quantity sold: {quantity}")
        print(f"   Remaining stock: {inventory[product_id]['stock']}")
    else:
        print(f"⚠️  INVENTORY: Product {product_id} not found")
    
    print(f"   Full order details: {order_data}")
    print("-" * 60)

def main():
    """
    Start the inventory service consumer
    This runs continuously, listening for events
    """
    print("🚀 Starting Inventory Service...")
    print("   Current inventory:", inventory)
    print("   Waiting for order.created events...")
    
    broker = EventBroker()
    # Subscribe to the same 'order.created' channel
    broker.subscribe('order.created', update_inventory)

if __name__ == "__main__":
    main()
