import urllib,hashlib,time,json,httplib  
from django.conf import settings  

def get_item(id,args):
    '''
    detail_url,num_iid,title,nick,type,cid,seller_cids,props,input_pids,input_str,
    desc,pic_url,num,valid_thru,list_time,delist_time,stuff_status,location,price,
    post_fee,express_fee,ems_fee,has_discount,freight_payer,has_invoice,has_warranty,
    has_showcase,modified,increment,approve_status,postage_id,product_id,auction_point,
    property_alias,item_img,prop_img,sku,video,outer_id,is_virtual
    '''
    params = {
		'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
		'v':'2.0',
		'app_key':settings.TAOBAO_APP_KEY,
		'method':'taobao.item.get',
		'partner_id': 'top-apitools',
		'format':'json',
        'num_iid':id
    }
    S=''
    for arg in args:
        S+=arg+','
    S=S[:len(S)-1]
    params.update({'fields':S})

    try:
        keys = params.keys()
        keys.sort()
        temp = "".join([x+params[x] for x in keys])
        sign = hashlib.md5(settings.TAOBAO_APP_SECRET+temp).hexdigest().upper()
        params.update({'sign':sign})

        alihost = 'gw.api.taobao.com'
        urls = '/router/rest'
        conn = httplib.HTTPConnection(alihost)
        conn.request('GET',urls+'?'+urllib.urlencode(params))
        r = conn.getresponse()
        r = r.read()
        data = json.loads(r)
        result=data['item_get_response']['item']

        if 'item_img' in args:
            urls=data['item_get_response']['item']['item_imgs']['item_img']
            imgs=[]
            for url in urls:
                imgs.append(url['url'])
            result['item_img']=imgs
    except:

        result=-1
    return result



def get_cats(cids_id=None, parent_id=None,args=None):

        params = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'v':'2.0',
            'app_key':settings.TAOBAO_APP_KEY,
            'method':'taobao.itemcats.get',
            'partner_id': 'top-apitools',
            'format':'json',

        }
        if cids_id:
            params['cids']=str(cids_id)
        if parent_id:
            params['parent_cid']=str(parent_id)
        S=''
        for arg in args:
            S+=arg+','
        S=S[:len(S)-1]
        params.update({'fields':S})

#    try:
        keys = params.keys()
        keys.sort()
        temp = "".join([x+params[x] for x in keys])
        sign = hashlib.md5(settings.TAOBAO_APP_SECRET+temp).hexdigest().upper()
        params.update({'sign':sign})

        alihost = 'gw.api.taobao.com'
        urls = '/router/rest'
        conn = httplib.HTTPConnection(alihost)
        conn.request('GET',urls+'?'+urllib.urlencode(params))
        r = conn.getresponse()
        r = r.read()
        print r
        data = json.loads(r)

        result=data['itemcats_get_response']['item_cats']['item_cat']

#    except:
#        result=-1
        return result