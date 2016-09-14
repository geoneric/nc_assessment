FROM python:3.5.2

MAINTAINER Kor de Jong <k.dejong@geoneric.eu>
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /
COPY nc_assessment /nc_assessment
COPY uwsgi.ini /
COPY cmd.sh /
COPY run_server.py /

USER uwsgi
CMD ["/cmd.sh"]
