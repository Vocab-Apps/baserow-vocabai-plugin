# docker build -t lucwastiaux/baserow-vocabai-plugin:20220910-1 -f Dockerfile .
# docker push lucwastiaux/baserow-vocabai-plugin:20220910-1

FROM baserow/baserow:1.12.0

ARG SENTRY_RELEASE
ENV SENTRY_RELEASE=${SENTRY_RELEASE:-baserow-vocabai@0.0.0}

# install ubuntu packages
RUN apt-get update && apt-get install -y --no-install-recommends wget

# install cloudlanguagetools
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==3.1 && pip3 cache purge

COPY ./plugins/baserow_vocabai_plugin/ /baserow/plugins/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/baserow_vocabai_plugin
