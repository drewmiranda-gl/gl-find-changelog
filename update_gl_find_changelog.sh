#!/usr/bin/env bash

# Pull Latest Image
docker compose -f Gl-Find-Changelog-DockerCompose.yml pull
# Start Container, rebuild if there are changes
docker compose -f Gl-Find-Changelog-DockerCompose.yml up -d --build
