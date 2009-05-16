#!/usr/bin/python

import httplib
import cgi
import csv
from string import Template

def no_blanks(x):
	if not x.startswith('--,'):
		return x

def get_spreadsheet_data(url):
	(host,slash,path) = url.partition('/')
	conn = httplib.HTTPConnection(host)
	conn.request("GET", "/" + path)
	try:
		resp = conn.getresponse()
	except httplib.HTTPException:
		print resp.status, resp.reason
		raise
	data_csv = resp.read()
	data_csv = data_csv.splitlines()
	return data_csv

def get_board_seats():
	return filter(no_blanks, get_spreadsheet_data("spreadsheets.google.com/pub?key=rWOj5fxWi1wQBwy8pVbajng&output=csv&gid=1"))

def get_board_detail():
	return filter(no_blanks, get_spreadsheet_data("spreadsheets.google.com/pub?key=rWOj5fxWi1wQBwy8pVbajng&output=csv&gid=3"))

def display_board_seats(board_seats_csv):
	accum = ''
	for bs in csv.DictReader(board_seats_csv):
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
			if not name:
				phone = ''
			elif email:
				phone = " or "
			else:
				phone = " at "
			phone += bs['Contact_Phone']

		accum += ''.join([
				"<li>For ", bs['Charity'], url,
				", contact ", name, email, phone,
				".</li>\n"
			       ])
	return "<ul>\n" + accum + "</ul>"

def display_board_detail(board_details):
	accum = ''
	for i in csv.DictReader(board_details):
		name = "<b>" + i['Organization_Name'] + "</b>"
		desc = i['Description'].replace(i['Organization_Name'], name, 1)

		accum += "<li>" + desc + "</li>\n"
	return "<ul>\n" + accum + "</ul>"
