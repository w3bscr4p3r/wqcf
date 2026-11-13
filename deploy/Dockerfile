FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY api/pyproject.toml /app/pyproject.toml
COPY api/src /app/src
RUN pip install --no-cache-dir .
USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "wqcf_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
