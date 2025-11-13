import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import re

class VentanaDashboard(ctk.CTkToplevel):
    def __init__(self, parent, bd, userEmail, onLogout):
        super().__init__(parent)
        
        self.bd = bd
        self.userEmail = userEmail
        self.onLogout = onLogout
        self.datosUsuario = self.bd.obtenerDatosUsuario(userEmail)
        
        self.title("Panel Principal")
        
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()
        w = min(900, int(ancho * 0.8))
        h = min(650, int(alto * 0.8))
        
        x = (ancho // 2) - (w // 2)
        y = (alto // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.configure(fg_color="#1e1e1e")
        self.resizable(True, True)
        self.minsize(750, 550)
        
        self.crearInterfaz()
        self.transient(parent)
        self.grab_set()
        self.mostrarPerfil()
    
    def crearInterfaz(self):
        headerFrame = ctk.CTkFrame(self, fg_color="#262626", corner_radius=0, height=80)
        headerFrame.pack(fill="x", padx=0, pady=0)
        headerFrame.pack_propagate(False)
        
        ctk.CTkLabel(headerFrame, text="🏠 Panel Principal", 
                    font=ctk.CTkFont(size=28, weight="bold"),
                    text_color="#4a90e2").pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(headerFrame, text="🚪 Cerrar Sesión", command=self.cerrarSesion,
                     width=140, height=35, fg_color="#d9534f", hover_color="#c9302c",
                     corner_radius=6, font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", padx=30)
        
        containerFrame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        containerFrame.pack(fill="both", expand=True, padx=20, pady=20)
        
        menuFrame = ctk.CTkFrame(containerFrame, fg_color="#262626", width=200, corner_radius=12)
        menuFrame.pack(side="left", fill="y", padx=(0, 15))
        menuFrame.pack_propagate(False)
        
        ctk.CTkLabel(menuFrame, text="📋 Menú", font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#e0e0e0").pack(pady=(20, 15), padx=15)
        
        self.btnPerfil = ctk.CTkButton(menuFrame, text="👤 Mi Perfil", command=self.mostrarPerfil,
                                       width=170, height=45, fg_color="#4a90e2", hover_color="#357abd",
                                       corner_radius=6, font=ctk.CTkFont(size=13), anchor="w")
        self.btnPerfil.pack(pady=5, padx=15)
        
        self.btnSeguridad = ctk.CTkButton(menuFrame, text="🔐 Seguridad", command=self.mostrarSeguridad,
                                          width=170, height=45, fg_color="#3a3a3a", hover_color="#4a4a4a",
                                          corner_radius=6, font=ctk.CTkFont(size=13), anchor="w")
        self.btnSeguridad.pack(pady=5, padx=15)
        
        self.contentFrame = ctk.CTkFrame(containerFrame, fg_color="#1e1e1e")
        self.contentFrame.pack(side="right", fill="both", expand=True)
    
    def limpiarContenido(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
    
    def mostrarPerfil(self):
        self.limpiarContenido()
        
        self.btnPerfil.configure(fg_color="#4a90e2")
        self.btnSeguridad.configure(fg_color="#3a3a3a")
        
        scrollFrame = ctk.CTkScrollableFrame(self.contentFrame, fg_color="#1e1e1e")
        scrollFrame.pack(fill="both", expand=True)
        
        card = ctk.CTkFrame(scrollFrame, fg_color="#262626", corner_radius=12)
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(card, text="👤 Mi Perfil", font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#4a90e2").pack(pady=(25, 10), padx=30, anchor="w")
        
        ctk.CTkLabel(card, text="Información personal de tu cuenta",
                    font=ctk.CTkFont(size=12), text_color="#8a8a8a").pack(pady=(0, 25), padx=30, anchor="w")
        
        # formulario
        formFrame = ctk.CTkFrame(card, fg_color="transparent")
        formFrame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # email
        ctk.CTkLabel(formFrame, text="📧 Email", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        self.emailEntry = ctk.CTkEntry(formFrame, height=42, fg_color="#1e1e1e", 
                                  border_color="#3a3a3a", placeholder_text="tu@email.com")
        self.emailEntry.pack(pady=(0, 15), fill="x")
        self.emailEntry.insert(0, self.datosUsuario['email'])
        
        # nombre
        ctk.CTkLabel(formFrame, text="👤 Nombre completo", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        self.nombreEntry = ctk.CTkEntry(formFrame, height=42, fg_color="#1e1e1e",
                                        border_color="#3a3a3a", placeholder_text="Ej: Juan Pérez")
        self.nombreEntry.pack(pady=(0, 25), fill="x")
        self.nombreEntry.insert(0, self.datosUsuario['nombre'])
        
        # boton guardar
        ctk.CTkButton(formFrame, text="💾 Guardar Cambios", command=self.guardarPerfil,
                     height=45, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=14, weight="bold")).pack(fill="x")
    
    def mostrarSeguridad(self):
        self.limpiarContenido()
        
        self.btnPerfil.configure(fg_color="#3a3a3a")
        self.btnSeguridad.configure(fg_color="#4a90e2")
        
        scrollFrame = ctk.CTkScrollableFrame(self.contentFrame, fg_color="#1e1e1e")
        scrollFrame.pack(fill="both", expand=True)
        
        card = ctk.CTkFrame(scrollFrame, fg_color="#262626", corner_radius=12)
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(card, text="🔐 Seguridad", font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#4a90e2").pack(pady=(25, 10), padx=30, anchor="w")
        
        ctk.CTkLabel(card, text="Actualiza tu contraseña y pregunta de seguridad",
                    font=ctk.CTkFont(size=12), text_color="#8a8a8a").pack(pady=(0, 25), padx=30, anchor="w")
        
        # formulario
        formFrame = ctk.CTkFrame(card, fg_color="transparent")
        formFrame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        ctk.CTkLabel(formFrame, text="🔑 Cambiar Contraseña", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#e0e0e0").pack(pady=(0, 15), anchor="w")
        
        ctk.CTkLabel(formFrame, text="🔒 Contraseña actual", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        
        passActualFrame = ctk.CTkFrame(formFrame, fg_color="transparent")
        passActualFrame.pack(pady=(0, 15), fill="x")
        
        self.passActualEntry = ctk.CTkEntry(passActualFrame, height=42, show="●", fg_color="#1e1e1e",
                                            border_color="#3a3a3a", placeholder_text="Tu contraseña actual")
        self.passActualEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btnMostrarActual = ctk.CTkButton(passActualFrame, text="👁", width=42, height=42,
                                              fg_color="#3a3a3a", hover_color="#4a4a4a",
                                              font=ctk.CTkFont(size=16),
                                              command=lambda: self.togglePassDash(1))
        self.btnMostrarActual.pack(side="right")
        self.mostrarActual = False
        
        ctk.CTkLabel(formFrame, text="🔑 Nueva contraseña", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        
        passNuevaFrame = ctk.CTkFrame(formFrame, fg_color="transparent")
        passNuevaFrame.pack(pady=(0, 10), fill="x")
        
        self.passNuevaEntry = ctk.CTkEntry(passNuevaFrame, height=42, show="●", fg_color="#1e1e1e",
                                           border_color="#3a3a3a", placeholder_text="Nueva contraseña segura")
        self.passNuevaEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.passNuevaEntry.bind("<KeyRelease>", self.validarPasswordNueva)
        
        self.btnMostrarNueva = ctk.CTkButton(passNuevaFrame, text="👁", width=42, height=42,
                                             fg_color="#3a3a3a", hover_color="#4a4a4a",
                                             font=ctk.CTkFont(size=16),
                                             command=lambda: self.togglePassDash(2))
        self.btnMostrarNueva.pack(side="right")
        self.mostrarNueva = False
        
        self.reqFrame = ctk.CTkFrame(formFrame, fg_color="#1e1e1e", corner_radius=6)
        self.reqFrame.pack(pady=(0, 15), fill="x")
        
        self.req1 = ctk.CTkLabel(self.reqFrame, text="✗ Mínimo 7 caracteres",
                                 font=ctk.CTkFont(size=10), text_color="#d9534f", anchor="w")
        self.req1.pack(pady=3, padx=15, fill="x")
        
        self.req2 = ctk.CTkLabel(self.reqFrame, text="✗ Una mayúscula (A-Z)",
                                 font=ctk.CTkFont(size=10), text_color="#d9534f", anchor="w")
        self.req2.pack(pady=3, padx=15, fill="x")
        
        self.req3 = ctk.CTkLabel(self.reqFrame, text="✗ Una minúscula (a-z)",
                                 font=ctk.CTkFont(size=10), text_color="#d9534f", anchor="w")
        self.req3.pack(pady=3, padx=15, fill="x")
        
        self.req4 = ctk.CTkLabel(self.reqFrame, text="✗ Un símbolo (!@#$...)",
                                 font=ctk.CTkFont(size=10), text_color="#d9534f", anchor="w")
        self.req4.pack(pady=3, padx=15, fill="x")
        
        ctk.CTkLabel(formFrame, text="🔑 Confirmar contraseña", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        
        passConfirmFrame = ctk.CTkFrame(formFrame, fg_color="transparent")
        passConfirmFrame.pack(pady=(0, 20), fill="x")
        
        self.passConfirmEntry = ctk.CTkEntry(passConfirmFrame, height=42, show="●", fg_color="#1e1e1e",
                                             border_color="#3a3a3a", placeholder_text="Repite la nueva contraseña")
        self.passConfirmEntry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btnMostrarConfirm = ctk.CTkButton(passConfirmFrame, text="👁", width=42, height=42,
                                               fg_color="#3a3a3a", hover_color="#4a4a4a",
                                               font=ctk.CTkFont(size=16),
                                               command=lambda: self.togglePassDash(3))
        self.btnMostrarConfirm.pack(side="right")
        self.mostrarConfirm = False
        
        ctk.CTkFrame(formFrame, height=2, fg_color="#3a3a3a").pack(pady=20, fill="x")
        
        ctk.CTkLabel(formFrame, text="❓ Pregunta de Seguridad", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#e0e0e0").pack(pady=(0, 15), anchor="w")
        
        # pregunta actual
        ctk.CTkLabel(formFrame, text="📝 Pregunta actual", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        preguntaActualLabel = ctk.CTkLabel(formFrame, text=self.datosUsuario['preguntaSeguridad'],
                                          font=ctk.CTkFont(size=12), text_color="#4a90e2",
                                          anchor="w", wraplength=500)
        preguntaActualLabel.pack(pady=(0, 15), fill="x", padx=10)
        
        # nueva pregunta
        ctk.CTkLabel(formFrame, text="❓ Nueva pregunta", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        
        PREGUNTAS = [
            "¿Cuál es tu fecha de nacimiento?",
            "¿Cuál es el nombre de tu primera mascota?",
            "¿Cuál es tu comida favorita?",
            "¿Cuál es tu ciudad natal?"
        ]
        
        self.preguntaCombo = ctk.CTkComboBox(formFrame, height=42, values=PREGUNTAS,
                                            fg_color="#1e1e1e", border_color="#3a3a3a",
                                            button_color="#4a90e2", dropdown_fg_color="#262626")
        self.preguntaCombo.set(self.datosUsuario['preguntaSeguridad'])
        self.preguntaCombo.pack(pady=(0, 15), fill="x")
        
        # nueva respuesta
        ctk.CTkLabel(formFrame, text="✍️ Nueva respuesta", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#d0d0d0", anchor="w").pack(pady=(0, 5), fill="x")
        self.respuestaEntry = ctk.CTkEntry(formFrame, height=42, fg_color="#1e1e1e",
                                          border_color="#3a3a3a", placeholder_text="Tu respuesta secreta")
        self.respuestaEntry.pack(pady=(0, 25), fill="x")
        
        # boton guardar
        ctk.CTkButton(formFrame, text="🔐 Guardar Cambios de Seguridad", command=self.guardarSeguridad,
                     height=45, fg_color="#d9534f", hover_color="#c9302c",
                     corner_radius=6, font=ctk.CTkFont(size=14, weight="bold")).pack(fill="x")
    
    def validarPasswordNueva(self, event=None):
        password = self.passNuevaEntry.get()
        
        validaciones = [
            (self.req1, len(password) >= 7, "Mínimo 7 caracteres"),
            (self.req2, bool(re.search(r"[A-Z]", password)), "Una mayúscula (A-Z)"),
            (self.req3, bool(re.search(r"[a-z]", password)), "Una minúscula (a-z)"),
            (self.req4, bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)), "Un símbolo (!@#$...)")
        ]
        
        for label, cumple, texto in validaciones:
            icono = "✓" if cumple else "✗"
            color = "#2d7a3e" if cumple else "#d9534f"
            label.configure(text=f"{icono} {texto}", text_color=color)
    
    def togglePassDash(self, campo):
        if campo == 1:
            self.mostrarActual = not self.mostrarActual
            self.passActualEntry.configure(show="" if self.mostrarActual else "●")
            self.btnMostrarActual.configure(text="🙈" if self.mostrarActual else "👁")
        elif campo == 2:
            self.mostrarNueva = not self.mostrarNueva
            self.passNuevaEntry.configure(show="" if self.mostrarNueva else "●")
            self.btnMostrarNueva.configure(text="🙈" if self.mostrarNueva else "👁")
        else:
            self.mostrarConfirm = not self.mostrarConfirm
            self.passConfirmEntry.configure(show="" if self.mostrarConfirm else "●")
            self.btnMostrarConfirm.configure(text="🙈" if self.mostrarConfirm else "👁")
    
    def guardarPerfil(self):
        emailNuevo = self.emailEntry.get().strip()
        nombre = self.nombreEntry.get().strip()
        
        if not emailNuevo:
            messagebox.showerror("Error", "El email no puede estar vacío")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", emailNuevo):
            messagebox.showerror("Error", "Email inválido")
            return
        
        if self.bd.actualizarPerfil(self.userEmail, emailNuevo, nombre):
            self.userEmail = emailNuevo  # actualizar email en la variable
            self.datosUsuario['email'] = emailNuevo
            self.datosUsuario['nombre'] = nombre
            messagebox.showinfo("✅ Éxito", "Perfil actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el perfil.\nEs posible que el email ya esté registrado.")
    
    def guardarSeguridad(self):
        actual = self.passActualEntry.get()
        nueva = self.passNuevaEntry.get()
        confirmar = self.passConfirmEntry.get()
        pregunta = self.preguntaCombo.get()
        respuesta = self.respuestaEntry.get().strip()
        
        if not nueva and not respuesta:
            messagebox.showinfo("Info", "No hay cambios para guardar")
            return
        
        if nueva:
            if not actual:
                messagebox.showerror("Error", "Debes ingresar tu contraseña actual")
                return
            
            if len(nueva) < 7:
                messagebox.showerror("Error", "La contraseña debe tener al menos 7 caracteres")
                return
            if not re.search(r"[A-Z]", nueva):
                messagebox.showerror("Error", "La contraseña debe tener al menos una mayúscula")
                return
            if not re.search(r"[a-z]", nueva):
                messagebox.showerror("Error", "La contraseña debe tener al menos una minúscula")
                return
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", nueva):
                messagebox.showerror("Error", "La contraseña debe tener al menos un símbolo")
                return
            
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
        
        if respuesta and not pregunta:
            messagebox.showerror("Error", "Selecciona una pregunta de seguridad")
            return
        
        if self.bd.actualizarSeguridad(self.userEmail, actual, nueva, pregunta if respuesta else None, respuesta):
            messagebox.showinfo("✅ Éxito", "Configuración de seguridad actualizada correctamente")
            self.passActualEntry.delete(0, 'end')
            self.passNuevaEntry.delete(0, 'end')
            self.passConfirmEntry.delete(0, 'end')
            self.respuestaEntry.delete(0, 'end')
            
            if respuesta:
                self.datosUsuario['preguntaSeguridad'] = pregunta
                self.mostrarSeguridad()
        else:
            messagebox.showerror("Error", "Contraseña actual incorrecta")
    
    def cerrarSesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", 
                                       "¿Estás seguro que deseas cerrar sesión?")
        if respuesta:
            self.destroy()
            self.onLogout()
