FROM python:3.10-slim

WORKDIR CODE/
COPY req.txt .
RUN apt-get update && apt-get install -y ffmpeg
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r req.txt
COPY . .
CMD python run.py