FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
CORY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver
COPY . /app/

