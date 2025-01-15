class KafkaBaseError(Exception):
    """Base class for Kafka-related exceptions."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__} (status_code={self.status_code}, message={self.message})"


class KafkaTopicError(KafkaBaseError):
    """Custom exception for Kafka topic-related errors."""
    def __init__(self, message: str = "Kafka topic error"):
        super().__init__(status_code=400, message=message)


class KafkaConnectionError(KafkaBaseError):
    """Custom exception for Kafka connection-related errors."""
    def __init__(self, message: str = "Kafka connection error"):
        super().__init__(status_code=500, message=message)


class KafkaMessageError(KafkaBaseError):
    """Custom exception for Kafka message-related errors."""
    def __init__(self, message: str = "Kafka message error"):
        super().__init__(status_code=503, message=message)
