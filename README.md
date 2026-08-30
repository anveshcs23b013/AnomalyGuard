# 🛡️ AnomalyGuard: Real-Time User Behavior Surveillance

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![BentoML](https://img.shields.io/badge/ML%20Serving-BentoML-green.svg)
![Kafka](https://img.shields.io/badge/Streaming-Confluent%20Kafka-black.svg)

**AnomalyGuard** is a production-grade, event-driven Machine Learning pipeline designed to detect anomalies in user clickstream data in real-time.

It leverages a decoupled microservices architecture to process streaming data from **Confluent Cloud (Kafka)**, maintain stateful features using **Feast**, and serve low-latency predictions via **BentoML**.

---

## 🏗️ Architecture

The system follows the **Modern Data Stack** principles for MLOps:

1.  **Ingestion Layer (Producer):**
    * Simulates high-velocity user traffic (clickstream).
    * Injects synthetic anomalies (e.g., bot attacks/high click rates) into a **Kafka Topic**.
2.  **Stream Processing (Processor):**
    * Consumes raw events from **Confluent Cloud**.
    * Performs real-time aggregation (windowing).
    * Updates the **Feast Online Store** (SQLite/Redis) with the latest user state.
3.  **Inference Service (BentoML):**
    * Exposes a high-performance REST API.
    * Retrieves real-time feature vectors from Feast (solving training-serving skew).
    * Runs an **Isolation Forest** model to score anomaly probability.
4.  **Presentation Layer (Streamlit):**
    * A live dashboard that visualizes user sessions and alerts on critical anomalies (latency < 200ms).

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Streaming:** Confluent Cloud (Apache Kafka)
* **Feature Store:** Feast (Feature Store)
* **Model Serving:** BentoML (Unified Model Serving)
* **Machine Learning:** Scikit-Learn (Isolation Forest)
* **Frontend:** Streamlit
* **Validation:** Pydantic (Data Contracts)

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9 or higher
* A free [Confluent Cloud](https://confluent.cloud) account.

### 2. Installation

Clone the repository and install dependencies:

```bash
# Clone the repository
git clone [https://github.com/SohiniManne/AnomalyGuard](https://github.com/SohiniManne/AnomalyGuard)
cd AnomalyGuard

# Install dependencies
pip install -r requirements.txt
