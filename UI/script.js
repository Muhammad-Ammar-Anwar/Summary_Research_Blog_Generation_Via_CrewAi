// Theme Toggle
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = themeToggle.querySelector('.theme-icon');
        const themeLabel = themeToggle.querySelector('.theme-label');
        const body = document.body;

        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        body.setAttribute('data-theme', savedTheme);
        updateThemeToggle(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeToggle(newTheme);
        });

        function updateThemeToggle(theme) {
            if (theme === 'dark') {
                themeIcon.textContent = '🌙';
                themeLabel.textContent = 'Dark Mode';
            } else {
                themeIcon.textContent = '☀️';
                themeLabel.textContent = 'Light Mode';
            }
        }

        // API Configuration
        const API_BASE_URL = 'https://ammaranwar-blog-crewai.hf.space';

        // DOM Elements
        let selectedAction = null;
        const actionCards = document.querySelectorAll('.action-card');
        const urlInput = document.getElementById('urlInput');
        const generateBtn = document.getElementById('generateBtn');
        const loading = document.getElementById('loading');
        const responseSection = document.getElementById('responseSection');
        const responseTitle = document.getElementById('responseTitle');
        const responseContent = document.getElementById('responseContent');
        const copyBtn = document.getElementById('copyBtn');
        const toast = document.getElementById('toast');

        // Action card selection
        actionCards.forEach(card => {
            card.addEventListener('click', () => {
                actionCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedAction = card.dataset.action;
                updateGenerateButton();
            });
        });

        // URL input validation
        urlInput.addEventListener('input', updateGenerateButton);

        function updateGenerateButton() {
            const hasUrl = urlInput.value.trim().length > 0;
            const hasAction = selectedAction !== null;
            generateBtn.disabled = !(hasUrl && hasAction);
        }

        // Generate button click
        generateBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const url = urlInput.value.trim();

            if (!url || !selectedAction) {
                showToast('Please enter a URL and select an action');
                return;
            }

            // Validate YouTube URL
            if (!isValidYouTubeUrl(url)) {
                showToast('Please enter a valid YouTube URL');
                return;
            }

            await processContent(url, selectedAction);
        });

        // Process content
        async function processContent(url, action) {
            // Show loading state
            loading.classList.add('active');
            responseSection.classList.remove('active');
            generateBtn.disabled = true;

            try {
                // Determine endpoint based on action
                let endpoint;
                if (action === 'blog') {
                    endpoint = '/blog_writter';
                } else if (action === 'summary') {
                    endpoint = '/Summary';
                } else if (action === 'research') {
                    endpoint = '/Research';
                }

                const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ topic: url })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                if (data.final_answer) {
                    displayStructuredResponse(data);
                }
                else {
                    showToast("No result returned from server");
                }

            } catch (error) {
                console.error('Error:', error);
                showToast(error.message || 'An error occurred while processing. Please try again.');
            } finally {
                loading.classList.remove('active');
                generateBtn.disabled = false;
            }
        }

        // Display structured response
        function displayStructuredResponse(data) {
            // Create agent header with icon
            const agentHeader = `
                <div class="agent-header">
                    <div class="agent-icon">🤖</div>
                    <h2 class="agent-name">${data.agent}</h2>
                </div>
            `;

            // Format task with proper structure
            const formattedTask = `
                <div class="task-section">
                    <h3 class="section-title">📌 Task</h3>
                    <div class="task-content">${formatTaskContent(data.task)}</div>
                </div>
            `;

            // Format final answer
            const formattedAnswer = `
                <div class="answer-section">
                    <h3 class="section-title">✅ Final Answer</h3>
                    <div class="answer-content">${formatResponse(data.final_answer)}</div>
                </div>
            `;

            responseContent.innerHTML = agentHeader + formattedTask + formattedAnswer;

            responseSection.classList.add('active');
            responseSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Format task content with structure
        function formatTaskContent(task) {
            // Split task by numbered steps
            const lines = task.split('\n').filter(line => line.trim());
            let html = '<ol class="task-list">';
            
            lines.forEach(line => {
                line = line.trim();
                // Remove leading numbers and dots if present
                const cleanLine = line.replace(/^\d+\.\s*/, '');
                if (cleanLine) {
                    html += `<li>${cleanLine}</li>`;
                }
            });
            
            html += '</ol>';
            return html;
        }

        // Format response to HTML
        function formatResponse(text) {
            // Split into lines
            let lines = text.split('\n');
            let html = '';
            let inList = false;

            lines.forEach(line => {
                line = line.trim();

                if (!line) {
                    if (inList) {
                        html += '</ul>';
                        inList = false;
                    }
                    return;
                }

                // Headers
                if (line.startsWith('# ')) {
                    if (inList) {
                        html += '</ul>';
                        inList = false;
                    }
                    html += `<h1>${line.substring(2)}</h1>`;
                } else if (line.startsWith('## ')) {
                    if (inList) {
                        html += '</ul>';
                        inList = false;
                    }
                    html += `<h2>${line.substring(3)}</h2>`;
                } else if (line.startsWith('### ')) {
                    if (inList) {
                        html += '</ul>';
                        inList = false;
                    }
                    html += `<h3>${line.substring(4)}</h3>`;
                }
                // List items
                else if (line.startsWith('- ') || line.startsWith('* ')) {
                    if (!inList) {
                        html += '<ul>';
                        inList = true;
                    }
                    html += `<li>${line.substring(2)}</li>`;
                }
                // Numbered lists
                else if (/^\d+\.\s/.test(line)) {
                    if (inList && html.includes('<ul>')) {
                        html += '</ul>';
                    }
                    if (!inList || !html.includes('<ol>')) {
                        if (inList) html += '</ul>';
                        html += '<ol>';
                        inList = true;
                    }
                    html += `<li>${line.replace(/^\d+\.\s/, '')}</li>`;
                }
                // Bold text
                else if (line.includes('**')) {
                    if (inList) {
                        html += inList && html.includes('<ul>') ? '</ul>' : '</ol>';
                        inList = false;
                    }
                    const formatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    html += `<p>${formatted}</p>`;
                }
                // Regular paragraphs
                else {
                    if (inList) {
                        html += inList && html.includes('<ul>') ? '</ul>' : '</ol>';
                        inList = false;
                    }
                    html += `<p>${line}</p>`;
                }
            });

            if (inList) {
                html += inList && html.includes('<ul>') ? '</ul>' : '</ol>';
            }

            return html || `<p>${text}</p>`;
        }

        // Copy to clipboard
        copyBtn.addEventListener('click', () => {
            const textContent = responseContent.innerText;
            navigator.clipboard.writeText(textContent).then(() => {
                showToast('Copied to clipboard!');
            }).catch(err => {
                showToast('Failed to copy');
                console.error('Copy failed:', err);
            });
        });

        // Toast notification
        function showToast(message) {
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        // Validate YouTube URL
        function isValidYouTubeUrl(url) {
            const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
            return pattern.test(url);
        }


