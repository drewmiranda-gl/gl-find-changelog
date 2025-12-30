# BUILD
# ============================================================================= 
# # Multi ARCH Try it out
# # One time only
# docker buildx create --name multiarch --driver docker-container --use
# # build AND PUSH

# ======== UNCOMMENT BELOW TO COPY BUILD COMMAND ========
# docker buildx build \
# --push \
# --platform linux/arm64/v8,linux/amd64 \
# --tag drewmiranda/gl-find-changelog:latest \
# --tag drewmiranda/gl-find-changelog:v0.4 \
# .
# ======== ======== ======== ======== ======== ========

# 
# =============================================================================
# # Single ARCH
# docker build -t drewmiranda/gl-find-changelog:latest .
# 
# ADD TAG
# docker tag drewmiranda/gl-find-changelog:latest drewmiranda/gl-find-changelog:v0.1
# 
# PUSH TAGS
# If needed, login using `docker login`
# docker push drewmiranda/gl-find-changelog:latest
# docker push drewmiranda/gl-find-changelog:v0.1
# 
# =============================================================================
# 
# Public URL
# https://hub.docker.com/r/drewmiranda/gl-find-changelog
# 
# Github
# https://github.com/drewmiranda-gl/gl-find-changelog
# 
FROM python:3.11-slim

LABEL version="0.5"

WORKDIR /app

COPY requirements.txt .
COPY wsgi.py .
COPY dev_launch.sh .
COPY static ./static
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w 1", "-b 0.0.0.0:80", "-k gevent", "wsgi:app"]