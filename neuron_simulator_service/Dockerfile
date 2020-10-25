FROM ubuntu:16.04

MAINTAINER jp

WORKDIR /

EXPOSE 5000

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN apt-get install wget -y

COPY ./requirements.txt /requirements.txt

RUN apt install -y libx11-dev git bison flex automake libtool libxext-dev libncurses-dev python-dev xfonts-100dpi cython libopenmpi-dev python-scipy make zlib1g-dev

RUN pip install -r requirements.txt

#Install neuron
RUN wget -c https://neuron.yale.edu/ftp/neuron/versions/v7.7/nrn-7.7.tar.gz && \
    tar -xf nrn-7.7.tar.gz && \
    mv nrn-7.7 nrn && \
    cd nrn && \
    ./configure --without-iv --with-paranrn --with-nrnpython=python2 && \
    make -j && \
    make install -j && \
    cd src/nrnpython && \
    python2 setup.py install

COPY . /

ENV PATH="$PATH:/usr/local/nrn/x86_64/bin"

RUN nrnivmodl SAC_network/mechanism

ENTRYPOINT [ "python" ]
CMD [ "SAC_network/app.py" ]