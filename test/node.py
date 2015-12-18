#!/usr/bin/python

class Node(object):
    def __init__(self, host="localhost", port=1212):
        self.host=host
        self.port=port
        self.name="Node: %s:%d" % (host, port)
    def __name__(self):
        return self.name
