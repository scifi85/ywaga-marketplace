from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from registr.views import activate
from registr.views import register, login1, change_password_done, reset_done,update,change_password_complete


urlpatterns = patterns('',
	url(r'^page/$',
		update,
		),
		
	url(r'^activate/(?P<activation_key>\w+)/$',
		activate,
		name='registration_activate'),
		
	url(r'^login/$',
		login1,
		name='auth_login'),
		
	url(r'^logout/$',
		auth_views.logout,{'next_page':'/'},
		name='auth_logout'),
			
	url(r'^password/change/$', 
		auth_views.password_change,
		{'post_change_redirect' : '/accounts/password_change/done/','template_name': 'registration/password_change.html','from_email':'trade@ywaga.com'},
		name='auth_password_change'),

	url(r'^password_change/done',                           
		change_password_done 
		),

	url(r'^password/reset/$',
		auth_views.password_reset,
		{'post_reset_redirect' : '/accounts/password/reset/done/','template_name': 'registration/reset.html'},
		name='auth_password_reset'),

	url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
		auth_views.password_reset_confirm, {'template_name': 'registration/registration_form.html', 'post_reset_redirect':'/accounts/password/reset/complete/'},                                                      
		name='auth_password_reset_confirm'),

	url(r'^password/reset/complete/$',
		change_password_complete,		
		name='auth_password_reset_complete'),

	url(r'^password/reset/done/$',
		reset_done,
	),

	url(r'^register/$',
		register,
		name='registration_register'),
		
	url(r'^register/complete/$',
		direct_to_template,
		{'template': 'registration/registration_complete.html'},
		name='registration_complete'),
	)
