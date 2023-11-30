############
# TEMPLATE #
############

FROM python:3.10-alpine as python_geos

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev libpq binutils proj gdal geos \
    && ln -s /usr/lib/libproj.so.25 /usr/lib/libproj.so \
    && ln -s /usr/lib/libgdal.so.32 /usr/lib/libgdal.so \
    && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so

############
# BUILDER #
############
FROM python:3.10-alpine as builder

WORKDIR /usr/src/app/

RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python3.10-alpine_python_geos

RUN mkdir -p /home/app/

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]