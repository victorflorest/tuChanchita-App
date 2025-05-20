from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import windows_app.dashboard_window as dashboard_w
import helpers.readfiles as readfiles
from datetime import date
import tkinter.messagebox as MessageBox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import os
from PIL import Image, ImageTk

monthDic = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def CreateGraphV(frame):
    registers = readfiles.GetRegisterFile()
    categories = ["Entretenimiento", "Comida", "Educación", "Ropa", "Otros"]
    totals = {c: 0 for c in categories}

    ruta = readfiles.Route()
    with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
        usuario = f.read().strip()

    for r in registers:
        if r[0] == usuario and int(r[5]) == date.today().month:
            if r[2] in totals:
                totals[r[2]] += float(r[1])

    fig, ax = plt.subplots(figsize=(4, 2), dpi=100, facecolor='#0d8ddf')
    categorias = list(totals.keys())
    montos = list(totals.values())
    ax.bar(categorias, montos, color="#0d8ddf")
    ax.set_title("Gasto por Categoría (Mes actual)", fontsize=10, color="white", pad=10)
    ax.set_facecolor('#0d8ddf')
    ax.tick_params(axis='x', colors='white', labelsize=8, rotation=45)
    ax.tick_params(axis='y', colors='white', labelsize=8)
    for i, v in enumerate(montos):
        ax.text(i, v, f"S/. {v:.2f}", ha="center", va="bottom", fontsize=8, color="white")
    plt.tight_layout()

    canvas_chart = FigureCanvasTkAgg(fig, master=frame)
    canvas_chart.draw()
    canvas_chart.get_tk_widget().pack(pady=2)

def CreateGraphH(frame):
    registers = readfiles.GetRegisterFile()
    payments = {}

    ruta = readfiles.Route()
    with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
        usuario = f.read().strip()

    for r in registers:
        if r[0] == usuario and int(r[5]) == date.today().month:
            payments[r[3]] = payments.get(r[3], 0) + float(r[1])

    if payments:
        fig, ax = plt.subplots(figsize=(3.75, 1.5), dpi=100, facecolor='#0d8ddf')
        labels = list(payments.keys())
        values = list(payments.values())
        ax.barh(labels, values, color="#58D68D")
        ax.set_title("Gasto por Método de Pago", fontsize=10, color="white", pad=10)
        ax.set_facecolor('#0d8ddf')
        ax.tick_params(axis='x', colors='white', labelsize=8)
        ax.tick_params(axis='y', colors='white', labelsize=8)
        for i, v in enumerate(values):
            ax.text(v, i, f"S/. {v:.2f}", va="center", fontsize=8, color="white")
        plt.tight_layout()

        canvas_chart = FigureCanvasTkAgg(fig, master=frame)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack(pady=2)

def CreateTable(frame):
    ruta = readfiles.Route()
    with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
        usuario = f.read().strip()

    resumen = {m: 0 for m in monthDic.values()}
    registros = readfiles.GetRegisterFile()
    for r in registros:
        if r[0] == usuario:
            mes = int(r[5])
            resumen[monthDic[mes]] += float(r[1])

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.Treeview", 
                    background="#0d8ddf", 
                    foreground="white", 
                    fieldbackground="#0d8ddf")
    style.configure("Custom.Treeview.Heading", 
                    background="#0d8ddf", 
                    foreground="white")

    Label(frame, text="Resumen por mes", font=("Arial", 12), bg='#0d8ddf', fg='white').pack(pady=(5, 0))
    tabla = ttk.Treeview(frame, columns=("Mes", "Total"), show="headings", height=12, style="Custom.Treeview")
    tabla.column("Mes", width=200, anchor=CENTER)
    tabla.column("Total", width=200, anchor=CENTER)
    tabla.heading("Mes", text="Mes")
    tabla.heading("Total", text="Total Gastado")
    for mes, monto in resumen.items():
        tabla.insert("", "end", values=(mes, f"S/. {monto:.2f}"))
    tabla.pack(pady=5)

def ExportToPDF():
    try:
        ruta = readfiles.Route()
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as f:
            usuario = f.read().strip()
    except:
        MessageBox.showerror("Error", "No se pudo identificar al usuario.")
        return

    registros = readfiles.GetRegisterFile()
    data = []
    for r in registros:
        if r[0] == usuario:
            data.append([r[4], r[1], r[2], r[3], r[6]])

    if not data:
        MessageBox.showinfo("Sin datos", "No hay gastos para exportar.")
        return

    output_path = os.path.join(ruta, "fakedb", "reporte_gastos.pdf")
    c = pdf_canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Reporte de Gastos - {usuario}")
    headers = ["Fecha", "Monto", "Categoría", "Pago", "Tienda"]
    for i, h in enumerate(headers):
        c.drawString(50 + i * 90, 730, h)

    y = 710
    for d in data:
        for i, val in enumerate(d):
            c.drawString(50 + i * 90, y, str(val))
        y -= 15
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    MessageBox.showinfo("Exportado", f"Exportado a:\n{output_path}")

def Reports(root, mainFrame):
    root.title("Reporte Mensual")
    mainFrame.destroy()

    # Ajustamos el tamaño del contenedor al mismo que el Login (425x700)
    container = Frame(root, width=425, height=700)
    container.pack(fill="both", expand=False)

    # Creamos un Canvas con Scrollbar para permitir desplazamiento
    canvas = Canvas(container, width=425, height=700, bg='#0d8ddf')  # Fondo azul como respaldo
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Configuramos el desplazamiento
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fondo personalizado ajustado para cubrir toda la ventana visible
    try:
        my_path = readfiles.Route()
        ruta_fondo = os.path.join(my_path, "images", "Reporte_Mensual.png")
        imagen_fondo = Image.open(ruta_fondo).resize((425, 700), Image.Resampling.LANCZOS)  # Redimensionamos con mejor calidad
        foto_fondo = ImageTk.PhotoImage(imagen_fondo)
        fondo_label = Label(scrollable_frame, image=foto_fondo)
        fondo_label.image = foto_fondo  # Evita el garbage collection
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("⚠️ Error cargando fondo:", e)

    # Contenido sobre el fondo
    Label(scrollable_frame, text="Reporte Mensual", font=("Arial", 16), bg='#0d8ddf', fg='white').pack(pady=(10, 0))
    Label(scrollable_frame, text=f"Mes actual: {monthDic[date.today().month]}", font=("Arial", 10), bg='#0d8ddf', fg='white').pack(pady=(0, 5))

    CreateGraphV(scrollable_frame)
    CreateGraphH(scrollable_frame)
    CreateTable(scrollable_frame)

    Button(scrollable_frame, text="Exportar a PDF", command=ExportToPDF, width=30, bg="#4682B4", fg="white", activebackground="#5DADE2", activeforeground="white").pack(pady=5)
    Button(scrollable_frame, text="Volver", command=lambda: dashboard_w.Dashboard(root, container), width=30, bg="#4682B4", fg="white", activebackground="#5DADE2", activeforeground="white").pack(pady=(0, 5))