"""
Notification Service - Event Consumer
Listens for 'order.created' events and sends notifications
"""
import sys
import os

# Add parent directory to path to import event_broker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from event_broker import EventBroker

def send_notification(order_data):
    """
    Handle the order.created event by sending a notification
    
    This demonstrates the Consumer pattern in event-driven architecture.
    The service reacts to events without direct coupling to the order service.
    """
    user_id = order_data.get('user_id')
    total = order_data.get('total')
    
    print(f"📧 NOTIFICATION: Sending email to user {user_id}")
    print(f"   Subject: Order Confirmation")
    print(f"   Message: Your order of ${total:.2f} has been confirmed!")
    print(f"   Full order details: {order_data}")
    print("-" * 60)

def main():
    """
    Start the notification service consumer
    This runs continuously, listening for events
    """
    print("🚀 Starting Notification Service...")
    print("   Waiting for order.created events...")
    
    broker = EventBroker()
    # Subscribe to 'order.created' channel and process events with send_notification
    broker.subscribe('order.created', send_notification)

if __name__ == "__main__":
    main()
