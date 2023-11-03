#!/bin/bash

function error_with_msg {
    if [[ "$count" -eq 0 ]]
    then
        echo
        echo >&2 "$1"
        exit 1
    fi
}

function check_port_status {
    for count in {10..0}; do
        echo 2>/dev/null >/dev/tcp/localhost/$1
        if [[ "$?" -eq 0 ]]
        then
            echo "- Port $1 is listening"
            break
        else
            echo "- Port $1 is not listening"
            sleep 1
        fi
    done
}

function start_service {
    if [[ "$1" = "SLURM_PATH" ]]
    then
        echo "- SLURM  Path Owner Setting"
        chown -R slurm: /etc/sysconfig/slurm /var/spool/slurmd /var/spool/slurmctld /var/log/slurm  /var/run/slurm /etc/slurm/
    elif [[ "$1" = "nslcd" ]]
    then
        echo "- Starting $1"
        check_running_status $1
    else
        echo "- Starting $1"
         /usr/bin/supervisorctl start $1
        check_running_status $1
    fi
}

function check_running_status {
    for count in {10..0}; do
        STATUS=$(/usr/bin/supervisorctl status $1 | awk '{print $2}')
        echo "- $1 is in the $STATUS state."
        if [[ "$STATUS" = "RUNNING" ]]
        then
            break
        else
            sleep 1
        fi
    done
}

# pick up relevant supervisord conf
# SUPERVISORD_CONFIG=${SUPERVISORD_CONFIG:-/supervisord.conf}
echo "- Starting supervisord process manager"
/usr/bin/supervisord --configuration /etc/supervisord.conf

# setup munge file
if [ -e /etc/munge/munge.key ]; then
  echo "Copying munge key from /EDISON2/SYSTEM/kubernetes/munge/munge.key"
#  cp ${MOUNT_PATH}/slurm_config/munge/munge.key /etc/munge/munge.key
  chown munge: /etc/munge/munge.key
  chmod 400 /etc/munge/munge.key
fi

for service in  munged slurmd
do
    start_service $service
done

for port in 6818
do
    check_port_status $port
done

echo "- Waiting for the cluster to become available"
for count in {10..0}; do
    if ! grep -q "normal.*idle" <(timeout 1 sinfo)
    then
        sleep 1
    else
        break
    fi
done

#error_with_msg "Slurm partitions failed to start successfully."

echo "- Cluster is now available"
echo "Service Status Info"
supervisorctl status

tail -f /dev/null