#!/usr/bin/python
import redis
import argparse
import random
import string 
import time
from utils import string_generator
from dyno_node import DynoNode
from redis_node import RedisNode

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

def run_key_value_tests(r, d):
    #Set some
    max_keys = 1000
    for x in range(0, max_keys):
        key = __name__ + str(x)
        value = string_generator(size=random.randint(512, 1024))
        r_result = r.set(key, value)
        d_result = d.set(key, value)
    # get them and see
    for x in range(0, max_keys):
        key = __name__ + str(x)
        r_result = r.get(key)
        d_result = d.get(key)
        assert r_result == d_result, ResultMismatchError(r_result, d_result)
    # append a key
    key = __name__ + str(random.randint(0, max_keys-1))
    value = string_generator()
    r_result = r.append(key, value)
    d_result = d.append(key, value)
    assert r_result == d_result, ResultMismatchError(r_result, d_result)
    r_result = r.get(key)
    d_result = d.get(key)
    assert r_result == d_result, ResultMismatchError(r_result, d_result)
    # expire a few
    key = __name__ + str(random.randint(0, max_keys-1))
    r_result = r.expire(key, 5)
    d_result = d.expire(key, 5)
    assert r_result == d_result, ResultMismatchError(r_result, d_result)
    time.sleep(7);
    r_result = r.exists(key)
    d_result = d.exists(key)
    assert r_result == d_result, ResultMismatchError(r_result, d_result)


def main(args):
    redis_port = args.redis_port
    dyno_port = args.dyno_port
    r = RedisNode(host="localhost", port=redis_port)
    d = DynoNode(host="localhost", port=dyno_port)
    r_c = r.get_connection()
    d_c = d.get_connection()
    print "Running get_set func test"
    run_key_value_tests(r_c, d_c)
    print "All test ran fine"
    return 0

if __name__ == "__main__":
    args = parse_args()
    main(args)
