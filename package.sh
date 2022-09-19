#!/bin/sh

VERSION_NUMBER=$1 # for example 0.1
GIT_TAG=v${VERSION_NUMBER}
SENTRY_RELEASE="baserow-vocabai@${VERSION_NUMBER}"

git commit -a -m "upgraded version to ${VERSION_NUMBER}"
git push
git tag -a ${GIT_TAG} -m "version ${GIT_TAG}"
git push origin ${GIT_TAG}

# docker build
docker build --build-arg SENTRY_RELEASE=${SENTRY_RELEASE} -t lucwastiaux/baserow-vocabai-plugin:${VERSION_NUMBER} -f Dockerfile .
docker push lucwastiaux/baserow-vocabai-plugin:${VERSION_NUMBER}