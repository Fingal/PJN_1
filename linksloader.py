# -*- coding: utf-8 -*-
__author__ = 'Fingal'
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
mpoint=9000
links = open('links.txt',mode='w')
url='http://stackoverflow.com/questions?page={}&sort=votes'
i=1
for i in range(2800):
    u = url.format(i)
    req = Request(u, headers={'User-Agent' : "Magic Browser"})
    page = urlopen(req)
    soup = BeautifulSoup(page.read())
    questions = soup.find_all('a', class_='question-hyperlink')
    points=[int(point.strong.get_text()) for point in soup.find_all('span', class_='vote-count-post')]
    for point,link in zip(points,['http://stackoverflow.com'+question['href']+'\n' for question in questions]):
        if point>=50:
            links.write(link)
    print('pobieranie linków wykonano w {:2.2f} procentach'.format((i/2800.0)*100))
links.close()