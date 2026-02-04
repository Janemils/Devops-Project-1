# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
# Copy requirements.txt from Day01
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
# Copy all app files from Day01
COPY . . 
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

