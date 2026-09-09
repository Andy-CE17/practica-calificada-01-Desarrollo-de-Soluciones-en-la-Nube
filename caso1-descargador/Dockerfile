FROM node:22-bookworm-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . .

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

RUN mkdir -p downloads

EXPOSE 5000

CMD ["python3", "app.py"]
