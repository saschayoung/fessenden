#!/bin/bash


python reset_pgdb.py --host=128.173.90.88
python field_rx.py --host=128.173.90.88 -r 20 -i 1000 -m
python db_agent.py --host=128.173.90.88
# python fast_geolocation_db.py --host=128.173.90.88 
