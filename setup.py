# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 19:15:22 2024

@author: mikey
"""

from cx_Freeze import setup, Executable

setup(
    name="Lab_calculator",
    version="0.1",
    description="Lab Calculator",
    executables=[Executable("Lab_calculator_0.1.0.py")]
)