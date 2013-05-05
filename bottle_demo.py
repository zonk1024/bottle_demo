#!/usr/bin/env python

import bottle
from bottle import run
import redis
import time

r = redis.Redis()

application = bottle.Bottle()

a = {'1': 1, 1: 2}

def wrap(func):
    def color():
        return '<font color=\'red\'>{}</font>'.format(func())
    return color

class Prime(object):
    def __init__(self, number):
        self.prime = self.next_prime(number)
    def next_prime(self, n):
        start = time.time()
        n_in = n
        v = r.get(n)
        good = True
        if v:
            good = False
            n = v
        while good:
            for i in xrange(2, n - 1):
                if n % i == 0:
                    n += 1
                    continue
            good = False
            r.set(n_in, n)
        self._time = round(time.time() - start, 4)
        return n
    def time_run(self):
        return self._time
    def __str__(self):
        return str(self.prime)

@application.route('/')
@wrap
def index():
    return 'Hello, World!'

@application.route('/prime/<number:int>')
def prime_ret(number):
    p = Prime(number)
    n = p.prime
    t = p.time_run()
    return '{}\nRan in {} seconds.'.format(n, t)

@application.route('/a')
def a_json():
    return a

run(application, port=8091)
