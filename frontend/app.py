import streamlit as st
import requests
import pandas as pd
import time
import altair as alt

# Config
API_URL = "http://localhost:3000/predict"
st.set_page_config(page_title="AnomalyGuard", layout="wide", page_icon="🛡️")

# Styling
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ AnomalyGuard")
st.sidebar.markdown("Real-time ML Surveillance")
user_id = st.sidebar.selectbox("Select User Stream", [1001, 1002, 1003, 1004, 1005])
auto_refresh = st.sidebar.toggle("Live Monitoring", value=True)

# Main
st.title(f"Live Monitor: User {user_id}")
col1, col2 = st.columns([3, 1])

# State
if "history" not in st.session_state:
    st.session_state.history = []

placeholder = st.empty()

while auto_refresh:
    try:
       # Change key from "user_id" to "input_data" so it matches the argument name in service.py
        resp = requests.post(API_URL, json={"input_data": {"user_id": int(user_id)}}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            
            # Update History
            if "features" in data:
                st.session_state.history.append({
                    "time": pd.Timestamp.now(),
                    "clicks": data['features']['clicks'],
                    "anomaly": data['is_anomaly']
                })
                # Keep last 50 points
                if len(st.session_state.history) > 50:
                    st.session_state.history.pop(0)
            
            with placeholder.container():
                # Top Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Live Clicks", data['features']['clicks'])
                m2.metric("Session Duration", f"{data['features']['session_duration']:.1f}s")
                
                status_color = "red" if data['is_anomaly'] else "green"
                status_text = "CRITICAL ANOMALY" if data['is_anomaly'] else "Normal Behavior"
                m3.markdown(f":{status_color}[**{status_text}**]")

                # Chart
                df_chart = pd.DataFrame(st.session_state.history)
                if not df_chart.empty:
                    chart = alt.Chart(df_chart).mark_line().encode(
                        x='time',
                        y='clicks',
                        color=alt.condition(
                            alt.datum.anomaly,
                            alt.value('red'),  # The positive color
                            alt.value('steelblue')  # The negative color
                        )
                    ).properties(height=400)
                    st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Waiting for stream... ({e})")
    
    time.sleep(1)