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

logger = logging.getLogger()
logger.setLevel(20)
if len(sys.argv) > 1 and sys.argv[1] == '-v':
    print('Verbose mode enabled')
    verbose = True

file_log_handler = logging.FileHandler('approved_members.log')
stdout_log_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(file_log_handler)
logger.addHandler(stdout_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
file_log_handler.setFormatter(formatter)
stdout_log_handler.setFormatter(formatter)

load_dotenv()
username = os.getenv('username')
password = os.getenv('password')

options = ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

def accept_members(table):
    # Retrieve prospective members
    members = table.find_elements(By.TAG_NAME, 'tr')
    for member in members:
        # Click 'APPROVE' button
        try:
            name = member.find_element(By.XPATH, 'td[2]/span[1]').text
            member.find_element(By.XPATH, 'td[4]/button[1]').click()
            logger.info(f'Approved "{name}"')
            time.sleep(5)
        except:
            if verbose: logger.info('No requests, skipping...')
            break


def login():
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="prospective"]/div/table/tbody')))
        return True
    except:
        try:
            # Initial login process
            driver.get('https://asu.campuslabs.com/engage/actioncenter/organization/soda/roster/Roster/prospective')
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(username)
            driver.find_element(By.ID, 'password').send_keys(password)
            driver.find_element(By.NAME, 'submit').click()

            # Duo 2FA
            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@id="duo_iframe"]')))
            # Assume making it this far means successful log in
            
            # Enable "Remember me for 7 days" checkbox
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div[2]/div/label/input'))).click()
            
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Send Me a Push"]'))).click()
            logger.info(f'Logged in as {username}, sending Duo 2FA push...')
            return True
        except:
            return False

def main():
    if login():
        try:
            table: WebElement = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="prospective"]/div/table/tbody')))
            logger.info('Duo 2FA push accepted, proceeding to Engage')
            while True:
                accept_members(table)
                time.sleep(60)
                if verbose: logger.info(f'Refreshing...')
                driver.refresh()
                table = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="prospective"]/div/table/tbody')))
        except Exception as e:
            print(e)
            logger.error(f'Crashed...')
            main()
    else:
        main()

if __name__ == "__main__":
    main()
    # driver.quit()