RoboTEA ha sido desarrollado y probado con el sistema operativo Ubuntu 20.04. No se ha probado con ninguna otra versión ni otros sistemas operativos.

El primer paso de la instalación sería instalar Python en el ordenador en el que se vaya a ejecutar la aplicación. Para ello, hay que abrir el terminal y escribir lo siguiente:
```
  sudo apt update
  sudo apt install python3
```

El siguiente paso es instalar los paquetes necesarios para el correcto funcionamiento:
```
  sudo apt install python3-pip cmake python3-zeroc-ice libnss3 
  libxcomposite1 libxcursor1 libxi6 libxkbcommon0 libasound2
  
  sudo pip3 install apriltag requests mysql_connector pyunpack 
  opencv-python-headless numpy imutils six tensorflow pycozmo 
  dlib paramiko Pillow paho_mqtt pyttsx3 PySide2 
  pyparsing qdarkstyle future pyqt5
```

Una vez se tienen los paquetes instalados, el siguiente paso es descargarse el proyecto. Para ello, hay que moverse al directorio \textit{home} y posteriormente usar el comando de Git, \textit{clone}, para poder obtener el proyecto. Esto se haría ejecutando en el terminal los siguientes comandos:
```
  cd
  git clone https://github.com/mmoraleso/RoboTEA.git

```
Con esto, ya estaría instalado todo lo necesario para usar RoboTEA.


Enlaces a los íconos utilizados:
All icons from flaticon.com
- robot face from flaticon.com
- <a href="https://www.flaticon.es/iconos-gratis/boton-de-play" title="botón de play iconos">Botón de play iconos creados por xnimrodx - Flaticon</a>
- <a href="https://www.flaticon.es/iconos-gratis/boton-detener" title="botón detener iconos">Botón detener iconos creados por xnimrodx - Flaticon</a>
- <a href="https://www.flaticon.es/iconos-gratis/boton-de-pausa" title="botón de pausa iconos">Botón de pausa iconos creados por xnimrodx - Flaticon</a>
- <a href="https://www.flaticon.es/iconos-gratis/camara-del-telefono" title="cámara del teléfono iconos">Cámara del teléfono iconos creados por Creatype - Flaticon</a>
- volumen up from flaticon.com
- question mark from flaticon.com
- https://www.visualpharm.com/free-icons/help-595b40b65ba036ed117d1438
- <a href="https://www.flaticon.es/iconos-gratis/emociones" title="emociones iconos">Emociones iconos creados por Flat Icons - Flaticon</a>
- <a href="https://www.flaticon.es/iconos-gratis/medalla" title="medalla iconos">Medalla iconos creados por Freepik - Flaticon</a>
- <a href="https://www.flaticon.es/iconos-gratis/configuracion" title="configuración iconos">Configuración iconos creados por Andy Horvath - Flaticon</a>
