from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

# Set up Selenium webdriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# telegram info
f = open('/home/ubuntu/crawling/token.txt', mode='rt', encoding='utf-8')
telegram_bot_token = f.read().splitlines()[0]
# telegram_bot_token = '5895967085:AAFJY2ln43kPMf4EqYV-XM6j8tXoVMuu1yE'
telegram_chat_id = '-1001835326415'

# send telegram message
def send(title,number,page):
    link = "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=view%%26pbancSn=%d%%26page=%i%%26schStr=regist%%26pbancEndYn=N" % (number, page)
    txt=title+'\n'+link
    telegram_api_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={txt}'
    response = requests.get(telegram_api_url)

# pagination
def pagination(i):
    button_xpath="//a[@title='%d 페이지로 이동']"%i
    button = driver.find_element(By.XPATH, button_xpath)
    driver.execute_script("arguments[0].click();", button)
    print("page %d"%i)



def main():
    url = 'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do'
    driver.get(url)
    time.sleep(5)

    # read file
    try:
        with open('k-startup.txt', 'r', encoding='utf-8') as f:
            old_kstartup = set(f.read().splitlines())
    except FileNotFoundError:
        old_kstartup = set()

    # open file
    with open('k-startup.txt', 'a', encoding='utf-8') as f:
        
        for i in range(2,5):
            lis = driver.find_elements(By.CSS_SELECTOR, 'li.notice')

            for li in lis:
                # get title
                notice_tit = li.find_element(By.CSS_SELECTOR, 'p.tit')
                title = notice_tit.get_attribute('innerHTML')

                if title not in old_kstartup:
                    # get link
                    notice_a_tag = li.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
                    notice_number = int(notice_a_tag.split("(")[1].split(")")[0])
                    # write file & send telegram message
                    f.write(title + '\n') 
                    send(title,notice_number,i-1)

            pagination(i)
            time.sleep(5)

        print("done")

if __name__ == "__main__":
    main()
