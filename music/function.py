import random
from typing import Dict, List, Optional

from django.http import Http404
from django.shortcuts import get_object_or_404
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import YoutubePlaylist

# Constants
YOUTUBE_API_VERSION = "v3"
MAX_RESULTS = 50
MAX_RECOMMENDATIONS = 5
THUMBNAIL_QUALITIES = ["standard", "high", "medium", "default"]
DEFAULT_THUMBNAIL = "https://placehold.co/120x68?text=No+Thumbnail"


class YouTubeAPIError(Exception):
    """Custom exception for YouTube API errors."""

    pass


class YouTubeService:
    """Handle YouTube API interactions."""

    def __init__(self, api_key: str):
        self.youtube = build("youtube", YOUTUBE_API_VERSION, developerKey=api_key)

    def get_playlist_videos(self, playlist_id: str) -> List[Dict]:
        """Fetch all videos from a playlist."""
        videos = []
        next_page_token = None

        while True:
            try:
                response = (
                    self.youtube.playlistItems()
                    .list(
                        part="snippet,contentDetails",
                        playlistId=playlist_id,
                        maxResults=MAX_RESULTS,
                        pageToken=next_page_token,
                    )
                    .execute()
                )

                videos.extend(self._process_playlist_items(response.get("items", [])))

                if not (next_page_token := response.get("nextPageToken")):
                    break

            except HttpError as e:
                raise YouTubeAPIError(f"Failed to fetch playlist videos: {str(e)}")

        return videos

    def _process_playlist_items(self, items: List[Dict]) -> List[Dict]:
        """Process raw playlist items into video objects."""
        return [self._create_video_object(item) for item in items]

    def _create_video_object(self, item: Dict) -> Dict:
        """Create a video object from a playlist item."""
        snippet = item.get("snippet", {})
        content_details = item.get("contentDetails", {})

        return {
            "title": snippet.get("title", "Untitled Video"),
            "video_id": content_details.get("videoId", ""),
            "thumbnail": self._get_best_thumbnail(snippet.get("thumbnails", {})),
            "position": snippet.get("position", 0),
        }

    @staticmethod
    def _get_best_thumbnail(thumbnails: Dict) -> str:
        """Get best available thumbnail URL."""
        for quality in THUMBNAIL_QUALITIES:
            if url := thumbnails.get(quality, {}).get("url"):
                return url
        return DEFAULT_THUMBNAIL


class PlaylistService:
    """Handle playlist-related operations."""

    @staticmethod
    def get_playlist(playlist_id: Optional[str], mood: Optional[str]) -> YoutubePlaylist:
        """Get playlist based on ID or mood."""
        if playlist_id:
            return get_object_or_404(YoutubePlaylist, playlist_id=playlist_id)

        queryset = (
            YoutubePlaylist.objects.filter(mood=mood.lower())
            if mood
            else YoutubePlaylist.objects.all()
        )

        if not queryset.exists():
            raise Http404(f"No playlists found{f' for mood: {mood}' if mood else ''}")

        return random.choice(queryset)

    @staticmethod
    def get_recommended_playlists(playlist: YoutubePlaylist) -> List[YoutubePlaylist]:
        """Get recommended playlists with same mood."""
        return YoutubePlaylist.objects.filter(mood=playlist.mood).exclude(
            playlist_id=playlist.playlist_id
        )[:MAX_RECOMMENDATIONS]

    @staticmethod
    def serialize_playlist(playlist: YoutubePlaylist) -> Dict:
        """Serialize playlist for JSON response."""
        return {
            "title": playlist.title,
            "description": playlist.description,
            "playlist_id": playlist.playlist_id,
            "mood": playlist.mood,
            "video_count": playlist.video_count,
        }
