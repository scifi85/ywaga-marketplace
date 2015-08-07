from django.forms import ModelForm
from django import forms
from cart.models import *
#from django import forms

class AddressForm(ModelForm):
    class Meta:
        model= Address
