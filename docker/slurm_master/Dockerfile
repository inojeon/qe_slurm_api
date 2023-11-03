FROM inojeon/slurm_base_rocky8:21


# RUN yum install sqlite-devel \
#     && yum clean all \
#     && rm -rf /var/cache/yum

# python 3.11.5 install 
RUN set -ex \
  && dnf install bzip2-devel libffi-devel  sqlite-devel -y \
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

RUN pip3 install tomli ase fastapi uvicorn python-multipart Jinja2 uvicorn[standard] gunicorn pyyaml toml sqlalchemy

# 실행 파일 Copy
COPY slurm_master/master-entrypoint.sh /usr/local/bin/master-entrypoint.sh

# END
RUN ["chmod", "+x", "/usr/local/bin/master-entrypoint.sh"]
ENTRYPOINT ["/usr/local/bin/master-entrypoint.sh"]
# CMD ["/bin/bash"]
