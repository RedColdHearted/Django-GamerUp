from django.contrib import admin
from django.urls import re_path
from django.views.generic import TemplateView

from app.urls.base import *

urlpatterns += [
    path('admin/', admin.site.urls),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html'))
]
