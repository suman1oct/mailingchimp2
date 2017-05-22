#python imports

#django imports
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#local imports



def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        raise ValidationError("Please enter a valid  email id")