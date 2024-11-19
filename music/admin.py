# admin.py
from django.contrib import admin

from .models import YoutubePlaylist


@admin.register(YoutubePlaylist)
class YoutubePlaylistAdmin(admin.ModelAdmin):
    readonly_fields = (
        "title",
        "description",
        "thumbnail_url",
        "video_count",
        "channel_title",
        "created_at",
        "updated_at",
    )
    list_display = ("title", "mood", "video_count", "created_at")
    fields = ("playlist_id", "mood") + readonly_fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("playlist_id",)
        return self.readonly_fields
