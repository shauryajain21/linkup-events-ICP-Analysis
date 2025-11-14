// Event ICP Matcher - Frontend JavaScript

// Smooth scroll to form
function scrollToForm() {
    document.getElementById('form-section').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Form submission handler
document.getElementById('analysis-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = this.querySelector('button[type="submit"]');
    const resultsSection = document.getElementById('results-section');

    // Get form data
    const formData = {
        event_url: document.getElementById('event-url').value,
        company_url: document.getElementById('company-url').value,
        company_name: document.getElementById('company-name').value || 'Linkup'
    };

    try {
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        // Hide previous results
        resultsSection.style.display = 'none';

        // Show progress message
        const formInfo = document.querySelector('.form-info span');
        const originalInfoText = formInfo.textContent;
        formInfo.textContent = 'Analyzing... This takes 30-60 seconds. Please wait.';
        formInfo.style.fontWeight = '600';
        formInfo.style.color = 'var(--color-primary)';

        // Make API request with extended timeout (3 minutes)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 180000);

        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Display results
        displayResults(data);

        // Scroll to results
        resultsSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (error) {
        console.error('Error:', error);

        // Show user-friendly error message
        let errorMessage = 'Analysis failed. Please try again.';
        if (error.name === 'AbortError') {
            errorMessage = 'Request timed out after 3 minutes. The event may be too large or the servers may be busy. Please try again.';
        } else if (error.message) {
            errorMessage = error.message;
        }

        alert('Error: ' + errorMessage);

        // Reset progress message
        const formInfo = document.querySelector('.form-info span');
        formInfo.textContent = 'Analysis typically takes 20-40 seconds depending on event size';
        formInfo.style.fontWeight = 'normal';
        formInfo.style.color = 'var(--color-text-secondary)';
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
    }
});

// Display results in the UI
function displayResults(data) {
    const resultsContainer = document.querySelector('.results-container');
    const resultsSection = document.getElementById('results-section');

    const { metadata, step4_matches } = data;
    const { summary, attendees, overall_event_assessment, recommendations } = step4_matches;

    // Build results HTML
    const resultsHTML = `
        <div class="results-header">
            <h2>Event ICP Analysis Results</h2>
            <div class="results-meta">
                ${metadata.event_url ? `
                    <div class="meta-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                            <path d="M10 13C10.4295 13.5741 10.9774 14.0491 11.6066 14.3929C12.2357 14.7367 12.9315 14.9411 13.6467 14.9923C14.3618 15.0435 15.0796 14.9403 15.7513 14.6897C16.4231 14.4392 17.0331 14.047 17.54 13.54L20.54 10.54C21.4508 9.59695 21.9548 8.33394 21.9434 7.02296C21.932 5.71198 21.4061 4.45791 20.4791 3.53087C19.5521 2.60383 18.298 2.07799 16.987 2.0666C15.676 2.0552 14.413 2.55918 13.47 3.46997L11.75 5.17997" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            <path d="M14 11C13.5705 10.4259 13.0226 9.95083 12.3934 9.60707C11.7642 9.26331 11.0685 9.05889 10.3533 9.00768C9.63816 8.95646 8.92037 9.05965 8.24861 9.31023C7.57685 9.5608 6.96684 9.95303 6.45996 10.46L3.45996 13.46C2.54917 14.403 2.04519 15.666 2.05659 16.977C2.06798 18.288 2.59382 19.5421 3.52086 20.4691C4.4479 21.3961 5.70197 21.922 7.01295 21.9334C8.32393 21.9448 9.58694 21.4408 10.53 20.53L12.24 18.82" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        <a href="${metadata.event_url}" target="_blank">${new URL(metadata.event_url).hostname}</a>
                    </div>
                ` : ''}
                <div class="meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                        <path d="M16 2V6M8 2V6M3 10H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    ${new Date(metadata.analysis_date).toLocaleDateString()}
                </div>
                <div class="meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                        <path d="M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    ${summary.total_attendees_analyzed} attendees analyzed
                </div>
            </div>
        </div>

        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-card-value">${summary.high_priority_matches}</div>
                <div class="summary-card-label">High Priority</div>
            </div>
            <div class="summary-card">
                <div class="summary-card-value">${summary.medium_priority_matches}</div>
                <div class="summary-card-label">Medium Priority</div>
            </div>
            <div class="summary-card">
                <div class="summary-card-value">${summary.low_priority_matches}</div>
                <div class="summary-card-label">Low Priority</div>
            </div>
            <div class="summary-card">
                <div class="summary-card-value">${summary.not_a_fit}</div>
                <div class="summary-card-label">Not a Fit</div>
            </div>
        </div>

        ${overall_event_assessment ? `
            <div class="detail-section" style="background-color: var(--color-bg); padding: var(--spacing-lg); border-radius: var(--radius-md); margin-bottom: var(--spacing-xl);">
                <h5>Overall Assessment</h5>
                <p>${overall_event_assessment}</p>
            </div>
        ` : ''}

        ${recommendations && recommendations.length > 0 ? `
            <div class="detail-section" style="background-color: var(--color-bg); padding: var(--spacing-lg); border-radius: var(--radius-md); margin-bottom: var(--spacing-xl);">
                <h5>Recommendations</h5>
                <ul class="talking-points">
                    ${recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        ` : ''}

        <div class="attendees-list">
            <h3>Attendee Analysis</h3>
            ${renderAttendees(attendees)}
        </div>
    `;

    resultsContainer.innerHTML = resultsHTML;
    resultsSection.style.display = 'block';
}

// Render attendees list
function renderAttendees(attendees) {
    // Sort by ICP match score (highest first)
    const sortedAttendees = [...attendees].sort((a, b) =>
        (b.icp_match_score || 0) - (a.icp_match_score || 0)
    );

    return sortedAttendees.map(attendee => {
        const priorityClass = attendee.opportunity_type.toLowerCase().replace(' ', '-');
        const scoreClass = attendee.icp_match_score >= 7 ? 'high' :
                          attendee.icp_match_score >= 5 ? 'medium' : 'low';

        return `
            <div class="attendee-card">
                <div class="attendee-header">
                    <div class="attendee-info">
                        <h4>${attendee.name}</h4>
                        <div class="attendee-role">${attendee.role}</div>
                        <div class="attendee-company">${attendee.company}</div>
                    </div>
                    <div class="score-badge ${scoreClass}">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="currentColor"/>
                        </svg>
                        ${attendee.icp_match_score}/10
                    </div>
                </div>

                <div class="attendee-details">
                    ${attendee.match_reasoning ? `
                        <div class="detail-section">
                            <h5>Why They're a Match</h5>
                            <p>${attendee.match_reasoning}</p>
                        </div>
                    ` : ''}

                    ${attendee.recommended_action ? `
                        <div class="detail-section">
                            <h5>Recommended Action</h5>
                            <p>${attendee.recommended_action}</p>
                        </div>
                    ` : ''}

                    ${attendee.key_talking_points && attendee.key_talking_points.length > 0 ? `
                        <div class="detail-section">
                            <h5>Key Talking Points</h5>
                            <ul class="talking-points">
                                ${attendee.key_talking_points.map(point => `<li>${point}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${renderContactInfo(attendee.contact_info)}
                </div>
            </div>
        `;
    }).join('');
}

// Render contact information
function renderContactInfo(contactInfo) {
    if (!contactInfo) return '';

    const links = [];

    if (contactInfo.linkedin) {
        links.push(`
            <a href="${contactInfo.linkedin}" target="_blank" class="contact-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M16 8C17.5913 8 19.1174 8.63214 20.2426 9.75736C21.3679 10.8826 22 12.4087 22 14V21H18V14C18 13.4696 17.7893 12.9609 17.4142 12.5858C17.0391 12.2107 16.5304 12 16 12C15.4696 12 14.9609 12.2107 14.5858 12.5858C14.2107 12.9609 14 13.4696 14 14V21H10V14C10 12.4087 10.6321 10.8826 11.7574 9.75736C12.8826 8.63214 14.4087 8 16 8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <rect x="2" y="9" width="4" height="12" stroke="currentColor" stroke-width="2"/>
                    <circle cx="4" cy="4" r="2" stroke="currentColor" stroke-width="2"/>
                </svg>
                LinkedIn
            </a>
        `);
    }

    if (contactInfo.email) {
        links.push(`
            <a href="mailto:${contactInfo.email}" class="contact-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                    <path d="M3 7L12 13L21 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Email
            </a>
        `);
    }

    if (contactInfo.twitter) {
        const twitterUrl = contactInfo.twitter.startsWith('http')
            ? contactInfo.twitter
            : `https://twitter.com/${contactInfo.twitter.replace('@', '')}`;
        links.push(`
            <a href="${twitterUrl}" target="_blank" class="contact-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M23 3C22.0424 3.67548 20.9821 4.19211 19.86 4.53C19.2577 3.83751 18.4573 3.34669 17.567 3.12393C16.6767 2.90116 15.7395 2.95718 14.8821 3.28445C14.0247 3.61173 13.2884 4.1944 12.773 4.95372C12.2575 5.71303 11.9877 6.61234 12 7.53V8.53C10.2426 8.57557 8.50127 8.18581 6.93101 7.39545C5.36074 6.60508 4.01032 5.43864 3 4C3 4 -1 13 8 17C5.94053 18.398 3.48716 19.0989 1 19C10 24 21 19 21 7.5C20.9991 7.22145 20.9723 6.94359 20.92 6.67C21.9406 5.66349 22.6608 4.39271 23 3V3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Twitter
            </a>
        `);
    }

    if (links.length === 0) return '';

    return `
        <div class="detail-section">
            <h5>Contact</h5>
            <div class="contact-links">
                ${links.join('')}
            </div>
        </div>
    `;
}

// Check API health on page load
window.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/api/health');
        const health = await response.json();

        if (!health.linkup_configured || !health.openai_configured) {
            console.warn('API not fully configured. Check your .env file.');
        }
    } catch (error) {
        console.error('Could not check API health:', error);
    }
});
