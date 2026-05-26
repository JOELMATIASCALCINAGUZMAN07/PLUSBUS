
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

document.addEventListener('DOMContentLoaded', () => {
    // SE RECUPERAN LOS DATOS ALMACENADOS PREVIAMENTE
    let compraData = JSON.parse(localStorage.getItem('compraPendiente')) || {};
    
    // NODOS DEL COMPONENTE TICKET DIGITAL
    let tOrigen = document.getElementById('ticketOrigen');
    let tDestino = document.getElementById('ticketDestino');
    let tFecha = document.getElementById('ticketFecha');
    let tHora = document.getElementById('ticketHora');
    let tEmpresa = document.getElementById('ticketEmpresa');
    let tPrecio = document.getElementById('ticketPrecio');

    // NODOS DEL RESUMEN DE FACTURACIÓN
    let invRuta = document.getElementById('invoiceItemRuta');
    let invMontoBase = document.getElementById('invoiceMontoBase');
    let invMontoTotal = document.getElementById('invoiceMontoTotal');

    if (compraData.id) {
        // ACTUALIZACIÓN DE TEXTOS EN EL BOLETO VIRTUAL
        tOrigen.textContent = compraData.origen;
        tDestino.textContent = compraData.destino;
        tFecha.textContent = compraData.fecha || "26/02/2026";
        tHora.textContent = compraData.hora || "17:00";
        tEmpresa.textContent = compraData.empresa;
        tPrecio.textContent = compraData.precio;

        // ACTUALIZACIÓN EN EL RESUMEN DE COMPRA INFERIOR
        invRuta.textContent = `Pasaje: ${compraData.origen} a ${compraData.destino}`;
        invMontoBase.textContent = compraData.precio;
        invMontoTotal.textContent = compraData.precio;
    } else {
        // SI SE ENTRA SIN SELECCIONAR VIAJE, SE ENVIARÁ UN AVISO EN EL PANEL
        let formularioCompleto = document.getElementById('contenedorFormulario');
        formularioCompleto.innerHTML = `
            <div style="text-align: center; padding: 40px 20px;">
                <i class="fas fa-shopping-cart" style="font-size: 3.5rem; color: #ccc; margin-bottom: 20px;"></i>
                <h3 style="color: var(--blue-dark); margin-bottom: 10px;">Tu carrito está vacío</h3>
                <p style="color: var(--text-muted); margin-bottom: 25px;">No has seleccionado ningún boleto de bus todavía.</p>
                <a href="/pasajes" style="background-color: var(--blue-medium); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block;">Ver pasajes disponibles</a>
            </div>
        `;
    }

    // MÁSCARA AUTOMÁTICA EN EL CAMPO DE NÚMERO DE TARJETA
    let cardInput = document.getElementById('cardNumber');
    if (cardInput) {
        cardInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let matches = v.match(/\d{4,16}/g);
            let match = matches && matches[0] || '';
            let parts = [];

            for (let i = 0, len = match.length; i < len; i += 4) {
                parts.push(match.substring(i, i + 4));
            }

            if (parts.length > 0) {
                e.target.value = parts.join(' ');
            } else {
                e.target.value = v;
            }
        });
    }

    // ESCUCHADORES DE EVENTO "CHANGE" PARA ALTERNAR EL MÉTODO DE PAGO
    let radioTarjeta = document.getElementById('radioTarjeta');
    let radioQR = document.getElementById('radioQR');

    if (radioTarjeta && radioQR) {
        radioTarjeta.addEventListener('change', () => alternarMetodoPago('tarjeta'));
        radioQR.addEventListener('change', () => alternarMetodoPago('qr'));
    }

    // ESCUCHADOR DE ENVÍO DE FORMULARIO
    let formularioPago = document.getElementById('paymentForm');
    if (formularioPago) {
        formularioPago.addEventListener('submit', procesarFormularioPago);
    }
});
 
// FUNCIÓN PARA CONMUTAR VISIBILIDAD ENTRE PANELES DE TARJETA Y QR 
function alternarMetodoPago(tipo) {
    let panelTarjeta = document.getElementById('panelTarjeta');
    let panelQR = document.getElementById('panelQR');
    let optCard = document.getElementById('optionCard');
    let optQR = document.getElementById('optionQR');

    if (tipo === 'tarjeta') {
        panelTarjeta.classList.add('active');
        panelQR.classList.remove('active');
        optCard.classList.add('active');
        optQR.classList.remove('active');
    } else {
        panelTarjeta.classList.remove('active');
        panelQR.classList.add('active');
        optCard.classList.remove('active');
        optQR.classList.add('active');
    }
}
 
// PROCESAMIENTO Y VALIDACIÓN FINAL DE LA COMPRA 
function procesarFormularioPago(event) {
    event.preventDefault();
    
    let compraData = JSON.parse(localStorage.getItem('compraPendiente')) || {};
    let email = document.getElementById('emailPasajero').value;
    let nombre = document.getElementById('nombrePasajero').value;
    let metodo = document.querySelector('input[name="paymentMethod"]:checked').value;

    if (metodo === 'tarjeta') {
        let nro = document.getElementById('cardNumber').value;
        if (nro.length < 12) {
            alert('Por favor ingrese un número de tarjeta válido.');
            return;
        }
    }

    // ALERTAS DE ÉXITO ADAPTATIVAS SEGÚN EL MEDIO ELEGIDO
    if (metodo === 'tarjeta') {
        alert(`✅ ¡Pago Procesado Exitosamente!\n\nEstimado(a) ${nombre}, el cobro de Bs ${compraData.precio || 0} se realizó correctamente.\nTu boleto digital con código QR de embarque fue enviado a: ${email}`);
    } else {
        alert(`📲 ¡Código QR Generado!\n\nSe ha creado la orden de cobro en tu cuenta bancaria. Al aprobarla desde tu app móvil, tu pasaje digital se activará y llegará a: ${email}`);
    }

    // LIMPIEZA DE DATOS Y REDIRECCIÓN AL MENÚ PRINCIPAL
    localStorage.removeItem('compraPendiente');
    window.location.href = '/';
}