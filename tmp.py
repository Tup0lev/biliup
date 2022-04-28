#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 12:04:26 2022

@author: tup0lev
"""

for _char in string:
    if '\u4e00' <= _char <= '\u9fa5':
        print(False)



if all(x.isalpha() or x.isspace() or x.isdigit() or x=="_" or x=="-" for x in string ):
    print(True)
else: 
    print(False)
