from tkinter import *
import webbrowser
from PIL import Image, ImageTk
import os
import helpers.readfiles as readfiles
import windows_app.dashboard_window as dashboard_w

# Lista de recomendaciones con título y enlace
videos = [
    ("https://youtu.be/nmqjz8vZOIY?si=TTHUzkLwsox4l97G"),
    ("https://youtu.be/Vg4CL6GmvrU?si=MBbpi5tOLTOjWz5u"),
    ("https://youtu.be/9sCVcWD1Svs?si=kaxREXNziW74SWrL"),
]

def open_video(url):
    webbrowser.open(url)

def Recommendations(root, mainFrame):
    root.title("Recomendaciones Financieras")
    mainFrame.destroy()
    mainFrame = Frame(root, width=425, height=700)
    mainFrame.pack()

    # Fondo como en el login
    try:
        my_path = readfiles.Route()
        bg_path = os.path.join(my_path, "images", "background-recommendations.png")
        bg_image = Image.open(bg_path).resize((425, 700))
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Referencia para evitar que se borre
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo en Recommendations:", e)
        mainFrame.config(bg="blue")


    # Videos
    y_offset = 210
    for link in videos:
        Button(mainFrame, text="Ver video", command=lambda l=link: open_video(l), 
           font=("Arial", 11, "underline"), fg="white", bg="#41AADC", 
           relief="flat", activebackground="#0d8ddf", bd=0, padx=31, pady=3).place(x=239, y=y_offset)
        y_offset += 126

    # Botón de volver
    Button(mainFrame, text="Volver",
           command=lambda: dashboard_w.Dashboard(root, mainFrame),
           font=("Arial", 11, "underline"), fg="white", bg="#41AADC", 
           relief="flat", activebackground="#0d8ddf", bd=0, padx=40, pady=3).place(x=147, y=619)
