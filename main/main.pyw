from tkinter import *
import os
import windows_app.login_window as login_w
import helpers.readfiles as readfiles

#* Estructura general
root = Tk()
root.resizable(0,0)
mainFrame = Frame(root)
mainFrame.pack() 
login_w.Login(root, mainFrame)
my_path = readfiles.Route()
root.iconbitmap(os.path.join(my_path, "images", "Icono.ico"))

#* Función para cerrar y destruir la ventana al cerrar la aplicación externamente.
def quit_me():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", quit_me)
root.mainloop()