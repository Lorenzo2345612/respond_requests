from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from unittest import TestCase

@fixture
def browser_chrome(context):
    context.driver = webdriver.Chrome()
    context.driver.implicitly_wait(5)
    # context.keys = Keys
    # context.test = TestCase()

    context.url = 'http://localhost:8000'
    # yield context.driver
    # context.driver.quit()

def before_all(context):
    use_fixture(browser_chrome, context)