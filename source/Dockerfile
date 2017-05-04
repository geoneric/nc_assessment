FROM posbank.geoneric.eu:5000/nca/nc_base:latest

MAINTAINER Kor de Jong <k.dejong@geoneric.eu>

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY nc_assessment /nc_assessment
COPY test /test

CMD ["/cmd.sh"]
