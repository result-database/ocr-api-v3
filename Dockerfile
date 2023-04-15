FROM ubuntu:22.04

WORKDIR /app

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y curl gnupg
RUN echo "deb https://ppa.launchpadcontent.net/alex-p/tesseract-ocr5/ubuntu jammy main" >> /etc/apt/sources.list \
    && echo "deb-src https://ppa.launchpadcontent.net/alex-p/tesseract-ocr5/ubuntu jammy main" >> /etc/apt/sources.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8529B1E0F8BF7F65C12FABB0A4BCBD87CEF9E52D
RUN apt-get update
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip
RUN apt-get -y install tesseract-ocr tesseract-ocr-jpn libtesseract-dev libleptonica-dev tesseract-ocr-script-jpan libgl1-mesa-dev
RUN apt update
RUN apt install -y python3-dev libpq-dev
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python3 -m pip install -r /app/requirements.txt --no-cache-dir

COPY app/ /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
