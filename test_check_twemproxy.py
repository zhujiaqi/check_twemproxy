#!/usr/bin/python
# -*- coding: utf-8 -*-

from mock import Mock
from mock import call
from mock import patch

from check_twemproxy import check_once, compare_results

conf = {
    'host': '',
    'port': 22222,
}

test_value1 = '''{"service":"nutcracker", "source":"gh-r410-05", "version":"0.2.4", "uptime":395737, "timestamp":1384402695, "gamma": {"client_eof":1691, "client_err":85, "client_connections":91, "server_ejects":1, "forward_error":6956, "fragments":69764780, "192.168.10.14:11212": {"server_eof":0, "server_err":0, "server_timedout":214, "server_connections":1, "server_ejected_at":1384007400136892, "requests":129794606, "request_bytes":20316998020, "responses":129206462, "response_bytes":45151527179, "in_queue":1, "in_queue_bytes":31, "out_queue":0, "out_queue_bytes":0}}}\n'''
test_value2 = '''{"service":"nutcracker", "source":"gh-r410-05", "version":"0.2.4", "uptime":395737, "timestamp":1384402695, "gamma": {"client_eof":1691, "client_err":85, "client_connections":91, "server_ejects":1, "forward_error":6956, "fragments":69764780, "192.168.10.14:11212": {"server_eof":0, "server_err":0, "server_timedout":214, "server_connections":0, "server_ejected_at":1384007400136892, "requests":0, "request_bytes":20316998020, "responses":129206462, "response_bytes":45151527179, "in_queue":1, "in_queue_bytes":31, "out_queue":0, "out_queue_bytes":0}}}\n'''

mock_check_output = Mock()
mock_check_output.return_value = test_value1

with patch('subprocess.check_output', mock_check_output):
    trial1 = check_once(conf)

problem1, rv1 = compare_results(trial1, trial1)
assert problem1 is None
assert rv1 == 0
    
mock_check_output.return_value = test_value2
with patch('subprocess.check_output', mock_check_output):
    trial2 = check_once(conf)

problem2, rv2 = compare_results(trial1, trial2)
assert problem2 is not None
print problem2
assert rv2 == 1

