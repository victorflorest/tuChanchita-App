from tkinter import *
from tkinter import messagebox as MessageBox
import windows_app.profile_window as profile_w
import helpers.readfiles as readfiles
from datetime import date
import os

def SetLimit(root, mainFrame):
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

        # 🔥 SOLUCIÓN: Limpiar frame anterior para evitar superposición
        for widget in mainFrame.winfo_children():
            widget.destroy()
        mainFrame.destroy()

        profile_w.Profile(root, Frame(root))

    except Exception as e:
        print("❌ Error al guardar el límite:", e)
        MessageBox.showerror("Error", "Ocurrió un error al guardar el límite.")

#* Estructura de la ventana donde se asigna el límite mensual.
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
    mainFrame = Frame()
    mainFrame.config(width=425, height=700)
    mainFrame.pack()

    Label(mainFrame, text="Establece tu límite mensual").place(x=140, y=70)
    Label(mainFrame, text="Mes: " + monthDic[date.today().month]).place(x=180, y=110)
    Label(mainFrame, text="Ingresa tu monto límite: ").place(x=65, y=150)
    Entry(mainFrame, width=25, borderwidth=2, textvariable=limitEntry).place(x=220, y=150)

    Button(mainFrame, text="Guardar", width=10, command=lambda: SetLimit(root, mainFrame)).place(x=170, y=220)
    Button(mainFrame, text="Volver", width=10, command=lambda: volver_a_perfil(root, mainFrame)).place(x=170, y=280)

def volver_a_perfil(root, mainFrame):
    for widget in mainFrame.winfo_children():
        widget.destroy()
    mainFrame.destroy()
    profile_w.Profile(root, Frame(root))
