#!/bin/bash
cd ..
value=$(python3 webserv.py tests/broken_config2.cfg  2>&1 tests/broken_cfg_extrafield_expected.out)
cd - > /dev/null
echo $value | diff - broken_cfg_extrafield_expected.out