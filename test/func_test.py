#!/usr/bin/python
import redis
import argparse
import random
import string 
import time
from utils import string_generator, number_generator
from dyno_node import DynoNode
from redis_node import RedisNode
from dual_run import dual_run, ResultMismatchError

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

def run_key_value_tests(c, max_keys=1000, max_payload=1024):
    #Set some
    test_name="KEY_VALUE"
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

def run_hash_tests(c, max_keys=10):
    test_name="HASH_MAP"
    # keys
    keys = []
    for x in range(0, max_keys):
        key = create_key(test_name, x)
        keys.append(key)

    # fields
    fields = []
    for x in range(0, max_keys):
        field = create_key("_field", x)
        fields.append(field)

    #hset
    for x in range(0, 1000000):
        key = random.choice(keys)
        field = random.choice(fields)
        value = number_generator()
        c.run_verify("hset", key, key + field, value)

    # hmset
    key = random.choice(keys)
    kv_pairs = {}
    for x in range(0, 5):
        field = random.choice(fields)
        value = number_generator()
        kv_pairs[key+field] = value
    c.run_verify("hmset", key, kv_pairs)

    # hmget
    key = random.choice(keys)
    list_args = [key]
    for x in range(0, 5):
        field = random.choice(fields)
        list_args.append(key + field)
    args = tuple(list_args)
    c.run_verify("hmget", *args)

    # hincrby, hdel, hexists
    key = random.choice(keys)
    field = random.choice(fields)
    c.run_verify("hincrby", key, key + field, 50)
    c.run_verify("hdel", key, key + field)
    c.run_verify("hexists", key, key + field)

    # hgetall, hkeys, hvals, hlen
    key = random.choice(keys)
    c.run_verify("hgetall", key)
    key = random.choice(keys)
    c.run_verify("hkeys", key)
    key = random.choice(keys)
    c.run_verify("hvals", key)
    key = random.choice(keys)
    c.run_verify("hlen", key)

    # finally do a hscan
    key = random.choice(keys)
    c.run_verify("hscan", key, 0)

def main(args):
    redis_port = args.redis_port
    dyno_port = args.dyno_port
    r = RedisNode(host="localhost", port=redis_port)
    d = DynoNode(host="127.0.0.2", port=dyno_port)
    r_c = r.get_connection()
    d_c = d.get_connection()
    c = dual_run(r_c, d_c)
    try:
        print "Running get_set func test"
        run_key_value_tests(c)
        print "Running large payload get_set func test"
        run_key_value_tests(c, max_payload=16384*1024)
        print "Running Hash Map func test"
        run_hash_tests(c)
        print "All test ran fine"
    except ResultMismatchError as r:
        print r;
    return 0

if __name__ == "__main__":
    args = parse_args()
    main(args)
