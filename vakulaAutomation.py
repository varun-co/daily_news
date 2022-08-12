#!/usr/bin/env python3
import time
import requests
import smtplib
from bs4 import BeautifulSoup
import ssl
from email.message import EmailMessage
from datetime import date
DRIVER_PATH = '/home/varun/scripts/drivers'
WEBSTIE_NAMES_FILE_PATH = './newsWebsite.txt'
SENDER = 'vr9clown@gmail.com'
RECIVER = 'varungiri13@gmail.com'
PASSWORD = '*************'
def getAllWebSiteNames(fileName):
    with open(fileName) as fhandle:
        allWebsites = fhandle.read().splitlines()
    return allWebsites
def barAndBench(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    divs = soup.find_all('div',class_='three-col-seven-story-m_card__79HKh')
    allGeneratedLinks = list()
    for div in divs:
        soup = BeautifulSoup(str(div),'html5lib')
        links = soup.find_all('a')
        for link in links:
            allGeneratedLinks.append(link.get('href'))
        allGeneratedLinks = filterLinks(allGeneratedLinks)
    return list(set(allGeneratedLinks))


def bharat(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    divs = soup.find_all('div',class_='is-layout-flow wp-block-group alignwide')
    allGeneratedLinks = list()
    for div in divs:
        soup = BeautifulSoup(str(div),'html5lib')
        links = soup.find_all('a')
        for link in links:
            allGeneratedLinks.append(link.get('href'))
        #allGeneratedLinks = filterLinks(allGeneratedLinks)
    return list(set(allGeneratedLinks))

def nls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    divs = soup.find_all('div',class_='blog-listing__top')
    allGeneratedLinks = list()
    for div in divs:
        soup = BeautifulSoup(str(div),'html5lib')
        links = soup.find_all('a')
        for link in links:
            allGeneratedLinks.append(link.get('href'))
        #allGeneratedLinks = filterLinks(allGeneratedLinks)
    return list(set(allGeneratedLinks))
def liveLaw(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    divs = soup.find('div',class_='m_top10')

    soup = BeautifulSoup(str(divs),'html5lib')
    divs = soup.find_all('h2',class_='text_heading text_margin_top_bottom')
    divs = divs + soup.find_all('h2',class_='text_heading m_bottom20')

    allGeneratedLinks = list()
    for div in divs:
        soup = BeautifulSoup(str(div),'html5lib')
        links = soup.find_all('a')
        for link in links:
            allGeneratedLinks.append(link.get('href'))
    allGeneratedLinks = attachBasetoGeneratedLinks(allGeneratedLinks,url)
    return list(set(allGeneratedLinks))

def project39a(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    divs = soup.find_all('div',class_='col sqs-col-6 span-6')
    allGeneratedLinks = list()
    for div in divs:
        soup = BeautifulSoup(str(div),'html5lib')
        links = soup.find_all('a')
        for link in links:
            allGeneratedLinks.append(link.get('href'))
        #allGeneratedLinks = filterLinks(allGeneratedLinks)
    return list(set(allGeneratedLinks))

def getModifier(url):
    if url == 'https://www.barandbench.com':
        return barAndBench(url)
    elif url == 'https://www.livelaw.in':
        return liveLaw(url)
    elif url == 'https://bharatchugh.in':
        return bharat(url)
    elif url == 'https://www.nls.ac.in/the-nls-blog':
        return nls(url)
    elif url == 'https://www.project39a.com':
        return project39a(url)

def writeToFile(filename,contentList):
    with open(filename,mode='w') as fhandle:
        for line in contentList:
            fhandle.write(line + '\n')

def getTopStoriesUrl(url):
    if url == 'https://www.livelaw.in/top-stories':
        return url
    else:
        return url


def attachBasetoGeneratedLinks(links,url):
    links = list(links)
    for i,_ in enumerate(links):
        links[i] = url +  links[i]
    return links

def filterLinks(unFilteredLinks):
    filteredLinks = list()
    for link in unFilteredLinks:
        if link[:8] == 'https://':
            filteredLinks.append(link)
    return filteredLinks

def getHeadLines(url):
    allGeneratedLinks = getModifier(url)
    return allGeneratedLinks
def sendMail(msg):
    print('Sending Mail')
    today = date.today()
    subject = 'Daily News' + today
    body = "\n".join(msg)
    em = EmailMessage()
    em['From'] = SENDER
    em['To'] = RECIVER
    em['Subject'] = subject
    em.set_content(body)
    context =ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as fhandle:
        fhandle.login(SENDER,PASSWORD)
        fhandle.sendmail(SENDER,RECIVER,em.as_string())
def main():
    websitesNames = getAllWebSiteNames(WEBSTIE_NAMES_FILE_PATH)
    links = list()
    for website in websitesNames:
        links = links + getHeadLines(website)
    sendMail(links)
    #writeToFile('temp.txt',links)




if __name__ == '__main__':
    main()
