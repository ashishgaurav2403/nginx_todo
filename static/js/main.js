async function loadTodos() {
    const response = await fetch('/todos');
    const todos = await response.json();
    const list = document.getElementById('todoList');
    list.innerHTML = '';
    
    todos.forEach(todo => {
        const li = document.createElement('li');
        if (todo.completed) li.classList.add('completed');
        
        li.innerHTML = `
            <span class="task-text" onclick="toggleTask(${todo.id})">${todo.task}</span>
            <button class="delete-btn" onclick="deleteTask(${todo.id})">Delete</button>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const input = document.getElementById('taskInput');
    const task = input.value.trim();
    if (!task) return;

    await fetch('/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    });
    input.value = '';
    loadTodos();
}

function handleKeyPress(event) {
    if (event.key === 'Enter') addTask();
}

async function toggleTask(id) {
    await fetch(`/todos/${id}`, { method: 'PUT' });
    loadTodos();
}

async function deleteTask(id) {
    await fetch(`/todos/${id}`, { method: 'DELETE' });
    loadTodos();
}

loadTodos();