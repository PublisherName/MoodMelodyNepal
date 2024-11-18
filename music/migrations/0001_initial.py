# Generated by Django 5.1.3 on 2024-11-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubePlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('playlist_id', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('mood', models.CharField(choices=[('angry', 'Angry'), ('happy', 'Happy'), ('neutral', 'Neutral'), ('sad', 'Sad'), ('surprise', 'Surprise')], default='neutral', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'YouTube Playlist',
                'verbose_name_plural': 'YouTube Playlists',
                'ordering': ['-created_at'],
            },
        ),
    ]