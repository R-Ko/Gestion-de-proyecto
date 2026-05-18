/**
 * APP.JS - Lógica Frontend
 * Se comunica con API backend en Render + Aiven
 */

// Configuración
const API_URL = (typeof process !== 'undefined' && process.env && process.env.API_URL)
    ? process.env.API_URL
    : (typeof window !== 'undefined' && window.API_URL)
        ? window.API_URL
        : 'http://localhost:5000';
const isDevelopment = window.location.hostname === 'localhost';

// Estado global
let currentUser = null;
let currentProject = null;
let allProjects = [];
let allTasks = [];

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

// ============================================================================
// AUTENTICACIÓN
// ============================================================================

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    
    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = email;
            localStorage.setItem('user', email);
            showPage('projects-page');
            document.getElementById('user-email').textContent = email;
            document.getElementById('user-email-detail').textContent = email;
            loadProjects();
            errorDiv.textContent = '';
        } else {
            errorDiv.textContent = data.error || 'Login fallido';
        }
    } catch (error) {
        console.error('Error en login:', error);
        errorDiv.textContent = 'Error de conexión. Intenta nuevamente.';
    }
}

async function handleLogout() {
    try {
        await fetch(`${API_URL}/api/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        currentUser = null;
        localStorage.removeItem('user');
        showPage('login-page');
        document.getElementById('login-email').value = '';
        document.getElementById('login-password').value = '';
    } catch (error) {
        console.error('Error en logout:', error);
    }
}

async function checkAuth() {
    const savedUser = localStorage.getItem('user');
    
    if (savedUser) {
        try {
            const response = await fetch(`${API_URL}/api/user`, {
                credentials: 'include'
            });
            
            if (response.ok) {
                currentUser = savedUser;
                document.getElementById('user-email').textContent = savedUser;
                document.getElementById('user-email-detail').textContent = savedUser;
                showPage('projects-page');
                loadProjects();
            } else {
                showPage('login-page');
            }
        } catch (error) {
            console.error('Error verificando autenticación:', error);
            showPage('login-page');
        }
    } else {
        showPage('login-page');
    }
}

// ============================================================================
// NAVEGACIÓN
// ============================================================================

function showPage(pageId) {
    // Ocultar todas las páginas
    document.querySelectorAll('.page').forEach(page => {
        page.classList.add('hidden');
    });
    
    // Mostrar la página solicitada
    const page = document.getElementById(pageId);
    if (page) {
        page.classList.remove('hidden');
    }
}

// ============================================================================
// PROYECTOS
// ============================================================================

async function loadProjects() {
    const grid = document.getElementById('projects-grid');
    grid.innerHTML = '<div class="loading">Cargando proyectos...</div>';
    
    try {
        const response = await fetch(`${API_URL}/api/projects`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const projects = await response.json();
            allProjects = projects;
            renderProjects(projects);
        } else if (response.status === 401) {
            handleLogout();
        }
    } catch (error) {
        console.error('Error cargando proyectos:', error);
        grid.innerHTML = '<div class="error">Error al cargar proyectos</div>';
    }
}

function renderProjects(projects) {
    const grid = document.getElementById('projects-grid');
    
    if (projects.length === 0) {
        grid.innerHTML = '<div class="empty-state">No hay proyectos. Crea uno nuevo.</div>';
        return;
    }
    
    grid.innerHTML = projects.map(project => `
        <div class="proj-card" onclick="viewProject(${project.id})">
            <div class="proj-header">
                <div class="proj-label">⭐ ${project.name}</div>
                <span class="project-tag">Proyecto</span>
            </div>
            <div class="proj-meta">
                <span>👤 Propietario: ${project.owner_email}</span><br>
                <span>👥 Asignados: ${project.assigned_emails || 'N/A'}</span>
            </div>
            <div class="proj-booster">
                <div class="proj-stat"><span class="icon">📋</span><strong>${project.tasks_count || 0}</strong> Tasks</div>
                <div class="proj-stat"><span class="icon">🎫</span><strong>${project.tickets_count || 0}</strong> Tickets</div>
            </div>
        </div>
    `).join('');
}

function filterProjects(filter) {
    let filtered = allProjects;
    
    if (filter === 'owner') {
        filtered = allProjects.filter(p => p.owner_email === currentUser);
    } else if (filter === 'assigned') {
        filtered = allProjects.filter(p => 
            p.assigned_emails && p.assigned_emails.includes(currentUser)
        );
    }
    
    renderProjects(filtered);
    
    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

function searchProjects() {
    const searchTerm = document.getElementById('search-box').value.toLowerCase();
    const filtered = allProjects.filter(p => 
        p.name.toLowerCase().includes(searchTerm)
    );
    renderProjects(filtered);
}

async function viewProject(projectId) {
    try {
        const response = await fetch(`${API_URL}/api/projects/${projectId}`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const project = await response.json();
            currentProject = project;
            document.getElementById('project-name').textContent = project.name;
            document.getElementById('project-owner').textContent = `Propietario: ${project.owner_email}`;
            showPage('project-detail-page');
            loadTasks(projectId);
        }
    } catch (error) {
        console.error('Error cargando proyecto:', error);
    }
}

async function handleCreateProject(event) {
    event.preventDefault();
    
    const name = document.getElementById('project-name-input').value;
    
    try {
        const response = await fetch(`${API_URL}/api/projects`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name })
        });
        
        if (response.ok) {
            showPage('projects-page');
            loadProjects();
            document.getElementById('project-name-input').value = '';
            document.getElementById('project-description-input').value = '';
        }
    } catch (error) {
        console.error('Error creando proyecto:', error);
    }
}

// ============================================================================
// TAREAS
// ============================================================================

async function loadTasks(projectId) {
    const container = document.getElementById('tasks-container');
    container.innerHTML = '<div class="loading">Cargando tareas...</div>';
    
    try {
        const response = await fetch(`${API_URL}/api/projects/${projectId}/tasks`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            allTasks = await response.json();
            renderTasks(allTasks);
        }
    } catch (error) {
        console.error('Error cargando tareas:', error);
        container.innerHTML = '<div class="error">Error al cargar tareas</div>';
    }
}

function renderTasks(tasks) {
    const container = document.getElementById('tasks-container');
    
    if (tasks.length === 0) {
        container.innerHTML = '<div class="empty-state">No hay tareas en este proyecto</div>';
        return;
    }
    
    container.innerHTML = `
        <table class="tasks-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Título</th>
                    <th>Asignado</th>
                    <th>Stage</th>
                    <th>Deadline</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                ${tasks.map(task => `
                    <tr class="task-row" onclick="viewTask(${task.id})">
                        <td>${task.id}</td>
                        <td><strong>${task.title}</strong></td>
                        <td>${task.assigned_email || 'Sin asignar'}</td>
                        <td><span class="badge badge-${task.stage}">${task.stage}</span></td>
                        <td>${task.deadline || '-'}</td>
                        <td>
                            <button class="btn-sm" onclick="event.stopPropagation(); editTask(${task.id})">Editar</button>
                            <select class="stage-select" onchange="changeTaskStage(${task.id}, this.value)">
                                <option value="">Cambiar stage...</option>
                                <option value="backlog">Backlog</option>
                                <option value="pending">Pendiente</option>
                                <option value="inprogress">En progreso</option>
                                <option value="qa">QA</option>
                                <option value="validation">Validación</option>
                                <option value="deployed">Desplegada</option>
                            </select>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function filterTasks(stage) {
    let filtered = allTasks;
    
    if (stage !== 'all') {
        filtered = allTasks.filter(t => t.stage === stage);
    }
    
    renderTasks(filtered);
    
    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

async function changeTaskStage(taskId, newStage) {
    if (!newStage) return;
    
    try {
        const response = await fetch(`${API_URL}/api/tasks/${taskId}/stage`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                stage: newStage,
                note: `Cambio a ${newStage}`
            })
        });
        
        if (response.ok) {
            loadTasks(currentProject.id);
        }
    } catch (error) {
        console.error('Error actualizando stage:', error);
    }
}

async function handleCreateTask(event) {
    event.preventDefault();
    
    const title = document.getElementById('task-title-input').value;
    const description = document.getElementById('task-description-input').value;
    const assignedEmail = document.getElementById('task-assigned-input').value;
    const taskType = document.getElementById('task-type-input').value;
    const deadline = document.getElementById('task-deadline-input').value;
    
    try {
        const response = await fetch(`${API_URL}/api/tasks`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                project_id: currentProject.id,
                title,
                description,
                assigned_email: assignedEmail || currentUser,
                task_type: taskType,
                deadline,
                stage: 'backlog'
            })
        });
        
        if (response.ok) {
            showPage('project-detail-page');
            loadTasks(currentProject.id);
            // Limpiar formulario
            document.getElementById('task-title-input').value = '';
            document.getElementById('task-description-input').value = '';
            document.getElementById('task-assigned-input').value = '';
            document.getElementById('task-deadline-input').value = '';
        }
    } catch (error) {
        console.error('Error creando tarea:', error);
    }
}

function viewTask(taskId) {
    const task = allTasks.find(t => t.id === taskId);
    if (task) {
        alert(`Tarea: ${task.title}\n\nDescripción: ${task.description}\n\nAsignado: ${task.assigned_email}`);
    }
}

function editTask(taskId) {
    alert('Función de edición disponible pronto');
}
