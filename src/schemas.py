from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserEvent(BaseModel):
    user_id: int = Field(..., ge=1000, le=9999, description="User ID must be 4 digits")
    clicks: int = Field(..., ge=0)
    session_duration: float = Field(..., ge=0.0)
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())

class PredictionResponse(BaseModel):
    user_id: int
    is_anomaly: bool
    anomaly_score: float
    features: dict