<a id="readme-top"></a>

<div align="center">

<h1>🌾 Chaupal.AI (चौपाल.AI)</h1>

### The Village Square, Reimagined with AI — Speak, Snap, Decide.

*A **chaupal** (चौपाल) is the traditional village gathering where farmers meet to discuss problems and make decisions. Chaupal.AI brings that decision-making space online: snap a leaf photo, ask any farming question by voice in your own language, and get a clear decision — not just data. Built for climate-resilient farming.*

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-View_App-22c55e?style=for-the-badge)]()
[![API Docs](https://img.shields.io/badge/⚙️_API-Swagger-46E3B7?style=for-the-badge)](https://krisisar-ai.onrender.com/docs)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github)](https://github.com/yash0238/CropRakshak)

[![Next.js](https://img.shields.io/badge/Next.js_15-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Sarvam AI](https://img.shields.io/badge/Sarvam_AI-FF6B00?style=for-the-badge)](https://www.sarvam.ai/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![NVIDIA RAPIDS](https://img.shields.io/badge/NVIDIA_RAPIDS-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://rapids.ai/)

> 🏆 Built for **HACKHAZARDS '26** — Theme: **🌍 Climate & Sustainability Systems** · Track: **Sarvam AI**

</div>

---

<details>
<summary><strong>📑 Table of Contents</strong></summary>

- [The Problem](#the-problem)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [Voice Assistant — Our Standout Feature](#voice-assistant--our-standout-feature)
- [Results & Impact](#results--impact)
- [Screenshots](#screenshots)
- [HACKHAZARDS Alignment](#hackhazards-alignment)
- [Built With](#built-with)
- [Architecture](#architecture)
- [Data Pipeline](#data-pipeline)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Team](#team)
- [License](#license)
- [Acknowledgments](#acknowledgments)

</details>

---

## The Problem

Farmers make high-stakes decisions every day — when to irrigate, which pesticide to spray, whether a leaf spot is a real threat. Yet the information they need is scattered across weather apps, YouTube, WhatsApp groups, and local dealers. Worse, most agri-tools are **English-only and text-first**, locking out the millions of farmers who are more comfortable *speaking* in Hindi, Marathi, Tamil, or Telugu.

The result: poor timing, wasted water and chemicals, undiagnosed disease, and lost income — all made sharper by an increasingly volatile climate.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Our Solution

**Chaupal.AI turns fragmented information into confident decisions — and it works by voice.** It unifies diagnosis, weather, risk, schemes, and a multilingual AI assistant into one platform that returns *decisions, not just data*. A farmer can simply speak a question in their language and hear the answer read back.

- 📸 Snap a leaf photo → instant disease diagnosis + targeted treatment (less pesticide waste).
- 🎙️ Speak a question → hear a spoken answer in your language (built for low-literacy, hands-free field use).
- 🎯 Check a live 0–100 farm risk score built from weather, disease, and crop-health signals.
- 💧 Get water-smart irrigation guidance that cuts resource waste.
- 📊 Explore national-scale analytics powered by a GPU-accelerated data pipeline.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Key Features

| Feature | What it does | Powered by |
|---|---|---|
| 🎙️ **Voice Assistant** | Speak in 5 languages, hear the answer aloud — full speech loop | Sarvam Saarika (STT) + Bulbul (TTS) |
| 💬 **Multilingual Chat** | Ask any farming question in your language | Sarvam `sarvam-30b` (Gemini fallback) |
| 📸 **Crop Diagnosis** | Photo → disease detection, severity, and treatment | Google Gemini Vision |
| 🎯 **Farm Risk Score** | Live 0–100 risk from multi-factor analysis | Weather + disease + crop-health |
| 🌤️ **Weather Intelligence** | 7-day forecast + irrigation & disease-risk advice | Open-Meteo |
| 🏛️ **Government Schemes** | Match to schemes you're eligible for | Scheme matching |
| 📊 **Analytics Dashboard** | Yield, risk, and disease insights over 500K records | BigQuery + RAPIDS |
| 🌐 **Multilingual UI** | Landing page in English, Hindi, Marathi, Tamil, Telugu | Built-in i18n |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Voice Assistant — Our Standout Feature

Most agri-apps stop at English text boxes. Chaupal.AI closes the loop with a **full voice pipeline** in five Indian languages, powered end-to-end by Sarvam AI:

```
🎙️ Speak  →  Sarvam Saarika (STT)  →  Sarvam sarvam-30b  →  Sarvam Bulbul (TTS)  →  🔊 Hear
```

- **Speak your question** — tap the mic on the Voice page (`/dashboard/voice`) or the chat page and talk naturally in Hindi, Marathi, Tamil, Telugu, or English.
- **Hear the answer** — replies are read aloud with a **natural Indian voice chosen per language** (Hindi → *manisha*, English → *anushka*, Tamil/Telugu → *vidya*).
- **Hands-free & inclusive** — designed for low-literacy farmers and real field conditions. A **Stop** button interrupts playback anytime.
- **Robust by design** — the browser records WebM, which we re-encode to WAV for reliable transcription; Bulbul's multi-chunk audio is merged server-side into a single playable file; and if Sarvam is unavailable, chat automatically falls back to Gemini.

> This is why we chose the **Sarvam AI track**: voice + Indian languages are exactly where Sarvam shines, and exactly what the last-mile farmer needs. Just like a real *chaupal*, every farmer gets heard — in their own language, out loud.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Results & Impact

<div align="center">

| 📦 Data scale | ⚡ GPU speedup | 🎙️ Voice languages | 🌐 UI languages |
|:---:|:---:|:---:|:---:|
| **500,000** farm records | **22.58×** avg (49.8× GroupBy) | **5** | **5** |

</div>

- **Acceleration evidence.** NVIDIA RAPIDS cuDF processes the same 500K-row analytics **22.58× faster on average** than pandas on a Google Colab T4 GPU — GroupBy aggregations run **49.8× faster**. This is what makes real-time insight viable at national farmer scale. See [`analytics/rapids_benchmark.ipynb`](./analytics/rapids_benchmark.ipynb).
- **Real, queryable warehouse.** The Analytics dashboard is served from a Google BigQuery dataset (see [`database/bigquery/schema.sql`](./database/bigquery/schema.sql)) — yield by crop, risk by state, and disease spread.
- **Voice-first inclusion.** The full speak→answer→listen loop works in 5 Indian languages, bringing AI advice to farmers who can't (or prefer not to) type.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Screenshots

<div align="center">

### ⚡ NVIDIA RAPIDS — 22.58× average speedup (49.8× on GroupBy), 500K records
<img src="docs/screenshots/rapids-benchmark.png" alt="Pandas vs cuDF benchmark — 22.58x average speedup" width="90%"/>

### 📊 BigQuery + Looker Studio Analytics
<table>
  <tr>
    <td width="60%"><img src="docs/screenshots/looker-yield-by-crop.png" alt="Average yield by crop"/></td>
    <td width="40%"><img src="docs/screenshots/looker-crop-distribution.png" alt="Crop distribution"/></td>
  </tr>
  <tr>
    <td><img src="docs/screenshots/looker-yield-scatter.png" alt="Yield vs farm size"/></td>
    <td><img src="docs/screenshots/looker-scorecards.png" alt="Key metrics — 500,000 farms analyzed"/></td>
  </tr>
</table>

</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## HACKHAZARDS Alignment

**Theme — 🌍 Climate & Sustainability Systems.** Chaupal.AI is agri-tech for climate resilience: it reduces water and pesticide waste through targeted, timely advice, and helps farmers act before climate shocks cause losses.

**Track — Sarvam AI.** We use Sarvam across the full language stack — chat (`sarvam-30b`), speech-to-text (Saarika), and text-to-speech (Bulbul) — to make the platform usable by voice, in five Indian languages.

| Judging lens | How Chaupal.AI delivers |
|---|---|
| Real user & problem | Farmers deciding irrigation / pesticide / disease action, in their own language |
| Meaningful use of the track tech | Sarvam powers chat **and** the full voice loop (STT + TTS) in 5 languages |
| Working product | 7 live dashboard tools on a deployed Next.js + FastAPI stack |
| Data & acceleration | BigQuery warehouse (500K rows) + NVIDIA RAPIDS cuDF (22.58× avg speedup) |
| Sustainability impact | Water-smart irrigation, reduced chemical overuse, climate risk scoring |
| Inclusivity | Voice-first + multilingual — built for low-literacy, last-mile access |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

**Frontend** — Next.js 15 · React 19 · TypeScript · Tailwind CSS v4 · Recharts · Framer Motion
**Backend** — FastAPI · Python 3.11+ · Pydantic v2 · multi-agent design (6 agents)
**AI** — Sarvam AI (chat · Saarika STT · Bulbul TTS) · Google Gemini (vision + fallback)
**Data & Analytics** — Google BigQuery · NVIDIA RAPIDS cuDF · Looker Studio
**Infra** — Vercel (frontend) · Render (backend) · Supabase (optional auth)
**External APIs** — Open-Meteo · BigDataCloud

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Architecture

Chaupal.AI is a Next.js frontend talking to a FastAPI backend that orchestrates 6 AI agents across Sarvam AI, Google Gemini, and BigQuery.

```
┌──────────────────────────────┐        ┌───────────────────────────────┐
│   Next.js 15 (Vercel)        │  REST  │   FastAPI (Render)            │
│   Landing · Dashboard · Voice ├───────►│   8 route groups · 6 agents   │
└──────────────────────────────┘        └────┬──────────┬──────────┬─────┘
                                              │          │          │
                                     ┌────────▼───┐ ┌────▼─────┐ ┌──▼──────────┐
                                     │  Sarvam AI │ │  Gemini  │ │  BigQuery   │
                                     │ chat·STT·TTS│ │  vision  │ │  + RAPIDS   │
                                     └────────────┘ └──────────┘ └─────────────┘
```

> 📐 Full details — agents, AI providers, the voice pipeline, and the data/GPU pipeline — are in **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Data Pipeline

1. **Generate** — 500K synthetic farm records via [`analytics/generate_synthetic_data.py`](./analytics/generate_synthetic_data.py) → `farm_performance_500k.csv`.
2. **Store** — load into a BigQuery dataset ([`database/bigquery/schema.sql`](./database/bigquery/schema.sql): tables + analytics views).
3. **Accelerate** — [`analytics/rapids_benchmark.ipynb`](./analytics/rapids_benchmark.ipynb) proves a 22.58× average (49.8× GroupBy) speedup of cuDF vs pandas on a Colab T4 GPU.
4. **Serve** — `GET /api/v1/analytics/farm-insights` aggregates yield by crop, risk by state, and disease spread.
5. **Visualize** — the in-app Analytics page (Recharts) + a Looker Studio dashboard.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites
- **Node.js 22+** and **pnpm 9+**
- **Python 3.11+**
- A **Google Gemini** API key ([ai.google.dev](https://ai.google.dev/))
- A **Sarvam AI** API key ([dashboard.sarvam.ai](https://dashboard.sarvam.ai/)) — for chat + voice
- *(Optional)* A Google Cloud project with BigQuery + a service-account JSON, for the analytics dashboard

### 1. Clone
```sh
git clone https://github.com/yash0238/CropRakshak.git
cd CropRakshak
```

### 2. Backend (FastAPI)
```sh
cd backend
python -m venv venv
venv\Scripts\activate            # Windows  (source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
# create .env (see Environment Variables) + add service-account.json for BigQuery
python main.py                   # http://localhost:8000  (Swagger at /docs)
```

### 3. Frontend (Next.js)
```sh
cd frontend
pnpm install
# create .env.local (see Environment Variables)
pnpm dev                         # http://localhost:3000
```

Open **http://localhost:3000**, go to the dashboard, and try the **Voice Assistant**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Environment Variables

**`frontend/.env.local`**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
# Optional (auth): app runs fine without these
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**`backend/.env`** — `GOOGLE_API_KEY`, `DATABASE_URL`, and `BIGQUERY_PROJECT_ID` are required; the rest are optional.
```env
GOOGLE_API_KEY=your_gemini_api_key
SARVAM_API_KEY=your_sarvam_api_key          # enables chat + voice
DATABASE_URL=postgresql://user:pass@host:5432/db
BIGQUERY_PROJECT_ID=your_gcp_project_id
BIGQUERY_DATASET_ID=krisisar_analytics
BIGQUERY_CREDENTIALS_PATH=./service-account.json
OPEN_METEO_API_URL=https://api.open-meteo.com/v1/forecast
SECRET_KEY=change-me-to-a-random-string
```

> ⚠️ `.env`, `.env.local`, and `service-account.json` are **gitignored** and must never be committed. In production, set them as platform environment variables / secret files.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Project Structure

```
Chaupal.AI/
├── frontend/                 # Next.js 15 app
│   ├── app/
│   │   ├── page.tsx          # Multilingual landing page
│   │   └── dashboard/        # 7 tools incl. voice/ and chat/
│   ├── components/           # DashboardTiles, FeatureShell, ...
│   └── lib/                  # api.ts, landing-i18n.ts, supabase.ts
├── backend/                  # FastAPI service
│   ├── agents/               # 6 AI agents
│   ├── api/routes/           # 8 route groups (incl. chat = text + voice)
│   ├── services/             # sarvam_client.py (chat · STT · TTS)
│   ├── config.py · main.py
│   └── requirements.txt
├── analytics/                # synthetic data generator + RAPIDS benchmark
├── database/bigquery/        # schema.sql (tables + views)
├── docs/screenshots/         # RAPIDS + Looker screenshots
├── ARCHITECTURE.md           # System design deep-dive
├── LICENSE
└── README.md
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [x] Multi-agent FastAPI backend (diagnosis, weather, risk, recommendation, schemes, analytics)
- [x] Multilingual AI chat via Sarvam (`sarvam-30b`) with Gemini fallback
- [x] **Voice Assistant** — full Sarvam STT + TTS loop in 5 languages
- [x] Gemini Vision crop diagnosis
- [x] BigQuery pipeline + 500K-record analytics
- [x] NVIDIA RAPIDS cuDF benchmark (22.58× average speedup)
- [x] Multilingual landing page (5 languages)
- [ ] Full multilingual support across all dashboard pages
- [ ] Offline-first PWA for low-connectivity areas
- [ ] Live data.gov.in ingestion (mandi prices, rainfall)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Team

Built with 🌱 for HACKHAZARDS '26 by:

- **Yashovardhan Thopte**
- **Ritik Gupta**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

- [Sarvam AI](https://www.sarvam.ai/) — India-first LLM, speech-to-text, and text-to-speech
- [Google Gemini](https://ai.google.dev/) · [BigQuery](https://cloud.google.com/bigquery) · [Looker Studio](https://lookerstudio.google.com/)
- [NVIDIA RAPIDS](https://rapids.ai/)
- [Open-Meteo](https://open-meteo.com/) · [BigDataCloud](https://www.bigdatacloud.com/)
- [Vercel](https://vercel.com/) · [Render](https://render.com/) · [Supabase](https://supabase.com/)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) for structure inspiration

<p align="right">(<a href="#readme-top">back to top</a>)</p>
