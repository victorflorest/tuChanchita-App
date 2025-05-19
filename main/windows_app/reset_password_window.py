from tkinter import *
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import os
import helpers.readfiles as readfiles
import windows_app.login_window as login_w

def ResetPassword(root, mainFrame, correo_usuario):
    root.title("Restablecer Contraseña")
    mainFrame.config(width=425, height=700)
    mainFrame.pack()
    my_path = readfiles.Route()

    # Fondo
    try:
        bg_path = os.path.join(my_path, "images", "background-reset-password.png")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Evita que se borre por el recolector de basura
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        mainFrame.config(bg="white")

    # Etiquetas y campos
    Label(mainFrame, text=f"Correo: {correo_usuario}", font=("Calibri", 14), fg="white", bg="#090B64").place(x=95, y=318)
    entry_pass = Entry(mainFrame, width=30)
    entry_pass.place(x=125, y=405)

    def guardar_contraseña():
        nueva = entry_pass.get().strip()
        if not nueva:
            MessageBox.showwarning("Vacío", "Ingresa una nueva contraseña.")
            return

        users_path = os.path.join(my_path, "fakedb", "users.txt")
        tokens_path = os.path.join(my_path, "fakedb", "recovery_tokens.txt")

        try:
            with open(users_path, "r", encoding="utf-8") as f:
                users = [line.strip().split(",") for line in f if line.strip()]
            for user in users:
                if user[0] == correo_usuario:
                    user[1] = nueva
                    break
            with open(users_path, "w", encoding="utf-8") as f:
                for user in users:
                    f.write(",".join(user) + "\n")

            # Eliminar token utilizado
            with open(tokens_path, "r", encoding="utf-8") as f:
                tokens = [line for line in f if not line.startswith(correo_usuario + ",")]
            with open(tokens_path, "w", encoding="utf-8") as f:
                f.writelines(tokens)

            MessageBox.showinfo("Listo", "Contraseña actualizada.")
            mainFrame.destroy()
            login_w.Login(root, Frame(root))

        except Exception as e:
            print("Error cambiando la contraseña:", e)
            MessageBox.showerror("Error", "No se pudo actualizar la contraseña.")

    Button(mainFrame, text="Guardar nueva contraseña", command=guardar_contraseña, 
           font=("Arial", 11, "underline"), fg="white", bg="#41AADC", 
           relief="flat", activebackground="#0d8ddf", bd=0, padx=15, pady=3).place(x=110, y=462)