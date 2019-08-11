#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:07:34 2019

@author: manzars
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

url = "http://welcome.muarfurniture.org/en/member"

wb = webdriver.Chrome("/home/manzars/Downloads/chromedriver")
wb.get(url)

xpath_main = '//*[@id="filters"]/li['

for i in range(3, 29):
    xpath = xpath_main + str(i) + ']'
    wb.find_element_by_xpath(xpath).click()
    time.sleep(4)
    
html = wb.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')
wb.close()

div = soup.findAll('div', {'id': 'portfoliolist'})
a = div[0].findAll('a')

links = []
for ele in a:
    links.append(ele.attrs['href'])

header = "Company Name, Telephone, Email, Website\n"
file = open('assignment.csv', 'w')
file.write(header) 

for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    name = soup.findAll('head')[0].title.text.split('- Muar Furniture Association')[0]
    #print(name)
    table = soup.findAll('table')
    td = table[1].findAll('td')
    td = td[2::3]
    
    try:
        tel = td[0].text
    except:
        tel = 'NaN'
        
    try:    
        fax = td[1].text
    except:
        fax = 'NaN'
    
    try:
        email = td[2].a.text
    except:
        email = 'NaN'
        
    try:  
        web = td[3].a.text
    except:
        web = 'NaN'
        
    if(tel == '-'):
        tel = 'NaN'
    if(fax == '-'):
        fax = 'NaN'
    if(email == '-'):
        email = 'NaN'
    if(web == '-'):
        web = 'NaN'
    
    print(tel, fax, email, web)
    file.write(name.replace(',', '').replace('\n', '') + ', ' + tel.replace(',', '').replace('\n', '') + ', ' + email.replace(',', '').replace('\n', '') + ', ' + web.replace(',', '').replace('\n', '') + '\n')
file.close() 