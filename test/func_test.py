#!/usr/bin/python
import redis
import argparse
import random
import string 
import time
from utils import string_generator
from dyno_node import DynoNode
from redis_node import RedisNode
from dual_run import dual_run

class ResultMismatchError(Exception):
    def __init__(self, r_result, d_result):
        self.r_result = r_result
        self.d_result = d_result
    def __str__(self):
        return "\n======Result Mismatch=======\n"\
                "Redis:'%s'"\
                "\n===========================\n"\
                "Dyno:'%s'" % (self.r_result, self.d_result)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--redis_port', metavar='r', nargs='?', default=1212,
                        type=int, help='redis server port')
    parser.add_argument('--dyno_port', metavar='d', nargs='?', default=8102,
                        type=int, help='dynomite server port')
    return parser.parse_args()


def get_dyno_connection(dyno_port):
    d = redis.StrictRedis(host='localhost', port=dyno_port, db=0)
    return d

def create_key(test_name, key_id):
    return test_name + "_" + str(key_id)

def run_key_value_tests(r, d, max_keys=1000, max_payload=1024):
    #Set some
    test_name="key_value"
    c = dual_run(r, d)
    for x in range(0, max_keys):
        key = create_key(test_name, x)
        value = string_generator(size=random.randint(512, 1024))
        c.run_verify("set", key, value)
    # get them and see
    for x in range(0, max_keys):
        key = create_key(test_name, x)
        c.run_verify("get", key)
    # append a key
    key = create_key(test_name, random.randint(0, max_keys-1))
    value = string_generator()
    c.run_verify("append", key, value)
    c.run_verify("get", key)
    # expire a few
    key = create_key(test_name, random.randint(0, max_keys-1))
    c.run_verify("expire", key, 5)
    time.sleep(7);
    c.run_verify("exists", key)

def main(args):
    redis_port = args.redis_port
    dyno_port = args.dyno_port
    r = RedisNode(host="localhost", port=redis_port)
    d = DynoNode(host="localhost", port=dyno_port)
    r_c = r.get_connection()
    d_c = d.get_connection()
    print "Running get_set func test"
    run_key_value_tests(r_c, d_c)
    print "Running large payload get_set func test"
    run_key_value_tests(r_c, d_c, max_payload=16384*1024)
    print "All test ran fine"
    return 0

if __name__ == "__main__":
    args = parse_args()
    main(args)
