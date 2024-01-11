FROM python:3.12-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# ENV PYTHONUNBUFFERED=0


COPY ./app /app
COPY ./data /data
COPY ./python /python
COPY ./sql /sql
RUN python /sql/execute.py

EXPOSE 8501

WORKDIR /app

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
