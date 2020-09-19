from django.contrib import admin
from django.urls import path

from upload.views import home, run

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('run', run, name='run'),
    path('dev/run', run, name='run')
]
