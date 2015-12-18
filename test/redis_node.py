#!/usr/bin/python
import redis
from node import Node

class RedisNode(Node):

    def __init__(self, host, port):
        super(RedisNode, self).__init__(host, port)

    def get_connection(self):
        return redis.StrictRedis(self.host, self.port, db=0)
