from bs4 import BeautifulSoup
import requests
import sys
import os
import re

from .models import Title

# 드라마 전체 링크 수집
def collectLinks():

    # 스크래이핑 타겟 URL
    host = 'https://www.hypnoweb.net'
    route = '/www/series-tv.2.18/'
    url = host + route

    # HTTP 요청
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    # 페이지 내 드라마 목록이 존재하는 구역
    divs = soup.findAll('div', {'class': 'rubrique'})

    case = {}
    for rubrique in divs:

        # 드라마 링크
        rows = rubrique.findAll('div', {'class': 'row'})

        # "드라마 제목: 링크" 형태로 스크래이핑
        if rows:
            for r in rows:
                titles = r.findAll('div', {'class': re.compile('^(large).+')})
                for title in titles:
                    case[title.text.strip()] =  title.find('a').attrs['href'].strip()

    return case


# 스크래이퍼 실행
scrape = collectLinks()
db = Title.objects.all()
exist = [i.title for i in db]

# DB 저장
for title, sub in scrape.items():
    if title not in exist:
        Title(title=title, sub=sub).save()
