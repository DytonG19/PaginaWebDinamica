// Obtén todos los botones del menú
const menuButtons = document.querySelectorAll('.menu-button');

// Agrega eventos click a cada botón
menuButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Alternar la clase 'open' en el botón
        button.classList.toggle('open');
    });
});
