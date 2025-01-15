import asyncio
import json
from aiokafka import AIOKafkaProducer
from aiokafka.errors import UnknownTopicOrPartitionError
from custom_exceptions import KafkaConnectionError, KafkaMessageError,KafkaTopicError
from kafka_utils import create_topic


BROKER = 'localhost:9092,localhost:9093,localhost:9095'


async def produce_orders():
    topic_name = "Orders"

    try:
        # Dynamically create the topic if not exists
        create_topic(topic_name)
    except KafkaConnectionError as e:
        print(f"Connection Error: {e}")
        return
    except KafkaTopicError as e:
        print(f"Topic Error: {e}")
        return

    producer = AIOKafkaProducer(bootstrap_servers=BROKER)
    try:
        await producer.start()
        print("Kafka producer connected successfully.")
    except Exception as e:
        raise KafkaConnectionError(f"Failed to connect Kafka producer: {e}")
    
    try:
        orders = [
            {"order_id": 1, "customer_name": "Alice", "item": "Laptop", "quantity": 1},
            {"order_id": 2, "customer_name": "Bob", "item": "Headphones", "quantity": 2},
            {"order_id": 3, "customer_name": "Wonderland", "item": "PowerBank", "quantity": 1},
            {"order_id": 4, "customer_name": "Marley", "item": "Earpods", "quantity": 2},
            {"order_id": 5, "customer_name": "Chandler", "item": "Charger", "quantity": 1},
            {"order_id": 6, "customer_name": "Joey", "item": "Earbuds", "quantity": 2},
        ]

        print(f"Sending orders to Kafka topic '{topic_name}'...")
        for order in orders:
            try:
                order_json = json.dumps(order).encode('utf-8')
                await producer.send_and_wait(topic_name, order_json)
                print(f"Order Sent: {order}")
            except UnknownTopicOrPartitionError as e:
                raise KafkaMessageError(f"Unknown topic or partition error: {e}")
            except Exception as e:
                raise KafkaMessageError(f"Failed to send order {order}: {e}")
    finally:
        try:
            await producer.stop()
        except Exception as e:
            print(f"Error stopping producer: {e}")

asyncio.run(produce_orders())
