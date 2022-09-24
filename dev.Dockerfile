# This a dev image for testing your plugin when installed into the Baserow all-in-one image

# to start up in dev:
# docker-compose -f docker-compose.dev.yml up
# to build:
# docker-compose -f docker-compose.dev.yml up --build
# docker-compose -f docker-compose.dev.yml up -d --build
# (no rebuild)
# docker-compose -f docker-compose.dev.yml up -d
# https://baserow.io/docs/plugins/boilerplate
#
# attaching to container (for debugging)
# docker exec -it baserow-vocabai-plugin bash
#
# following logs:
# docker logs --since 1h -f baserow-vocabai-plugin
# 
# to bring down
# docker-compose -f docker-compose.dev.yml down
# bring down and clear volumes:
# docker-compose -f docker-compose.dev.yml down -v
#
# to restart
# ==========
# docker-compose -f docker-compose.dev.yml restart


FROM lucwastiaux/baserow-clt:1.12.0-3.4 as base

FROM lucwastiaux/baserow-clt:1.12.0-3.4

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

# install plugin

COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./plugins/baserow_vocabai_plugin/ $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin --dev

ENV BASEROW_ALL_IN_ONE_DEV_MODE='true'
