#! /bin/sh
#
# one.sh
# Copyright (C) 2019 root <root@MrRobot.local>
#
# Distributed under terms of the MIT license.
#

jmeter -n -t seckill.jmx -l result/result.txt -e -o webreport
