from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView

#import django_cron
#django_cron.autodiscover()
class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(
            context, content_type='text/plain', **kwargs)


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^robots\.txt$', RedirectView.as_view(url='/static/robots.txt')),
    url(r'^sitemap\.xml', RedirectView.as_view(url='/static/sitemap.xml')),
    url(r'^xtaoAuth\.txt', RedirectView.as_view(url='/static/xtaoAuth.txt')),
    
    (r'^tinymce/', include('tinymce.urls')),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    (r'^rosetta/', include('rosetta.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),
#    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
#    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('cart',),}),

    (r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    (r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
    (r'^admin/', include(admin.site.urls)),

    (r'shop/', include('shop.urls')),
    (r'statistic/', include('statistic.urls')),

    (r'^', include('cart.urls')),

    (r'^', include('comments.urls')),
    (r'^', include('log.urls')),
    (r'^', include('news.urls')),

    (r'payment/', include('payments.urls')),
    (r'^accounts/', include('registr.urls')),
)
