from django.contrib import admin
from django.urls import path
from upload.views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', hello),
]
