# coding: utf-8
import os
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import datetime
import json
import smtplib
from email.mime.text import MIMEText
from settings import MAILL_SETTING

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}
ACTIVITIES_FILE = "activities.json"

if not os.path.isfile(ACTIVITIES_FILE):
    print("create %s" % ACTIVITIES_FILE)
    activities_file = open(ACTIVITIES_FILE, "w")
    activities_file.write("{}")
    activities_file.close()


def send_mail(title, href):
    maill_boday = "<a href='"+href+"'>"+title+"</a>"
    msg = MIMEText(maill_boday, 'html', 'utf-8')
    msg['From'] = MAILL_SETTING['from']
    msg['To'] = MAILL_SETTING['to']
    msg['Subject'] = 'bwg new activity!'

    server = smtplib.SMTP(MAILL_SETTING['smtp'])
    server.login(user=MAILL_SETTING["from"],
                 password=MAILL_SETTING['password'])
    server.send_message(msg=msg)
    server.close()


def load_activities():
    activities_dict = json.load(open(ACTIVITIES_FILE, "r"))
    if not activities_dict:
        return {}
    return activities_dict


def save_activities(title, href):
    href = str(href)
    activities_dict = (load_activities())
    if href not in activities_dict:
        print("<a href='"+href+"'>"+title+"</a>")
        activities_dict[href] = title
        activities_file = open(ACTIVITIES_FILE, "w")
        activities_file.write(json.dumps(
            activities_dict, ensure_ascii=False, indent=2))
        activities_file.close()
        send_mail(title, href)


def fetch_activities():
    url = "https://www.bwgyhw.com/"
    response = requests.get(url, headers=header)
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    articles = soup.select("article")
    for article in articles:        
        title = article.select("h2 a")[0].get("title")
        href = article.select("h2 a")[0].get("href")
        time=article.select("time")[0].text
        save_activities(time +" "+ title, href)


if __name__ == '__main__':
    fetch_activities()
