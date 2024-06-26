#!/bin/bash
baxsh /app/start-turbovnc.sh
export DISPLAY=:1
source activate py36
exec "$@"