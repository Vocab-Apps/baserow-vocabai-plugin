# docker build -t lucwastiaux/baserow-clt:1.18.0-6.2-b -f baserow_clt.Dockerfile .
# docker push lucwastiaux/baserow-clt:1.18.0-6.2-b

FROM baserow/baserow:1.18.0

# install packages first
RUN apt-get update -y && apt-get install -y libasound2 build-essential wget procps
# required by Epitran module
RUN wget https://github.com/festvox/flite/archive/refs/tags/v2.2.tar.gz && tar xvzf v2.2.tar.gz && cd flite-2.2 && ./configure && make && make install && cd testsuite && make lex_lookup && cp lex_lookup /usr/local/bin

RUN . /baserow/venv/bin/activate && pip3 install sentry-sdk==1.9.8 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_wenlin==1.0 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==0.9 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==6.2 && pip3 cache purge
