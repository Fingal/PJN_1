# -*- coding: utf-8 -*-
__author__ = 'Fingal'
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
import datetime
import pickle
import winsound
import sys
import os


def process_number(number):
    if number[-1]=='k':
        return int(float(number[:-1])*1000)
    return int(number.replace(',',''))


def process_date(date_):
        if "'" in date_:
            return datetime.datetime.strptime(date_, "%b %d '%y at %H:%M")
        return datetime.datetime.strptime(date_ +' 15', "%b %d at %H:%M %y")

links=open('links.txt').readlines()
bad_counter=0
start=8000
stop=10000
try:
    for i,link in zip(range(stop-start),links[start:stop+1]):
        url=link.rstrip()
        req = Request(url, headers={'User-Agent' : "Magic Browser"})
        page = urlopen(req)
        soup = BeautifulSoup(page.read())
        data={}
        div_question=soup.find('div',id='question')
        user=div_question.find('td',class_='post-signature owner')
        question = {'title': soup.find('a', class_='question-hyperlink').get_text(),
                   'text': str(div_question.find('div',class_='post-text')),
                   'votes': int(div_question.find('span',class_='vote-count-post').get_text()),
                   'favorites_count': int(div_question.find('div',class_='favoritecount').b.get_text()),
                   'tags': [tag.get_text() for tag in div_question.find_all('a',rel='tag')]}
        try:
            question['time'] = process_date(user.find('span',class_='relativetime').get_text())
        except:
            pass
        try:
            question['user'] = {'name': user.find('div',class_='user-details').a.get_text()}
        except AttributeError:
            pass
        try:
            question['user']['reputation'] = process_number(user.find('div',class_='user-details').span.get_text())
        except:
            pass
        data['question']=question
        data['answers']=[]
        for div_answer in soup.find_all('div',class_="answer"):
            try:
                user = div_answer.find_all('td',class_='post-signature')[-1]
            except:
                bad_counter+=1
                continue
            answer = {'text': str(div_answer.find('div',class_='post-text')),
                      'votes': int(div_answer.find('span',class_='vote-count-post').get_text())}
            try:
                answer['time'] = process_date(user.find('span',class_='relativetime').get_text())
            except:
                pass
            try:
                answer['user'] = {'name': user.find('div',class_='user-details').a.get_text()}
            except AttributeError:
                pass
            try:
                answer['user']['reputation'] = process_number(user.find('div',class_='user-details').span.get_text())
            except:
                pass
            if div_answer.find('span', class_='vote-accepted-on'):
                answer['accepted'] = True
            else:
                answer['accepted'] = False
            data['answers'].append(answer)
        file=open('pickled/'+str(i+start),'wb')
        pickle.dump(data,file)
        file.close()
        print('link: ',link,end='\t')
        print('plik: ',i+start,end='\t')
        print("wykonano pobrano {:2.3f}% postów. {:d} odpowiedzi źle wczytanych.".format((i+1)/float(stop-start)*100,bad_counter))
    print('pobieranie zakończone')
except Exception as a:
    winsound.Beep(500,5000)
    raise a
winsound.Beep(1000,2000)
#os.system('shutdown /h /t 1')