## Scraper

- 드라마 스크립트 사이트(https://www.hypnoweb.net/)의 영문 스크립트를 스크래이핑.
- 드라마 타이틀 > 시즌 및 에피소드 > 스크립트 순으로 링크를 타고 이동해야 함.
 

### scrape_title.py

- 스크래이핑 1단계, 드라마 타이틀 링크 수집.
- [드라마 id, 타이틀, 드라마 링크]의 형태로 스크래이핑 후 Django models.Title과 연결.


### scrape_episode.py

- 스크래이핑 2단계, 드라마 타이틀 별 전체 시즌 및 에피소드 링크 수집.
- [드라마 id, 에피소드 id, 시즌 번호, 에피소드 번호, 에피소드 명, 에피소드 링크]의 형태로 스크래이핑 후 Django models.Episode와 연결.
- 드라마 id를 Foreign key로 설정, Title과 Episode를 연결.


### scrape_script.py

- 스크래이핑 3단계, 각 드라마 에피소드 별 영문 스크립트 수집.
- Script > 각 드라마 타이틀의 구조로 폴더를 생성하고 각 폴더에 txt 형태로 스크립트 저장.
- (시즌번호 + 에피소드 번호).txt 형태로 파일명 지정. e.g) S01, Ep12 > 0112.txt


### Update

- 2021.05.10. : 스크래이퍼 완성 및 테스트 완료.


### Todo

- 스크립트의 적절한 위치에 빈 칸을 생성하는 Puncher 완성.