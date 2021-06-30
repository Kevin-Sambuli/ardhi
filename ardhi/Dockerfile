FROM python:3.8-slim-buster

LABEL maintainer=kevoh
LABEL description="Web based geodjango Land Information application"

# set our working directory inside the container (when it's finally created from this image)
# depending on your environment you may need to
# RUN mkdir -p /app
#WORKDIR /app
RUN mkdir -p /home/app

# create the app user
#RUN addgroup -S app && adduser -S app -G app

# depending on your environment you may also need to
RUN mkdir -p /postgres_data
RUN mkdir -p /pgadmin
RUN mkdir -p /geoserver_data

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
#RUN mkdir $APP_HOME/geoserver
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing .pyc files to disc
ENV PYTHONUNBUFFERED 1 # Prevents Python from buffering stdout and stderr

# install psycopg2 dependencies
#RUN apt-get update \
#   && apt-get -y install netcat gcc postgresql \
#   && apt-get clean

# # install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Setup GDAL
RUN apt-get update &&\
   apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal 
RUN pip install numpy scipy pandas geopandas sqlalchemy networkx osmnx shapely \
    rasterio geopy geoip2 geopandas pyproj Shapely rasterio Fiona Rtree descartes
#RUN apt install --reinstall gnupg2
#RUN apt install dirmngr

# upgrade pip version
RUN pip install --upgrade pip

# RUN pip install flake8
# COPY . .
# RUN flake8 --ignore=E501,F401 .

# copy requirements to the image
COPY ./requirements.txt /home/app/web/requirements.txt

RUN pip install -r requirements.txt

# enabling static files


# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy to project
COPY . $APP_HOME

# chown all the files to the app user
#RUN chown -R app:app $APP_HOME

# WORKDIR /usr/src/app
# RUN addgroup --system admin && adduser --system --no-create-home --group admin && \
#     chown -R admin:admin /usr && chmod -R 755 /usr

# change to the app user
#USER app



#RUN adduser -D kevoh
#USER kevoh
#CMD gunicorn ardhi.wsgi:application --bind 0.0.0.0:$PORT 8000

#ENTRYPOINT ["home/app/web/entrypoint.sh"]

#CMD gunicorn ardhi.wsgi:application --bind 0.0.0.0:8000

# define the default command to run when starting the container
# CMD ["gunicorn", "--chdir", "hello", "--bind", ":8000", "hello.wsgi:application"]
#CMD python manage.py runserver 0.0.0.0:8000