# For Maintainers

## Deployment

Build and push docker image:

```
make docker-build-push
```

Serialize

```bash
IMAGE=ghcr.io/unionai-oss/flyte-school:00-intro-latest
pyflyte --pkgs workflows package --image $IMAGE -f
```

Register

```bash
flytectl register files \
    --project flytesnacks \
    --domain development \
    --archive flyte-package.tgz \
    --version v0
```

Fast Register

```bash
pyflyte --pkgs workflows package --image $IMAGE --fast -f
flytectl register files \
    --project flytesnacks \
    --domain development \
    --archive flyte-package.tgz \
    --version v0-fast0
```
