FROM python:3.10-slim

WORKDIR CODE/
COPY req.txt .
RUN pip install -r req.txt
COPY . .
CMD python run.py