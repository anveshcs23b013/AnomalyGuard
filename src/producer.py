import json
import time
import random
import logging
from confluent_kafka import Producer
from src.config import get_settings
from src.schemas import UserEvent

# Configure Structured Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("KafkaProducer")
settings = get_settings()

class StreamGenerator:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': settings.KAFKA_API_KEY,
            'sasl.password': settings.KAFKA_API_SECRET
        })

    def _delivery_report(self, err, msg):
        if err:
            logger.error(f"Delivery failed: {err}")
        else:
            logger.debug(f"Record sent to {msg.topic()}")

    def generate_event(self) -> UserEvent:
        # 95% Normal, 5% Anomaly
        is_anomaly = random.random() > 0.95
        
        clicks = random.randint(500, 1000) if is_anomaly else random.randint(1, 50)
        duration = random.uniform(5.0, 10.0) if is_anomaly else random.uniform(60.0, 300.0)
        
        return UserEvent(
            user_id=random.randint(1001, 1005),
            clicks=clicks,
            session_duration=duration
        )

    def run(self):
        logger.info(f"Starting Producer on topic: {settings.KAFKA_TOPIC}")
        try:
            while True:
                event = self.generate_event()
                
                # Send to Kafka
                self.producer.produce(
                    settings.KAFKA_TOPIC,
                    key=str(event.user_id),
                    value=event.model_dump_json(), # Pydantic serialization
                    callback=self._delivery_report
                )
                self.producer.poll(0)
                
                logger.info(f"Sent: User={event.user_id} | Clicks={event.clicks}")
                time.sleep(1) # Simulate real-time
        except KeyboardInterrupt:
            logger.info("Stopping producer...")
            self.producer.flush()

if __name__ == "__main__":
    StreamGenerator().run()