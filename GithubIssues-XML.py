"""
Exports Issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import xml.etree.cElementTree as ET
import requests


GITHUB_USER = 'lxl_tuizi@hotmail.com'
GITHUB_PASSWORD = 'ziranzhiyi123='
REPO = 'elastic/elasticsearch'  # format is username/repo
#REPO = 'video-react/video-react'
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO # use this for first, and following for sub url
ISSUES_FOR_SUB_URL = 'https://api.github.com/repositories/507775/issues?filter=all&state=all&page=511'
params_payload = {'filter' : 'all', 'state' : 'all' } # state: closed, open, all
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    if not res.status_code == 200:
        tree = ET.ElementTree(rss)
        tree.write("githubIssues.xml")
        raise Exception(res.status_code)
    for issue in res.json():
        try:
            print (issue['number'])
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = issue['title']
            ET.SubElement(item, "link").text = issue['url']
            ET.SubElement(item, "project", key="", id="")
            ET.SubElement(item, "description").text = issue['body']
            ET.SubElement(item, "key", id=str(issue['id'])).text = str(issue['number'])
            ET.SubElement(item, "summary").text = issue['title']
            ET.SubElement(item, "type", id="", iconUrl="")
            ET.SubElement(item, "priority", id="", iconUrl = "")
            ET.SubElement(item, "status", id="", iconUrl="", description="").text = issue['state']
            ET.SubElement(item, "statusCategory", key="", id="", colorName="")
            ET.SubElement(item, "resolution", id="", colorName="")
            ET.SubElement(item, "assignee", username="").text = str(issue['assignee'])
            ET.SubElement(item, "reporter", username="").text = issue['user']['login']
            labels = ET.SubElement(item, "labels")
            for label in issue['labels']:
                ET.SubElement(labels, 'label').text = label['name']
            ET.SubElement(item, "created").text = issue['created_at']
            ET.SubElement(item, "updated").text = issue['updated_at']
            ET.SubElement(item, "resolved").text = issue['closed_at']
            ET.SubElement(item, "version")
            ET.SubElement(item, "fixVersion")
            ET.SubElement(item, "component")
            ET.SubElement(item, "due")
            ET.SubElement(item, "votes")
            ET.SubElement(item, "watches")
            comments = ET.SubElement(item, "comments")
            get_comments(issue['comments_url'], comments)
            ET.SubElement(item, "attachments")
            ET.SubElement(item, "subtasks")
            ET.SubElement(item, "customfields")
        except:
            print ("Exception: " + str(issue['number']))
def get_comments(commentURL, comments):
   try:     
        comment_res = requests.get(commentURL, auth = AUTH)
        for comment in comment_res.json():
            if comment != None:
                ET.SubElement(comments, "comment", id=str(comment['id']), created=comment['created_at'], author=comment['user']['login']).text = comment['body']
   except:
       print ("comment exception!")
res = requests.get(ISSUES_FOR_SUB_URL, params=params_payload, auth=AUTH)
rss = ET.Element("rss")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title")
ET.SubElement(channel, "link")
ET.SubElement(channel, "description")
ET.SubElement(channel, "language")
ET.SubElement(channel, "issue", total="0", end="0", start="0")
buildInfo = ET.SubElement(channel, "build-info")
ET.SubElement(buildInfo, "version")
ET.SubElement(buildInfo, "build-number")
ET.SubElement(buildInfo, "build-date")
write_issues(res)
pageNumber = 1
fileNumber = 13

#more pages? examine the 'link' header returned
while True:
    if 'link' not in res.headers:
        break;
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                res.headers['link'].split(',')]])
    print (pages['next'])
    res = requests.get(pages['next'], params=params_payload, auth=AUTH)
    write_issues(res)
    
    if pages['next'] == pages['last']:
        break
    pageNumber += 1
    if pageNumber == 30:
        tree = ET.ElementTree(rss)
        tree.write("githubIssues" + str(fileNumber) + ".xml")        
        fileNumber += 1
        pageNumber = 0;
        rss = ET.Element("rss")
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title")
        ET.SubElement(channel, "link")
        ET.SubElement(channel, "description")
        ET.SubElement(channel, "language")
        ET.SubElement(channel, "issue", total="0", end="0", start="0")
        buildInfo = ET.SubElement(channel, "build-info")
        ET.SubElement(buildInfo, "version")
        ET.SubElement(buildInfo, "build-number")
        ET.SubElement(buildInfo, "build-date")
        
tree = ET.ElementTree(rss)
tree.write("githubIssues" + str(fileNumber) + ".xml")
