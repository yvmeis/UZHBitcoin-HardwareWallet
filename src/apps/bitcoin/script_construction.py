# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 14:13:46 2021

@author: Robin
"""
import btclib
import btclib.tests.test_tx
from btclib import *
from btclib.tests import *

def locking_script():
    pass

def unlocking_script():
    pass

btclib.tests.test_tx.Tx()

a = b"\x00\x01".hex()
print(a)