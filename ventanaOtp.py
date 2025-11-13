import customtkinter as ctk
from tkinter import messagebox

class VentanaOtp(ctk.CTkToplevel):
    PREGUNTAS = [
        "¿Cuál es tu fecha de nacimiento?",
        "¿Cuál es el nombre de tu primera mascota?",
        "¿Cuál es tu comida favorita?",
        "¿Cuál es tu ciudad natal?"
    ]
    
    def __init__(self, parent, bd, userId, codigoGenerado, onSuccess):
        super().__init__(parent)
        
        self.bd = bd
        self.userId = userId
        self.codigoGenerado = codigoGenerado
        self.onSuccess = onSuccess
        
        self.title("Verificación OTP")
        self.geometry("490x500")
        x = (self.winfo_screenwidth() // 2) - 245
        y = (self.winfo_screenheight() // 2) - 250
        self.geometry(f"490x500+{x}+{y}")
        self.configure(fg_color="#1e1e1e")
        
        self.crearInterfaz()
        self.transient(parent)
        self.grab_set()
    
    def crearInterfaz(self):
        frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="🔒 Verificación OTP", font=ctk.CTkFont(size=26, weight="bold"),
                    text_color="#4a90e2").pack(pady=(25, 10))
        
        ctk.CTkLabel(frame, text="Tu código de acceso temporal",
                    font=ctk.CTkFont(size=12), text_color="#9b9b9b").pack(pady=(0, 20))
        
        codigoFrame = ctk.CTkFrame(frame, fg_color="#262626", corner_radius=10, border_width=2,
                                   border_color="#4a90e2")
        codigoFrame.pack(pady=20, padx=40)
        
        ctk.CTkLabel(codigoFrame, text="CÓDIGO GENERADO:",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="#8a8a8a").pack(padx=40, pady=(15, 5))
        
        ctk.CTkLabel(codigoFrame, text=str(self.codigoGenerado),
                    font=ctk.CTkFont(size=42, weight="bold"),
                    text_color="#4a90e2").pack(padx=40, pady=(0, 15))
        
        ctk.CTkLabel(frame, text="Ingresa el código arriba para verificar tu identidad",
                    font=ctk.CTkFont(size=11), text_color="#a0a0a0").pack(pady=(20, 8))
        
        self.otpEntry = ctk.CTkEntry(frame, width=350, height=50, 
                                     placeholder_text="Ingresa 6 dígitos",
                                     fg_color="#262626", border_color="#3a3a3a", border_width=1,
                                     corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                                     text_color="#ffffff", placeholder_text_color="#6b6b6b",
                                     justify="center")
        self.otpEntry.pack(pady=8)
        
        btnFrame = ctk.CTkFrame(frame, fg_color="transparent")
        btnFrame.pack(pady=25)
        
        ctk.CTkButton(btnFrame, text="✓ Verificar código", command=self.validar,
                     width=165, height=45, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(btnFrame, text="✕ Cancelar", command=self.destroy,
                     width=165, height=45, fg_color="#505050", hover_color="#404040",
                     corner_radius=6, font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
    
    def validar(self):
        try:
            codigo = self.otpEntry.get().strip()
            
            if not codigo:
                messagebox.showerror("Error", "Ingresa el código OTP")
                return
            
            resultado = self.bd.validarOTP(self.userId, codigo)
            
            if resultado:
                self.destroy()
                self.onSuccess()
            else:
                messagebox.showerror("Error", "Código incorrecto, expirado o sin intentos")
        except Exception as e:
            print(f"Error validando OTP: {e}")
            messagebox.showerror("Error", "Ocurrió un error al validar el código")
