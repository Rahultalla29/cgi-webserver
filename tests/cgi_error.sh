#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl -I -XGET 127.0.0.1:8070/cgibin/error.py 2> /dev/null | head -n 1  | diff - cgi_error_test.out
kill $PID