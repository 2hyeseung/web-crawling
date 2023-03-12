# telegram_bot_token = '5895967085:AAFJY2ln43kPMf4EqYV-XM6j8tXoVMuu1yE'
# telegram_chat_id = '6173488270'

# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

# Set up Selenium webdriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Initialize previous li tag id
previous_li_id = None

while True:
    # Navigate to the URL
    url = 'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do'
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Find the li tag with class "notice"
    notice_li = driver.find_element(By.CSS_SELECTOR, 'li.notice')

    # Get the id of the current li tag
    current_li_id = notice_li.get_attribute('id')

    # Compare current li tag id with previous li tag id
    if current_li_id != previous_li_id:
        # Find all p tags with class "tit" within the li tag
        tit_ps = notice_li.find_elements(By.CSS_SELECTOR, 'p.tit')

        # Get the innerHTML of each p tag and join them with a newline character
        notice_text = '\n'.join([tit.get_attribute('innerHTML') for tit in tit_ps])

        # Send the innerHTML to Telegram
        telegram_bot_token = '5895967085:AAFJY2ln43kPMf4EqYV-XM6j8tXoVMuu1yE'
        telegram_chat_id = '6173488270'
        telegram_message = f'The notice is:\n{notice_text}'

        telegram_api_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={telegram_message}'
        response = requests.get(telegram_api_url)

        # Update previous li tag id
        previous_li_id = current_li_id

    # Wait for 1 minute before checking again
    time.sleep(60)

# Quit the driver
driver.quit()

