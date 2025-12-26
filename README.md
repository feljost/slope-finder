<div align="center">

# Slope Finder

**Find the perfect Swiss ski resort based on your location and travel dates.**

[![Website](https://img.shields.io/badge/Live_Site-slopefinder.ch-blue?style=for-the-badge&logo=google-chrome)](https://slopefinder.ch)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=white)](https://docs.astral.sh/uv/)

</div>


## 🏔️ About The Project

**Slope Finder** solves the problem of deciding where to ski by calculating the real travel effort required to reach Swiss resorts. Unlike standard map searches, it combines travel logistics with live resort conditions.

Simply enter your location and date, and the application provides a ranked list of resorts, complete with driving times, snow depths, and weather forecasts.

## ✨ Key Features

* **Smart Travel Routing:** Calculates distance and driving or transit duration from your specific location to the resort.
* **Live Conditions:** Real-time snow depths, piste status, and lift information.
* **Weather Intelligence:** 24h forecasts including snowfall, temperature, and visibility.
* **Responsive UI:** Infinite scrolling lists and mobile-optimized design.
* **Search & Filter:** Filter resorts by availability and travel dates.

## Mobile Demo

<div align="center">
  <video src=".github/assets/demo-mobile.mp4" controls width="300"></video>
</div>

## 🛠️ Architecture & Tech Stack

The project is split into two distinct services, both containerized for deployment on Google Cloud Run.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React, TypeScript, Vite | A responsive SPA that handles location inputs and displays resort cards. |
| **Backend** | Python, FastAPI, uv | REST API that aggregates weather data, calculates geodesic distances, and manages resort metadata. |
| **Infra** | Docker, Google Cloud Run | Stateless container deployment. |

## 🚀 Getting Started

To run the full stack locally, you will need to run the backend and frontend in separate terminal instances.

### Prerequisites
* **Node.js** (v18+)
* **Python** (v3.10+)
* **uv** (Python package manager)

### 1. Run the Backend
Navigate to the backend directory to start the API server.

```bash
cd backend

# Create virtual environment and install dependencies
uv venv
uv pip install -e .

# Start the server (default port: 8000)
uvicorn slope_finder_be.api.main:app --reload
```

The API docs will be available at http://127.0.0.1:8000/docs

### 2. Run the Frontend

Open a new terminal and navigate to the frontend directory.

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be running at http://localhost:3000 (or the port shown in your terminal).

### 📦 Deployment

Both services include a Dockerfile optimized for Google Cloud Run. Simply create two instances, one for the backend and one for the frontend, and link the respective dockerfiles at `frontend/Dockerfile` and `backend/Dockerfile`

See the specific README.md in the /backend or /frontend folders for  environment variable configurations needed.