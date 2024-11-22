import random

from django.conf import settings
from django.core.cache import cache
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .function import PlaylistService, YouTubeService
from .models import YoutubePlaylist


def playlist_view(request: HttpRequest) -> HttpResponse:
    """Handle playlist listing and filtering."""
    mood = request.GET.get("mood")
    playlists = (
        YoutubePlaylist.objects.filter(mood=mood.lower())
        if mood
        else YoutubePlaylist.objects.all()
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        playlist_data = [PlaylistService.serialize_playlist(p) for p in playlists]
        return JsonResponse({"playlists": playlist_data})

    return render(request, "playlist.html", {"playlists": playlists, "current_mood": mood})


def player_view(request: HttpRequest, playlist_id: str = None) -> HttpResponse:
    """Handle video player and playlist playback with randomized order."""
    try:
        playlist = PlaylistService.get_playlist(
            playlist_id=playlist_id, mood=request.GET.get("mood")
        )

        cache_key = f"playlist_videos_{playlist.playlist_id}_random"
        videos = cache.get(cache_key)

        if not videos:
            youtube_service = YouTubeService(settings.YOUTUBE_API_KEY)
            videos = youtube_service.get_playlist_videos(playlist.playlist_id)
            random.shuffle(videos)
            cache.set(cache_key, videos)
        recommended_playlists = list(PlaylistService.get_recommended_playlists(playlist))
        random.shuffle(recommended_playlists)

        return render(
            request,
            "player.html",
            {
                "playlist": playlist,
                "videos": videos,
                "current_mood": playlist.mood,
                "recommended_playlists": recommended_playlists[:5],
            },
        )

    except Http404 as e:
        return render(request, "error.html", {"error_message": str(e)})
    except Exception as e:
        return render(
            request, "error.html", {"error_message": f"An unexpected error occurred: {str(e)}"}
        )
