# docker build -t lucwastiaux/baserow-clt:1.12.0-3.4 -f baserow_clt.Dockerfile .
# docker push lucwastiaux/baserow-clt:1.12.0-3.4

FROM baserow/baserow:1.12.0

# install packages first
RUN apt-get update -y && apt-get install -y libasound2 build-essential wget
# required by Epitran module
RUN wget http://tts.speech.cs.cmu.edu/awb/flite-2.0.5-current.tar.bz2 && tar xvjf flite-2.0.5-current.tar.bz2 && cd flite-2.0.5-current && ./configure && make && make install && cd testsuite && make lex_lookup && cp lex_lookup /usr/local/bin

RUN . /baserow/venv/bin/activate && pip3 install sentry-sdk==1.9.8 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==3.6 && pip3 cache purge
