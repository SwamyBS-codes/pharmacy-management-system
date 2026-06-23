# Pharmacy Management System — Smart Pharmacy Inventory & POS Network

Backend and frontend for Pharmacy Management System, a secure, role-based platform that coordinates pharmacy operations, tracks inventory expiration, processes POS billing, and integrates Machine Learning models for sales forecasting and reorder recommendation. The lightweight Flask REST API backend communicates with a PostgreSQL database, while the React + Vite frontend provides an interactive, modern user experience with integrated real-time barcode scanning.

This repository is a modular monorepo containing both the Flask Python backend, the React + Vite frontend, and the machine learning forecasting model components.

New here? This README gets you from a fresh clone to a running application configured for local development and testing.

## Table of contents
- Tech stack
- Architecture
- Prerequisites
- Getting started
- Environment variables
- Running the app
- Project structure
- Modules
- Authentication & authorization
- Testing (Local Development)
- Scripts reference
- Coding conventions
- Troubleshooting

## Tech stack
| Area | Technology |
| :--- | :--- |
| Runtime | Python 3.8+ / Node.js 18+ (LTS) |
| Frontend Framework | React 18 (Vite, Tailwind CSS, Radix UI) |
| Backend Framework | Flask (Python) + psycopg2-binary |
| Auth / Security | JWT (JSON Web Tokens) & bcrypt password hashing |
| ML / Analytics | scikit-learn, joblib, pandas, numpy |
| Database | PostgreSQL |
| Invoicing & Utilities | ReportLab & Pillow (PDF generation), html5-qrcode (barcode scanning) |

## Architecture
```
             HTTP REST API / JSON
       ┌─────────────────────────┐
       │                         │
       ▼                         ▼
┌──────────────┐          ┌──────────────┐
│ React Client │          │ Flask Backend│
│  (Frontend)  │          │   (API/ML)   │
└──────┬───────┘          └──────┬───────┘
       │                         │
       └─────────────────────────┘
           PostgreSQL DB Pool
```

Modular monolith design. 
- The backend is separated into clean blueprints and controllers inside `backend/src/`.
- The frontend is built as a Single Page Application (SPA) with a dedicated dashboard, custom hooks, and page-based routing.
- The Machine learning pipeline is integrated into the backend using `scikit-learn` to process historical sales data and supply dynamic predictions (reorders, seasonal demand).
- Automated PDF invoicing is generated server-side using ReportLab.
- Real-time client-side barcode scanning using `html5-qrcode` integration with the database.

## Prerequisites
- Python 3.8 or 3.10+ (LTS recommended) and pip.
- Node.js 18.x or 20.x and npm or pnpm.
- PostgreSQL database instance (local or hosted).

## Getting started
### 1. Clone and install
```bash
git clone <repo-url> pharmacy
cd pharmacy

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # on Windows use: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Create your env files
Create a `.env` file in the root or set environment variables directly.

### 3. Verify health
```bash
curl http://localhost:5000/api/health
```

## Environment variables
Configuration is read from standard environment variables (or `.env` files).

### Backend Variables
| Variable | Required | Description |
| :--- | :--- | :--- |
| DB_HOST | yes | Database host address (e.g. `localhost`). |
| DB_PORT | no | Database port number (default `5432`). |
| DB_NAME | yes | Database name. |
| DB_USER | yes | Database user name. |
| DB_PASSWORD | yes | Database user password. |
| SECRET_KEY | yes | Secret key used to sign and verify JWT tokens. |
| PYTHON_PORT | no | Port number the backend server binds to (default `5000`). |
| DEBUG | no | Set to `True` for development, `False` for production. |
| ADMIN_SETUP_KEY | no | Secure setup bootstrap key for administrative tasks (dev only). |

### Frontend Variables
| Variable | Required | Description |
| :--- | :--- | :--- |
| VITE_API_URL | no | REST API endpoint URL (default is proxying to `/api` via Vite server). |

## Running the app
```bash
# Start backend (from backend directory)
source venv/bin/activate
python src/app.py

# Start frontend (from frontend directory)
npm run dev
```
Base URL: `http://localhost:5173` (Frontend) / `http://localhost:5000` (Backend)

## Project structure
```
pharmacy/
├── backend/                 # Python Flask Backend
│   ├── src/                 # Application Source
│   │   ├── app.py           # Main bootstrapper & blueprints register
│   │   ├── config.py        # Configuration manager
│   │   ├── db.py            # Database setup & connection pool
│   │   ├── auth.py          # Authentication blueprint
│   │   ├── predictions.py   # Machine Learning predictions API
│   │   ├── billing.py       # Invoices & PDF generation API
│   │   └── inventory.py     # Inventory tracking API
│   ├── schema.sql           # Database tables schema definition
│   └── requirements.txt     # Python requirements
├── frontend/                # React SPA Frontend
│   ├── src/
│   │   ├── main.tsx         # SPA entry point
│   │   ├── App.tsx          # Route layout component
│   │   ├── components/      # Reusable UI widgets
│   │   └── pages/           # Admin pages, POS, billing, predictions
├── model/                   # Machine learning models & scripts
│   ├── train.py             # Script to train forecasting models
│   ├── prediction.py        # Local testing inference pipeline
│   ├── sales_prediction_model.pkl # Trained Random Forest model
│   └── historical_sales.csv # Dataset for sales training
```

## Modules
### Backend Modules
| Module | Responsibility |
| :--- | :--- |
| auth | Manages registration, authentication, JWT tokens, and user status. |
| inventory | Manages stock batches, low-stock notifications, and barcode associations. |
| billing | Generates customer purchase invoices and handles ReportLab PDF generation. |
| predictions | Loads joblib ML models to estimate medicine demand, reorders, and seasonal changes. |
| sales | Coordinates POS transactions, sale records, and updates inventory stock levels. |

### Frontend Modules
| Module | Responsibility |
| :--- | :--- |
| POS / Billing | Handles item cart scanning, pricing calculations, and transaction checkout. |
| BarcodeScanner | Interface to stream video feed and scan barcodes using the device camera. |
| PredictionsContent | Graphs and analytics highlighting future sales forecasting and critical reorders. |
| Inventory | Manages active batches, updates expiry status, and monitors low-stock alerts. |

### Machine Learning Modules
| Module | Responsibility |
| :--- | :--- |
| train.py | Runs scikit-learn models on historical data to generate serialized pkl weights. |
| prediction.py | Local prediction scripts to forecast future sales demand using weather features. |
| classify.py | Script to categorize medicines and determine primary tags for seasonal demand. |

## Authentication & authorization
- **Tokens**: JWT (JSON Web Tokens) are generated upon successful login. The backend signs the tokens using the configured `SECRET_KEY`.
- **Verification**: Secure routes require an `Authorization` header containing the JWT token. The backend verifies the token validation, extracts the user role (`ADMIN` or `EMPLOYEE`), and denies request access on failure.
- **Roles**: Role-based decorators restrict administrative operations (e.g. creating/deactivating users, resetting passwords, and viewing database-wide statistics) to `ADMIN` users only.

## Testing (Local Development)
The project includes test configurations to run locally during development:
- **Backend**: Multiple validation and API flow test scripts are located under the `backend/src/` directory. You can run them using:
  ```bash
  # Test the general auth flow
  python src/test_auth_flow.py

  # Test endpoint responses
  python src/test_endpoints.py

  # Test sales and prediction modules
  python src/test_sales_api.py
  python src/test_predictions.py
  ```
- **Frontend**: Unit tests for utilities are written with Vitest and can be executed via:
  ```bash
  npm run test
  ```
## Scripts reference
### Backend Scripts
| Script | Purpose |
| :--- | :--- |
| `python src/app.py` | Starts the Flask development server on port 5000. |
| `python src/initialize_db.py` | Boots schema tables and initial roles mapping inside the database. |
| `python src/reset_admin_password.py` | Resets administrative passwords securely (requires setup keys). |

### Frontend Scripts
| Script | Purpose |
| :--- | :--- |
| `npm run dev` | Runs the local Vite development server on port 5173. |
| `npm run build` | Compiles production assets into `dist/spa` and node server into `dist/server`. |
| `npm run start` | Boots the built production host to serve static client assets. |
| `npm run test` | Executes unit tests using Vitest. |

## Coding conventions
- Blueprints-oriented routing on the Flask server for modular features separation.
- Component-driven development on the React frontend using Radix UI primitives.
- Separation of concerns for ML processing—models load once at boot time, and fall back to local database statistics if pickle files are not found.
- Consistent snake_case for Python parameters/endpoints and camelCase for React hooks/handlers.

## Troubleshooting
| Symptom | Fix |
| :--- | :--- |
| Flask connection rejected | Ensure that the database container/service is running and accessible on the port configured in `.env`. |
| ML Predictions return 503 | Make sure `sales_prediction_model.pkl` and `model_encodings.pkl` exist in the `model/` directory. Run `python model/train.py` to recreate them. |
| Barcode scanner fails to load | Camera capture requires HTTPS or localhost origins. Check browser camera permissions in site preferences. |
| CORS errors in frontend console | Ensure the frontend domain (e.g. `http://localhost:5173`) is listed inside the backend's allowed CORS origins list. |
