# This a dev image for testing your plugin when installed into the Baserow all-in-one image

# to start up in dev:
# docker-compose -f docker-compose.dev.yml up
# to build:
# docker-compose -f docker-compose.dev.yml up --build
# docker-compose -f docker-compose.dev.yml up -d --build
# https://baserow.io/docs/plugins/boilerplate
#
# attaching to container (for debugging)
# docker exec -it 051b1e429d3d bash
#
# following logs:
# docker logs --since 1h -f baserow-vocabai-plugin
# 
# to bring down
# docker-compose -f docker-compose.dev.yml down
# bring down and clear volumes:
# docker-compose -f docker-compose.dev.yml down -v


FROM baserow/baserow:1.12.0 as base

FROM baserow/baserow:1.12.0

ARG PLUGIN_BUILD_UID
ENV PLUGIN_BUILD_UID=${PLUGIN_BUILD_UID:-9999}
ARG PLUGIN_BUILD_GID
ENV PLUGIN_BUILD_GID=${PLUGIN_BUILD_GID:-9999}

# Use a multi-stage copy to quickly chown the contents of Baserow to match the user
# that will be running this image.
COPY --from=base --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID /baserow /baserow

RUN groupmod -g $PLUGIN_BUILD_GID baserow_docker_group && usermod -u $PLUGIN_BUILD_UID $DOCKER_USER

# Install your dev dependencies manually.
COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./plugins/baserow_vocabai_plugin/backend/requirements/dev.txt /tmp/plugin-dev-requirements.txt
RUN . /baserow/venv/bin/activate && pip3 install -r /tmp/plugin-dev-requirements.txt

# common between dev/prod
# =======================

# install cloudlanguagetools dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN . /baserow/venv/bin/activate && pip3 install clt_spacy==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_wenlin==0.8 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==2.9 && pip3 cache purge

# install sentry
RUN . /baserow/venv/bin/activate && pip3 install sentry-sdk && pip3 cache purge

# modify some assets
COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./graphics/logo.svg /baserow/web-frontend/modules/core/static/img/logo.svg

# apply patches
# =============

# backend
# diff -Naur baserow/backend/ baserow-vocabai-patched/backend/ > ~/python/baserow-vocabai-plugin/baserow-patches/backend.patch
COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./baserow-patches/backend.patch /patches/backend.patch
RUN cd /baserow && patch -u -p1 -i /patches/backend.patch

# frontend
# diff -Naur baserow/web-frontend/ baserow-vocabai-patched/web-frontend/ > ~/python/baserow-vocabai-plugin/baserow-patches/sentry_setup.patch
COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./baserow-patches/sentry_setup.patch /patches/sentry_setup.patch
RUN cd /baserow && patch -u -p1 -i /patches/sentry_setup.patch

# =============

COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./plugins/baserow_vocabai_plugin/ $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin --dev

ENV BASEROW_ALL_IN_ONE_DEV_MODE='true'
