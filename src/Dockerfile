# BUILD
# docker build -t drewmiranda/gl-find-changelog:latest .
# 
# ADD TAG
# docker tag drewmiranda/gl-find-changelog:latest drewmiranda/gl-find-changelog:v0.1
# 
# PUSH TAGS
# docker push drewmiranda/gl-find-changelog:latest
# docker push drewmiranda/gl-find-changelog:v0.1
# 
# Public URL
# https://hub.docker.com/r/drewmiranda/gl-find-changelog
# 
# Github
# 
# 
FROM python:3.11-slim

LABEL version="0.1"

WORKDIR /app

COPY requirements.txt .
COPY wsgi.py .
COPY dev_launch.sh .
COPY static ./static
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w 1", "-b 0.0.0.0:80", "-k gevent", "wsgi:app"]