import customtkinter as ctk
from tkinter import messagebox
from baseDatos import BaseDatos
from ventanaRegistro import VentanaRegistro
from ventanaOtp import VentanaOtp
from ventanaRecuperacion import VentanaRecuperacion
from servicioCorreo import ServicioCorreo

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.bd = BaseDatos()
        self.servicioCorreo = ServicioCorreo()
        
        self.title("Autenticación")
        self.state('zoomed')
        
        self.configure(fg_color="#121212")
        self.crearInterfaz()
        
        self.protocol("WM_DELETE_WINDOW", self.alCerrar)
    
    def crearInterfaz(self):
        ctk.CTkLabel(self, text="🔐 Autenticación", font=ctk.CTkFont(size=32, weight="bold"),
                    text_color="#4a90e2").pack(pady=(50, 10))
        
        ctk.CTkLabel(self, text="Accede a tu cuenta de forma segura",
                    font=ctk.CTkFont(size=13), text_color="#9b9b9b").pack(pady=(0, 30))
        
        frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12, border_width=1,
                            border_color="#2a2a2a")
        frame.pack(padx=60, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Correo electrónico", font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#e0e0e0", anchor="w").pack(pady=(30, 5), padx=40, fill="x")
        self.emailEntry = ctk.CTkEntry(frame, width=400, height=45, 
                                       placeholder_text="usuario@ejemplo.com",
                                       fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                       corner_radius=6, text_color="#ffffff",
                                       placeholder_text_color="#6b6b6b")
        self.emailEntry.pack(pady=(0, 20), padx=40)
        
        ctk.CTkLabel(frame, text="Contraseña", font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#e0e0e0", anchor="w").pack(pady=(0, 5), padx=40, fill="x")
        self.passwordEntry = ctk.CTkEntry(frame, width=400, height=45, show="●",
                                          placeholder_text="Ingresa tu contraseña",
                                          fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                          corner_radius=6, text_color="#ffffff",
                                          placeholder_text_color="#6b6b6b")
        self.passwordEntry.pack(pady=(0, 30), padx=40)
        self.passwordEntry.bind("<Return>", lambda e: self.iniciarSesion())
        
        ctk.CTkButton(frame, text="INICIAR SESIÓN", command=self.iniciarSesion,
                     width=400, height=50, fg_color="#4a90e2", hover_color="#357abd",
                     corner_radius=6, font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffffff").pack(pady=(0, 15), padx=40)
        
        separator = ctk.CTkFrame(frame, height=1, fg_color="#2a2a2a")
        separator.pack(pady=20, padx=40, fill="x")
        
        ctk.CTkLabel(frame, text="¿No tienes cuenta o necesitas ayuda?",
                    font=ctk.CTkFont(size=11), text_color="#8a8a8a").pack(pady=(0, 15))
        
        btnFrame = ctk.CTkFrame(frame, fg_color="transparent")
        btnFrame.pack(pady=(0, 30))
        
        ctk.CTkButton(btnFrame, text="📝 Crear cuenta nueva", command=self.abrirRegistro,
                     width=190, height=42, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(btnFrame, text="🔑 Recuperar acceso", command=self.abrirRecuperacion,
                     width=190, height=42, fg_color="#d9534f", hover_color="#c9302c",
                     corner_radius=6, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
    
    def iniciarSesion(self):
        try:
            email = self.emailEntry.get().strip()
            password = self.passwordEntry.get()
            
            if not email or not password:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            userId = self.bd.login(email, password)
            
            if userId:
                codigo = self.bd.generarOTP(userId)
                
                try:
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
                except Exception as e:
                    print(f"Error enviando correo: {e}")
                    messagebox.showwarning("Advertencia",
                                         f"No se pudo enviar el correo.\n"
                                         f"Tu código OTP es: {codigo}")
                
                self.abrirOTP(userId, codigo)
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos")
        except Exception as e:
            print(f"Error en inicio de sesión: {e}")
            messagebox.showerror("Error", "Ocurrió un error. Por favor intenta de nuevo.")
    
    def abrirRegistro(self):
        try:
            VentanaRegistro(self, self.bd, onSuccess=self.limpiarCampos)
        except Exception as e:
            print(f"Error abriendo registro: {e}")
            messagebox.showerror("Error", "No se pudo abrir la ventana de registro")
    
    def abrirOTP(self, userId, codigo):
        try:
            VentanaOtp(self, self.bd, userId, codigo, onSuccess=self.mostrarExito)
        except Exception as e:
            print(f"Error abriendo OTP: {e}")
            messagebox.showerror("Error", "No se pudo abrir la ventana OTP")
    
    def abrirRecuperacion(self):
        try:
            VentanaRecuperacion(self, self.bd, self.servicioCorreo, onSuccess=self.limpiarCampos)
        except Exception as e:
            print(f"Error abriendo recuperación: {e}")
            messagebox.showerror("Error", "No se pudo abrir la ventana de recuperación")
    
    def limpiarCampos(self):
        self.emailEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
    
    def mostrarExito(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Éxito")
        ventana.geometry("450x320")
        x = (ventana.winfo_screenwidth() // 2) - 225
        y = (ventana.winfo_screenheight() // 2) - 160
        ventana.geometry(f"450x320+{x}+{y}")
        ventana.configure(fg_color="#1e1e1e")
        
        frame = ctk.CTkFrame(ventana, fg_color="#1e1e1e", corner_radius=12)
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        ctk.CTkLabel(frame, text="✅", font=ctk.CTkFont(size=70)).pack(pady=(20, 10))
        ctk.CTkLabel(frame, text="¡Acceso autorizado!",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#2d7a3e").pack(pady=5)
        ctk.CTkLabel(frame, text="Has iniciado sesión correctamente",
                    font=ctk.CTkFont(size=13), text_color="#a0a0a0").pack(pady=(5, 25))
        
        ctk.CTkButton(frame, text="Continuar →", command=ventana.destroy,
                     width=250, height=45, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(0, 15))
        
        ventana.transient(self)
        ventana.grab_set()
        self.limpiarCampos()
    
    def alCerrar(self):
        self.bd.cerrar()
        self.destroy()

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
