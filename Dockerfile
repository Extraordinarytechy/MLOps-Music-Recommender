FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./melorec ./melorec

# Copy the trained model
COPY ./melorec/models/svd_model.joblib ./melorec/models/svd_model.joblib

EXPOSE 8000

CMD ["uvicorn", "melorec.api.main:app", "--host", "0.0.0.0", "--port", "8000"]