# smart-screener

[![CI](https://github.com/OWNER/smart-screener/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/smart-screener/actions/workflows/ci.yml)

This repository contains a backend FastAPI service and a React frontend.

> **Disclaimer:** This project is for educational purposes only and does not
constitute investment advice.

## Local development with Docker

Ensure Docker is installed. The project ships with a compose setup that runs
PostgreSQL, the backend API, and the frontend.

```
make dev
```

The frontend will be available at http://localhost:5173 and the backend at
http://localhost:8000/health. To stop the stack:

```
make down
```

## Frontend standalone

```
cd frontend
npm install
npm run dev
```

Run tests:

```
cd frontend
npm test
```

## Backend standalone

```
cd backend
PYTHONPATH=. pytest
```
