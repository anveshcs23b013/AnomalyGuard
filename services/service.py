import bentoml
import joblib
import pandas as pd
from feast import FeatureStore
from src.config import get_settings
from pydantic import BaseModel, Field # Added Field

# Input Schema
class UserInput(BaseModel):
    user_id: int

settings = get_settings()

@bentoml.service(name="anomaly_detector", traffic={"timeout": 10})
class AnomalyDetectorService:
    def __init__(self):
        print(f"Loading model from {settings.MODEL_PATH}...")
        self.model = joblib.load(settings.MODEL_PATH)
        self.store = FeatureStore(repo_path=settings.FEATURE_REPO_PATH)

    @bentoml.api
    def predict(self, input_data: UserInput) -> dict:
        # Debug print
        print(f"Received request for user: {input_data.user_id}")
        
        user_id = input_data.user_id
        
        features = self.store.get_online_features(
            features=[
                "user_activity_view:clicks",
                "user_activity_view:session_duration"
            ],
            entity_rows=[{"user_id": user_id}]
        ).to_dict()
        
        if not features['user_id'] or features['user_id'][0] is None:
            return {"error": "User not found in stream", "is_anomaly": False, "features": {}}

        clicks = features['clicks'][0]
        duration = features['session_duration'][0]

        df = pd.DataFrame({'clicks': [clicks], 'session_duration': [duration]})
        
        prediction = self.model.predict(df)[0]
        score = self.model.decision_function(df)[0]
        
        return {
            "user_id": user_id,
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": float(score),
            "features": {"clicks": clicks, "session_duration": duration}
        }