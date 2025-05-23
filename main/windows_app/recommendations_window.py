from tkinter import *
import webbrowser
from PIL import Image, ImageTk
import os
import windows_app.dashboard_window as dashboard_w

# Lista de recomendaciones con título, enlace y thumbnail path
videos = [
    ("Haz Esto a Tus 18", "https://www.youtube.com/watch?v=9sCVcWD1Svs", "images/Imagen3_recomendaciones.png"),
    ("5 Tips Sencillos", "https://www.youtube.com/watch?v=VCEE58Oy7ig", "images/Imagen2_recomendaciones.png"),
    ("Empieza Por Aquí", "https://www.youtube.com/watch?v=dUiZ5is-Chw", "images/Imagen1_recomendaciones.png"),
]

def open_video(url):
    webbrowser.open(url)

def Recommendations(root, mainFrame):
    root.title("Recomendaciones Financieras")
    mainFrame.destroy()
    mainFrame = Frame(root, width=425, height=700)
    mainFrame.pack()

    # Fondo de la ventana con FONDO_PROTO.jpg
    try:
        my_path = os.path.dirname(os.path.abspath(__file__))
        # Adjust path to go up one directory to access the images folder at the root
        ruta_fondo = os.path.join(my_path, "..", "images", "FONDO_PROTO.jpg")
        print(f"Attempting to load background image from: {ruta_fondo}")  # Debugging line
        if not os.path.exists(ruta_fondo):
            raise FileNotFoundError(f"Background image not found at {ruta_fondo}")
        imagen_fondo = Image.open(ruta_fondo).resize((425, 700), Image.Resampling.LANCZOS)
        foto_fondo = ImageTk.PhotoImage(imagen_fondo)
        fondo_label = Label(mainFrame, image=foto_fondo)
        fondo_label.image = foto_fondo  # Keep a reference to avoid garbage collection
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        # Fallback to a colored background if the image fails to load
        mainFrame.config(bg="blue")

    # Title
    Label(mainFrame, text="Recomendaciones", font=("Arial", 16, "bold"), fg="white", bg="#4A00E0").place(relx=0.5, y=40, anchor="center")
    Label(mainFrame, text="Financieras", font=("Arial", 16, "bold"), fg="white", bg="#4A00E0").place(relx=0.5, y=65, anchor="center")

    # Video recommendations
    y_offset = 120
    for title, link, thumbnail_path in videos:
        # Frame for each video card
        card = Frame(mainFrame, bg='white', width=350, height=80)
        card.place(x=37, y=y_offset)

        # Thumbnail
        try:
            # Adjust thumbnail path to go up one directory to the root images folder
            thumbnail_path = os.path.join(my_path, "..", thumbnail_path)
            print(f"Attempting to load thumbnail from: {thumbnail_path}")  # Debugging line
            img = Image.open(thumbnail_path).resize((80, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            thumbnail_label = Label(card, image=photo, bg='white')
            thumbnail_label.image = photo  # Keep a reference
            thumbnail_label.place(x=0, y=0)
        except Exception as e:
            print("⚠️ Error cargando thumbnail:", e)
            thumbnail_label = Label(card, text="No Image", bg='white')
            thumbnail_label.place(x=0, y=0)

        # Title
        Label(card, text=title, wraplength=200, justify="left", font=("Arial", 10), bg='white').place(x=90, y=10)

        # Play Button
        play_btn = Button(card, text="▶", command=lambda l=link: open_video(l), font=("Arial", 12), bg='#1DB954', fg='white', width=2)
        play_btn.place(x=300, y=30)

        y_offset += 100

    # Back Button
    volver_btn = Button(mainFrame, text="Volver", command=lambda: dashboard_w.Dashboard(root, mainFrame), 
                        font=("Arial", 12), bg='#00C4CC', fg='white', width=10)
    volver_btn.place(x=140, y=620)

if __name__ == "__main__":
    root = Tk()
    mainFrame = Frame(root)
    Recommendations(root, mainFrame)
    root.geometry("425x700")
    root.mainloop()