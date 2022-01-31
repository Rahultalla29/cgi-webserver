#!/bin/bash
cd ..
value=$(python3 webserv.py tests/broken_config3.cfg  2>&1 tests/broken_cfg_field_missing.out)
cd - > /dev/null
echo $value | diff - broken_cfg_field_missing.out