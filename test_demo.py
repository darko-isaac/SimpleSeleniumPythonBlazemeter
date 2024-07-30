import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

@pytest.fixture(scope="module")
def driver():
    browser = os.environ.get('BROWSER', 'chrome').lower()  # 'chrome' by default
    if os.environ.get('IS_LOCAL') == 'True':
        if browser == 'chrome':
            driver = webdriver.Firefox()
        elif browser == 'firefox':
            driver = webdriver.Firefox()
        else:
            raise ValueError(f"Browser '{browser}' is not supported locally.")
    else:
        api_key = "c3756f607bc070c5a2ef3b64"
        api_secret = "40a7cce5ccbda67f9d54aafb8307242670588029c5bf779eead7a774ed6b535af0052625"
        base = "a.blazemeter.com"
        blazegrid_url = f'https://{api_key}:{api_secret}@{base}/api/v4/grid/wd/hub'

        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.set_capability('blazemeter.reportName', 'Demo report')
            driver = webdriver.Remote(command_executor=blazegrid_url, options=options)
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            options.set_capability('blazemeter.reportName', 'Demo report')
            driver = webdriver.Remote(command_executor=blazegrid_url, options=options)
        else:
            raise ValueError(f"Browser '{browser}' is not supported on BlazeMeter.")

    yield driver
    driver.quit()

def get_element(driver, by_locator):
    return WebDriverWait(driver, 20).until(EC.visibility_of_element_located(by_locator))

@pytest.fixture(scope="function", autouse=True)
def name_blazemeter_report(request, driver):
    args = {
        "testCaseName": 'test case demo',
        "testSuiteName": 'test suite demo'
    }
    driver.execute_script("/* start report */", args)
    yield
    status = 'passed' if request.node.session.testsfailed == 0 else 'failed'
    args = {
        "status": status,
        "message": f'test demo has {status}'
    }
    driver.execute_script("/* end report */", args)

def test_verify_title(driver):
    driver.get("http://dbankdemo.com/bank/login")
    driver.implicitly_wait(10)
    assert "Digital Bank" == driver.title
@allure.step("login")
def test_login(driver):
    get_element(driver, (By.ID, "username")).send_keys("jsmith@demo.io")
    get_element(driver, (By.ID, "password")).send_keys("Demo123!")
    driver.find_element(By.ID, "submit").click()
    assert "home" in driver.current_url
@allure.step("label validar")
def test_verify_label(driver):
    get_element(driver, (By.ID, 'checking-menu')).click()
    sleep(2)
    assert 'Checking' in get_element(driver, (By.ID, 'checking-menu')).text
@allure.step("label 2 validar")
def test_verify_label2(driver):
    driver.find_element(By.ID, 'checking-menu').click()
    sleep(2)
    assert 'Checking' in driver.find_element(By.ID, 'checking-menu').text
