FROM rockylinux:8

ENV PATH="/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin"

EXPOSE 6817 6818 6819 6820

# Reference
# https://github.com/slaclab/slac-ondemand/blob/master/Dockerfile
# https://github.com/giovtorres/docker-centos7-slurm/blob/main/Dockerfile
# https://github.com/anybox/openldap-docker/blob/master/Dockerfile

# TimeZone
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# setup munge User
ARG MUNGEUSER=101
RUN groupadd -g $MUNGEUSER munge \
    && useradd  -m -c "MUNGE Uid 'N' Gid Emporium" -d /var/lib/munge -u $MUNGEUSER -g munge  -s /sbin/nologin munge

# setup munge Slurm
ARG SLURMUSER=102
RUN groupadd -g $SLURMUSER slurm \
    && useradd  -m -c "SLURM Uid 'N' Gid Emporium" -d /var/lib/slurm -u $SLURMUSER -g slurm  -s /sbin/nologin slurm

RUN echo "sslverify=0" >> /etc/yum.repos.d/Rocky-AppStream.repo
RUN echo "sslverify=0" >> /etc/yum.repos.d/Rocky-BaseOS.repo
RUN echo "sslverify=0" >> /etc/yum.repos.d/Rocky-Extras.repo
RUN echo "sslverify=0" >> /etc/yum.repos.d/Rocky-PowerTools.repo

# Install common YUM dependency packages
RUN set -ex \
    && yum makecache \
    && yum -y update \
    && yum -y install dnf-plugins-core \
    && yum config-manager --set-enabled powertools \
    && yum -y install \
      wget \
      gcc \
      gcc-c++ \
      make \
      bzip2 \
      munge \
      munge-devel \
      perl-core \
      python3-devel \
      python3-pip \
      python3 \
      http-parser-devel \
      json-c-devel  \
      mariadb-devel  \
      openssh-server \
      openssh-clients \
      openssh-askpass \
      dbus-devel \
      git \
      gnupg \
      psmisc \
      bash-completion \
      vim-enhanced \
      http-parser-devel \
      json-c-devel \
    && yum clean all \
    && rm -rf /var/cache/yum

#RUN dnf update
COPY slurm_base/epel.repo /etc/yum.repos.d/
RUN yum repolist
RUN yum clean all
RUN yum install --nogpgcheck -y supervisor \
      openldap-clients \
      singularity*  \
      libjwt-devel  \
      nss-pam-ldapd

#Compile, build and install Slurm
ARG SLURM_TAG=slurm-21-08-8-2

RUN set -x \
    && git clone -b ${SLURM_TAG} --single-branch --depth=1 https://github.com/SchedMD/slurm.git \
    && pushd slurm \
    && ./configure --enable-debug --prefix=/usr --sysconfdir=/etc/slurm \
        --with-mysql_config=/usr/bin  --libdir=/usr/lib64 \
    && make -j4 \
    && make install \
    && install -D -m644 etc/cgroup.conf.example /etc/slurm/cgroup.conf.example \
    && install -D -m644 etc/slurm.conf.example /etc/slurm/slurm.conf.example \
    && install -D -m644 etc/slurmdbd.conf.example /etc/slurm/slurmdbd.conf.example \
    && install -D -m644 contribs/slurm_completion_help/slurm_completion.sh /etc/profile.d/slurm_completion.sh \
    && popd \
    && rm -rf slurm \
    && mkdir /etc/sysconfig/slurm \
        /var/spool/slurmd \
        /var/spool/slurmctld \
        /var/run/slurm \
        /var/run/slurmdbd \
        /var/lib/slurmd \
        /var/log/slurm \
        /data \
    && touch /var/lib/slurmd/node_state \
        /var/lib/slurmd/front_end_state \
        /var/lib/slurmd/job_state \
        /var/lib/slurmd/resv_state \
        /var/lib/slurmd/trigger_state \
        /var/lib/slurmd/assoc_mgr_state \
        /var/lib/slurmd/assoc_usage \
        /var/lib/slurmd/qos_usage \
        /var/lib/slurmd/fed_mgr_state \
    && chown -R slurm:slurm /var/*/slurm* \
    && /sbin/create-munge-key

COPY slurm_config/config_file/slurm.conf /etc/slurm/
COPY slurm_config/config_file/slurmdbd.conf /etc/slurm/
RUN set -x \
    && chown slurm:slurm /etc/slurm/slurmdbd.conf \
    && chmod 600 /etc/slurm/slurmdbd.conf      

RUN chown -R munge: /etc/munge/ \
   /var/log/munge/ \
   /var/run/munge/ \
   /run/munge/ \
  && chmod 700 /etc/munge \
  /var/log/munge/ \
  /var/run/munge/ \
  && chmod 751 /run/munge 

# openLDAP Setting & supervisord Setting
COPY slurm_config/ldap/nscd.conf \
     slurm_config/ldap/nslcd.conf \
     slurm_config/ldap/nsswitch.conf \
     slurm_config/ldap/supervisord.conf /etc/

RUN alternatives --set python /usr/bin/python3

#slurm config file copy
COPY slurm_config/jwt/jwt_hs256.key /etc/slurm/

#munge key and jwt key copy
COPY slurm_config/munge/munge.key /etc/munge/munge.key
RUN chown -R slurm: /etc/sysconfig/slurm \
             /var/spool/slurmd \
             /var/spool/slurmctld \
             /var/log/slurm \
             /var/run/slurm \
             /etc/slurm/
# END
#CMD ["/bin/bash"]