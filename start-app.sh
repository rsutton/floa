#!/bin/bash
export FLASK_APP=floa
export FLASK_ENV='development'

# flask run --cert=adhoc
flask run $SECURE
