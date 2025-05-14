from tkinter import *
from tkinter import messagebox as MessageBox
import helpers.readfiles as readfiles
import os
import windows_app.login_window as login_w

def save_user(nombre, apellido, correo, password, root, mainFrame):
    if not nombre or not apellido or not correo or not password:
        MessageBox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return

    ruta = readfiles.Route()
    usuarios_path = os.path.join(ruta, "fakedb", "users.txt")

    # Verificar si el correo ya existe
    try:
        with open(usuarios_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts and parts[0] == correo:
                    MessageBox.showerror("Error", "El correo ya está registrado.")
                    return
    except FileNotFoundError:
        pass  # si no existe el archivo, lo crearemos

    # Guardar usuario
    with open(usuarios_path, "a", encoding="utf-8") as f:
        f.write(f"{correo},{password},{nombre},{apellido}\n")

    MessageBox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    mainFrame.destroy()
    login_w.Login(root, Frame(root))


def RegisterUserWindow(root, mainFrame):
    root.title("Registro de Usuario")
    mainFrame.destroy()
    mainFrame = Frame()
    mainFrame.config(width=425, height=500, bg="white")
    mainFrame.pack()

    Label(mainFrame, text="Crear cuenta", font=("Arial", 16), bg="white").place(x=150, y=30)

    Label(mainFrame, text="Nombre:", bg="white").place(x=70, y=100)
    entry_nombre = Entry(mainFrame, width=30)
    entry_nombre.place(x=70, y=125)

    Label(mainFrame, text="Apellido:", bg="white").place(x=70, y=160)
    entry_apellido = Entry(mainFrame, width=30)
    entry_apellido.place(x=70, y=185)

    Label(mainFrame, text="Correo electrónico:", bg="white").place(x=70, y=220)
    entry_correo = Entry(mainFrame, width=30)
    entry_correo.place(x=70, y=245)

    Label(mainFrame, text="Contraseña:", bg="white").place(x=70, y=280)
    entry_password = Entry(mainFrame, width=30, show="*")
    entry_password.place(x=70, y=305)

    Button(mainFrame, text="Registrarse", width=15, command=lambda: save_user(
        entry_nombre.get().strip(),
        entry_apellido.get().strip(),
        entry_correo.get().strip(),
        entry_password.get().strip(),
        root, mainFrame)).place(x=150, y=370)

    Button(mainFrame, text="Volver al Login", command=lambda: [mainFrame.destroy(), login_w.Login(root, Frame(root))]).place(x=155, y=420)
