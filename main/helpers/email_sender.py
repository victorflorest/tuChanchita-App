
import smtplib
from email.message import EmailMessage

def enviar_token(destinatario, token, remitente, clave_app):
    msg = EmailMessage()
    msg['Subject'] = "Recuperación de contraseña - TuChanchita"
    msg['From'] = remitente
    msg['To'] = destinatario
    msg.set_content(f"Hola,\n\nTu código de recuperación es: {token}\n\nIngresa este código en la aplicación para restablecer tu contraseña.\n\nGracias,\nTuChanchita")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, clave_app)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Error al enviar el correo:", e)
        return False
