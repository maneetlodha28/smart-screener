# Smart Screener Backend

Minimal FastAPI backend scaffold for an AI-powered Indian stock screener.

## Running the server

From within `backend/`:

```bash
python -m uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/health` to verify the service is running.

## Testing

Run the test suite with:

```bash
pytest
```
