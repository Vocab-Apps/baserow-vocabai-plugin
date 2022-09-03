# This a dev image for testing your plugin when installed into the Baserow all-in-one image

# to start up in dev:
# docker-compose -f docker-compose.dev.yml up

FROM baserow/baserow:1.11.0 as base

FROM baserow/baserow:1.11.0

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

# install cloudlanguagetools dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN . /baserow/venv/bin/activate && pip3 install clt_spacy==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_argostranslate==0.5 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_wenlin==0.7 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==2.4 && pip3 cache purge

COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./plugins/baserow_vocabai_plugin/ $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin --dev

ENV BASEROW_ALL_IN_ONE_DEV_MODE='true'
