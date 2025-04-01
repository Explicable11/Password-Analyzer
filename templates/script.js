// Password visibility toggle
document.querySelector('.toggle-password').addEventListener('click', function() {
    const passwordInput = document.getElementById('password-input');
    const icon = this.querySelector('i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

// Real-time password analysis
document.getElementById('password-input').addEventListener('input', async function() {
    const password = this.value;
    if (!password) {
        resetStrengthIndicator();
        return;
    }

    const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password })
    });

    const result = await response.json();
    updateStrengthIndicator(result);
});

// Password generation
// Simplified password generation function for testing
async function generatePasswords() {
    try {
        console.log("Generating passwords...");
        
        // Make the request to the server
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        });
        
        // Parse the response
        const data = await response.json();
        console.log("Server response:", data);
        
        // Update the UI with the passwords
        if (data.passwords && data.passwords.length > 0) {
            const container = document.querySelector('.generate-content .suggestion-cards');
            
            // Clear previous content
            container.innerHTML = '';
            
            // Add each password card
            data.passwords.forEach(pwd => {
                const card = document.createElement('div');
                card.className = 'suggestion-card';
                card.innerHTML = `
                    <button class="copy-btn" title="Copy password"><i class="far fa-copy"></i></button>
                    <div class="password-text">${pwd.text}</div>
                    <div class="password-meta">
                        <span>Memorability: ${pwd.memorability}</span>
                        <div class="password-score">
                            <span class="score-badge">${Math.floor(pwd.score/10)}/10</span>
                            <span>Strength</span>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
            
            // Add copy functionality
            document.querySelectorAll('.copy-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const passwordText = this.nextElementSibling.textContent;
                    navigator.clipboard.writeText(passwordText);
                    
                    const icon = this.querySelector('i');
                    icon.classList.remove('fa-copy');
                    icon.classList.add('fa-check');
                    
                    setTimeout(() => {
                        icon.classList.remove('fa-check');
                        icon.classList.add('fa-copy');
                    }, 2000);
                });
            });
        } else {
            console.error("No passwords in response");
        }
    } catch (error) {
        console.error('Error generating passwords:', error);
    }
}

function updateSuggestions(passwords) {
    if (!passwords || passwords.length === 0) {
        console.error("No passwords received");
        return;
    }
    
    const container = document.querySelector('.suggestion-cards');
    container.innerHTML = passwords.map(pwd => `
        <div class="suggestion-card">
            <button class="copy-btn" title="Copy password"><i class="far fa-copy"></i></button>
            <div class="password-text">${pwd.text}</div>
            <div class="password-meta">
                <span>Memorability: ${pwd.memorability}</span>
                <div class="password-score">
                    <span class="score-badge">${Math.floor(pwd.score/10)}/10</span>
                    <span>Strength</span>
                </div>
            </div>
        </div>
    `).join('');

    initializeCopyButtons();
}

function initializeCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const passwordText = this.nextElementSibling.textContent;
            navigator.clipboard.writeText(passwordText);
            
            const icon = this.querySelector('i');
            icon.classList.remove('fa-copy');
            icon.classList.add('fa-check');
            
            setTimeout(() => {
                icon.classList.remove('fa-check');
                icon.classList.add('fa-copy');
            }, 2000);
        });
    });
}

// Make sure this is properly set up
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    // Set up the generate button
    const generateBtn = document.querySelector('.generate-btn');
    if (generateBtn) {
        console.log("Generate button found");
        generateBtn.addEventListener('click', function() {
            console.log("Generate button clicked");
            generatePasswords();
        });
    } else {
        console.error("Generate button not found");
    }
    
    // Set up tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const analyzeContent = document.querySelector('.password-form');
    const generateContent = document.querySelector('.generate-content');
    
    if (tabBtns.length && analyzeContent && generateContent) {
        console.log("Tab elements found");
        
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                console.log("Tab clicked:", this.textContent.trim());
                
                // Update active tab
                tabBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                // Show/hide content based on tab
                if (this.textContent.trim() === 'Generate Password') {
                    analyzeContent.style.display = 'none';
                    generateContent.style.display = 'block';
                    generatePasswords(); // Generate passwords when tab is clicked
                } else {
                    analyzeContent.style.display = 'block';
                    generateContent.style.display = 'none';
                }
            });
        });
    } else {
        console.error("Tab elements not found");
    }
});

// Helper functions
function updateStrengthIndicator(result) {
    const meterFill = document.querySelector('.strength-meter-fill');
    const strengthBadge = document.querySelector('.strength-badge');
    const factorsContainer = document.querySelector('.strength-factors');

    meterFill.style.width = `${result.score}%`;
    strengthBadge.textContent = result.strength;

    factorsContainer.innerHTML = result.feedback.map(item => `
        <div class="factor-item">
            <span class="factor-icon ${item.pass ? '' : 'fail'}">
                <i class="fas fa-${item.pass ? 'check' : 'times'}-circle"></i>
            </span>
            <span>${item.message}</span>
        </div>
    `).join('');
}

function resetStrengthIndicator() {
    const meterFill = document.querySelector('.strength-meter-fill');
    const strengthBadge = document.querySelector('.strength-badge');
    const factorsContainer = document.querySelector('.strength-factors');

    meterFill.style.width = '0%';
    strengthBadge.textContent = 'None';
    factorsContainer.innerHTML = '';
}