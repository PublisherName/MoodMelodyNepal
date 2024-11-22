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

function onPlayerReady() {
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
    ensurePlayerInitialized(() => {
        try {
            if (player && typeof player.loadVideoById === 'function') {
                scrollToTop();
                player.loadVideoById(videoId);
                updateActiveVideo(videoId);
                player.playVideo();
            } else {
                throw new Error('Player is not initialized or loadVideoById method is not available.');
            }
        } catch (error) {
            console.error('Error playing video:', error);
        }
    });
}

function updateActiveVideo(videoId) {
    document.querySelectorAll('#videoList .list-group-item').forEach(item => {
        item.classList.remove('active');
    });

    const activeVideo = document.querySelector(`[data-video-id="${videoId}"]`);
    if (activeVideo) {
        activeVideo.classList.add('active');
    } else {
        console.warn(`No video found with videoId: ${videoId}`);
    }
    currentVideoId = videoId;
}

function ensurePlayerInitialized(callback) {
    if (player && typeof player.loadVideoById === 'function') {
        callback();
    } else {
        console.warn('Player is not initialized. Initializing now...');
        onYouTubeIframeAPIReady();
        const checkPlayerInitialized = setInterval(() => {
            if (player && typeof player.loadVideoById === 'function') {
                clearInterval(checkPlayerInitialized);
                callback();
            } else {
                console.warn('Waiting for player to be initialized...');
            }
        }, 100);
    }
}

window.onbeforeunload = () => {
    player = null;
    currentVideoId = null;
};

/* For Playlist Description */
function showMore() {
    document.getElementById('short-description').style.display = 'none';
    document.getElementById('full-description').style.display = 'block';
}

function showLess() {
    document.getElementById('short-description').style.display = 'block';
    document.getElementById('full-description').style.display = 'none';
}
/* End For Playlist Description */
