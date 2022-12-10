# docker build -t lucwastiaux/baserow-clt:1.13.2-4.2-a -f baserow_clt.Dockerfile .
# docker push lucwastiaux/baserow-clt:1.13.2-4.2-a

FROM baserow/baserow:1.13.2

# install packages first
RUN apt-get update -y && apt-get install -y libasound2 build-essential wget
# required by Epitran module
RUN wget http://tts.speech.cs.cmu.edu/awb/flite-2.0.5-current.tar.bz2 && tar xvjf flite-2.0.5-current.tar.bz2 && cd flite-2.0.5-current && ./configure && make && make install && cd testsuite && make lex_lookup && cp lex_lookup /usr/local/bin

RUN . /baserow/venv/bin/activate && pip3 install sentry-sdk==1.11.1 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_wenlin==1.0 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install clt_requirements==0.3 && pip3 cache purge
RUN . /baserow/venv/bin/activate && pip3 install cloudlanguagetools==4.2 && pip3 cache purge
