FROM python:3.9-alpine3.16

COPY requirements.txt app/requirements.txt
COPY . .
WORKDIR /app
EXPOSE 8000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN adduser --disabled-password service-user

USER service-user
CMD ["uvicorn", "search-service:app", "--host", "0.0.0.0", "--port", "8000"]
