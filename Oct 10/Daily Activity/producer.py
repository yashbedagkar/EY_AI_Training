import pika
import json

# 1.Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2.Create a queue (idempotent - creates only if not existing)
channel.queue_declare(queue="student_tasks")

# 3.Prepare a message
task = {
    "student_id": 101,
    "action": "generate_certificate",
    "email": "rahul@example.com"
}

# 4.Publish the message to the queue
channel.basic_publish(
    exchange='',
    routing_key='student_tasks',
    body=json.dumps(task)
)

print("Tasks sent to queue:", task)

connection.close()