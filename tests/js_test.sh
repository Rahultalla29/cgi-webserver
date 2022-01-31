#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl localhost:8070/home.js | diff - js_expected.out 

kill $PID
