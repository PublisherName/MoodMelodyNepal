// static/js/emotion-detection.js

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const startButton = document.getElementById('startCamera');
    const detectButton = document.getElementById('detectEmotion');
    const moodDisplay = document.getElementById('moodDisplay');
    let stream = null;
    let detectionInterval = null;
    const DETECTION_DELAY = 2000;

    detectButton.disabled = true;

    async function detectEmotion() {
        if (!stream) {
            console.warn('Camera not started');
            detectButton.disabled = true;
            return;
        }

        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);

        const imageData = canvas.toDataURL('image/jpeg');

        try {
            const response = await fetch('/expression', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image_uri: imageData })
            });

            const data = await response.json();
            updateMoodDisplay(data.mood);
        } catch (err) {
            console.error('Error detecting emotion:', err);
            stopDetection();
        }
    }

    function startDetection() {
        if (!stream) {
            console.warn('Cannot start detection without camera');
            return;
        }
        detectButton.textContent = 'Stop Detection';
        detectButton.classList.replace('btn-success', 'btn-danger');
        detectionInterval = setInterval(detectEmotion, DETECTION_DELAY);
    }

    function stopDetection() {
        if (detectionInterval) {
            clearInterval(detectionInterval);
            detectionInterval = null;
        }
        detectButton.textContent = 'Start Detection';
        detectButton.classList.replace('btn-danger', 'btn-success');
    }

    startButton.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: 640,
                    height: 480,
                    facingMode: 'user'
                }
            });
            video.srcObject = stream;
            startButton.disabled = true;
            detectButton.disabled = false;
            startDetection();
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Could not access camera');
            detectButton.disabled = true;
        }
    });

    detectButton.addEventListener('click', () => {
        if (detectionInterval) {
            stopDetection();
        } else {
            startDetection();
        }
    });

    function updateMoodDisplay(mood) {
        const moodEmojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'surprise': '😲',
            'neutral': '😐'
        };

        const detectedMood = document.getElementById('detectedMood');
        if (detectedMood) {
            detectedMood.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
        }
        if (moodDisplay) {
            moodDisplay.style.transform = 'scale(1.2)';
            moodDisplay.textContent = moodEmojis[mood] || '😐';
            setTimeout(() => {
                moodDisplay.style.transform = 'scale(1)';
            }, 200);
        }
    }

    window.addEventListener('beforeunload', () => {
        stopDetection();
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });
});
