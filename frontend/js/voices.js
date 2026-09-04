// Voice Manager - Handles voice loading, character names, and engine filtering
const VoiceManager = {
    allVoices: [],
    filteredVoices: [],

    async init() {
        console.log('Voice Manager initializing...');
        await this.loadVoices();
        this.setupFilters();
    },

    async loadVoices() {
        const voiceSelect = document.getElementById('voiceSelect');
        const languageSelect = document.getElementById('languageSelect');
        const engineSelect = document.getElementById('engineSelect');
        const currentEngine = engineSelect ? engineSelect.value : 'edge';

        try {
            voiceSelect.innerHTML = '<option value="">Loading voices...</option>';
            const response = await fetch(`/api/voices/?engine=${currentEngine}`);
            const data = await response.json();
            this.allVoices = data.voices;
            this.filteredVoices = [...this.allVoices];

            // Populate language dropdown
            const languages = [...new Set(this.allVoices.map(v => v.Locale || ''))].filter(Boolean).sort();

            languageSelect.innerHTML = '<option value="">All Languages</option>' +
                languages.map(lang => `<option value="${lang}">${lang}</option>`).join('');

            // Populate voice dropdown
            this.updateVoiceDropdown();

            console.log(`Loaded ${this.allVoices.length} voices for engine: ${currentEngine}`);
        } catch (error) {
            console.error('Failed to load voices:', error);
            voiceSelect.innerHTML = '<option value="">Failed to load voices</option>';
            showNotification('Failed to load voices. Is the server running?', 'error');
        }
    },

    setupFilters() {
        const engineSelect = document.getElementById('engineSelect');
        const languageSelect = document.getElementById('languageSelect');
        const genderSelect = document.getElementById('genderSelect');

        if (engineSelect) {
            engineSelect.addEventListener('change', () => this.loadVoices());
        }
        languageSelect.addEventListener('change', () => this.applyFilters());
        genderSelect.addEventListener('change', () => this.applyFilters());
    },

    applyFilters() {
        const language = document.getElementById('languageSelect').value;
        const gender = document.getElementById('genderSelect').value;

        this.filteredVoices = this.allVoices.filter(v => {
            let match = true;
            if (language) {
                match = match && (v.Locale || '').toLowerCase().startsWith(language.toLowerCase());
            }
            if (gender) {
                match = match && (v.Gender || '').toLowerCase() === gender.toLowerCase();
            }
            return match;
        });

        this.updateVoiceDropdown();
    },

    updateVoiceDropdown() {
        const voiceSelect = document.getElementById('voiceSelect');
        const voices = this.filteredVoices;

        if (voices.length === 0) {
            voiceSelect.innerHTML = '<option value="">No voices found</option>';
            return;
        }

        voiceSelect.innerHTML = voices.map(v => {
            const label = v.DisplayName || `${v.CharacterName || v.ShortName} (${v.Locale})`;
            return `<option value="${v.ShortName}">${label}</option>`;
        }).join('');

        // Default voice selection
        const defaultVoice = voices.find(v => v.ShortName === 'en-US-AriaNeural') || voices[0];
        if (defaultVoice) {
            voiceSelect.value = defaultVoice.ShortName;
        }
    }
};
