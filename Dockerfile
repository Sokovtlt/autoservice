FROM python:3.11.4-alpine

ENV PYTHONBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r /usr/src/app/requirements.txt

#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app

# Добавляем права на выполнение для entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
