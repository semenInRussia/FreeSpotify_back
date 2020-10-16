from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tracks/', include('tracks.urls')),
    path('api/artists/', include('artists.urls')),
]
