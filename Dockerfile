FROM python:3.12.2

WORKDIR /python

COPY . /python
RUN apt-get update && apt-get install -y wget gnupg2

# Установка ключа Google Chrome и добавление репозитория
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Обновление списка пакетов и установка Google Chrome
RUN apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Установка драйвера Chrome WebDriver
RUN LATEST=`wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 80

CMD [ "python", "main.py" ]
