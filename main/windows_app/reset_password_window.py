
from tkinter import *
from tkinter import messagebox as MessageBox
import os
import helpers.readfiles as readfiles
import windows_app.login_window as login_w

def ResetPassword(root, mainFrame, correo_usuario):
    root.title("Restablecer Contraseña")
    mainFrame.config(width=425, height=700, bg="white")
    mainFrame.pack()
    my_path = readfiles.Route()

    Label(mainFrame, text="Nueva Contraseña", font=("Arial", 14), bg="white").place(x=130, y=60)
    Label(mainFrame, text=f"Correo: {correo_usuario}", bg="white").place(x=70, y=130)

    Label(mainFrame, text="Nueva contraseña:", bg="white").place(x=70, y=180)
    entry_pass = Entry(mainFrame, show="*", width=30)
    entry_pass.place(x=70, y=205)

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

    Button(mainFrame, text="Guardar nueva contraseña", command=guardar_contraseña).place(x=120, y=260)
