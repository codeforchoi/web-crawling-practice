# import os, urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.wait import WebDriverWait
# import requests
from bs4 import BeautifulSoup
import openpyxl

# service = Service(executable_path=r'/content/drive/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)
URL = 'https://kto.visitkorea.or.kr/kor/ktom/menupan/menupan/menuName_search.kto'

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["한국어", "Roman", "English", "日本語"])
# sheet.append(["한국어", "Roman", "English", "日本語", "中文(简体)", "中文（繁體)"])   # 중국어는 메뉴명에 문자 오류로 크롤링 불가

css_selector = "div.table_list table tbody tr"

for idx in range(292):
    next = 0
    browser.get(URL)   
    while next < idx:
        browser.find_element(By.CLASS_NAME, 'next').click()
        browser.implicitly_wait(200)
        next += 1

    if next == 291:
        for i in range(9): 
            number = str((next * 10) + i + 1)
            if i != 0:
                browser_button = browser.find_element(By.LINK_TEXT, number)
                browser_button.click()
                browser.implicitly_wait(200)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            container = soup.select(css_selector)
            for con in container:
                korean = con.select("td")[0].text.strip()
                roman = con.select("td")[1].text.strip()
                english = con.select("td")[2].text.strip()
                japanese = con.select("td")[3].text.strip()
                # chinese1 = con.select("td")[4].text.strip()
                # chinese2 = con.select("td")[5].text.strip()

                # sheet 내 각 행에 데이터 추가
                sheet.append([korean, roman, english, japanese])
                # sheet.append([korean, roman, english, japanese, chinese1, chinese2])
    else:
        for i in range(10): 
            number = str((next * 10) + i + 1)
            if i != 0:
                browser_button = browser.find_element(By.LINK_TEXT, number)
                browser_button.click()
                browser.implicitly_wait(200)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            container = soup.select(css_selector)
            for con in container:
                korean = con.select("td")[0].text.strip()
                roman = con.select("td")[1].text.strip()
                english = con.select("td")[2].text.strip()
                japanese = con.select("td")[3].text.strip()
                # chinese1 = con.select("td")[4].text.strip()
                # chinese2 = con.select("td")[5].text.strip()

                # sheet 내 각 행에 데이터 추가
                sheet.append([korean, roman, english, japanese])
                # sheet.append([korean, roman, english, japanese, chinese1, chinese2])
  
wb.save("translate_data.xlsx")

print("데이터 수집 완료")
