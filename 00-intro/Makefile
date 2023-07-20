VERSION=$(shell git rev-parse HEAD | cut -c1-7)

docker-build:
	docker buildx build --push . --platform=linux/amd64,linux/arm64 \
		-t ghcr.io/unionai-oss/flyte-school:00-intro-${VERSION} \
		-t ghcr.io/unionai-oss/flyte-school:00-intro-latest

ci-docker-build:
	docker build --push . -f Dockerfile.ci -t ghcr.io/unionai-oss/flyte-school:00-intro-ci

sandbox-docker-build:
	docker build --push . -t localhost:30000/flyte-school:00-intro-ci --platform=linux/amd64,linux/arm64
