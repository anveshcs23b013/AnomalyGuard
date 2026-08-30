import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from src.config import get_settings

def train():
    settings = get_settings()
    # Create synthetic normal data
    X = pd.DataFrame({
        'clicks': np.random.randint(1, 50, 1000),
        'session_duration': np.random.uniform(60, 300, 1000)
    })
    
    # Isolation Forest
    clf = IsolationForest(random_state=42, contamination=0.05)
    clf.fit(X)
    
    joblib.dump(clf, settings.MODEL_PATH)
    print(f"Model saved to {settings.MODEL_PATH}")

if __name__ == "__main__":
    train()