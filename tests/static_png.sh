#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
sleep 1
curl localhost:8070/playerRight.png | diff - static_png_expected.out

kill $PID
