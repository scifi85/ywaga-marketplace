import urllib
import urllib2
import base64
import sha
import logging
import decimal

try:
    import xml.etree.ElementTree as ET # in python >=2.5
except ImportError:
    try:
        import cElementTree as ET # effbot's C module
    except ImportError:
        try:
            import elementtree.ElementTree as ET # effbot's pure Python module
        except ImportError:
            try:
                import lxml.etree as ET # ElementTree API using libxml2
            except ImportError:
                import warnings
                warnings.warn("could not import ElementTree "
                              "(http://effbot.org/zone/element-index.htm)")
                # Or you might just want to raise an ImportError here.

logger = logging.getLogger('liqpay')
#logger = logging.basicConfig(filename='example.log')
class LiqpayError(Exception): pass
class LiqpayResponseError(LiqpayError): pass
class LiqpaySignatureError(LiqpayError): pass
class LiqpayOperationError(LiqpayError): pass

# Payment methods
PayWayLiqpay = 'liqpay'
PayWayCard = 'card'

# Currencies
CurrencyUAH = 'UAH'
CurrencyUSD = 'USD'
CurrencyEUR = 'EUR'
CurrencyRUR = 'RUR'

class Transaction(object):
    def __init__(self, id, amount, currency, description, merchant_phone, order_id, sender, to, referer_url, status):
        self.id = id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.merchant_phone = merchant_phone
        self.order_id = order_id
        self.sender = sender
        self.to = to
        self.referer_url = referer_url
        self.status = status

class MerchantXml(object):
    def __init__(self, xml, signature):
        self.xml = xml
        self.signature = signature
        
    @property
    def encoded_xml(self):
        return base64.encodestring(self.xml).strip()

    @property
    def encoded_signature(self):
        return base64.encodestring(self.signature).strip()
        
class MerchantResponse(object):
    def __init__(self, version, action_type, merchant_id, order_id, amount, currency, description, status, code, transaction_id, pay_way, pay_details, sender_phone):
        self.version = version
        self.action_type = action_type
        self.merchant_id = merchant_id
        self.order_id = order_id
        self.amount = amount
        self.currency = currency
        self.description = description
        self.status = status
        self.code = code
        self.transaction_id = transaction_id
        self.pay_way = pay_way
        self.pay_details = pay_details
        self.sender_phone = sender_phone
    
class _ResponseElementFinder(object):
    def __init__(self, response):
        self.response = response
        
    def find(self, el_name, coerce=unicode):
        el = self.response.find(el_name)
        if el is not None:
            return coerce(el.text)
        return None

class Liqpay(object):
    def __init__(self, merchant_id,  signature):
        self.merchant_id = merchant_id
        self.signature = signature

    def build_merchant_xml(self, order_id, amount, currency, description, pay_way=None, default_phone=None, result_url=None, server_url=None):
        request_el = ET.Element('request')
        ET.SubElement(request_el, 'version').text = '1.2'
        if result_url:
            ET.SubElement(request_el, 'result_url').text = result_url 
        if server_url:
            ET.SubElement(request_el, 'server_url').text = server_url
        ET.SubElement(request_el, 'merchant_id').text = self.merchant_id
        ET.SubElement(request_el, 'order_id').text = unicode(order_id)
        ET.SubElement(request_el, 'amount').text = str(amount)
        ET.SubElement(request_el, 'currency').text = currency
        ET.SubElement(request_el, 'description').text = description
        if pay_way:
            ET.SubElement(request_el, 'pay_way').text = pay_way or ''
        ET.SubElement(request_el, 'default_phone').text = default_phone or ''

        xml = ET.tostring(request_el, 'utf-8')
        
        return MerchantXml(xml, self._sign_xml(xml))

    def parse_merchant_response_xml(self, opxml, signature):
        xml = base64.decodestring(opxml)
        
        if not self._verify_sig(xml, base64.decodestring(signature)):
            raise LiqpaySignatureError('Response signature verification failed')
        
        response = ET.fromstring(xml)
        
        assert(response.tag == 'response')
                
        f = _ResponseElementFinder(response)
                
        return MerchantResponse(
                    f.find('version'),
                    f.find('action'),
                    f.find('merchant_id'),
                    f.find('order_id'),
                    f.find('amount', decimal.Decimal),
                    f.find('currency'),
                    f.find('description'),
                    f.find('status'),
                    f.find('code'),
                    f.find('transaction_id'),
                    f.find('pay_way'),
                    f.find('pay_details'),
                    f.find('sender_phone')
            
        )
        
        return xml

    def get_ballances(self):
        request_el = ET.Element('request')
        ET.SubElement(request_el, 'version').text = '1.2'
        ET.SubElement(request_el, 'action').text = 'view_balance'
        ET.SubElement(request_el, 'merchant_id').text = self.merchant_id

        response_text = self._send_request(ET.tostring(request_el))
        response_el = ET.fromstring(response_text)

        logger.debug('view_balance response: %r' % response_text)
        
        status_el = response_el.find('status')
        if status_el is not None and status_el.text == 'failure':
            description_el = response_el.find('response_description')
            if description_el is None:
                raise LiqpayOperationError('Operation failed')
            else:
                raise LiqpayOperationError(description_el.text.strip())
        
        balance_el = response_el.find('balances')
        if balance_el is None:
            raise LiqpayResponseError('Balance response had no <balances> tag')
        
        return dict([x.tag, decimal.Decimal(x.text)] for x in balance_el)
        
    def get_transaction(self, transaction_id=None, order_id=None):
        request_el = ET.Element('request')
        ET.SubElement(request_el, 'version').text = '1.2'
        ET.SubElement(request_el, 'action').text = 'view_transaction'
        ET.SubElement(request_el, 'merchant_id').text = self.merchant_id

        if transaction_id:
            ET.SubElement(request_el, 'transaction_id').text = unicode(transaction_id)
            
        if order_id:
            ET.SubElement(request_el, 'order_id').text = unicode(order_id)
            

        response_text = self._send_request(ET.tostring(request_el))
        response_el = ET.fromstring(response_text)

        logger.debug('view_transaction response: %r' % response_text)
        
        status_el = response_el.find('status')
        if status_el is not None and status_el.text == 'failure':
            description_el = response_el.find('response_description')
            if description_el is None:
                raise LiqpayOperationError('Operation failed')
            else:
                raise LiqpayOperationError(description_el.text.strip())
        
        transaction_el = response_el.find('transaction')
        if transaction_el is None:
            raise LiqpayResponseError('View transaction response had no <transaction> tag')
        
        f = _ResponseElementFinder(transaction_el)
                
        return Transaction(
            f.find('id'),
            f.find('amount', decimal.Decimal),
            f.find('currency'),
            f.find('description'),
            f.find('merchant_phone'),
            f.find('order_id'),
            f.find('from'),
            f.find('to'),
            f.find('referer_url'),
            f.find('status')
        )
    
    def send_money(self, to, amount, currency, description=None, order_id=None):
        request_el = ET.Element('request')
        ET.SubElement(request_el, 'version').text = '1.2'
        ET.SubElement(request_el, 'action').text = 'send_money'
        ET.SubElement(request_el, 'merchant_id').text = self.merchant_id
        
        ET.SubElement(request_el, 'kind').text = 'phone'
        
        ET.SubElement(request_el, 'to').text = to
        ET.SubElement(request_el, 'amount').text = unicode(amount)
        ET.SubElement(request_el, 'currency').text = currency
        ET.SubElement(request_el, 'description').text = description or ''
        
        if order_id:
            ET.SubElement(request_el, 'order_id').text = unicode(order_id)
            
        response_text = self._send_request(ET.tostring(request_el, 'utf-8'))
        response_el = ET.fromstring(response_text)

        logger.debug('send_money response: %r' % response_text)
        
        status_el = response_el.find('status')
        if status_el is not None and status_el.text == 'failure':
            description_el = response_el.find('response_description')
            if description_el is None:
                raise LiqpayOperationError('Operation failed')
            else:
                raise LiqpayOperationError(description_el.text.strip())
        
        transaction_el = response_el.find('transaction_id')
        if transaction_el is None:
            raise LiqpayResponseError('Send money response had no <transaction_id> tag')
    
        return transaction_el.text
    
    def _send_request(self, op_list):
        request_xml = self._build_request(op_list)
        logger.debug("Sending request '%r'", request_xml)
        try:
            req = urllib2.urlopen(urllib2.Request('https://liqpay.com/?do=api_xml', request_xml, {'Content-Type':'text/xml'}))
        except IOError, e:
            print "error"
            if hasattr(e, 'reason'):
                logger.error('We failed to reach a server. Reason: %s', e.reason)
            elif hasattr(e, 'code'):
                logger.error('The server couldn\'t fulfill the request. Error code: %s', e.code)
            raise
        
        response_text = req.read()
        logger.debug("Got response '%r'", response_text)
        
        return self._extract_response(response_text)

    def _build_request(self, opxml):
        request_el = ET.Element('request')
        liqpay_el = ET.SubElement(request_el, 'liqpay')

        envelope_el = ET.SubElement(liqpay_el, 'operation_envelope')
        opxml_el = ET.SubElement(envelope_el, 'operation_xml')
        sig_el = ET.SubElement(envelope_el, 'signature')
        
        opxml_el.text = self._base64(opxml)
        sig_el.text = self._base64(self._sign_xml(opxml))
        return (u'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(request_el)).encode('utf-8')

    def _extract_response(self, data):
        response_el = ET.fromstring(data)
        el = response_el.find('liqpay/operation_envelope')

        if el is None:
            raise LiqpayResponseError('Response had no <operation_envelope>')
        
        opxml_el = el.find('operation_xml')
        sig_el = el.find('signature')

        opxml = base64.decodestring(opxml_el.text)
        response_sig = base64.decodestring(sig_el.text)

        if not self._verify_sig(opxml, response_sig):
            raise LiqpaySignatureError('Response signature verification failed')
        
        return opxml

    def _base64(self, text):
        return base64.encodestring(text).strip()

    def _sign_xml(self, xml):
        return sha.new(self.signature + xml + self.signature).digest()

    def _verify_sig(self, xml, sig):
        xml_sig = sha.new(self.signature + xml + self.signature).digest()
        return sig == xml_sig
