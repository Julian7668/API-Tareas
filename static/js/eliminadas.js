// URL base de la API
const API_BASE_URL = "http://localhost:8000";

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

// Función para cargar todas las tareas eliminadas
async function cargarTareasEliminadas() {
  console.log("Iniciando carga de tareas eliminadas...");
  console.log("URL de la API:", `${API_BASE_URL}/eliminadas`);
  try {
    const response = await fetch(`${API_BASE_URL}/eliminadas`);
    console.log("Respuesta del fetch - Status:", response.status, "OK:", response.ok);
    if (!response.ok) {
      console.error("Respuesta no OK. Status:", response.status, "StatusText:", response.statusText);
      throw new Error(`Error al cargar las tareas eliminadas: ${response.status} ${response.statusText}`);
    }

    const tareas = await response.json();
    console.log("Tareas eliminadas recibidas:", tareas);
    mostrarTareasEliminadas(tareas);
  } catch (error) {
    console.error("Error completo en cargarTareasEliminadas:", error);
    mostrarMensaje("Error al cargar las tareas eliminadas", "error");
    document.getElementById("eliminadas-container").innerHTML =
      '<div class="alert alert-error">Error al cargar las tareas eliminadas. Verifica que la API esté ejecutándose.</div>';
  }
}

// Función para mostrar las tareas eliminadas en el HTML
function mostrarTareasEliminadas(tareas) {
  const container = document.getElementById("eliminadas-container");

  if (tareas.length === 0) {
    container.innerHTML =
      '<div class="no-tasks">No hay tareas eliminadas.</div>';
    return;
  }

  const tareasHTML = tareas
    .map((tarea) => {
      const fechaEliminacion = new Date(tarea.fecha_eliminacion).toLocaleString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });

      return `
<div class="task-card deleted">
  <div class="task-header">
    <h3 class="task-title">${tarea.titulo}</h3>
    <span class="task-id">ID: ${tarea.id}</span>
  </div>
  <p class="task-description">${tarea.descripcion}</p>
  <div class="task-meta">
    <span class="task-status status-deleted">Eliminada</span>
    <span class="deletion-date">Eliminada el: ${fechaEliminacion}</span>
  </div>
  <div class="task-actions">
    <button class="btn btn-success" onclick="restaurarTarea(${tarea.id})">
      🔄 Restaurar
    </button>
  </div>
</div>
`;
    })
    .join("");

  container.innerHTML = tareasHTML;
}

// Función para restaurar una tarea eliminada
async function restaurarTarea(id) {
  if (!confirm("¿Estás seguro de que quieres restaurar esta tarea?")) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/eliminadas/${id}`, {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error("Error al restaurar la tarea");
    }

    const tareaRestaurada = await response.json();
    mostrarMensaje(`Tarea "${tareaRestaurada.titulo}" restaurada exitosamente!`);
    cargarTareasEliminadas();
  } catch (error) {
    console.error("Error:", error);
    mostrarMensaje("Error al restaurar la tarea", "error");
  }
}

// Función para volver a la vista de tareas activas
function volverATareas() {
  window.location.href = "/";
}

// Cargar las tareas eliminadas al cargar la página
window.addEventListener("load", cargarTareasEliminadas);