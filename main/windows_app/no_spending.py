from tkinter import *
from tkinter import messagebox

def no_spending():
    win = Toplevel()
    win.title("Sin Gastos Superfluos")
    win.geometry("425x700")
    win.configure(bg="#1e1f6e")

    Label(win, text="Sin Gastos Superfluos", font=("Helvetica", 12, "bold"), bg="#1e1f6e", fg="white").pack(pady=10)
    Label(win, text="¿Cuánto gastaste hoy?", bg="#1e1f6e", fg="white").pack()

    amount_entry = Entry(win)
    amount_entry.pack(pady=5)

    frame_table = Frame(win, bg="#1e1f6e")
    frame_table.pack(pady=10)

    header = Label(frame_table, text="Día\tGasto (S/.)", bg="#1e1f6e", fg="white", justify="left", anchor="w")
    header.pack(anchor="w")

    history_label = Label(frame_table, text="", bg="#1e1f6e", fg="white", justify="left", anchor="w")
    history_label.pack(anchor="w")

    total_label = Label(win, text="Total gasto: S/.0", bg="#1e1f6e", fg="white")
    total_label.pack(pady=5)

    history = []
    total_spent = [0]
    day = [1]

    def register_spending():
        try:
            amount = float(amount_entry.get())
            if amount == 0:
                text_amount = "Sin gastos"
            else:
                text_amount = f"S/.{amount:.2f}"

            history.append(f"Día {day[0]}\t{text_amount}")
            total_spent[0] += amount

            history_label.config(text="\n".join(history))
            total_label.config(text=f"Total gasto: S/.{total_spent[0]:.2f}")
            amount_entry.delete(0, END)

            # Mostrar mensaje al finalizar la semana (día 7)
            if day[0] == 7:
                messagebox.showinfo("Resumen semanal", f"Has gastado un total de S/.{total_spent[0]:.2f} esta semana.")
                # Reiniciar contador de día y total para nueva semana si quieres
                day[0] = 1
                total_spent[0] = 0
                history.clear()
                history_label.config(text="")
                total_label.config(text="Total gasto: S/.0")
            else:
                day[0] += 1

        except ValueError:
            messagebox.showerror("Error", "Ingresa un monto válido")

    Button(win, text="Registrar gasto", bg="#635bff", fg="white", command=register_spending).pack(pady=5)
    Button(win, text="Finalizar reto", bg="#4CAF50", fg="white").pack(pady=5)
    Button(win, text="Volver", command=win.destroy).pack()
