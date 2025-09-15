function appData() {
    return {
        loading: false,
        error: null,
        githubConnected: false,
        userSession: {
            user_id: null,
            session_id: null,
            memory_enabled: false
        },
        memorySummary: {
            preferences: [],
            semantic_memories: [],
            total_memories: 0
        },
        formData: {
            product_name: '',
            product_type: 'SaaS',
            product_description: '',
            target_audience: '',
            launch_date: '',
            additional_notes: '',
            github_repo: '',
            user_id: null,
            session_id: null
        },
        results: {
            analysis: null,
            timeline: null,
            marketing: null,
            research: null
        },

        async init() {
            // Initialize user session and memory
            await this.createUserSession();
            await this.loadMemorySummary();
        },

        async createUserSession() {
            try {
                const response = await fetch('/api/session/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (data.success) {
                    this.userSession = {
                        user_id: data.user_id,
                        session_id: data.session_id,
                        memory_enabled: data.memory_enabled
                    };
                    this.formData.user_id = data.user_id;
                    this.formData.session_id = data.session_id;
                }
            } catch (err) {
                console.error('Error creating user session:', err);
            }
        },

        async loadMemorySummary() {
            if (!this.userSession.user_id) return;

            try {
                const response = await fetch('/api/memory/summary', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: this.userSession.user_id,
                        session_id: this.userSession.session_id
                    })
                });

                const data = await response.json();

                if (data.success) {
                    this.memorySummary = {
                        preferences: data.preferences || [],
                        semantic_memories: data.semantic_memories || [],
                        total_memories: data.total_memories || 0
                    };
                }
            } catch (err) {
                console.error('Error loading memory summary:', err);
            }
        },

        async seedMemory() {
            if (!this.formData.product_name || !this.formData.product_description) {
                this.error = 'Please fill in required fields to seed memory';
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await fetch('/api/memory/seed', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                });

                const data = await response.json();

                if (data.success) {
                    // Update session info if provided
                    if (data.data && data.data.user_id) {
                        this.userSession.user_id = data.data.user_id;
                        this.userSession.session_id = data.data.session_id;
                        this.formData.user_id = data.data.user_id;
                        this.formData.session_id = data.data.session_id;
                    }
                    await this.loadMemorySummary();
                } else {
                    this.error = data.error || 'Failed to seed memory';
                }
            } catch (err) {
                this.error = 'Error seeding memory: ' + err.message;
            } finally {
                this.loading = false;
            }
        },

        async connectGithub() {
            if (!this.formData.github_repo) {
                this.error = 'Please enter a GitHub repository URL';
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await fetch('/api/connect-github', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ github_url: this.formData.github_repo })
                });

                const data = await response.json();

                if (data.success) {
                    this.githubConnected = true;
                    // Show a temporary success message
                    this.error = null;
                } else {
                    this.error = data.message || 'Failed to connect GitHub repository';
                }
            } catch (err) {
                this.error = 'Error connecting to GitHub: ' + err.message;
            } finally {
                this.loading = false;
            }
        },

        async analyzeProduct() {
            if (!this.formData.product_name || !this.formData.product_description) {
                this.error = 'Please fill in required fields (Product Name and Description)';
                return;
            }

            this.loading = true;
            this.error = null;
            this.results.analysis = null;

            try {
                // First seed memory with product information
                await this.seedMemory();

                const response = await fetch('/api/analyze-product', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                });

                const data = await response.json();

                if (data.success) {
                    this.results.analysis = data.response;
                    // Update session info if provided
                    if (data.data && data.data.user_id) {
                        this.userSession.user_id = data.data.user_id;
                        this.userSession.session_id = data.data.session_id;
                        this.formData.user_id = data.data.user_id;
                        this.formData.session_id = data.data.session_id;
                    }
                    // Reload memory summary to show updated context
                    await this.loadMemorySummary();
                } else {
                    this.error = data.error || 'Failed to analyze product';
                }
            } catch (err) {
                this.error = 'Error analyzing product: ' + err.message;
            } finally {
                this.loading = false;
            }

            // Redirect to chat interface with product context
            const productData = encodeURIComponent(JSON.stringify(this.formData));
            window.location.href = `/chat?product=${productData}`;
        },

        async generateTimeline() {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch('/api/generate-timeline', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                });

                const data = await response.json();

                if (data.success) {
                    this.results.timeline = data;
                } else {
                    this.error = data.error || 'Failed to generate timeline';
                }
            } catch (err) {
                this.error = 'Error generating timeline: ' + err.message;
            } finally {
                this.loading = false;
            }
        },

        async generateMarketing() {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch('/api/generate-marketing', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                });

                const data = await response.json();

                if (data.success) {
                    this.results.marketing = data;
                } else {
                    this.error = data.error || 'Failed to generate marketing assets';
                }
            } catch (err) {
                this.error = 'Error generating marketing assets: ' + err.message;
            } finally {
                this.loading = false;
            }
        },

        async researchCompetition() {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch('/api/research-competition', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                });

                const data = await response.json();

                if (data.success) {
                    this.results.research = data;
                } else {
                    this.error = data.error || 'Failed to research competition';
                }
            } catch (err) {
                this.error = 'Error researching competition: ' + err.message;
            } finally {
                this.loading = false;
            }
        },

        formatResponse(text) {
            if (!text) return '';

            // Convert markdown-like formatting to HTML
            return text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n- /g, '<br>• ')
                .replace(/\n\n/g, '<br><br>')
                .replace(/\n/g, '<br>');
        },

        formatTimeline(timelineData) {
            if (!timelineData || !timelineData.timeline) return '';

            let html = `<div class="mb-4">
                <p class="text-sm text-gray-600">
                    <i class="fas fa-calendar mr-1"></i>
                    Launch Date: <strong>${timelineData.launch_date}</strong>
                    (${timelineData.total_days} days from now)
                </p>
            </div>`;

            timelineData.timeline.forEach(phase => {
                html += `<div class="mb-6 border-l-4 border-orange-200 pl-4">
                    <h4 class="font-semibold text-gray-800 mb-2">${phase.phase}</h4>
                    <div class="space-y-2">`;

                phase.tasks.forEach(task => {
                    html += `<div class="bg-gray-50 p-3 rounded">
                        <div class="flex items-start justify-between">
                            <h5 class="font-medium text-gray-700">${task.name}</h5>
                            <span class="text-xs px-2 py-1 bg-${task.priority === 'High' ? 'red' : 'yellow'}-100 text-${task.priority === 'High' ? 'red' : 'yellow'}-800 rounded">
                                ${task.priority}
                            </span>
                        </div>
                        <p class="text-sm text-gray-600 mt-1">
                            <i class="fas fa-clock mr-1"></i>Due: ${task.due_date}
                            <i class="fas fa-hourglass-half ml-3 mr-1"></i>Time: ${task.time_estimate}
                        </p>
                        <p class="text-xs text-gray-500 mt-1">${task.success_criteria}</p>
                    </div>`;
                });

                html += `</div></div>`;
            });

            return html;
        },

        formatMarketing(marketingData) {
            if (!marketingData) return '';

            let html = '';

            if (marketingData.taglines) {
                html += `<div class="mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">
                        <i class="fas fa-tag mr-1"></i>Taglines
                    </h4>
                    <div class="grid gap-2">`;

                marketingData.taglines.forEach(tagline => {
                    html += `<div class="p-3 bg-gray-50 rounded border-l-4 border-orange-200">
                        "${tagline}"
                    </div>`;
                });

                html += `</div></div>`;
            }

            if (marketingData.short_description) {
                html += `<div class="mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">
                        <i class="fas fa-file-alt mr-1"></i>Product Description
                    </h4>
                    <div class="p-4 bg-blue-50 rounded">
                        ${marketingData.short_description}
                    </div>
                </div>`;
            }

            if (marketingData.tweets) {
                html += `<div class="mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">
                        <i class="fab fa-twitter mr-1"></i>Tweet Templates
                    </h4>
                    <div class="space-y-3">`;

                marketingData.tweets.forEach((tweet, index) => {
                    html += `<div class="p-3 bg-blue-50 rounded border-l-4 border-blue-200">
                        <div class="flex items-start">
                            <i class="fab fa-twitter text-blue-500 mr-2 mt-1"></i>
                            <span>${tweet}</span>
                        </div>
                    </div>`;
                });

                html += `</div></div>`;
            }

            return html;
        },

        formatResearch(researchData) {
            if (!researchData) return '';

            let html = '';

            if (researchData.insights) {
                html += `<div class="mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">
                        <i class="fas fa-lightbulb mr-1"></i>Key Insights
                    </h4>
                    <div class="space-y-2">`;

                researchData.insights.forEach(insight => {
                    html += `<div class="flex items-start p-3 bg-green-50 rounded">
                        <i class="fas fa-check-circle text-green-500 mr-2 mt-0.5"></i>
                        <span>${insight}</span>
                    </div>`;
                });

                html += `</div></div>`;
            }

            if (researchData.recommended_hunters) {
                html += `<div class="mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">
                        <i class="fas fa-user-friends mr-1"></i>Recommended Hunters
                    </h4>
                    <div class="grid gap-4">`;

                researchData.recommended_hunters.forEach(hunter => {
                    html += `<div class="p-4 border border-gray-200 rounded-lg">
                        <div class="flex items-center justify-between mb-2">
                            <h5 class="font-medium text-gray-800">${hunter.name}</h5>
                            <span class="text-sm text-gray-500">${hunter.handle}</span>
                        </div>
                        <p class="text-sm text-gray-600 mb-2">${hunter.specialization}</p>
                        <div class="flex items-center justify-between text-xs text-gray-500">
                            <span><i class="fas fa-users mr-1"></i>${hunter.followers}</span>
                            <span><i class="fas fa-star mr-1"></i>${hunter.success_rate}</span>
                        </div>
                        <p class="text-xs text-gray-400 mt-2">${hunter.why_fit}</p>
                    </div>`;
                });

                html += `</div></div>`;
            }

            return html;
        }
    }
}