#!/bin/bash
set -e

# if the user is and arbitrary ID
if ! whoami &> dev/null; then
    #make sure we have r/w access to /etc/passwd
    if [ -w /etc/passwd ]; then
        # write a line in /etc/passwd for the arbitrary uid in the 'root' group
        echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${HOME}:/sbin/nologin" >> /etc/passwd
    fi
fi

if [ "$1" = 'supervisord' ]; then
    exec /usr/bin/supervisord
fi

exec "$@"