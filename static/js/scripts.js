/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


function createToast(color, message,delay=5000, icon ="fa-circle-check") {
    if (color=="danger"){
        icon="fa-exclamation-circle"
    }
    // Create toast element
    const toastElement = document.createElement('div');
    toastElement.classList.add('toast', "align-items-center", "border-start", "border-5", `border-${color}`);
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');
    toastElement.setAttribute('data-bs-delay', Number(delay));
  
    // create flex
    const flexForBody = document.createElement('div');
    flexForBody.classList.add('d-flex');
  
    // Toast body
    const toastBody = document.createElement('div');
    toastBody.classList.add('toast-body', `text-${color}`, "d-flex");
    toastBody.innerHTML = `<div class="align-self-center me-1"><i class="fas ${icon}"></i></div>
    <div>${message}</div>`;

    //button
    const button = document.createElement('button');
    button.type = 'button';
    button.classList.add('btn-close', 'me-2', 'm-auto');
    button.setAttribute('data-bs-dismiss', 'toast');
    button.setAttribute('aria-label', 'Close');
    
    //assemble flexed body
    flexForBody.appendChild(toastBody)
    flexForBody.appendChild(button)
    // Assemble the toast
    toastElement.appendChild(flexForBody);
    
  
    // Append to toast container
    const toastContainer = document.getElementById('toastPlacement');
    toastContainer.appendChild(toastElement);
  
    // Initialize and show the toast using Bootstrap's Toast class
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
  }


  // Function to update the status
function updateOnlineStatus() {
    if (!navigator.onLine) {
       createToast("warning", "You are offline. Please check your connection", delay=10000, icon ="fa-plug")
        // Perform actions when online
    } 
}

window.addEventListener('offline', updateOnlineStatus);

updateOnlineStatus()