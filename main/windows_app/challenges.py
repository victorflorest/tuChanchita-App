from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import helpers.readfiles as readfiles
from .saving_money import saving_money
from .no_spending import no_spending
from .limit_spending import limit_spending


def Challenges(root, mainFrame):
    root.title("Retos financieros")
    mainFrame.destroy()
    mainFrame = Frame(root, width=425, height=700)
    mainFrame.pack()

    # Cargar fondo como en Login
    try:
        my_path = readfiles.Route()
        bg_path = os.path.join(my_path, "images", "background.jpg")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Guardar referencia para evitar que se borre
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo en Challenges:", e)
        mainFrame.config(bg="#1e1f6e")  # Color de respaldo

    # Título
    Label(mainFrame, text="Retos para mejorar\nhábitos financieros", fg="white", bg="#1e1f6e",
          font=("Helvetica", 14, "bold")).place(x=80, y=30)

    # Lista de retos
    retos = [
        ("Desafío del ahorro", "Ahorra una cantidad cada semana"),
        ("Sin gastos superfluos", "Evita compras no deseadas"),
        ("Reto de no gastar", "Limítate con los gastos")
    ]

    y_pos = 100
    for i, (titulo, descripcion) in enumerate(retos):
        reto_frame = Frame(mainFrame, bg="#635bff", width=350, height=80)
        reto_frame.place(x=40, y=y_pos)

        Label(reto_frame, text=titulo, fg="white", bg="#635bff",
              font=("Helvetica", 11, "bold")).place(x=10, y=10)

        Label(reto_frame, text=descripcion, fg="white", bg="#635bff",
              font=("Helvetica", 9)).place(x=10, y=35)

        Button(reto_frame, text="Empezar", bg="#e6e6e6", font=("Helvetica", 9),
               command=[saving_money, no_spending, limit_spending][i]).place(x=260, y=25)

        y_pos += 100

    # Botón de volver
    Button(mainFrame, text="Volver", bg="#48aaff", fg="white", font=("Helvetica", 11, "bold"),
           command=lambda: import_dashboard(root, mainFrame)).place(x=160, y=600)


def import_dashboard(root, mainFrame):
    from windows_app.dashboard_window import Dashboard
    Dashboard(root, mainFrame)
