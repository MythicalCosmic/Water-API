from django.contrib import admin
from django.urls import path, include
from docs.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', home, name="home")
]
