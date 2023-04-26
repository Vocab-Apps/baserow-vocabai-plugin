# This a dev image for testing your plugin when installed into the Baserow all-in-one image


FROM lucwastiaux/baserow-clt:1.16.0-5.4-a as base

FROM lucwastiaux/baserow-clt:1.16.0-5.4-a

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
