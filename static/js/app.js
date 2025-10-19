// URL base de la API
const API_BASE_URL = "http://localhost:8000";

// Variables globales
let editandoTarea = false;
let tareaEditandoId = null;

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo = "success") {
  const messageArea = document.getElementById("message-area");
  const alertClass = tipo === "success" ? "alert-success" : "alert-error";

  messageArea.innerHTML = `
<div class="alert ${alertClass}">${mensaje}</div>
`;

  // Ocultar el mensaje después de 5 segundos
  setTimeout(() => {
    messageArea.innerHTML = "";
  }, 5000);
}

// Función para cargar todas las tareas
async function cargarTareas() {
  try {
    const response = await fetch(`${API_BASE_URL}/tareas`);
    if (!response.ok) {
      throw new Error("Error al cargar las tareas");
    }

    const tareas = await response.json();
    mostrarTareas(tareas);
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al cargar las tareas", "error");
    document.getElementById("tasks-container").innerHTML =
      '<div class="alert alert-error">Error al cargar las tareas. Verifica que la API esté ejecutándose.</div>';
  }
}

// Función para mostrar las tareas en el HTML
function mostrarTareas(tareas) {
  const container = document.getElementById("tasks-container");

  if (tareas.length === 0) {
    container.innerHTML =
      '<div class="no-tasks">No hay tareas todavía. ¡Crea la primera!</div>';
    return;
  }

  const tareasHTML = tareas
    .map((tarea) => {
      const completedClass = tarea.completada ? "completed" : "";
      const titleClass = tarea.completada ? "task-completed" : "";
      const statusClass = tarea.completada
        ? "status-completed"
        : "status-pending";
      const statusText = tarea.completada ? "Completada" : "Pendiente";

      return `
<div class="task-card ${completedClass}">
  <div class="task-header">
    <h3 class="task-title ${titleClass}">${tarea.titulo}</h3>
    <span class="task-id">ID: ${tarea.id}</span>
  </div>
  <p class="task-description">${tarea.descripcion}</p>
  <span class="task-status ${statusClass}">${statusText}</span>
  <div class="task-actions">
    <button class="btn" onclick="editarTarea(${tarea.id})">✏️ Editar</button>
    <button class="btn btn-warning" onclick="toggleCompletada(${
      tarea.id
    }, ${!tarea.completada})"> ${
        tarea.completada ? "↩️ Marcar Pendiente" : "✅ Marcar Completada"
      }</button>
    <button class="btn btn-danger" onclick="eliminarTarea(${
      tarea.id
    })">🗑️ Eliminar</button>
  </div>
</div>
`;
    })
    .join("");

  container.innerHTML = tareasHTML;
}

// Función para crear una nueva tarea
async function crearTarea(tarea) {
  try {
    const response = await fetch(`${API_BASE_URL}/tareas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tarea),
    });

    if (!response.ok) {
      throw new Error("Error al crear la tarea");
    }

    const nuevaTarea = await response.json();
    mostrarMensaje(`Tarea "${nuevaTarea.titulo}" creada exitosamente!`);
    cargarTareas();
    return nuevaTarea;
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al crear la tarea", "error");
  }
}

// Función para actualizar una tarea
async function actualizarTarea(id, tarea) {
  try {
    const response = await fetch(`${API_BASE_URL}/tareas/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tarea),
    });

    if (!response.ok) {
      throw new Error("Error al actualizar la tarea");
    }

    const tareaActualizada = await response.json();
    mostrarMensaje(
      `Tarea "${tareaActualizada.titulo}" actualizada exitosamente!`
    );
    cargarTareas();
    return tareaActualizada;
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al actualizar la tarea", "error");
  }
}

// Función para cambiar el estado de completada
async function toggleCompletada(id, completada) {
  try {
    const response = await fetch(`${API_BASE_URL}/tareas/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ completada }),
    });

    if (!response.ok) {
      throw new Error("Error al actualizar el estado");
    }

    const tareaActualizada = await response.json();
    mostrarMensaje(
      `Tarea marcada como ${completada ? "completada" : "pendiente"}!`
    );
    cargarTareas();
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al actualizar el estado", "error");
  }
}

// Función para eliminar una tarea
async function eliminarTarea(id) {
  if (!confirm("¿Estás seguro de que quieres eliminar esta tarea?")) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/tareas/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Error al eliminar la tarea");
    }

    const resultado = await response.json();
    mostrarMensaje("Tarea eliminada exitosamente!");
    cargarTareas();
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al eliminar la tarea", "error");
  }
}

// Función para preparar la edición de una tarea
async function editarTarea(id) {
  try {
    const response = await fetch(`${API_BASE_URL}/tareas/${id}`);
    if (!response.ok) {
      throw new Error("Error al obtener la tarea");
    }

    const tarea = await response.json();

    // Llenar el formulario con los datos de la tarea
    document.getElementById("titulo").value = tarea.titulo;
    document.getElementById("descripcion").value = tarea.descripcion;
    document.getElementById("completada").checked = tarea.completada;
    document.getElementById("task-id").value = tarea.id;

    // Cambiar el estado del formulario a modo edición
    editandoTarea = true;
    tareaEditandoId = id;
    document.getElementById("form-title").textContent = "✏️ Editar Tarea";
    document.getElementById("submit-btn").textContent = "Actualizar Tarea";
    document.getElementById("cancel-btn").style.display = "inline-block";

    // Hacer scroll al formulario
    document.getElementById("task-form").scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al cargar la tarea para edición", "error");
  }
}

// Función para limpiar el formulario
function limpiarFormulario() {
  document.getElementById("task-form").reset();
  editandoTarea = false;
  tareaEditandoId = null;
  document.getElementById("form-title").textContent = "📝 Crear Nueva Tarea";
  document.getElementById("submit-btn").textContent = "Crear Tarea";
  document.getElementById("cancel-btn").style.display = "none";
}

// Función para ir a la vista de tareas eliminadas
function irAVistaEliminadas() {
  window.location.href = "/eliminadas";
}

// Manejar el envío del formulario
document.getElementById("task-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const tarea = {
    titulo: formData.get("titulo"),
    descripcion: formData.get("descripcion"),
    completada: formData.has("completada"),
  };

  if (editandoTarea && tareaEditandoId) {
    await actualizarTarea(tareaEditandoId, tarea);
  } else {
    await crearTarea(tarea);
  }

  limpiarFormulario();
});

// Manejar el botón cancelar
document
  .getElementById("cancel-btn")
  .addEventListener("click", limpiarFormulario);

// Cargar las tareas al cargar la página
window.addEventListener("load", cargarTareas);
