#!/usr/bin/env python3
#
#
import os
import time
from redis import Redis
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import Response
from datetime import datetime

import requests


def gen():
    start_val = 100
    inc = 1
    curr = 100
    max_val = 120
    while True:
        curr += inc
        if curr > max_val:
            curr = start_val
        yield curr


appcontainer = Flask(__name__)
vals = gen()

app_version="0.7.5"
count = 0
cert_file = os.getenv('CERTFILE')
key_file = os.getenv('KEYFILE')
secret_file = os.getenv('SECRET')
redis_host = os.getenv('REDIS_HOST')
config_val = os.getenv('CONFIG_VAL')

context = None

if cert_file is not None and key_file is not None:
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        context = (cert_file, key_file)


@appcontainer.route("/")
def home():
    response = make_response(render_template('home.html', value='my_test_value'))
    return response


@appcontainer.route("/secret")
def secret():
    if secret_file is None:
        print('no SECRET environment variable provided, leaving...')
        return Response(app_version + ':no secret environment variable', status=200, mimetype='text')
    if not os.path.isfile(secret_file):
        print(app_version + ':secret file ' + secret_file + ' does not appear to exist.')
        return Response(app_version + ':' + secret_file + ' does not exist...', status=200)
    secret_fd = open(secret_file, 'r')
    secret_data = secret_fd.read()
    return Response(secret_data, status=200, mimetype='text')


@appcontainer.route("/record")
def record_hit():
    hdrs = request.headers
    for k in hdrs.keys():
        print('key: ' + k + '\tvalue: ' + hdrs[k])
    print(datetime.now())
    v = next(vals)
    return Response('{"value":' + str(v) + ',"version": "' + app_version + '"}', status=200,
                    mimetype='application/json')


@appcontainer.route("/value")
def get_value():
    if redis_host is None:
        print('redis_host not set')
        return Response('Redis not setup', status=404)
    print('value:redis_host: [' + redis_host + ']')
    rc = Redis(host=redis_host)
    rc.set('foo', 'abc')
    v = rc.get('foo').decode('utf-8')
    return Response('{"foo":"' + v + '"}', status=200)


@appcontainer.route("/config")
def get_config():
    print('config value is ' + config_val)
    return Response('{"config_val":"' + config_val + '"}', status=200, mimetype='application/json')


@appcontainer.route("/health")
def health_check():
    global count
    if count >= 100:
        count = 0
        return Response('preset failure', status=400)
    count += 1
    return Response('all good', status=200)


@appcontainer.route("/slowresp")
def slow_response():
    time.sleep(30)
    return Response('slow done', status=200)


@appcontainer.route("/call")
def call_rest():
    resp = requests.get("http://restserv:5100/value")
    if resp.ok:
        return Response(resp.content, status=200, mimetype="application/json")
    else:
        return Response("hmmm...." + resp, status=400)


@appcontainer.route("/configfile")
def configfile():
    filename = '/config/file.yaml'
    if os.path.exists(filename) is False:
        return Response('no config file', status=200)
    else:
        f = open(filename, 'r')
        buff = ''
        for line in f:
            buff = buff + line
        return Response(buff, status=200)


def start():
    print('version: ' + app_version)
    if context is None:
        print('no ssl defined...')
    else:
        print('trying to use ssl...')
    appcontainer.run(host="0.0.0.0", port=5000, debug=False, ssl_context=context)


if __name__ == '__main__':
    start()
