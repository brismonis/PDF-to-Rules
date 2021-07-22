/*!
    * Start Bootstrap - SB Admin v7.0.1 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2021 Start Bootstrap
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
        if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
            document.body.classList.toggle('sb-sidenav-toggled');
        }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


// document.getElementById('sidebarToggle').addEventListener('click', navStatus);

// // Prüfen ob die Navigation geöffnet oder geschlossen ist

// function navStatus() {
//   if (document.body.classList.contains('sb-sidenav-toggled')) {
//    navClose();
//  } 
//  else {
//    navOpen();
//  }
// }

// // Wenn die Navi geschlossen wird, Klasse für »offen« entfernen

// function navClose() {
//   document.body.classList.remove('sb-sidenav-toggled');
// }

// // Wenn die Navi geöffnet wird, Klasse für »geschlossen« entfernen

// function navOpen() {
//   document.body.classList.add('sb-sidenav-toggled');
// }
