from django.urls import path

from . import views
from . import contact
urlpatterns = [
    path('', views.index, name='index'),
]