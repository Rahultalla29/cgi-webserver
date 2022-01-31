#!/bin/bash
cd ..
python3 webserv.py tests/broken_cfg_spacing.cfg 2> tests/broken_cfg_spacing.in
cd - > /dev/null
diff broken_cfg_spacing.in broken_cfg_spacing.out
