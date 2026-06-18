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

# --- PÁGINA 1: INICIO (BÚSQUEDA RÁPIDA) ---
class InicioView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller
        
        ctk.CTkLabel(self, text="Busca tus pasajes en Bolivia", font=("Inter", 26, "bold"), text_color=COLOR_BLUE_DARK).pack(pady=(40, 5))
        ctk.CTkLabel(self, text="Viaja de forma rápida, segura y completamente autónoma", font=("Inter", 14), text_color=COLOR_TEXT_MUTED).pack(pady=(0, 30))
        
        form_card = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=12, border_width=1, border_color="#e2e8f0", width=600, height=420)
        form_card.pack(pady=20, padx=40)
        form_card.pack_propagate(False)
        
        self.origen_var = tk.StringVar(value="La Paz")
        self.destino_var = tk.StringVar(value="Cochabamba")
        
        ctk.CTkLabel(form_card, text="Ciudad de Origen", font=("Inter", 12, "bold"), text_color=COLOR_TEXT_DARK).pack(pady=(25, 2), padx=30, anchor="w")
        self.entry_origen = ctk.CTkEntry(form_card, textvariable=self.origen_var, height=40, fg_color=COLOR_BG_LIGHT, text_color=COLOR_TEXT_DARK, border_color="#cbd5e1")
        self.entry_origen.pack(fill=tk.X, padx=30, pady=5)
        
        self.btn_swap = ctk.CTkButton(form_card, text="🔄 Intercambiar Ciudades", font=("Inter", 11), fg_color="transparent", text_color=COLOR_BLUE_MEDIUM, hover_color="#eff6ff", width=150, command=self.swap_locations)
        self.btn_swap.pack(pady=5)
        
        ctk.CTkLabel(form_card, text="Ciudad de Destino", font=("Inter", 12, "bold"), text_color=COLOR_TEXT_DARK).pack(pady=(5, 2), padx=30, anchor="w")
        self.entry_destino = ctk.CTkEntry(form_card, textvariable=self.destino_var, height=40, fg_color=COLOR_BG_LIGHT, text_color=COLOR_TEXT_DARK, border_color="#cbd5e1")
        self.entry_destino.pack(fill=tk.X, padx=30, pady=5)
        
        btn_buscar = ctk.CTkButton(form_card, text="Buscar Flotas Disponibles", font=("Inter", 14, "bold"), fg_color=COLOR_ORANGE, text_color=COLOR_WHITE, hover_color="#ea580c", height=45, command=self.buscar_viaje)
        btn_buscar.pack(fill=tk.X, padx=30, pady=25)

    def swap_locations(self):
        ori = self.origen_var.get()
        des = self.destino_var.get()
        self.origen_var.set(des)
        self.destino_var.set(ori)

    def buscar_viaje(self):
        self.controller.busqueda_rapida = {
            "origen": self.origen_var.get().strip(),
            "destino": self.destino_var.get().strip()
        }
        self.controller.show_frame("PasajesView")

        # --- PÁGINA 2: LISTADO DE SALIDAS ---
class PasajesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=COLOR_BG_LIGHT)
        self.controller = controller
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill=tk.X, padx=30, pady=(30, 10))
        
        self.titulo_label = ctk.CTkLabel(self.header_frame, text="Resultados de Salidas Disponibles", font=("Inter", 22, "bold"), text_color=COLOR_BLUE_DARK)
        self.titulo_label.pack(side=tk.LEFT)
        
        self.contador_label = ctk.CTkLabel(self.header_frame, text="0 flotas encontradas", font=("Inter", 12, "bold"), fg_color=COLOR_BLUE_LIGHT, text_color=COLOR_BLUE_MEDIUM, corner_radius=6, height=26, padx=10)
        self.contador_label.pack(side=tk.RIGHT)
        
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

    def al_mostrar_vista(self):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()
            
        filtro = self.controller.busqueda_rapida
        
        if filtro:
            viajes_filtrados = [
                v for v in self.controller.viajes_data 
                if filtro["origen"].lower() in v["origen"].lower() and 
                   filtro["destino"].lower() in v["destino"].lower()
            ]
        else:
            viajes_filtrados = self.controller.viajes_data

        self.contador_label.configure(text=f"{len(viajes_filtrados)} flotas encontradas")

        if not viajes_filtrados:
            no_results = ctk.CTkLabel(self.scroll_container, text="❌ No se encontraron flotas para la ruta seleccionada.", font=("Inter", 14), text_color=COLOR_TEXT_MUTED)
            no_results.pack(pady=40)
            return

        for viaje in viajes_filtrados:
            card = ctk.CTkFrame(self.scroll_container, fg_color=COLOR_WHITE, corner_radius=10, border_width=1, border_color="#e2e8f0", height=100)
            card.pack(fill=tk.X, pady=8, padx=5)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side=tk.LEFT, padx=20, pady=15, fill=tk.BOTH, expand=True)
            
            ctk.CTkLabel(info_frame, text=viaje["empresa"], font=("Inter", 16, "bold"), text_color=COLOR_BLUE_DARK).grid(row=0, column=0, sticky="w")
            
            ruta_texto = f"📍 Ruta: {viaje['origen']} ➔ {viaje['destino']}"
            ctk.CTkLabel(info_frame, text=ruta_texto, font=("Inter", 12), text_color=COLOR_TEXT_DARK).grid(row=1, column=0, sticky="w", pady=(2, 0))
            
            horario_texto = f"📅 {viaje['fecha']}  |  🕒 Salida: {viaje['hora']}"
            ctk.CTkLabel(info_frame, text=horario_texto, font=("Inter", 11), text_color=COLOR_TEXT_MUTED).grid(row=2, column=0, sticky="w")
            
            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side=tk.RIGHT, padx=20, pady=15, fill=tk.Y)
            
            ctk.CTkLabel(action_frame, text=f"Bs {viaje['precio']}", font=("Inter", 20, "bold"), text_color=COLOR_ORANGE).pack(anchor="e")
            
            btn_comprar = ctk.CTkButton(action_frame, text="Seleccionar", font=("Inter", 12, "bold"), fg_color=COLOR_BLUE_DARK, text_color=COLOR_WHITE, hover_color=COLOR_BLUE_MEDIUM, width=100, height=32, command=lambda v=viaje: self.ir_a_pagar(v))
            btn_comprar.pack(pady=(5, 0))

    def ir_a_pagar(self, viaje):
        self.controller.compra_pendiente = viaje
        self.controller.show_frame("PagoView")