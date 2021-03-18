from .views import health_check, CreateSurvivorAPIView, RetrieveUpdateSurvivorView, CreateFlagAPIView
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    url(r'^$', CreateSurvivorAPIView.as_view(), name='create-list-survivors'),
    url(r'^(?P<pk>\d+)$', RetrieveUpdateSurvivorView.as_view(), name='ru-survivor'),
    url(r'flag/$', CreateFlagAPIView.as_view(), name='flag-create'),
]