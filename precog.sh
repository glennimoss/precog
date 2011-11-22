#!/bin/bash
# silly os doesn't pass in COLUMNS envvar...
# so unless we're explicit, 80 is assumed :(
BASE=$(dirname "$(realpath "$0")")
COLUMNS=$(tput cols) PYTHONPATH="$PYTHONPATH:$BASE" python3.2 $BASE/precog.py "$@"
