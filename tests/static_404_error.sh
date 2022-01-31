#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl localhost:8070/no_file_exists.txt | diff - static_404_error_expected.out
# curl localhost:8070/greetings.html 2> /dev/null
kill $PID