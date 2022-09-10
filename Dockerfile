FROM baserow/baserow:1.12.0

COPY ./plugins/baserow_vocabai_plugin/ /baserow/plugins/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/baserow_vocabai_plugin
