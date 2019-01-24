FROM python:3

COPY src/lib /app/lib
COPY src/bin /app/bin

WORKDIR /app/bin

RUN pip install -r requirements.txt

CMD python main.py