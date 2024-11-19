document.addEventListener('DOMContentLoaded', function () {
    initializeMoodDetection();
});

function initializeMoodDetection() {
    const currentMood = document.getElementById('currentMood').textContent.toLowerCase();
    updateMoodEmoji(currentMood);

    const modal = new bootstrap.Modal(document.getElementById('moodDetectionModal'));
    document.getElementById('detectMoodBtn').addEventListener('click', () => modal.show());

    // Initialize camera controls
    const startCameraBtn = document.getElementById('startCamera');
    const detectEmotionBtn = document.getElementById('detectEmotion');

    startCameraBtn.addEventListener('click', initializeCamera);
    detectEmotionBtn.addEventListener('click', detectMood);
}

async function initializeCamera() {
    try {
        const video = document.getElementById('video');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        document.getElementById('detectEmotion').disabled = false;
        document.getElementById('startCamera').disabled = true;
        updateMoodMessage('Camera started! Click Detect Emotion to analyze your mood.', 'info');
    } catch (error) {
        updateMoodMessage('Failed to access camera. Please allow camera access.', 'danger');
    }
}

async function detectMood() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.remove('d-none');

    try {
        const canvas = document.getElementById('canvas');
        const video = document.getElementById('video');

        // Capture video frame
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);

        const imageData = canvas.toDataURL('image/jpeg');

        // Send to backend
        const response = await fetch('/expression', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image_uri: imageData })
        });

        const data = await response.json();
        handleMoodDetection(data.mood);
    } catch (error) {
        updateMoodMessage('Error detecting mood. Please try again.', 'danger');
    } finally {
        loadingOverlay.classList.add('d-none');
    }
}

function handleMoodDetection(newMood) {
    const currentMood = document.getElementById('currentMood');
    const moodEmoji = document.getElementById('moodEmoji');

    // Animate mood change
    moodEmoji.style.animation = 'none';
    moodEmoji.offsetHeight; // Trigger reflow
    moodEmoji.style.animation = 'moodTransition 0.5s ease-in-out';

    updateMoodEmoji(newMood);
    currentMood.textContent = newMood.charAt(0).toUpperCase() + newMood.slice(1);

    updateMoodMessage(`Mood detected: ${newMood}! Updating playlist...`, 'success');

    // Reload page with new mood after animation
    setTimeout(() => {
        window.location.href = `/player?mood=${newMood.toLowerCase()}`;
    }, 1500);
}

function updateMoodEmoji(mood) {
    const emojis = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'neutral': '😐',
        'surprise': '😲'
    };

    const moodEmoji = document.getElementById('moodEmoji');
    moodEmoji.textContent = emojis[mood] || '😐';
    moodEmoji.dataset.mood = mood;
}

function updateMoodMessage(message, type) {
    const moodMessage = document.getElementById('moodMessage');
    moodMessage.className = `alert alert-${type} mt-3`;
    moodMessage.innerHTML = `<i class="bi bi-${type === 'success' ? 'check' : 'info'}-circle-fill"></i> ${message}`;
}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes moodTransition {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }

    #moodEmoji {
        transition: all 0.3s ease;
    }

    .mood-transition {
        animation: moodTransition 0.5s ease-in-out;
    }
`;
document.head.appendChild(style);
