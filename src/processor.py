import json
import logging
import pandas as pd
from confluent_kafka import Consumer
from feast import FeatureStore
from src.config import get_settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StreamProcessor")
settings = get_settings()

class FeatureProcessor:
    def __init__(self):
        self.store = FeatureStore(repo_path=settings.FEATURE_REPO_PATH)
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': settings.KAFKA_API_KEY,
            'sasl.password': settings.KAFKA_API_SECRET,
            'group.id': 'production_group_v1',
            'auto.offset.reset': 'latest'
        })
        self.consumer.subscribe([settings.KAFKA_TOPIC])

    def process(self):
        logger.info("🔴 Processor Started. Listening for events...")
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None: continue
                if msg.error():
                    logger.error(f"Consumer Error: {msg.error()}")
                    continue

                # Deserialize
                data = json.loads(msg.value().decode('utf-8'))
                
                # Transform to Pandas for Feast
                df = pd.DataFrame([{
                    "user_id": data['user_id'],
                    "clicks": data['clicks'],
                    "session_duration": data['session_duration'],
                    "event_timestamp": pd.Timestamp.now()
                }])

                # Push to Online Store
                self.store.push("user_stats_push_source", df)
                logger.info(f"✅ Feast Updated: User {data['user_id']}")

        except KeyboardInterrupt:
            self.consumer.close()

if __name__ == "__main__":
    FeatureProcessor().process()