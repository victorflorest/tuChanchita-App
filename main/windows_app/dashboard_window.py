from tkinter import *
import windows_app.register_window as register_w
import windows_app.reports_window as reports_w
import windows_app.profile_window as profile_w
import helpers.readfiles as readfiles
import os
from datetime import date
from tkinter import Label
import os
from datetime import date
import helpers.readfiles as readfiles

import windows_app.recommendations_window as rec_w  

def abrir_chatbot(root, mainFrame):
    try:
        from chatbot_model import chatbot_window as chatbot_w
        chatbot_w.Chatbot(root, mainFrame)
    except Exception as e:
        print("❌ Error al abrir el chatbot:", e)

#* Función que crea la lista de los últimos 5 registros.
def CreateDashList():
    registros = readfiles.GetRegisterFile()
    if not registros:
        return []
    
    for i in range(len(registros)):
        registros[i][6] = registros[i][6].strip()  # columna tienda
    
    return registros[-10:]



#* Función que calcula y devuelve el total registrado del mes.
def TotalMonthSpent():
    try:
        registers_ = readfiles.GetRegisterFile()
        with open(os.path.join(readfiles.Route(), "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo = f.read().strip()

        amount = 0.0
        for r in registers_:
            if len(r) >= 7 and r[0] == correo and int(r[5]) == date.today().month:
                amount += float(r[1])
        return amount
    except Exception as e:
        print("❌ Error en TotalMonthSpent:", e)
        return 0.0


#* Función que lee el límite para mostrarlo luego.
def TakeLimit():
    limits = readfiles.GetLimitFile()
    try:
        with open(readfiles.Route() + r"\fakedb\session.txt", "r", encoding="utf-8") as f:
            correo_actual = f.read().strip()

        for line in limits:
            if line[0] == correo_actual and int(line[2]) == date.today().month and int(line[3]) == date.today().year:
                return line[1]  # el monto límite como string

        return "No establecido"

    except Exception as e:
        print("Error al tomar el límite:", e)
        return "Error"


#* Estructura de la ventana del Dashboard general.
def Dashboard(root, mainFrame):
    root.title("Dashboard")
    mainFrame.destroy()
    mainFrame = Frame(root)
    mainFrame.config(width = "425", height = "670")
    mainFrame.pack()
    
    amount = TotalMonthSpent()
    shownRegisters = CreateDashList()
    finalLimit = TakeLimit()
    Label(mainFrame, text = "Límite establecido:  " + finalLimit).place(x = 140, y = 50)

    # Obtener correo
    ruta = readfiles.Route()
    with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
        correo = f.read().strip()

    # Obtener límites y monto
    limites = readfiles.GetLimitFile()
    limite = None
    for l in limites:
        if l[0] == correo and int(l[2]) == date.today().month and int(l[3]) == date.today().year:
            limite = float(l[1])
            break

    color = "black"
    if limite is not None and amount > limite:
        color = "red"

    Label(mainFrame, text=f"Usted está gastando en el mes: S/.{amount:.2f}", fg=color).place(x=110, y=100)

    Label(mainFrame, text = "Últimos 10 gastos registrados: ").place(x = 50, y = 160)

    Label(mainFrame, text = "Fecha").place(x = 50, y = 200)
    Label(mainFrame, text = "Tienda").place(x = 200, y = 200)
    Label(mainFrame, text = "Monto").place(x = 340, y = 200)

    positiony = 230
    for i in range(len(shownRegisters)-1, -1, -1):
        if len(shownRegisters[i]) >= 6:
            Label(mainFrame, text=shownRegisters[i][4], bg="white").place(x=50, y=positiony)
            Label(mainFrame, text=shownRegisters[i][6], bg="white").place(x=200, y=positiony)
            Label(mainFrame, text="S/." + shownRegisters[i][1], bg="white").place(x=340, y=positiony)
            positiony += 30



    Button(mainFrame, text="Registro", width=10, command=lambda: register_w.Register(root, mainFrame)).place(x=40, y=580)
    Button(mainFrame, text="Reportes", width=10, command=lambda: reports_w.Reports(root, mainFrame)).place(x=160, y=580)
    Button(mainFrame, text="Perfil", width=10, command=lambda: profile_w.Profile(root, mainFrame)).place(x=280, y=580)
    Button(mainFrame, text="Chatbot", width=10, command=lambda: abrir_chatbot(root, mainFrame)).place(x=40, y=630)
    Button(mainFrame, text="Recomendaciones", width=14, command=lambda: rec_w.Recommendations(root, mainFrame)).place(x=140, y=630)
    Button(mainFrame, text="Salir", width=10, command=root.destroy).place(x=280, y=630)