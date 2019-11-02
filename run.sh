#!/usr/bin/env sh
docker run -t --rm --name simpleweb -p 5000:5000 \
           -v /Users/marc/local/python-project/simpleweb/secrets:/secrets \
           --env CERTFILE=/secrets/localhost.cert.pem \
           --env KEYFILE=/secrets/localhost.pem simpleweb
