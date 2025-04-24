FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y texlive-latex-base texlive-luatex texlive-fonts-recommended texlive-lang-cjk fonts-noto-cjk && \
    apt-get clean

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
