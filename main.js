 
let menuToggle = document.getElementById('menuToggle');
let sidebarMenu = document.getElementById('sidebarMenu');
let mainLayout = document.getElementById('mainLayout');

if (menuToggle && sidebarMenu && mainLayout) {
    menuToggle.addEventListener('click', () => {
        sidebarMenu.classList.toggle('active');
        mainLayout.classList.toggle('shifted');
        
        let icon = menuToggle.querySelector('i');
        if (sidebarMenu.classList.contains('active')) {
            icon.className = 'fas fa-times';
        } else {
            icon.className = 'fas fa-bars';
        }
    });
}
 
let swapBtn = document.getElementById('swapLocations');
if (swapBtn) {
    swapBtn.addEventListener('click', () => {
        let oriInput = document.getElementById('quickOrigen');
        let desInput = document.getElementById('quickDestino');
        if (oriInput && desInput) {
            let temporal = oriInput.value;
            oriInput.value = desInput.value;
            desInput.value = temporal;
        }
    });
}
 
let counters = document.querySelectorAll('.counter');
if (counters.length > 0) {
    counters.forEach(counter => {
        counter.innerText = '0';
        let actualizarContador = () => {
            let target = +counter.getAttribute('data-target');
            let c = +counter.innerText;
            let incremento = target / 50;

            if (c < target) {
                counter.innerText = `${Math.ceil(c + incremento)}`;
                setTimeout(actualizarContador, 25);
            } else {
                counter.innerText = target + '+';
            }
        };
        actualizarContador();
    });
}
 
let quickBuscarBtn = document.getElementById('quickBuscarBtn');
if (quickBuscarBtn) {
    quickBuscarBtn.addEventListener('click', () => {
        let origen = document.getElementById('quickOrigen').value;
        let destino = document.getElementById('quickDestino').value;
        let fecha = document.getElementById('quickFecha').value;
        
        localStorage.setItem('busquedaRapida', JSON.stringify({ origen, destino, fecha }));
        window.location.href = '/pasajes';
    });
}
 
// PINTAR LISTADO DINÁMICO DE PASAJES 
let datosContenedor = document.getElementById('viajesDataContainer');
let viajesData = [];

if (datosContenedor && datosContenedor.getAttribute('data-viajes')) {
    try {
        viajesData = JSON.parse(datosContenedor.getAttribute('data-viajes'));
        if (viajesData.length === 0) {
            viajesData = [
                { id: 1, empresa: "Flota El Dorado", origen: "La Paz", destino: "Cochabamba", fecha_salida: "2026-05-25", hora_salida: "20:00", duracion: "7h", asientos_disponibles: 14, precio: 90, imagen: "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=400" },
                { id: 2, empresa: "Trans Copacabana", origen: "Cochabamba", destino: "Santa Cruz", fecha_salida: "2026-05-26", hora_salida: "22:00", duracion: "10h", asientos_disponibles: 8, precio: 130, imagen: "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?auto=format&fit=crop&q=80&w=400" }
            ];
        }
    } catch (err) {
        console.log("Error al mapear JSON");
    }
}

function pintarViajes(viajes) {
    let container = document.getElementById('resultadosPasajes');
    let contador = document.getElementById('contadorViajes');
    if (!container) return;

    if (contador) contador.innerText = `${viajes.length} Buses Disponibles`;

    if (viajes.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding: 40px; color:#64748b; font-weight:500;">No se encontraron flotas para la ruta seleccionada.</div>';
        return;
    }

    let html = '';
    viajes.forEach(v => {
        html += `
            <div class="viaje-card-horizontal">
                <div class="viaje-img-wrapper">
                    <img src="${v.imagen}" alt="Bus" class="viaje-img">
                </div>
                <div class="viaje-info">
                    <div class="viaje-detalles">
                        <h3>${v.empresa}</h3>
                        <p><i class="fas fa-map-marker-alt"></i> ${v.origen} a ${v.destino}</p>
                        <p><i class="fas fa-clock"></i> Salida: ${v.hora_salida} — Llega en ${v.duracion}</p>
                        <p><i class="fas fa-couch"></i> ${v.asientos_disponibles} Asientos disponibles</p>
                    </div>
                    <div class="viaje-accion">
                        <div class="precio-tag"><span>Bs</span>${v.precio}</div>
                        <button class="btn-comprar" data-id="${v.id}" data-precio="${v.precio}" data-empresa="${v.empresa}" data-origen="${v.origen}" data-destino="${v.destino}">Seleccionar</button>
                    </div>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;

    document.querySelectorAll('.btn-comprar').forEach(btn => {
        btn.addEventListener('click', () => {
            localStorage.setItem('compraPendiente', JSON.stringify({
                id: btn.dataset.id, empresa: btn.dataset.empresa, origen: btn.dataset.origen, destino: btn.dataset.destino, precio: btn.dataset.precio
            }));
            window.location.href = '/pago';
        });
    });
}

let btnFiltrar = document.getElementById('btnFiltrar');
if (btnFiltrar) {
    btnFiltrar.addEventListener('click', () => {
        let ori = document.getElementById('filtroOrigen').value.toLowerCase();
        let des = document.getElementById('filtroDestino').value.toLowerCase();
        let filtrados = viajesData.filter(v => v.origen.toLowerCase().includes(ori) && v.destino.toLowerCase().includes(des));
        pintarViajes(filtrados);
    });
}

if (document.getElementById('resultadosPasajes')) {
    let fastSearch = JSON.parse(localStorage.getItem('busquedaRapida'));
    if (fastSearch) {
        document.getElementById('filtroOrigen').value = fastSearch.origen;
        document.getElementById('filtroDestino').value = fastSearch.destino;
        let filtrados = viajesData.filter(v => v.origen.toLowerCase().includes(fastSearch.origen.toLowerCase()) && v.destino.toLowerCase().includes(fastSearch.destino.toLowerCase()));
        setTimeout(() => { pintarViajes(filtrados); localStorage.removeItem('busquedaRapida'); }, 300);
    } else {
        setTimeout(() => { pintarViajes(viajesData); }, 300);
    }
}
 
// CONTROLADORES DE COMPRA Y TARJETA (PAGO) 
let resumenCompra = document.getElementById('resumenCompra');
if (resumenCompra) {
    let compra = JSON.parse(localStorage.getItem('compraPendiente'));
    if (compra) {
        resumenCompra.innerHTML = `<i class="fas fa-check-circle"></i> Destino confirmado: <strong>${compra.empresa}</strong> de ${compra.origen} a ${compra.destino}. Importe total: <strong>Bs ${compra.precio}</strong>`;
    } else {
        resumenCompra.innerHTML = `⚠️ No has seleccionado ningún ticket. Vuelve a la pestaña de Pasajes.`;
    }
}

document.querySelectorAll('.tab-trigger').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab-trigger').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).classList.add('active');
    });
});

let cardNameInput = document.getElementById('cardNameInput');
let cardNumberInput = document.getElementById('cardNumberInput');
let cardExpiryInput = document.getElementById('cardExpiryInput');

if (cardNameInput) {
    cardNameInput.addEventListener('input', (e) => { document.getElementById('cardNameView').innerText = e.target.value.toUpperCase() || 'JUAN PEREZ FLORES'; });
}
if (cardNumberInput) {
    cardNumberInput.addEventListener('input', (e) => { document.getElementById('cardNumberView').innerText = e.target.value || '•••• •••• •••• ••••'; });
}
if (cardExpiryInput) {
    cardExpiryInput.addEventListener('input', (e) => { document.getElementById('cardExpiryView').innerText = e.target.value || 'MM/AA'; });
}

let formPago = document.getElementById('formPago');
if (formPago) {
    formPago.addEventListener('submit', (e) => {
        e.preventDefault();
        alert("🔒 ¡Transacción exitosa! Tu pasaje digital PlusBus ha sido enviado.");
        localStorage.clear();
        window.location.href = '/';
    });
}
 
// VENTANAS EMERGENTES (TURISMO) 
function abrirPopUp(titulo, desc, img) {
    let popup = document.getElementById('popupTurismo');
    if (!popup) return;
    document.getElementById('popupTitle').innerText = titulo;
    document.getElementById('popupDesc').innerText = desc;
    document.getElementById('popupImg').src = img;
    popup.style.display = 'flex';
}

function cerrarPopUp() {
    let popup = document.getElementById('popupTurismo');
    if (popup) popup.style.display = 'none';
}

document.querySelectorAll('.filter-trigger-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-trigger-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        let cat = btn.dataset.filter;
        document.querySelectorAll('.photo-card').forEach(card => {
            if (cat === 'todos' || card.dataset.cat === cat) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});