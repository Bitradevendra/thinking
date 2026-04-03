// Global state
let currentSessionId = null;
let uploadedFiles = [];
let progressInterval = null;

// DOM elements
const inputSection = document.getElementById('input-section');
const progressSection = document.getElementById('progress-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');

const problemInput = document.getElementById('problem-input');
const fileUpload = document.getElementById('file-upload');
const fileList = document.getElementById('file-list');
const iterationsInput = document.getElementById('iterations');
const timeEstimate = document.getElementById('time-estimate');
const startBtn = document.getElementById('start-btn');

const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const statusMessage = document.getElementById('status-message');

const toggleAdvanced = document.getElementById('toggle-advanced');
const advancedSettings = document.getElementById('advanced-settings');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateTimeEstimate();
});

function setupEventListeners() {
    startBtn.addEventListener('click', startReasoning);
    fileUpload.addEventListener('change', handleFileUpload);
    iterationsInput.addEventListener('input', updateTimeEstimate);

    toggleAdvanced.addEventListener('click', () => {
        const isHidden = advancedSettings.style.display === 'none';
        advancedSettings.style.display = isHidden ? 'block' : 'none';
        toggleAdvanced.textContent = isHidden ? 'Hide Advanced Settings' : 'Show Advanced Settings';
    });

    document.getElementById('new-problem-btn')?.addEventListener('click', resetUI);
    document.getElementById('retry-btn')?.addEventListener('click', resetUI);
    document.getElementById('view-logs-btn')?.addEventListener('click', toggleLogFiles);
}

function updateTimeEstimate() {
    const iterations = parseInt(iterationsInput.value) || 1800;  // Default to 1800 for deep thinking
    const seconds = Math.round(iterations / 2);  // ~2 iterations per second
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
        if (remainingSeconds > 0) {
            timeEstimate.value = `~${minutes}m ${remainingSeconds}s`;
        } else {
            timeEstimate.value = `~${minutes} minutes`;
        }
    } else {
        timeEstimate.value = `~${seconds}s`;
    }
}

async function handleFileUpload(event) {
    const files = Array.from(event.target.files);

    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                uploadedFiles.push(data.filename);
                addFileToList(data.filename, data.size);
            } else {
                showError('Failed to upload file: ' + file.name);
            }
        } catch (error) {
            showError('Error uploading file: ' + error.message);
        }
    }
}

function addFileToList(filename, size) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.innerHTML = `
        <span class="file-name">📄 ${filename}</span>
        <span class="file-size">${formatFileSize(size)}</span>
        <button class="file-remove" onclick="removeFile('${filename}')">✕</button>
    `;
    fileList.appendChild(fileItem);
}

function removeFile(filename) {
    uploadedFiles = uploadedFiles.filter(f => f !== filename);
    updateFileList();
}

function updateFileList() {
    fileList.innerHTML = '';
    uploadedFiles.forEach(filename => {
        addFileToList(filename, 0);
    });
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

async function startReasoning() {
    const problem = problemInput.value.trim();

    if (!problem) {
        showError('Please enter a problem to solve');
        return;
    }

    const iterations = parseInt(iterationsInput.value) || 50;

    // Show progress section
    inputSection.style.display = 'none';
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                problem: problem,
                max_iterations: iterations,
                files: uploadedFiles
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to start reasoning session');
        }

        const data = await response.json();
        currentSessionId = data.session_id;
        console.log('Session started:', currentSessionId);

        // Start polling for progress
        startProgressPolling();

    } catch (error) {
        showError('Error starting reasoning: ' + error.message);
    }
}

function startProgressPolling() {
    if (progressInterval) {
        clearInterval(progressInterval);
    }

    progressInterval = setInterval(async () => {
        if (!currentSessionId) return;

        try {
            const response = await fetch(`/api/progress/${currentSessionId}`);
            const data = await response.json();

            // Check for errors
            if (!response.ok || data.error) {
                console.error('Progress error:', data);
                clearInterval(progressInterval);
                showError(data.error || 'Session not found');
                return;
            }

            // Update progress if available
            if (data.progress) {
                updateProgress(data.progress);

                if (data.progress.status === 'completed' && data.result) {
                    clearInterval(progressInterval);
                    showResults(data.result);
                } else if (data.progress.status === 'error') {
                    clearInterval(progressInterval);
                    showError(data.error || 'An error occurred during reasoning');
                }
            }

        } catch (error) {
            console.error('Error fetching progress:', error);
            // Don't stop polling on network errors, might be temporary
        }
    }, 1000); // Poll every second
}

function updateProgress(progress) {
    // Safety check
    if (!progress) {
        console.warn('Progress data is undefined');
        return;
    }

    const percentage = progress.percentage || 0;

    progressFill.style.width = percentage + '%';
    progressText.textContent = percentage + '%';

    document.getElementById('stat-iterations').textContent =
        `${progress.current_iteration || 0} / ${progress.total_iterations || 0}`;
    document.getElementById('stat-nodes').textContent = progress.nodes_explored || 0;
    document.getElementById('stat-elapsed').textContent = formatTime(progress.elapsed_time || 0);
    document.getElementById('stat-remaining').textContent =
        (progress.estimated_remaining && progress.estimated_remaining > 0) ?
            formatTime(progress.estimated_remaining) : '-';

    // Update status message
    if (progress.status === 'running') {
        const messages = [
            'Exploring solution branches...',
            'Verifying mathematical expressions...',
            'Scoring solution paths...',
            'Pruning low-quality branches...',
            'Expanding promising approaches...',
            'Running CAS verification...',
            'Evaluating solution quality...'
        ];
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        statusMessage.textContent = randomMessage;
    } else if (progress.status === 'error') {
        statusMessage.textContent = 'Error occurred...';
        statusMessage.style.color = '#ef4444';
    } else {
        statusMessage.textContent = 'Initializing...';
        statusMessage.style.color = '';
    }
}

function formatTime(seconds) {
    if (seconds < 60) {
        return seconds + 's';
    }
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
}

function showResults(result) {
    progressSection.style.display = 'none';
    resultsSection.style.display = 'block';

    document.getElementById('result-score').textContent = result.best_score.toFixed(2);
    document.getElementById('result-time').textContent = formatTime(Math.round(result.elapsed_time));
    document.getElementById('result-nodes').textContent = result.stats.total_nodes;
    document.getElementById('result-text').textContent = result.solution;

    // Setup log links
    const logLinks = document.getElementById('log-links');
    logLinks.innerHTML = `
        <p><strong>Session Directory:</strong> ${result.session_dir}</p>
        <ul>
            <li>📄 final_result.txt - Best solution</li>
            <li>📄 summary.txt - Session summary</li>
            <li>📄 thought_tree.json - Complete reasoning tree</li>
            <li>📄 api_responses.log - All API calls</li>
            <li>📄 cas_computations.log - Math verifications</li>
        </ul>
    `;
}

function toggleLogFiles() {
    const logFiles = document.getElementById('log-files');
    const btn = document.getElementById('view-logs-btn');

    if (logFiles.style.display === 'none') {
        logFiles.style.display = 'block';
        btn.textContent = '📁 Hide Log Files';
    } else {
        logFiles.style.display = 'none';
        btn.textContent = '📁 View Log Files';
    }
}

function showError(message) {
    inputSection.style.display = 'none';
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'block';

    document.getElementById('error-message').textContent = message;
}

function resetUI() {
    inputSection.style.display = 'block';
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }

    currentSessionId = null;
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
}
