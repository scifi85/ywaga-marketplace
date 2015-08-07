from modeltranslation.translator import translator, TranslationOptions
from news.models import NewsItem
from log.models import UserLog

class NewsItemTranslationOptions(TranslationOptions):
    fields = ('name','short','long')

class UserLogTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(NewsItem,NewsItemTranslationOptions)
translator.register(UserLog,UserLogTranslationOptions)
