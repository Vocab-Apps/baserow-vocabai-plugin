# docker build -t lucwastiaux/baserow-vocabai-plugin:20220910-1 -f Dockerfile .
# docker push lucwastiaux/baserow-vocabai-plugin:20220910-1

FROM baserow/baserow:1.12.0

# install cloudlanguagetools dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN . /baserow/venv/bin/activate && pip3 install clt_spacy==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_argostranslate==0.5 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_wenlin==0.8 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==0.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==2.5 && pip3 cache purge

# install sentry
RUN . /baserow/venv/bin/activate && pip3 install sentry-sdk && pip3 cache purge

COPY ./plugins/baserow_vocabai_plugin/ /baserow/plugins/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/baserow_vocabai_plugin
