from django.urls import path

from . import views

urlpatterns = [
    path('<str:artist_name>/', views.view_artist_detail, name="artist_detail")
]
