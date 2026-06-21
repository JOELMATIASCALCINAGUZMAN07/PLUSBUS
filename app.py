# Sistema de Gestión Autónoma de Pasajes y Turismo - PlusBus Bolivia

# Importación de CustomTkinter para una interfaz moderna y atractiva, junto con módulos estándar como re para validación de entradas y random para generar datos de prueba. CustomTkinter se utiliza para crear una experiencia de usuario más agradable y profesional, con estilos personalizados que reflejan la identidad visual de PlusBus Bolivia.
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import re
import random 

#CONFIGURACIÓN GLOBAL DE ESTILOS

COLOR_BLUE_DARK = "#0f2d59"     # Azul oscuro (Sidebar / Login)
COLOR_BLUE_MEDIUM = "#1d4ed8"   # Azul medio para énfasis y botones secundarios
COLOR_BLUE_LIGHT = "#dbeafe"    # Azul claro para etiquetas
COLOR_ORANGE = "#f97316"        # Naranja primario para botones de acción y precios
COLOR_BG_LIGHT = "#f8fafc"      # Fondo gris claro limpio para las vistas
COLOR_WHITE = "#ffffff"         # Blanco para tarjetas y contenedores de datos
COLOR_TEXT_DARK = "#1e293b"     # Gris oscuro para legibilidad de textos
COLOR_TEXT_MUTED = "#64748b"    # Gris apagado para etiquetas secundarias

# Configuración inicial del tema base de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Clase principal de la aplicación: Esta clase se encarga de inicializar la ventana principal, configurar la arquitectura de contenedores para el menú lateral y el área de contenido dinámico, y gestionar el estado centralizado del sistema autónomo PlusBus. Además, incluye funciones para activar la interfaz principal tras un inicio de sesión exitoso, dibujar el menú lateral con opciones de navegación y mostrar las diferentes vistas según la interacción del usuario.
class PlusBusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Parámetros de la ventana principal
        self.title("PlusBus Bolivia - Sistema de Gestión Autónoma")
        self.geometry("1100x650")
        self.configure(fg_color=COLOR_BG_LIGHT)
        
        # ESTADO CENTRALIZADO  
        # Este estado centralizado se utiliza para almacenar información relevante sobre los viajes disponibles, el historial de compras de la sesión, los usuarios registrados y el estado de autenticación. Al centralizar esta información en el controlador principal, se facilita la gestión de datos entre las diferentes vistas del sistema autónomo PlusBus, permitiendo una experiencia de usuario coherente y fluida a medida que navegan por las distintas secciones de la aplicación.
        self.viajes_data = [
            {"id": 1, "empresa": "Flota El Dorado", "origen": "La Paz", "destino": "Cochabamba", "precio": 90, "hora": "08:30", "fecha": "2026-06-20", "asientos_ocupados": [1, 2, 5, 12, 20]},
            {"id": 2, "empresa": "Trans Copacabana", "origen": "Cochabamba", "destino": "Santa Cruz", "precio": 130, "hora": "22:00", "fecha": "2026-06-21", "asientos_ocupados": [10, 11, 14, 30]},
            {"id": 3, "empresa": "Bolívar", "origen": "La Paz", "destino": "Oruro", "precio": 35, "hora": "14:15", "fecha": "2026-06-20", "asientos_ocupados": [3, 4, 7, 8, 9, 15]},
            {"id": 4, "empresa": "Flota Cosmos", "origen": "Sucre", "destino": "Potosí", "precio": 25, "hora": "10:00", "fecha": "2026-06-22", "asientos_ocupados": [22, 23]}
        ]
        
        # Historial dinámico de transacciones de la sesión
        self.historial_compras = []

        # Base de datos local en memoria para usuarios registrados 
        self.usuarios_registrados = {
            "admin": "1234",
            "invitado@plusbus.bo": "bolivia2026"
        }
        
        # Estado de control de acceso
        self.usuario_autenticado = False
        
        # Variables de estado para la búsqueda rápida y la compra pendiente, que se utilizan para almacenar temporalmente la información ingresada por el usuario en la vista de inicio y la selección de viaje en la vista de pasajes, respectivamente. Estas variables permiten mantener un flujo de datos coherente entre las diferentes vistas del sistema autónomo PlusBus, facilitando la navegación y la experiencia de usuario.
        self.busqueda_rapida = {}
        self.compra_pendiente = {}
        self.usuario_autenticado = False

        # ARQUITECTURA DE CONTENEDORES 
        # Menú Lateral (Inicialmente oculto por Login)
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=COLOR_BLUE_DARK)
        
        # Contenedor derecho para las páginas dinámicas
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Configuración de la cuadrícula para el contenedor principal, permitiendo que las vistas se expandan y llenen el espacio disponible de manera uniforme.
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.inicializar_vistas()

    def inicializar_vistas(self):
        self.frames = {}
        
        # Incluye LoginView dentro del diccionario de control de navegación
        for PageClass in (LoginView, InicioView, PasajesView, PagoView, TurismoView, HistorialView):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Fuerza la carga obligatoria de la pantalla de inicio de sesión
        self.show_frame("LoginView")

    # Función para activar la interfaz principal tras un inicio de sesión exitoso: Esta función se encarga de mostrar el sidebar de navegación y habilitar el acceso a las diferentes vistas del sistema autónomo PlusBus después de que el usuario haya sido autenticado correctamente. Al activar esta función, se actualiza el estado de autenticación del usuario, se muestra el menú lateral y se dibuja el contenido del sidebar, permitiendo así una navegación fluida entre las diferentes secciones del sistema.
    def activar_interfaz_principal(self):
        """Muestra el sidebar de navegación tras un inicio de sesión exitoso."""
        self.usuario_autenticado = True
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.dibujar_sidebar()
        self.show_frame("InicioView")

    def dibujar_sidebar(self):

        # Limpieza de widgets previos para evitar duplicación de memoria
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        # Diseño del menú lateral: El menú lateral se ha diseñado para ser visualmente atractivo y fácil de navegar, utilizando colores institucionales y una tipografía clara. El logo de PlusBus se muestra en la parte superior para reforzar la identidad de la marca, seguido de botones de navegación que permiten a los usuarios acceder rápidamente a las diferentes secciones del sistema. Cada botón está diseñado con un estilo consistente y un color que resalta su función, facilitando así la experiencia de usuario al interactuar con el menú lateral.
        logo_label = ctk.CTkLabel(self.sidebar, text="PlusBus", font=("Inter", 30, "bold"), text_color=COLOR_WHITE)
        logo_label.pack(pady=35, padx=20, anchor="w")
        
        # Botones de navegación: Cada botón en el menú lateral está diseñado para permitir a los usuarios acceder rápidamente a las diferentes secciones del sistema. Al hacer clic en cada botón, se activa la función "show_frame" con el nombre de la vista correspondiente, lo que permite una navegación fluida entre las diferentes partes de la aplicación. El diseño de los botones utiliza colores que resaltan su función, facilitando así la experiencia de usuario al interactuar con el menú lateral.
        self.btn_inicio = ctk.CTkButton(self.sidebar, text="Inicio", font=("arial", 18, "bold"), fg_color="transparent", text_color=COLOR_WHITE, height=45, anchor="w", command=lambda: self.show_frame("InicioView"))
        self.btn_inicio.pack(fill=tk.X, padx=15, pady=5)
        
        # Botón de pasajes: Este botón permite a los usuarios acceder a la sección de pasajes, donde pueden ver los resultados de su búsqueda rápida y seleccionar un viaje para proceder al pago. Al hacer clic en este botón, se activa la función "show_frame" con el nombre de la vista "PasajesView", lo que permite una navegación fluida hacia la sección de pasajes.
        self.btn_pasajes = ctk.CTkButton(self.sidebar, text="Pasajes", font=("arial", 18, "bold"), fg_color="transparent", text_color=COLOR_ORANGE, height=45, anchor="w", command=lambda: self.show_frame("PasajesView"))
        self.btn_pasajes.pack(fill=tk.X, padx=15, pady=5)

        # Botón de pago: Este botón permite a los usuarios acceder a la sección de pago, donde pueden completar la transacción para el viaje seleccionado. Al hacer clic en este botón, se activa la función "show_frame" con el nombre de la vista "PagoView", lo que permite una navegación fluida hacia la sección de pago. Este botón está diseñado con un color que resalta su función, facilitando así la experiencia de usuario al interactuar con el menú lateral.
        self.btn_pago = ctk.CTkButton(self.sidebar, text="Pagar", font=("arial", 18, "bold"), fg_color="transparent", text_color=COLOR_WHITE, height=45, anchor="w", command=lambda: self.show_frame("PagoView"))
        self.btn_pago.pack(fill=tk.X, padx=15, pady=5)
        
        # Botón de historial: Este botón permite a los usuarios acceder a la sección de historial, donde pueden ver un
        self.btn_historial = ctk.CTkButton(self.sidebar, text="📜   Historial", font=("Inter", 18, "bold"), fg_color="transparent", text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, height=45, anchor="w", command=lambda: self.show_frame("HistorialView"))
        self.btn_historial.pack(fill=tk.X, padx=15, pady=5)

        # Botón de turismo: Este botón permite a los usuarios acceder a la sección de turismo, donde pueden encontrar información sobre destinos turísticos en Bolivia y planificar sus viajes de manera autónoma. Al hacer clic en este botón, se activa la función "show_frame" con el nombre de la vista "TurismoView", lo que permite una navegación fluida hacia la sección de turismo. Este botón está diseñado con un color que resalta su función, facilitando así la experiencia de usuario al interactuar con el menú lateral.
        self.btn_turismo = ctk.CTkButton(self.sidebar, text="Guía", font=("arial", 18, "bold"), fg_color="transparent", text_color=COLOR_ORANGE,height=45, anchor="w", command=lambda: self.show_frame("TurismoView"))
        self.btn_turismo.pack(fill=tk.X, padx=15, pady=5)

    # Función para mostrar las diferentes vistas según la interacción del usuario: Esta función se encarga de gestionar la navegación entre las diferentes vistas del sistema autónomo PlusBus. Antes de mostrar una vista, se verifica si el usuario está autenticado; si no lo está y se intenta acceder a una vista diferente a la de inicio de sesión, se muestra un mensaje de acceso denegado. Si el usuario está autenticado o se accede a la vista de inicio de sesión, se muestra la vista correspondiente y, si la vista tiene una función específica para ejecutar al mostrarse (como actualizar datos o aplicar filtros), se llama a esa función para garantizar que la información mostrada esté actualizada y sea relevante para el usuario.
    def show_frame(self, page_name):
        
        # Bloqueo de seguridad: Si no está autenticado, no permite cambiar de vista
        if not self.usuario_autenticado and page_name != "LoginView":
            print("Acceso denegado: Autenticación requerida.")
            return

        # Navegación a la vista solicitada: Si el usuario está autenticado o se accede a la vista de inicio de sesión, se muestra la vista correspondiente. Además, si la vista tiene una función específica para ejecutar al mostrarse (como actualizar datos o aplicar filtros), se llama a esa función para garantizar que la información mostrada esté actualizada y sea relevante para el usuario.
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
            if hasattr(frame, "al_mostrar_vista"):
                frame.al_mostrar_vista()


#VISTA CENTRAL DE AUTENTICACIÓN (LOGIN obligatorio)
#El LoginView se integra como la primera pantalla que el usuario ve al iniciar la aplicación. Solo tras una autenticación exitosa, se muestra el menú lateral y se habilitan las demás vistas. Esto garantiza un flujo de acceso controlado y una experiencia de usuario coherente desde el inicio.
class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller

        # Estructura del LoginView: Se ha diseñado una estructura clara y centrada para la pantalla de inicio de sesión, con un card central que contiene el título, una breve descripción del sistema, los campos de entrada para el usuario y la contraseña, y los botones de acción para iniciar sesión o registrar una nueva cuenta. Esta estructura facilita la navegación y proporciona una experiencia de usuario intuitiva desde el primer contacto con la aplicación.
        login_card = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0",
            width=450,
            height=500
        )
        # El card de login se posiciona en el centro de la pantalla utilizando el método "place" con coordenadas relativas, lo que garantiza que se mantenga centrado independientemente del tamaño de la ventana. Además, se establece un tamaño fijo para el card y se desactiva la propagación de tamaño para mantener la consistencia visual y evitar que el contenido interno afecte las dimensiones del card.
        login_card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        login_card.pack_propagate(False)

        # Título principal del sistema, con un estilo destacado para resaltar la identidad de la plataforma y generar una primera impresión sólida en los usuarios. El uso de un ícono de autobús junto al nombre refuerza visualmente el propósito de la aplicación y crea una conexión inmediata con el tema de transporte y viajes.
        ctk.CTkLabel(
            login_card,
            text="🚌 PlusBus Bolivia",
            font=("Inter", 45, "bold"),
            text_color=COLOR_BLUE_DARK
        ).pack(pady=(35, 5))

        # Descripción breve del sistema, con un estilo que complementa el título y resalta la propuesta de valor de la plataforma, para generar interés y motivar a los usuarios a iniciar sesión.
        ctk.CTkLabel(
            login_card,
            text="Gestión de Pasajes y Turismo Autónomo",
            font=("Inter", 15),
            text_color=COLOR_ORANGE
        ).pack(pady=(0, 25))

        # Campo de entrada para el nombre de usuario o correo electrónico, con un diseño que incluye un borde destacado para mejorar la visibilidad y un placeholder que indica claramente que se debe ingresar un correo electrónico o nombre de usuario válido. Este campo es esencial para identificar al usuario y permitir el acceso al sistema, asegurando que solo personas autorizadas puedan ingresar.
        ctk.CTkLabel(
            login_card,
            text="Nombre de Usuario / Correo",
            font=("Inter", 15, "bold"),
            text_color=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=40, pady=(10, 2))

        # Campo de entrada para el nombre de usuario o correo electrónico, con un diseño que incluye un borde destacado para mejorar la visibilidad y un placeholder que indica claramente que se debe ingresar un correo electrónico o nombre de usuario válido. Este campo es esencial para identificar al usuario y permitir el acceso al sistema, asegurando que solo personas autorizadas puedan ingresar.
        self.entry_user = ctk.CTkEntry(
            login_card,
            height=38,
            corner_radius=35,
           text_color=COLOR_TEXT_DARK,
            fg_color=COLOR_BG_LIGHT,
            border_color=COLOR_BLUE_DARK,
            placeholder_text="ejemplo@sistema.com"
        )
        self.entry_user.pack(fill=tk.X, padx=40, pady=5)
        
        # Campo de entrada para el nombre de usuario o correo electrónico, con un diseño que incluye un borde destacado para mejorar la visibilidad y un placeholder que indica claramente que se debe ingresar un correo electrónico o nombre de usuario válido. Este campo es esencial para identificar al usuario y permitir el acceso al sistema, asegurando que solo personas autorizadas puedan ingresar.
        ctk.CTkLabel(
            login_card,
            text="Contraseña de Acceso",
            font=("Inter", 15, "bold"),
            text_color=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=40, pady=(10, 2))

        # Campo de entrada para la contraseña, con un diseño que oculta el texto ingresado para mayor seguridad. Este campo es esencial para proteger la información de acceso del usuario y garantizar que solo personas autorizadas puedan ingresar al sistema. El diseño incluye un borde destacado para mejorar la visibilidad y un placeholder que indica claramente que se debe ingresar una contraseña.
        self.entry_pass = ctk.CTkEntry(
            login_card,
            height=38,
           text_color=COLOR_TEXT_DARK,
            fg_color=COLOR_BG_LIGHT,
            corner_radius=35,
            border_color=COLOR_BLUE_DARK,
            show="*",
            placeholder_text="••••••••"
        )
        self.entry_pass.pack(fill=tk.X, padx=40, pady=5)
        
        # Botón de inicio de sesión: Este botón se encuentra debajo de los campos de entrada para el usuario y la contraseña. Al hacer clic en este botón, se activa la función "validar_credenciales" que se encarga de verificar la información ingresada por el usuario. Si las credenciales son válidas, se muestra un mensaje de bienvenida y se activa la interfaz principal del sistema autónomo PlusBus. En un sistema real, aquí se implementaría la lógica de autenticación contra una base de datos o servicio externo para verificar las credenciales ingresadas por el usuario.
        ctk.CTkButton(
            login_card,
            text="Iniciar Sesión",
            font=("Inter", 17, "bold"),
            fg_color=COLOR_BLUE_DARK,
            text_color=COLOR_WHITE,
            hover_color=COLOR_BLUE_MEDIUM,
            height=42,
            command=self.validar_credenciales
        ).pack(fill=tk.X, padx=40, pady=(30, 5))

        # Botón de registro: Este botón se encuentra debajo del botón de inicio de sesión y se encarga de redirigir a los usuarios a un proceso de registro para crear una nueva cuenta. Al hacer clic en este botón, se muestra un mensaje informativo indicando que el módulo de creación de cuentas ha sido sincronizado con éxito. En un sistema real, aquí se implementaría la lógica para permitir a los usuarios registrarse y crear una cuenta en el sistema.
        ctk.CTkButton(
            login_card,
            text="Registrar Nueva Cuenta",
            font=("Inter", 17),
            fg_color="transparent",
            text_color=COLOR_ORANGE,
            command=self.registrar_usuario
        ).pack(pady=5)

        # Mensaje de prueba para facilitar el acceso rápido durante el desarrollo, indicando a los usuarios que pueden usar las credenciales "admin" y "1234" para iniciar sesión rápidamente. Este mensaje es útil para pruebas internas y puede ser eliminado o modificado en la versión final del sistema.
    def validar_credenciales(self):
        usuario = self.entry_user.get().strip()
        contra = self.entry_pass.get().strip()

        # Validación de campos vacíos: Antes de verificar las credenciales, se realiza una validación para asegurarse de que los campos de usuario y contraseña no estén vacíos. Si alguno de los campos está vacío, se muestra un mensaje de advertencia indicando que ambos campos son necesarios para autenticarse en el sistema. Esta validación ayuda a mejorar la experiencia del usuario al proporcionar una guía clara sobre cómo proceder y evita intentos de inicio de sesión con información incompleta.
        if not usuario or not contra:
            messagebox.showwarning("Campos Vacíos", "Por favor, introduzca sus datos para autenticarse en el sistema.")
            return

         # Validación de credenciales: Esta función se encarga de verificar la información ingresada por el usuario en los campos de usuario y contraseña. Primero, se verifica que ambos campos no estén vacíos, mostrando un mensaje de advertencia si alguno de los campos está vacío. Luego, se verifica si el nombre de usuario ingresado existe en la base de datos local de usuarios registrados. Si el usuario existe, se compara la contraseña ingresada con la contraseña almacenada para ese usuario. Si las credenciales son correctas, se muestra un mensaje de bienvenida y se activa la interfaz principal del sistema autónomo PlusBus. Si las credenciales son incorrectas o el usuario no existe, se muestran mensajes de error correspondientes para informar al usuario sobre el problema.
        if usuario in self.controller.usuarios_registrados:
            if self.controller.usuarios_registrados[usuario] == contra:
                messagebox.showinfo("Acceso Concedido", f"Bienvenido al sistema autónomo PlusBus, {usuario}.")
                self.controller.activar_interfaz_principal()
            else:
                messagebox.showerror("Error de Acceso", "Contraseña incorrecta. Inténtelo de nuevo.")
        else:
            messagebox.showerror("Error de Acceso", "El usuario ingresado no existe. Regístrelo usando el botón inferior.")
    
    # la función "registrar_usuario" se encarga de manejar el proceso de registro de nuevos usuarios en el sistema autónomo PlusBus. Esta función realiza varias validaciones para garantizar la calidad de las cuentas registradas, como verificar que los campos de usuario y contraseña no estén vacíos, asegurarse de que la contraseña tenga un nivel mínimo de seguridad (al menos 4 caracteres) y comprobar que el nombre de usuario no esté duplicado en la base de datos local. Si todas las validaciones son exitosas, se registra la nueva cuenta en la base de datos local y se muestra un mensaje de confirmación al usuario.
    def registrar_usuario(self):
        usuario = self.entry_user.get().strip()
        contra = self.entry_pass.get().strip()
        
        # Validación de campos vacíos y seguridad de contraseña: Antes de registrar una nueva cuenta, se verifica que los campos de usuario y contraseña no estén vacíos. Si alguno de los campos está vacío, se muestra un mensaje de advertencia indicando que ambos campos son requeridos para el registro. Además, se verifica que la contraseña tenga al menos 4 caracteres para garantizar un nivel mínimo de seguridad. Si la contraseña es demasiado corta, se muestra un mensaje de advertencia indicando que la contraseña debe tener por lo menos 4 caracteres. Estas validaciones ayudan a mejorar la calidad de las cuentas registradas y a proporcionar una experiencia de usuario más segura.
        if not usuario or not contra:
            messagebox.showwarning("Campos Requeridos", "Para registrar una cuenta, escriba el usuario y contraseña deseados en las cajas de texto superiores.")
            return
        
        if len(contra) < 4:
            messagebox.showwarning("Seguridad Débil", "La contraseña debe tener por lo menos 4 caracteres.")
            return

        # Verificación de usuario duplicado: Antes de registrar una nueva cuenta, se verifica si el nombre de usuario ingresado ya existe en la base de datos local de usuarios registrados. Si el usuario ya está registrado, se muestra un mensaje de advertencia indicando que el nombre de usuario ya está en uso y se sugiere intentar iniciar sesión en su lugar. Esto ayuda a prevenir la creación de cuentas duplicadas y mejora la experiencia del usuario al proporcionar una guía clara sobre cómo proceder.
        if usuario in self.controller.usuarios_registrados:
            messagebox.showwarning("Registro Duplicado", "Este nombre de usuario ya está registrado. Intente iniciar sesión.")
        else:
            self.controller.usuarios_registrados[usuario] = contra
            messagebox.showinfo("Registro Exitoso", f"Cuenta para '{usuario}' guardada correctamente.\n¡Ya puede iniciar sesión!")

#PÁGINA 1: INICIO
#La vista de inicio se ha diseñado para ser la primera experiencia que el usuario tiene al ingresar al sistema. Aquí se presenta un formulario de búsqueda rápida que permite a los usuarios ingresar su ciudad de origen y destino para encontrar flotas disponibles. Además, se ha incluido un botón de intercambio para facilitar la corrección rápida de las ciudades ingresadas. Esta página actúa como el punto de partida para la navegación hacia la sección de pasajes, donde se mostrarán los resultados filtrados según la búsqueda realizada.
class InicioView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller
        
        # Estructura de la vista de inicio: Se ha diseñado una estructura clara y atractiva para la vista de inicio, que incluye un título principal, una breve descripción del sistema y un formulario de búsqueda rápida para que los usuarios puedan ingresar su ciudad de origen y destino. Además, se ha incluido un botón de intercambio para facilitar la corrección rápida de las ciudades ingresadas. Esta estructura permite a los usuarios comenzar su experiencia en el sistema autónomo PlusBus de manera intuitiva y eficiente.
        ctk.CTkLabel(self, text="Busca tus pasajes en Bolivia", font=("arial", 38, "bold"), text_color=COLOR_BLUE_DARK).pack(pady=(40, 5))
        ctk.CTkLabel(self, text="Viaja de forma rápida, segura y completamente autónoma", font=("Inter", 22), text_color=COLOR_TEXT_MUTED).pack(pady=(0, 30))
        
        # Card de búsqueda rápida: Este card se ha diseñado para ser visualmente atractivo y funcional, con un fondo blanco, bordes redondeados y un diseño limpio que resalta los campos de entrada y el botón de búsqueda. El card está centrado en la pantalla para facilitar la interacción del usuario y se ha configurado con un tamaño fijo para mantener la consistencia visual. Dentro del card, se encuentran los campos de entrada para la ciudad de origen y destino, así como un botón de intercambio para facilitar la corrección rápida de las ciudades ingresadas. Esta sección actúa como el punto de partida para que los usuarios puedan buscar flotas disponibles según sus necesidades.
        form_card = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=35, border_width=1, border_color="#e2e8f0", width=570, height=360)
        form_card.pack(pady=20, padx=40)
        form_card.pack_propagate(False)

        # Variables de control para los campos de origen y destino, con valores predeterminados para facilitar pruebas rápidas
        self.origen_var = tk.StringVar(value="La Paz")
        self.destino_var = tk.StringVar(value="Cochabamba")

        # Campo de Origen
        ctk.CTkLabel(form_card, text="Ciudad de Origen", font=("Inter", 20, "bold"), text_color=COLOR_TEXT_DARK).pack(pady=(25, 2), padx=30, anchor="w")
        self.entry_origen = ctk.CTkEntry(form_card, textvariable=self.origen_var, height=40, corner_radius=35, fg_color=COLOR_BG_LIGHT, text_color=COLOR_TEXT_DARK, border_color="#cbd5e1")
        self.entry_origen.pack(fill=tk.X, padx=30, pady=5)

        # Botón de intercambio: Permite a los usuarios corregir rápidamente su búsqueda sin tener que reescribir ambos campos. Esto mejora la experiencia del usuario al facilitar ajustes rápidos en la búsqueda de pasajes.
        self.btn_swap = ctk.CTkButton(form_card, text="Intercambiar Ciudades", font=("Inter", 20), fg_color="transparent", text_color=COLOR_BLUE_MEDIUM, hover_color="#eff6ff", width=150, command=self.swap_locations)
        self.btn_swap.pack(pady=5)

        ctk.CTkLabel(form_card, text="Ciudad de Destino", font=("Inter", 20, "bold"), text_color=COLOR_TEXT_DARK).pack(pady=(5, 2), padx=30, anchor="w")
        self.entry_destino = ctk.CTkEntry(form_card, textvariable=self.destino_var,corner_radius=35, height=40, fg_color=COLOR_BG_LIGHT, text_color=COLOR_TEXT_DARK, border_color="#cbd5e1")
        self.entry_destino.pack(fill=tk.X, padx=30, pady=5)
        
        # Botón de búsqueda: Al hacer clic en este botón, se recopilan los valores ingresados en los campos de origen y destino, se almacenan en el estado centralizado del controlador bajo la clave "busqueda_rapida" y luego se navega automáticamente a la vista de pasajes (PasajesView) para mostrar los resultados filtrados según la búsqueda realizada. Esto crea un flujo de navegación intuitivo desde la búsqueda inicial hasta la visualización de las opciones disponibles.
        btn_buscar = ctk.CTkButton(form_card, text="Buscar Flotas Disponibles", font=("Inter", 20, "bold"), fg_color=COLOR_ORANGE, text_color=COLOR_WHITE, hover_color="#ea580c", height=45, command=self.buscar_viaje)
        btn_buscar.pack(fill=tk.X, padx=30, pady=25)
        
    # Función de intercambio: Esta función se activa cuando el usuario hace clic en el botón "Intercambiar Ciudades". Toma los valores actuales de los campos de origen y destino, los intercambia y actualiza los campos de entrada con los nuevos valores. Esto permite a los usuarios corregir rápidamente su búsqueda sin tener que reescribir ambos campos, mejorando así la experiencia del usuario al facilitar ajustes rápidos en la búsqueda de pasajes.
    def swap_locations(self):
        ori = self.origen_var.get()
        des = self.destino_var.get()
        self.origen_var.set(des)
        self.destino_var.set(ori)

    # Función de búsqueda: Al hacer clic en el botón de búsqueda, esta función recopila los valores ingresados en los campos de origen y destino, los almacena en el estado centralizado del controlador bajo la clave "busqueda_rapida" y luego navega automáticamente a la vista de pasajes (PasajesView) para mostrar los resultados filtrados según la búsqueda realizada. Esto crea un flujo de navegación intuitivo desde la búsqueda inicial hasta la visualización de las opciones disponibles.
    def buscar_viaje(self):
        self.controller.busqueda_rapida = {
            "origen": self.origen_var.get().strip(),
            "destino": self.destino_var.get().strip()
        }
        self.controller.show_frame("PasajesView")

#PÁGINA 2: LISTADO DE SALIDAS
class PasajesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=20, fg_color=COLOR_BG_LIGHT)
        self.controller = controller

        # Estructura de la vista: Se ha diseñado una estructura clara y organizada para la vista de pasajes, que incluye un encabezado con el título y un contador dinámico de resultados, seguido de un contenedor scrollable donde se mostrarán las tarjetas de cada viaje disponible. Esto permite a los usuarios navegar fácilmente por las opciones de viaje y obtener información relevante de manera rápida.
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill=tk.X, padx=30, pady=(30, 10))
        
        # Título principal de la sección, con un estilo destacado para resaltar la importancia de los resultados mostrados.
        self.titulo_label = ctk.CTkLabel(self.header_frame, text="Resultados de Salidas Disponibles", font=("Inter", 25, "bold"), text_color=COLOR_BLUE_DARK)
        self.titulo_label.pack(side=tk.LEFT)
        
        # Contador dinámico de resultados encontrados, que se actualiza cada vez que se muestra la vista de pasajes para reflejar el número de flotas disponibles según el filtro de búsqueda aplicado. Esto proporciona a los usuarios una referencia inmediata sobre la cantidad de opciones que tienen para elegir.
        self.contador_label = ctk.CTkLabel(self.header_frame, text="0 flotas encontradas", font=("Inter", 18, "bold"), fg_color=COLOR_BLUE_LIGHT, text_color=COLOR_BLUE_MEDIUM, corner_radius=9, height=26, padx=10)
        self.contador_label.pack(side=tk.RIGHT)
        
        # Contenedor scrollable para las tarjetas de viaje: Este contenedor permite mostrar una lista de viajes disponibles que puede ser más larga que el espacio visible en la pantalla. Al ser scrollable, los usuarios pueden desplazarse hacia abajo para ver todas las opciones sin que la interfaz se sature, manteniendo una experiencia de usuario fluida y organizada.
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    # Al mostrar la vista de pasajes, esta función se encarga de limpiar cualquier resultado previo, aplicar el filtro de búsqueda rápida almacenado en el controlador para mostrar solo los viajes que coincidan con el origen y destino ingresados por el usuario, actualizar el contador de resultados encontrados y generar dinámicamente las tarjetas de cada viaje disponible. Si no se encuentran resultados, se muestra un mensaje informativo al usuario.
    def al_mostrar_vista(self):
        # Limpieza de resultados previos para evitar acumulación de tarjetas al navegar entre vistas
        for widget in self.scroll_container.winfo_children():
            widget.destroy()
          
        filtro = self.controller.busqueda_rapida
        # Aplicación del filtro de búsqueda rápida: Se verifica si hay un filtro de búsqueda rápida almacenado en el controlador. Si existe, se filtran los viajes disponibles en el estado centralizado para mostrar solo aquellos que coincidan con el origen y destino ingresados por el usuario. Esto permite a los usuarios ver solo las opciones relevantes según su búsqueda, mejorando la experiencia de navegación y facilitando la toma de decisiones al elegir un viaje.
        if filtro:
            viajes_filtrados = [
                v for v in self.controller.viajes_data 
                if filtro["origen"].lower() in v["origen"].lower() and 
                   filtro["destino"].lower() in v["destino"].lower()
            ]
        else:
            viajes_filtrados = self.controller.viajes_data

        self.contador_label.configure(text=f"{len(viajes_filtrados)} flotas encontradas")
        # Generación dinámica de tarjetas de viaje: Para cada viaje que cumple con el filtro de búsqueda, se crea una tarjeta visual que muestra información relevante como la empresa, ruta, horario y precio. Cada tarjeta también incluye un botón de acción que permite a los usuarios seleccionar el viaje y proceder al pago. Esto facilita la navegación y selección de opciones para los usuarios, proporcionando una experiencia interactiva y visualmente atractiva.
        if not viajes_filtrados:
            no_results = ctk.CTkLabel(self.scroll_container, text="❌ No se encontraron flotas para la ruta seleccionada.", font=("Inter", 17), text_color=COLOR_TEXT_MUTED)
            no_results.pack(pady=40)
            return
        # Creación de tarjetas para cada viaje filtrado, mostrando información relevante y un botón de acción para seleccionar el viaje y proceder al pago.
        for viaje in viajes_filtrados:
            card = ctk.CTkFrame(self.scroll_container, fg_color=COLOR_WHITE, corner_radius=15, border_width=1, border_color="#e2e8f0", height=100)
            card.pack(fill=tk.X, pady=8, padx=5)
            
            # Componente de información del viaje: Este componente se encarga de mostrar los detalles relevantes de cada viaje, como la empresa, ruta, horario y precio. Se organiza de manera clara y visualmente atractiva para facilitar la lectura y comprensión por parte de los usuarios.
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side=tk.LEFT, padx=20, pady=15, fill=tk.BOTH, expand=True)
            
            #Filtrado de Asientos Libres (Capacidad máxima estándar: 40 asientos)
            asientos_libres = [str(n) for n in range(1, 41) if n not in viaje["asientos_ocupados"]]
            
            # Información del viaje: Se muestra la empresa, ruta, horario y precio de cada viaje en un formato claro y organizado para facilitar la lectura por parte de los usuarios. Esto les permite comparar rápidamente las opciones disponibles y tomar decisiones informadas al seleccionar un viaje.
            selector_frame = ctk.CTkFrame(card, fg_color="transparent")
            selector_frame.pack(side=tk.RIGHT, padx=10, pady=15, fill=tk.Y)
            
            # Información del viaje: Se muestra la empresa, ruta, horario y precio de cada viaje en un formato claro y organizado para facilitar la lectura por parte de los usuarios. Esto les permite comparar rápidamente las opciones disponibles y tomar decisiones informadas al seleccionar un viaje.
            ctk.CTkLabel(selector_frame, text="Asiento:", font=("Inter", 11, "bold"), text_color=COLOR_TEXT_DARK).pack(anchor="w")
            combo_asiento = ctk.CTkComboBox(selector_frame, values=asientos_libres, width=80, height=28, state="readonly")
            combo_asiento.set(asientos_libres[0] if asientos_libres else "Lleno")
            combo_asiento.pack(pady=2)
            
            # Información del viaje: Se muestra la empresa, ruta, horario y precio de cada viaje en un formato claro y organizado para facilitar la lectura por parte de los usuarios. Esto les permite comparar rápidamente las opciones disponibles y tomar decisiones informadas al seleccionar un viaje.
            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)
            
            ctk.CTkLabel(action_frame, text=f"Bs {viaje['precio']}", font=("Inter", 20, "bold"), text_color=COLOR_ORANGE).pack(anchor="e")
            
            # Se vincula el combo_asiento a la función de transferencia
            btn_comprar = ctk.CTkButton(action_frame, text="Seleccionar", font=("Inter", 12, "bold"), fg_color=COLOR_BLUE_DARK, text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, width=100, height=32, command=lambda v=viaje, cb=combo_asiento: self.ir_a_pagar(v, cb))
            btn_comprar.pack(pady=(5, 0))

            # Al hacer clic en el botón "Seleccionar", se activa la función "ir_a_pagar" que toma como parámetros el viaje seleccionado y el combo box de asientos. Esta función verifica si el asiento elegido está disponible y, si es así, empaqueta toda la información relevante del viaje junto con el asiento seleccionado en el estado centralizado del controlador bajo la clave "compra_pendiente". Luego, navega automáticamente a la vista de pago (PagoView) para que el usuario pueda completar la transacción. Si el asiento elegido no está disponible o no se ha seleccionado un asiento, se muestra un mensaje de advertencia al usuario.

def ir_a_pagar(self, viaje, combo_asiento):
        asiento_elegido = combo_asiento.get()
        if asiento_elegido == "Lleno" or not asiento_elegido:
            messagebox.showwarning("Sin Espacio", "Esta flota no dispone de asientos libres.")
            return
            
        # Empaquetamos los parámetros lógicos incluyendo el asiento seleccionado
        self.controller.compra_pendiente = {
            "viaje_id": viaje["id"],
            "empresa": viaje["empresa"],
            "origen": viaje["origen"],
            "destino": viaje["destino"],
            "precio": viaje["precio"],
            "hora": viaje["hora"],
            "fecha": viaje["fecha"],
            "asiento": int(asiento_elegido)
        }
        self.controller.show_frame("PagoView")

#PÁGINA 3: PROCESAMIENTO DE PAGO ÚNICO POR TARJETA
class PagoView(ctk.CTkFrame):

    # La vista de pago se ha diseñado para ofrecer una experiencia de compra segura y fluida, centrada en un único método de pago autorizado: tarjeta de crédito o débito. Se ha eliminado la opción de QR para simplificar el proceso
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=25, fg_color=COLOR_BG_LIGHT)
        self.controller = controller
        
        ctk.CTkLabel(self, text="Completar Pago Seguro", font=("Inter", 24, "bold"), text_color=COLOR_BLUE_DARK).pack(pady=(30, 10), padx=30, anchor="w")
        
        # Descripción clara del proceso de pago, destacando la seguridad y la simplicidad del método de pago autorizado, para generar confianza en los usuarios y facilitar la finalización de la compra.
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        self.grid_container.grid_columnconfigure(0, weight=1, uniform="group1") 
        self.grid_container.grid_columnconfigure(1, weight=1, uniform="group1") 
        self.grid_container.grid_rowconfigure(0, weight=1)
        
        #COLUMNA 1: FORMULARIO
        form_side = ctk.CTkFrame(self.grid_container, fg_color=COLOR_WHITE, corner_radius=25, border_width=1, border_color="#e5e7eb")
        form_side.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=10)

        # Contenedor interno para el formulario de pago: Este contenedor se encuentra dentro del lado izquierdo de la vista de pago y se encarga de organizar los campos de entrada para los datos del pasajero, así como la información sobre el método de pago autorizado. Se ha diseñado con un estilo limpio y organizado para facilitar la introducción de datos por parte del usuario, mejorando así la experiencia de compra.
        form_inner = ctk.CTkFrame(form_side, fg_color="transparent")
        form_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(form_inner, text="Datos del Pasajero", font=("Inter", 23, "bold"), text_color=COLOR_BLUE_DARK).pack(anchor="w", pady=(0, 15))

        # Campos de entrada para el nombre completo y correo electrónico del pasajero, con un diseño limpio y organizado para facilitar la introducción de datos por parte del usuario. Estos campos son esenciales para emitir el boleto digital y enviar la información de embarque al correo proporcionado.
        ctk.CTkLabel(form_inner, text="Nombre Completo", font=("Inter", 16, "bold"),text_color=COLOR_TEXT_DARK).pack(anchor="w", pady=(5, 2))
        self.entry_nombre = ctk.CTkEntry(form_inner, height=38, fg_color=COLOR_BG_LIGHT, border_color="#cbd5e1")
        self.entry_nombre.pack(fill=tk.X, pady=(0, 15))
        
        # Campo de entrada para el correo electrónico del pasajero, con un diseño limpio y organizado para facilitar la introducción de datos por parte del usuario. Este campo es esencial para emitir el boleto digital y enviar la información de embarque al correo proporcionado.
        ctk.CTkLabel(form_inner, text="Correo Electrónico", font=("Inter", 16, "bold"),text_color=COLOR_TEXT_DARK).pack(anchor="w", pady=(5, 2))
        self.entry_email = ctk.CTkEntry(form_inner, height=38, fg_color=COLOR_BG_LIGHT, border_color="#cbd5e1")
        self.entry_email.pack(fill=tk.X, pady=(0, 20))
         
        ctk.CTkLabel(form_inner, text="Método de Pago Autorizado", font=("Inter", 16, "bold"), text_color=COLOR_BLUE_DARK).pack(anchor="w", pady=(5, 8))
        
        #   Información sobre el método de pago autorizado: Se muestra un mensaje claro y visualmente destacado que indica que el único método de pago autorizado es a través de tarjeta de crédito o débito. Esto ayuda a establecer expectativas claras para los usuarios y a generar confianza en la seguridad del proceso de pago.
        self.lbl_metodo_unico = ctk.CTkLabel(form_inner, text="💳  Tarjeta de Crédito / Débito", font=("Inter", 16, "bold"), text_color=COLOR_BLUE_MEDIUM)
        self.lbl_metodo_unico.pack(anchor="w", pady=6)
        
        #COLUMNA 2: RESUMEN / TICKET DIGITAL
        self.ticket_side = ctk.CTkFrame(self.grid_container, fg_color=COLOR_BLUE_DARK, corner_radius=25)
        self.ticket_side.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=10)
        
        # Contenedor interno para el resumen del viaje y el ticket digital: Este contenedor se encuentra dentro del lado derecho de la vista de pago y se encarga de mostrar un resumen detallado del viaje seleccionado, incluyendo información como la empresa, ruta, horario y precio. Además, proporciona un espacio para mostrar el ticket digital con un código QR de embarque una vez que se haya procesado el pago. Se ha diseñado con un estilo visualmente atractivo para resaltar la información importante y mejorar la experiencia de compra.
        ticket_inner = ctk.CTkFrame(self.ticket_side, fg_color="transparent")
        ticket_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Título del ticket digital, con un estilo destacado para resaltar la importancia de esta sección y generar entusiasmo en los usuarios al completar su compra.
        self.ticket_titulo = ctk.CTkLabel(ticket_inner, text="🎫 Ticket Digital", font=("Inter", 23, "bold"), text_color=COLOR_WHITE)
        self.ticket_titulo.pack(anchor="w", pady=(0, 15))
        
        #Label para mostrar la información del viaje seleccionado y el resumen de la compra, con un diseño claro y organizado para facilitar la lectura y comprensión por parte de los usuarios. Este label se actualizará dinámicamente al mostrar la vista de pago para reflejar los detalles del viaje seleccionado.
        self.ticket_info = ctk.CTkLabel(ticket_inner, text="No hay ningún viaje seleccionado.", font=("Inter", 18), text_color=COLOR_BLUE_LIGHT, justify="left", anchor="w")
        self.ticket_info.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botón para procesar el pago: Este botón se encuentra debajo del resumen del viaje y se encarga de iniciar el proceso de pago cuando el usuario hace clic en él. Al hacer clic, se recopilan los datos ingresados por el usuario, se valida la información y se muestra un mensaje de confirmación de la transacción. Además, se actualiza el estado centralizado del controlador para reflejar que la compra ha sido procesada y se navega automáticamente a la vista de inicio para que el usuario pueda realizar nuevas búsquedas o compras.
        self.btn_pagar = ctk.CTkButton(ticket_inner, text="Confirmar Transacción", font=("Inter", 18, "bold"), fg_color=COLOR_ORANGE,corner_radius=25,text_color=COLOR_WHITE, hover_color="#ea580c", height=45, command=self.procesar_pago)
        self.btn_pagar.pack(fill=tk.X, pady=(15, 0))

    # Al mostrar la vista de pago, esta función se encarga de verificar si hay un viaje seleccionado en el estado centralizado del controlador bajo la clave "compra_pendiente". Si existe un viaje seleccionado, se muestra un resumen detallado del viaje, incluyendo información como la empresa, ruta, horario y precio. Además, se habilita el botón de confirmación de la transacción para que el usuario pueda proceder con el pago. Si no hay ningún viaje seleccionado, se muestra un mensaje informativo indicando que la orden está vacía y se deshabilita el botón de pago para evitar que los usuarios intenten procesar una compra sin haber seleccionado un viaje.
    def al_mostrar_vista(self):
        compra = self.controller.compra_pendiente

        # Verificación de compra pendiente: Al mostrar la vista de pago, se verifica si hay un viaje seleccionado en el estado centralizado del controlador bajo la clave "compra_pendiente". Si existe un viaje seleccionado, se muestra un resumen detallado del viaje, incluyendo información como la empresa, ruta, horario y precio. Además, se habilita el botón de confirmación de la transacción para que el usuario pueda proceder con el pago. Si no hay ningún viaje seleccionado, se muestra un mensaje informativo indicando que la orden está vacía y se deshabilita el botón de pago para evitar que los usuarios intenten procesar una compra sin haber seleccionado un viaje.
        if compra:
            resumen = f"Empresa:\n{compra['empresa']}\n\nOrigen:\n{compra['origen']}\n\nDestino:\n{compra['destino']}\n\nFecha y Hora:\n{compra['fecha']} - {compra['hora']}\n\n═══════════════════════\nMonto Total:  Bs {compra['precio']}"
            self.ticket_info.configure(text=resumen)
            self.btn_pagar.configure(state=tk.NORMAL, fg_color=COLOR_ORANGE)
        else:
            self.ticket_info.configure(text="⚠️ Tu orden está vacía.\nPor favor regresa a la sección de pasajes y escoge una salida.")
            self.btn_pagar.configure(state=tk.DISABLED, fg_color="#94a3b8")

            # Función de procesamiento de pago: Esta función se activa cuando el usuario hace clic en el botón "Confirmar Transacción". Se encarga de recopilar los datos ingresados por el usuario, validar la información y mostrar un mensaje de confirmación de la transacción. Además, se actualiza el estado centralizado del controlador para reflejar que la compra ha sido procesada, se bloquea el asiento seleccionado en la base de datos local para que figure como ocupado, se inserta el ticket generado dentro del historial dinámico de la sesión y se navega automáticamente a la vista de inicio para que el usuario pueda realizar nuevas búsquedas o compras.
def procesar_pago(self):
    nombre = self.entry_nombre.get().strip()
    email = self.entry_email.get().strip()
    compra = self.controller.compra_pendiente
    # Validación de campos: Antes de procesar el pago, se verifica que los campos de nombre completo y correo electrónico estén completos. Si alguno de estos campos está vacío, se muestra una advertencia al usuario indicando que debe completar sus datos de contacto para emitir el boleto. Además, se verifica que haya un viaje seleccionado para procesar el pago; si no hay ningún viaje seleccionado, se muestra un mensaje de error indicando que no se ha seleccionado ningún viaje para procesar la compra. Esto garantiza que el proceso de pago solo se realice cuando se cuenta con la información necesaria y un viaje seleccionado, mejorando así la experiencia del usuario y evitando
    if not nombre or not email:
        messagebox.showwarning("Campos Requeridos", "Por favor, complete sus datos de contacto para emitir el boleto.")
        return
    if not compra or 'precio' not in compra:
        messagebox.showerror("Error de Compra", "No se ha seleccionado ningún viaje para procesar el pago.")
        return
            
    # --- PROCESAMIENTO INTERNO Y LÓGICA DE NEGOCIO REAL ---
    # Generación aleatoria del código alfanumérico único para el ticket
    codigo_ticket = f"PBB-{random.randint(1000, 9999)}{random.choice(['A','B','C','D','X'])}"
    compra["codigo_boleto"] = codigo_ticket
    compra["pasajero_nombre"] = nombre
    compra["pasajero_email"] = email
    
    # Bloqueo del asiento seleccionado en la base de datos local para que figure ocupado
    for viaje in self.controller.viajes_data:
        if viaje["id"] == compra["viaje_id"]:
            viaje["asientos_ocupados"].append(compra["asiento"])
            break
    
    # Inserción del ticket generado dentro del historial dinámico de la sesión
    self.controller.historial_compras.append(compra)
            
    msg = f"¡Pago Procesado Exitosamente!\n\nEstimado(a) {nombre}, el cobro de Bs {compra['precio']} se realizó correctamente a tu tarjeta.\n\nCódigo Único de Boleto: {codigo_ticket}\nAsiento Reservado: #{compra['asiento']}\n\nTu boleto digital con código QR de embarque fue enviado a: {email}"
            
    messagebox.showinfo("Transacción Exitosa", msg)
    # Limpieza de datos y navegación a inicio: Después de procesar el pago, se limpian los campos de entrada para el nombre completo y correo electrónico, se restablece el estado centralizado del controlador para reflejar que no hay ninguna compra pendiente ni búsqueda rápida activa, y se navega automáticamente a la vista de inicio para que el usuario pueda realizar nuevas búsquedas o compras. Esto garantiza un flujo de navegación fluido y una experiencia de usuario coherente después
    self.entry_nombre.delete(0, tk.END)
    self.entry_email.delete(0, tk.END)
    self.controller.compra_pendiente = {}
    self.controller.busqueda_rapida = {}
    self.controller.show_frame("InicioView")

#PÁGINA 4: GUÍA DE TURISMO DE BOLIVIA (CON CONTENEDORES IMÁGENES)
class TurismoView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller

        # Estructura de la vista de turismo: Se ha diseñado una estructura clara y visualmente atractiva para la vista de turismo, que incluye un encabezado con un título destacado y una descripción introductoria, seguido de un contenedor scrollable donde se muestran tarjetas visuales de destinos turísticos emblemáticos de Bolivia. Cada tarjeta incluye un marcador de posición para la imagen, un título, una descripción y una categoría, lo que enriquece la experiencia del usuario al proporcionar contenido adicional relacionado con los viajes que pueden realizar a través de PlusBus.
        ctk.CTkLabel(self, text="Descubre Bolivia con PlusBus", font=("Inter", 30, "bold"), text_color=COLOR_BLUE_DARK).pack(pady=(30, 5), padx=30, anchor="w")
        ctk.CTkLabel(self, text="Conoce los destinos emblemáticos a los que puedes viajar con nuestras flotas", font=("Inter", 18), text_color=COLOR_TEXT_MUTED).pack(pady=(0, 15), padx=30, anchor="w")
        
        # Contenedor scrollable para los destinos turísticos: Este contenedor permite mostrar una lista de destinos turísticos que puede ser más larga que el espacio visible en la pantalla. Al ser scrollable, los usuarios pueden desplazarse hacia abajo para explorar todas las opciones disponibles sin que la interfaz se sature, manteniendo una experiencia de usuario fluida y organizada.
        self.scroll_turismo = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_turismo.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Listado de destinos turísticos: Se ha creado un listado de destinos turísticos emblemáticos de Bolivia, cada uno con un título, descripción, categoría y un marcador de posición para la imagen. Estos destinos se muestran en tarjetas visuales dentro de un contenedor scrollable, lo que permite a los usuarios explorar fácilmente las opciones disponibles y obtener información relevante sobre cada destino. Esto enriquece la experiencia del usuario al proporcionar contenido adicional relacionado con los viajes que pueden realizar a través de PlusBus.
        destinos = [
    {"titulo": "Salar de Uyuni (Potosí)", "desc": "El desierto de sal continuo más grande y alto del mundo. Un espejo natural infinito durante la época de lluvias.", "cat": "Altiplano", "img_placeholder": "🖼️ [FOTOGRAFÍA: SALAR DE UYUNI INFINITO]"},
    
    {"titulo": "Cochabamba - Ciudad Jardín", "desc": "El corazón de Bolivia. Famosa por su gastronomía insuperable, clima templado y el imponente Cristo de la Concordia.", "cat": "Valles", "img_placeholder": "🖼️ [FOTOGRAFÍA: PAISAJE CRISTO DE LA CONCORDIA Y VALLES]"},
    {"titulo": "Tiahuanaco (La Paz)", "desc": "Cuna de una de las civilizaciones prehispánicas más longevas y avanzadas de América del Sur. Misterio arqueológico ancestral.", "cat": "Altiplano", "img_placeholder": "🖼️ [FOTOGRAFÍA: PUERTA DEL SOL - RUINAS TIAHUANACO]"},
    {"titulo": "Amazonía Indómita (Pando)", "desc": "El rincón salvaje y verde de Bolivia. Cubierto por densas selvas tropicales y ríos caudalosos ideales para la aventura.", "cat": "Llanos", "img_placeholder": "🖼️ [FOTOGRAFÍA: RESERVA NATURAL AMAZÓNICA - PANDO]"},
    {"titulo": "Misiones de Santa Cruz", "desc": "El motor económico de Bolivia. Tierra tropical vibrante, famosa por sus misiones jesuíticas y el Parque Nacional Amboró.", "cat": "Llanos", "img_placeholder": "🖼️ [FOTOGRAFÍA: CATEDRAL DE SANTA CRUZ O SELVA]"},
    {"titulo": "Ciudad Blanca (Chuquisaca)", "desc": "La capital constitucional de Bolivia. Destaca por su arquitectura colonial impecable y las impresionantes huellas de dinosaurio.", "cat": "Valles", "img_placeholder": "🖼️ [FOTOGRAFÍA: CALLES COLONIALES DE SUCRE]"},
    {"titulo": "Capital del Folklore (Oruro)", "desc": "Sede de uno de los carnavales más espectaculares del mundo, lleno de devoción, danzas tradicionales y cultura andina.", "cat": "Altiplano", "img_placeholder": "🖼️ [FOTOGRAFÍA: BAILARÍN DE DIABLADA EN ORURO]"},
    {"titulo": "Ruta del Vino (Tarija)", "desc": "El valle andaluz. Un destino de clima cálido, gente amable y los viñedos a mayor altitud del mundo.", "cat": "Valles", "img_placeholder": "🖼️ [FOTOGRAFÍA: VIÑEDOS DE TARIJA AL ATARDECER]"},
    {"titulo": "Sabana Amazónica (Beni)", "desc": "Un paraíso de biodiversidad y llanuras inundables. Ideal para navegar por ríos y observar fauna exótica en su hábitat natural.", "cat": "Llanos", "img_placeholder": "🖼️ [FOTOGRAFÍA: RÍO Y SELVA EN EL BENI]"}
]
        # Generación de tarjetas para cada destino turístico: Para cada destino en el listado, se crea una tarjeta visual que incluye un marcador de posición para la imagen, un título destacado, una descripción informativa y una categoría resaltada. Estas tarjetas se organizan dentro de un contenedor scrollable, lo que permite a los usuarios explorar fácilmente las opciones disponibles y obtener información relevante sobre cada destino. Esto enriquece la experiencia del usuario al proporcionar contenido adicional relacionado con los viajes que pueden realizar a través de PlusBus.
        for dest in destinos:
            card = ctk.CTkFrame(self.scroll_turismo, fg_color=COLOR_WHITE, corner_radius=25, border_width=1, border_color="#e2e8f0")
            card.pack(fill=tk.X, pady=12, padx=5)
            
            #COMPONENTE VISUAL: Marco contenedor de Imagen
            img_frame = ctk.CTkFrame(card, height=140, fg_color="#cbd5e1", corner_radius=18)
            img_frame.pack(fill=tk.X, padx=12, pady=(12, 4))
            img_frame.pack_propagate(False)
            
            #label con marcador de posición para la imagen del destino turístico, diseñado para ser visualmente atractivo y proporcionar una referencia clara de que se espera una imagen en ese espacio. Esto ayuda a mejorar la experiencia del usuario al indicar que se mostrará una fotografía representativa del destino turístico, lo que puede generar mayor interés y conexión emocional con el contenido presentado.
            lbl_img = ctk.CTkLabel(img_frame, text=dest["img_placeholder"], font=("Inter", 15, "bold"), text_color=COLOR_BLUE_DARK)
            lbl_img.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            #COMPONENTE TEXTUAL: Datos informativos
            card_inner = ctk.CTkFrame(card, fg_color="transparent")
            card_inner.pack(fill=tk.X, padx=15, pady=(4, 15))

            # Estructura de la información del destino turístico: Dentro de cada tarjeta, se organiza la información del destino turístico en un marco interno que incluye un encabezado con el título y la categoría, seguido de una descripción detallada. El título se destaca con un estilo de fuente más grande y negrita, mientras que la categoría se resalta con un fondo de color y un estilo de fuente más pequeño. La descripción se presenta con un diseño claro y legible para facilitar la lectura y comprensión por parte de los usuarios. Esto mejora la experiencia del usuario al proporcionar información relevante sobre cada destino turístico de manera organizada y visualmente atractiva.
            top_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
            top_frame.pack(fill=tk.X)
            
            # título del destino turístico, con un estilo destacado para resaltar la importancia de esta información y generar interés en los usuarios al explorar las opciones de destinos turísticos disponibles a través de PlusBus.
            ctk.CTkLabel(top_frame, text=dest["titulo"], font=("Inter", 22, "bold"), text_color=COLOR_BLUE_DARK).pack(side=tk.LEFT)
            ctk.CTkLabel(top_frame, text=dest["cat"], font=("Inter", 17, "bold"), fg_color=COLOR_BLUE_LIGHT, text_color=COLOR_BLUE_MEDIUM, corner_radius=4, height=20, padx=8).pack(side=tk.RIGHT)
            
            # descripción del destino turístico, con un diseño claro y legible para facilitar la lectura y comprensión por parte de los usuarios. Esta descripción proporciona información relevante sobre el destino, lo que puede ayudar a los usuarios a generar interés y conexión emocional con el contenido presentado, enriqueciendo así su experiencia al explorar las opciones de destinos turísticos disponibles a través de PlusBus.
            desc_label = ctk.CTkLabel(card_inner, text=dest["desc"], font=("Inter", 18), text_color=COLOR_TEXT_DARK, wraplength=680)
            desc_label.pack(anchor="w", pady=(10, 0), fill=tk.X)

#NUEVA PÁGINA: HISTORIAL DE COMPRAS 
class HistorialView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller
        
        ctk.CTkLabel(self, text="Historial de Boletos Emitidos", font=("Inter", 24, "bold"), text_color=COLOR_BLUE_DARK).pack(pady=(30, 5), padx=30, anchor="w")
        ctk.CTkLabel(self, text="Registro centralizado de pasajes adquiridos durante la sesión activa", font=("Inter", 13), text_color=COLOR_TEXT_MUTED).pack(pady=(0, 15), padx=30, anchor="w")
        
        self.scroll_historial = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_historial.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    def al_mostrar_vista(self):
        # Limpieza recursiva de elementos visuales previos para redibujar con datos nuevos
        for widget in self.scroll_historial.winfo_children():
            widget.destroy()
            
        compras = self.controller.historial_compras
        
        if not compras:
            no_tickets = ctk.CTkLabel(self.scroll_historial, text="📜 No se registran pasajes adquiridos en este momento.", font=("Inter", 14), text_color=COLOR_TEXT_MUTED)
            no_tickets.pack(pady=50)
            return
            
        # Despliegue visual ordenado (Muestra los boletos más recientes primero)
        for ticket in reversed(compras):
            card = ctk.CTkFrame(self.scroll_historial, fg_color=COLOR_WHITE, corner_radius=10, border_width=1, border_color="#e2e8f0")
            card.pack(fill=tk.X, pady=8, padx=5)

            # Componente de información del boleto: Este componente se encarga de mostrar los detalles relevantes de cada boleto adquirido durante la sesión activa, como la empresa, ruta, horario, precio y asiento seleccionado. Se organiza de manera clara y visualmente atractiva para facilitar la lectura y comprensión por parte de los usuarios, permitiéndoles revisar fácilmente su historial de compras.
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
            
            # Información principal del boleto: Se muestra la empresa de transporte y el código del boleto en un formato destacado para resaltar la información más relevante de cada compra. Esto permite a los usuarios identificar rápidamente cada boleto adquirido durante la sesión activa, facilitando la navegación y revisión de su historial de compras.
            ctk.CTkLabel(inner, text=ticket["empresa"], font=("Inter", 16, "bold"), text_color=COLOR_BLUE_DARK).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(inner, text=ticket["codigo_boleto"], font=("Inter", 13, "bold"), fg_color=COLOR_BLUE_LIGHT, text_color=COLOR_BLUE_MEDIUM, corner_radius=6, height=24, padx=10).grid(row=0, column=1, sticky="e")
            
            # Información detallada de la ruta: Se muestra información relevante sobre la ruta del viaje, incluyendo el origen, destino, fecha y hora. Esta información se presenta de manera clara y organizada para facilitar la lectura y comprensión por parte de los usuarios, proporcionando un resumen completo de cada compra realizada durante la sesión activa.
            detalles_ruta = f"📍 {ticket['origen']} ➔ {ticket['destino']}    |    📅 {ticket['fecha']} - 🕒 {ticket['hora']}"
            ctk.CTkLabel(inner, text=detalles_ruta, font=("Inter", 12), text_color=COLOR_TEXT_DARK).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 2))
            
            # Información detallada del boleto: Se muestra información relevante sobre el boleto adquirido, incluyendo el nombre del pasajero, el asiento seleccionado y el total pagado. Esta información se presenta de manera clara y organizada para facilitar la lectura y comprensión por parte de los usuarios, proporcionando un resumen completo de cada compra realizada durante la sesión activa.
            detalles_pasajero = f"👤 Pasajero: {ticket['pasajero_nombre']}    •    💺 Asiento Seleccionado: #{ticket['asiento']}    •    💵 Total Pagado: Bs {ticket['precio']}"
            ctk.CTkLabel(inner, text=detalles_pasajero, font=("Inter", 11), text_color=COLOR_TEXT_MUTED).grid(row=2, column=0, columnspan=2, sticky="w")
            
            # Configuración de pesos para que el contenido se distribuya adecuadamente dentro de la tarjeta, permitiendo que el título y el código del boleto se alineen a los extremos opuestos, mientras que los detalles de la ruta y del pasajero se muestren de manera clara y organizada debajo.
            inner.grid_columnconfigure(0, weight=1)
            inner.grid_columnconfigure(1, weight=1)

# CONTROLADOR PRINCIPAL DE LA APLICACIÓN
if __name__ == "__main__":
    app = PlusBusApp()
    app.mainloop()

