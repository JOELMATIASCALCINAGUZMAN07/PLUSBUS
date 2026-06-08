// Aporte individual: clase para registrar los datos del pasajero
// dentro del sistema de reserva y compra de pasajes PlusBus Bolivia.

class Pasajero {
    constructor(nombreCompleto, tipoDocumento, numeroDocumento, correo, telefono) {
        this.nombreCompleto = nombreCompleto;
        this.tipoDocumento = tipoDocumento;
        this.numeroDocumento = numeroDocumento;
        this.correo = correo;
        this.telefono = telefono;
    }

    mostrarDatos() {
        return `Pasajero: ${this.nombreCompleto} | Documento: ${this.tipoDocumento} ${this.numeroDocumento} | Contacto: ${this.correo} - ${this.telefono}`;
    }
}

// Ejemplo de uso de la clase Pasajero
const pasajero1 = new Pasajero(
    "Waldo Cossio Cespedes",
    "CI",
    "12345678",
    "correo@ejemplo.com",
    "70000000"
);

console.log(pasajero1.mostrarDatos());
