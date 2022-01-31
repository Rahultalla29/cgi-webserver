#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl localhost:8070/hello_world.txt | diff - static_hello_expected.out
# curl localhost:8070/greetings.html 2> /dev/null
kill $PID