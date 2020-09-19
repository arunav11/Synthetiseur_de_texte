from django.contrib import admin
from django.urls import path

from upload.views import home, run,run_youtube

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('run', run, name='run'),
    path('dev/run', run, name='run'),
    path('run_youtube', run_youtube, name='run_youtube'),
    path('dev/run_youtube', run_youtube, name='run_youtube'),
]
