"""
Order Service - Event Publisher
This service creates orders and publishes 'order.created' events
"""
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import event_broker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from event_broker import EventBroker

app = FastAPI()
broker = EventBroker()

class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    price: float

@app.post("/orders")
def create_order(order: Order):
    """
    Create an order and publish an event
    
    This demonstrates the Publisher pattern in event-driven architecture.
    When an order is created, we publish an event that other services can react to.
    """
    order_data = {
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "price": order.price,
        "total": order.quantity * order.price
    }
    
    # Publish event to 'order.created' channel
    # Any service subscribed to this channel will receive this event
    broker.publish('order.created', order_data)
    
    return {
        "status": "success",
        "message": "Order created and event published",
        "order": order_data
    }

@app.get("/")
def health():
    return {"service": "order_service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
