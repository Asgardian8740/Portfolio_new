from django.contrib import admin

# Register your models here.
from .models import  UrlHit,HitCount

admin.site.register(UrlHit)
admin.site.register(HitCount)