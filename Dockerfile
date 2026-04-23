FROM wordle-base

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
COPY results.csv ./
COPY word_scores.csv ./
COPY WebServer.py ./
COPY Play_Script.py ./
COPY main.py ./
COPY templates/index.html templates/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "main.py"]
