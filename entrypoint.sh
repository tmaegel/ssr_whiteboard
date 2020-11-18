#!/bin/sh

exec gunicorn -w 4 --threads 2 -b 0.0.0.0:8080 "whiteboard:create_app()"
