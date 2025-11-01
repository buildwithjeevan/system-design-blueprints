from fastapi import FastAPI

app = FastAPI(title="Order Service")

ORDERS = {
    1: [
        {"order_id": 101, "item": "Laptop", "amount": 1200},
        {"order_id": 102, "item": "Mouse", "amount": 25},
    ],
    2: [
        {"order_id": 103, "item": "Keyboard", "amount": 45},
    ],
}


@app.get("/orders/{user_id}")
def get_orders(user_id: int):
    return ORDERS.get(user_id, [])