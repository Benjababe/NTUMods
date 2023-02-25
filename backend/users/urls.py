from django.urls import include, path


# Using djoser to help with login/logout
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
