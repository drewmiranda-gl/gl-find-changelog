Initialize and create buildx container

```sh
# One time only
docker buildx create --name multiarch --driver docker-container --use
# build AND PUSH
```

UPDATE build tag (in CMD below) and version (in `./Dockerfile`)!

Build and Publish to Docker Hub

```sh
docker buildx build \
--push \
--platform linux/arm64/v8,linux/amd64 \
--tag drewmiranda/gl-find-changelog:latest \
--tag drewmiranda/gl-find-changelog:v0.5 \
.
```