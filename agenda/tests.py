from django.test import TestCase
from django.core.urlresolvers import reverse

from . import utils
from . import forms

# run
# python manage.py test agenda

# TODO

class TestContactPhone(TestCase):
    
    def test_integration(self):
        """
        Each contact gets his own phone
        """
        env = utils.BasicEnvironment(self.client.login)
        contact1 = utils.create_contact(env.user, 'auido')
        contact2 = utils.create_contact(env.user, 'dam')
        contact3 = utils.create_contact(env.user, 'linus')
        
        contact1.phone_set.create(number='9832-3384')
        contact2.phone_set.create(number='8478-4383')
        
        response = self.client.get(reverse('agenda:main'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['contacts_lst']
          , ['<Contact: auido>', '<Contact: dam>', '<Contact: linus>']
        )
        self.assertQuerysetEqual(
            response.context['phones_lst']
          , ['<Phone: 9832-3384>', '<Phone: 8478-4383>', "'#'"]
        )


class TestAddContact(TestCase):
    
    def test_with_no_contact(self):
        """
        With no contact the 'contacts_lst' should be empty
        """
        env = utils.BasicEnvironment(self.client.login)
        
        response = self.client.get(reverse('agenda:main'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact')
        self.assertQuerysetEqual(response.context['contacts_lst'], [])
    
    def test_with_two_contacts(self):
        """
        If a contact is added is in shown on main page
        """
        env = utils.BasicEnvironment(self.client.login)
        contact1 = utils.create_contact(env.user, 'lion')
        contact2 = utils.create_contact(env.user, 'elephant')
        
        response = self.client.get(reverse('agenda:main'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contacts')
        self.assertQuerysetEqual(
            response.context['contacts_lst']
          , ['<Contact: elephant>', '<Contact: lion>']
        )
        
class TestDeleteContact(TestCase):
    
    def test_remove_one_of_three_contacts(self):
        """
        If a contact is deleted it is not shown
        """
        env = utils.BasicEnvironment(self.client.login)
        contact1 = utils.create_contact(env.user, 'blue')
        contact2 = utils.create_contact(env.user, 'pink')
        contact3 = utils.create_contact(env.user, 'green')
        
        # after deletion the user is redirect to main page
        response = self.client.get(
            reverse('agenda:confdeluser', args=(contact2.id, ))
          , follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['contacts_lst']
          , ['<Contact: blue>', '<Contact: green>']
        )

class TestEditContact(TestCase):
    
    def test_edit_a_contact(self):
        """
        If contact's name change the name on context change too
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'alex')
        
        response = self.client.get(reverse('agenda:main'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['contacts_lst'], ['<Contact: alex>']
        )
        
        contact.name = 'dennis'
        contact.save()
        
        response = self.client.get(reverse('agenda:main'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['contacts_lst'], ['<Contact: dennis>']
        )

class TestAddPhone(TestCase):
    
    def test_with_no_phone(self):
        """
        If there is no phone the 'phones_lst' should be empty
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'aj')
        
        response = self.client.get(
            reverse('agenda:detail', args=(contact.id, ))
          , follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['phones_lst'], []
        )
    
    def test_add_a_phone(self):
        """
        If a phone is added to a contact it is shown
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'a1')
        contact.phone_set.create(number='9828-9382')
        
        response = self.client.get(
            reverse('agenda:detail', args=(contact.id, ))
          , follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'a1')
        self.assertQuerysetEqual(
            response.context['phones_lst']
          , ['<Phone: 9828-9382>']
        )
        
    
    def test_add_three_phones(self):
        """
        If three phones are added to a contact they are shown
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'buy')
        
        contact.phone_set.create(number='9374-3492')
        contact.phone_set.create(number='3847-3948')
        contact.phone_set.create(number='3878-40593')
        
        response = self.client.get(
            reverse('agenda:detail', args=(contact.id, )), follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'buy')
        self.assertQuerysetEqual(
            response.context['phones_lst']
          , [   '<Phone: 9374-3492>'
               , '<Phone: 3847-3948>'
               , '<Phone: 3878-40593>'
            ]
          , ordered=False
        )

class TestDeltePhone(TestCase):
    
    def test_remove_all_phones(self):
        """
        If all contact's phones are deleted 'phones_lst' should be empty
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'pencil')
        
        p1 = contact.phone_set.create(number='9374-3492')
        p2 = contact.phone_set.create(number='3847-3948')
        p3 = contact.phone_set.create(number='3878-40593')
        
        response = self.client.get(
            reverse('agenda:dphone', args=(p1.id,)), follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(
            reverse('agenda:dphone', args=(p2.id, )), follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(
            reverse('agenda:dphone', args=(p3.id, )), follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertQuerysetEqual(response.context['phones_lst'], [])
    
    def test_remove_a_phone_that_no_exist(self):
        """
        If try to delete a phone that does not exist 404 is raised
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'mouse')
        
        response = self.client.get(
            reverse('agenda:dphone', args=(1, )), follow=True
        )
        
        self.assertEqual(response.status_code, 404)

class TestEditPhone(TestCase):
    
    def test_edit_phone(self):
        """
        If a phone number change the value on 'phones_lst' change too
        """
        env = utils.BasicEnvironment(self.client.login)
        contact = utils.create_contact(env.user, 'pencil')
        
        p1 = contact.phone_set.create(number='9374-3492')
        p2 = contact.phone_set.create(number='3847-3948')
        p3 = contact.phone_set.create(number='3878-40593')
        
        p3.number = '90902-9090'
        p3.save()
        
        response = self.client.get(
            reverse('agenda:detail', args=(contact.id, )), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['phones_lst']
          , [    '<Phone: 9374-3492>'
               , '<Phone: 3847-3948>'
               , '<Phone: 90902-9090>'
            ]
          , ordered=False
        )

class TestHomePage(TestCase):
    
    def test_home_with_no_user_loged(self):
        """
        If an user is not loged a message 'Ola forasterio' is shown it stay
        in agenda:home
        """
        response = self.client.get(reverse('agenda:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ola forasteiro')
        self.assertContains(response, "/agenda/login")
        self.assertContains(response, "/agenda/sign")
    
    def test_home_send_a_query_string(self):
        """
        If a query string msg is send in home it is shown
        """
        response = self.client.get(reverse('agenda:home') + '?msg=test work')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test work')
    
    def test_with_authenticated_user_simple_page(self):
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
        self.assertTrue(
            self.client.login(username=user_name, password=password)
          , True
        )
        utils.create_contact(user, 'a1')
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

class TestPhoneForm(TestCase):
    
    def test_with_valid_numbers(self):
        """
        A Form Phone with a valid number should be valid
        """
        form = forms.PhoneForm({'phone':'9990-1111'})
        self.assertTrue(form.is_valid())
        
        form = forms.PhoneForm({'phone': '99999-3333'})
        self.assertTrue(form.is_valid())
    
    def test_with_invalid_numbers(self):
        """
        A Form Phone with a invalid number should be invalid
        """
        form = forms.PhoneForm({'phone':'oooe-ffe13'})
        self.assertFalse(form.is_valid())
        
        form = forms.PhoneForm({'phone':'1111-000f'})
        self.assertFalse(form.is_valid())
        
        form = forms.PhoneForm({'phone':'1111-00000'})
        self.assertFalse(form.is_valid())
        
        form = forms.PhoneForm({'phone':'99-00'})
        self.assertFalse(form.is_valid())

# this form NewContactForm unit Contact and Phone, see agenda/forms.py
class TestNewContactForm(TestCase):
    
    def test_with_valid_data(self):
        """
        With name and phone valid the from should be valid
        """
        form = forms.NewContactForm(
            {'name':'alex', 'phone':'1234-4522'}
        )
        self.assertTrue(form.is_valid())
    
    def test_with_invalid_name(self):
        """
        With name invalid and phone valid the form should be invalid
        """
        form = forms.NewContactForm(
            {'name': '', 'phone': '8273-2323'}
        )
        self.assertFalse(form.is_valid())
    
    def test_with_invalid_phone(self):
        """
        With name valid and phone invalid the form should be invalid
        """
        form = forms.NewContactForm(
            {'name': 'alex', 'phone': '8273-23234'}
        )
        self.assertFalse(form.is_valid())
