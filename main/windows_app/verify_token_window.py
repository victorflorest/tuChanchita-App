
from tkinter import *
from tkinter import messagebox as MessageBox
import os
import windows_app.reset_password_window as reset_w
import helpers.readfiles as readfiles

def VerifyToken(root, mainFrame, correo_usuario):
    root.title("Verificar código")
    mainFrame.config(width=425, height=700, bg="white")
    mainFrame.pack()
    my_path = readfiles.Route()

    Label(mainFrame, text="Verificar código de seguridad", font=("Arial", 14), bg="white").place(x=80, y=60)
    Label(mainFrame, text=f"Correo: {correo_usuario}", bg="white").place(x=70, y=130)

    Label(mainFrame, text="Código recibido:", bg="white").place(x=70, y=180)
    entry_token = Entry(mainFrame, width=30)
    entry_token.place(x=70, y=205)

    def validar_token():
        token_ingresado = entry_token.get().strip()
        tokens_path = os.path.join(my_path, "fakedb", "recovery_tokens.txt")

        try:
            with open(tokens_path, "r", encoding="utf-8") as f:
                registros = [line.strip().split(",") for line in f if line.strip()]
        except:
            MessageBox.showerror("Error", "No se pudo acceder a los tokens.")
            return

        for correo, token in registros:
            if correo == correo_usuario and token == token_ingresado:
                MessageBox.showinfo("Éxito", "Código verificado correctamente.")
                mainFrame.destroy()
                reset_w.ResetPassword(root, Frame(root), correo_usuario)
                return

        MessageBox.showerror("Inválido", "El código ingresado no es válido.")

    Button(mainFrame, text="Validar código", command=validar_token).place(x=150, y=260)
