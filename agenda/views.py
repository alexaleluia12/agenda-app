from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import decorators

from . import forms

"""
query orm

>>> p = User.objects.get(username="pedro")
>>> p
<User: pedro>
>>> p.username
'pedro'
>>> p.user
p.user_permissions(  p.username           
>>> p.contact_set.all()
[<Contact: hulke>]
>>> p.contact_set.creat
p.contact_set.create(           p.contact_set.creation_counter
>>> p.contact_set.create(name="pano azul")
<Contact: pano azul>
>>> p.contact_set.all()
[<Contact: hulke>, <Contact: pano azul>]
>>> c = p.contact_set.create(name="teclado")
>>> c
<Contact: teclado>
>>> c.phone_set.all()
[]
>>> 
>>>
"""


title = 'agenda'
default_dict_to_render = {}
default_dict_to_render['title'] = title

@decorators.login_required(login_url='/agenda/login/')
def main(request):
    contacts_lst = request.user.contact_set.all()
    dict_render = {'len': len(contacts_lst), 'title': request.user.username}
    page = 'agenda/main.html'
    
    return render(request, page, dict_render)


def home(request):
    return render(request, 'agenda/index.html', default_dict_to_render)

def sign(request):
    page = 'agenda/sign.html'
    dict_render = {}
    to_render = None
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            if User.objects.filter(username=clean_form['name']):
                # this name alread exist
                msg = 'this name alreda exist, choice another'
                form = forms.LoginForm()
                to_render = render(request, page, 
                    {'form': form, 'msg': msg}
                )
            else: ## sucess
                User.objects.create_user(
                    username=clean_form['name'],
                    password=clean_form['password']
                )
                return redirect(reverse('agenda:home') + '?msg=user successfully created')
                # passando query string para uma url
                # nota que eu nao preciso mecher no url.py
                # pois
                # http://www.example.com/myapp/
                # http://www.example.com/myapp/?page=3
                # vao buscar o mesmo padrao q eh myapp/
                
        else:
            to_render = render(request, page, {'form': form})
    else:
        form = forms.LoginForm()
        to_render = render(request, page, {'form': form})
    
    return to_render

def login(request):
    page = 'agenda/login.html'
    dict_render = {}
    to_render = None
    
    if request.method == 'POST' :
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            clean_form = form.cleaned_data
            user = auth.authenticate(username=clean_form['name'], 
                                     password=clean_form['password'])
            if user:
                auth.login(request, user)
                return redirect(reverse('agenda:main'))
            else:
                to_render = render(request, page,
                    {  'form': forms.LoginForm()
                     , 'msg' : 'Usuario ou senha invalidos'
                    }
                )
        else:
            to_render = render(request, page, {'form': form})
    else:
        form = forms.LoginForm()
        to_render = render(request, page,  {'form': form})
    
    return to_render

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect(reverse('agenda:home'))

# Create your views here.
