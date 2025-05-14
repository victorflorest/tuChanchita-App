from tkinter import *
import webbrowser
import windows_app.dashboard_window as dashboard_w

# Lista de recomendaciones con título y enlace
videos = [
    ("Educación Financiera para Principiantes", "https://www.youtube.com/watch?v=9sCVcWD1Svs"),
    ("Cosas que puedes hacer para mejorar tus Finanzas", "https://www.youtube.com/watch?v=VCEE58Oy7ig"),
    ("La Manera Más Fácil para Entender las Finanzas", "https://www.youtube.com/watch?v=dUiZ5is-Chw"),
]

def open_video(url):
    webbrowser.open(url)

def Recommendations(root, mainFrame):
    root.title("Recomendaciones Financieras")
    mainFrame.destroy()
    mainFrame = Frame(root, width=425, height=700)
    mainFrame.pack()

    Label(mainFrame, text="Recomendaciones Financieras", font=("Arial", 14)).place(x=60, y=40)

    y_offset = 120
    for title, link in videos:
        Label(mainFrame, text=title, wraplength=250, justify="left").place(x=30, y=y_offset)
        Button(mainFrame, text="Ver video", command=lambda l=link: open_video(l)).place(x=300, y=y_offset)
        y_offset += 50

    Button(mainFrame, text="Volver al Dashboard", command=lambda: dashboard_w.Dashboard(root, mainFrame)).place(x=140, y=620)
