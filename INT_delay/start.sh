#!/bin/bash

simple_switch_CLI --thrift-port 9090 < s1-commands.txt
simple_switch_CLI --thrift-port 9091 < s2-commands.txt
simple_switch_CLI --thrift-port 9092 < s3-commands.txt

