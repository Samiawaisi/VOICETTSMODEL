// Main Application Controller
document.addEventListener('DOMContentLoaded', () => {
    // Initialize modules
    VoiceManager.init();
    TTSManager.init();

    // DOM Elements
    const textInput = document.getElementById('textInput');
    const wordCount = document.getElementById('wordCount');
    const charCount = document.getElementById('charCount');
    const chunkInfo = document.getElementById('chunkInfo');
    const chunkText = document.getElementById('chunkText');
    const themeToggle = document.getElementById('themeToggle');
    const historyBtn = document.getElementById('historyBtn');
    const historySection = document.getElementById('historySection');
    const refreshHistory = document.getElementById('refreshHistory');

    // Text input stats
    textInput.addEventListener('input', () => {
        const text = textInput.value;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const chars = text.length;

        wordCount.textContent = `Words: ${words.toLocaleString()}`;
        charCount.textContent = `Characters: ${chars.toLocaleString()}`;

        // Show chunk info for long text
        if (chars > 5000) {
            const numChunks = Math.ceil(chars / 5000);
            chunkInfo.style.display = 'flex';
            chunkText.textContent = `Text will be processed in ${numChunks} chunks for optimal quality`;
        } else {
            chunkInfo.style.display = 'none';
        }
    });

    // Theme Toggle
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle.addEventListener('click', () => {
        const current = document.body.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateThemeIcon(next);
    });

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    // History Toggle
    historyBtn.addEventListener('click', () => {
        const isVisible = historySection.style.display !== 'none';
        historySection.style.display = isVisible ? 'none' : 'block';
        if (!isVisible) {
            TTSManager.loadHistory();
        }
    });

    refreshHistory.addEventListener('click', () => {
        TTSManager.loadHistory();
    });

    // Slider value displays
    const rateSlider = document.getElementById('rateSlider');
    const pitchSlider = document.getElementById('pitchSlider');
    const volumeSlider = document.getElementById('volumeSlider');
    const rateValue = document.getElementById('rateValue');
    const pitchValue = document.getElementById('pitchValue');
    const volumeValue = document.getElementById('volumeValue');

    rateSlider.addEventListener('input', () => {
        const val = rateSlider.value;
        rateValue.textContent = `${val >= 0 ? '+' : ''}${val}%`;
    });

    pitchSlider.addEventListener('input', () => {
        const val = pitchSlider.value;
        pitchValue.textContent = `${val >= 0 ? '+' : ''}${val}Hz`;
    });

    volumeSlider.addEventListener('input', () => {
        const val = volumeSlider.value;
        volumeValue.textContent = `${val >= 0 ? '+' : ''}${val}%`;
    });

    // Generate button
    document.getElementById('generateBtn').addEventListener('click', () => {
        const text = textInput.value.trim();
        if (!text) {
            showNotification('Please enter some text first!', 'warning');
            textInput.focus();
            return;
        }
        TTSManager.generate(text);
    });

    // Keyboard shortcut: Ctrl+Enter to generate
    textInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            document.getElementById('generateBtn').click();
        }
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : type === 'error' ? 'times-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('show'), 10);
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
