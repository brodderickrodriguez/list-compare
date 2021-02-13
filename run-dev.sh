#!/usr/bin/env bash

export FLASK_APP=passenger_wsgi
export FLASK_ENV=development

flask run -p 5003