import tkinter as tk
import yfinance as yf

def investment_module():
    # Crear ventana principal
    win = tk.Toplevel()
    win.title("Módulo de Inversión")
    win.geometry("425x700")
    win.configure(bg="#1e1f6e")

    # Título
    tk.Label(win, text="Oportunidades de Inversión", font=("Helvetica", 14, "bold"), bg="#1e1f6e", fg="white").pack(pady=10)

    # Entrada para monto a invertir
    tk.Label(win, text="¿Cuánto te gustaría invertir?", bg="#1e1f6e", fg="white").pack()
    investment_entry = tk.Entry(win)
    investment_entry.pack(pady=5)

    # Función para obtener los precios de las acciones
    def get_stock_prices():
        symbols = ['TSLA', '005380.KS', '7203.T']
        prices = {}
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d", interval="1h")
            current_price = hist['Close'].iloc[-1]
            one_hour_ago = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            one_day_ago = hist['Close'].iloc[0] if len(hist) > 1 else current_price
            prices[symbol] = {
                'current': current_price,
                'one_hour_ago': one_hour_ago,
                'one_day_ago': one_day_ago
            }
        return prices

    # Función para mostrar los precios
    def display_prices():
        prices = get_stock_prices()
        frame = tk.Frame(win, bg="#1e1f6e")
        frame.pack(pady=10)

        for symbol, data in prices.items():
            company_name = {'TSLA': 'Tesla', '005380.KS': 'Hyundai', '7203.T': 'Toyota'}.get(symbol, symbol)
            tk.Label(frame, text=f"{company_name} ({symbol}):", bg="#1e1f6e", fg="white").pack(anchor="w")
            tk.Label(frame, text=f"Precio actual: ${data['current']:.2f}", bg="#1e1f6e", fg="white").pack(anchor="w")
            tk.Label(frame, text=f"Hace 1 hora: ${data['one_hour_ago']:.2f}", bg="#1e1f6e", fg="white").pack(anchor="w")
            tk.Label(frame, text=f"Hace 1 día: ${data['one_day_ago']:.2f}", bg="#1e1f6e", fg="white").pack(anchor="w")
            tk.Label(frame, text="-"*30, bg="#1e1f6e", fg="white").pack()

    # Botón para mostrar los precios
    tk.Button(win, text="Mostrar precios de acciones", command=display_prices, bg="#635bff", fg="white").pack(pady=10)

    # Botón para volver
    tk.Button(win, text="Volver", command=win.destroy, bg="#48aaff", fg="white").pack(pady=10)