#!/bin/bash

HOST=128.173.90.68

python reset_pgdb.py --host=$HOST
python field_rx.py --host=$HOST -r 2 -i 1000  --inc_move
python db_agent.py --host=$HOST
python fast_geolocation_db.py --host=$HOST
