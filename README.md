# github-graylog-issue-release-finder

Proof of concept tool that can automate searching for a given GH issue across multiple release tags and/or branches

# How to use

## Download Files
* `DockerCompose.yml`
* `config.example.yml`

## Rename Config File
Rename `config.example.yml` to `config.yml`

## Create a Github access token
If you do not already have one: obtain a Github access token using your Graylog Org GH account

e.g. Settings / Developer Settings / Personal access tokens / Fine-grained personal access tokens

Requires the following permissions:

```
Contents            Read-Only
Issues              Read-Only
Pull Requests       Read-Only
```

## Save access token in config file

Modify `config.yml` and save your Github access token using the github.api-token parameter. Do not enclose the token in double quotes (`"`)

## Use Docker Compose to run the container

`docker compose -f DockerCompose.yml up -d --build`

Listens on port [TCP] 89 by default and can be reached via your web browser at http://127.0.0.1:89