from tkinter import *
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import os
import windows_app.reset_password_window as reset_w
import helpers.readfiles as readfiles

def VerifyToken(root, mainFrame, correo_usuario):
    root.title("Verificar código")
    mainFrame.config(width=425, height=700)
    mainFrame.pack()
    my_path = readfiles.Route()

    # Fondo
    try:
        bg_path = os.path.join(my_path, "images", "background-verify.png")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Evita que se borre la imagen
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        mainFrame.config(bg="blue")

    # Contenido
    Label(mainFrame, text=f"Correo: {correo_usuario}", font=("Calibri", 14), fg="white", bg="#090B64").place(x=95, y=318)
    entry_token = Entry(mainFrame, width=30)
    entry_token.place(x=125, y=405)

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

    Button(mainFrame, text="Validar código", command=validar_token, 
           font=("Arial", 11, "underline"), fg="white", bg="#41AADC", 
           relief="flat", activebackground="#0d8ddf", bd=0, padx=15, pady=3).place(x=153, y=462)