import customtkinter as ctk
from tkinter import messagebox
from baseDatos import BaseDatos
from ventanaRegistro import VentanaRegistro
from ventanaOtp import VentanaOtp
from ventanaRecuperacion import VentanaRecuperacion
from servicioCorreo import ServicioCorreo
from ventanaDashboard import VentanaDashboard

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.bd = BaseDatos()
        self.servicioCorreo = ServicioCorreo()
        
        self.title("Autenticación")
        
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        w = min(1000, int(ancho_pantalla * 0.7))
        h = min(700, int(alto_pantalla * 0.8))
        
        x = (ancho_pantalla // 2) - (w // 2)
        y = (alto_pantalla // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.minsize(800, 600)
        
        self.configure(fg_color="#121212")
        self.crearInterfaz()
        
        self.protocol("WM_DELETE_WINDOW", self.alCerrar)
    
    def crearInterfaz(self):
        mainContainer = ctk.CTkFrame(self, fg_color="#121212")
        mainContainer.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(mainContainer, text="🔐 Autenticación", font=ctk.CTkFont(size=32, weight="bold"),
                    text_color="#4a90e2").pack(pady=(30, 10))
        
        ctk.CTkLabel(mainContainer, text="Accede a tu cuenta de forma segura",
                    font=ctk.CTkFont(size=13), text_color="#9b9b9b").pack(pady=(0, 20))
        
        frame = ctk.CTkFrame(mainContainer, fg_color="#1e1e1e", corner_radius=12, border_width=1,
                            border_color="#2a2a2a")
        frame.pack(padx=40, pady=10, fill="both", expand=True)

        innerFrame = ctk.CTkFrame(frame, fg_color="transparent")
        innerFrame.pack(fill="both", expand=True, padx=40, pady=30)
        
        ctk.CTkLabel(innerFrame, text="Correo electrónico", font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#e0e0e0", anchor="w").pack(pady=(0, 5), fill="x")
        self.emailEntry = ctk.CTkEntry(innerFrame, height=45, 
                                       placeholder_text="usuario@ejemplo.com",
                                       fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                       corner_radius=6, text_color="#ffffff",
                                       placeholder_text_color="#6b6b6b")
        self.emailEntry.pack(pady=(0, 20), fill="x")
        
        ctk.CTkLabel(innerFrame, text="Contraseña", font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#e0e0e0", anchor="w").pack(pady=(0, 5), fill="x")
        
        passFrame = ctk.CTkFrame(innerFrame, fg_color="transparent")
        passFrame.pack(pady=(0, 25), fill="x")
        
        self.passwordEntry = ctk.CTkEntry(passFrame, height=45, show="●",
                                          placeholder_text="Ingresa tu contraseña",
                                          fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                          corner_radius=6, text_color="#ffffff",
                                          placeholder_text_color="#6b6b6b")
        self.passwordEntry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.passwordEntry.bind("<Return>", lambda e: self.iniciarSesion())
        
        self.mostrarPassVar = False
        self.btnMostrarPass = ctk.CTkButton(passFrame, text="👁", width=45, height=45,
                                           fg_color="#3a3a3a", hover_color="#4a4a4a",
                                           font=ctk.CTkFont(size=16),
                                           command=self.togglePassword)
        self.btnMostrarPass.pack(side="right")
        
        ctk.CTkButton(innerFrame, text="INICIAR SESIÓN", command=self.iniciarSesion,
                     height=50, fg_color="#4a90e2", hover_color="#357abd",
                     corner_radius=6, font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff").pack(pady=(0, 15), fill="x")
        
        separator = ctk.CTkFrame(innerFrame, height=1, fg_color="#2a2a2a")
        separator.pack(pady=15, fill="x")
        
        ctk.CTkLabel(innerFrame, text="¿No tienes cuenta o necesitas ayuda?",
                    font=ctk.CTkFont(size=11), text_color="#8a8a8a").pack(pady=(0, 12))
        
        btnFrame = ctk.CTkFrame(innerFrame, fg_color="transparent")
        btnFrame.pack(pady=(0, 10), fill="x")
        
        btnFrame.grid_columnconfigure(0, weight=1)
        btnFrame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkButton(btnFrame, text="📝 Crear cuenta nueva", command=self.abrirRegistro,
                     height=42, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btnFrame, text="🔑 Recuperar acceso", command=self.abrirRecuperacion,
                     height=42, fg_color="#d9534f", hover_color="#c9302c",
                     corner_radius=6, font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, padx=5, sticky="ew")
    
    def iniciarSesion(self):
        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        
        userId = self.bd.login(email, password)
        
        if userId:
            self.currentUserEmail = email
            codigo = self.bd.generarOTP(userId)
            
            enviado = self.servicioCorreo.enviarOTP(email, codigo)
            if enviado:
                messagebox.showinfo("✓ Correo enviado", 
                                  f"Se ha enviado un código OTP a tu correo electrónico.\n\n"
                                  f"Revisa tu bandeja de entrada y spam.\n\n"
                                  f"Código: {codigo}")
            else:
                messagebox.showwarning("Advertencia",
                                     f"No se pudo enviar el correo.\n"
                                     f"Tu código OTP es: {codigo}")
            
            self.abrirOTP(userId, codigo)
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")
    
    def abrirRegistro(self):
        VentanaRegistro(self, self.bd, onSuccess=self.limpiarCampos)
    
    def abrirOTP(self, userId, codigo):
        VentanaOtp(self, self.bd, userId, codigo, onSuccess=self.mostrarExito)
    
    def abrirRecuperacion(self):
        VentanaRecuperacion(self, self.bd, self.servicioCorreo, onSuccess=self.limpiarCampos)
    
    def limpiarCampos(self):
        self.emailEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.passwordEntry.configure(show="●")
        self.mostrarPassVar = False
        self.btnMostrarPass.configure(text="👁")
    
    def togglePassword(self):
        self.mostrarPassVar = not self.mostrarPassVar
        if self.mostrarPassVar:
            self.passwordEntry.configure(show="")
            self.btnMostrarPass.configure(text="🙈")
        else:
            self.passwordEntry.configure(show="●")
            self.btnMostrarPass.configure(text="👁")
    
    def mostrarExito(self):
        self.limpiarCampos()
        VentanaDashboard(self, self.bd, self.currentUserEmail, onLogout=self.limpiarCampos)
    
    def alCerrar(self):
        self.bd.cerrar()
        self.destroy()

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
