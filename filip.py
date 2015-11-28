__author__ = 'Fingal'
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen

import csv

url='http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl'
page = open('site')
soup = BeautifulSoup(page.read())
table_body = soup.find('tbody')
values=[[value.get_text().strip() for value in row.find_all('td') if value.get_text().rstrip()] for row in table_body.find_all('tr')]
values=list(filter(None,values))
new_values=[]
more=[]
for value in values:
    if value[1].isalpha():
        more=value[0:2]
    elif value[0].isalpha():
        value[0:1]=more
    else:
        value[0:0]=more
    new_values.append(value[0:4])
with open('eggs.csv','w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    writer.writerows(new_values)