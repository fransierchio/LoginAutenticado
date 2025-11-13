import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ServicioCorreo:
    def __init__(self):
        self.correoRemitente = "codigogenerador45@gmail.com"
        self.passwordApp = "gvszgpushpbwohkq"
        self.servidorSmtp = "smtp.gmail.com"
        self.puertoSmtp = 587
    
    def enviarOTP(self, correoDestino, codigoOTP):
        try:
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = "🔐 Código de Verificación - Sistema de Autenticación"
            mensaje["From"] = self.correoRemitente
            mensaje["To"] = correoDestino
            
            textoPlano = f"""
Código de Verificación
            
Tu código OTP es: {codigoOTP}

Este código es válido por 5 minutos.
No compartas este código con nadie.

Si no solicitaste este código, ignora este mensaje.
            """
            
            textoHtml = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                  <h2 style="color: #4a90e2; text-align: center;">🔐 Código de Verificación</h2>
                  <p style="color: #666; font-size: 16px;">Hola,</p>
                  <p style="color: #666; font-size: 16px;">Tu código OTP para acceder al sistema es:</p>
                  <div style="background-color: #f0f7ff; border-left: 4px solid #4a90e2; padding: 20px; margin: 20px 0; text-align: center;">
                    <h1 style="color: #4a90e2; font-size: 42px; margin: 0; letter-spacing: 5px;">{codigoOTP}</h1>
                  </div>
                  <p style="color: #666; font-size: 14px;">⏱️ Este código es válido por <strong>5 minutos</strong>.</p>
                  <p style="color: #666; font-size: 14px;">🔒 Por tu seguridad, no compartas este código con nadie.</p>
                  <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                  <p style="color: #999; font-size: 12px; text-align: center;">Si no solicitaste este código, ignora este mensaje.</p>
                </div>
              </body>
            </html>
            """
            
            partePlano = MIMEText(textoPlano, "plain")
            parteHtml = MIMEText(textoHtml, "html")
            
            mensaje.attach(partePlano)
            mensaje.attach(parteHtml)
            
            with smtplib.SMTP(self.servidorSmtp, self.puertoSmtp) as servidor:
                servidor.starttls()
                servidor.login(self.correoRemitente, self.passwordApp)
                servidor.send_message(mensaje)
            
            return True
        except Exception as e:
            print(f"Error al enviar correo OTP: {e}")
            return False
    
    def enviarPasswordTemporal(self, correoDestino, passwordTemporal):
        try:
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = "🔑 Contraseña Temporal - Recuperación de Cuenta"
            mensaje["From"] = self.correoRemitente
            mensaje["To"] = correoDestino
            
            textoPlano = f"""
Recuperación de Contraseña
            
Tu nueva contraseña temporal es: {passwordTemporal}

Por seguridad, cambia esta contraseña después de iniciar sesión.

Si no solicitaste esta recuperación, contacta al administrador inmediatamente.
            """
            
            textoHtml = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                  <h2 style="color: #d9534f; text-align: center;">🔑 Recuperación de Cuenta</h2>
                  <p style="color: #666; font-size: 16px;">Hola,</p>
                  <p style="color: #666; font-size: 16px;">Tu contraseña ha sido restablecida. Tu nueva contraseña temporal es:</p>
                  <div style="background-color: #fff5f5; border-left: 4px solid #d9534f; padding: 20px; margin: 20px 0; text-align: center;">
                    <h3 style="color: #d9534f; font-size: 24px; margin: 0; font-family: 'Courier New', monospace;">{passwordTemporal}</h3>
                  </div>
                  <p style="color: #d9534f; font-size: 14px;">⚠️ <strong>IMPORTANTE:</strong> Cambia esta contraseña después de iniciar sesión.</p>
                  <p style="color: #666; font-size: 14px;">🔐 Por tu seguridad, usa una contraseña fuerte y única.</p>
                  <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                  <p style="color: #999; font-size: 12px; text-align: center;">Si no solicitaste esta recuperación, contacta al administrador inmediatamente.</p>
                </div>
              </body>
            </html>
            """
            
            partePlano = MIMEText(textoPlano, "plain")
            parteHtml = MIMEText(textoHtml, "html")
            
            mensaje.attach(partePlano)
            mensaje.attach(parteHtml)
            
            with smtplib.SMTP(self.servidorSmtp, self.puertoSmtp) as servidor:
                servidor.starttls()
                servidor.login(self.correoRemitente, self.passwordApp)
                servidor.send_message(mensaje)
            
            return True
        except Exception as e:
            print(f"Error al enviar correo de contraseña temporal: {e}")
            return False
