from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import  Paginator,PageNotAnInteger,EmptyPage
from django import forms
from .models import UrlHit, HitCount
from django.core.mail import send_mail, get_connection
from django.http import HttpResponseRedirect



class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(required=False, label='Your e-mail address')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

def index(request):
    cnts=hit_count(request)
    return render(request, 'index.html',{'counts':cnts+40})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hit_count(request):
    if not request.session.session_key:
        request.session.save()
    s_key = request.session.session_key
    ip = get_client_ip(request)
    url, url_created = UrlHit.objects.get_or_create(url=request.path)

    if url_created:
        track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
        if created:
            url.increase()
            request.session[ip] = ip
            request.session[request.path] = request.path
    else:
        if ip and request.path not in request.session:
            track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
            if created:
                url.increase()
                request.session[ip] = ip
                request.session[request.path] = request.path
    return url.hits
