import customtkinter as ctk
import re
from tkinter import messagebox

class VentanaRegistro(ctk.CTkToplevel):
    PREGUNTAS = [
        "¿Cuál es tu fecha de nacimiento?",
        "¿Cuál es el nombre de tu primera mascota?",
        "¿Cuál es tu comida favorita?",
        "¿Cuál es tu ciudad natal?"
    ]
    
    def __init__(self, parent, bd, onSuccess):
        super().__init__(parent)
        
        self.bd = bd
        self.onSuccess = onSuccess
        
        self.title("Crear cuenta nueva")
        self.geometry("520x680")
        x = (self.winfo_screenwidth() // 2) - 260
        y = (self.winfo_screenheight() // 2) - 340
        self.geometry(f"520x680+{x}+{y}")
        self.configure(fg_color="#1e1e1e")
        
        self.crearInterfaz()
        self.transient(parent)
        self.grab_set()
    
    def crearInterfaz(self):
        frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12)
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(frame, text="📝 Crear cuenta nueva", font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#2d7a3e").pack(pady=(20, 8))
        
        ctk.CTkLabel(frame, text="Completa todos los campos para registrarte",
                    font=ctk.CTkFont(size=12), text_color="#9b9b9b").pack(pady=(0, 25))
        
        ctk.CTkLabel(frame, text="Correo electrónico", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.emailEntry = ctk.CTkEntry(frame, width=430, height=42, placeholder_text="ejemplo@correo.com",
                                       fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                       corner_radius=6, text_color="#ffffff", placeholder_text_color="#6b6b6b")
        self.emailEntry.pack(pady=(0, 15), padx=40)
        
        ctk.CTkLabel(frame, text="Contraseña", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.passwordEntry = ctk.CTkEntry(frame, width=430, height=42, show="●",
                                          placeholder_text="Mínimo 7 caracteres (Mayús, minus, símbolo)",
                                          fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                          corner_radius=6, text_color="#ffffff", placeholder_text_color="#6b6b6b")
        self.passwordEntry.pack(pady=(0, 15), padx=40)
        
        ctk.CTkLabel(frame, text="Confirmar contraseña", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.confirmEntry = ctk.CTkEntry(frame, width=430, height=42, show="●",
                                        placeholder_text="Repite tu contraseña",
                                        fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                        corner_radius=6, text_color="#ffffff", placeholder_text_color="#6b6b6b")
        self.confirmEntry.pack(pady=(0, 15), padx=40)
        
        ctk.CTkLabel(frame, text="Pregunta de seguridad", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.preguntaCombo = ctk.CTkComboBox(frame, width=430, height=42,
                                            values=self.PREGUNTAS, state="readonly",
                                            fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                            button_color="#2d7a3e", corner_radius=6,
                                            text_color="#ffffff", dropdown_fg_color="#262626",
                                            dropdown_text_color="#ffffff", dropdown_hover_color="#3a3a3a")
        self.preguntaCombo.set(self.PREGUNTAS[0])
        self.preguntaCombo.pack(pady=(0, 15), padx=40)
        
        ctk.CTkLabel(frame, text="Respuesta de seguridad", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.respuestaEntry = ctk.CTkEntry(frame, width=430, height=42,
                                           placeholder_text="Tu respuesta secreta",
                                           fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                           corner_radius=6, text_color="#ffffff", placeholder_text_color="#6b6b6b")
        self.respuestaEntry.pack(pady=(0, 25), padx=40)
        
        btnFrame = ctk.CTkFrame(frame, fg_color="transparent")
        btnFrame.pack(pady=(0, 20))
        
        ctk.CTkButton(btnFrame, text="✓ Crear cuenta", command=self.registrar,
                     width=205, height=45, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(btnFrame, text="✕ Cancelar", command=self.destroy,
                     width=205, height=45, fg_color="#505050", hover_color="#404040",
                     corner_radius=6, font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
    
    def validarPassword(self, password):
        if len(password) < 7:
            return False, "La contraseña debe tener al menos 7 caracteres"
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe tener al menos una mayúscula"
        if not re.search(r"[a-z]", password):
            return False, "La contraseña debe tener al menos una minúscula"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "La contraseña debe tener al menos un carácter especial"
        return True, "OK"
    
    def registrar(self):
        try:
            email = self.emailEntry.get().strip()
            password = self.passwordEntry.get()
            confirm = self.confirmEntry.get()
            pregunta = self.preguntaCombo.get()
            respuesta = self.respuestaEntry.get().strip()
            
            if not email or not password or not confirm or not respuesta:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
        
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Correo electrónico inválido")
                return
            
            valido, mensaje = self.validarPassword(password)
            if not valido:
                messagebox.showerror("Error", mensaje)
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            
            if self.bd.registrar(email, password, pregunta, respuesta):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.onSuccess()
                self.destroy()
            else:
                messagebox.showerror("Error", "El correo electrónico ya está registrado")
        except Exception as e:
            print(f"Error en registro: {e}")
            messagebox.showerror("Error", "Ocurrió un error al registrar. Intenta de nuevo.")
