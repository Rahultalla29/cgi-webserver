#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl "localhost:8070/cgibin/query_string.py?NAME=Jeff&AGE=18" 2> /dev/null | diff - cgi_query_test.out
# curl localhost:8070/greetings.html 2> /dev/null
kill $PID