from confluent_kafka.admin import AdminClient, NewTopic
from custom_exceptions import KafkaTopicError
from aiokafka.errors import KafkaConnectionError

BROKERS = "localhost:9092,localhost:9093"#,localhost:9094"


def create_topic(topic_name, num_partitions=1, replication_factor=1):
    """Create a Kafka topic dynamically, only if it doesn't already exist."""
    try:
        admin_client = AdminClient({
            "bootstrap.servers": BROKERS
        })

    except Exception as e:
        raise KafkaConnectionError(f"Failed to connect to Kafka brokers: {e}")

    try:
        # Check if the topic already exists
        existing_topics = admin_client.list_topics(timeout=10).topics
        if topic_name in existing_topics:
            print(f"Topic '{topic_name}' already exists. Skipping creation.")
            return
    except Exception as e:
        raise KafkaConnectionError(f"Error while listing Kafka topics: {e}")

    # Create the topic if it does not exist
    topic_list = [NewTopic(topic_name, num_partitions, replication_factor)]
    try:
        futures = admin_client.create_topics(topic_list)
        for topic, future in futures.items():
            try:
                future.result()  # Wait for topic creation to complete
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                raise KafkaTopicError(f"Failed to create topic '{topic}': {e}")
    except Exception as e:
        raise KafkaTopicError(f"Error in topic creation: {e}")
