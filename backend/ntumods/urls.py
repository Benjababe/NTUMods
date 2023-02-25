"""ntumod URL Configuration

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
from django.urls import path, re_path
from django.urls.conf import include
from django.shortcuts import render
from users.urls import urlpatterns as users_urlpatterns
from course_module.views import ModuleSearchViewSet
from timeslot.views import VenueTimeSlotViewSet
from venue.views import VenueSearchViewSet

admin.site.index_title = 'NTU MODULE ADMIN'
admin.site.site_url = 'www.google.com'
admin.site.site_header = 'NTUMODS'


def render_react(request):
    return render(request, "index.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_react),
    path('', include('course_module.urls')),
    path('', include('venue.urls')),
    re_path('modulesearch/', ModuleSearchViewSet.as_view()),
    re_path('venuesearch/', VenueSearchViewSet.as_view()),
    re_path('timeslot/', VenueTimeSlotViewSet.as_view()),
]

urlpatterns += users_urlpatterns
urlpatterns += [re_path(r'^.*', render_react)]
