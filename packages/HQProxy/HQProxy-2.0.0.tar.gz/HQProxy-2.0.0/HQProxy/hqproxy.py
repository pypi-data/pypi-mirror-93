from fp.fp import FreeProxy
import urllib.request
import socket

proxy = FreeProxy(country_id=['GB','US']).get()
prox = proxy[7:]


def is_bad_proxy(pip):    
    try:        
        proxy_handler = urllib.request.ProxyHandler({'http': pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        sock=urllib.request.urlopen('http://www.google.com')
    except urllib.error.HTTPError as e:        
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail)
        return 1
    return 0

def check_proxy():
    prox = [proxy[7:]]
    for item in prox:
        if is_bad_proxy(item):
            print ("Bad Proxy")
        else:
            print (item)