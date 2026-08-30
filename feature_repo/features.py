from datetime import timedelta
from feast import Entity, FeatureView, Field, PushSource, FileSource, ValueType
from feast.data_format import ParquetFormat
from feast.types import Float32, Int64

# 1. Define the Entity (Fixed: Added value_type to silence warning)
user = Entity(
    name="user_id", 
    join_keys=["user_id"], 
    value_type=ValueType.INT64
)

# 2. Define the Push Source (Fixed: Used ParquetFormat object)
user_stats_push_source = PushSource(
    name="user_stats_push_source",
    batch_source=FileSource(
        file_format=ParquetFormat(), # <--- This was the error
        path="data/historical_data.parquet",
        timestamp_field="event_timestamp"
    )
)

# 3. Define the Feature View
user_activity_view = FeatureView(
    name="user_activity_view",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="clicks", dtype=Int64),
        Field(name="session_duration", dtype=Float32),
    ],
    online=True,
    source=user_stats_push_source,
)