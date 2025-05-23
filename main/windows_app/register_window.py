from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from tkcalendar import *
from PIL import Image, ImageTk
import windows_app.dashboard_window as dashboard_w
import helpers.readfiles as readfiles
import os
from datetime import date

#* Función para crear la lista de los nombres de los tipos de pago creados.
def GetPaymets():
    paymentsFile = readfiles.GetPaymentsFile()
    payments = []
    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo_actual = f.read().strip()
        for p in paymentsFile:
            if p[0] == correo_actual:
                banco = p[2]
                ultimos = p[3]
                payments.append(f"{banco} ****{ultimos}")
    except:
        pass
    return payments

#* Función para calcular el total gastado por usuario en el mes.
def TotalMonthSpent():
    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo = f.read().strip()
        registros = readfiles.GetRegisterFile()
        monto = 0.0
        for r in registros:
            if len(r) >= 7 and r[0] == correo and int(r[5]) == date.today().month:
                monto += float(r[1])
        return monto
    except:
        return 0.0

#* Verifica si el nuevo gasto supera el límite mensual
def VerifyLimit(amount, monthR, yearR):
    limits = readfiles.GetLimitFile()
    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo_actual = f.read().strip()

        for line in limits:
            if line[0] == correo_actual and int(line[2]) == monthR and int(line[3]) == yearR:
                limite = float(line[1])
                gastado = TotalMonthSpent()
                return (gastado + amount) <= limite

        return True
    except Exception as e:
        print("Error en VerifyLimit:", e)
        return True

#* Guarda el registro
def GetRegisters(root, mainFrame):
    amount = amountEntry.get()
    category = categoriesDropBox.get()
    payment = paymentsDropBox.get()
    date_ = varDateEntry.get_date()
    month = date_.month
    store = storeEntry.get()

    my_path = readfiles.Route()

    try:
        with open(os.path.join(my_path, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo = f.read().strip()
    except Exception as e:
        print("Error leyendo session.txt:", e)
        MessageBox.showerror("Error", "No se pudo identificar al usuario actual.")
        return

    limitVerified = VerifyLimit(float(amount), month, date_.year)

    registro = ",".join([
        correo,
        str(amount),
        category,
        payment,
        str(date_),
        str(month),
        store
    ])

    try:
        with open(os.path.join(my_path, "fakedb", "registers.txt"), "a", encoding="utf-8") as file:
            file.write(registro + "\n")

        if not limitVerified:
            MessageBox.showwarning("Advertencia", f"El gasto (S/.{amount}) excede el límite mensual.")

        mainFrame.destroy()
        dashboard_w.Dashboard(root, Frame(root))

    except Exception as e:
        print("❌ Error guardando registro:", e)
        MessageBox.showerror("Error", "No se pudo guardar el gasto.")

#* Estructura ventana de registro
def Register(root, mainFrame):
    root.title("Registro")
    global amountEntry
    amountEntry = StringVar()

    mainFrame.destroy()
    mainFrame = Frame()
    mainFrame.config(width=425, height=700)
    mainFrame.pack()

    # Fondo de la ventana
    try:
        ruta_fondo = os.path.join(readfiles.Route(), "images", "FONDO_PROTO.jpg")
        imagen_fondo = Image.open(ruta_fondo).resize((425, 700))
        foto_fondo = ImageTk.PhotoImage(imagen_fondo)
        fondo_label = Label(mainFrame, image=foto_fondo)
        fondo_label.image = foto_fondo  # Evitar que se libere de memoria
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)

    Label(mainFrame, text="Ingrese el monto gastado").place(x=150, y=50)
    Entry(mainFrame, width=25, borderwidth=2, textvariable=amountEntry).place(x=145, y=75)

    categoriesNames = ["Entretenimiento", "Comida", "Educación", "Ropa", "Otros"]
    Label(mainFrame, text="Seleccione la categoría correspondiente").place(x=110, y=120)
    global categoriesDropBox
    categoriesDropBox = ttk.Combobox(mainFrame)
    categoriesDropBox.set("Selecciona una opción")
    categoriesDropBox["values"] = categoriesNames
    categoriesDropBox.place(x=145, y=145)

    paymentsNames = GetPaymets()
    Label(mainFrame, text="Seleccione el modo de pago empleado").place(x=110, y=190)
    global paymentsDropBox
    paymentsDropBox = ttk.Combobox(mainFrame)
    paymentsDropBox.set("Selecciona una opción")
    paymentsDropBox["values"] = paymentsNames
    paymentsDropBox.place(x=145, y=215)

    Label(mainFrame, text="Ingrese la fecha de la compra").place(x=110, y=260)
    global varDateEntry
    varDateEntry = DateEntry(mainFrame, selectmode="day")
    varDateEntry.place(x=145, y=285)

    Label(mainFrame, text="Ingrese el nombre de la tienda o servicio").place(x=110, y=330)
    global storeEntry
    storeEntry = StringVar()
    Entry(mainFrame, width=25, borderwidth=2, textvariable=storeEntry).place(x=145, y=355)

    Button(mainFrame, text="Guardar", width=10, command=lambda: GetRegisters(root, mainFrame)).place(x=80, y=450)
    Button(mainFrame, text="Cancelar", width=10, command=lambda: [mainFrame.destroy(), dashboard_w.Dashboard(root, Frame(root))]).place(x=250, y=450)
