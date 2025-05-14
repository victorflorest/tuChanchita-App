from tkinter import *
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

import helpers.readfiles as readfiles
from datetime import date

def get_response(intents_list):
    if not intents_list:
        return "Lo siento, no entiendo tu mensaje."

    tag = intents_list[0]['intent']

    if tag == "ahorro_actual":
        return calcular_ahorro()
    elif tag == "categoria_mas_gasto":
        return categoria_con_mas_gasto()
    
    # Default response
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

    chat_log = Text(mainFrame, width=50, height=25, wrap=WORD)
    chat_log.place(x=10, y=50)

    entry_box = Entry(mainFrame, width=40)
    entry_box.place(x=10, y=550)

    def send_message():
        msg = entry_box.get()
        if not msg.strip():
            return

        chat_log.insert(END, f"Tú: {msg}\n")
        entry_box.delete(0, END)

        try:
            with open("main/fakedb/session.txt", "r", encoding="utf-8") as f:
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

            chat_log.insert(END, f"Bot: {res}\n\n")

        except Exception as e:
            chat_log.insert(END, f"❌ Error: {e}\n\n")

    Label(mainFrame, text="Asistente Financiero", font=("Arial", 14)).place(x=100, y=10)
    Button(mainFrame, text="Enviar", command=send_message).place(x=320, y=545)
    Button(mainFrame, text="Volver", command=lambda: dashboard_w.Dashboard(root, mainFrame)).place(x=170, y=600)


    Label(mainFrame, text="Asistente Financiero", font=("Arial", 14)).place(x=100, y=10)
    entry_box = Entry(mainFrame, width=40)
    entry_box.place(x=10, y=550)
    Button(mainFrame, text="Enviar", command=send_message).place(x=320, y=545)
    Button(mainFrame, text="Volver", command=lambda: __volver_al_dashboard(root, mainFrame)).place(x=170, y=600)

def __volver_al_dashboard(root, mainFrame):
    from windows_app import dashboard_window as dashboard_w
    dashboard_w.Dashboard(root, mainFrame)

