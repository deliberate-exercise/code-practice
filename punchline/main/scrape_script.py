from bs4 import BeautifulSoup
import requests
import sys
import os
import re

from .models import Title, Episode

# 스크립트를 저장할 폴더 생성
def createFolder(sub):

    path = os.path.dirname(os.path.abspath(__file__)) + r'\%s'%sub
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else: return False


# 에피소드 별 스크립트 수집
def collectScript(url):

    pat = re.compile(r'^(https://www\.hypnoweb\.net)')
    if re.match(pat, url): return False

    # HTTP 요청
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    # 페이지 스크립트가 존재하는 구역
    divs = soup.findAll('div', {'class': 'rubrique'})

    for rubrique in divs:
        script = rubrique.find('div', {'class': 'content', 'id': 'script_vo'})
        
        # 스크립트 수집 후 'br' 태그를 '\n'으로 변환
        if script: 
            script = script.get_text('\n', strip=True)
            return script


# 수집한 스크립트 저장
def saveScript(script, sub, fname):
    
    # 스크립트를 저장할 폴더 생성
    createFolder(sub)
    path = os.path.dirname(os.path.abspath(__file__)) + r'\%s'%sub + r'\%s.txt'%fname
    
    f = open(path, 'w', encoding='utf-8')
    if script: 
        f.write(script)
        result = True
    else: 
        f.write('Sorry, not available yet.')
        result = False
    f.close()

    return result


# Title Id : 프렌즈 1200 / 왕좌의 게임 1224 / 모던 패밀리 2247 / 셜록 2897 / 빅뱅이론 3229
TitleIDs = [1200, 1224, 2247, 2897, 3229] 

# 스크립트를 저장할 폴더 생성
createFolder('script')

successRate = []
for ID in TitleIDs:
    db = Episode.objects.filter(title=ID).values()
    titleID = db[0]['title_id']

    # 드라마 제목의 특수문자 제거
    title = Title.objects.filter(id=titleID).first().title
    pat = re.compile('\W')
    title = re.sub(pat, '', title)
        
    # 드라마 제목과 같은 이름의 폴더 생성
    sub = 'script' + r'\%s'%title
    createFolder(sub)

    total = 0
    success = 0
    for row in db:
        seasonNum = row['seasonNum']
        epiNum = row['epiNum']
        url = row['link']

        # 시즌 번호 + 에피소드 번호로 파일명 지정
        fname = str(seasonNum).zfill(2) + str(epiNum).zfill(2)
 
        # 스크래이퍼 실행 및 저장
        path = os.path.dirname(os.path.abspath(__file__)) + r'\%s'%sub + r'\%s.txt'%fname
        if not os.path.exists(path):
            script = collectScript(url)
            save = saveScript(script, sub, fname)
            
            if save: 
                success += 1
                print(title, fname, 'Success')
            else: print(title, fname, 'No Script')
            total += 1

    # 스크래이핑 성공률 기록
    successRate.append((title, '%0.2f%%'%(success*100/total)))

# 스크래이핑 종료 후 성공률 출력
for r in successRate: print(*r)