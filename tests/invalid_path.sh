#!/bin/bash
cd ..
python3 webserv.py config.cfg &
PID=$!
cd - > /dev/null
python3 ../webserv.py invalid  2> invalid_path.in
diff invalid_path.in invalid_path.out
kill $PID
