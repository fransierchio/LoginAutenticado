import sqlite3
import hashlib
from datetime import datetime, timedelta
import random
import string

class BaseDatos:
    def __init__(self):
        self.conn = sqlite3.connect("auth.db")
        self.cursor = self.conn.cursor()
        self.crearTablas()
    
    def crearTablas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                passwordHash TEXT NOT NULL,
                securityQuestion TEXT NOT NULL,
                securityAnswerHash TEXT NOT NULL,
                nombre TEXT DEFAULT '',
                telefono TEXT DEFAULT ''
            )
        """)
        
        columnas_adicionales = [
            "ALTER TABLE users ADD COLUMN nombre TEXT DEFAULT ''",
            "ALTER TABLE users ADD COLUMN telefono TEXT DEFAULT ''"
        ]
        
        for columna in columnas_adicionales:
            try:
                self.cursor.execute(columna)
            except sqlite3.OperationalError:
                pass
        
        # Códigos OTP
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS otpCodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER NOT NULL,
                code TEXT NOT NULL,
                expiresAt TEXT NOT NULL,
                attempts INTEGER DEFAULT 0,
                used INTEGER DEFAULT 0,
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        """)
        
        self.conn.commit()
    
    def hash(self, texto):
        return hashlib.sha256(texto.encode()).hexdigest()
    
    def registrar(self, email, password, pregunta, respuesta):
        try:
            passHash = self.hash(password)
            respHash = self.hash(respuesta.lower().strip())
            self.cursor.execute("INSERT INTO users (email, passwordHash, securityQuestion, securityAnswerHash) VALUES (?, ?, ?, ?)",
                              (email, passHash, pregunta, respHash))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def login(self, email, password):
        passHash = self.hash(password)
        self.cursor.execute("SELECT id FROM users WHERE email = ? AND passwordHash = ?",
                          (email, passHash))
        res = self.cursor.fetchone()
        return res[0] if res else None
    
    def generarOTP(self, userId):
        codigo = ''.join(random.choices(string.digits, k=6))
        expira = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO otpCodes (userId, code, expiresAt, attempts, used) VALUES (?, ?, ?, 0, 0)",
                          (userId, codigo, expira))
        self.conn.commit()
        return codigo
    
    def validarOTP(self, userId, codigo):
        self.cursor.execute("""
            SELECT id, code, expiresAt, attempts
            FROM otpCodes
            WHERE userId = ? AND used = 0
            ORDER BY id DESC
            LIMIT 1
        """, (userId,))
        
        result = self.cursor.fetchone()
        if not result:
            return False
        
        otpId, codigoGuardado, expira, intentos = result
        
        expirationTime = datetime.strptime(expira, "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expirationTime or intentos >= 3:
            return False
        
        self.cursor.execute("UPDATE otpCodes SET attempts = attempts + 1 WHERE id = ?", (otpId,))
        self.conn.commit()
        
        if codigo == codigoGuardado:
            self.cursor.execute("UPDATE otpCodes SET used = 1 WHERE id = ?", (otpId,))
            self.conn.commit()
            return True
        return False
    
    def validarRespuestaSeguridad(self, email, pregunta, respuesta):
        respHash = self.hash(respuesta.lower().strip())
        self.cursor.execute("SELECT id FROM users WHERE email = ? AND securityQuestion = ? AND securityAnswerHash = ?",
                          (email, pregunta, respHash))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def generarPasswordTemporal(self, userId):
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        temp = (random.choice(string.ascii_uppercase) +
               random.choice(string.ascii_lowercase) +
               random.choice("!@#$%&*") +
               ''.join(random.choices(chars, k=7)))
        passHash = self.hash(temp)
        self.cursor.execute("UPDATE users SET passwordHash = ? WHERE id = ?", (passHash, userId))
        self.conn.commit()
        return temp
    
    def obtenerDatosUsuario(self, email):
        self.cursor.execute("SELECT id, email, nombre, securityQuestion, securityAnswerHash FROM users WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'email': result[1],
                'nombre': result[2] or '',
                'preguntaSeguridad': result[3],
                'respuestaHash': result[4]
            }
        return None
    
    def actualizarPerfil(self, emailActual, emailNuevo, nombre):
        try:
            if emailActual != emailNuevo:
                self.cursor.execute("SELECT id FROM users WHERE email = ?", (emailNuevo,))
                if self.cursor.fetchone():
                    return False
            
            self.cursor.execute("UPDATE users SET email = ?, nombre = ? WHERE email = ?", 
                              (emailNuevo, nombre, emailActual))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def actualizarSeguridad(self, email, passwordActual, passwordNueva, pregunta, respuesta):
        if passwordNueva:
            hashActual = self.hash(passwordActual)
            self.cursor.execute("SELECT id FROM users WHERE email = ? AND passwordHash = ?", 
                              (email, hashActual))
            if not self.cursor.fetchone():
                return False
            
            hashNueva = self.hash(passwordNueva)
            self.cursor.execute("UPDATE users SET passwordHash = ? WHERE email = ?", 
                              (hashNueva, email))
        
        if pregunta and respuesta:
            respHash = self.hash(respuesta.lower().strip())
            self.cursor.execute("UPDATE users SET securityQuestion = ?, securityAnswerHash = ? WHERE email = ?",
                              (pregunta, respHash, email))
        
        self.conn.commit()
        return True
    
    def cerrar(self):
        self.conn.close()
