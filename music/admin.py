# admin.py
from django.contrib import admin

from .models import YoutubePlaylist


@admin.register(YoutubePlaylist)
class YoutubePlaylistAdmin(admin.ModelAdmin):
    list_display = ("title", "mood", "playlist_id", "created_at", "updated_at")
    list_filter = ("mood", "created_at")
    search_fields = ("title", "description", "playlist_id")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
