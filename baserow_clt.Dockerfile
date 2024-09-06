# docker build -t lucwastiaux/baserow-clt:1.26.1-11.3.2-a -f baserow_clt.Dockerfile .
# docker push lucwastiaux/baserow-clt:1.26.1-11.3.2-a

ARG BASEROW_IMAGE_VERSION=1.26.0
FROM baserow/baserow:${BASEROW_IMAGE_VERSION}

# arguments
ARG CLT_VERSION
ARG CLT_REQUIREMENTS_VERSION

# install packages first
RUN apt-get update -y && apt-get install -y libasound2 build-essential wget procps iproute2 nano
# required by Epitran module
RUN wget https://github.com/festvox/flite/archive/refs/tags/v2.2.tar.gz && tar xvzf v2.2.tar.gz && cd flite-2.2 && ./configure && make && make install && cd testsuite && make lex_lookup && cp lex_lookup /usr/local/bin

RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==${CLT_REQUIREMENTS_VERSION} && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==${CLT_VERSION} && pip3 cache purge

