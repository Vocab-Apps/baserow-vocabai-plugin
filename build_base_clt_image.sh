#!/bin/bash

. baserow_clt_versions.sh

docker build \
--build-arg BASEROW_IMAGE_VERSION=${BASEROW_IMAGE_VERSION} \
--build-arg CLT_VERSION=${CLT_VERSION} \
--build-arg CLT_REQUIREMENTS_VERSION=${CLT_REQUIREMENTS_VERSION} \
-t ${BASE_BASEROW_CLT_IMAGE} -f baserow_clt.Dockerfile .
docker push ${BASE_BASEROW_CLT_IMAGE}