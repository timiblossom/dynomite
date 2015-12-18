#!/usr/bin/python
import redis
import argparse
import random
import string 
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

def run_get_set(r, d):
    for x in range(0, 1000):
        key = __name__ + str(x)
        value = string_generator(size=random.randint(512, 1024))
        r_result = r.set(key, value)
        d_result = d.set(key, value)
    for x in range(0, 1000):
        key = __name__ + str(x)
        r_result = r.get(key)
        d_result = d.get(key)
        assert r_result == d_result, ResultMismatchError(r_result, d_result)

def main(args):
    redis_port = args.redis_port
    dyno_port = args.dyno_port
    r = RedisNode(host="localhost", port=redis_port)
    d = DynoNode(host="localhost", port=dyno_port)
    r_c = r.get_connection()
    d_c = d.get_connection()
    run_get_set(r_c, d_c)

if __name__ == "__main__":
    args = parse_args()
    main(args)
