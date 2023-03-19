from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

# Set up Selenium webdriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# telegram info
telegram_bot_token = '5895967085:AAFJY2ln43kPMf4EqYV-XM6j8tXoVMuu1yE'
telegram_chat_id = '6173488270'

# send telegram message
def send(txt):
    telegram_api_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={txt}'
    response = requests.get(telegram_api_url)

def main():
    url = 'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do'
    driver.get(url)
    time.sleep(5)

    # read file
    try:
        with open('k-startup.txt', 'r') as f:
            old_kstartup = set(f.read().splitlines())
    except FileNotFoundError:
        old_kstartup = set()

    # Find the li tag with class "notice"
    with open('k-startup.txt', 'a') as f:
        while True:

            for i in range(1,5):
                # 페이지 이동해야하는데 잘 안됨 ..
                lis = driver.find_elements(By.CSS_SELECTOR, 'li.notice')
                for li in lis:
                    notice_tit = li.find_element(By.CSS_SELECTOR, 'p.tit')
                    txt = notice_tit.get_attribute('innerHTML')
                    if txt not in old_kstartup:
                        f.write(txt + '\n') 
                        send(txt)
                        old_kstartup.add(txt)

                # check if there's a "next page" button and click it
                # try:
                #     next_page_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.nextAll.page_btn.last')
                #     driver.execute_script("arguments[0].click();", next_page_button)
                # except:
                #     break 

                time.sleep(5)

if __name__ == "__main__":
    main()
