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
 
// NUEVA CLASE: GESTOR DE DESCUENTOS  
class GestorDescuentos {
    constructor(precioBase) {
        // Almacena el costo original del pasaje recuperado
        this.precioBase = parseFloat(precioBase) || 0;
    }

    // IMPLEMENTACIÓN DEL MÉTODO COMPLEMENTARIO SOLICITADO
    calcularDescuento(codigo) {
        let descuento = 0;
        let codigoLimpio = codigo.trim().toUpperCase();

        // Lógica condicional analítica para evaluar cupones válidos
        if (codigoLimpio === "PLUSBUS2026") {
            descuento = this.precioBase * 0.15; // 15% Descuento Promocional General
        } else if (codigoLimpio === "ESTUDIANTE") {
            descuento = this.precioBase * 0.10; // 10% Descuento preferencial de estudiante
        }

        return descuento;
    }
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

    // Instancia global inicial del precio base para la lógica de negocio
    let precioOriginal = parseFloat(compraData.precio) || 0;

    // INYECCIÓN DE TEXTOS EN LOS NODOS DEL TICKET DIGITAL (Efecto espejo)
    if (compraData.origen) tOrigen.innerText = compraData.origen;
    if (compraData.destino) tDestino.innerText = compraData.destino;
    if (compraData.fecha) tFecha.innerText = compraData.fecha;
    if (compraData.hora) tHora.innerText = compraData.hora;
    if (compraData.empresa) tEmpresa.innerText = compraData.empresa;
    if (compraData.precio) tPrecio.innerText = precioOriginal;

    // INYECCIÓN DE VALORES EN EL CUADRO DE DETALLE DE TRANSACCIÓN
    if (compraData.origen && compraData.destino) {
        invRuta.innerText = `Pasaje: ${compraData.origen} a ${compraData.destino}`;
    }
    invMontoBase.innerText = precioOriginal;
    invMontoTotal.innerText = precioOriginal;

    // MANEJO E INTEGRACIÓN INTERACTIVA DE LA NUEVA CLASE DE DESCUENTOS
    let btnAplicarPromo = document.getElementById('btnAplicarPromo');
    let inputCodigoPromo = document.getElementById('codigoPromo');
    let filaDescuento = document.getElementById('invoiceFilaDescuento');
    let montoDescuentoTexto = document.getElementById('invoiceMontoDescuento');

    if (btnAplicarPromo && inputCodigoPromo) {
        btnAplicarPromo.addEventListener('click', () => {
            let codigoIngresado = inputCodigoPromo.value;

            // Creación del objeto basado en la nueva clase
            let gestor = new GestorDescuentos(precioOriginal);
            // Llamada interactiva al método de cálculo
            let ahorro = gestor.calcularDescuento(codigoIngresado);

            if (ahorro > 0) {
                let nuevoTotal = precioOriginal - ahorro;

                // Actualización en caliente de la interfaz y elementos gráficos de cobro
                montoDescuentoTexto.innerText = ahorro.toFixed(2);
                filaDescuento.classList.remove('oculto-promo');
                invMontoTotal.innerText = nuevoTotal.toFixed(2);
                tPrecio.innerText = nuevoTotal.toFixed(2); // Modifica también el boleto visual

                alert(`🎉 ¡Cupón Aplicado! Se ha descontado Bs ${ahorro.toFixed(2)} a tu saldo.`);
            } else {
                alert("❌ El código ingresado no es válido o ya caducó.");
                filaDescuento.classList.add('oculto-promo');
                invMontoTotal.innerText = precioOriginal;
                tPrecio.innerText = precioOriginal;
            }
        });
    }

    // GESTIÓN DE PESTAÑAS DE PAGO (TARJETA vs QR)
    let radioTarjeta = document.getElementById('radioTarjeta');
    let radioQR = document.getElementById('radioQR');

    if (radioTarjeta && radioQR) {
        radioTarjeta.addEventListener('change', alternarPanelesPago);
        radioQR.addEventListener('change', alternarPanelesPago);
    }

    // CAPTURA DEL SUBMIT DEL FORMULARIO
    let paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', procesarFormularioPago);
    }
});

// FUNCIÓN PARA CAMBIAR VISUALMENTE ENTRE FORMULARIO DE TARJETA O QR
function alternarPanelesPago() {
    let panelTarjeta = document.getElementById('panelTarjeta');
    let panelQR = document.getElementById('panelQR');
    let optCard = document.getElementById('optionCard');
    let optQR = document.getElementById('optionQR');

    if (document.getElementById('radioTarjeta').checked) {
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

    let totalPagarActual = document.getElementById('invoiceMontoTotal').innerText;
    let email = document.getElementById('emailPasajero').value;
    let nombre = document.getElementById('nombrePasajero').value;
    let metodo = document.querySelector('input[name="paymentMethod"]:checked').value;

    if (metodo === 'tarjeta') {
        let nro = document.getElementById('cardNumber').value;
        if (nro.replace(/\s+/g, '').length < 12) {
            alert('Por favor ingrese un número de tarjeta válido.');
            return;
        }
    }

    // ALERTAS DE ÉXITO ADAPTATIVAS SEGÚN EL MEDIO ELEGIDO
    if (metodo === 'tarjeta') {
        alert(`¡Pago Procesado Exitosamente!\n\nEstimado(a) ${nombre}, el cobro de Bs ${totalPagarActual} se realizó correctamente.\nTu boleto digital con código QR de embarque fue enviado a: ${email}`);
    } else {
        alert(`¡Código QR Generado!\n\nSe ha creado la orden de cobro por Bs ${totalPagarActual}. Al aprobarla desde tu app móvil bancaria se emitirá el pasaje a: ${email}`);
    }

    // Limpieza de memoria temporal y redirección de vuelta al home indexado
    localStorage.clear();
    window.location.href = '/';
}