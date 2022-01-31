#!/bin/bash
cd ..
value=$(python3 webserv.py tests/broken_config.cfg  2>&1 tests/broken_cfg_port_expected.out)
cd - > /dev/null
echo $value | diff - broken_cfg_port_expected.out


