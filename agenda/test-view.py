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
# $ PYTHONPATH=.. python test-view.py


url = 'http://127.0.0.1:8000'
user = 'test_blue'
password = 'myname is jonh'
# If you change the user name set the 'start' to False
start = True
gb = None

class Browser:
    def __init__(self):
        self.driver = None
    
    def __enter__(self):
        self.driver = webdriver.Firefox()
    
    def __exit__(self, ex_type, ex_val, tb):
        self.driver.close()
        
        # propagate the exeception if it happen
        return ex_type is not None

# assume all the pages are in the rigth place
def login_user(obj):
    
    name = obj.driver.find_element_by_name('name')
    name.send_keys(user)
    
    _password = obj.driver.find_element_by_name('password')
    _password.send_keys(password)
    
    send = obj.driver.find_element_by_xpath('//input[@type="submit"]')
    send.click()
    
    return True

def add_contact(obj, _name, _phone):
    name = obj.driver.find_element_by_name('name')
    name.send_keys(_name)
    
    phone = obj.driver.find_element_by_name('phone')
    phone.send_keys(_phone)
    
    send = obj.driver.find_element_by_xpath('//input[@type="submit"]')
    send.click()
    
    return True


class TestSignIn(TestCase):
    
    def test_sigin_expected_user_already_created(self):
        gb.driver.get(url + reverse('agenda:sign'))
        name = gb.driver.find_element_by_name('name')
        name.send_keys(user)
        
        _password = gb.driver.find_element_by_name('password')
        _password.send_keys(password)
        
        send = gb.driver.find_element_by_xpath(
            '//input[@type="submit"]')
        send.click()
        
        self.assertIn('this name already exist, choice another',
            gb.driver.page_source)
    
    def test_sigin_from_fail(self):
        gb.driver.get(url + reverse('agenda:sign'))
        name = gb.driver.find_element_by_name('name')
        name.send_keys(user)
        
        _password = gb.driver.find_element_by_name('password')
        
        
        send = gb.driver.find_element_by_xpath(
            '//input[@type="submit"]')
        send.click()
        
        self.assertIn(':( Form invalid', gb.driver.page_source)
    

class TestLogin(TestCase):
    
    def test_login_user_expected_fail(self):
        gb.driver.get(url + reverse('agenda:login'))
        name = gb.driver.find_element_by_name('name')
        name.send_keys('user_no_exist')
        
        _password = gb.driver.find_element_by_name('password')
        _password.send_keys(password)
        
        send = gb.driver.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        self.assertIn('User or password invalid', gb.driver.page_source)

    @unittest.skipIf(start, "One contact was added")
    def test_login_sucess(self):
        gb.driver.get(url + reverse('agenda:login'))
        self.assertTrue(login_user(gb))
        
        contacts_lst = gb.driver.find_elements_by_xpath('//ul//li')
        self.assertEqual(0, len(contacts_lst))
    
    @unittest.skipIf(start, "This contact already was added")
    def test_add_one_contact(self):
        """
        Goes to add_contact page clicking
        """
        
        gb.driver.get(url + reverse('agenda:login'))
        assert login_user(gb)
        _contact = gb.driver.find_element_by_xpath(
            '//a[@href="{}"]'.format(reverse('agenda:acontact')))
        _contact.click()# now I am in the add_contact page
        
        name = gb.driver.find_element_by_name('name')
        name.send_keys('c name 1')
        phone = gb.driver.find_element_by_name('phone')
        phone.send_keys('8883-3883')
        send = gb.driver.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        # now the contacts in list main page should have 1 (was redirected)
        contacts_lst = gb.driver.find_elements_by_xpath('//ul//li')
        self.assertEqual(1, len(contacts_lst))
    
    @unittest.skipIf(start, "This two contanct was added")
    def test_add_two_contacts(self):
        """
        One contact already exist
        """
        gb.driver.get(url + reverse('agenda:login'))
        assert login_user(gb)
        
        # I am in the home page
        contacts_lst = gb.driver.find_elements_by_xpath('//ul//li')
        self.assertEqual(1, len(contacts_lst))
        
        # now that I am loged I can go direct to add_contact page
        gb.driver.get(url + reverse('agenda:acontact'))
        
        
        assert add_contact(gb, 'contact test bs', '9383-9832')
        
        # after add a contact The user is redirected to home page
        # so I need to go back to add_contact page
        gb.driver.get(url + reverse('agenda:acontact'))
        assert add_contact(gb, 'contact test aj', '8347-3264')
        
        contacts_lst = gb.driver.find_elements_by_xpath('//ul//li')
        self.assertEqual(3, len(contacts_lst))

class TestPhone(TestCase):
    def test_update_with_invalid_phone(self):
        """
        send invalid number, expected error
        """
        
        # click flow
        # (home) select user > select edit a phone > update the form
        # select send button
        gb.driver.get(url + reverse('agenda:login'))
        assert login_user(gb)
        
        # use the first one 'c name 1'
        link = gb.driver.find_element_by_link_text('c name 1')
        link.click()
        # takes the sencond link
        link_edit = gb.driver.find_elements_by_link_text('edit')[1]
        link_edit.click()
        form = gb.driver.find_element_by_xpath(
            '//input[@id="id_phone"]'
        )
        form.send_keys('888-3883')
        
        submit = gb.driver.find_element_by_xpath(
            '//input[@type="submit"]'
        ).click()
        
        self.assertIn('is not a valid number', gb.driver.page_source)

if __name__ == '__main__':
    gb = Browser()
    with gb:
        unittest.main()
