#!/usr/bin/bash
clear;
python -m gunicorn -b "0.0.0.0:18052" --threads 24 --name "translate_api" --log-level INFO --error-logfile /dev/stdout --access-logfile /dev/stderr --access-logformat '%({x-forwarded-for}i)s %(l)s
 %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' chat_api:app;
