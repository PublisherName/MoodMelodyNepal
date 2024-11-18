// static/js/emotion-detection.js

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const startButton = document.getElementById('startCamera');
    const detectButton = document.getElementById('detectEmotion');
    const moodDisplay = document.getElementById('moodDisplay');
    let stream = null;

    // Start camera
    startButton.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            startButton.disabled = true;
            detectButton.disabled = false;
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Could not access camera');
        }
    });

    // Capture and detect emotion
    detectButton.addEventListener('click', async () => {
        if (!stream) return;

        // Capture frame from video
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);

        // Convert to base64
        const imageData = canvas.toDataURL('image/jpeg');

        try {
            // Send to backend
            const response = await fetch('/expression', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image_uri: imageData })
            });

            const data = await response.json();

            // Update UI with detected emotion
            updateMoodDisplay(data.mood);

        } catch (err) {
            console.error('Error detecting emotion:', err);
            alert('Failed to detect emotion');
        }
    });

    // Update mood display
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
            moodDisplay.textContent = moodEmojis[mood] || '😐';
        }
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });
});
