feather.replace() // icooooooon

document.addEventListener("DOMContentLoaded", function() {
    // Attacher des événements aux boutons de suppression
    const deleteButtons = document.querySelectorAll(".deleteButton");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();  // Empêche le rechargement de la page
            const taskId = this.dataset.id;  // Récupère l'ID de la tâche via data-id

            console.log(`Task ID: ${taskId} - Delete button clicked`);

            fetch(`/tasks/${taskId}/delete`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Response from server:", data);
                if (data.success) {
                    // Supprimer la tâche du DOM après suppression
                    const taskItem = document.getElementById(`task-${taskId}`);
                    if (taskItem) {
                        taskItem.remove();
                        console.log(`Task ${taskId} removed from DOM`);
                    }
                } else {
                    alert("Erreur lors de la suppression de la tâche.");
                }
            })
            .catch(error => {
                console.error("Erreur :", error);
                alert("Une erreur est survenue lors de la suppression.");
            });
        });
    });

    const taskForm = document.getElementById("taskForm");
    if (taskForm) {
        taskForm.addEventListener("submit", function(event) {
            event.preventDefault();  // Empêche le rechargement de la page

            // Récupérer les données du formulaire
            const formData = new FormData(taskForm);
            const title = formData.get("title");
            const description = formData.get("description");
            const due_date = formData.get("due_date");

            // Créer l'objet de la tâche
            const taskData = {
                title: title,
                description: description,
                due_date: due_date
            };

            console.log("Task data to be created:", taskData);

            // Envoyer les données en AJAX
            fetch("/tasks/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(taskData)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Response from server:", data);
                if (data.success) {
                    // Ajouter la nouvelle tâche au DOM sans recharger la page
                    const taskList = document.getElementById("taskList");
                    const newTask = document.createElement("li");
                    newTask.setAttribute("id", `task-${data.task.id}`);
                    newTask.innerHTML = `
                        <h3>${data.task.title}</h3>
                        <p>${data.task.description}</p>
                        <p><strong>Date d'échéance :</strong> ${data.task.due_date ? data.task.due_date : "Pas de date"}</p>
                        <button type="button" class="deleteButton" data-id="${data.task.id}">Supprimer</button>
                    `;
                    taskList.appendChild(newTask);

                    // Attacher l'événement de suppression au nouveau bouton créé
                    newTask.querySelector(".deleteButton").addEventListener("click", function(event) {
                        event.preventDefault();
                        const taskId = this.dataset.id;
                        fetch(`/tasks/${taskId}/delete`, {
                            method: "DELETE",
                            headers: {
                                "Content-Type": "application/json"
                            }
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                newTask.remove();
                            } else {
                                alert("Erreur lors de la suppression de la tâche.");
                            }
                        })
                        .catch(error => console.error("Erreur :", error));
                    });

                    // Réinitialiser le formulaire
                    taskForm.reset();
                } else {
                    alert("Erreur lors de la création de la tâche.");
                }
            })
            .catch(error => {
                console.error("Erreur :", error);
                alert("Une erreur est survenue lors de la création.");
            });
        });
    }
});
