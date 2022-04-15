from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import requests
import os

def set_selenium():
    #selenium
    # user_profile = (r'C:\Users\Panasonic\Desktop\Python\money forward\userdata')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('–profile-directory=' + user_profile)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--disable-dev-shm-usage")
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    options.add_argument("--user-agent=" + UA)
    driver = webdriver.Chrome(r'/app/.chromedriver/bin/chromedriver', options=options)
    # driver =  webdriver.Chrome(r'C:\Users\Panasonic\Desktop\Python\money forward\driver\chromedriver.exe', options=options)


def line_notify(message:str):
	line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
	line_notify_api = 'https://notify-api.line.me/api/notify'
	payload = {'message': message}
	headers = {'Authorization': 'Bearer ' + line_notify_token}
	requests.post(line_notify_api, data=payload, headers=headers)

def move_to_search_resault(bookname:str,writer:str):
    # 資料検索に移動
    driver.get('https://www.lib.nerima.tokyo.jp/opw/OPW/OPWSRCH2.CSP')
    bookname_txt_box = driver.find_element(by=By.ID, value='text1')
    writer_txt_box = driver.find_element(by=By.ID, value='text3')
    search_btn = driver.find_element(by=By.NAME, value='srchbtn2')
    #結果画面に遷移
    writer_txt_box.send_keys(writer)
    search_btn.click()


def judge_book_existence(bookname:str):
    #結果画面で本の名前を検索
    try:
        #本が存在する時
        book = driver.find_element(by=By.LINK_TEXT, value=bookname)
        print('本が所蔵されています')
        line_notify(f'「{bookname}」が所蔵されています')
    except:
        print('本はまだ所蔵されていません')

def run_every_three_hours() -> bool: 
    dt_now = datetime.now()
    hour = int(dt_now.strftime('%H'))
    print(f'今{hour}時です')
    if hour % 3 == 0:
        return False
    else:
        return True

if run_every_three_hours():
    print('この時間には実行しません')
    exit()

set_selenium()
move_to_search_resault('激変','上田晋也')
judge_book_existence('激変')


driver.close()
driver.quit()
exit()