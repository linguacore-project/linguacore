FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . uvicorn psycopg[binary]
COPY . .
CMD ["uvicorn", "linguacore.main:app", "--host", "0.0.0.0", "--port", "8000"]
