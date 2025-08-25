from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.webhook, name='webhook'),  # Matches both /webhook and /webhook/
]
