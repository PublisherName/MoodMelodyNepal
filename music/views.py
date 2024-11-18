# Create your views here.
import random

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import YoutubePlaylist


def playlist_view(request):
    mood = request.GET.get("mood", None)

    # Filter playlists by mood if specified
    if mood:
        playlists = YoutubePlaylist.objects.filter(mood=mood.lower())
    else:
        playlists = YoutubePlaylist.objects.all()

    # Return JSON for AJAX requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        playlist_data = [
            {
                "title": playlist.title,
                "description": playlist.description,
                "playlist_id": playlist.playlist_id,
                "mood": playlist.mood,
                "video_count": playlist.video_count,
            }
            for playlist in playlists
        ]
        return JsonResponse({"playlists": playlist_data})

    # Render template for normal requests
    context = {"playlists": playlists, "current_mood": mood}
    return render(request, "playlist.html", context)


def player_view(request):
    # Get mood and playlist_id from request
    mood = request.GET.get("mood", None)
    playlist_id = request.GET.get("playlist_id", None)

    try:
        if playlist_id:
            # Get specific playlist if ID provided
            playlist = get_object_or_404(YoutubePlaylist, playlist_id=playlist_id)
        elif mood:
            # Get random playlist matching mood
            mood_playlists = YoutubePlaylist.objects.filter(mood=mood.lower())
            if not mood_playlists.exists():
                raise Http404(f"No playlists found for mood: {mood}")
            playlist = random.choice(mood_playlists)
        else:
            # Get random playlist if no mood or ID specified
            playlists = YoutubePlaylist.objects.all()
            if not playlists.exists():
                raise Http404("No playlists available")
            playlist = random.choice(playlists)

        # Get recommended playlists with same mood
        recommended_playlists = YoutubePlaylist.objects.filter(mood=playlist.mood).exclude(
            playlist_id=playlist.playlist_id
        )[:5]

        context = {
            "playlist": playlist,
            "current_mood": playlist.mood,
            "recommended_playlists": recommended_playlists,
        }
        return render(request, "player.html", context)

    except Http404 as e:
        context = {"error_message": str(e)}
        return render(request, "error.html", context)
