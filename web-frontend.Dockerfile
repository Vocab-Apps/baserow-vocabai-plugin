FROM baserow/web-frontend:1.26.1

USER root

COPY ./plugins/baserow_vocabai_plugin/ /baserow/plugins/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/baserow_vocabai_plugin

USER $UID:$GID
