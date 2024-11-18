from django.urls import path

from music import views

urlpatterns = [
    path("playlist", views.playlist_view, name="playlist"),
    path("player", views.player_view, name="player"),
]
