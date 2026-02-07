const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");
const toggleThemeBtn = document.getElementById("toggle-theme");
const exportBtn = document.getElementById("export-btn");
const importFile = document.getElementById("import-file");
const body = document.body;

let todos = [];

/* Thêm task */
function addTodo(text) {
    todos.push({
        id: Date.now(),
        title: text,
        completed: false
    });
    render();
}

/* Toggle hoàn thành */
function toggleComplete(id) {
    const todo = todos.find(t => t.id === id);
    todo.completed = !todo.completed;
    render();
}

/* Xoá */
function deleteTodo(id) {
    todos = todos.filter(t => t.id !== id);
    render();
}

/* Sửa */
function editTodo(id) {
    const todo = todos.find(t => t.id === id);
    const newTitle = prompt("Sửa công việc:", todo.title);
    if (newTitle && newTitle.trim()) {
        todo.title = newTitle.trim();
        render();
    }
}

/* Render */
function render() {
    list.innerHTML = "";
    todos.forEach(todo => {
        const li = document.createElement("li");
        if (todo.completed) li.classList.add("completed");

        li.innerHTML = `
            <div class="left">
                <input type="checkbox"
                    ${todo.completed ? "checked" : ""}
                    onclick="toggleComplete(${todo.id})">
                <span>${todo.title}</span>
            </div>
            <div class="actions">
                <button onclick="editTodo(${todo.id})">✏️</button>
                <button onclick="deleteTodo(${todo.id})">🗑️</button>
            </div>
        `;
        list.appendChild(li);
    });
}

/* Enter để thêm */
input.addEventListener("keydown", e => {
    if (e.key === "Enter" && input.value.trim()) {
        addTodo(input.value.trim());
        input.value = "";
    }
});

/* Chế độ ngày / đêm */
toggleThemeBtn.addEventListener("click", () => {
    body.classList.toggle("dark");
    body.classList.toggle("light");
    toggleThemeBtn.textContent =
        body.classList.contains("dark") ? "☀️" : "🌙";
});

/* Export file */
exportBtn.addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(todos, null, 2)], {
        type: "application/json"
    });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "todo-list.json";
    a.click();

    URL.revokeObjectURL(url);
});

/* Import file */
importFile.addEventListener("change", e => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
        try {
            todos = JSON.parse(reader.result);
            render();
        } catch {
            alert("File không hợp lệ!");
        }
    };
    reader.readAsText(file);
});
