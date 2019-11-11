FROM python:3.7

EXPOSE 80/tcp
EXPOSE 9191/tcp

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
  libatlas-base-dev \
  gfortran \
  nginx \
  supervisor

RUN pip3 install uwsgi psycopg2

RUN useradd --no-create-home nginx
RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx
COPY flask-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /ect/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN celery -A app.celery worker --loglevel=info

CMD ["/usr/bin/supervisord"]

