"""tgmcombine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from tgm_channel import views as tgm_channel_view
from parser import views as parser_view
#from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from tgmcombine import api_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parsdata/', parser_view.pars_data),
    path('startparser/', parser_view.start_parser, name='parsdonor1'),
    path('update/', tgm_channel_view.update_data),
    path('addchannel/', tgm_channel_view.add_channel),
    path('category/<int:category_id>/', tgm_channel_view.category_page, name='categories-id'),
    path('channel/<int:channel_id>/', tgm_channel_view.channel_page, name='channel-id'),
    path('about/', tgm_channel_view.about, name='about'),


    #path('api/v1/channel/', tgm_channel_view.ChannelAPIView.as_view(), name='api-channel'),
    #path('api/v1/channel/', tgm_channel_view.ChannelAPIView.as_view(), name='api-channel'),
     path("api/", include(api_route.urls)),
    # path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    path('users/', include('users.urls')),

    path('', tgm_channel_view.main_page),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
