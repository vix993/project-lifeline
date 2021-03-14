from .views import health_check
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    url(r'^$', health_check, name='health-check'),
    # url(r'reports/(?P<pk>\d+)$', ReportsView.as_view(), name='reports-ru')
]