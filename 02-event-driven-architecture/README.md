# 📡 Event-Driven Architecture

### 📘 Problem
How do we build loosely coupled systems where services can react to changes without directly calling each other? How can we scale services independently and handle asynchronous operations?

### 🧠 What is Event-Driven Architecture?

**Event-Driven Architecture (EDA)** is a design pattern where services communicate by publishing and consuming events through a message broker, rather than making direct API calls to each other.

**Key Concepts:**
- **Event**: Something that happened (e.g., "Order Created", "Payment Completed")
- **Publisher**: Service that emits events when something happens
- **Consumer**: Service that listens for and reacts to events
- **Message Broker**: Middleware that routes events from publishers to consumers

### 🏗️ Architecture

```
┌─────────────────┐
│  Order Service  │ (Publisher)
│   Port: 8001    │
└────────┬────────┘
         │ Publishes "order.created"
         ↓
┌────────────────────┐
│   Event Broker     │ (Redis Pub/Sub)
│   (Message Queue)  │
└────────┬───────────┘
         │ Distributes events
         ├──────────────┬──────────────┐
         ↓              ↓              ↓
┌─────────────┐  ┌──────────────┐  ┌─────────────┐
│Notification │  │  Inventory   │  │   Future    │
│  Service    │  │   Service    │  │  Services   │
└─────────────┘  └──────────────┘  └─────────────┘
   (Consumer)       (Consumer)       (Consumer)
```

### ✨ How It Works

1. **Order Service** (Publisher):
   - When a new order is created via POST /orders
   - Publishes an `order.created` event to the message broker
   - Doesn't know or care who consumes the event

2. **Event Broker** (Redis):
   - Receives events from publishers
   - Maintains channels (topics) for different event types
   - Distributes events to all subscribed consumers

3. **Notification Service** (Consumer):
   - Subscribes to `order.created` events
   - Sends email/SMS notifications to users
   - Operates independently

4. **Inventory Service** (Consumer):
   - Also subscribes to `order.created` events
   - Updates product stock levels
   - Runs without knowledge of other consumers

### 🎯 Key Benefits

**1. Loose Coupling**
- Services don't need to know about each other
- Order Service doesn't call Notification/Inventory services directly
- Easy to add/remove services without changing existing code

**2. Asynchronous Processing**
- Publisher doesn't wait for consumers to finish
- Faster response times for users
- Background tasks don't block main operations

**3. Scalability**
- Each service can scale independently
- Add more consumers if event processing is slow
- No single point of failure (except the broker)

**4. Flexibility**
- Easy to add new features by adding new consumers
- No need to modify existing services
- Better separation of concerns

### ⚙️ Code Overview

**Event Broker (event_broker.py)**
```python
class EventBroker:
    def publish(self, channel: str, event_data: dict):
        # Publishes event to a channel
        self.redis_client.publish(channel, json.dumps(event_data))
    
    def subscribe(self, channel: str, callback: function):
        # Listens for events and calls callback
        for message in self.pubsub.listen():
            callback(json.loads(message['data']))
```

**Publisher (order_service/main.py)**
```python
@app.post("/orders")
def create_order(order: Order):
    order_data = {...}
    
    # Publish event - fire and forget!
    broker.publish('order.created', order_data)
    
    return {"status": "success", "order": order_data}
```

**Consumer (notification_service/main.py)**
```python
def send_notification(order_data):
    # React to the event
    print(f"Sending email to user {order_data['user_id']}")

# Subscribe to events
broker.subscribe('order.created', send_notification)
```

### 🔄 Comparison with API Gateway Pattern

| Aspect | API Gateway (01) | Event-Driven (02) |
|--------|------------------|-------------------|
| **Communication** | Synchronous (request-response) | Asynchronous (fire-and-forget) |
| **Coupling** | Services called directly | Services don't know each other |
| **Response** | Gateway waits for all services | Publisher continues immediately |
| **Use Case** | Aggregating data for clients | Triggering background tasks |
| **Example** | "Get user profile + orders" | "Order created → notify user + update inventory" |

### 🚀 Running the System

**Prerequisites:**
```bash
# Install Redis (message broker)
brew install redis  # macOS
# OR
apt-get install redis-server  # Linux

# Start Redis
redis-server
```

**Terminal 1 - Start Order Service (Publisher)**
```bash
cd 02-event-driven-architecture/order_service
python main.py
```

**Terminal 2 - Start Notification Consumer**
```bash
cd 02-event-driven-architecture/notification_service
python main.py
```

**Terminal 3 - Start Inventory Consumer**
```bash
cd 02-event-driven-architecture/inventory_service
python main.py
```

**Terminal 4 - Create an Order (Trigger Event)**
```bash
curl -X POST http://localhost:8001/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "product_id": 1,
    "quantity": 2,
    "price": 999.99
  }'
```

### 📊 What You'll See

When you create an order, watch all three terminals:

**Terminal 1 (Order Service):**
```
📢 Published to 'order.created': {"user_id": 123, "product_id": 1, ...}
```

**Terminal 2 (Notification Service):**
```
📧 NOTIFICATION: Sending email to user 123
   Subject: Order Confirmation
   Message: Your order of $1999.98 has been confirmed!
```

**Terminal 3 (Inventory Service):**
```
📦 INVENTORY: Updated product 1
   Product: Laptop
   Quantity sold: 2
   Remaining stock: 48
```

### 🎓 Key Takeaways

1. **Decoupling**: Order Service has no idea Notification/Inventory services exist
2. **Async**: Order Service responds immediately without waiting for notifications
3. **Scalability**: Can run multiple instances of any consumer for load distribution
4. **Extensibility**: Add a new "Analytics Service" consumer without touching existing code
5. **Resilience**: If Notification Service fails, Inventory Service keeps working

### 📈 When to Use Event-Driven Architecture

**Good for:**
- Background task processing (emails, notifications)
- Microservices that need to react to state changes
- Systems requiring high scalability
- Audit logs and analytics pipelines
- IoT and real-time data streaming

**Not ideal for:**
- Simple CRUD operations
- When you need immediate response from all services
- Systems with complex distributed transactions
- Small applications with tight coupling requirements

### 🔍 Real-World Examples

- **E-commerce**: Order → Payment → Shipping → Notification
- **Social Media**: Post created → Feed update → Notification → Analytics
- **Banking**: Transaction → Fraud check → Balance update → SMS alert
- **Uber**: Ride requested → Driver matching → Location tracking → ETA updates

---

### 🛠️ Technology Stack

- **FastAPI**: For the Order Service REST API
- **Redis Pub/Sub**: Message broker for event distribution
- **Python**: All service implementations

### 📚 Next Steps

Try modifying the code:
1. Add a new "Analytics Service" to track order metrics
2. Add error handling for failed event processing
3. Implement event persistence (save events to database)
4. Add event filtering (consumers only process certain orders)
5. Explore RabbitMQ or Kafka for more advanced messaging
