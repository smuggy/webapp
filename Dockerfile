FROM mmckernan/python:3

ARG appversion
ARG PIP_FLAGS="--disable-pip-version-check"
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:5000 --access-logfile - --error-logfile - --log-file -"

RUN mkdir -p /app
WORKDIR /app

COPY dist/webapp-${appversion}-py3-none-any.whl /app/
COPY requirements.txt /app/

RUN pip3 install -r requirements.txt ${PIP_FLAGS}
RUN pip3 install ${PIP_FLAGS} /app/webapp-${appversion}-py3-none-any.whl

CMD ["gunicorn", "app:appcontainer"]
