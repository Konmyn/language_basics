#! /usr/bin/env bash

# https://stackoverflow.com/questions/592620/how-to-check-if-a-program-exists-from-a-bash-script
if hash python 2> /dev/null; then
    python3 -m http.server 8000
elif hash python 2>/dev/null; then
    python -m SimpleHTTPServer 8000
fi

