FROM python:3.7-alpine

ENV PYTHONIOENCODING utf-8

WORKDIR /app

RUN apk add --no-cache curl fontconfig ttf-freefont chromium chromium-chromedriver

RUN curl -O https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip \
  && mkdir -p /usr/share/fonts/NotoSansCJKjp \
  && unzip NotoSansCJKjp-hinted.zip -d /usr/share/fonts/NotoSansCJKjp/ \
  && rm NotoSansCJKjp-hinted.zip \
  && fc-cache -fv

RUN pip install selenium
