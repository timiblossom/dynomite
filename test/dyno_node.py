#!/usr/bin/python
import redis
from node import Node

class DynoNode(Node):

    def __init__(self, host, port):
        super(DynoNode, self).__init__(host, port)
        self.name="Dyno" + self.name

    def get_connection(self):
        return redis.StrictRedis(self.host, self.port, db=0)
