-- BigQuery Schema for KrisiSar AI Analytics
-- Project: krisisar-ai
-- Dataset: krisisar_analytics

-- Create dataset (run once)
-- CREATE SCHEMA IF NOT EXISTS krisisar_analytics;

-- Diagnosis Events Table
CREATE TABLE IF NOT EXISTS krisisar_analytics.diagnosis_events (
  event_id STRING NOT NULL,
  user_id STRING,
  disease STRING,
  confidence FLOAT64,
  severity STRING,
  crop_type STRING,
  location JSON,
  timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, disease
OPTIONS(
  description="Crop diagnosis events from image analysis"
);

-- Risk Score Events Table
CREATE TABLE IF NOT EXISTS krisisar_analytics.risk_score_events (
  event_id STRING NOT NULL,
  user_id STRING,
  overall_score INT64,
  risk_level STRING,
  weather_risk INT64,
  disease_risk INT64,
  crop_health_risk INT64,
  location JSON,
  timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, risk_level
OPTIONS(
  description="Farm risk score calculations"
);

-- Weather Events Table
CREATE TABLE IF NOT EXISTS krisisar_analytics.weather_events (
  event_id STRING NOT NULL,
  location JSON,
  temperature FLOAT64,
  humidity FLOAT64,
  rainfall FLOAT64,
  wind_speed FLOAT64,
  disease_risk_score INT64,
  timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp)
OPTIONS(
  description="Weather data and disease risk assessments"
);

-- Chat Sessions Table
CREATE TABLE IF NOT EXISTS krisisar_analytics.chat_sessions (
  session_id STRING NOT NULL,
  user_id STRING,
  message STRING,
  response STRING,
  language STRING,
  intent STRING,
  timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, language
OPTIONS(
  description="AI chat interactions"
);

-- User Activity Table
CREATE TABLE IF NOT EXISTS krisisar_analytics.user_activity (
  activity_id STRING NOT NULL,
  user_id STRING,
  activity_type STRING,
  activity_data JSON,
  timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, activity_type
OPTIONS(
  description="General user activity tracking"
);

-- Farm Performance Table (synthetic data for RAPIDS benchmark)
CREATE TABLE IF NOT EXISTS krisisar_analytics.farm_performance (
  farm_id STRING NOT NULL,
  user_id STRING,
  crop_type STRING,
  farm_size_acres FLOAT64,
  yield_kg FLOAT64,
  diseases_count INT64,
  avg_risk_score INT64,
  weather_score INT64,
  location JSON,
  season STRING,
  year INT64,
  timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp)
CLUSTER BY crop_type, year
OPTIONS(
  description="Farm performance data for analytics (500K synthetic records)"
);

-- Views for Analytics Dashboards

-- Disease Heatmap View
CREATE OR REPLACE VIEW krisisar_analytics.disease_heatmap AS
SELECT
  DATE(timestamp) as date,
  JSON_EXTRACT_SCALAR(location, '$.state') as state,
  JSON_EXTRACT_SCALAR(location, '$.district') as district,
  disease,
  COUNT(*) as cases,
  AVG(confidence) as avg_confidence
FROM krisisar_analytics.diagnosis_events
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date, state, district, disease
ORDER BY date DESC, cases DESC;

-- Top Diseases View
CREATE OR REPLACE VIEW krisisar_analytics.top_diseases AS
SELECT
  disease,
  COUNT(*) as total_cases,
  AVG(confidence) as avg_confidence,
  COUNTIF(severity = 'critical') as critical_cases,
  COUNTIF(severity = 'high') as high_cases
FROM krisisar_analytics.diagnosis_events
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY disease
ORDER BY total_cases DESC
LIMIT 20;

-- Risk Distribution View
CREATE OR REPLACE VIEW krisisar_analytics.risk_distribution AS
SELECT
  risk_level,
  COUNT(*) as count,
  AVG(overall_score) as avg_score,
  AVG(weather_risk) as avg_weather_risk,
  AVG(disease_risk) as avg_disease_risk
FROM krisisar_analytics.risk_score_events
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY risk_level
ORDER BY avg_score DESC;

-- Daily Activity View
CREATE OR REPLACE VIEW krisisar_analytics.daily_activity AS
SELECT
  DATE(timestamp) as date,
  COUNT(DISTINCT user_id) as active_users,
  COUNT(*) as total_events,
  COUNTIF(activity_type = 'diagnosis') as diagnoses,
  COUNTIF(activity_type = 'chat') as chats,
  COUNTIF(activity_type = 'risk_check') as risk_checks
FROM krisisar_analytics.user_activity
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date DESC;

-- Farmer Engagement Metrics
CREATE OR REPLACE VIEW krisisar_analytics.farmer_engagement AS
SELECT
  user_id,
  COUNT(*) as total_interactions,
  COUNT(DISTINCT DATE(timestamp)) as active_days,
  MAX(timestamp) as last_activity,
  AVG(CASE WHEN activity_type = 'diagnosis' THEN 1 ELSE 0 END) * 100 as diagnosis_rate
FROM krisisar_analytics.user_activity
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY user_id
HAVING total_interactions >= 5
ORDER BY total_interactions DESC;
