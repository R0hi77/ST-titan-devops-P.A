FROM python:slim-bullseye

LABEL maintainer="Petersburg-Lab-Exercise-3"
LABEL version="1.0"

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python","app.py"]