from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from survivor.views import health_check 

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/survivor/', include(('survivor.urls', 'survivor'), namespace='api-survivor')),
    url(r'^$', health_check, name='health-check')
]
