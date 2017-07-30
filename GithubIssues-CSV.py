"""
Exports Issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests


GITHUB_USER = 'lwc541117@gmail.com'
GITHUB_PASSWORD = 'lwc541117+'
REPO = 'video-react/video-react'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
params_payload = {'filter' : 'all', 'state' : 'all' } # state: closed, open, all
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    print "output a list of issues to csv"
    if not res.status_code == 200:
        raise Exception(res.status_code)
    for issue in res.json():
        print issue
        csvout.writerow([issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'), issue['created_at'], issue['updated_at']])


res = requests.get(ISSUES_FOR_REPO_URL, params=params_payload, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
f = open(csvfile, 'wb')
csvout = csv.writer(f)
csvout.writerow(('id', 'Title', 'Body', 'Created At', 'Updated At'))
write_issues(res)

#more pages? examine the 'link' header returned
if 'link' in res.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                res.headers['link'].split(',')]])
    while 'last' in pages and 'next' in pages:
        res = requests.get(pages['next'], params=params_payload, auth=AUTH)
        write_issues(res)
        if pages['next'] == pages['last']:
            break
f.close()
