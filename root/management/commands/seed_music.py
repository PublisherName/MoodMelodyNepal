import json
from pathlib import Path

from django.core.management.base import BaseCommand

from music.models import YoutubePlaylist


class Command(BaseCommand):
    help = "Seed the database with music data from music.json"

    def handle(self, *args, **kwargs):
        file_path = Path(__file__).resolve().parent.parent.parent.parent / "seeds" / "music.json"
        with open(file_path) as file:
            data = json.load(file)
            for item in data:
                model = item["model"]
                if model == "music.youtubeplaylist":
                    fields = item["fields"]
                    YoutubePlaylist.objects.update_or_create(pk=item["pk"], defaults=fields)
        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
