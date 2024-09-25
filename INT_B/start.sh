#!/bin/bash
cd ./flowtable
simple_switch_CLI --thrift-port 9090 < s1-commands.txt
simple_switch_CLI --thrift-port 9094 < s5-commands.txt
simple_switch_CLI --thrift-port 9092 < s3-commands.txt
simple_switch_CLI --thrift-port 9091 < s2-commands.txt
simple_switch_CLI --thrift-port 9095 < s6-commands.txt
simple_switch_CLI --thrift-port 9093 < s4-commands.txt
