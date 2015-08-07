# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from registr.forms import RegistrationForm, RegistrationFormUniqueEmail,LoginForm
from registr.models import RegistrationProfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from notification_email import *
from django.utils.translation import ugettext_lazy as _

@csrf_exempt
def activate(request, activation_key,
             template_name='registration/activate.html',
             extra_context=None):
  
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    
        
    next="/"
    error= True
    if account:
		next=account.get_profile().url
		error=False	
		       
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value	
    messages.info(request, 'Activation complete, enter login and password')
		
    #return HttpResponseRedirect('/accounts/login/?activation_complete=true')
    return render_to_response('registration/registration_form.html', {'next':next},context_instance=context )

@csrf_exempt		
def register(request, success_url=None,
             form_class=RegistrationFormUniqueEmail, profile_callback=None,
             template_name='registration/registration_form.html',
             extra_context=None):
    lform = LoginForm()
    rform = RegistrationFormUniqueEmail()
    context = RequestContext(request)

    if request.method == 'POST':
		
        rform = form_class(data=request.POST, files=request.FILES)

        if rform.is_valid():
            new_user = rform.save(profile_callback=profile_callback)
            user = authenticate(username=rform.cleaned_data['username'], password=rform.cleaned_data['password1'])
            from django.utils import translation
            lang= translation.get_language_from_request(request)
            profile = user.get_profile()
            profile.lang=lang
            profile.save()

            sendEmail(user=user,type='registr',extra=[rform.cleaned_data['password1']])
            login(request,user)
            return HttpResponseRedirect('/accounts/register/complete/')
        else:
            lform = LoginForm()

    return render_to_response(template_name,{'rForm':rform,'lForm':lform,'next':next},context_instance=context)

def change_password_done(request):
	return HttpResponse('complete')
	
def change_password_complete(request):
	messages.info(request,_(u'Ваш пароль успешно изменен'))#'Пожалуйста, введите свой логин и пароль')
	return HttpResponseRedirect('/accounts/login/')
	
def reset_done(request):	
	return HttpResponse('complete')

def update(request):
	complete=False
	if request.method == 'POST':
		entry=RegistrationProfile.objects.get(user=request.user)
		entry.skype=request.POST['skype']
		entry.msn=request.POST['msn']
		entry.icq=request.POST['icq']
		entry.save()
		complete=True
	
	SN=False

	return render_to_response('registration/page.html',{'complete':complete, 'SN':SN},context_instance=RequestContext(request))

@csrf_exempt
def login1(request,form_class=RegistrationFormUniqueEmail,template_name='registration/registration_form.html',extra_context=None):
   lform = LoginForm() 
   rform = RegistrationFormUniqueEmail()


   if request.method == 'POST':	
	lform = LoginForm(data=request.POST, files=request.FILES)
	if lform.is_valid():
		user = authenticate(username=lform.cleaned_data['login'], password=lform.cleaned_data['password'])
		if user is None:
			try:
				username=User.objects.get(email=lform.cleaned_data['login']).username
				user = authenticate(username=username, password=lform.cleaned_data['password'])	
			except:
				lform.non_field_errors="Your username or password was incorrect."
	
		if user is not None:           	   
		   if user.is_active: 						
				login(request,user)						
				return HttpResponseRedirect('/')
							
   if extra_context is None:
       extra_context = {}
   context = RequestContext(request)
   for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
         
   return render_to_response(template_name, {'rForm':rform,'lForm':lform,'next':next},context_instance=context )
