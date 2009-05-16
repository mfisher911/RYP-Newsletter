#!/usr/bin/python

import RYP
import cgitb

cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print """
<h2>Board Seat Opportunities</h2>

As many of you know, RYP is working hard to secure board seats for young professionals. These organizations are interested in opening board and committee seats to young professionals. If you have an interest in serving on a board, contact the organization at their email address.

<h3>Featured Boards</h3>
"""

print RYP.display_board_detail(RYP.get_board_detail())

print "<h3>Additional Boards Seeking Members</h3>"
print RYP.display_board_seats(RYP.get_board_seats())
