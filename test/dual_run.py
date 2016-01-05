#!/usr/bin/python
import redis

class ResultMismatchError(Exception):
    def __init__(self, r_result, d_result):
        self.r_result = r_result
        self.d_result = d_result
    def __str__(self):
        return "\n======Result Mismatch=======\n"\
                "Redis:'%s'"\
                "\n===========================\n"\
                "Dyno:'%s'" % (str(self.r_result), str(self.d_result))

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
