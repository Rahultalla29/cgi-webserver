#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
curl localhost:8070/cgibin/hello_world_sleep.py &> /dev/null & 
curl localhost:8070/cgibin/hello_world_sleep.py &> /dev/null & 
curl localhost:8070/cgibin/hello_world_sleep.py &> /dev/null & 
curl localhost:8070/cgibin/hello_world_sleep.py &> /dev/null & 
curl localhost:8070/cgibin/hello_world_sleep.py  | diff - multiple_connections_expected.out
kill $PID