FROM baserow/backend:1.15.2

USER root

COPY ./plugins/baserow_vocabai_plugin/ $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/baserow_vocabai_plugin

USER $UID:$GID
