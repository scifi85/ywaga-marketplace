from django.conf import settings
import json
import urllib2
from django.utils.http import urlquote
def translate(text,from_lang='zh-CN',to_lang='ru'):
    text=urlquote(text)

    url='https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=%s&target=%s'\
                % (settings.GOOGLE_KEY,text,from_lang,to_lang)

    recv = urllib2.build_opener().open(url).read()
    return json.loads(recv)['data']['translations'][0]['translatedText']

