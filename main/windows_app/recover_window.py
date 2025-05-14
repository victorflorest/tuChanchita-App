
from tkinter import *
from tkinter import messagebox as MessageBox
import helpers.readfiles as readfiles
import helpers.email_sender as mailer
import random, string, os

import windows_app.verify_token_window as verify_token_w

def Recover(root, mainFrame):
    root.title("Recuperación de contraseña")
    mainFrame.config(width=425, height=700, bg="white")
    mainFrame.pack()
    my_path = readfiles.Route()

    Label(mainFrame, text="Recuperar contraseña", font=("Arial", 14), bg="white").place(x=110, y=60)

    Label(mainFrame, text="Correo registrado:", bg="white").place(x=70, y=150)
    entry_email = Entry(mainFrame, width=30)
    entry_email.place(x=70, y=175)

    def generar_token():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def enviar_codigo():
        correo = entry_email.get().strip()
        if not correo:
            MessageBox.showwarning("Campo vacío", "Por favor, escribe tu correo.")
            return

        users_path = os.path.join(my_path, "fakedb", "users.txt")
        tokens_path = os.path.join(my_path, "fakedb", "recovery_tokens.txt")

        try:
            with open(users_path, "r", encoding="utf-8") as f:
                usuarios = [line.strip().split(",") for line in f if line.strip()]
            if not any(user[0] == correo for user in usuarios):
                MessageBox.showerror("Error", "El correo no está registrado.")
                return
        except:
            MessageBox.showerror("Error", "No se pudo leer la base de datos de usuarios.")
            return

        token = generar_token()

        try:
            with open(tokens_path, "a", encoding="utf-8") as f:
                f.write(f"{correo},{token}\n")
        except:
            MessageBox.showerror("Error", "No se pudo guardar el token.")
            return

        # CONFIGURA TU CORREO EMISOR ABAJO
        remitente = "gianfranco22.ft@gmail.com"
        clave_app = "rdqw ueyn bjql jtve"

        if mailer.enviar_token(correo, token, remitente, clave_app):
            MessageBox.showinfo("Correo enviado", "Hemos enviado un código a tu correo.")
            mainFrame.destroy()
            verify_token_w.VerifyToken(root, Frame(root), correo)
        else:
            MessageBox.showerror("Error", "No se pudo enviar el correo. Revisa la configuración.")

    Button(mainFrame, text="Enviar código", command=enviar_codigo).place(x=150, y=230)
