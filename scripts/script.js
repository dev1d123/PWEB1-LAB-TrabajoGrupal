document.addEventListener('DOMContentLoaded', function() {
    // Código para manejar el menú
    const menuItems = document.querySelectorAll('.generation');

    menuItems.forEach(function(item) {
        item.addEventListener('mouseover', function() {
            toggleSubMenu(item);
        });

        item.addEventListener('mouseout', function() {
            hideSubmenus();
        });
    });

    function toggleSubMenu(item) {
        hideSubmenus();

        const submenu = item.querySelector('.submenu');
        if (submenu) {
            submenu.style.display = 'flex';
        }
    }

    function hideSubmenus() {
        const submenus = document.querySelectorAll('.submenu');
        submenus.forEach(function(submenu) {
            submenu.style.display = 'none';
        });
    }

    // Código para el reloj
    function mostrarHora() {
        var fecha = new Date();
        var hora = fecha.getHours();
        var minutos = fecha.getMinutes();
        var segundos = fecha.getSeconds();

        document.getElementById('reloj').innerHTML = hora + ":" + minutos + ":" + segundos;
    }

    setInterval(mostrarHora, 1000); // Actualizar cada segundo

    // Código para el mensaje de bienvenida
    var nombre = prompt("Por favor, ingresa tu nombre:");
    alert("¡Bienvenido, " + nombre + "!");

    // Código para el contador de visitas
    var contadorVisitas = localStorage.getItem('contador') || 0;
    contadorVisitas++;
    localStorage.setItem('contador', contadorVisitas);
    alert("Bienvenido. Esta es tu visita número " + contadorVisitas);

    window.scrollToBottom = function() {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    };

    // Puedes agregar estilos para el botón flotante en tu hoja de estilo CSS o aquí mismo
    var styles = `
        .scroll-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
    `;

    var styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = styles;
    document.head.appendChild(styleSheet);
});

// Nueva función para cerrar la ventana modal
function cerrarVentanaModal() {
    document.getElementById('abueloModal').style.display = 'none';
}

function abrirVentanaModal(nombre, fecha, lugar, descripcion) {
    console.log('Abriendo ventana modal');
    var modalContent = document.getElementById('abueloModalContent');
    modalContent.innerHTML = `
        <div class="modal-header">
            <button class="close" onclick="cerrarVentanaModal()">&times;</button>
        </div>
        <div class="modal-body">
            <p><strong>Nombre:</strong> ${nombre}</p>
            <p><strong>Fecha:</strong> ${fecha}</p>
            <p><strong>Lugar:</strong> ${lugar}</p>
            <p><strong>Descripción:</strong> ${descripcion}</p>
        </div>
    `;
    
    // Mostrar la ventana modal
    document.getElementById('abueloModal').style.display = 'flex';
}

// Iniciar la reproducción automática al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    var carousel = document.getElementById('abueloCarousel');
    var intervalId;

    function startCarousel() {
        intervalId = setInterval(function() {
            nextSlide();
        }, 1000);
    }

    function pauseCarousel() {
        clearInterval(intervalId);
    }

    function nextSlide() {
        var activeItem = carousel.querySelector('.carousel-item.active');
        activeItem.classList.remove('active');
        var nextItem = activeItem.nextElementSibling || carousel.querySelector('.carousel-item:first-child');
        nextItem.classList.add('active');
    }

    carousel.addEventListener('mouseenter', pauseCarousel);
    carousel.addEventListener('mouseleave', startCarousel);

    startCarousel();
});

document.addEventListener('DOMContentLoaded', function() {

    // Nueva función para abrir la ventana modal
    function abrirVentanaModalDesdeImagen(imgElement) {
        var info = imgElement.getAttribute('data-info').split(',');
        abrirVentanaModal(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7]);
    }

    // Agregar un listener para cada imagen del carrusel
    var carouselImages = document.querySelectorAll('#abueloCarousel img');
    carouselImages.forEach(function(img) {
        img.addEventListener('click', function() {
            abrirVentanaModalDesdeImagen(img);
        });
    });
});

//script para imagenes hover en h3
    document.addEventListener('DOMContentLoaded', function() {
        const title = document.getElementById('hoverTitle');
        const abueloThumbnail = document.getElementById('abueloThumbnail');
        const abuelaThumbnail = document.getElementById('abuelaThumbnail');
        const tioThumbnail = document.getElementById('tioThumbnail');

        title.addEventListener('mouseover', function() {
            abueloThumbnail.style.display = 'inline-block';
            abuelaThumbnail.style.display = 'inline-block';
            tioThumbnail.style.display = 'inline-block';
        });

        title.addEventListener('mouseout', function() {
            abueloThumbnail.style.display = 'none';
            abuelaThumbnail.style.display = 'none';
            tioThumbnail.style.display = 'none';
        });
    });
