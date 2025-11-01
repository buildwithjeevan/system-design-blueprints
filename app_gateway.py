from fastapi import FastAPI
import requests

app = FastAPI(title="API Gateway")

USER_SERVICE_URL = "http://localhost:8001"
ORDER_SERVICE_URL = "http://localhost:8002"


@app.get("/user-orders/{user_id}")
def get_user_orders(user_id: int):
    """
    Aggregate data from User Service and Order Service.
    """
    user = requests.get(f"{USER_SERVICE_URL}/user/{user_id}").json()
    orders = requests.get(f"{ORDER_SERVICE_URL}/orders/{user_id}").json()
    return {"user": user, "orders": orders}