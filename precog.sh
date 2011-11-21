#!/bin/bash
# silly os doesn't pass in COLUMNS envvar...
# so unless we're explicit, 80 is assumed :(
COLUMNS=$(tput cols) python3.2 precog.py "$@"
