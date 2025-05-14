
from tkinter import *
import helpers.readfiles as rfiles
import os

def NewPaymenMethod(root, mainFrame):
    root.title("Nuevo método de pago")
    mainFrame.destroy()
    mainFrame = Frame()
    mainFrame.config(width=425, height=700, bg="white")
    mainFrame.pack()
    my_path = rfiles.Route()

    Label(mainFrame, text="Agregar nuevo método de pago", font=("Arial", 14), bg="white").place(x=70, y=60)


    Label(mainFrame, text="Tipo (1:Visa, 2:Mastercard, 3:Paypal):", bg="white").place(x=70, y=190)
    entry_tipo = Entry(mainFrame, width=30)
    entry_tipo.place(x=70, y=215)

    Label(mainFrame, text="Entidad bancaria:", bg="white").place(x=70, y=250)
    entry_banco = Entry(mainFrame, width=30)
    entry_banco.place(x=70, y=275)

    Label(mainFrame, text="Últimos 4 dígitos:", bg="white").place(x=70, y=310)
    entry_ultimos = Entry(mainFrame, width=30)
    entry_ultimos.place(x=70, y=335)

    Label(mainFrame, text="Mes de vencimiento:", bg="white").place(x=70, y=370)
    entry_mes = Entry(mainFrame, width=30)
    entry_mes.place(x=70, y=395)

    Label(mainFrame, text="Año de vencimiento:", bg="white").place(x=70, y=430)
    entry_anio = Entry(mainFrame, width=30)
    entry_anio.place(x=70, y=455)

    def guardar():
        print("Boton Guardar presionado")
        tipo = entry_tipo.get().strip()
        banco = entry_banco.get().strip()
        ultimos = entry_ultimos.get().strip()
        mes = entry_mes.get().strip()
        anio = entry_anio.get().strip()

        if not all([tipo, banco, ultimos, mes, anio]):
            from tkinter import messagebox
            messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
            return

        try:
            with open(os.path.join(my_path,"fakedb", "session.txt"), "r", encoding="utf-8") as f:
                correo = f.read().strip()

            linea = ",".join([correo, tipo, banco, ultimos, mes, anio])
            with open(os.path.join(my_path,"fakedb", "payments.txt"), "a", encoding="utf-8") as f:
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

    Button(mainFrame, text="Guardar", command=guardar).place(x=180, y=510)
