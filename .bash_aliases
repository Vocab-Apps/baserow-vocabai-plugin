CONTAINER_NAME=baserow-vocabai-plugin
DOCKER_COMMAND="docker compose -f docker-compose.dev.yml exec ${CONTAINER_NAME}"

alias run_docker_interactive='docker compose -f docker-compose.dev.yml exec baserow-vocabai-plugin /baserow.sh backend-cmd bash -c bash'
alias attach_docker_container='docker compose -f docker-compose.dev.yml exec baserow-vocabai-plugin /baserow.sh backend-cmd bash -c bash'
alias run='docker compose -f docker-compose.dev.yml up'
alias run_build='docker compose -f docker-compose.dev.yml up --build'
alias log_tail='docker logs --since 1h -f baserow-vocabai-plugin'
alias log_inspect='docker logs --since 1h baserow-vocabai-plugin'
alias test='${DOCKER_COMMAND} /baserow.sh backend-cmd bash -c "pytest --reuse-db /baserow/data/plugins/baserow_vocabai_plugin/backend/tests"'
alias test_clt='${DOCKER_COMMAND} /baserow.sh backend-cmd bash -c "CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes pytest --reuse-db /baserow/data/plugins/baserow_vocabai_plugin/backend/tests"'