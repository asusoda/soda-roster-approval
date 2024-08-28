import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from dotenv import load_dotenv
import os
import logging
import sys
from getpass import getpass

from urllib.parse import unquote

load_dotenv()

logger = logging.getLogger('engage-roster-approver')
logger.setLevel(10)
file_log_handler = logging.FileHandler('approved_members.log')
file_log_handler.setLevel(20)
stdout_log_handler = logging.StreamHandler(sys.stdout)
# if len(sys.argv) > 1 and sys.argv[1] == '-v':
print('Verbose mode enabled')
stdout_log_handler.setLevel(10)
# else:
    # stdout_log_handler.setLevel(20)
logger.addHandler(file_log_handler)
logger.addHandler(stdout_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
file_log_handler.setFormatter(formatter)
stdout_log_handler.setFormatter(formatter)

options = ChromeOptions()
options.arguments.extend([
    '--headless=new',
    f'--user-data-dir={os.getcwd()}/userdata'
])
driver = webdriver.Chrome(options=options)

def accept_member(member: WebElement):
    # Click 'APPROVE' button
    name = member.find_element(By.XPATH, 'td[2]').text
    button: WebElement = member.find_element(By.XPATH, 'td[4]/button[1]')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(button))
    button.click()
    logger.info(f'Approved "{name}"')
    time.sleep(3)

username = os.getenv('username')
if username is None:
    username = input('Username: ')
password = os.getenv('password')
if password is None:
    password = getpass('Password: ')
prospective_url = os.getenv('prospective_url')
if prospective_url is None:
    prospective_url = input('Prospective URL: ')

def login():
    try:
        driver.get(prospective_url)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="prospective"]/div/table/tbody')))
        name = unquote(driver.execute_script('return SVG.CurrentMember.Name'))
        logger.info(f'Already logged in as {name}, skipping login process...')
        return True
    except:
        try:
            try:
                # Initial login process
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'username'))).send_keys(username)
                driver.find_element(By.ID, 'password').send_keys(password)
                driver.find_element(By.NAME, 'submit').click()
            finally:
                # # Duo 2FA
                # WebDriverWait(driver, 20).until(
                #     EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@id="duo_iframe"]')))
                
                # # Enable "Remember me for 7 days" checkbox
                # WebDriverWait(driver, 20).until(
                #     EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div[2]/div/label/input'))).click()
                
                logger.info(f'Logged in as {username}, sending Duo 2FA push...')
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="trust-browser-button"]'))).click()
                return True
        except:
            logger.info(f'Failed log in, retrying...')
            with open('check.html', 'w') as file:
                file.write(driver.page_source)
            return False

def main():
    if login():
        try:
            table: WebElement = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="prospective"]/div/table/tbody')))
            logger.info('Authenticated, proceeding to Engage')
            while True:
                try:
                    # Retrieve a prospective member
                    member = table.find_element(By.TAG_NAME, 'tr')
                    accept_member(member)
                except:
                    logger.debug('No requests, skipping...')
                    time.sleep(60)
                    logger.debug(f'Refreshing...')
                    driver.refresh()
                table = WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="prospective"]/div/table/tbody')))
        except Exception as e:
            print(type(e))
            logger.error(f'Crashed...')
    main()

if __name__ == "__main__":
    try:
        main()
    except:
        pass
    driver.quit()