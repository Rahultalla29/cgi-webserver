#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl -H 'Accept-Encoding: gzip' localhost:8070/js_gzip_test.js  2> /dev/null > gzip_test_js_expected.out
python3 decompress.py

kill $PID