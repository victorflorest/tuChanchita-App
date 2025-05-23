from tkinter import *
from PIL import Image, ImageTk
import helpers.readfiles as rfiles
import os
from datetime import datetime

def NewPaymenMethod(root, mainFrame):
    root.title("Nuevo método de pago")
    mainFrame.destroy()
    mainFrame = Frame()
    mainFrame.config(width=425, height=700)
    mainFrame.pack()
    my_path = rfiles.Route()

    # Fondo
    try:
        bg_path = os.path.join(my_path, "images", "FONDO_PROTO.jpg")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Mantén la referencia para evitar recolección de basura
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        # Fallback a gradiente si falla la imagen
        canvas = Canvas(mainFrame, width=425, height=700, bg="#4B0082", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(200, 400, 600, 800, fill="#6A0DAD", outline="")

    # Etiquetas e Entradas
    labels = [
        "Nombre del propietario",
        "Tipo de tarjeta",
        "Red de tarjeta",
        "Número de tarjeta",
        "Fecha de expiración"
    ]
    entries = []

    for i, label_text in enumerate(labels):
        # Centrar las etiquetas con fondo #3B82F6
        label = Label(mainFrame, text=label_text, font=("Arial", 12), fg="white", bg="#3B82F6")
        label.place(relx=0.5, y=100 + i * 80, anchor="center")

        # Configuración especial para "Tipo de tarjeta"
        if label_text == "Tipo de tarjeta":
            options = ["Débito", "Crédito"]
            var = StringVar(mainFrame)
            var.set(options[0])  # Opción por defecto
            entry = OptionMenu(mainFrame, var, *options)
            entry.config(width=27, font=("Arial", 12), anchor="center", bg="#1E3A8A", fg="white", 
                         highlightthickness=0, bd=0)  # Fondo azul oscuro
            entry.place(relx=0.5, y=130 + i * 80, anchor="center")
            entries.append(var)  # Guardamos la variable StringVar
        # Configuración especial para "Número de tarjeta"
        elif label_text == "Número de tarjeta":
            entry = Entry(mainFrame, width=30, fg="white", font=("Arial", 12), justify="center", show="*",
                          bg="#1E3A8A", highlightthickness=0, bd=0)  # Fondo azul oscuro
            entry.place(relx=0.5, y=130 + i * 80, anchor="center")
            entries.append(entry)
        # Configuración para "Fecha de expiración"
        elif label_text == "Fecha de expiración":
            entry = Entry(mainFrame, width=30, fg="white", font=("Arial", 12), justify="center",
                          bg="#1E3A8A", highlightthickness=0, bd=0)  # Fondo azul oscuro
            entry.place(relx=0.5, y=130 + i * 80, anchor="center")
            entries.append(entry)
        else:
            entry = Entry(mainFrame, width=30, fg="white", font=("Arial", 12), justify="center",
                          bg="#1E3A8A", highlightthickness=0, bd=0)  # Fondo azul oscuro
            entry.place(relx=0.5, y=130 + i * 80, anchor="center")
            entries.append(entry)

    def guardar():
        print("Botón Guardar presionado")
        # Obtener los valores (para StringVar usamos .get(), para Entry también)
        data = [entry.get().strip() if isinstance(entry, Entry) else entry.get() for entry in entries]
        if not all(data):
            from tkinter import messagebox
            messagebox.showwarning("Campos incompletos", "Completa todos los campos correctamente.")
            return

        # Validación adicional para la fecha de expiración (DD/MM/AAAA)
        expiry_date = entries[4].get().strip()
        if not (len(expiry_date) == 10 and expiry_date[2] == "/" and expiry_date[5] == "/" and
                expiry_date[:2].isdigit() and expiry_date[3:5].isdigit() and expiry_date[6:].isdigit()):
            from tkinter import messagebox
            messagebox.showwarning("Formato inválido", "La fecha de expiración debe tener el formato DD/MM/AAAA.")
            return

        # Convertir a enteros para validación
        day, month, year = map(int, expiry_date.split("/"))
        if not (1 <= day <= 31 and 1 <= month <= 12 and 2000 <= year <= 2100):
            from tkinter import messagebox
            messagebox.showwarning("Fecha inválida", "Día (01-31), mes (01-12) y año (2000-2100) inválidos.")
            return

        # Verificar si la fecha no está expirada (basado en la fecha actual: 19/05/2025, 12:32 PM -05)
        current_date = datetime(2025, 5, 19)
        input_date = datetime(year, month, day)
        if input_date < current_date:
            from tkinter import messagebox
            messagebox.showwarning("Fecha expirada", "La tarjeta está expirada.")
            return

        try:
            with open(os.path.join(my_path, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
                correo = f.read().strip()
            linea = ",".join([correo] + data)
            with open(os.path.join(my_path, "fakedb", "payments.txt"), "a", encoding="utf-8") as f:
                f.write(linea + "\n")
            from tkinter import messagebox
            messagebox.showinfo("Éxito", "Método de pago guardado.")
            mainFrame.destroy()
            from importlib import import_module
            profile_w = import_module("windows_app.profile_window")
            profile_w.Profile(root, Frame(root))
        except Exception as e:
            print("Error guardando método de pago:", e)
            from tkinter import messagebox
            messagebox.showerror("Error", "No se pudo guardar el método.")

    def cancelar():
        mainFrame.destroy()
        from importlib import import_module
        profile_w = import_module("windows_app.profile_window")
        profile_w.Profile(root, Frame(root))

    # Botones
    Button(mainFrame, text="Cancelar", command=cancelar, font=("Arial", 12), bg="#41AADC", fg="white",
           activebackground="#0d8ddf", relief="flat", bd=0, padx=20, pady=5).place(x=110, y=580)
    Button(mainFrame, text="Guardar", command=guardar, font=("Arial", 12), bg="#41AADC", fg="white",
           activebackground="#0d8ddf", relief="flat", bd=0, padx=20, pady=5).place(x=230, y=580)