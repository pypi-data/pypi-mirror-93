#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 04-01-2021
           """

from notus import PROJECT_NAME
from draugr import get_backend_module

__all__ = ["Class"]

Class = get_backend_module(
    PROJECT_NAME
).Class  # Change !Class! to backend class   #TODO: NOT DONE!
del get_backend_module

if __name__ == "__main__":
    print(Class.__doc__)
