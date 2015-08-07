    # -*- encoding: utf-8 -*-
from django import forms
from shop.models import *
from django.forms import ModelForm
from django import forms
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext_lazy as _

#attrs_dict = { 'class': 'required' }

class NewProductForm(ModelForm):
#    meta_description = forms.CharField(widget=forms.TextInput(), max_length=255, required=False)
#
    description = forms.CharField(widget=TinyMCE(attrs={"class":"tiny_class","style":"width:335px"},), required=False)

    price = forms.FloatField(widget=forms.TextInput(attrs={"class":"input-medium onlyFloat", 'placeholder':_(u"Цена"),"maxlength":"8"}),
        required=True)
    promotion_price = forms.FloatField(widget=forms.TextInput(attrs={"class":"input-medium onlyFloat", "placeholder":_(u"Цена"),"maxlength":"8"}),
        required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"input-medium", "placeholder":_(u"Название")}),
        max_length=255, required=True)
    quantity = forms.CharField(widget=forms.TextInput(attrs={"class":"input-medium onlyInt", "placeholder":_(u"Количество")}),
        max_length=8,required=True)
    preorder_days= forms.IntegerField(widget=forms.TextInput(attrs={"class":"input-medium onlyInt", "placeholder":_(u"Дни"),"maxlength":"3"}),
        required=False)
    internal_delivery= forms.FloatField(widget=forms.TextInput(attrs={"class":"input-medium onlyFloat","maxlength":"5"}),initial=0.0,
        required=False)
    external_delivery= forms.FloatField(widget=forms.TextInput(attrs={"class":"input-medium onlyFloat","maxlength":"5"}),initial=0.0,
        required=False)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(NewProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data=super(NewProductForm, self).clean()
        if '<script>' in cleaned_data.get("description"):
            from log.models import *
            SystemLog.objects.create(user=self.request.user,type="hack",text="hack attempt "+cleaned_data.get("description"))
            del cleaned_data["description"]
        return cleaned_data

    class Meta:
        model = Product
        exclude = ('user','barcode','images','self_price','front_image','keywords','colors','sizes','price'
            'comments','category','bought','comments','votes','deals','link')



