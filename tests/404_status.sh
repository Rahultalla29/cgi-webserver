#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl -I 127.0.0.1:8070/missing.html 2> /dev/null | diff - 404_status_expected.out 
kill -9 $PID
