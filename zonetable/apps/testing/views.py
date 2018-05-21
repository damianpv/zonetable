# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

#from urllib2 import urlopen, Request
#import re, socket
from django.conf import settings


def testing_view(request):
	#domain_re = re.compile('^(http|https):\/\/?([^\/]+)')
	#domain = domain_re.match('http://www.desarrollloinfo.com').group(2)

	remote_addr = request.META.get('REMOTE_ADDR',"127.0.0.1")
	ip_address = request.META.get('REMOTE_ADDR')
	HTTP_HOST = request.META.get('HTTP_HOST')
	REMOTE_HOST = request.META.get('REMOTE_HOST')
	HTTP_X_FORWARDED_HOST = request.META.get('HTTP_X_FORWARDED_HOST')
	HTTP_X_FORWARDED_FOR = request.META.get('HTTP_X_FORWARDED_FOR')
	HTTP_X_FORWARDED_SERVER = request.META.get('HTTP_X_FORWARDED_SERVER')

	#url = "http://api.wipmania.com/" + remote_addr + "?" + domain
    #socket.setdefaulttimeout(5)
    #headers = {'Typ':'django','Ver':'1.0','Connection':'Close'}

	#request.META['REMOTE_ADDR']
	ctx = {
		'content':'%s - %s - %s - %s - %s - %s - %s' % (remote_addr, ip_address, HTTP_HOST, REMOTE_HOST, HTTP_X_FORWARDED_HOST, HTTP_X_FORWARDED_FOR, HTTP_X_FORWARDED_SERVER),
	}
	return render_to_response('testing.html', ctx, context_instance=RequestContext(request))