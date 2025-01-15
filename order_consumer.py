import asyncio
import json
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import UnknownTopicOrPartitionError
from custom_exceptions import KafkaConnectionError, KafkaTopicError, KafkaMessageError
from kafka_utils import create_topic
import time



BROKER = 'localhost:9092,localhost:9093,localhost:9095'



async def process_orders():
    topic_name = "Orders"
    retries = 5  # Number of retries for transient errors

    # Retry connection and topic creation
    for attempt in range(retries):
        try:
            create_topic(topic_name)  # Dynamically create the topic
            break
        except KafkaConnectionError as e:
            print(f"Connection Error: {e}")
            return
        except KafkaTopicError as e:
            print(f"Topic Error: {e}")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to create topic '{topic_name}'. Retrying in 2 seconds. Error: {e}")
            time.sleep(2)
    else:
        print(f"Failed to create topic '{topic_name}' after {retries} attempts.")
        return

    consumer = AIOKafkaConsumer(
        topic_name,
        bootstrap_servers= BROKER,
        group_id="order-processing-group",  # Consumer group
        enable_auto_commit=True,
    )
    for attempt in range(retries):
        try:
            await consumer.start()
            print("Kafka consumer connected successfully.")
            break

        except Exception as e:
            raise KafkaConnectionError(f"Failed to connect Kafka consumer: {e}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to connect Kafka consumer. Retrying in 2 seconds. Error: {e}")
            time.sleep(2)
    else:
        print("Failed to connect Kafka consumer after retries.")
        return

    try:
        print(f"Processing orders from Kafka topic '{topic_name}' as part of group 'order-processing-group'...")
        async for message in consumer:
            try:
                order = json.loads(message.value.decode('utf-8'))
                process_order(order)
            except UnknownTopicOrPartitionError as e:
                raise KafkaMessageError(f"Unknown topic or partition error: {e}")
            except Exception as e:
                print(f"Error processing message {message.value}: {e}")
    finally:
        try:
            await consumer.stop()
        except Exception as e:
            print(f"Error stopping consumer: {e}")

def process_order(order):
    try:
        print(f"Order Processed: Order ID: {order['order_id']}, Item: {order['item']}, Quantity: {order['quantity']}")
    except KeyError as e:
        print(f"Missing key in order: {e}")
    except Exception as e:
        print(f"Unexpected error while processing order: {e}")

asyncio.run(process_orders())
