from django.contrib.auth.models import User

def create_user(name, password):
    return User.objects.create_user(username=name, password=password)

def create_contact(user, name):
    return user.contact_set.create(name=name)

class BasicEnvironment:
    """
    Give an user logged
    """
    def __init__(self, callback_login):
        user_name = 'pedro'
        password = '987654321'
        self.user = create_user(user_name, password)
        response = callback_login(username=user_name, password=password)
        assert(response == True)
