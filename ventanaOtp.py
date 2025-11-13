import customtkinter as ctk
from tkinter import messagebox
import time
from datetime import datetime, timedelta

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
        self.intentosRestantes = 3
        self.tiempoExpiracion = datetime.now() + timedelta(minutes=5)
        self.ventanaCerrada = False
        
        self.title("Verificación OTP")
        
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()
        w = min(520, ancho - 100)
        h = min(580, alto - 100)
        
        x = (ancho // 2) - (w // 2)
        y = (alto // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.configure(fg_color="#1e1e1e")
        self.resizable(False, False)
        
        self.crearInterfaz()
        self.transient(parent)
        self.grab_set()
        
        # iniciar temporizador
        self.actualizarTemporizador()
    
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
        self.otpEntry.bind("<Return>", lambda e: self.validar())
        
        # Label para mostrar intentos restantes
        self.intentosLabel = ctk.CTkLabel(frame, text="💡 Tienes 3 intentos disponibles",
                                         font=ctk.CTkFont(size=11), text_color="#4a90e2")
        self.intentosLabel.pack(pady=(5, 0))
        
        # Label para tiempo restante
        self.tiempoLabel = ctk.CTkLabel(frame, text="⏱️ El código expira en 5 minutos",
                                       font=ctk.CTkFont(size=10), text_color="#8a8a8a")
        self.tiempoLabel.pack(pady=(3, 10))
        
        btnFrame = ctk.CTkFrame(frame, fg_color="transparent")
        btnFrame.pack(pady=25)
        
        ctk.CTkButton(btnFrame, text="✓ Verificar código", command=self.validar,
                     width=165, height=45, fg_color="#2d7a3e", hover_color="#256430",
                     corner_radius=6, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(btnFrame, text="✕ Cancelar", command=self.cancelar,
                     width=165, height=45, fg_color="#505050", hover_color="#404040",
                     corner_radius=6, font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
    
    def cancelar(self):
        self.ventanaCerrada = True
        self.destroy()
    
    def validar(self):
        try:
            codigo = self.otpEntry.get().strip()
            
            if not codigo:
                messagebox.showerror("Error", "Ingresa el código OTP")
                return
            
            # validar que sean exactamente 6 digitos
            if len(codigo) != 6:
                self.intentosRestantes -= 1
                self.otpEntry.delete(0, 'end')
                
                if self.intentosRestantes <= 0:
                    messagebox.showerror("❌ Sin intentos", 
                                       f"Has agotado todos los intentos.\n\n"
                                       f"El código debe tener exactamente 6 dígitos.\n\n"
                                       f"Debes iniciar sesión nuevamente.")
                    self.ventanaCerrada = True
                    self.destroy()
                    return
                else:
                    if self.intentosRestantes == 1:
                        self.intentosLabel.configure(text="⚠️ ÚLTIMO INTENTO disponible", text_color="#d9534f")
                        messagebox.showwarning("Intento fallido", 
                                             f"El código debe tener 6 dígitos, no {len(codigo)}.\n\n"
                                             f"¡Cuidado! Solo tienes 1 intento más.")
                    else:
                        self.intentosLabel.configure(text=f"⚠️ Te quedan {self.intentosRestantes} intentos", text_color="#ff9800")
                        messagebox.showwarning("Intento fallido", 
                                             f"El código debe tener 6 dígitos, no {len(codigo)}.\n\n"
                                             f"Te quedan {self.intentosRestantes} intentos.")
                    return
            
            # validar que sean solo numeros
            if not codigo.isdigit():
                self.intentosRestantes -= 1
                self.otpEntry.delete(0, 'end')
                
                if self.intentosRestantes <= 0:
                    messagebox.showerror("❌ Sin intentos", 
                                       f"Has agotado todos los intentos.\n\n"
                                       f"El código debe contener solo números.\n\n"
                                       f"Debes iniciar sesión nuevamente.")
                    self.ventanaCerrada = True
                    self.destroy()
                    return
                else:
                    if self.intentosRestantes == 1:
                        self.intentosLabel.configure(text="⚠️ ÚLTIMO INTENTO disponible", text_color="#d9534f")
                        messagebox.showwarning("Intento fallido", 
                                             f"El código debe contener solo números.\n\n"
                                             f"¡Cuidado! Solo tienes 1 intento más.")
                    else:
                        self.intentosLabel.configure(text=f"⚠️ Te quedan {self.intentosRestantes} intentos", text_color="#ff9800")
                        messagebox.showwarning("Intento fallido", 
                                             f"El código debe contener solo números.\n\n"
                                             f"Te quedan {self.intentosRestantes} intentos.")
                    return
            
            # ahora si validar con la BD
            resultado = self.bd.validarOTP(self.userId, codigo)
            
            if resultado:
                self.ventanaCerrada = True
                self.destroy()
                self.onSuccess()
            else:
                self.intentosRestantes -= 1
                
                if self.intentosRestantes <= 0:
                    # se acabaron los intentos
                    messagebox.showerror("❌ Sin intentos", 
                                       "Has agotado todos los intentos.\n\n"
                                       "Debes iniciar sesión nuevamente para obtener un nuevo código.")
                    self.ventanaCerrada = True
                    self.destroy()
                else:
                    # aun quedan intentos
                    self.otpEntry.delete(0, 'end')
                    
                    if self.intentosRestantes == 1:
                        self.intentosLabel.configure(
                            text="⚠️ ÚLTIMO INTENTO disponible",
                            text_color="#d9534f"
                        )
                        messagebox.showwarning("Intento fallido", 
                                             f"Código incorrecto.\n\n¡Cuidado! Solo tienes 1 intento más.")
                    else:
                        self.intentosLabel.configure(
                            text=f"⚠️ Te quedan {self.intentosRestantes} intentos",
                            text_color="#ff9800"
                        )
                        messagebox.showwarning("Intento fallido", 
                                             f"Código incorrecto.\n\nTe quedan {self.intentosRestantes} intentos.")
                    
        except Exception as e:
            print(f"Error validando OTP: {e}")
            messagebox.showerror("Error", "Ocurrió un error al validar el código")
    
    def actualizarTemporizador(self):
        if self.ventanaCerrada:
            return
        
        try:
            ahora = datetime.now()
            diferencia = self.tiempoExpiracion - ahora
            
            if diferencia.total_seconds() <= 0:
                # se acabo el tiempo
                if not self.ventanaCerrada:
                    self.ventanaCerrada = True
                    messagebox.showerror("⏰ Tiempo agotado", 
                                       "El código OTP ha expirado.\n\n"
                                       "Debes iniciar sesión nuevamente.")
                    self.destroy()
                return
            
            # calcular minutos y segundos restantes
            segundos_totales = int(diferencia.total_seconds())
            minutos = segundos_totales // 60
            segundos = segundos_totales % 60
            
            # actualizar el label con el tiempo
            if minutos > 0:
                tiempo_texto = f"⏱️ Expira en {minutos}:{segundos:02d} minutos"
            else:
                tiempo_texto = f"⏱️ Expira en {segundos} segundos"
                
            # cambiar color si queda poco tiempo
            if segundos_totales <= 60:
                self.tiempoLabel.configure(text=tiempo_texto, text_color="#d9534f")
            elif segundos_totales <= 120:
                self.tiempoLabel.configure(text=tiempo_texto, text_color="#ff9800")
            else:
                self.tiempoLabel.configure(text=tiempo_texto, text_color="#8a8a8a")
            
            # actualizar cada segundo
            self.after(1000, self.actualizarTemporizador)
            
        except Exception as e:
            print(f"Error en temporizador: {e}")
