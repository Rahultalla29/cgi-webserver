#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd -> /dev/null
sleep 1
curl -I 127.0.0.1:8070/  | grep '200 OK' | diff - index_status_expected.out 
kill $PID
