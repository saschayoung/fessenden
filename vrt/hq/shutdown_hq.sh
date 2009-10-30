#!/bin/bash

sudo kill -9 `ps ax | grep python | grep hq | awk {'print $1'}`