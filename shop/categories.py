import urllib,hashlib,time,json,httplib

CATEGORIES = {
    'Clothes':{
               't-shirt':{
                            'official':0,
                            'casual':0
                         },
               'pants':{
                            'jeans':{
                                       'brand':{
                                                  'levis':0,
                                                  'not levis':0
                                       },
                                       'no brand':0,
                            },
                            'usual':0
               }
    },
    'Electronics': {
                    'Smartphones': 0
    },
}

a={1:None,2:{21:None,22:{221:{2211:None},222:None,223:{2231:None,2232:None}}},3:None,4:None}
#a={1:None,2:{21:None},3:None}
#a=CATEGORIES
parents =[]
def find(index):
    def f(a,z=[]):
        for k,v in a.items():
            if k==index:
                global parents
                parents = z[0:]

            if not v==None:
                z.append(k)
                f(a[k],z)
                z.remove(k)
        return a
    f(a)
    return parents
print find(123)
from django.conf import settings
#import json
#import urllib2
#from django.utils.http import urlquote
#def translate(text,from_lang='zh-CN',to_lang='ru'):
#    GOOGLE_KEY='AIzaSyC3m8MhAx_7JZuc-jH98S5mQ7tR_YrpOW0'
#    text=urlquote(text)
#
#    url='https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=%s&target=%s'\
#    % (GOOGLE_KEY,text,from_lang,to_lang)
#
#
#    while(True):
#        try:
#            recv = urllib2.build_opener().open(url).read()
#        except :
#            recv=-1
#        if recv==-1:
#            print 'translate error'
#        else:
#            break
#    return json.loads(recv)['data']['translations'][0]['translatedText']
#
#
#
#def get_cats(cids_id=None, parent_id=None,args=None):
#    TAOBAO_APP_KEY = '21030068'
#    TAOBAO_APP_SECRET = '55ee08ff60c6af37667ac96b89f4178a'
#    params = {
#        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
#        'v':'2.0',
#        'app_key':TAOBAO_APP_KEY,
#        'method':'taobao.itemcats.get',
#        'partner_id': 'top-apitools',
#        'format':'json',
#
#        }
#    if cids_id:
#        params['cids']=str(cids_id)
#    if parent_id:
#        params['parent_cid']=str(parent_id)
#    S=''
#    for arg in args:
#        S+=arg+','
#    S=S[:len(S)-1]
#    params.update({'fields':S})
#
#    try:
#        keys = params.keys()
#        keys.sort()
#        temp = "".join([x+params[x] for x in keys])
#        sign = hashlib.md5(TAOBAO_APP_SECRET+temp).hexdigest().upper()
#        params.update({'sign':sign})
#
#        alihost = 'gw.api.taobao.com'
#        urls = '/router/rest'
#        conn = httplib.HTTPConnection(alihost)
#        conn.request('GET',urls+'?'+urllib.urlencode(params))
#        r = conn.getresponse()
#        r = r.read()
#        data = json.loads(r)
#
#        result=data['itemcats_get_response']['item_cats']['item_cat']
#
#    except:
#        result=-1
#    return result
#
#def get(parent_id):
#    while(True):
#        a=get_cats(parent_id=str(parent_id),args=['cid','is_parent','name'])
#        if a==-1:
#            print 'error'
#        else:
#            break
#    return a
#q={}
#n=0
#def get_cids(parent_id):
#    z={}
#    a=get(parent_id)
#    for i in a:
#        global q,n
#        n+=1
#        print i['cid'],n
#        q[i['cid']]={'cn':i['name'],'en':translate(i['name'],to_lang='en'),'ru':translate(i['name'])}
#
#        if i['is_parent']:
#            z[i['cid']]=get_cids(i['cid'])
#        else:
#            z[i['cid']]=None
#    return z
#
#print '--------------'
##get_cids(0)
##w = open('category_name.py','w')
##w.write(str(q))
##w.close
#
#
#
##def get_name(name):
##    while(True):
##        a=get_cats(cids_id=str(name),args=['name',])
##        if a==-1:
##            print 'error'
##        else:
##            break
##    return a[0]['name']
##
##from categoryTree import *
##q={}
##i=0
##def f(a,z={}):
##    for k,v in a.items():
##        global i
##        i+=1
##        z[k]=v if v==None else f(a[k])
##    return a
##
##f(catTree)
##print i
#
