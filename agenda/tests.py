from django.test import TestCase
from django.core.urlresolvers import reverse

from . import utils

# rodar
# python manage.py test agenda

class Test_home_page(TestCase):
    
    def test_home_with_no_user_loged(self):
        """
        If an user is not loged a message 'Ola forasterio' is shown
        """
        response = self.client.get(reverse('agenda:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ola forasteiro');
    
    def test_home_send_a_query_string(self):
        """
        If a query string msg is send in home it is shown
        """
        response = self.client.get(reverse('agenda:home') + '?msg=test work')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test work')
    
    def test_with_authenticated_user_simple_pages(self):
        """
        If the user is authenticated is redirect to the main page 
        get his name on title and have no contacts
        """
        user_name = 'pedro'
        password = '987654321'
        utils.create_user(user_name, password)
        self.assertTrue(
            self.client.login(username=user_name, password=password)
          , True
        )
        response = self.client.get(reverse('agenda:home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>' + user_name + '</title>')
        # the title is on context but the comparation with pedro is weird
        # the assertQuerysetEqual works fine for complex objects on context
        self.assertQuerysetEqual(
            response.context['contacts_phones_lst'], []
        )
    
    def test_with_authenticated_user_wiht_contacts(self):
        """
        If an user have a contact it is shown
        """
        user_name = 'pedro'
        password = '987654321'
        user = utils.create_user(user_name, password)
        assert(utils.create_contact(user, 'a1') != None)
        self.assertTrue(
            self.client.login(username=user_name, password=password)
          , True
        )
        response = self.client.get(reverse('agenda:main'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(user.contact_set.all()), 1)
        self.assertContains(response, 'Contact')
        # response.context['contacts_phones_lst']
        # I can't use contacts_phones_lst because it was yeld firt on templte
        # iterate over it now gave nothing
        
        self.assertQuerysetEqual(
            response.context['contacts_lst']
          , ['<Contact: a1>']
        )
        
        # create more two contacts
        utils.create_contact(user, 'a2')
        utils.create_contact(user, 'a3')
        
        response = self.client.get(reverse('agenda:main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contacts')
        self.assertQuerysetEqual(
            response.context['contacts_lst']
          , ['<Contact: a1>', '<Contact: a2>', '<Contact: a3>']
          , ordered=False
        )
        
