from tkinter import *
from tkinter import messagebox

def saving_money():
    
    ahorro_win = Toplevel()
    ahorro_win.title("Desafío del ahorro")
    ahorro_win.geometry("320x450")
    ahorro_win.configure(bg="#1e1f6e")

    Label(ahorro_win, text="Desafío del ahorro", font=("Helvetica", 12, "bold"), bg="#1e1f6e", fg="white").pack(pady=10)
    Label(ahorro_win, text="¿Cuánto deseas ahorrar esta semana?", bg="#1e1f6e", fg="white").pack()

    monto_entry = Entry(ahorro_win)
    monto_entry.pack(pady=5)

    frame_tabla = Frame(ahorro_win, bg="#1e1f6e")
    frame_tabla.pack(pady=10)

    header = Label(frame_tabla, text="Semana\tMonto (S/.)", bg="#1e1f6e", fg="white", justify="left", anchor="w")
    header.pack(anchor="w")

    historial_label = Label(frame_tabla, text="", bg="#1e1f6e", fg="white", justify="left", anchor="w")
    historial_label.pack(anchor="w")

    total_label = Label(ahorro_win, text="Total ahorrado: S/.0", bg="#1e1f6e", fg="white")
    total_label.pack(pady=5)

    historial = []
    total_ahorro = [0]  # lista para que sea mutable desde inner function
    semana = [1]        # contador de semana mutable

    def registrar_ahorro():
        try:
            monto = float(monto_entry.get())
            historial.append(f"Semana {semana[0]}\tS/.{monto:.2f}")
            total_ahorro[0] += monto
            semana[0] += 1

            historial_label.config(text="\n".join(historial))
            total_label.config(text=f"Total ahorrado: S/.{total_ahorro[0]:.2f}")
            monto_entry.delete(0, END)
        except ValueError:
            messagebox.showerror("Error", "Ingresa un monto válido")

    Button(ahorro_win, text="Registrar ahorro", bg="#635bff", fg="white", command=registrar_ahorro).pack(pady=5)
    Button(ahorro_win, text="Finalizar reto", bg="#4CAF50", fg="white").pack(pady=5)
    Button(ahorro_win, text="Volver", command=ahorro_win.destroy).pack()
