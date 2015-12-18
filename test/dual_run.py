#!/usr/bin/python
import redis

class dual_run():
    def __init__(self, r, d):
        self.r = r
        self.d = d
    def run_verify(self, func, *args):
        r_func = getattr(self.r, func)
        d_func = getattr(self.d, func)
        r_result = r_func(*args)
        d_result = d_func(*args)
        assert r_result == d_result, ResultMismatchError(r_result, d_result)
