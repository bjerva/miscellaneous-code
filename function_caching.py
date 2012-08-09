#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Function caching (Py-decorator).

This should significantly speed up function calls in cases where:
    -A function is called often with the same in-data
    AND especially if:
    -The function being called is computationally expensive
It will be useless to use this decorator if:
    -The function is never called with the same in-data multiple times
    OR
    -The function is computationally virtually cost-free (i.e. ~O(1)).

The time saved by using this is at the expense of space,
as each in-data : return-value pair is stored in a dictionary.
"""
__author__ = "Johannes Bjerva"
__version__ = "1.0.0"
__email__ = "johannesbjerva@gmail.com"
__status__ = "Fully functional"

import functools

class FuncCache(object):
    def __init__(self, function):
        """Constructor takes a function as in-data"""
        self.function = function
        self.cache = {}
    
    def __call__(self, *args):
        """
        When the function is called, the cache is searched for previous func. calls 
        with the same indata, which is returned if found. Otherwise, the function is
        called 'normally' and the data is cached and returned.
        """
        if args in self.cache: return self.cache[args] #Return if cached
        
        try:
            value = self.function(*args)    #Calculate 'normally'
            self.cache[args] = value        #Cache it
            return value
        except TypeError:
            #Uncachable, i.e. if argument is list (can't be key)
            #TODO: Convert to tuple?
            return self.function(*args) #Return without caching
    
@FuncCache
def cached_fib(n):
    "Recursive calculation of fibonacci numbers."
    if n in (0, 1):
        return n
    return cached_fib(n-1) + cached_fib(n-2)

def uncached_fib(n):
    "Recursive calculation of fibonacci numbers."
    if n in (0, 1):
        return n
    return uncached_fib(n-1) + uncached_fib(n-2)


if __name__ == "__main__":
    # Simple proof of concept
    import time
    start = time.time()
    print cached_fib(35)
    end = time.time()
    first = end-start
    start = time.time()
    print uncached_fib(35)
    end = time.time()
    second = end-start
    
    print "Cached calculation:\t"+str(first)+" s"
    print "Uncached calculation:\t"+str(second)+" s"
