
# 🎮 Tkinter 모듈을 이용한 간단한 게임만들기

**파이썬 프로그래밍 PBL 프로젝트 - 개인**  
> 프로젝트 기간: 2024년 5월 23일 ~ 2024년 6월 18일

---

## 📌 프로젝트 개요

이 프로젝트는 GUI프로그래밍 작성을 위한 tkinter 모듈에 대해 학습하고, 배치관리자, 이벤트처리 등의 </br>
동작과정을 이해하고, tkinter를 이용하여 **간단한 게임을 만들어**보는 것을 목표로 합니다.  

---

## 🛠️ 사용 기술

- Python 3
- tkinter

---

## 🧱 프로젝트 구조

```bash
📁 Python-Game/
├── 결과사진                 # 게임 실행 결과 사진 폴더
├── breakout[test3].py      # 게임 실행 코드
├── README.md               # 프로젝트 설명 파일
└── docs                    # 프로젝트 부록 폴더
    ├── 결과보고서.pdf       # 프로젝트 요약 보고서
    └── 발표자료.pptx        # 팀 프로젝트 발표 자료

```

---

## 🔍 크롤링 내용

이디야 공식 웹사이트([https://ediya.com/contents/drink.html](https://ediya.com/contents/drink.html))에서 다음 정보를 수집했습니다:

- 음료 이름 (`h2` 태그)
- 음료 설명 (`p` 태그)
- 영양 정보 (`div.pro_nutri`)
- 알러지 정보 (`div.pro_allergy`)

---

## 💻 주요 코드 예시

```python
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

def Ediya_menu(result):
    Ediya_url = 'https://ediya.com/contents/drink.html' # 가져올 url 문자열로 입력
    html = urllib.request.urlopen(Ediya_url) # url을 요청하여 응답받은 html이 담긴 자료를 받아와서 저장함.
    soupEdiya = BeautifulSoup(html, 'html.parser') #BeautifulSoup의 객체를 생성함.(html을 잘 정리된 형태로 변환)
    menu_items = soupEdiya.find_all('div', class_='pro_detail') #필요한 항목의 태그와 클래스를 분석하여 파싱한다.

    for menu in menu_items:
        if menu:
            menu_name = menu.find('h2').text.strip() # 음료 메뉴 항목에서 음료 이름에 해당하는 부분 추출
            menu_detail = menu.find('p').text.strip() # 음료 설명에 해당하는 부분 추출
            menu_nutri = menu.find('div', class_='pro_nutri').text.strip()  # 음료 영양분에 해당하는 부분 추출
            menu_allergy = menu.find('div', class_='pro_allergy').text.strip() # 알러지 성분에 해당하는 부분 추출
            result.append([menu_name, menu_detail, menu_nutri, menu_allergy]) # 추출한 결과들을 result에 추가 저장

def main():
    result = [] #추출한 결과들을 저장할 공간 생성
    Ediya_menu(result) #위의 Ediya_menu함수 호출
    Ediya_tbl = pd.DataFrame(result, columns=('name', 'detail', 'nutri', 'allergy')) #추출한 결과를 데이터프레임으로 저장
    Ediya_tbl.to_csv('Ediya_menu.csv', encoding='utf-8-sig', mode='w', index=False) # Ediya_menu.csv파일로 저장

if __name__ == '__main__':
    main()

```

---

## 📊 결과 예시 (CSV)

![image](https://github.com/user-attachments/assets/6aba4dac-4db7-462b-8718-dc316e0efefd)


---

## 💡 활용 방안

- **건강 정보 기반 음료 추천 시스템** 개발 가능성
- **음료 성분 기반 마케팅 전략 수립**
- **웹 크롤링 기술 실습 및 포트폴리오 구성**

---

## 📝 프로젝트를 하고 느낀점

> HTML 구조를 파악하고 웹사이트에서 원하는 데이터를 추출하는 과정이 유익했으며, 실무에서 API 및 데이터 수집에 활용할 수 있다는 점에서 큰 의미가 있었습니다.  

---

## 📎 부록

- 📄 [PBL 결과보고서 PDF](./인공지능과%20데이터과학%20PBL%20결과보고서_인싸조(0613).pdf)
- 📊 [발표 PPT](./인공지능과%20데이터과학%20인싸조%20팀프로젝트%20발표%20PPT.pptx)
