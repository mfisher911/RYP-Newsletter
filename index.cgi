#!/usr/bin/python

import RYP
import cgitb

cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print """
<h2>Board Seat Opportunities</h2>

As many of you know, RYP is working hard to secure board seats for young professionals. These organizations are interested in opening board and committee seats to young professionals. If you have an interest in serving on a board, contact the organization at their email address.
"""

board_detail_list = RYP.get_board_detail()
board_seat_summary = RYP.de_dupe(board_detail_list, RYP.get_board_seats())

if len(board_detail_list) > 0:
    print "<h3>Featured Boards</h3>"
    print RYP.display_board_detail(board_detail_list)

if len(board_seat_summary) > 1:
    if len(board_detail_list) == 0:
        print "<h3>Boards Seeking Members</h3>"
    else:
        print "<h3>Additional Boards Seeking Members</h3>"
    print RYP.display_board_seats(board_seat_summary)

job_ops = RYP.get_job_ops()
if len(job_ops) > 0:
    print """
<h2>Employment Opportunities</h2>

RYP will announce employment opportunities that are a strong fit for our members. If your organization is actively recruiting young professionals, please contact us at <networking@r-y-p.org> to provide details that we can share.
"""
    print RYP.display_job_ops(job_ops)
