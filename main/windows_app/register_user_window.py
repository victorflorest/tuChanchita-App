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
    import os
    from PIL import Image, ImageTk

    root.title("Registro de Usuario")
    mainFrame.destroy()
    mainFrame = Frame(root)
    mainFrame.config(width=425, height=700)
    mainFrame.pack()

    # Cargar fondo igual que en Login
    my_path = readfiles.Route()
    try:
        bg_path = os.path.join(my_path, "images", "background-user-register.png")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Evita recolección de basura
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        mainFrame.config(bg="white")

    # Entradas y etiquetas sobre el fondo

    entry_nombre = Entry(mainFrame, width=14)
    entry_nombre.place(x=140, y=345)

    entry_apellido = Entry(mainFrame, width=14)
    entry_apellido.place(x=235, y=345)

    entry_correo = Entry(mainFrame, width=26)
    entry_correo.place(x=160, y=433)

    entry_password = Entry(mainFrame, width=26, show="*")
    entry_password.place(x=160, y=520)

    Button(mainFrame, text="Registrarse", command=lambda: save_user(
        entry_nombre.get().strip(),
        entry_apellido.get().strip(),
        entry_correo.get().strip(),
        entry_password.get().strip(),
        root, mainFrame), font=("Arial", 11), bg="#41AADC", fg="white", activebackground="#0d8ddf",
           relief="flat", bd=0, padx=11, pady=3).place(x=93, y=595)

    Button(mainFrame, text="Volver", command=lambda: [mainFrame.destroy(), login_w.Login(root, Frame(root))], font=("Arial", 11), bg="#41AADC", fg="white", activebackground="#0d8ddf",
           relief="flat", bd=0, padx=28, pady=3).place(x=233, y=595)
