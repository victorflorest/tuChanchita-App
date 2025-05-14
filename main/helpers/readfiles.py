import os

def Route():
    # Devuelve la ruta base del proyecto (hasta la carpeta 'main')
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def GetRegisterFile():
    ruta = Route()
    try:
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as s:
            correo = s.read().strip()
        with open(os.path.join(ruta, "fakedb", "registers.txt"), "r", encoding="utf-8") as file:
            data = [line.strip().split(",") for line in file if line.strip()]
        registros_usuario = [r for r in data if r[0] == correo and len(r) >= 7]
        return registros_usuario
    except Exception as e:
        print("Error leyendo registers.txt:", e)
        return []


def GetPaymentsFile():
    ruta = Route()
    try:
        with open(os.path.join(ruta, "fakedb", "session.txt"), "r", encoding="utf-8") as s:
            correo = s.read().strip()
        with open(os.path.join(ruta, "fakedb", "payments.txt"), "r", encoding="utf-8") as f:
            pagos = [line.strip().split(",") for line in f if line.strip()]
        pagos_usuario = [p for p in pagos if p[0] == correo]
        return pagos_usuario
    except Exception as e:
        print("❌ Error leyendo payments:", e)
        return []


def GetLimitFile():
    try:
        path = Route()
        with open(path + r"\fakedb\limit.txt", "r", encoding="utf-8") as file:
            return [line.strip().split(",") for line in file if line.strip()]
    except Exception as e:
        print("Error al leer limit.txt:", e)
        return []


