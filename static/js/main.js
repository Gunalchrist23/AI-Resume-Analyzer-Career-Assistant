// ========================================
// AI Resume Analyzer - Frontend JavaScript
// ========================================

const API_BASE = '';  // Same origin

// ---- Home Page: Resume Upload & Analysis ----

const uploadForm = document.getElementById('uploadForm');
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById('resumeFile');
        const loading = document.getElementById('loadingIndicator');
        const resultDiv = document.getElementById('uploadResult');

        if (!fileInput.files.length) {
            alert('Please select a resume file.');
            return;
        }

        const file = fileInput.files[0];

        // Step 1: Upload and parse the resume
        loading.style.display = 'block';
        resultDiv.style.display = 'none';

        try {
            const formData = new FormData();
            formData.append('file', file);

            const uploadRes = await fetch(`${API_BASE}/upload-resume`, {
                method: 'POST',
                body: formData
            });

            if (!uploadRes.ok) {
                const err = await uploadRes.json();
                throw new Error(err.detail || 'Upload failed.');
            }

            const uploadData = await uploadRes.json();
            const resumeText = uploadData.text;

            // Step 2: Analyze the resume text
            const analyzeRes = await fetch(`${API_BASE}/analyze-resume`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_text: resumeText })
            });

            if (!analyzeRes.ok) {
                const err = await analyzeRes.json();
                throw new Error(err.detail || 'Analysis failed.');
            }

            const analysisData = await analyzeRes.json();

            // Save to localStorage so the Analysis page can read it
            localStorage.setItem('analysisData', JSON.stringify(analysisData));

            loading.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <p style="color: green; font-weight: bold;">&#10003; Analysis complete!</p>
                <p>Name: <strong>${analysisData.details.name || 'N/A'}</strong></p>
                <p>Skills found: <strong>${(analysisData.details.skills || []).length}</strong></p>
                <p>Top match: <strong>${analysisData.recommendations.length ? analysisData.recommendations[0].role + ' (' + analysisData.recommendations[0].match_score + '%)' : 'N/A'}</strong></p>
                <br>
                <a href="/static/analysis.html" class="btn">View Full Analysis</a>
            `;

        } catch (error) {
            loading.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    });
}


// ---- Analysis Page: Display Results ----

function fetchAnalysisResults() {
    const data = localStorage.getItem('analysisData');
    const noDataMsg = document.getElementById('noDataMessage');

    if (!data) {
        // No data available
        if (noDataMsg) noDataMsg.style.display = 'block';
        return;
    }

    const analysisData = JSON.parse(data);
    if (noDataMsg) noDataMsg.style.display = 'none';

    // Show resume details card
    const detailsCard = document.getElementById('resumeDetailsCard');
    if (detailsCard) {
        detailsCard.style.display = 'block';
        document.getElementById('candName').textContent = analysisData.details.name || 'N/A';
        document.getElementById('candEmail').textContent = analysisData.details.email || 'N/A';
        document.getElementById('candPhone').textContent = analysisData.details.phone || 'N/A';

        // Education
        const eduList = document.getElementById('candEducation');
        eduList.innerHTML = '';
        (analysisData.details.education || []).forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            eduList.appendChild(li);
        });

        // Skills
        const skillsDiv = document.getElementById('candSkills');
        skillsDiv.innerHTML = '';
        (analysisData.details.skills || []).forEach(skill => {
            const span = document.createElement('span');
            span.className = 'skill-tag matched-skill';
            span.textContent = skill;
            skillsDiv.appendChild(span);
        });
    }

    // Show recommendations card
    const recsCard = document.getElementById('recommendationsCard');
    if (recsCard && analysisData.recommendations && analysisData.recommendations.length) {
        recsCard.style.display = 'block';
        const container = document.getElementById('rolesContainer');
        container.innerHTML = '';

        analysisData.recommendations.forEach((rec, index) => {
            const roleDiv = document.createElement('div');
            roleDiv.style.marginBottom = '1.5rem';
            roleDiv.style.paddingBottom = '1rem';
            if (index < analysisData.recommendations.length - 1) {
                roleDiv.style.borderBottom = '1px solid #eee';
            }

            // Role title and score
            const title = document.createElement('h3');
            title.innerHTML = `${index + 1}. ${rec.role} <span style="color: ${rec.match_score >= 70 ? '#27ae60' : rec.match_score >= 40 ? '#f39c12' : '#e74c3c'};">(${rec.match_score}%)</span>`;
            roleDiv.appendChild(title);

            // Progress bar
            const barContainer = document.createElement('div');
            barContainer.style.cssText = 'background: #eee; border-radius: 4px; height: 10px; margin: 8px 0;';
            const bar = document.createElement('div');
            bar.style.cssText = `background: ${rec.match_score >= 70 ? '#27ae60' : rec.match_score >= 40 ? '#f39c12' : '#e74c3c'}; height: 100%; border-radius: 4px; width: ${rec.match_score}%;`;
            barContainer.appendChild(bar);
            roleDiv.appendChild(barContainer);

            // Matched Skills
            const matchedLabel = document.createElement('p');
            matchedLabel.innerHTML = '<strong>Matched Skills:</strong>';
            roleDiv.appendChild(matchedLabel);
            rec.matched_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'skill-tag matched-skill';
                span.textContent = skill;
                roleDiv.appendChild(span);
            });

            // Missing Skills
            if (rec.missing_skills.length > 0) {
                const missingLabel = document.createElement('p');
                missingLabel.innerHTML = '<strong style="margin-top: 8px; display: inline-block;">Missing Skills:</strong>';
                roleDiv.appendChild(missingLabel);
                rec.missing_skills.forEach(skill => {
                    const span = document.createElement('span');
                    span.className = 'skill-tag missing-skill';
                    span.textContent = skill;
                    roleDiv.appendChild(span);
                });
            }

            container.appendChild(roleDiv);
        });
    }

    // Show roadmap card
    const roadmapCard = document.getElementById('roadmapCard');
    if (roadmapCard && analysisData.recommendations && analysisData.recommendations.length) {
        roadmapCard.style.display = 'block';
        const topRole = analysisData.recommendations[0].role;
        document.getElementById('roadmapRole').textContent = topRole;

        const loadBtn = document.getElementById('loadRoadmapBtn');
        const roadmapContent = document.getElementById('roadmapContent');

        loadBtn.addEventListener('click', async () => {
            loadBtn.disabled = true;
            loadBtn.textContent = 'Loading...';
            roadmapContent.textContent = 'Generating roadmap using AI...';

            try {
                const res = await fetch(`${API_BASE}/career-roadmap`);
                if (!res.ok) throw new Error('Failed to fetch roadmap.');
                const data = await res.json();
                roadmapContent.textContent = data.roadmap || 'No roadmap available.';
            } catch (err) {
                roadmapContent.textContent = 'Error: ' + err.message;
            } finally {
                loadBtn.disabled = false;
                loadBtn.textContent = 'Generate Detailed Roadmap';
            }
        });
    }
}


// ---- Chat Page: Send Messages ----

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const messagesDiv = document.getElementById('chatMessages');
    const userText = input.value.trim();

    if (!userText) return;

    // Show user message
    const userMsg = document.createElement('div');
    userMsg.className = 'message user-message';
    userMsg.textContent = userText;
    messagesDiv.appendChild(userMsg);
    input.value = '';

    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Show typing indicator
    const typingMsg = document.createElement('div');
    typingMsg.className = 'message bot-message';
    typingMsg.textContent = 'Thinking...';
    messagesDiv.appendChild(typingMsg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userText })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Chat request failed.');
        }

        const data = await res.json();
        typingMsg.textContent = data.response;
    } catch (error) {
        typingMsg.textContent = 'Error: ' + error.message;
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
