CONTAINER_NAME=baserow-vocabai-plugin
DOCKER_COMPOSE_COMMAND="docker compose -f docker-compose.dev.yml"
DOCKER_EXEC_COMMAND="docker compose -f docker-compose.dev.yml exec ${CONTAINER_NAME}"
DOCKER_BASEROW_EXECUTE_BASH="${DOCKER_EXEC_COMMAND} /baserow.sh backend-cmd bash -c "

alias attach_docker_container='${DOCKER_BASEROW_EXECUTE_BASH} bash'
alias run='source ./baserow_clt_versions.sh ; ${DOCKER_COMPOSE_COMMAND} up'
alias run_build='source ./baserow_clt_versions.sh ; ${DOCKER_COMPOSE_COMMAND} up --build'
alias log_tail='docker logs --since 1h -f ${CONTAINER_NAME}'
alias log_inspect='docker logs --since 1h ${CONTAINER_NAME}'
alias test='${DOCKER_BASEROW_EXECUTE_BASH} "pytest --reuse-db /baserow/data/plugins/baserow_vocabai_plugin/backend/tests"'
alias test_clt='${DOCKER_BASEROW_EXECUTE_BASH} "CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes pytest --reuse-db /baserow/data/plugins/baserow_vocabai_plugin/backend/tests"'