FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev tzdata \
     && cp -r -f /usr/share/zoneinfo/Europe/Moscow /etc/localtime
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python","-u","code.py"]
