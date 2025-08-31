FROM python:3.11-slim

WORKDIR /workspaces/smart-screener/backend
COPY . /workspaces/smart-screener/backend

RUN pip install --no-cache-dir .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
