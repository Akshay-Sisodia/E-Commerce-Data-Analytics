from confluent_kafka import Producer
import json
import time
import random
import sys

# Kafka configuration
bootstrap_servers = 'localhost:9093'  # Replace with your Kafka broker address
topic_name = 'user_actions'           # Kafka topic to send messages to

# Create a Kafka producer
producer = Producer({
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'python-producer'
})

# List of possible user actions
actions = ["click", "purchase", "add_to_cart"]

# Function to generate random user data
def generate_user_data():
    return {
        "user_id": random.randint(1, 2),  # Random user ID between 1 and 100
        "action": random.choice(actions),   # Random action from the list
        "timestamp": int(time.time())       # Current timestamp
    }

# Callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Send messages to Kafka
try:
    for i in range(1000):  # Send 1000 messages
        data = generate_user_data()  # Generate random user data
        producer.produce(
            topic=topic_name,
            key=str(data["user_id"]),  # Use user_id as the key
            value=json.dumps(data),    # Serialize data to JSON
            callback=delivery_report   # Attach delivery report callback
        )
        print(f"Sent: {data}")  # Print the sent data
        producer.poll(0)  # Poll for events (e.g., delivery reports)
        time.sleep(1)  # Wait for 1 second between messages
except KeyboardInterrupt:
    print("Producer interrupted.")
finally:
    producer.flush()  # Ensure all messages are sent
    print("Producer closed.")