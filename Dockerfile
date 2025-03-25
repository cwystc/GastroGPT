FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ✅ Set env so nltk knows where to find resources
ENV NLTK_DATA=/root/nltk_data

# ✅ Download nltk resources to that path
RUN python -m nltk.downloader -d /root/nltk_data punkt stopwords wordnet

CMD ["python", "main.py"]
