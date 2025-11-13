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
        # Tabla de usuarios
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                passwordHash TEXT NOT NULL,
                securityQuestion TEXT NOT NULL,
                securityAnswerHash TEXT NOT NULL
            )
        """)
        
        # Tabla de códigos OTP
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
        except:
            return False
    
    def login(self, email, password):
        try:
            passHash = self.hash(password)
            self.cursor.execute("SELECT id FROM users WHERE email = ? AND passwordHash = ?", 
                              (email, passHash))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except:
            return None
    
    def generarOTP(self, userId):
        try:
            codigo = ''.join(random.choices(string.digits, k=6))
            expira = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO otpCodes (userId, code, expiresAt, attempts, used) VALUES (?, ?, ?, 0, 0)",
                              (userId, codigo, expira))
            self.conn.commit()
            return codigo
        except:
            return '000000'
    
    def validarOTP(self, userId, codigo):
        try:
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
            
            expiraFecha = datetime.strptime(expira, "%Y-%m-%d %H:%M:%S")
            if datetime.now() > expiraFecha:
                return False
            
            if intentos >= 3:
                return False
            
            self.cursor.execute("UPDATE otpCodes SET attempts = attempts + 1 WHERE id = ?", (otpId,))
            self.conn.commit()
            
            if codigo == codigoGuardado:
                self.cursor.execute("UPDATE otpCodes SET used = 1 WHERE id = ?", (otpId,))
                self.conn.commit()
                return True
            return False
        except:
            return False
    
    def validarRespuestaSeguridad(self, email, pregunta, respuesta):
        try:
            respHash = self.hash(respuesta.lower().strip())
            self.cursor.execute("SELECT id FROM users WHERE email = ? AND securityQuestion = ? AND securityAnswerHash = ?",
                              (email, pregunta, respHash))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except:
            return None
    
    def generarPasswordTemporal(self, userId):
        try:
            chars = string.ascii_letters + string.digits + "!@#$%&*"
            temp = (random.choice(string.ascii_uppercase) +
                   random.choice(string.ascii_lowercase) +
                   random.choice("!@#$%&*") +
                   ''.join(random.choices(chars, k=7)))
            passHash = self.hash(temp)
            self.cursor.execute("UPDATE users SET passwordHash = ? WHERE id = ?", (passHash, userId))
            self.conn.commit()
            return temp
        except:
            return "Error123!"
    
    def cerrar(self):
        self.conn.close()
