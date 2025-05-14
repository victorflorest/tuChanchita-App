from tkinter import *
import windows_app.dashboard_window as dashboard_w
import windows_app.newPayment_window as payment_w
import windows_app.limit_window as limit_w
import helpers.readfiles as rfiles
from PIL import Image, ImageTk
from tkinter import messagebox as MessageBox
import os

my_path = rfiles.Route()

def get_user_info():
    try:
        with open(my_path + r"\fakedb\session.txt", "r", encoding="utf-8") as f:
            correo_actual = f.read().strip()
        with open(my_path + r"\fakedb\users.txt", "r", encoding="utf-8") as f:
            usuarios = [line.strip().split(",") for line in f if line.strip()]
        for user in usuarios:
            print("🔎 Comparando:", user[0], "vs", correo_actual)
            if user[0] == correo_actual:
                return user

    except Exception as e:
        print("Error cargando datos del usuario:", e)
    return ["", "", "Usuario", "Desconocido"]

def CreateList():
    paymentsList = rfiles.GetPaymentsFile()
    for i in range(len(paymentsList)):
        paymentsList[i][5] = paymentsList[i][5].strip()
    return paymentsList


def Erase(index, root, mainFrame):
    paymentsList = CreateList()
    answer = MessageBox.askyesno(message="¿Desea continuar?")
    if answer:
        del paymentsList[index]
        with open(my_path + r"\fakedb\payments.txt", "w", encoding="utf-8") as file:
            for i in range(len(paymentsList)):
                file.write(",".join(paymentsList[i]) + "\n")
        for widget in mainFrame.winfo_children():
            widget.destroy()
        Profile(root, mainFrame)
    else:
        Profile(root, mainFrame)

def CheckPayments(root, mainFrame):
    numPayments = rfiles.GetPaymentsFile()
    if len(numPayments) >= 5:
        MessageBox.showwarning("Cuidado", "Ha alcanzado la máxima cantidad de metodos de pago")
    else:
        payment_w.NewPaymenMethod(root, mainFrame)

def Profile(root, mainFrame):
    print("Abriendo ventana de perfil...")
    root.title("Perfil")
    mainFrame.destroy()
    mainFrame = Frame()
    mainFrame.config(width=425, height=700, bg="white")
    mainFrame.pack()
    root.update()

    user_info = get_user_info()
    nombre, apellido, correo = user_info[2], user_info[3], user_info[0]

    try:
        def cargar_imagen(nombre_archivo, size):
            ruta = os.path.join(my_path,"images", nombre_archivo)
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"No se encontró: {ruta}")
            return ImageTk.PhotoImage(Image.open(ruta).resize(size))

        global visaLogo, paypalLogo, mastercardLogo, profileLogo
        visaLogo = cargar_imagen("Visa.png", (50, 25))
        paypalLogo = cargar_imagen("Paypal.png", (52, 20))
        mastercardLogo = cargar_imagen("Mastercard.png", (50, 28))
        profileLogo = cargar_imagen("Profile.png", (150, 150))
    except Exception as img_err:
        print("⚠️ Error cargando imágenes del perfil:", img_err)
        MessageBox.showerror("Error", "No se pudieron cargar las imágenes del perfil.")
        return


    Label(mainFrame, text="Perfil").place(x=250, y=50)
    Label(mainFrame, image=profileLogo).place(x=30, y=30)
    Label(mainFrame, text=f"Nombre: {nombre}").place(x=200, y=100)
    Label(mainFrame, text=f"Apellidos: {apellido}").place(x=200, y=130)
    Label(mainFrame, text=f"Correo: {correo}").place(x=200, y=160)
    Label(mainFrame, text="Cuentas asociadas:").place(x=70, y=250)

    imageDic = {"1": visaLogo, "2": mastercardLogo, "3": paypalLogo}
    paymentsList = CreateList()
    positiony = 320

    if not paymentsList:
        Label(mainFrame, text="No hay métodos de pago registrados.").place(x=100, y=320)
    else:
        for i in range(len(paymentsList) - 1, -1, -1):
            try:
                Label(mainFrame, image=imageDic[paymentsList[i][1]]).place(x=50, y=positiony)
                Label(mainFrame, text=paymentsList[i][2], bg="white").place(x=120, y=positiony)
                Label(mainFrame, text="****" + paymentsList[i][3], bg="white").place(x=200, y=positiony)
                Label(mainFrame, text=paymentsList[i][4] + "/" + paymentsList[i][5], bg="white").place(x=260, y=positiony)
                Button(mainFrame, text="Borrar", command=lambda index=i: Erase(int(index), root, mainFrame)).place(x=330, y=positiony)
                positiony += 40
            except Exception as loop_err:
                print(f"Error mostrando tarjeta #{i}: {loop_err}")

    Button(mainFrame, text="Agregar nuevo método de pago", command=lambda: CheckPayments(root, mainFrame)).place(x=110, y=530)
    Button(mainFrame, text="Agregar monto límite", command=lambda: limit_w.Limit(root, mainFrame)).place(x=140, y=580)
    Button(mainFrame, text="Volver", command=lambda: dashboard_w.Dashboard(root, mainFrame)).place(x=180, y=630)
