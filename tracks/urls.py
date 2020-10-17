from django.urls import path

from tracks import views

urlpatterns = [
    path('<str:artist>/<str:album>/<str:track>/', views.get_track_view, name='get_track'),
    path('top/<str:artist>/', views.view_tracks_info, name='tracks_info'),
    path('search/<str:q>/', views.search_track_view, name='search_track')
]
