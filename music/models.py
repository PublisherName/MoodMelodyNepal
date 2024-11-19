from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from googleapiclient.discovery import build

from music.enum import MoodChoices


class YoutubePlaylist(models.Model):
    title = models.CharField(max_length=200, editable=False)
    playlist_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, editable=False)
    mood = models.CharField(
        max_length=10, choices=MoodChoices.choices(), default=MoodChoices.NEUTRAL.value
    )
    thumbnail_url = models.URLField(blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_count = models.IntegerField(default=0, editable=False)
    channel_title = models.CharField(max_length=100, blank=True, editable=False)

    def clean(self):
        if not self.playlist_id:
            raise ValidationError("Playlist ID is required")
        super().clean()

    def fetch_playlist_data(self):
        try:
            youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)

            # Get playlist details
            playlist_response = (
                youtube.playlists()
                .list(part="snippet,contentDetails", id=self.playlist_id)
                .execute()
            )

            if not playlist_response["items"]:
                raise ValidationError(f"No playlist found with ID: {self.playlist_id}")

            playlist_data = playlist_response["items"][0]

            # Update model fields
            self.title = playlist_data["snippet"]["title"]
            self.description = playlist_data["snippet"]["description"]
            self.channel_title = playlist_data["snippet"]["channelTitle"]
            self.thumbnail_url = playlist_data["snippet"]["thumbnails"]["standard"]["url"]
            self.video_count = playlist_data["contentDetails"]["itemCount"]

        except Exception as e:
            raise ValidationError(f"Error fetching playlist data: {str(e)}")

    def save(self, *args, **kwargs):
        if not self.title or not self.video_count:  # Only fetch if data missing
            self.fetch_playlist_data()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "YouTube Playlist"
        verbose_name_plural = "YouTube Playlists"

    def __str__(self):
        return f"{self.title} ({self.mood})"
