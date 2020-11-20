FROM python:3

ENV CODE_DEST /opt/tou-exporter
WORKDIR ${CODE_DEST}

COPY tou-exporter.py ${CODE_DEST}

RUN pip install prometheus_client envargparse

EXPOSE 8000

CMD [ "python", "./tou-exporter.py" ]
