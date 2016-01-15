import os
from unittest import TestCase
import unittest
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()

from django.core.urlresolvers import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys





# run ($ in this directory)
# PYTHONPATH=.. python test-view.py


url = 'http://127.0.0.1:8000'
user = 'test_blue'
password = 'myname is jonh'
start = True

class TestSignIn(TestCase):
    driver = None
    
    @classmethod
    def setUpClass(cls):
        TestSignIn.driver = webdriver.Firefox()
    
    @classmethod
    def tearDownClass(cls):
        TestSignIn.driver.close()

    def test_sigin_expected_user_already_created(self):
        TestSignIn.driver.get(url + reverse('agenda:sign'))
        name = TestSignIn.driver.find_element_by_name('name')
        name.send_keys(user)
        
        _password = TestSignIn.driver.find_element_by_name('password')
        _password.send_keys(password)
        
        send = TestSignIn.driver.find_element_by_xpath(
            '//input[@type="submit"]')
        send.click()
        
        self.assertIn('this name already exist, choice another',
            TestSignIn.driver.page_source)
    
    def test_sigin_from_fail(self):
        TestSignIn.driver.get(url + reverse('agenda:sign'))
        name = TestSignIn.driver.find_element_by_name('name')
        name.send_keys(user)
        
        _password = TestSignIn.driver.find_element_by_name('password')
        
        
        send = TestSignIn.driver.find_element_by_xpath(
            '//input[@type="submit"]')
        send.click()
        
        self.assertIn(':( Form invalid', TestSignIn.driver.page_source)
    

class TestLogin(TestCase):
    driver = None
    
    @classmethod
    def setUpClass(cls):
        TestLogin.driver = webdriver.Firefox()
    
    @classmethod
    def tearDownClass(cls):
        TestLogin.driver.close()
    
    def test_login_user_expected_fail(self):
        TestLogin.driver.get(url + reverse('agenda:login'))
        name = TestLogin.driver.find_element_by_name('name')
        name.send_keys('user_no_exist')
        
        _password = TestLogin.driver.find_element_by_name('password')
        _password.send_keys(password)
        
        send = TestLogin.driver.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        self.assertIn('User or password invalid', TestLogin.driver.page_source)


if __name__ == '__main__':
    unittest.main()


