#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl localhost:8070/cgibin/servaddr.py 2> /dev/null | diff - server_env_test.out
# curl localhost:8070/greetings.html 2> /dev/null
kill $PID