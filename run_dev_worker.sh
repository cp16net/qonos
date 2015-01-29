#/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_DIR="$DIR/etc/qonos"
CONFIG_FILE="$CONFIG_DIR/qonos-worker.conf"
ROOT_CONFIG="/etc/qonos/qonos-worker.conf"
if [[ -f $ROOT_CONFIG ]]; then
    CONFIG_FILE=$ROOT_CONFIG
fi


if [ ! -f $CONFIG_FILE ]
then
    cp $CONFIG_FILE.sample $CONFIG_FILE
fi

$DIR/bin/qonos-worker --config-file=$CONFIG_FILE