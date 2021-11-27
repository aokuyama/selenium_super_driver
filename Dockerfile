FROM public.ecr.aws/lambda/python:3.7 as build
RUN mkdir -p /opt/chromium && chmod 777 /opt/chromium
RUN curl -SL https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip > /tmp/chromedriver.zip && \
    curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip > /tmp/headless-chromium.zip && \
    unzip /tmp/chromedriver.zip -d /opt/chromium/ && \
    unzip /tmp/headless-chromium.zip -d /opt/chromium/

FROM public.ecr.aws/lambda/python:3.7

ENV PYTHONIOENCODING utf-8
RUN python -m pip install --upgrade pip

RUN mkdir -p /opt/chromium && chmod 777 /opt/chromium
COPY --from=build /opt/chromium/headless-chromium /opt/chromium
COPY --from=build /opt/chromium/chromedriver /opt/chromium

RUN yum install -y git
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./selenium_super_driver ./

ENTRYPOINT [ "python" ]
