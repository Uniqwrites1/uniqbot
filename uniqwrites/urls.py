from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Uniqwrites WhatsApp Bot is running!")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('webhook/', include('whatsapp_bot.urls')),
]
