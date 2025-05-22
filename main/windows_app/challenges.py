from tkinter import *
from tkinter import messagebox
from .saving_money import saving_money
from .no_spending import no_spending
from .limit_spending import limit_spending


def Challenges(root, mainFrame):
    root.title("Retos financieros")
    mainFrame.destroy()
    mainFrame = Frame(root, width=425, height=670, bg="#1e1f6e")
    mainFrame.pack()

    Label(mainFrame, text="Retos para mejorar\nhábitos financieros", fg="white", bg="#1e1f6e",
          font=("Helvetica", 14, "bold")).place(x=80, y=30)

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

        if i == 0:
            Button(reto_frame, text="Empezar", bg="#e6e6e6", font=("Helvetica", 9),
                command=saving_money).place(x=260, y=25)
        elif i == 1:
            Button(reto_frame, text="Empezar", bg="#e6e6e6", font=("Helvetica", 9),
                command=no_spending).place(x=260, y=25)
        else:
            Button(reto_frame, text="Empezar", bg="#e6e6e6", font=("Helvetica", 9),
                command=limit_spending).place(x=260, y=25)

        y_pos += 100

    Button(mainFrame, text="Volver", bg="#48aaff", fg="white", font=("Helvetica", 11, "bold"),
           command=lambda: import_dashboard(root, mainFrame)).place(x=160, y=600)


def import_dashboard(root, mainFrame):
    from windows_app.dashboard_window import Dashboard
    Dashboard(root, mainFrame)
