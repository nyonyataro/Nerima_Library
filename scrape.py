from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os

def line_notify(message:str):
	line_notify_token = 'g46tCIWBKHPAMYd1cik1qipMnfmZGpaVZDDlO0Sc75V'
	line_notify_api = 'https://notify-api.line.me/api/notify'
	payload = {'message': message}
	headers = {'Authorization': 'Bearer ' + line_notify_token}
	requests.post(line_notify_api, data=payload, headers=headers)


def run_every_three_hours() -> bool: 
    dt_now = datetime.now()
    hour = int(dt_now.strftime('%H'))
    print(f'今{hour}時です')
    if hour % 3 == 0:
        return False
    else:
        return True

def check_existence(bookname:str):
    #図書館トップページを取得
    s = requests.Session()
    r = s.get('https://www.lib.nerima.tokyo.jp/index.html')
    cookie = r.cookies
    soup = BeautifulSoup(r.text, 'html.parser')

    #ログインに必要な情報を取得
    # form_tag = ['DB','PID2','FLG','MODE','SORT','opr(1)','qual(1)']
    # form_tag = ['opr(1)','qual(1)']
    form_data = {}
    # for tag in form_tag:
    #     form_data[tag] = soup.find({'name':tag}).get('value')
    form_data['text(1)'] = bookname
    form_data['opr(1)'] = 'OR'
    form_data['qual(1)'] = 'ALL'

    #検索
    form_url = 'https://www.lib.nerima.tokyo.jp/opw/OPS/OPSSRCHLIST.CSP'
    r = s.post(form_url, data=form_data, cookies=cookie)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        name = soup.find('font', attrs={'class':'listttl'}).text
        result = f'「{name}」が所蔵されています'
    except Exception as e:
        result = 'お探しの本はまだ所蔵されていません'
    s.close()

    print(result)
    return result

if __name__ == '__main__':
    check_existence('52ヘルツ')
    exit()