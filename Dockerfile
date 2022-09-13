# docker build -t lucwastiaux/baserow-vocabai-plugin:20220910-1 -f Dockerfile .
# docker push lucwastiaux/baserow-vocabai-plugin:20220910-1

FROM baserow/baserow:1.12.0

# common between dev/prod
# =======================

# install cloudlanguagetools dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN . /baserow/venv/bin/activate && pip3 install clt_spacy==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_argostranslate==0.5 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_wenlin==0.8 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==2.5 && pip3 cache purge

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

COPY ./plugins/baserow_vocabai_plugin/ /baserow/plugins/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/baserow_vocabai_plugin
