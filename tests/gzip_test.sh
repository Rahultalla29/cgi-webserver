#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl -H 'Accept-Encoding: gzip' localhost:8070/testzip.txt  2> /dev/null > gzip_test_expected.out
python3 decompress.py
kill $PID
