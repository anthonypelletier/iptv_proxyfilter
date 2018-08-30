FROM python:3
MAINTAINER Anthony PELLETIER <contact@anthonypelletier.fr>

RUN apt-get update \
	&& apt-get install -y \
		supervisor \
		nginx \
	&& pip install --no-cache-dir --upgrade \
		pip \
		uwsgi \
		flask

ADD ./src/requirements.txt /opt/requirements.txt

RUN if [ -s /opt/requirements.txt ]; then pip install -r /opt/requirements.txt; fi \
	&& rm -rf /var/cache/* \
	&& rm -rf /root/.cache/* \
	&& rm -rf /tmp/*

ADD ./rootfs/ /
ADD ./src/ /opt/

WORKDIR /opt/

ENV PROJECT_NAME iptv_proxyfilter
ENV DEBUG False

EXPOSE 80

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
