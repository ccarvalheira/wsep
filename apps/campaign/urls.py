from django.conf.urls import *

from apps.campaign.views import CenasView

urlpatterns = patterns('apps.campaign.views',

    url(r'home/', CenasView.as_view(), name="home"),
    
)
