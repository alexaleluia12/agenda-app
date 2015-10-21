from django.db import models

len_name = 50
# follow the Brazil low
# https://en.wikipedia.org/wiki/National_conventions_for_writing_telephone_numbers#Brazil
# 10 === 9NNNN-NNNN , 9 digits plus -
len_phone = 10

class Contact(models.Model):
    name = models.CharField(max_length=len_name)
    owner = models.ManyToManyField('auth.User')
    
    def __str__(self):
        return self.name


class Phone(models.Model):
    
    number = models.CharField(max_length=len_phone)
    contact = models.ForeignKey(Contact)
    
    def __str__(self):
        return self.number
