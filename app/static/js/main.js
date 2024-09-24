feather.replace() // icooooooon

// checbox test
/*
setTimeout(function(){
  document.querySelector('input[type="checkbox"]').setAttribute('checked',true);
},100);
*/


// redirect after creating a task

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
            .then(response => {
                if (response.redirected) {
                    console.log(`Redirection to: ${response.url}`);
                    // Attendre 2 secondes avant de rediriger
                    setTimeout(() => {
                        window.location.href = response.url;
                    }, 1200);
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data && data.success) {
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
                } else if (data) {
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




// create task form animation

$(document).ready(function() {
  setTimeout(function() {
    // Tous vos événements jQuery ici, après un petit délai
    $('.taskFormTitle').on("change keyup paste", function() {
      if ($(this).val()) {
        $('.icon-paper-plane').addClass("next");
      } else {
        $('.icon-paper-plane').removeClass("next");
      }
    });

    $('.next-button').hover(function() {
      $(this).css('cursor', 'pointer');
    });

    $('.next-button.taskFormTitle').click(function() {
      console.log("Title button clicked");
      $('.createTitle-section').addClass("fold-up");
      $('.createDesc-section').removeClass("folded");
    });

    $('.taskFormDesc').on("change keyup paste", function() {
      if ($(this).val()) {
        $('.icon-lock').addClass("next");
      } else {
        $('.icon-lock').removeClass("next");
      }
    });

    $('.next-button.taskFormDesc').click(function() {
      console.log("Password button clicked");
      $('.createDesc-section').addClass("fold-up");
      $('.createDueDate-section').removeClass("folded");
    });

    $('.taskFormDueDate').on("change keyup paste", function() {
      if ($(this).val()) {
        $('.icon-repeat-lock').addClass("next");
      } else {
        $('.icon-repeat-lock').removeClass("next");
      }
    });

    $('.next-button.taskFormDueDate').click(function() {
      console.log("Repeat password button clicked");
      $('.createDueDate-section').addClass("fold-up");
      $('.success').css("marginTop", 0);
    });
  }, 100); // Attendre 100ms avant d'attacher les événements jQuery
});



// context v2



class ContextMenu {
  constructor({ target = null, menuItems = [] }) {
    this.target = target;
    this.menuItems = menuItems;
    this.mode = "dark"; // Force dark mode
    this.targetNode = this.getTargetNode();
    this.menuItemsNode = this.getMenuItemsNode();
    this.isOpened = false;
  }

  getTargetNode() {
    const nodes = document.querySelectorAll(this.target);
console.log(nodes); // Debug: check if target nodes are found

    if (nodes && nodes.length !== 0) {
      return nodes;
    } else {
      console.error(`getTargetNode :: "${this.target}" target not found`);
      return [];
    }
  }

  getMenuItemsNode() {
    const nodes = [];

    if (!this.menuItems) {
      console.error("getMenuItemsNode :: Please enter menu items");
      return [];
    }

    this.menuItems.forEach((data, index) => {
      const item = this.createItemMarkup(data);
      item.firstChild.setAttribute(
        "style",
        `animation-delay: ${index * 0.08}s`
      );
      nodes.push(item);
    });

    return nodes;
  }

  createItemMarkup(data) {
    const button = document.createElement("BUTTON");
    const item = document.createElement("LI");

    button.innerHTML = data.content;
    button.classList.add("contextMenu-button");
    item.classList.add("contextMenu-item");

    if (data.divider) item.setAttribute("data-divider", data.divider);
    item.appendChild(button);

    if (data.events && data.events.length !== 0) {
      Object.entries(data.events).forEach((event) => {
        const [key, value] = event;
        button.addEventListener(key, value);
      });
    }

    return item;
  }

  renderMenu() {
    const menuContainer = document.createElement("UL");

    menuContainer.classList.add("contextMenu");
    menuContainer.setAttribute("data-theme", this.mode); // Dark mode forced

    this.menuItemsNode.forEach((item) => menuContainer.appendChild(item));

    return menuContainer;
  }

  closeMenu(menu) {
    if (this.isOpened) {
      this.isOpened = false;
      menu.remove();
    }
  }

  init() {
    const contextMenu = this.renderMenu();
    document.addEventListener("click", () => this.closeMenu(contextMenu));
    window.addEventListener("blur", () => this.closeMenu(contextMenu));

    this.targetNode.forEach((target) => {
      target.addEventListener("contextmenu", (e) => {
        e.preventDefault(); // Prevent default browser menu
        this.isOpened = true;

        // Debug log to confirm the right-click is working
        console.log(`Context menu opened for target: ${target}, at coordinates: (${e.clientX}, ${e.clientY})`);

        const { clientX, clientY } = e;
        document.body.appendChild(contextMenu);
        contextMenu.style.display = "block"; // Make sure the menu is visible

        // Positioning logic
        const positionY = clientY + contextMenu.scrollHeight >= window.innerHeight
          ? window.innerHeight - contextMenu.scrollHeight - 20
          : clientY;

        const positionX = clientX + contextMenu.scrollWidth >= window.innerWidth
          ? window.innerWidth - contextMenu.scrollWidth - 20
          : clientX;

        // Set the position directly
        contextMenu.style.top = `${positionY}px`;
        contextMenu.style.left = `${positionX}px`;

        // Log final position to ensure correct placement
        console.log(`Menu position set to top: ${positionY}px, left: ${positionX}px`);
      });
    });

  }
}

const copyIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" style="margin-right: 7px" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;

const cutIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" style="margin-right: 7px" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>`;

const pasteIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" style="margin-right: 7px; position: relative; top: -1px" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>`;

const downloadIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" style="margin-right: 7px; position: relative; top: -1px" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>`;

const dateIcon = `<svg viewBox="0 0 24 24" width="13px" height="13px"  fill="none" stroke="currentColor" stroke-width="2.5" style="margin-right: 7px; position: relative; top: -1px" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M20 13V7C20 5.89543 19.1046 5 18 5H6C4.89543 5 4 5.89543 4 7V19C4 20.1046 4.89543 21 6 21H8M15 3V7M9 3V7M4 11H20M14 19H17M14 17H13C11.8954 17 11 17.8954 11 19C11 20.1046 11.8954 21 13 21H14M17 21H18C19.1046 21 20 20.1046 20 19C20 17.8954 19.1046 17 18 17H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

const deleteIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`;



/*
// context menu
document.addEventListener("DOMContentLoaded", function () {
  const contextMenu = document.getElementById('context-menu');
  let clickedTaskId = null;

  // Show context menu on right-click
  document.querySelectorAll('.todo').forEach(function (todo) {
    todo.addEventListener('contextmenu', function (e) {
      e.preventDefault();

      clickedTaskId = todo.getAttribute('data-id'); // Get the ID of the right-clicked task

      // Set the position of the context menu
      contextMenu.style.top = `${e.pageY}px`;
      contextMenu.style.left = `${e.pageX}px`;
      contextMenu.style.display = 'block';

      // Update the delete button data-id with the clicked task ID
      const deleteButton = contextMenu.querySelector('.deleteButton');
      deleteButton.setAttribute('data-id', clickedTaskId);
    });
  });

  // Hide the context menu when clicking elsewhere
  document.addEventListener('click', function () {
    contextMenu.style.display = 'none';
  });
});
*/


function logout() {
  // Remove the JWT token from localStorage or sessionStorage
  localStorage.removeItem("access_token");

  // Optionally, redirect to login page
  window.location.href = "/login";
}