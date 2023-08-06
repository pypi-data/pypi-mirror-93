# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:29:12 2021

@author: Arghya Tarafdar
"""


from urllib.request import Request, urlopen

import pandas as pd


def testtop10batters():
    url='https://feed.cricket-rankings.com/feed/test/batting/'
    req_testbatting = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req_testbatting).read()
        
    result=pd.read_html(webpage)
    return(result[0][:10])
    


def testtop10bowlers():
    url='https://feed.cricket-rankings.com/feed/test/bowling/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
       
    result=pd.read_html(webpage)
    return(result[0][:10])
    

def testtop10allrounder():
    url='https://feed.cricket-rankings.com/feed/test/all-rounder/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
        
    result=pd.read_html(webpage)     
    return(result[0][:10])



def oditop10batters():
    url='https://feed.cricket-rankings.com/feed/odi/batting/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def oditop10bowling():
    url='https://feed.cricket-rankings.com/feed/odi/bowling/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def oditop10allrounder():
    url='https://feed.cricket-rankings.com/feed/odi/all-rounder/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def t20top10batters():
    url='https://feed.cricket-rankings.com/feed/t20/batting/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def t20top10bowlers():
    url='https://feed.cricket-rankings.com/feed/t20/bowling/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])

def t20top10allrounder():
    url='https://feed.cricket-rankings.com/feed/t20/all-rounder/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])



def toptestteams():
    url='https://www.espncricinfo.com/rankings/content/page/211271.html'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)[0]
    header=result.columns.to_list()
    header[1]="Top Test Teams"
    result.columns=header
    return(result)

def topoditeams():
    url='https://www.espncricinfo.com/rankings/content/page/211271.html'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)[1]
    header=result.columns.to_list()
    header[1]="Top ODI Teams"
    result.columns=header
    return(result)

def topt20teams():
    url='https://www.espncricinfo.com/rankings/content/page/211271.html'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)[2][:20]
    header=result.columns.to_list()
    header[1]="Top T20 Teams"
    result.columns=header
    return(result)

def odiwonentop10batters():
    url='https://feed.cricket-rankings.com/feed/womenodi/batting/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def odiwonentop10bowlers():
    url='https://feed.cricket-rankings.com/feed/womenodi/bowling/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])

def odiwonentop10allrounder():
    url='https://feed.cricket-rankings.com/feed/womenodi/all-rounder/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def t20wonentop10batters():
    url='https://feed.cricket-rankings.com/feed/woment20/batting/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])


def t20wonentop10bowlers():
    url='https://feed.cricket-rankings.com/feed/woment20/bowling/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])

def t20wonentop10allrounder():
    url='https://feed.cricket-rankings.com/feed/woment20/all-rounder/'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    result=pd.read_html(webpage)   
    return(result[0][:10])



# print(odiwonentop10allrounder())


