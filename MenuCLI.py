import time
import os
from Proyecto import *
def menuS():
        while True:
            print("!!!Seleccione uno de nuestros videos!!!")
            print("SentadillaP2 1)")
            print("SentadillaP3 2)")
            print("SentadillaP4 3)")
            print("Salir 4)")
            op = int(input("Digite su opción:"))
            
            if op==1:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/SentadillaP2.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/SentadillaP2Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/SentadillaP2Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesSentadilla(coordenadasy)
                agregar_texto_en_video("VideosPrueba/SentadillaP2.mp4","VideosResultados/SentadillaP2Analizado.mp4",r,v,f)

            elif op==2:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/SentadillaP3.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/SentadillaP3Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/SentadillaP3Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesSentadilla(coordenadasy)
                agregar_texto_en_video("VideosPrueba/SentadillaP3.mp4","VideosResultados/SentadillaP3Analizado.mp4",r,v,f)

            elif op==3:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/SentadillaP4.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/SentadillaP4Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/SentadillaP4Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesSentadilla(coordenadasy)
                agregar_texto_en_video("VideosPrueba/SentadillaP4.mp4","VideosResultados/SentadillaP4Analizado.mp4",r,v,f)

            elif op==4:
                print("Saliendo del Menú de Sentadilla...")
                time.sleep(2)
                os.system("cls")
                break
            else:
                print("Opción no válida")
                time.sleep(2)
                os.system("cls")

def menuB():
        while True:
            print("!!!Seleccione uno de nuestros videos!!!")
            print("BenchPressP1 1)")
            print("BenchPressP4 2)")
            print("Salir 3)")
            op = int(input("Digite su opción:"))
            
            if op==1:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/BenchPressP1.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/BenchPressP1Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/BenchPressP1Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesBanca(coordenadasy)
                agregar_texto_en_video("VideosPrueba/BenchPressP1.mp4","VideosResultados/BenchPressP1Analizado.mp4",r,v,f)

            elif op==2:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/BenchPressP4.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/BenchPressP4Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/BenchPressP4Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesSentadilla(coordenadasy)
                agregar_texto_en_video("VideosPrueba/BenchPressP4.mp4","VideosResultados/BenchPressP4Analizado.mp4",r,v,f)
            elif op==3:
                print("Saliendo del Menú de BenchPress...")
                time.sleep(2)
                os.system("cls")
                break
    
            else:
                print("Opción no válida")
                time.sleep(2)
                os.system("cls")

def menuD():
        while True:
            print("!!!Seleccione uno de nuestros videos!!!")
            print("DeadliftP1 1)")
            print("DeadliftP2 2)")
            print("DeadliftP3 3)")
            print("DeadliftP4 4)")
            print("Salir 5)")
            op = int(input("Digite su opción:"))
            
            if op==1:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/DeadliftP1.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/DeadliftP1Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/DeadliftP1Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesDeadlift(coordenadasy)
                agregar_texto_en_video("VideosPrueba/DeadliftP1.mp4","VideosResultados/DeadliftP1Analizado.mp4",r,v,f)

            elif op==2:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/DeadliftP2.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/DeadliftP2Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/DeadliftP2Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesDeadlift(coordenadasy)
                agregar_texto_en_video("VideosPrueba/DeadliftP2.mp4","VideosResultados/DeadliftP2Analizado.mp4",r,v,f)

            elif op==3:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/DeadliftP3.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/DeadliftP3Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/DeadliftP3Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesDeadlift(coordenadasy)
                agregar_texto_en_video("VideosPrueba/DeadliftP3.mp4","VideosResultados/DeadliftP3Analizado.mp4",r,v,f)

            elif op==4:
                model = obtenermodeloRoboflow("8aLI3Wjapr7Xpz2GLAz4","barbelld",3)#Se crea el modelo
                video = obtenerVideo("VideosPrueba/DeadliftP5.mp4")
                generarTrayectorias(video,model,"PrediccionesVideos/DeadliftP5Trayectoria.txt")
                coordenadasy=leer_coordenadas_y("PrediccionesVideos/DeadliftP5Trayectoria.txt")
                r,v,f = calculoVelocidadRepeticionesDeadlift(coordenadasy)
                agregar_texto_en_video("VideosPrueba/DeadliftP5.mp4","VideosResultados/DeadliftP5Analizado.mp4",r,v,f)
            
            elif op==5:
                print("Saliendo del Menú de Deadlift...")
                time.sleep(2)
                os.system("cls")
                break
            else:
                print("Opción no válida")
                time.sleep(2)
                os.system("cls")

os.system("cls")
while True:
    print("!!! Bienvenido al menú del analizador de ejercicios !!!")
    print("Seleccione el ejercicio a evaluar:")
    print("Squat 1)")
    print("Bench Press 2)")
    print("Deadlift 3)")
    print("Salir 4)")
    op = int(input("Digite su opción:"))
    if op==1:
        menuS()
    elif op==2:
        menuB()
    elif op==3:
        menuD()
    elif op==4:
        print("Adioooos :)")
        time.sleep(2)
        os.system("cls")
        break
    else:
        print("Opción no válida")
        time.sleep(2)
        os.system("cls")
    
