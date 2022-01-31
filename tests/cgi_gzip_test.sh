#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl -H 'Accept-Encoding: gzip' localhost:8070/cgibin/hello.py  2> /dev/null > cgi_gzip_test_expected.in
python3 decompress_cgi.py
kill $PID
