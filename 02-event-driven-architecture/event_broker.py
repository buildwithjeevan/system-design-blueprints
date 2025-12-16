"""
Simple Event Broker using Redis Pub/Sub
This acts as the message broker that facilitates communication between services
"""
import redis
import json
from typing import Callable, Dict, Any

class EventBroker:
    def __init__(self, host='localhost', port=6379):
        """Initialize Redis connection for pub/sub messaging"""
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        
    def publish(self, channel: str, event_data: Dict[Any, Any]):
        """
        Publish an event to a specific channel
        
        Args:
            channel: The event channel name (e.g., 'order.created')
            event_data: Dictionary containing event details
        """
        message = json.dumps(event_data)
        self.redis_client.publish(channel, message)
        print(f"📢 Published to '{channel}': {message}")
        
    def subscribe(self, channel: str, callback: Callable):
        """
        Subscribe to a channel and execute callback when messages arrive
        
        Args:
            channel: The event channel to subscribe to
            callback: Function to call when event is received
        """
        self.pubsub.subscribe(channel)
        print(f"👂 Subscribed to '{channel}'")
        
        # Listen for messages
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event_data = json.loads(message['data'])
                callback(event_data)
