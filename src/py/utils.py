#!/bin/python3
import sys


def func_name():
    """
    :return: name of caller
    """
    return sys._getframe(1).f_code.co_name
