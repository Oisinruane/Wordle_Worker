# Start with a Python base image
FROM python:3.13.1-slim

# Set the working directory
WORKDIR /app

# Step 1: Install Google Chrome and its dependencies
RUN apt-get update && apt-get install -y wget gnupg unzip && rm -rf /var/lib/apt/lists/*
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable \
    libnss3-dev libgconf-2-4 libasound2 libatk1.0-0 libcups2 libgdk-pixbuf2.0-0 libxss1 libappindicator1 libxtst6 fonts-liberation xdg-utils --no-install-recommends

# Step 2: Install Chromedriver using the new, robust method
RUN wget -q -O /tmp/chrome-headless-shell.zip "https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.138/linux64/chrome-headless-shell-linux64.zip" && \
    unzip -q /tmp/chrome-headless-shell.zip -d /tmp/ && \
    mv /tmp/chrome-headless-shell-linux64/chrome-headless-shell /usr/local/bin/ && \
    rm /tmp/chrome-headless-shell.zip

RUN wget -q -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.138/linux64/chromedriver-linux64.zip" && \
    unzip -q /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# In your Dockerfile
ENV PYTHONUNBUFFERED=1

# The rest of your Dockerfile
COPY requirements.txt ./
COPY results.csv ./
COPY word_scores.csv ./
COPY WebServer.py ./
COPY Play_Script.py ./
COPY main.py ./
COPY templates/index.html templates/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "main.py"]