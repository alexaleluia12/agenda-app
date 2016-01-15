from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import decorators

from . import forms
from . import models


# TODO


title = 'agenda'
default_dict_to_render = {}
default_dict_to_render['title'] = title


@decorators.login_required(login_url='/agenda/login/')
def delete_contact(request, contact_id):
    page = 'agenda/dcontact.html'
    contact = get_object_or_404(models.Contact, pk=contact_id)
    to_render = {
        'title':request.user.username
      , 'contact': contact
    }
    
    return render(request, page, to_render)

@decorators.login_required(login_url='/agenda/login/')
def delete_contact_confirmed(request, contact_id):
    contact = get_object_or_404(models.Contact, pk=contact_id)
    contact.delete()
    
    return redirect(reverse('agenda:main'))

# add a contact the user can also add a phone
@decorators.login_required(login_url='/agenda/login/')
def add_contact(request):
    page = 'agenda/acontact.html'
    to_render = {'title':request.user.username}
    
    if request.method == 'POST':
        form = forms.NewContactForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            usr = request.user
            contact = usr.contact_set.create(name=clean_form['name'])
            contact.phone_set.create(number=clean_form['phone'])
            return redirect(reverse('agenda:main'))
        
        else:
            to_render['msg'] = ':('
            to_render['form'] = form
    else:
        form = forms.NewContactForm()
        to_render['form'] = form
    
    return render(request, page, to_render)


# edit contact will allow change the exist name
@decorators.login_required(login_url='/agenda/login/')
def edit_contact(request, contact_id):
    page = 'agenda/econtact.html'
    contact = get_object_or_404(models.Contact, pk=contact_id)
    to_render = {'contact': contact, 'title': request.user.username}
    
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            contact.name = clean_form['name']
            contact.save()
            return redirect(reverse('agenda:main'))
        else:
            to_render['msg'] = ':('
            to_render['form'] = form
    else:
        form = forms.ContactForm({'name': contact.name})
        to_render['form'] = form
    
    return render(request, page, to_render)


# to add a phone i need to know the id of the contact
@decorators.login_required(login_url='/agenda/login/')
def add_phone(request, contact_id):
    page = 'agenda/aphone.html'
    contact = get_object_or_404(models.Contact, pk=contact_id)
    to_render = {'contact': contact, 'title': request.user.username}
    
    if request.method == 'POST':
        form = forms.PhoneForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            contact.phone_set.create(number=clean_form['phone'])
            return redirect(reverse('agenda:detail', args=(contact_id, )))
        else:
            to_render['msg'] = ':('
            to_render['form'] = form
    else:
        form = forms.PhoneForm({'phone':'9999-9999'})
        to_render['form'] = form
    
    return render(request, page, to_render)


@decorators.login_required(login_url='/agenda/login/')
def delete_phone(request, phone_id):
    phone = get_object_or_404(models.Phone, pk=phone_id)
    user_id = phone.contact.id
    phone.delete()
    return redirect(reverse('agenda:detail', args=(user_id, )))


@decorators.login_required(login_url='/agenda/login/')
def edit_phone(request, phone_id):
    page = 'agenda/ephone.html'
    phone = get_object_or_404(models.Phone, pk=phone_id)
    to_render = {'phone': phone}
    
    if request.method == 'POST':
        form = forms.PhoneForm(request.POST)
        if form.is_valid():
            clean_phone = form.cleaned_data
            phone.number = clean_phone['phone']
            phone.save()
            # return to detail page of the user
            return redirect(reverse('agenda:detail', args=(phone.contact.id, )))
        else:
            to_render['form'] = form
            to_render['msg'] = ':('
    else:
        form = forms.PhoneForm({'phone': phone.number})
        to_render['form'] = form
        
    return render(request, page, to_render)


@decorators.login_required(login_url='/agenda/login/')
def contact_detail(request, contact_id):
    page = 'agenda/detail.html'
    contact = get_object_or_404(models.Contact, pk=contact_id)
    tmp_lst = contact.phone_set.all()
    to_render = {
        'contact': contact
      , 'phones_lst': tmp_lst
      , 'title': request.user.username
      , 'len': 1 if tmp_lst.count() < 2 else 2
    }
    return render(request, page, to_render)


@decorators.login_required(login_url='/agenda/login/')
def main(request):
    page = 'agenda/main.html'
    contacts_lst = request.user.contact_set.order_by('name')
    phones_lst = [
       i.phone_set.first() if i.phone_set.first() else '#'
       for i in request.user.contact_set.order_by('name')
    ]
    to_render = {
        'len': 2 if len(contacts_lst) else 1
      , 'title': request.user.username
      , 'contacts_phones_lst': zip(contacts_lst, phones_lst)
      , 'contacts_lst': contacts_lst
      , 'phones_lst': phones_lst
    }
    
    return render(request, page, to_render)


def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('agenda:main'))
    return render(request, 'agenda/index.html', default_dict_to_render)


# refatorar esse methodo
def sign(request):
    page = 'agenda/sign.html'
    to_render = {'title': title}
    
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            if User.objects.filter(username=clean_form['name']):
                # this name alread exist
                msg = 'this name already exist, choice another'
                form = forms.LoginForm()
                to_render['form'] = form
                to_render['msg'] = msg
            else: ## sucess
                User.objects.create_user(
                    username=clean_form['name']
                  , password=clean_form['password']
                )
                return redirect(reverse('agenda:home') + '?msg=user successfully created')
                # http://www.example.com/myapp/
                # http://www.example.com/myapp/?page=3
                # use the same url pattern myapp/
        
        else: # invalid form
            to_render['form'] = form
            to_render['msg'] = ':( Form invalid'
    
    else: # GET method
        form = forms.LoginForm()
        to_render['form'] = form
    
    return render(request, page, to_render)


def login(request):
    page = 'agenda/login.html'
    to_render = {'title': title}
    
    if request.method == 'POST' :
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            user = auth.authenticate(
                username=clean_form['name']
              , password=clean_form['password']
            )
            if user:
                auth.login(request, user)
                return redirect(reverse('agenda:main'))
            else:
                to_render['form'] = form
                to_render['msg'] = 'User or password invalid'
        
        else: # invalid form
            to_render['form'] = form
            to_render['msg'] = ':( Invalid form'
    
    else: # GET method
        form = forms.LoginForm()
        to_render['form'] = form
    
    return render(request, page, to_render)


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect(reverse('agenda:home'))


