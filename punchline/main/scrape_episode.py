from bs4 import BeautifulSoup
import requests
import sys
import os
import re

from .models import Title, Episode

# 전체 에피소드 링크 수집
def collectLinks(sub):

    # 스크래이핑 타겟 URL
    host = 'https://www.hypnoweb.net'
    route = '/www/series-tv.2.18/'
    url = host + route + sub

    # HTTP 요청
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    # 페이지 내 에피소드 목록이 존재하는 구역
    divs = soup.findAll('div', {'class': 'rubrique'})
    
    case = []
    for rubrique in divs:
        epTable = rubrique.findAll('div', {'itemprop': 'containsSeason'})
        
        # 시즌 별 에피소드 테이블
        if epTable:
            for season in epTable:
                episodes = season.findAll('tr', {'itemprop': 'episode'})

                # 시즌 번호 수집
                seasonNum = season.find('h2', {'itemprop': 'name'}).text
                pat = re.compile('[0-9]+')
                seasonNum = re.findall(pat, seasonNum)[0]
                
                # 에피소드 테이블의 각 행에서 에피소드 번호, 에피소드 명, 에피소드 링크 수집 
                for e in episodes:
                    row = e.find('td')
                    link = row.find('a', {'itemprop': 'url'}).attrs['href'].strip()
                    epiNum = row.find('span', {'itemprop': 'episodeNumber'}).text
                    epiTitle = row.find('span', {'itemprop': 'name'}).text
                    data = [seasonNum, epiNum, epiTitle, link]
                    case.append(data)

    return case


db_title = Title.objects.values()
db_episode = Episode.objects.all()
exist = [i.title for i in db_episode]

# 스크래이퍼 실행 및 DB 저장
for k, row in enumerate(db_title, start=1):
    ID, title, sub = row.values()
    if ID not in exist:
        scrape = collectLinks(sub)
        for s in scrape:
            seasonNum, epiNum, epiTitle, link = s
            title = Title.objects.get(id=ID)
            Episode(title=title, seasonNum=seasonNum, epiNum=epiNum, epiTitle=epiTitle, link=link).save()
            
        if not k%500: print(f'Scraping: {k} Dramas Finished')
