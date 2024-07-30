#use the oficial python imige as the base image
FROM python:3.9-slim-buster

#install todos los navegadores que usa esta suite
RUN apt-get update && \
    apt-get install -y chromium-driver && rm -rf /var/lib/apt/lists/*
#upgradee pip
RUN pip install --upgrade pip
# copy & install todas las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#copy de dire
COPY . /app
WORKDIR /app
# iniciar un servidor virtual en segundo plano
ENV DISPLAY=:99
CMD Xvfb $DISPLAY -ac -screen 0 1280x24 &
ENTRYPOINT ["pytest","--allure=allure_results"]