# 🏗️ Krishivaani — Architecture

This document describes how Krishivaani is built: the system topology, the
multi-agent backend, the AI providers, the data layer, and the request flows
for the headline features (voice, diagnosis, analytics).

> For setup and feature overview, see the [README](./README.md).

---

## 1. System Overview

Krishivaani is a two-tier application:

- **Frontend** — a Next.js 15 (App Router) app deployed on Vercel. It renders
  the multilingual landing page and the dashboard (7 feature tools), and talks
  to the backend over a small typed `fetch` helper.
- **Backend** — a FastAPI service deployed on Render. It exposes 8 REST route
  groups, orchestrates 6 specialized AI agents, and integrates two AI
  providers (Sarvam AI and Google Gemini) plus Google BigQuery.

```
┌────────────────────────────────────────┐         ┌──────────────────────────────────────────┐
│         Next.js 15 (Vercel)            │  REST   │              FastAPI (Render)             │
│  Landing · Dashboard · Voice · i18n    │────────▶│   8 route groups · 6 AI agents            │
│  React 19 · Tailwind v4 · Recharts     │◀────────│   CORS · typed envelopes { success,data } │
└────────────────────────────────────────┘         └───────┬───────────────┬───────────┬───────┘
                                                            │               │           │
                                              ┌─────────────▼──┐   ┌────────▼──────┐  ┌─▼──────────────┐
                                              │  Sarvam AI      │   │ Google Gemini │  │ Google BigQuery│
                                              │  chat · STT·TTS │   │  vision·text  │  │   analytics    │
                                              └─────────────────┘   └───────────────┘  └────────────────┘
                                                            │
                                              ┌─────────────▼──────────────┐
                                              │  External data APIs         │
                                              │  Open-Meteo · BigDataCloud  │
                                              └─────────────────────────────┘
```

---

## 2. Frontend

**Stack:** Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS v4,
Framer Motion (animation), Recharts (charts), Supabase JS (optional auth),
`next-themes` (dark mode), `next-pwa` (opt-in offline).

**Structure:**

```
frontend/
├── app/
│   ├── page.tsx                 # Landing page (5-language i18n)
│   ├── dashboard/
│   │   ├── page.tsx             # Dashboard tile grid
│   │   ├── diagnosis/           # Crop photo → disease
│   │   ├── risk-score/          # 0–100 farm risk
│   │   ├── weather/             # 7-day forecast + advice
│   │   ├── chat/                # Ask Krishivaani (text + voice replies)
│   │   ├── voice/               # Voice Assistant (speak → hear)
│   │   ├── schemes/             # Government schemes
│   │   └── analytics/           # BigQuery-backed charts
│   ├── demo/ · docs/ · signup/
│   └── layout.tsx · loading.tsx · not-found.tsx
├── components/                  # DashboardTiles, FeatureShell, ThemeToggle, motion
└── lib/                         # api.ts (fetch helper), supabase.ts, landing-i18n.ts, utils.ts
```

**Client → server contract.** All calls go through `lib/api.ts`, which wraps
the backend's standard `{ success, data, error }` envelope, adds a request
timeout, and surfaces friendly errors. The base URL comes from
`NEXT_PUBLIC_API_URL`.

**Internationalization.** The landing page ships real translations for
English, Hindi, Marathi, Tamil, and Telugu in `lib/landing-i18n.ts` (text keyed
by locale; icons/colors stay in code).

---

## 3. Backend

**Stack:** FastAPI, Uvicorn, Pydantic v2 / pydantic-settings, httpx,
google-generativeai, google-cloud-bigquery, Pillow.

**Route groups** (`/api/v1/*`, registered in `main.py`):

| Prefix | Module | Purpose |
|---|---|---|
| `/diagnosis` | `routes/diagnosis.py` | Image upload → disease detection |
| `/weather` | `routes/weather.py` | Forecast + irrigation/disease-risk advice |
| `/risk` | `routes/risk_score.py` | 0–100 multi-factor farm risk |
| `/recommendations` | `routes/recommendations.py` | Decision cards |
| `/schemes` | `routes/schemes.py` | Government scheme matching |
| `/chat` | `routes/chat.py` | Multilingual chat **+ voice (STT/TTS)** |
| `/analytics` | `routes/analytics.py` | BigQuery aggregations |
| `/alerts` | `routes/alerts.py` | Farm alerts |

**Config.** `config.py` uses `pydantic-settings` to load a `.env` file. It
hard-requires `GOOGLE_API_KEY`, `DATABASE_URL`, and `BIGQUERY_PROJECT_ID`, and
treats Sarvam, Firebase, Redis, etc. as optional (graceful degradation).

---

## 4. Multi-Agent System

Six agents live in `backend/agents/`, each a focused unit that builds a prompt
or query and returns a typed result:

| Agent | Responsibility | Powered by |
|---|---|---|
| `ImageDiagnosisAgent` | Leaf photo → disease, severity, treatment | Gemini Vision |
| `WeatherIntelligenceAgent` | Forecast interpretation, irrigation windows | Open-Meteo + reasoning |
| `RiskPredictionAgent` | Fuse weather + disease + crop-health into a score | Rule + model logic |
| `RecommendationAgent` | Actionable "decision cards" (YES/NO/WAIT) | Sarvam / Gemini |
| `GovernmentSchemeAgent` | Match farmer to eligible schemes | Text matching |
| `AnalyticsAgent` | Event logging + BigQuery aggregations | BigQuery |

---

## 5. AI Providers

Krishivaani uses a **best-tool-per-job** strategy with automatic fallback.

### Sarvam AI (India-first — primary for language & voice)
- **Chat** — `POST https://api.sarvam.ai/v1/chat/completions`, model
  `sarvam-30b` (a reasoning model). Used for the multilingual assistant.
- **Speech-to-Text** — Saarika (`saarika:v2.5`) at
  `/speech-to-text`. Farmer speaks → transcript.
- **Text-to-Speech** — Bulbul (`bulbul:v2`) at `/text-to-speech`. Answer →
  base64 WAV, with a **natural Indian voice chosen per language**
  (Hindi → `manisha`, English → `anushka`, Tamil/Telugu → `vidya`).

All Sarvam calls live in `services/sarvam_client.py` (httpx, `api-subscription-key`
auth). Key design points:
- If `SARVAM_API_KEY` is unset or a call fails, chat **falls back to Gemini**,
  so the assistant always responds.
- Bulbul returns long text as **multiple WAV chunks**; the client merges them
  into one valid WAV (concatenating raw PCM and rewriting the header) so the
  browser can play a single file.

### Google Gemini (multimodal — vision + fallback)
- `gemini-2.5-flash` for image diagnosis (vision) and as the chat fallback.

---

## 6. Voice Pipeline (headline feature)

```
[🎙️ Browser mic]
      │  MediaRecorder → WebM/Opus
      ▼
[Frontend] decode + re-encode → 16-bit mono WAV   (AudioContext)
      │  multipart/form-data
      ▼
POST /api/v1/chat/transcribe ──▶ Sarvam Saarika (STT) ──▶ transcript
      │
      ▼
POST /api/v1/chat/message ─────▶ Sarvam sarvam-30b (Gemini fallback) ──▶ answer text
      │
      ▼
POST /api/v1/chat/speak ───────▶ Sarvam Bulbul (TTS) ──▶ merged WAV (base64)
      │
      ▼
[Frontend] <audio> playback  (Stop button interrupts)
```

The browser records WebM/Opus, but Sarvam's ASR is most reliable with WAV, so
the frontend decodes and re-encodes to 16-bit mono PCM WAV before upload.

---

## 7. Data & Analytics Pipeline

```
generate_synthetic_data.py ──▶ farm_performance_500k.csv ──▶ BigQuery (schema.sql)
                                                                    │
                              rapids_benchmark.ipynb (cuDF vs pandas)│ 22.58× avg
                                                                    ▼
                              GET /api/v1/analytics/farm-insights ──▶ Recharts + Looker
```

1. **Generate** — `analytics/generate_synthetic_data.py` creates 500K synthetic
   farm records (`farm_performance_500k.csv`).
2. **Store** — loaded into BigQuery per `database/bigquery/schema.sql` (event
   tables + `farm_performance` + analytics views, partitioned & clustered).
3. **Accelerate** — `analytics/rapids_benchmark.ipynb` benchmarks NVIDIA RAPIDS
   cuDF vs pandas on the same 500K rows (Google Colab T4 GPU):

   | Operation | Speedup |
   |---|---|
   | GroupBy aggregation | **49.8×** |
   | CSV load | 15.1× |
   | Filter | 2.8× |
   | **Average** | **22.58×** |

4. **Serve** — `AnalyticsAgent` runs BigQuery aggregations (yield-by-crop,
   risk-by-state via `JSON_EXTRACT_SCALAR`, disease-spread) behind
   `GET /api/v1/analytics/farm-insights`. Configured via a service-account JSON
   referenced by `BIGQUERY_CREDENTIALS_PATH` (never committed).
5. **Visualize** — in-app Analytics page (Recharts) + a Looker Studio dashboard.

**External APIs** — Open-Meteo (weather, no key), BigDataCloud
(reverse-geocoding, client-side).

---

## 8. Deployment

| Layer | Platform | Notes |
|---|---|---|
| Frontend | Vercel | `NEXT_PUBLIC_API_URL` points at the backend |
| Backend | Render | Web service; `.env` vars + `service-account.json` as a secret file |
| Analytics | Google BigQuery | Dataset + service account |
| Auth (optional) | Supabase | Public anon key protected by RLS |

**Backend container.** `backend/Dockerfile` builds the FastAPI service;
Uvicorn binds to `$PORT`.

---

## 9. Security Notes

- Secrets (`.env`, `service-account.json`, `*.pem`, `*.key`) are gitignored and
  never committed. Only `.env.example` (placeholders) is tracked.
- Uploads are validated by MIME type and capped at 10 MB.
- CORS allows the known frontend origins plus Vercel preview URLs.
- See the README's Security section for hardening recommendations
  (API auth, rate limiting, generic error responses).
