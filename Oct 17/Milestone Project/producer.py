import pika
import json
import time
import random

# RabbitMQ connection parameters
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue (creates if it doesn't exist)
channel.queue_declare(queue='shipments_queue')

# Example shipment updates
shipment_updates = [
    {"ShipmentID": "S001", "Status": "Dispatched"},
    {"ShipmentID": "S002", "Status": "Dispatched"},
    {"ShipmentID": "S003", "Status": "Delivered"},
    {"ShipmentID": "S004", "Status": "Delivered"},
    {"ShipmentID": "S005", "Status": "Dispatched"},
]

for update in shipment_updates:
    message = json.dumps(update)
    # Publish to RabbitMQ queue
    channel.basic_publish(
        exchange='',
        routing_key='shipments_queue',
        body=message
    )
    print(f"[Producer] Sent: {message}")
    time.sleep(random.uniform(0.5, 1.5))  # Simulate delay

# Close connection
connection.close()
print("[Producer] All shipment updates sent successfully.")
