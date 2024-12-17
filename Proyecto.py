from roboflow import Roboflow
import cv2
import re

def obtener_nombre_archivo(ruta):
    # Expresión regular para obtener lo que está entre "/" y ".mp4"
    match = re.search(r'\/([^\/]+)\.mp4$', ruta)
    if match:
        return match.group(1)  # Regresa lo que está entre "/" y ".mp4"
    else:
        # Si no hay "/..." o ".mp4", regresa la parte antes de ".mp4"
        return ruta.split(".mp4")[0]

def obtenermodeloRoboflow(apikey, project, version):
    rf = Roboflow(api_key=apikey)
    project = rf.workspace().project(project)
    return project.version(version).model


def obtenerVideo(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        return None
    return cap

    
def procesarVideo(video,model,output_fps,output_path,trajectory_file):
    # Propiedades del video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps = video.get(cv2.CAP_PROP_FPS)  # Obtener FPS original
    print(f"FPS original: {original_fps}, Resolución: {frame_width}x{frame_height}")

    # Configuración para guardar el video procesado
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, output_fps, (frame_width, frame_height))

    # Archivo para guardar las trayectorias
    trajectory_data = open(trajectory_file, 'w')  # Abrir el archivo para escritura

    # Parámetros de optimización
    resize_width = 640  # Reducir resolución
    resize_height = 360
    frame_skip = int(original_fps / output_fps)  # Ajustar la cantidad de frames a saltar según la diferencia de FPS
    frame_count = 0

    # Procesar el video
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_count += 1
        print(f"Procesando video {round((frame_count*100)/total_frames)}%")
        #os.system('cls')

        # Saltar frames según el FPS de salida
        if frame_count % frame_skip != 0:
            continue  # Saltar frames para ahorrar tiempo

        # Reducir resolución para procesamiento
        frame_resized = cv2.resize(frame, (resize_width, resize_height))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        # Predicciones del modelo
        detections = model.predict(frame_rgb, confidence=40, overlap=30).json()

        # Guardar las trayectorias en el archivo de texto
        trajectory_data.write(f"Frame {frame_count}:\n")
        for prediction in detections['predictions']:
            class_name = prediction['class']
            x = int(prediction['x'] * (frame_width / resize_width) - prediction['width'] / 2 * (frame_width / resize_width))
            y = int(prediction['y'] * (frame_height / resize_height) - prediction['height'] / 2 * (frame_height / resize_height))
            w = int(prediction['width'] * (frame_width / resize_width))
            h = int(prediction['height'] * (frame_height / resize_height))
            
            # Guardar la información de la detección (posición y clase)
            trajectory_data.write(f"  {class_name}: ({x}, {y}), ({x + w}, {y + h})\n")

            # Dibujar rectángulos y etiquetas
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Escribir el frame procesado
        out.write(frame)

    # Liberar recursos
    trajectory_data.close()  # Cerrar el archivo de trayectorias
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Video procesado guardado en: {output_path}")
    print(f"Trayectorias guardadas en: {trajectory_file}")

import cv2

def agregar_texto_en_video(input_path, output_path,repeticiones,listav,listaf):
    # Abrir el video de entrada
    if(not listav):
        print("No hay velocidads disponible para graficar")
    if (not listaf):
        print("No hay una lista de frames disponible para graficar")
    repA = 0
    velocidadA = 0
    frameA = 1
    video = cv2.VideoCapture(input_path)
    if not video.isOpened():
        print("Error al abrir el video.")
        return False

    # Obtener propiedades del video
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    #frame_skip = int(fps / 20)  # Ajustar la cantidad de frames a saltar según la diferencia de FPS
    frame_count = 0

    # Configuración para el video de salida
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Procesar cada frame del video
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_count+=1
        # Saltar frames para reducir el tiempo y los recursos
        #if frame_count % frame_skip != 0:
        #    continue  # Saltar frames para ahorrar tiempo y recursos


        posicionR = (10, frame_height - 10)  # Coordenadas (x, y)
        altura_fuente = 20  # Altura estimada de la fuente más un margen
        posicionV = (10, frame_height - 10 - altura_fuente)  # Coordenadas (x, y) ajustadas para estar arriba de posicionR
        
        # Configuración del texto
        font = cv2.FONT_HERSHEY_SIMPLEX  # Tipo de fuente
        tamaño_fuente = 1  # Tamaño de fuente
        color = (0, 255, 0)  # Color del texto (B, G, R)
        grosor = 2  # Grosor del texto
        #print(frameA)
        if(frameA in listaf):
            repA+=1
            velocidadA = listav[repA-1]
        # Agregar texto al frame
        
        (textoR_width, textoR_height), _ = cv2.getTextSize(f"Repeticiones:{repA}", font, tamaño_fuente, grosor)
        (textoV_width, textoV_height), _ = cv2.getTextSize(f"Velocidad:{velocidadA}", font, tamaño_fuente, grosor)

        # Dibujar el fondo para "Repeticiones"
        cv2.rectangle(frame, 
              (posicionR[0], posicionR[1] - textoR_height - 5),  # Esquina superior izquierda
              (posicionR[0] + textoR_width, posicionR[1] + 5),   # Esquina inferior derecha
              (0, 0, 0),  # Color negro
              -1)  # Relleno
        # Dibuja9r el fondo para "Velocidad"
        cv2.rectangle(frame, 
              (posicionV[0], posicionV[1] - textoV_height - 5), 
              (posicionV[0] + textoV_width, posicionV[1] + 5), 
              (0, 0, 0), 
              -1)

        # Agregar los textos sobre los fondos
        cv2.putText(frame, f"Repeticiones:{repA}", posicionR, font, tamaño_fuente, color, grosor, cv2.LINE_AA)
        cv2.putText(frame, f"Velocidad:{velocidadA}", posicionV, font, tamaño_fuente, color, grosor, cv2.LINE_AA)

        
        frameA+=1
        # Guardar el frame con el texto
        out.write(frame)
        

    # Liberar recursos
    video.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video procesado guardado en: {output_path}")
    return True
    



def generarTrayectorias(video, model,trajectory_file):
    # Propiedades del video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps = video.get(cv2.CAP_PROP_FPS)  # Obtener FPS original
    print(f"FPS original: {original_fps}, Resolución: {frame_width}x{frame_height}")

    # Archivo para guardar las trayectorias
    trajectory_data = open(trajectory_file, 'w')  # Abrir el archivo para escritura

    # Parámetros de optimización
    resize_width = 640  # Reducir resolución
    resize_height = 360
    frame_skip = int(original_fps / 20)  # Ajustar la cantidad de frames a saltar según la diferencia de FPS
    frame_count = 0

    # Procesar el video
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_count += 1
        print(f"Procesando video {round((frame_count * 100) / total_frames)}%")

        # Saltar frames para reducir el tiempo y los recursos
        if frame_count % frame_skip != 0:
            continue  # Saltar frames para ahorrar tiempo y recursos

        # Reducir resolución para procesamiento
        frame_resized = cv2.resize(frame, (resize_width, resize_height))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        # Predicciones del modelo
        detections = model.predict(frame_rgb, confidence=40, overlap=30).json()

        # Guardar las trayectorias en el archivo de texto
        trajectory_data.write(f"Frame {frame_count}:\n")
        for prediction in detections['predictions']:
            class_name = prediction['class']
            x = int(prediction['x'] * (frame_width / resize_width) - prediction['width'] / 2 * (frame_width / resize_width))
            y = int(prediction['y'] * (frame_height / resize_height) - prediction['height'] / 2 * (frame_height / resize_height))
            w = int(prediction['width'] * (frame_width / resize_width))
            h = int(prediction['height'] * (frame_height / resize_height))

            # Guardar la información de la detección (posición y clase)
            trajectory_data.write(f"  {class_name}: ({x}, {y}), ({x + w}, {y + h})\n")

    # Liberar recursos
    trajectory_data.close()  # Cerrar el archivo de trayectorias
    video.release()
    cv2.destroyAllWindows()

    print(f"Trayectorias guardadas en: {trajectory_file}")


def calcular_velocidad_y_repeticiones(trajectory_file, fps=20):
    # Leer las trayectorias desde el archivo
    with open(trajectory_file, 'r') as file:
        lines = file.readlines()
    
    posiciones_y = []
    i = 0  # Contador de línea
    
    while i < len(lines):
        if "Frame" in lines[i]:  # Si la línea contiene "Frame"
            i += 1  # Avanzar a la siguiente línea
            if i < len(lines) and "Barbell" in lines[i]:  # Si "Class1" está en la siguiente línea
                parts = lines[i].split(":")
                coords = parts[1].strip().split(",")
                y_position = int(coords[1].strip("()"))
                posiciones_y.append(y_position)
        i += 1
    
    # Iniciar variables
    velocidad = []
    repeticiones = 0
    calculando = False  # Indicador de si se está calculando la velocidad
    posicion_inicial = None
    direccion = 0  # 1 para subida, -1 para bajada
    
    # Iterar sobre las posiciones Y y calcular la velocidad
    for i in range(1, len(posiciones_y)):
        # Detectar la dirección de movimiento
        if posiciones_y[i] < posiciones_y[i - 1]:
            if direccion != -1:
                direccion = -1  # La barra está bajando
        elif posiciones_y[i] > posiciones_y[i - 1]:
            if direccion != 1:
                direccion = 1  # La barra está subiendo
                if not calculando:
                    # La barra comienza a subir, registrar la posición inicial
                    posicion_inicial = posiciones_y[i - 1]
                    calculando = True
                    print(f"Comienza a subir desde la posición {posicion_inicial} en el frame {i}")
        
        # Calcular velocidad solo si está subiendo
        if calculando and direccion == 1:
            # Cada medición está espaciada por 3 frames (como los datos son de 3 en 3)
            distancia = posiciones_y[i - 1] - posiciones_y[i]
            tiempo = 3 / fps  # Intervalo entre frames (3 frames)
            velocidad.append(distancia / tiempo)  # Velocidad en unidades por segundo
            
            # Si la barra supera la posición inicial, una repetición está completa
            if posiciones_y[i] >= posicion_inicial:
                repeticiones += 1
                calculando = False  # Deja de calcular hasta que comience a subir nuevamente
                print(f"Repetición {repeticiones} completada")
    
    return velocidad, repeticiones


def leer_coordenadas(trajectory_file):
    # Abrir el archivo para leer las líneas
    with open(trajectory_file, 'r') as file:
        lines = file.readlines()
    
    coordenadas = []  # Lista para almacenar las coordenadas (x, y)
    
    for line in lines:
        if "Barbell" in line:  # Detectar la línea que contiene las coordenadas
            parts = line.split(":")  # Dividir la línea para extraer las coordenadas
            coords = parts[1].strip().split(",")  # Separar las coordenadas por coma
            
            # Extraer y almacenar las coordenadas x, y como tupla
            x_position = int(coords[0].strip("()"))  # Eliminar paréntesis y convertir a entero
            y_position = int(coords[1].strip("()"))  # Eliminar paréntesis y convertir a entero
            coordenadas.append((x_position, y_position))  # Guardar la tupla (x, y)
    
    return coordenadas


def leer_coordenadas_y(trajectory_file):
    # Abrir el archivo para leer las líneas
    with open(trajectory_file, 'r') as file:
        lines = file.readlines()
    
    coordenadas_y = []  # Lista para almacenar solo las coordenadas y
    
    for line in lines:
        if "Barbell" in line:  # Detectar la línea que contiene las coordenadas
            parts = line.split(":")  # Dividir la línea para extraer las coordenadas
            coords = parts[1].strip().split(",")  # Separar las coordenadas por coma
            
            # Extraer solo la coordenada y
            y_position = int(coords[1].strip("()"))  # Eliminar paréntesis y convertir a entero
            coordenadas_y.append(y_position)  # Guardar solo la coordenada y
    
    return coordenadas_y


def calculoVelocidadRepeticionesSentadilla(lista):
    minimo = lista[0]#Barra arriba
    maximo = max(lista)#Barra abajo
    baja=False#Bandera que indicará si está en la fase concéntrica o excéntrica
    repeticiones = 0#Cantidad de repeticiones ejecutadas
    listaT = []#Lista temporal
    listaV = []#Lista que contiene las velocidades (Tiene la longitud de las repeticiones)
    listaF = []
    cont = 0#Contador de elementos recorridos
    for elemento in lista:#Recorriendo los elementos de la lista de coordenadas del eje Y
        if(elemento==minimo and baja):#Preguntamos si el elemento actual ya está en la posición de inicio para la sentadilla y ya hemos bajado
            repeticiones+=1#Se aumenta la repeticion
            listaF.append((cont+1)*3)
            baja=False#Se cambia la bandera porque ya estamos arriba
            if(listaT):#Si la lista temporal tiene elementos
                listaT.reverse()#La invertiremos para poder hacer los cálculos
                listaV.append( round( ( (-.1)*(listaT[0]-listaT[-1])/(len(listaT)) ),2 ))# A la lista de velocidades le agregamos la velocidad aproximada (más exactitud cuando haya mas fps)
                listaT.clear()#Se limpia la lista temporal
        if(elemento==maximo and not baja):#Si el elemento actual ya llegó al punto más bajo de la sentadilla y no hemos bajado
            baja = True#Se marca como que ya bajamos
            listan=lista[cont:]#Cortamos la lista desde la posición actual hasta el final
            maximo = max(listan)#Se establece la nueva altura de la barra cuando está abajo (porque puede que ahora baje mas o baje menos)
        if(baja):#Mientas estemos abajo
            listaT.append(elemento)#Añadiremos elementos a la lista temporal para calcular la velocidad mientras no hemos subido aún
        cont+=1#Se aumenta el contador


    print(f"Haz realizado {repeticiones} repeticiones")
    print(f"Han tardado respectivamente {listaV} m/s")
    print(f"Ocurrieron en los frames:{listaF}")
    return repeticiones,listaV,listaF
    

def calculoVelocidadRepeticionesBanca(lista):
    if (not lista):
        print("La lista de frames se encuentra vacía")
        return None,None,None
    print(f"Si hay elementos en la lista de puntos en y longitud:{len(lista)}")
    minimo = lista[0]#Barra arriba
    maximo = max(lista)#Barra abajo
    baja=False#Bandera que indicará si está en la fase concéntrica o excéntrica
    repeticiones = 0#Cantidad de repeticiones ejecutadas
    listaT = []#Lista temporal
    listaV = []#Lista que contiene las velocidades (Tiene la longitud de las repeticiones)
    listaF = []#Lista donde se almacena el frame exacto donde ocurrió la repetición
    cont = 0#Contador de elementos recorridos
    for elemento in lista:#Recorriendo los elementos de la lista de coordenadas del eje Y
        if(elemento==minimo and baja):#Preguntamos si el elemento actual ya está en la posición de inicio para la sentadilla y ya hemos bajado
            repeticiones+=1#Se aumenta la repeticion
            listaF.append((cont+1)*3)
            baja=False#Se cambia la bandera porque ya estamos arriba
            if(listaT):#Si la lista temporal tiene elementos
                listaT.reverse()#La invertiremos para poder hacer los cálculos
                listaV.append( round( ( (-.1)*(listaT[0]-listaT[-1])/(len(listaT)) ),2 ) )# A la lista de velocidades le agregamos la velocidad aproximada (más exactitud cuando haya mas fps)
                listaT.clear()#Se limpia la lista temporal
        if(elemento==maximo and not baja):#Si el elemento actual ya llegó al punto más bajo de la sentadilla y no hemos bajado
            baja = True#Se marca como que ya bajamos
            listan=lista[cont:]#Cortamos la lista desde la posición actual hasta el final
            maximo = max(listan)#Se establece la nueva altura de la barra cuando está abajo (porque puede que ahora baje mas o baje menos)
        if(baja):#Mientas estemos abajo
            listaT.append(elemento)#Añadiremos elementos a la lista temporal para calcular la velocidad mientras no hemos subido aún
        cont+=1#Se aumenta el contador
        

    print(f"Haz realizado {repeticiones} repeticiones")
    print(f"Han tardado respectivamente {listaV} m/s")
    print(f"Ocurrieron en los frames:{listaF}")
    return repeticiones,listaV,listaF
    

def calculoVelocidadRepeticionesDeadlift(lista):
    maximo = lista[0]#Primer elemento la barra está en el suelo y el Y es mas grande
    minimo = min(lista)#Elemento menor la barra está levantada y el Y es más chico
    arriba=False#Se inicia con la barra abajo, entonces no estamos arriba
    repeticiones = 0#No hay repeticiones hasta que alcemos la barra
    listaT = []#Lista temporal
    listaV = []#Lista de las velocidades de las repeticiones
    listaF = []#Lista donde se almacena el frame exacto donde ocurrió la repetición
    cont = 0
    for elemento in lista:
        if(elemento==minimo and not arriba):#Si el elemento actual ya está lo más arriba posible y no estabamos arriba
            repeticiones+=1
            arriba=True#Ahora estamos arriba
            listaF.append((cont+1)*3)
            if(listaT):#Si tiene elementos la lista temporal
                listaT.reverse()#
                listaV.append( round( ( (-.1)*(listaT[0]-listaT[-1])/(len(listaT)) ),2 ) )
                listaT.clear()
        if(elemento==maximo and arriba):#Si el elemento actual se encuentra en el suelo o sea en el Y positivo y ya habíamos subido
            arriba = False#Ahora estamos abajo
            listan=lista[cont:]#Se toman las trayectorias
            minimo = min(listan)#Ahora agarramos el mínimo de la lista cortada
        if(not arriba):#Mientras no estemos arriba
            listaT.append(elemento)#Agregamos a la lista temporal
        cont+=1    


    print(f"Haz realizado {repeticiones} repeticiones")
    print(f"Han tardado respectivamente {listaV} m/s")
    print(f"Ocurrieron en los frames:{listaF}")
    return repeticiones,listaV,listaF
    

