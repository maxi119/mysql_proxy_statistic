mysql_proxy_statistic
=====================

���R mysql-proxy log �� query time

�ҨϥΪ� module �� --proxy-lua-script=share/doc/mysql-proxy/tutorial-query-time.lua
�ϥΤ覡 

bin/mysql-proxy --defaults-file mysql-proxy.ini \
--proxy-lua-script=share/doc/mysql-proxy/tutorial-query-time.lua | python log_stat.py

�� Ctrl + C �����ɦL�X�έp���

>
    Max
    time                count        query
    1      25.719ms         16          INSERT INTO mytable
    2       5.759ms          1          SHOW TABLES
    3       3.934ms          6          CALL usp_write_1
    4       3.264ms          1          CALL usp_write_2
    5       2.995ms          2          CALL usp_write_3
    6       2.920ms          1          CALL usp_read_4
    7       2.732ms          1          update something
    8       2.573ms          7          select somethin
   
   
   