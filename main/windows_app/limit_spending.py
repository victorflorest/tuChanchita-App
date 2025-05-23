from tkinter import *

def limit_spending():
    win = Toplevel()
    win.title("Reto de No Gastar")
    win.geometry("425x700")
    win.configure(bg="#1e1f6e")

    Label(win, text="Reto de No Gastar", font=("Helvetica", 12, "bold"), bg="#1e1f6e", fg="white").pack(pady=10)
    Label(win, text="Selecciona tu gasto máximo permitido", bg="#1e1f6e", fg="white").pack()

    value_label = Label(win, text="Gasto máximo: S/.0", bg="#1e1f6e", fg="white", font=("Helvetica", 10))
    value_label.pack(pady=5)

    def on_slide(val):
        value_label.config(text=f"Gasto máximo: S/.{float(val):.2f}")

    scale = Scale(win, from_=0, to=1000, orient=HORIZONTAL, length=300,
                  bg="#1e1f6e", fg="white", troughcolor="#635bff",
                  command=on_slide)
    scale.pack(pady=10)

    Button(win, text="Volver", command=win.destroy).pack(pady=5)
