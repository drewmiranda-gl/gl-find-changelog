#!/usr/bin/env bash

wget https://raw.githubusercontent.com/drewmiranda-gl/gl-find-changelog/refs/heads/main/DockerCompose.yml -O Gl-Find-Changelog-DockerCompose.yml
wget https://raw.githubusercontent.com/drewmiranda-gl/gl-find-changelog/refs/heads/main/config.example.yml -O config.yml

set -Eeuo pipefail

case "$OSTYPE" in
  darwin*|bsd*)
    echo "Using BSD sed style"
    sed_no_backup=( -i '' )
    ;; 
  *)
    echo "Using GNU sed style"
    sed_no_backup=( -i )
    ;;
esac

echo -n "Enter GH api-token: " && tmppw=$(head -1 </dev/stdin | tr -d '\n') && sed ${sed_no_backup[@]} -e "s/  api-token:.*/  api-token: $tmppw/g" config.yml

docker compose -f Gl-Find-Changelog-DockerCompose.yml up -d --build