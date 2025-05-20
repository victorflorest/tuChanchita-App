from tkinter import *
from PIL import Image, ImageTk  # Para manejar imágenes JPG
import json, pickle, numpy as np, random
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import helpers.readfiles as readfiles
from datetime import date
import nltk
import os

nltk.download('punkt')
lemmatizer = WordNetLemmatizer()

model = load_model(os.path.join("main", "chatbot_model", "models", "chat_model.h5"))
intents = json.loads(open(os.path.join("main", "chatbot_model", "data", "intents.json"), encoding="utf-8").read())
words = pickle.load(open(os.path.join("main", "chatbot_model", "data", "words.pkl"), "rb"))
classes = pickle.load(open(os.path.join("main", "chatbot_model", "data", "classes.pkl"), "rb"))

def clean_up_sentence(sentence):
    return [lemmatizer.lemmatize(w.lower()) for w in nltk.word_tokenize(sentence)]

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

def predict_class(sentence):
    res = model.predict(np.array([bag_of_words(sentence)]))[0]
    ERROR_THRESHOLD = 0.25
    return [{"intent": classes[i], "probability": str(r)} for i, r in enumerate(res) if r > ERROR_THRESHOLD]

def get_response(intents_list):
    if not intents_list:
        return "Lo siento, no entiendo tu mensaje."

    tag = intents_list[0]['intent']

    if tag == "ahorro_actual":
        return calcular_ahorro()
    elif tag == "categoria_mas_gasto":
        return categoria_con_mas_gasto()
    
    # Respuesta por defecto
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

def calcular_ahorro():
    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo = f.read().strip()

        gastos = readfiles.GetRegisterFile()
        limites = readfiles.GetLimitFile()

        total_gasto = sum(float(r[1]) for r in gastos if r[0] == correo and int(r[5]) == date.today().month)
        limite_mes = next((float(l[1]) for l in limites if l[0] == correo and int(l[2]) == date.today().month and int(l[3]) == date.today().year), None)

        if limite_mes is None:
            return "No has definido un límite mensual, por lo tanto no puedo calcular tu ahorro."

        ahorro = limite_mes - total_gasto
        return f"Tu ahorro actual este mes es de aproximadamente S/. {ahorro:.2f}"

    except Exception as e:
        return f"Error al calcular el ahorro: {e}"

def categoria_con_mas_gasto():
    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            correo = f.read().strip()

        gastos = readfiles.GetRegisterFile()
        categorias = {}

        for r in gastos:
            if r[0] == correo and int(r[5]) == date.today().month:
                cat = r[2]
                categorias[cat] = categorias.get(cat, 0) + float(r[1])

        if not categorias:
            return "Aún no tienes gastos registrados este mes."

        categoria_max = max(categorias, key=categorias.get)
        return f"Estás gastando más en la categoría '{categoria_max}' con un total de S/. {categorias[categoria_max]:.2f}."

    except Exception as e:
        return f"Error al calcular la categoría con más gasto: {e}"

def total_gastado_mes_actual(correo):
    registros = readfiles.GetRegisterFile()
    total = 0.0
    for r in registros:
        if len(r) >= 7 and r[0] == correo and int(r[5]) == date.today().month:
            total += float(r[1])
    return total

def categoria_mas_gastada(correo):
    registros = readfiles.GetRegisterFile()
    categorias = {}
    for r in registros:
        if len(r) >= 7 and r[0] == correo and int(r[5]) == date.today().month:
            cat = r[2]
            monto = float(r[1])
            categorias[cat] = categorias.get(cat, 0) + monto
    if categorias:
        return max(categorias, key=categorias.get)
    return "No hay gastos registrados"

def Chatbot(root, mainFrame):
    import windows_app.dashboard_window as dashboard_w
    root.title("Chatbot financiero")
    mainFrame.destroy()
    mainFrame = Frame(root, width=425, height=700)
    mainFrame.pack()

    # Fondo con imagen FONDO_PROTO.jpg
    try:
        my_path = readfiles.Route()
        bg_path = os.path.join(my_path, "images", "FONDO_PROTO.jpg")
        bg_image = Image.open(bg_path).resize((425, 700), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        mainFrame.bg_photo = bg_photo  # Mantener referencia para evitar recolección de basura
        Label(mainFrame, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)
        # Fallback a gradiente si falla la imagen
        canvas = Canvas(mainFrame, width=425, height=700, bg="#1E3A8A", highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(0, 0, 425, 700, fill="#3B82F6", outline="")

    # Área de chat
    chat_log = Text(mainFrame, width=40, height=25, wrap=WORD, bg="#1E3A8A", fg="black", font=("Arial", 12), highlightthickness=0, bd=0)
    chat_log.place(x=20, y=20)
    chat_log.config(state=DISABLED)  # Solo lectura

    # Entrada de texto (subida a y=540)
    entry_frame = Frame(mainFrame, bg="#FFFFFF", width=380, height=40)
    entry_frame.place(x=20, y=540)

    entry_box = Entry(entry_frame, width=30, bg="#FFFFFF", fg="black", font=("Arial", 12), highlightthickness=0, bd=0)
    entry_box.place(x=10, y=10, width=320)

    # Botón de enviar (ícono de flecha)
    send_button = Button(entry_frame, text="➤", command=lambda: send_message(), font=("Arial", 12), bg="#FFFFFF", fg="#000000", relief="flat", bd=0)
    send_button.place(x=340, y=5)

    def send_message():
        msg = entry_box.get()
        if not msg.strip():
            return

        # Habilitar el área de texto para insertar
        chat_log.config(state=NORMAL)
        chat_log.insert(END, f"Tú: {msg}\n", "user")
        entry_box.delete(0, END)

        try:
            with open(os.path.join(readfiles.Route(), "fakedb", "session.txt"), "r", encoding="utf-8") as f:
                correo = f.read().strip()

            lower_msg = msg.lower()

            if "cuánto voy ahorrando" in lower_msg or "ahorrando" in lower_msg:
                total = total_gastado_mes_actual(correo)
                limite = next((float(l[1]) for l in readfiles.GetLimitFile() if l[0] == correo and int(l[2]) == date.today().month and int(l[3]) == date.today().year), None)
                if limite is not None:
                    ahorro = limite - total
                    res = f"Has ahorrado S/.{ahorro:.2f} este mes."
                else:
                    res = "No has definido un límite mensual, por lo tanto no puedo calcular tu ahorro."

            elif "en qué estoy gastando más" in lower_msg or "categoría más" in lower_msg:
                categoria = categoria_mas_gastada(correo)
                res = f"Tu mayor gasto este mes ha sido en: {categoria}."

            else:
                ints = predict_class(msg)
                res = get_response(ints)

            chat_log.insert(END, f"Bot: {res}\n\n", "bot")
            chat_log.see(END)

        except Exception as e:
            chat_log.insert(END, f"❌ Error: {e}\n\n", "error")
            chat_log.see(END)

        # Deshabilitar nuevamente el área de texto
        chat_log.config(state=DISABLED)

    # Configurar estilos para los mensajes
    chat_log.tag_configure("user", justify="right", foreground="black", background="#D1D5DB", wrap=WORD, lmargin1=100, rmargin=10)
    chat_log.tag_configure("bot", justify="left", foreground="black", background="#93C5FD", wrap=WORD, lmargin1=10, rmargin=100)
    chat_log.tag_configure("error", justify="center", foreground="red", background="#1E3A8A")

    # Botón "Volver" (bajado a y=650)
    Button(mainFrame, text="Volver", command=lambda: dashboard_w.Dashboard(root, mainFrame), font=("Arial", 12),
           bg="#41AADC", fg="white", activebackground="#0d8ddf", relief="flat", bd=0, padx=20, pady=5).place(relx=0.5, y=650, anchor="center")

def __volver_al_dashboard(root, mainFrame):
    from windows_app import dashboard_window as dashboard_w
    dashboard_w.Dashboard(root, mainFrame)