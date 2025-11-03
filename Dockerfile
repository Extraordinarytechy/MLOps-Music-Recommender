FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#    Install build-essential (which includes gcc) and python3-dev
RUN apt-get update && apt-get install -y build-essential python3-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./melorec ./melorec

COPY ./melorec/models/svd_model.joblib ./melorec/models/svd_model.joblib

EXPOSE 8000

CMD ["uvicorn", "melorec.api.main:app", "--host", "0.0.0.0", "--port", "8000"]