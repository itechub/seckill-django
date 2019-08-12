#! /bin/sh
#
# csv.sh
# Copyright (C) 2019 root <root@MrRobot.local>
#
# Distributed under terms of the MIT license.
#

filepath="jmeter/userconfig.csv"
system_info()
{
    echo "User Config Data Helper"
    echo "This script will generate user uuid, given the user amount when calling this script, it will generate JMeter csv config data format."
}   
> $filepath

system_info

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "To generate 10 user in config file: \$ $0 10"
    exit -1
fi

echo "Generate uuid from 1 to $1"

for((i=1;i<=$1;i++));
    do echo "$i," >> $filepath;
done
