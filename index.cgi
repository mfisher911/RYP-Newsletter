#!/usr/bin/python

import httplib
import cgi
import cgitb
import csv
from string import Template

cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

def get_board_seats():
	bs_conn = httplib.HTTPConnection('spreadsheets.google.com')
	bs_conn.request("GET", '/pub?key=rWOj5fxWi1wQBwy8pVbajng&output=csv&gid=1')
	bs_resp = bs_conn.getresponse()
	board_seats_csv = bs_resp.read()
	board_seats_csv = board_seats_csv.splitlines()
	return board_seats_csv

def display_board_seats(board_seats_csv):
	print "<h2>Board Seat Opportunities</h2>\n<ul>"
	for bs in csv.DictReader(board_seats_csv):
		# I'd like to remove the "--,--,--,--" blank lines at the source.
		if bs['Charity'] == "--":
			continue
		name = ''
		email = ''
		url = ''
		phone = ''

		if bs['Contact_Name']:
			name = bs['Contact_Name']

		if bs['Contact_Email']:
			if name:
				email = " at "
			email += "&lt;" + bs['Contact_Email'] + "&gt;"

		if bs['URL']:
			url = Template(" ($url)").substitute(url=bs['URL'])

		if bs['Contact_Phone']:
			if email:
				phone = " or "
			else:
				phone = " at "
			phone += bs['Contact_Phone']

		print ''.join([
			Template("<li>For $charity").substitute(charity=bs['Charity']),
				url,

				", contact ",
				name,
				email,
				phone,
			".</li>"])
	print "</ul>"

display_board_seats(get_board_seats())
