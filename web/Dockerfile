###########
# BUILDER #
###########

FROM python:3.10-alpine as builder

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY . .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt





#########
# FINAL #
#########

FROM python:3.10-alpine

# INSTALL GEOS
RUN apk add --no-cache binutils
RUN apk add --no-cache proj
RUN apk add --no-cache gdal
RUN apk add --no-cache geos

RUN ln -s /usr/lib/libproj.so.25 /usr/lib/libproj.so \
    && ln -s /usr/lib/libgdal.so.32 /usr/lib/libgdal.so \
    && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so




RUN mkdir -p /home/app/

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
# COPY ./static ${APP_HOME}/staticfiles
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

ENV LD_LIBRARY_PATH=/usr/local/lib
RUN echo /usr/local/lib >> /etc/ld.so.conf

COPY . $APP_HOME

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]