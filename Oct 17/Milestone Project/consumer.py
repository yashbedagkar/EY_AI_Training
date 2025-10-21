import pika
import json
import logging
import time
import random

# Configure logging
logging.basicConfig(
    filename="shipment_logs.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Mock reference data
valid_products = {"P101", "P102", "P103", "P104", "P105"}
valid_warehouses = {"W01", "W02", "W03"}

processed_shipments = {}

def process_message(ch, method, properties, body):
    """Callback function triggered when message arrives."""
    try:
        start_time = time.time()
        message = json.loads(body)
        shipment_id = message.get("ShipmentID")
        status = message.get("Status")

        # Simulate product and warehouse assignment (may randomly be missing)
        product_id = random.choice(list(valid_products) + [None])
        warehouse_id = random.choice(list(valid_warehouses) + [None])

        if not product_id or not warehouse_id:
            logging.error(f"Missing ProductID or WarehouseID for {shipment_id}.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Log based on shipment status
        if status.lower() == "dispatched":
            logging.info(f"Shipment {shipment_id} dispatched from {warehouse_id}.")
        elif status.lower() == "delivered":
            logging.info(f"Shipment {shipment_id} delivered to {warehouse_id}.")
        else:
            logging.warning(f"Unknown status for shipment {shipment_id}: {status}")

        # Save to in-memory processed shipments
        processed_shipments[shipment_id] = {
            "ProductID": product_id,
            "WarehouseID": warehouse_id,
            "Status": status
        }

        # Simulate delay in processing
        time.sleep(random.uniform(0.5, 1.5))

        # Log total processing time
        processing_time = time.time() - start_time
        logging.info(f"Processed shipment {shipment_id} in {processing_time:.2f} sec.")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.exception(f"Error processing shipment: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    """Set up RabbitMQ consumer."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Ensure the queue exists
    channel.queue_declare(queue='shipments_queue')

    # Listen to the queue
    channel.basic_consume(queue='shipments_queue', on_message_callback=process_message)

    print("[Consumer] Waiting for messages. Press CTRL+C to exit.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer stopped.")
        channel.stop_consuming()
        connection.close()

if __name__ == "__main__":
    main()
