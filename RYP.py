#!/usr/bin/python

import httplib
import cgi
import csv
from string import Template

def no_blanks(x):
    if not x.startswith('--,') and not x.startswith('#N/A,'):
        return x

def clean_spreadsheet_data(url):
    result = []
    data = csv.DictReader(filter(no_blanks, get_spreadsheet_data(url)))
    for i in data:
        result.append(i)
    return result

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
    return clean_spreadsheet_data("spreadsheets.google.com/pub?key=rWOj5fxWi1wQBwy8pVbajng&output=csv&gid=1")

def get_board_detail():
    return clean_spreadsheet_data("spreadsheets.google.com/pub?key=rWOj5fxWi1wQBwy8pVbajng&output=csv&gid=3")

def get_job_ops():
    return clean_spreadsheet_data("spreadsheets.google.com/pub?key=rWOj5fxWi1wQBwy8pVbajng&gid=5&output=csv")

def de_dupe(detail, seats):
    for i in detail:
        for j in seats:
            if i['Organization_Name'] == j['Charity']:
                seats = [s for s in seats if s['Charity'] <> j['Charity']]
    return seats

def display_board_seats(board_seats):
    accum = ''
    for bs in board_seats:
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

def format_desc_html(desc):
    return desc.replace("<", "&lt;").replace(">", "&gt;")

def format_org_name(i):
    name = "<b>" + i['Organization_Name'] + "</b>"
    desc = format_desc_html(i['Description'])
    desc = desc.replace(i['Organization_Name'], name, 1)
    return desc
    
def display_board_detail(board_details):
    accum = ''
    for i in board_details:
        desc = format_org_name(i)
        accum += "<li>" + desc + "</li>\n"
    return "<ul>\n" + accum + "</ul>"

def display_job_ops(job_ops):
    accum = ''
    if len(job_ops) == 1:
        i = job_ops[0]
        return "<p>" + format_org_name(i) + "</p>"
    elif len(job_ops) > 1:
        for i in job_ops:
            desc = format_org_name(i)
            accum += "<li>" + desc + "</li>\n"
        return "<ul>\n" + accum + "</ul>"
