#!/usr/bin/python

import RYP
import cgitb

cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print RYP.display_board_seats(RYP.get_board_seats())
