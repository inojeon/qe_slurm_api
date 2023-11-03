FROM inojeon/slurm_base_rocky8:21

# qe 7.2 install 

RUN set -ex \
  && dnf install -y autoconf gcc-gfortran openblas fftw-libs-double

RUN set -ex \
    && wget https://gitlab.com/QEF/q-e/-/archive/qe-7.2/q-e-qe-7.2.tar.gz \
    && tar -zxvf q-e-qe-7.2.tar.gz \
    && cd q-e-qe-7.2 \
    && ./configure --prefix=/usr/local/ \
    && make all \
    && make install \
    && cd .. \
    && rm -rf q-e-qe-7.2.tar.gz q-e-qe-7.2

# python 3.11.5 install 
RUN set -ex \
  && dnf install bzip2-devel libffi-devel -y \
  && VERSION=3.11.5 \
  && wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz \
  && tar xvf Python-$VERSION.tgz \ 
  && cd Python-$VERSION \
  && ./configure --enable-optimizations \
  && make altinstall \
  && cd .. \ 
  && rm -rf Python-$VERSION Python-$VERSION.tgz

RUN ln -fs /usr/local/bin/python3.11 /usr/bin/python \
  && ln -fs /usr/local/bin/python3.11 /usr/bin/python3 \
  && ln -fs /usr/local/bin/pip3.11 /usr/bin/pip \
  && ln -fs /usr/local/bin/pip3.11 /usr/bin/pip3 

RUN pip3 install tomli ase toml

# 실행 스크립트 파일 Copy
COPY slurm_worker/worker-entrypoint.sh /usr/local/bin/worker-entrypoint.sh

# END
RUN ["chmod", "+x", "/usr/local/bin/worker-entrypoint.sh"]
ENTRYPOINT ["/usr/local/bin/worker-entrypoint.sh"]