# Dev Workflows

## required env vars
```
source env.dev.sh
source ~/secrets/cloudlanguagetools/cloudlanguagetools_core_secret.sh
source ~/secrets/vocabai/dev.sh

```

```
docker compose -f docker-compose.dev.yml up
docker compose -f docker-compose.dev.yml up -d
```

## to build:
```
docker compose -f docker-compose.dev.yml up --build
docker compose -f docker-compose.dev.yml up -d --build
```


## bring down or restart

### to bring down
`docker-compose -f docker-compose.dev.yml down`
### bring down and clear volumes:
`docker-compose -f docker-compose.dev.yml down -v`
### to restart
`docker-compose -f docker-compose.dev.yml restart`

## looking at logs
following logs:
`docker logs --since 1h -f baserow-vocabai-plugin`

## running tests

### make sure to give database users correct permissions
```
docker compose -f docker-compose.dev.yml exec -T baserow-vocabai-plugin /baserow/supervisor/docker-postgres-setup.sh run <<< "ALTER USER baserow CREATEDB;"
```
(from https://baserow.io/docs/plugins/boilerplate)

### attach to docker container

```
docker compose -f docker-compose.dev.yml exec baserow-vocabai-plugin /baserow.sh backend-cmd bash -c bash
cd /baserow/data/plugins/baserow_vocabai_plugin/backend/tests
pytest
CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes pytest baserow_vocabai_plugin/cloudlanguagetools/test_clt.py
```

# Generating new baserow patch file
see ```plugins/baserow_vocabai_plugin/backend/build.sh```

# Updating baserow-vocabai-patches
get latest master
```
git fetch upstream
git rebase upstream/master
git push
```
create persistent branch with the baserow release
```
git checkout -b baserow-1.16.0 1.16.0
git push --set-upstream origin baserow-1.16.0
```
now, create a new vocabai branch, which we'll rebase with the latest baserow
```
git checkout baserow-vocabai-patch-1.12.0
git checkout -b baserow-vocabai-patch-1.16.0
git rebase baserow-1.16.0
```
(fix any conflicts that show up)
```
git push --set-upstream origin baserow-vocabai-patch-1.16.0
```

# Updating to a newer baserow release
```
cookiecutter gl:bramw/baserow --directory plugin-boilerplate
# provide name baserow-plugin-1-13-2
```
then, compare contents in `baserow-plugin-1-13-2` with existing plugin files.

```
diff --color=always -ur baserow-vocabai-plugin baserow-plugin-1-15-2   | less -r
```

* mass-replace `1.12.0` with `1.16.0`