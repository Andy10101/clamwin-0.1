#!/usr/bin/env python
#----------------------------------------------------------------------

"""
This is a way to save the startup time when running img2py on lots of
files...
"""

import sys
from wxPython.tools import img2py


command_lines = [

    "   -u -c bmp/scanprogress01.bmp throbImages.py",
    "-a -u -c bmp/scanprogress02.bmp throbImages.py",
    "-a -u -c bmp/scanprogress03.bmp throbImages.py",
    "-a -u -c bmp/scanprogress04.bmp throbImages.py",
    "-a -u -c bmp/scanprogress05.bmp throbImages.py",
    "-a -u -c bmp/scanprogress06.bmp throbImages.py",
    "-a -u -c bmp/scanprogress07.bmp throbImages.py",
    "-a -u -c bmp/scanprogress08.bmp throbImages.py",
    "-a -u -c bmp/scanprogress09.bmp throbImages.py",
    "-a -u -c bmp/scanprogress10.bmp throbImages.py",
    "-a -u -c bmp/scanprogress11.bmp throbImages.py",
    "-a -u -c bmp/scanprogress12.bmp throbImages.py",
    
    "-a -u -c -m #FF00FF bmp/update01.bmp throbImages.py",    
    "-a -u -c -m #FF00FF bmp/update02.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update03.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update04.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update05.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update06.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update07.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update08.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update09.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update10.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update11.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update12.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update13.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update14.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update15.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update16.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update17.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update18.bmp throbImages.py",
    "-a -u -c -m #FF00FF bmp/update19.bmp throbImages.py",    

    ]


for line in command_lines:
    args = line.split()
    img2py.main(args)

