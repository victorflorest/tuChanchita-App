from tkinter import *
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk, ImageDraw
import windows_app.dashboard_window as dashboard_w
import windows_app.register_window as register_w
import windows_app.recover_window as recover_w
import windows_app.register_user_window as register_user_w
import helpers.readfiles as readfiles
import os

def rounded_rectangle_image(width, height, radius, fill):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=fill)
    return ImageTk.PhotoImage(img)

def Login(root, mainFrame):
    root.title("Inicio de sesión")
    mainFrame.config(width=425, height=700)
    mainFrame.pack()
    my_path = readfiles.Route()

    # Fondo
    try:
        bg_path = os.path.join(my_path, "images", "background-login.png")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        mainFrame.config(bg="blue")

    # Campos centrados
    entry_email = Entry(mainFrame, width=25, font=("Arial", 12), justify='center')
    entry_email.place(x=100, y=305)

    entry_password = Entry(mainFrame, show="*", width=25, font=("Arial", 12), justify='center')
    entry_password.place(x=100, y=410)

    def iniciar_sesion():
        correo = entry_email.get().strip()
        password = entry_password.get().strip()

        if not correo or not password:
            MessageBox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        try:
            ruta_users = os.path.join(my_path, "fakedb", "users.txt")
            with open(ruta_users, "r", encoding="utf-8") as file:
                data = [line.strip().split(",") for line in file if line.strip()]
            for user in data:
                if user[0] == correo and user[1] == password:
                    MessageBox.showinfo("Bienvenido", f"Hola {user[2]}!")
                    with open(os.path.join(my_path, "fakedb", "session.txt"), "w", encoding="utf-8") as f:
                        f.write(correo)
                    mainFrame.destroy()
                    dashboard_w.Dashboard(root, Frame(root))
                    return
            MessageBox.showerror("Error", "Correo o contraseña incorrectos.")
        except Exception as e:
            print("⚠️ Error leyendo archivo de usuarios:", e)
            MessageBox.showerror("Error", f"No se pudo acceder a los datos.\n{e}")

    def ir_a_registro():
        mainFrame.destroy()
        register_w.Register(root, Frame(root))

    def ir_a_recuperar():
        mainFrame.destroy()
        recover_w.Recover(root, Frame(root))

    # Botones
    Button(mainFrame, text="Ingresar", command=iniciar_sesion,
           font=("Arial", 11), bg="#41AADC", fg="white", activebackground="#0d8ddf",
           relief="flat", bd=0, padx=13, pady=3).place(x=105, y=514)

    Button(mainFrame, text="Registrarse", command=lambda: [mainFrame.destroy(), register_user_w.RegisterUserWindow(root, Frame(root))],
           font=("Arial", 11), bg="#41AADC", fg="white", activebackground="#0d8ddf",
           relief="flat", bd=0, padx=13, pady=3).place(x=220, y=514)


    Button(mainFrame, text="¿Olvidaste tu contraseña?", command=ir_a_recuperar,
           font=("Arial", 11, "underline"), fg="white", bg="#41AADC", relief="flat", activebackground="#0d8ddf", bd=0, padx=13, pady=3).place(x=115, y=575)