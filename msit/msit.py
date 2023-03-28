from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import re
from urllib.parse import quote
import os

# Set up Selenium webdriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'msit.txt')

# telegram info
f = open('/home/ubuntu/crawling/token.txt', mode='rt', encoding='utf-8')
telegram_bot_token = f.read().splitlines()[0]
#telegram_bot_token = '5895967085:AAFJY2ln43kPMf4EqYV-XM6j8tXoVMuu1yE'
telegram_chat_id = '-1001835326415'

# send telegram message
def send(title,a_tag_number,page):
    if(page==1):
        page=""
    else:
        page=str(page)
    link = "https://www.msit.go.kr/bbs/view.do?sCode=user&mId=129&mPid=224&pageIndex=%s&bbsSeqNo=100&nttSeqNo=%s&searchOpt=ALL&searchTxt=" %(page,a_tag_number)
    escaped_link = quote(link, safe='')
    txt=title+"\n"+escaped_link
    telegram_api_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={txt}'
    response = requests.get(telegram_api_url)

# pagination
def pagination(i):
    button_xpath="//a[@title='%d 페이지로 이동']"%i
    button = driver.find_element(By.XPATH, button_xpath)
    driver.execute_script("arguments[0].click();", button)
    print("page %d"%i)

# get link
def get_link(str):
    link = re.search(r"\d+", str).group()
    return link



def main():
    url = 'https://www.msit.go.kr/bbs/list.do?sCode=user&mPid=224&mId=129'
    driver.get(url)
    time.sleep(5)

    # read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            old_msit = set(f.read().splitlines())
    except FileNotFoundError:
        old_msit = set()

    # open file
    with open(file_path, 'a', encoding='utf-8') as f:
        for i in range(2,4):
            divs = driver.find_elements(By.CSS_SELECTOR, 'div.toggle')
            
            for div in divs:
                # get title
                tit = div.find_element(By.CSS_SELECTOR,'p.title')
                title = tit.get_attribute('innerHTML').strip()

                if title not in old_msit:
                    # get link
                    a_tag = div.find_element(By.CSS_SELECTOR, 'a').get_attribute("onclick")
                    a_tag_number=get_link(a_tag)
                    # write file & send telegram message
                    f.write(title + '\n') 
                    send(title,a_tag_number,i-1)

            # pagination(i)
        print("done")

if __name__ == "__main__":
    main()
