from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import detail,brief

import time,hashlib

KEEP_PERIOD=30*24*60*60*1000
MODIFY=True
 
def brief_engaged(request,a,b):
	brf=get_unique(brief, imay=a)
	if brf:
		if brf.info!=b:
			brf.info=b
			brf.save()
			return HttpResponse('Update-Brief|'+ (brf.swap or brf.sha1)) 
		else:
			return HttpResponse('Repeat-Brief|'+ (brf.swap or brf.sha1))
	else:
		brf=brief.objects.create(imay=a,info=b,sha1='',swap=sha(a))
		return HttpResponse('OK-Brief|'+brf.swap) 

def sha(a):
	tmp=str(time.time())+a
	return hashlib.sha1(tmp.encode('utf-8')).hexdigest()

def get_unique(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        return None

def detail_engaged(request,a,b,c):
	a=a.strip()
	brf=get_unique(brief,sha1=a) or get_unique(brief,swap=a)

	if brf:
		remove_expired(brf,b)
		header="OK-Detail"
		tmp1=detail.objects.filter(head=brf,lump=c).order_by('-node')	
		if tmp1.count()>=2:
			tmp2=detail.objects.filter(node__gt=tmp1[1].node,node__lt=tmp1[0].node,head=brf)
			if tmp2.count()==0:
				detail.objects.filter(node=tmp1[0].node,head=brf).delete()
				header="OK-Stay"
		detail.objects.create(head=brf,node=b,lump=c)
	else:
		return HttpResponse('Format Error-Detail or Not Registered')

	if get_unique(brief,swap=a):
		brf.sha1=a
		brf.swap=''

	mrk=(MODIFY or brf.swap) and (brf.swap or sha(brf.imay))
	brf.swap=mrk
	# brf.save()

	mrk=(mrk and '|' or '') +mrk
	header=brf.comd or header
	brf.comd=''
	brf.save()
	return HttpResponse(header+mrk)


def location_engaged(request,a,f,t):
	brf=get_unique(brief,imay=a)
	tmp=detail.objects.filter(node__gte=f,node__lte=t,head=brf).order_by('-node')
	mrk=''
	for i in tmp:
		mrk+='@'+i.node+'|'+i.lump
	return HttpResponse("OK-location"+mrk)

def device_list(request):
	tmp=brief.objects.all()
	mrk=''
	for i in tmp:
		mrk+='|'+i.imay
	return HttpResponse("OK-Device"+mrk)

def command_engaged(request,a,c):
	brf=get_unique(brief,imay=a)
	brf.comd=c
	brf.save()
	
def valid_t(t):
	tmp=abs(int(t)-int(time.time()*1000))
	# return tmp<KEEP_PERIOD
	return True

# def valid_d(d):
# 	sep=d.split('|')
# 	tmp=True
# 	for i in sep:
# 		tmp=tmp and i.isnumeric()
# 	return tmp

def remove_expired(brf,t):
	tmp=int(t)-KEEP_PERIOD
	detail.objects.filter(head=brf,node__lt=tmp).delete()



