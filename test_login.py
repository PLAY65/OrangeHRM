import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import allure

@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield
    driver.quit()

@allure.description("Validated OrangeHRM with valid login credentials")
@allure.severity(severity_level="CRITICAL")
def test_validLogin(test_setup):
    driver.get("https://www.orangehrm.com/")
    enter_email("email@gmail.com")

    driver.find_element(By.ID,"Form_getForm_action_submitForm").click()

    assert "orangehrm-30-day-trial" in driver.current_url

@allure.description("Validated OrangeHRM with invalid login credentials")
@allure.severity(severity_level="NORMAL")
def test_invalidLogin(test_setup):
    driver.get("https://www.orangehrm.com/")
    enter_email("emailgmail.com")
    driver.find_element(By.ID, "Form_getForm_action_submitForm").click()
    try:
        assert "orangehrm-30-day-trial" in driver.current_url
    finally:
        if(AssertionError):
            allure.attach(driver.get_screenshot_as_png(),
                          name="Invalid Credentials",
                          attachment_type=allure.attachment_type.PNG)

@allure.step("Entering user email as {0}")
def enter_email(email):
    driver.find_element(By.ID, "Form_getForm_Email").send_keys(email)

# def test_teardown():
#     driver.quit()
