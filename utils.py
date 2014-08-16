# coding=utf-8
import time
import logging

def timeit(func):
    '''
    This function is used to evaluate the execution time of a function
    '''
    def timed_function(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        logging.info('function {} has spend {} seconds'.format(func.__name__, t2-t1))
    return timed_function

def append_or_extend(l, item):
    '''
    when item is a list, l.extends(item)
    when item is not a list, l.append(item)
    '''
    if type(item) == list:
        return l.extends(item)
    else:
        return l.append(item)


