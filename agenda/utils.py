from django.contrib.auth.models import User

def create_user(name, password):
    return User.objects.create_user(username=name, password=password)

def create_contact(user, name):
    return user.contact_set.create(name=name)

