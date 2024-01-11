FROM python:3.12-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# Mettez à jour le système et installez les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*
    

# Installer Chrome et ses dépendances
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver    
    
   
# Installez Selenium
RUN pip install selenium



RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet

# ENV PYTHONUNBUFFERED=0


COPY ./app /app
COPY ./data /data
COPY ./python /python
COPY ./sql /sql
RUN python /sql/execute.py

EXPOSE 8501

WORKDIR /app

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
