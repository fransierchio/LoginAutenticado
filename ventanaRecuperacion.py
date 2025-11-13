import customtkinter as ctk
from tkinter import messagebox

class VentanaRecuperacion(ctk.CTkToplevel):
    PREGUNTAS = [
        "¿Cuál es tu fecha de nacimiento?",
        "¿Cuál es el nombre de tu primera mascota?",
        "¿Cuál es tu comida favorita?",
        "¿Cuál es tu ciudad natal?"
    ]
    
    def __init__(self, parent, bd, servicioCorreo, onSuccess):
        super().__init__(parent)
        
        self.bd = bd
        self.servicioCorreo = servicioCorreo
        self.onSuccess = onSuccess
        
        self.title("Recuperar acceso")
        
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()
        w = min(540, ancho - 100)
        h = min(570, alto - 100)
        
        x = (ancho // 2) - (w // 2)
        y = (alto // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.configure(fg_color="#1e1e1e")
        self.resizable(False, False)
        
        self.crearInterfaz()
        self.transient(parent)
        self.grab_set()
    
    def crearInterfaz(self):
        frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12)
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(frame, text="🔑 Recuperar acceso", font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#d9534f").pack(pady=(20, 8))
        
        ctk.CTkLabel(frame, text="Verifica tu identidad con tu pregunta de seguridad",
                    font=ctk.CTkFont(size=12), text_color="#9b9b9b").pack(pady=(0, 30))
        
        ctk.CTkLabel(frame, text="Correo electrónico", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.emailEntry = ctk.CTkEntry(frame, width=420, height=45,
                                       placeholder_text="Tu correo registrado",
                                       fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                       corner_radius=6, text_color="#ffffff", placeholder_text_color="#6b6b6b")
        self.emailEntry.pack(pady=(0, 20), padx=40)
        
        ctk.CTkLabel(frame, text="Pregunta de seguridad", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.preguntaCombo = ctk.CTkComboBox(frame, width=420, height=45,
                                            values=self.PREGUNTAS, state="readonly",
                                            fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                            button_color="#d9534f", corner_radius=6,
                                            text_color="#ffffff", dropdown_fg_color="#262626",
                                            dropdown_text_color="#ffffff", dropdown_hover_color="#3a3a3a")
        self.preguntaCombo.set(self.PREGUNTAS[0])
        self.preguntaCombo.pack(pady=(0, 20), padx=40)
        
        ctk.CTkLabel(frame, text="Respuesta de seguridad", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.respuestaEntry = ctk.CTkEntry(frame, width=420, height=45,
                                           placeholder_text="Escribe tu respuesta",
                                           fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                           corner_radius=6, text_color="#ffffff", placeholder_text_color="#6b6b6b")
        self.respuestaEntry.pack(pady=(0, 30), padx=40)
        
        btnFrame = ctk.CTkFrame(frame, fg_color="transparent")
        btnFrame.pack(pady=(0, 20))
        
        ctk.CTkButton(btnFrame, text="🔓 Recuperar contraseña", command=self.recuperar,
                     width=200, height=45, fg_color="#d9534f", hover_color="#c9302c",
                     corner_radius=6, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(btnFrame, text="✕ Cancelar", command=self.destroy,
                     width=200, height=45, fg_color="#505050", hover_color="#404040",
                     corner_radius=6, font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
    
    def recuperar(self):
        email = self.emailEntry.get().strip()
        pregunta = self.preguntaCombo.get()
        respuesta = self.respuestaEntry.get().strip()
        
        if not email or not respuesta:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        
        userId = self.bd.validarRespuestaSeguridad(email, pregunta, respuesta)
        
        if userId:
            nuevaPassword = self.bd.generarPasswordTemporal(userId)
            enviado = self.servicioCorreo.enviarPasswordTemporal(email, nuevaPassword)
            self.mostrarPasswordVentana(nuevaPassword, enviado=enviado, email=email)
        else:
            messagebox.showerror("Error", "Los datos ingresados no coinciden con ninguna cuenta.")
    
    def mostrarPasswordVentana(self, password, enviado=False, email=""):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Contraseña Temporal")
        ventana.geometry("550x400")
        x = (ventana.winfo_screenwidth() // 2) - 275
        y = (ventana.winfo_screenheight() // 2) - 200
        ventana.geometry(f"550x400+{x}+{y}")
        ventana.configure(fg_color="#1e1e1e")
    
        frame = ctk.CTkFrame(ventana, fg_color="#1e1e1e", corner_radius=12)
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        if enviado:
            ctk.CTkLabel(frame, text="✅ Contraseña enviada", 
                        font=ctk.CTkFont(size=24, weight="bold"),
                        text_color="#2d7a3e").pack(pady=(20, 10))
            ctk.CTkLabel(frame, text=f"Se ha enviado a: {email}",
                        font=ctk.CTkFont(size=12), text_color="#9b9b9b").pack(pady=(0, 20))
            passwordFrame = ctk.CTkFrame(frame, fg_color="#262626", corner_radius=10, border_width=2,
                                         border_color="#2d7a3e")
        else:
            ctk.CTkLabel(frame, text="⚠️ No se pudo enviar el correo", 
                        font=ctk.CTkFont(size=22, weight="bold"),
                        text_color="#d9534f").pack(pady=(20, 10))
            ctk.CTkLabel(frame, text="Copia manualmente tu contraseña temporal",
                        font=ctk.CTkFont(size=12), text_color="#9b9b9b").pack(pady=(0, 20))
            passwordFrame = ctk.CTkFrame(frame, fg_color="#262626", corner_radius=10, border_width=2,
                                         border_color="#d9534f")
        
        passwordFrame.pack(pady=20, padx=30)
        
        ctk.CTkLabel(passwordFrame, text="CONTRASEÑA TEMPORAL:",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#8a8a8a").pack(padx=40, pady=(15, 5))
        
        color_password = "#2d7a3e" if enviado else "#d9534f"
        passwordLabel = ctk.CTkLabel(passwordFrame, text=password,
                                     font=ctk.CTkFont(size=28, weight="bold", family="Courier New"),
                                     text_color=color_password)
        passwordLabel.pack(padx=40, pady=(0, 15))
        
        ctk.CTkButton(frame, text="📋 Copiar al portapapeles", 
                     command=lambda: self.copiarPortapapeles(password, ventana),
                     width=300, height=45, fg_color="#4a90e2", hover_color="#357abd",
                     corner_radius=6, font=ctk.CTkFont(size=13, weight="bold")).pack(pady=10)
        
        ctk.CTkButton(frame, text="Cerrar", command=lambda: self.cerrarVentanas(ventana),
                     width=300, height=40, fg_color="#505050", hover_color="#404040",
                     corner_radius=6).pack(pady=5)
        
        ventana.transient(self)
        ventana.grab_set()
    
    def cerrarVentanas(self, ventanaModal):
        self.onSuccess()
        self.destroy()
        ventanaModal.destroy()
    
    def copiarPortapapeles(self, texto, ventana):
        ventana.clipboard_clear()
        ventana.clipboard_append(texto)
        messagebox.showinfo("✓ Copiado", "Contraseña copiada al portapapeles")
