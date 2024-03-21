from pydoc import classname
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tempfile import mkdtemp
import asyncio
import sys
import os

username = os.environ.get('EPARK_USERNAME')
password = os.environ.get('EPARK_PASSWORD')

def handler(event, context):

    platenumber = event['queryStringParameters']['plate']
    email = event['queryStringParameters']['email']

    print(f"Plate number is: {platenumber}")
    print(f"Email is: {email}")

    log(f"Starting up parking automation for {platenumber}")

    driver = initializeWebDriver()
    log("Signing in")
    signin(driver, username, password)

    log("Waiting for login to succeed")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#LicensePlate"))
    )
    log("Filling out plate details")
    elem = driver.find_element(By.ID, "LicensePlate")
    log("Found plate field, sending keys")
    elem.send_keys(platenumber)

    log("Filling out email")
    elem = driver.find_element(By.CSS_SELECTOR, ".form-group__item > input[type='text']")
    log("Found email input, sending keys")
    elem.send_keys(email)

    #inp = input('All done. Press enter to exit!')
    log("Clicking create")
    elem = driver.find_element(By.CSS_SELECTOR, "form div.form-section__main > input[type='button']")
    elem.click()

    log("Closing chrome")
    driver.close()

    return {
      "statusCode": 200,
    }



def signin(driver, username, password):

    driver.get("https://access.e-park.dk/Account/Login")
    assert "Log ind - e-park" in driver.title

    elem = driver.find_element(By.ID, "Email")
    elem.send_keys(username)

    elem = driver.find_element(By.ID, "Password")
    elem.send_keys(password)


    elem = driver.find_element(By.CSS_SELECTOR, "#loginForm input[type='submit']")
    #elem = FindByElementTextContains(driver, "Login")
    elem.click()

def initializeWebDriver():
    
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    
    service = webdriver.ChromeService("/opt/chromedriver")
    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(30)
    driver.start_client
    return driver

def getPrefixArg():
    #this is VERY naive
    return sys.argv[1]

def getDateArg():
    #this is VERY naive
    return sys.argv[2]

def log(message):
    print(message)

if __name__ == "__main__":
    asyncio.run(handler(None, None))