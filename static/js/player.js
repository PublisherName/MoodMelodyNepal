let player;
let currentVideoId = null;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('youtubePlayer', {
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    console.log('Player ready');
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        updateActiveVideo(player.getVideoData().video_id);
    } else if (event.data == YT.PlayerState.ENDED) {
        playNextVideo();
    }
}

function playNextVideo() {
    const currentVideo = document.querySelector('.list-group-item.active');
    if (currentVideo) {
        const nextVideo = currentVideo.nextElementSibling;
        if (nextVideo) {
            const nextVideoId = nextVideo.dataset.videoId;
            playVideo(nextVideoId);
        } else {
            const firstVideo = document.querySelector('#videoList .list-group-item:first-child');
            if (firstVideo) {
                const firstVideoId = firstVideo.dataset.videoId;
                playVideo(firstVideoId);
            }
        }
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function playVideo(videoId) {
    if (player && player.loadVideoById) {
        scrollToTop();
        player.loadVideoById(videoId);
        updateActiveVideo(videoId);
    }
}

function updateActiveVideo(videoId) {
    document.querySelectorAll('#videoList .list-group-item').forEach(item => {
        item.classList.remove('active');
    });

    const activeVideo = document.querySelector(`[data-video-id="${videoId}"]`);
    if (activeVideo) {
        activeVideo.classList.add('active');
    }

    currentVideoId = videoId;
}
