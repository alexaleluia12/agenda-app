
# https://docs.djangoproject.com/en/1.8/ref/validators/#django.core.validators.RegexValidator.message
import re

from django.core.exceptions import ValidationError

def validate_phone_number(value_str):
    """
    value_str need to be 9999-9999 or 99999-9999
    """
    
    """
    r'(\d{5}-\d{4})|(\d{4}-\d{4})' do not solve because
    9999-99999 (invalid) pass but the match is 9999-9999
    """
    str_regex = r'(^\d{5}-\d{4}$)|(^\d{4}-\d{4}$)'
    if not re.match(str_regex, value_str):
        raise ValidationError("%s is not a valid number" % value_str)
