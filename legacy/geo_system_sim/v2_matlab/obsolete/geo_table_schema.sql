DROP TABLE test01_table;
CREATE TABLE test01_table(index INT AUTO_INCREMENT, rpt_pkt_num INT, rpt_team_id INT, rpt_location CHAR(50),
                          rpt_timestamp CHAR(50), beaon_id INT, beacon_pkt_num INT);
CREATE INDEX index ON test01_table(index);