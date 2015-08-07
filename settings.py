try:
    from setting_local import *
    import os
except ImportError:
    pass

APEND_SLASH=False
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
#SESSION_COOKIE_DOMAIN = '.'+ADDRESS

EMAIL_HOST='email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT=25
EMAIL_HOST_USER='AKIAIC4ZIVB6YHPWGT3A'
EMAIL_HOST_PASSWORD='AmufkE5ksQYOIU4kbQ+p6m/90gsN521r2pjxDDocUsso'
EMAIL_USE_TLS =True
DEFAULT_FROM_EMAIL='trade@ywaga.com'
MANAGERS = ADMINS

MERCHANT_ID = 'i4259684524'
SIGNATURE = 'RkgiooGzGTk9jQGdhUsoiIwziok7EhX6l6NTJuusW0pu'
SEND_MONEY_SIGNATURE ='bhlFJqbGsSGOFquG9MRHsuf441IybGMlBE6x0ZqmCb'
CURRENCY ='UAH'
PHONE = '+380992499095'

COMISSION_PHONE='+380991701737'
#COMISSION_ID =
#COMISSION_SIGNATURE =
COMISSION_RATE='2'
TIME_ZONE = 'Europe/Kiev'

AUTH_PROFILE_MODULE='registr.RegistrationProfile'
LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL = '/'

#LANGUAGE_CODE = 'en-us'
SITE_ID = 1

#Languages
USE_I18N = True
#USE_L10N = True

LANGUAGE_CODE = 'ru'
gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
    )

MODELTRANSLATION_DEFAULT_LANGUAGE='ru'
DEFAULT_LANGUAGE = 'ru'#MODELTRANSLATION_DEFAULT_LANGUAGE
#MODELTRANSLATION_TRANSLATION_FILES=(
#    'news.translation','log.translation',
#)
#SITE_ID = 1
TRANSLATION_REGISTRY = "translation"

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SESSION_COOKIE_NAME = 'example'

MEDIA_ROOT = ROOT_SITE+'/media/'
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_URL = '/static/'
#STATIC_ROOT = ROOT_SITE +'/static/'

TAOBAO_APP_KEY = '12401383'
TAOBAO_APP_SECRET = '0ae91a5388c9b03d27763c490f7ade8d'
GOOGLE_KEY = 'AIzaSyC3m8MhAx_7JZuc-jH98S5mQ7tR_YrpOW0'

PAYPAL_RECEIVER_EMAIL='vn_1337243395_biz@xoposho.com'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '48237+z4n(fk9qwn6hr!ak!-*r_!0%qr&$a1e=s)eefj=kjhz6'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
#    'django.core.context_processors.auth',
#
#    'django.contrib.auth.context_processors.auth'
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'shop.middlware.addCartId',
    'shop.middlware.SubdomainsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
#    'django.middleware.locale.LocaleMiddleware',

)
#ROOT_HOSTCONF = 'busybird.hosts'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    ROOT_SITE+'/templates/'
)

TINYMCE_SPELLCHECKER = True
TINYMCE_JS_URL = "%s/plugins//tiny_mce/tiny_mce_src.js" % MEDIA_URL
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG = {
    'theme': "simple",
    'plugins': "spellchecker",
    'theme_advanced_buttons3_add': "|,spellchecker",
    }
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE ='ru'
ROSETTA_EXCLUDED_APPLICATIONS = ('admin_tools','admin_tools1','modeltranslation','multilingual','paypal','rosetta')
INSTALLED_APPS = (
    'paypal.standard.ipn',
    'tinymce',
    'rosetta',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'modeltranslation',
    'log',
    'comments',
    'shop',
    'cart',
    'payments',
    'registr',
    'news',
    'statistic'



    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
