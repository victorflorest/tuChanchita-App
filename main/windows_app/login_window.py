from tkinter import *
from tkinter import messagebox as MessageBox
import windows_app.dashboard_window as dashboard_w
import windows_app.register_window as register_w
import windows_app.recover_window as recover_w
import windows_app.register_user_window as register_user_w
import helpers.readfiles as readfiles
from PIL import Image, ImageTk
import os

def Login(root, mainFrame):
    root.title("Inicio de sesión")
    mainFrame.config(width=425, height=700, bg="white")
    mainFrame.pack()
    my_path = readfiles.Route()

    try:
        logo_path = os.path.join(my_path, "images", "Logo.png")
        print("📷 Logo en:", logo_path)
        logo_img = Image.open(logo_path).resize((120, 120))
        logo = ImageTk.PhotoImage(logo_img)
        mainFrame.logo = logo  # evitar que desaparezca la imagen
        Label(mainFrame, image=logo, bg="white").place(relx=0.32, rely=0.1)
    except Exception as e:
        print("⚠️ Error cargando logo:", e)
        Label(mainFrame, text="TuChanchita", font=("Arial", 18)).place(relx=0.35, rely=0.1)

    Label(mainFrame, text="Correo electrónico:", bg="white").place(x=70, y=260)
    entry_email = Entry(mainFrame, width=30)
    entry_email.place(x=70, y=285)

    Label(mainFrame, text="Contraseña:", bg="white").place(x=70, y=320)
    entry_password = Entry(mainFrame, show="*", width=30)
    entry_password.place(x=70, y=345)

    def iniciar_sesion():
        correo = entry_email.get().strip()
        password = entry_password.get().strip()

        if not correo or not password:
            MessageBox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        try:
            ruta_users = os.path.join(my_path, "fakedb", "users.txt")
            print("📄 Leyendo usuarios desde:", ruta_users)

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
            MessageBox.showerror("Error", f"No se pudo acceder a los datos.\\n{e}")

    def ir_a_registro():
        mainFrame.destroy()
        register_w.Register(root, Frame(root))

    def ir_a_recuperar():
        mainFrame.destroy()
        recover_w.Recover(root, Frame(root))

    Button(mainFrame, text="Iniciar sesión", command=iniciar_sesion).place(x=150, y=400)
    Button(mainFrame, text="Registrarse", command=lambda: [mainFrame.destroy(), register_user_w.RegisterUserWindow(root, Frame(root))]).place(x=150, y=440)
    Button(mainFrame, text="¿Olvidaste tu contraseña?", command=ir_a_recuperar, fg="blue", bg="white", bd=0).place(x=120, y=480)
