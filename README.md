# Trabajo Final Algoritmos Y Estructuras de Programación

Versiones: 
+ Python 3.9.5
+ pillow==8.3.2
+ matplotlib==3.4.3
+ tkcalendar==1.6.1
+ tensorflow==2.6.0
+ nltk==3.6.3
+ numpy==1.21.2
+ scikit-learn==0.24.2

Librerias: Tkinter, Pillow, Matplotlib, Tkcalendar, tensorflow, nltk, numpy, scikit-learn


## Paso 1:
+ Instalar Python 3.9.5
+ https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe
+ Activar la opción de añadir al path en la instalación y para todos los usuarios

## Paso 2:

+ Clonar repositorio

+ git clone https://github.com/victorflorest/tuChanchita-App.git

## Paso 3:

+ Nos dirigimos a la terminal y ingresamos los siguientes comandos:

+ py -3.9 -m venv venv39

+ .\venv39\Scripts\activate

+ en caso esto no funcione ejecutamos como administrados el powershell y ejecutamos el siguiente comando:

+ Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

+ y luego presionamos "S" para confirmar el comando

+ volvemos a ejecutar ".\venv39\Scripts\activate" en la terminal del visual studio code y nos debería aparecer entre parentesis y de color verde (venv39) al comienzo de la linea de comandos

## Paso 4:

+ Instalaremos las librerías

+ pip install -r requirements.txt


## Paso 5:

+ Ejecutamos el siguiente comando

+ python main/chatbot_model/train_chatbot.py

## Paso 6:

+ ejecutamos el programa

+ python main/main.pyw


## En caso cierras y vuelvas a abrir y no puedas ejecutar con python main/main.pyw solo escribe este comando .\venv39\Scripts\activate y ya podrás o presiona F1 escribes Select Interpreter y selecciona el que contenga venv39 y así podrás ejecutar el programa sin necesidad de escribir .\venv39\Scripts\activate cada que salgas y entres del programa


## Instrucciones por IDE
# VSCode
+ `Ctrl + Shift + P`
+ Abrir settings.json
+ Cambiar el servidor de python a Pylance
+ `"python.languageServer": "Pylance"`
+ Recomendado usar el plugin Code Runner
