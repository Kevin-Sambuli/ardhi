FROM python:3.9-slim-buster

LABEL maintainer=kevoh
LABEL description="Web based geodjango Land Information application"

# set environment variables Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y



# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && pip install psycopg2 \
    && rm -rf /var/lib/apt/lists/*
#    && apt-get clean

# Setup GDAL
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal


# set our working directory inside the container (when it's finally created from this image)
RUN mkdir -p /home/app

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
WORKDIR $APP_HOME

# installing geospatial libraries
RUN pip install numpy scipy pandas geopandas sqlalchemy networkx osmnx shapely \
    rasterio geopy geoip2 geopandas pyproj Shapely rasterio Fiona Rtree descartes

# upgrade pip version
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
#RUN pip install pipwin
#RUN pipwin refresh
#RUN pip install geoserver-rest

# RUN pip install flake8
# COPY . .
# RUN flake8 --ignore=E501,F401 .

# copy requirements to the image
COPY ./requirements.txt /home/app/web/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME
#COPY ./entrypoint.sh /home/app/web/entrypoint.sh

# copy to project
COPY . $APP_HOME


#ENTRYPOINT ["bash", "home/app/web/entrypoint.sh"]

#CMD gunicorn ardhi.wsgi:application --bind 0.0.0.0:8000
