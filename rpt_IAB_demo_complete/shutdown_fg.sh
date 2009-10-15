#!/bin/bash

kill -9 `ps ax | grep python | grep IAB | awk {'print $1'}`


kill -9 `ps ax | grep python | grep bench | awk {'print $1'}`
rm -f last_location
