FROM python:3.10-slim-bookworm

# Update packages
RUN apt-get update && apt-get upgrade -y

# Install required packages & build dependencies for native C-accelerated crypto (tgcrypto)
RUN apt-get install -y git curl wget bash neofetch ffmpeg software-properties-common \
    build-essential gcc g++ python3-dev libffi-dev libssl-dev

# Optimal I/O runtime flags
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Working directory
WORKDIR /app

# Copy requirements first (cache fast build)
COPY requirements.txt .

# Install python deps
RUN pip install --upgrade pip wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Port expose
EXPOSE 5000

# Start flask + bot
CMD flask run -h 0.0.0.0 -p 5000 & python3 main.py
