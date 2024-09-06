# docker build -t lucwastiaux/baserow-clt:1.26.1-11.3.2-a -f baserow_clt.Dockerfile .
# docker push lucwastiaux/baserow-clt:1.26.1-11.3.2-a

FROM baserow/baserow:1.26.1

# install packages first
RUN apt-get update -y && apt-get install -y libasound2 build-essential wget procps iproute2 nano
# required by Epitran module
RUN wget https://github.com/festvox/flite/archive/refs/tags/v2.2.tar.gz && tar xvzf v2.2.tar.gz && cd flite-2.2 && ./configure && make && make install && cd testsuite && make lex_lookup && cp lex_lookup /usr/local/bin

RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==1.7 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==11.3.2 && pip3 cache purge
