from tkinter import *
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import windows_app.profile_window as profile_w
import helpers.readfiles as readfiles
from datetime import date
import os

def SetLimit(root, mainFrame):
    # Fondo de la ventana
    try:
        my_path = readfiles.Route()
        ruta_fondo = os.path.join(my_path, "images", "FONDO_PROTO.jpg")  # Cambiado a FONDO_PROTO.jpg
        imagen_fondo = Image.open(ruta_fondo).resize((425, 700))
        foto_fondo = ImageTk.PhotoImage(imagen_fondo)
        fondo_label = Label(mainFrame, image=foto_fondo)
        fondo_label.image = foto_fondo  # Evitar que se libere de memoria
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        # Fallback a gradiente
        canvas = Canvas(mainFrame, width=425, height=700, bg="#4B0082", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(200, 400, 600, 800, fill="#6A0DAD", outline="")

    monto = limitEntry.get().strip()

    if not monto:
        MessageBox.showwarning("Campo vacío", "Por favor, ingresa un monto.")
        return

    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo = f.read().strip()

        año = date.today().year
        mes = date.today().month
        nueva_linea = f"{correo},{monto},{mes},{año}\n"

        # Leer todos los límites anteriores
        path_limit = os.path.join(ruta, "fakedb", "limit.txt")
        if os.path.exists(path_limit):
            with open(path_limit, "r", encoding="utf-8") as f:
                lineas = f.readlines()
            # Eliminar el límite anterior del mismo usuario, mes y año
            lineas = [l for l in lineas if not (l.startswith(f"{correo},") and f",{mes},{año}" in l)]
        else:
            lineas = []

        # Escribir los nuevos límites
        with open(path_limit, "w", encoding="utf-8") as f:
            f.writelines(lineas)
            f.write(nueva_linea)

        MessageBox.showinfo("Límite actualizado", "Tu límite mensual fue guardado correctamente.")

        # Limpiar frame anterior para evitar superposición
        for widget in mainFrame.winfo_children():
            widget.destroy()
        mainFrame.destroy()

        profile_w.Profile(root, Frame(root))

    except Exception as e:
        print("❌ Error al guardar el límite:", e)
        MessageBox.showerror("Error", "Ocurrió un error al guardar el límite.")

def Limit(root, mainFrame):
    monthDic = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo",
        6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre",
        10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    root.title("Límite")
    global limitEntry
    limitEntry = StringVar()
    mainFrame.destroy()
    mainFrame = Frame(root)  # Especificar que el Frame pertenece a root
    mainFrame.config(width=425, height=700)
    mainFrame.pack()

    # Fondo
    try:
        my_path = readfiles.Route()
        ruta_fondo = os.path.join(my_path, "images", "FONDO_PROTO.jpg")  # Cambiado a FONDO_PROTO.jpg
        imagen_fondo = Image.open(ruta_fondo).resize((425, 700))
        foto_fondo = ImageTk.PhotoImage(imagen_fondo)
        mainFrame.foto_fondo = foto_fondo  # Mantén la referencia
        Label(mainFrame, image=foto_fondo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        # Fallback a gradiente
        canvas = Canvas(mainFrame, width=425, height=700, bg="#4B0082", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(200, 400, 600, 800, fill="#6A0DAD", outline="")

    # Frame para el título
    title_frame = Frame(mainFrame, bg="#3B82F6", padx=20, pady=10)
    title_frame.place(relx=0.5, rely=0.25, anchor="center")
    Label(title_frame, text="Establece tu límite mensual", font=("Arial", 14, "bold"), fg="white", bg="#3B82F6").pack()

    # Frame para el mes
    month_frame = Frame(mainFrame, bg="#3B82F6", padx=15, pady=8)
    month_frame.place(relx=0.5, rely=0.375, anchor="center")
    Label(month_frame, text="Mes: " + monthDic[date.today().month], font=("Arial", 12), fg="white", bg="#3B82F6").pack()

    # Frame para el monto
    amount_frame = Frame(mainFrame, bg="#3B82F6", padx=15, pady=8)
    amount_frame.place(relx=0.5, rely=0.5, anchor="center")
    Label(amount_frame, text="Ingresa tu monto límite:", font=("Arial", 12), fg="white", bg="#3B82F6").pack()

    # Frame para la entrada
    entry_frame = Frame(mainFrame, bg="#1E3A8A", padx=10, pady=5)
    entry_frame.place(relx=0.5, rely=0.575, anchor="center")
    Entry(entry_frame, width=20, textvariable=limitEntry, fg="white", font=("Arial", 12), justify="center", bg="#1E3A8A", highlightthickness=0, bd=0).pack()

    # Botones
    Button(mainFrame, text="Volver", font=("Arial", 12), bg="#41AADC", fg="white", activebackground="#0d8ddf", relief="flat", bd=0, padx=20, pady=10, command=lambda: volver_a_perfil(root, mainFrame)).place(relx=0.3, y=500, anchor="center")
    Button(mainFrame, text="Guardar", font=("Arial", 12), bg="#41AADC", fg="white", activebackground="#0d8ddf", relief="flat", bd=0, padx=20, pady=10, command=lambda: SetLimit(root, mainFrame)).place(relx=0.7, y=500, anchor="center")

def volver_a_perfil(root, mainFrame):
    for widget in mainFrame.winfo_children():
        widget.destroy()
    mainFrame.destroy()
    profile_w.Profile(root, Frame(root))