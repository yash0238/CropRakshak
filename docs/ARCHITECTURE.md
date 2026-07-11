# 🏗️ KrisiSar AI — Architecture

This document describes how KrisiSar AI is put together: the layers, the data pipeline, the agents, and where GPU acceleration fits.

---

## 1. High-level overview

```
┌─────────────────────────────────────────────────────────┐
│                 Next.js 15 Frontend                        │
│   React 19 · TypeScript · Tailwind v4 · Recharts           │
│   Landing · Dashboard · 6 feature pages · Signup · Docs    │
└───────────────┬───────────────────────────┬──────────────┘
                │ REST (JSON)                │ Supabase JS (auth, optional)
                ▼                            ▼
┌─────────────────────────────────┐   ┌──────────────────┐
│         FastAPI Backend          │   │  Supabase Auth   │
│  8 route groups · 6 AI agents    │   │  (email/password)│
└───┬───────────┬──────────┬───────┘   └──────────────────┘
    │           │          │
    ▼           ▼          ▼
┌────────┐ ┌─────────┐ ┌──────────────┐
│ Gemini │ │Open-Meteo│ │   BigQuery   │
│  API   │ │ weather  │ │  analytics   │
└────────┘ └─────────┘ └──────┬───────┘
                              │
                 ┌────────────┼─────────────┐
                 ▼                          ▼
          ┌─────────────┐          ┌────────────────────┐
          │Looker Studio│          │ NVIDIA RAPIDS cuDF  │
          │  dashboard  │          │  (Colab T4 GPU)     │
          └─────────────┘          └────────────────────┘
```

---

## 2. Frontend

- **Framework:** Next.js 15 App Router with React 19 and TypeScript.
- **Styling:** Tailwind CSS v4, responsive across mobile → desktop (breakpoint classes on every page).
- **Pages:** landing (`/`), dashboard (`/dashboard`) with six feature pages (diagnosis, risk-score, weather, chat, schemes, analytics), plus signup, demo, and docs.
- **Data access:** a small typed fetch wrapper (`lib/api.ts`) that unwraps the backend's `{ success, data, error }` envelope, adds timeouts, and surfaces friendly errors. Helpers for geolocation and reverse geocoding (BigDataCloud) are included.
- **Charts:** Recharts (`ResponsiveContainer`) for the analytics dashboard.
- **Auth:** Supabase JS client (`lib/supabase.ts`). Auth is optional — the app is fully usable without signing in.
- **PWA:** opt-in only. Disabled unless `NEXT_PUBLIC_ENABLE_PWA=true`, to avoid service-worker caching surprises during development and demos.

---

## 3. Backend

- **Framework:** FastAPI (async), documented automatically at `/docs` (Swagger UI).
- **Routing:** eight route groups under `/api/v1/*` — diagnosis, weather, risk, recommendations, schemes, chat, analytics, alerts.
- **Config:** `config.py` uses pydantic settings loaded from `.env`. Notable keys: `GOOGLE_API_KEY`, `BIGQUERY_PROJECT_ID`, `BIGQUERY_DATASET_ID`, `BIGQUERY_FARM_TABLE`, `BIGQUERY_CREDENTIALS_PATH`.
- **Gemini models:** all three slots (flash / reasoning / vision) map to `gemini-2.5-flash`. The free tier has no quota on `gemini-2.5-pro`; switch the reasoning slot back to Pro on a billing-enabled key for higher-quality output.
- **CORS:** restricted to the known frontend origins (localhost + deployed URL).

### Agents (`backend/agents/`)

| Agent | Responsibility |
|---|---|
| `image_diagnosis_agent` | Sends an uploaded image to Gemini Vision, returns disease, confidence, severity, treatment |
| `weather_intelligence_agent` | Pulls Open-Meteo forecast, derives disease-risk and irrigation signals |
| `risk_prediction_agent` | Combines weather, disease, and crop-health factors into a 0–100 score |
| `recommendation_agent` | Produces decision cards (clear yes/no + reasoning) via Gemini |
| `government_scheme_agent` | RAG-style matching of farmer profile to schemes |
| `analytics_agent` | Writes events to BigQuery and runs aggregation queries |

---

## 4. Data pipeline

### Storage — BigQuery (`krisisar_analytics`)

**Tables**
- `farm_perf_raw` — the bulk 500K farm-performance dataset (loaded via CSV auto-detect; `location` is stored as a JSON string).
- `diagnosis_events`, `risk_score_events`, `weather_events`, `chat_sessions`, `user_activity` — event tables (populated when a `user_id` is supplied with requests).
- `farm_performance` — strict-schema variant defined in `schema.sql`.

**Views** — `disease_heatmap`, `top_diseases`, `risk_distribution`, `daily_activity`, `farmer_engagement`. Tables are partitioned by date and clustered for query efficiency.

### Serving — `/api/v1/analytics/farm-insights`

`AnalyticsAgent.get_farm_insights()` runs three aggregations over `farm_perf_raw`:
1. **Average yield by crop** — `GROUP BY crop_type`.
2. **Average risk by state** — `JSON_EXTRACT_SCALAR(location, '$.state')` (works on the JSON-as-string column).
3. **Disease spread** — `GROUP BY diseases_count`.

The in-app Analytics page renders these as bar and pie charts. A public Looker Studio report reads the same table for a richer, judge-facing dashboard (yield by crop, crop mix, yield by season, scorecards).

---

## 5. GPU acceleration (NVIDIA RAPIDS)

The `analytics/rapids_benchmark.ipynb` notebook demonstrates the acceleration layer required by the hackathon. On a Google Colab T4 GPU it compares pandas (CPU) vs cuDF (GPU) over the same 500K rows:

| Operation | Speedup |
|---|---|
| GroupBy aggregation | **49.8x** |
| CSV load | 15.1x |
| Filter | 2.8x |
| **Average** | **22.58x** |

This is the evidence that acceleration lowers time-to-insight: the same aggregations that power the dashboard run an order of magnitude faster on GPU, which is what makes real-time analytics viable at national farmer scale.

---

## 6. Security notes

- `service-account.json` (BigQuery credentials) is gitignored and injected as a secret file in deployment — never committed.
- The Supabase anon key is safe to expose (protected by row-level security); no service-role keys live in the frontend.
- Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`) are set in `next.config.ts`.

---

## 7. Deployment shape

- **Frontend:** Vercel (root = `frontend`).
- **Backend:** Render / Railway (root = `backend`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`, service-account as a secret file).
- **Data/analytics:** BigQuery + Looker Studio (already cloud-hosted); RAPIDS benchmark runs on Colab.
