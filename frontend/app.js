let token = null;

// Auth functions
function showRegister() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
}

function showLogin() {
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
}

async function register() {
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    
    try {
        const response = await fetch('http://localhost:8000/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            showDashboard();
        }
    } catch (error) {
        console.error('Registration failed:', error);
    }
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:8000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('token', token);
            showDashboard();
            loadProjects();
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Login failed:', error);
    }
}

function showDashboard() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
}

function showNewProject() {
    document.getElementById('project-form').style.display = 'block';
}

async function createProject() {
    const name = document.getElementById('project-name').value;
    const target_url = document.getElementById('project-url').value;
    
    try {
        const response = await fetch('http://localhost:8000/api/projects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, target_url })
        });
        
        if (response.ok) {
            document.getElementById('project-form').style.display = 'none';
            loadProjects();
        }
    } catch (error) {
        console.error('Failed to create project:', error);
    }
}

async function loadProjects() {
    try {
        const response = await fetch('http://localhost:8000/api/projects', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const projects = await response.json();
            const projectsList = document.getElementById('projects-list');
            projectsList.innerHTML = '';
            
            projects.forEach(project => {
                const projectElement = document.createElement('div');
                projectElement.className = 'project-card';
                projectElement.innerHTML = `
                    <h3>${project.name}</h3>
                    <p>${project.target_url}</p>
                    <button onclick="startScan('${project.id}', '${project.target_url}')">Start Scan</button>
                `;
                projectsList.appendChild(projectElement);
            });
        }
    } catch (error) {
        console.error('Failed to load projects:', error);
    }
}

async function startScan(projectId, targetUrl) {
    try {
        const response = await fetch('http://localhost:8000/api/scans/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                project_id: projectId,
                modules: ['headers', 'sqli', 'xss']
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            alert(`Scan started! Scan ID: ${data.scan_id}`);
            pollScanStatus(data.scan_id);
        }
    } catch (error) {
        console.error('Failed to start scan:', error);
    }
}

async function pollScanStatus(scanId) {
    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/scans/${scanId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    displayResults(data);
                }
            }
        } catch (error) {
            clearInterval(pollInterval);
        }
    }, 5000);
}

function displayResults(data) {
    const resultsDiv = document.getElementById('scan-results');
    const vulnDiv = document.getElementById('vulnerabilities');
    resultsDiv.style.display = 'block';
    vulnDiv.innerHTML = '';
    
    if (data.vulnerabilities.length === 0) {
        vulnDiv.innerHTML = '<p>No vulnerabilities found 🎉</p>';
        return;
    }
    
    data.vulnerabilities.forEach(vuln => {
        const vulnElement = document.createElement('div');
        vulnElement.className = 'vulnerability-card';
        vulnElement.innerHTML = `
            <h4>${vuln.title}</h4>
            <p>Severity: <span class="severity-${vuln.severity}">${vuln.severity.toUpperCase()}</span></p>
            <p>CVSS Score: ${vuln.cvss_score}</p>
            <p>URL: ${vuln.url}</p>
        `;
        vulnDiv.appendChild(vulnElement);
    });
}

// Check for existing token on page load
window.onload = function() {
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
        token = savedToken;
        showDashboard();
        loadProjects();
    }
};
