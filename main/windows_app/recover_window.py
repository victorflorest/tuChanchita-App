from tkinter import *
from tkinter import messagebox as MessageBox
import helpers.readfiles as readfiles
import helpers.email_sender as mailer
import random, string, os
import windows_app.verify_token_window as verify_token_w
import windows_app.login_window as login_w
from PIL import Image, ImageTk

def Recover(root, mainFrame):
    root.title("Recuperación de contraseña")
    mainFrame.config(width=425, height=700)
    mainFrame.pack()

    # Cargar fondo igual que en las otras ventanas
    my_path = readfiles.Route()
    try:
        bg_path = os.path.join(my_path, "images", "background-recover.png")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Evita que la imagen sea recolectada por el garbage collector
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        mainFrame.config(bg="white")  # Fallback en caso de error

    # Contenido de la ventana
    entry_email = Entry(mainFrame, width=35)
    entry_email.place(x=110, y=370)

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

    Button(mainFrame, text="Enviar código", command=enviar_codigo,
           font=("Arial", 11, "underline"), fg="white", bg="#41AADC", relief="flat", activebackground="#0d8ddf", bd=0, padx=19, pady=3).place(x=150, y=425)

    Button(mainFrame, text="Volver", command=lambda: [mainFrame.destroy(), login_w.Login(root, Frame(root))], font=("Arial", 11), bg="#41AADC", fg="white", activebackground="#0d8ddf",
           relief="flat", bd=0, padx=27, pady=3).place(x=166, y=486)
