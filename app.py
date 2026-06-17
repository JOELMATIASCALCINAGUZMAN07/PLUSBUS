import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# --- CONFIGURACIÓN GLOBAL DE ESTILOS ---
COLOR_BLUE_DARK = "#0f2d59"     # Azul oscuro institucional (Sidebar / Login)
COLOR_BLUE_MEDIUM = "#1d4ed8"   # Azul medio para énfasis y botones secundarios
COLOR_BLUE_LIGHT = "#dbeafe"    # Azul claro para badges/etiquetas
COLOR_ORANGE = "#f97316"        # Naranja primario para botones de acción y precios
COLOR_BG_LIGHT = "#f8fafc"      # Fondo gris claro limpio para las vistas
COLOR_WHITE = "#ffffff"         # Blanco para tarjetas y contenedores de datos
COLOR_TEXT_DARK = "#1e293b"     # Gris oscuro para legibilidad de textos
COLOR_TEXT_MUTED = "#64748b"    # Gris apagado para etiquetas secundarias

# Configuración inicial del tema base de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PlusBusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Parámetros de la ventana principal
        self.title("PlusBus Bolivia - Sistema de Gestión Autónoma")
        self.geometry("1100x650")
        self.configure(fg_color=COLOR_BG_LIGHT)
        
        # --- ESTADO CENTRALIZADO ---
        self.viajes_data = [
            {"id": 1, "empresa": "Flota El Dorado", "origen": "La Paz", "destino": "Cochabamba", "precio": 90, "hora": "08:30", "fecha": "2026-06-20"},
            {"id": 2, "empresa": "Trans Copacabana", "origen": "Cochabamba", "destino": "Santa Cruz", "precio": 130, "hora": "22:00", "fecha": "2026-06-21"},
            {"id": 3, "empresa": "Bolívar", "origen": "La Paz", "destino": "Oruro", "precio": 35, "hora": "14:15", "fecha": "2026-06-20"},
            {"id": 4, "empresa": "Flota Cosmos", "origen": "Sucre", "destino": "Potosí", "precio": 25, "hora": "10:00", "fecha": "2026-06-22"}
        ]
        self.busqueda_rapida = {}
        self.compra_pendiente = {}
        self.usuario_autenticado = False

        # --- ARQUITECTURA DE CONTENEDORES ---
        # Menú Lateral (Inicialmente oculto por Login)
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=COLOR_BLUE_DARK)
        
        # Contenedor derecho para las páginas dinámicas
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.inicializar_vistas()

    def inicializar_vistas(self):
        self.frames = {}
        
        # Incluye LoginView dentro del diccionario de control de navegación
        for PageClass in (LoginView, InicioView, PasajesView, PagoView, TurismoView):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Fuerza la carga obligatoria de la pantalla de inicio de sesión
        self.show_frame("LoginView")

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

        logo_label = ctk.CTkLabel(self.sidebar, text="🚌 PlusBus", font=("Inter", 24, "bold"), text_color=COLOR_WHITE)
        logo_label.pack(pady=35, padx=20, anchor="w")
        
        self.btn_inicio = ctk.CTkButton(self.sidebar, text="🏠   Inicio", font=("Inter", 14, "bold"), fg_color="transparent", text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, height=45, anchor="w", command=lambda: self.show_frame("InicioView"))
        self.btn_inicio.pack(fill=tk.X, padx=15, pady=5)
        
        self.btn_pasajes = ctk.CTkButton(self.sidebar, text="🎫   Pasajes", font=("Inter", 14, "bold"), fg_color="transparent", text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, height=45, anchor="w", command=lambda: self.show_frame("PasajesView"))
        self.btn_pasajes.pack(fill=tk.X, padx=15, pady=5)

        self.btn_pago = ctk.CTkButton(self.sidebar, text="💳   Pagar Ticket", font=("Inter", 14, "bold"), fg_color="transparent", text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, height=45, anchor="w", command=lambda: self.show_frame("PagoView"))
        self.btn_pago.pack(fill=tk.X, padx=15, pady=5)
        
        self.btn_turismo = ctk.CTkButton(self.sidebar, text="🗺️   Guía Turismo", font=("Inter", 14, "bold"), fg_color="transparent", text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, height=45, anchor="w", command=lambda: self.show_frame("TurismoView"))
        self.btn_turismo.pack(fill=tk.X, padx=15, pady=5)

    def show_frame(self, page_name):
        # Bloqueo de seguridad: Si no está autenticado, no permite cambiar de vista
        if not self.usuario_autenticado and page_name != "LoginView":
            print("Acceso denegado: Autenticación requerida.")
            return

        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
            if hasattr(frame, "al_mostrar_vista"):
                frame.al_mostrar_vista()

                # --- VISTA CENTRAL DE AUTENTICACIÓN (LOGIN obligatorio) ---
class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller

        login_card = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=16,
            border_width=1,
            border_color="#e2e8f0",
            width=420,
            height=460
        )
        login_card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        login_card.pack_propagate(False)

        ctk.CTkLabel(
            login_card,
            text="🚌 PlusBus Bolivia",
            font=("Inter", 24, "bold"),
            text_color=COLOR_BLUE_DARK
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            login_card,
            text="Gestión de Pasajes y Turismo Autónomo",
            font=("Inter", 12),
            text_color=COLOR_TEXT_MUTED
        ).pack(pady=(0, 25))

        ctk.CTkLabel(
            login_card,
            text="Nombre de Usuario / Correo",
            font=("Inter", 12, "bold"),
            text_color=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=40, pady=(10, 2))

        self.entry_user = ctk.CTkEntry(
            login_card,
            height=38,
            fg_color=COLOR_BG_LIGHT,
            border_color="#cbd5e1",
            placeholder_text="ejemplo@sistema.com"
        )
        self.entry_user.pack(fill=tk.X, padx=40, pady=5)

        ctk.CTkLabel(
            login_card,
            text="Contraseña de Acceso",
            font=("Inter", 12, "bold"),
            text_color=COLOR_TEXT_DARK
        ).pack(anchor="w", padx=40, pady=(10, 2))

        self.entry_pass = ctk.CTkEntry(
            login_card,
            height=38,
            fg_color=COLOR_BG_LIGHT,
            border_color="#cbd5e1",
            show="*",
            placeholder_text="••••••••"
        )
        self.entry_pass.pack(fill=tk.X, padx=40, pady=5)

        ctk.CTkButton(
            login_card,
            text="Iniciar Sesión",
            font=("Inter", 14, "bold"),
            fg_color=COLOR_BLUE_DARK,
            text_color=COLOR_WHITE,
            hover_color=COLOR_BLUE_MEDIUM,
            height=42,
            command=self.validar_credenciales
        ).pack(fill=tk.X, padx=40, pady=(30, 5))

        ctk.CTkButton(
            login_card,
            text="Registrar Nueva Cuenta",
            font=("Inter", 12),
            fg_color="transparent",
            text_color=COLOR_BLUE_MEDIUM,
            hover_color="#eff6ff",
            command=self.registrar_usuario
        ).pack(pady=5)

    def validar_credenciales(self):
        usuario = self.entry_user.get().strip()
        contra = self.entry_pass.get().strip()

        if not usuario or not contra:
            messagebox.showwarning(
                "Campos Vacíos",
                "Por favor, introduzca sus datos para autenticarse en el sistema."
            )
            return

        messagebox.showinfo(
            "Acceso Concedido",
            "Bienvenido al sistema autónomo PlusBus."
        )
        self.controller.activar_interfaz_principal()

    def registrar_usuario(self):
        messagebox.showinfo(
            "Registro de Cuentas",
            "Módulo de creación de cuentas sincronizado con éxito."
        )