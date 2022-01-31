#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
python3 ../webserv.py 2> missing_arg.in
diff missing_arg.in missing_arg.out
kill $PID
