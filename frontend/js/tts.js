// TTS Manager - Handles text-to-speech generation
const TTSManager = {
    currentFile: null,

    init() {
        console.log('TTS Manager initialized');
    },

    async generate(text) {
        const generateBtn = document.getElementById('generateBtn');
        const progressSection = document.getElementById('progressSection');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const playerSection = document.getElementById('playerSection');
        const audioPlayer = document.getElementById('audioPlayer');
        const downloadBtn = document.getElementById('downloadBtn');

        // Get settings
        const engine = document.getElementById('engineSelect') ? document.getElementById('engineSelect').value : 'edge';
        const voice = document.getElementById('voiceSelect').value;
        const rate = `${document.getElementById('rateSlider').value >= 0 ? '+' : ''}${document.getElementById('rateSlider').value}%`;
        const pitch = `${document.getElementById('pitchSlider').value >= 0 ? '+' : ''}${document.getElementById('pitchSlider').value}Hz`;
        const volume = `${document.getElementById('volumeSlider').value >= 0 ? '+' : ''}${document.getElementById('volumeSlider').value}%`;
        const outputFormat = document.getElementById('formatSelect').value;

        if (!voice) {
            showNotification('Please select a voice first!', 'warning');
            return;
        }

        // Show progress
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Generating...</span>';
        progressSection.style.display = 'block';
        playerSection.style.display = 'none';
        progressFill.style.width = '0%';
        progressText.textContent = 'Sending request...';

        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressFill.style.width = `${progress}%`;
            if (progress > 30) progressText.textContent = `Processing with ${engine === 'google' ? 'Google TTS' : 'Microsoft Edge TTS'}...`;
            if (progress > 60) progressText.textContent = 'Generating audio...';
        }, 500);

        try {
            const response = await fetch('/api/tts/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text,
                    voice,
                    engine,
                    rate,
                    pitch,
                    volume,
                    output_format: outputFormat
                })
            });

            clearInterval(progressInterval);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Generation failed');
            }

            const result = await response.json();
            this.currentFile = result;

            // Complete progress
            progressFill.style.width = '100%';
            progressText.textContent = 'Audio generated successfully!';

            setTimeout(() => {
                progressSection.style.display = 'none';

                // Show player
                playerSection.style.display = 'block';
                audioPlayer.src = result.download_url;
                audioPlayer.load();

                downloadBtn.onclick = () => {
                    const link = document.createElement('a');
                    link.href = `/api/tts/download/${result.filename}`;
                    link.download = result.filename;
                    link.click();
                };

                const formatLabel = outputFormat.toUpperCase();
                downloadBtn.innerHTML = `<i class="fas fa-download"></i> Download ${formatLabel}`;

                showNotification(
                    `Audio generated! ${result.chunks_used > 1 ? `(${result.chunks_used} chunks merged)` : ''}`,
                    'success'
                );
            }, 500);

        } catch (error) {
            clearInterval(progressInterval);
            progressSection.style.display = 'none';
            showNotification(`Error: ${error.message}`, 'error');
            console.error('TTS Generation error:', error);
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-play"></i> <span>Generate Speech</span>';
        }
    },

    async loadHistory() {
        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '<p class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</p>';

        try {
            const response = await fetch('/api/tts/history');
            const data = await response.json();

            if (data.files.length === 0) {
                historyList.innerHTML = '<p class="empty-state">No audio files generated yet.</p>';
                return;
            }

            historyList.innerHTML = data.files.map(file => `
                <div class="history-item">
                    <div class="history-info">
                        <i class="fas fa-file-audio"></i>
                        <span class="history-name">${file.filename}</span>
                        <span class="history-size">${(file.size / 1024).toFixed(1)} KB</span>
                    </div>
                    <div class="history-actions">
                        <button class="btn-icon-small" onclick="TTSManager.playHistoryItem('${file.filename}')" title="Play">
                            <i class="fas fa-play"></i>
                        </button>
                        <a href="/api/tts/download/${file.filename}" download class="btn-icon-small" title="Download">
                            <i class="fas fa-download"></i>
                        </a>
                        <button class="btn-icon-small btn-danger" onclick="TTSManager.deleteHistoryItem('${file.filename}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            historyList.innerHTML = '<p class="empty-state">Failed to load history.</p>';
        }
    },

    playHistoryItem(filename) {
        const audioPlayer = document.getElementById('audioPlayer');
        const playerSection = document.getElementById('playerSection');
        playerSection.style.display = 'block';
        audioPlayer.src = `/output/${filename}`;
        audioPlayer.play();
    },

    async deleteHistoryItem(filename) {
        if (!confirm('Delete this audio file?')) return;
        try {
            await fetch(`/api/tts/history/${filename}`, { method: 'DELETE' });
            this.loadHistory();
            showNotification('File deleted', 'success');
        } catch (error) {
            showNotification('Failed to delete file', 'error');
        }
    }
};
