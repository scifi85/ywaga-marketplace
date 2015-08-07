import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ywaga',
        'USER': 'root',
        'PASSWORD': 'laodzi140',
        'HOST': '',
        'PORT': '',
        }
}
import os
os.environ['LANG']='ru_RU.UTF-8'

ROOT_SITE = '/var/www/ywaga'#os.path.dirname(os.path.realpath(__file__))
#STATICFILES_DIRS = (
 #   os.path.join(ROOT_SITE, 'static/'),
  #  )
STATIC_ROOT = ROOT_SITE +'/static/'
ADDRESS = 'ywaga.com'
SESSION_COOKIE_DOMAIN = '.'+ADDRESS
sys.path.insert(0, '/var/www/apps/')
sys.path.insert(0, ROOT_SITE+'/utils/')
