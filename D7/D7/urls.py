from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('simpleapp/', include('simpleapp.urls')),
   path('account/', include('allauth.urls')),
   path('contact', include('contact.urls')),
]

