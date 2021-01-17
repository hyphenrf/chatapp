#!/bin/sh

cc -o libcrc.so $(paste -d" " compile_flags.txt) crc.c
