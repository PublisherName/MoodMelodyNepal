from django.db import models


class YoutubePlaylist(models.Model):
    MOOD_CHOICES = [
        ("angry", "Angry"),
        ("happy", "Happy"),
        ("neutral", "Neutral"),
        ("sad", "Sad"),
        ("surprise", "Surprise"),
    ]

    title = models.CharField(max_length=200)
    playlist_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default="neutral")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "YouTube Playlist"
        verbose_name_plural = "YouTube Playlists"

    def __str__(self):
        return f"{self.title} ({self.mood})"
