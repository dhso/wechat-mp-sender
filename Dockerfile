FROM python:2.7-alpine3.6

ENV APPID ''
ENV APPSECRET ''
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD  python ./wxmsg.py $APPID $APPSECRET