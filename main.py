import pygame
from componentes_generales import *
from enemigos import *
from personaje import *
from colores import *
import math
import sys
import random
import time
from personaje import Poder
from beneficios import Vida
from beneficios import Moneda
import sqlite3
pygame.init()

ancho_pantalla = 1200
alto_pantalla = 600

fuente_score = fuentes("Juego parcial/fuentes/fuente_inicio.otf", 25)
fuente_tiempo = fuentes("Juego parcial/fuentes/fuente_inicio.otf", 15)
fuente_musica = fuentes("Juego parcial/fuentes/fuente_inicio.otf", 20)
fuente_vidas= fuentes("Juego parcial/fuentes/fuente_inicio.otf",20)

pantalla_ppal = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Little Hero")
en_pantalla_de_inicio = True
rect_texto = dibujar_pantalla_de_inicio()

musica("Juego parcial/musica/music_home.mp3", 0.5, -1)
personaje = crear(150, 150, "Juego parcial/imagenes/player.png")
rayo_player = crear(60, 60, "Juego parcial/imagenes/rayo.png")
rect_personaje = personaje.get_rect()
rect_rayo_player = rayo_player.get_rect()
enemigo = crear(80, 80, "Juego parcial/imagenes/enemigo1.png")
fuego_enemigo = crear(60, 60, "Juego parcial/imagenes/fuego.png")
fondo = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo.png")
fondo2=crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo2.png")
enemigo2=crear(80,80,"Juego parcial/imagenes/enemigo2.png")
radio = 15
x_boton_verde = ancho_pantalla - 30
y_boton = 40
x_boton_rojo = ancho_pantalla - 90

musica_activada = True

flag_jugar = False

pos_horizontal_personaje = 400
pos_vertical_personaje = 200
score = 0

tiempo = 0
obstaculo = Obstaculo()
obstaculo2 = Obstaculo2()

poderes = []

rayos_enemigo = []

rayos_disparados = 0
max_rayos = 20
tiempo_ultimo_rayo = time.time()
tiempo_inicio = time.time()
tiempo_ultimo_reinicio = time.time()

tiempo_entre_rayos = 1.5
tiempo_ultimo_rayo_enemigo = time.time()
en_pantalla_de_inicio = True
rect_texto = dibujar_pantalla_de_inicio()

def mostrar_pantalla_fin():

#Esta funcion se usara a lo largo del juego para el eventual caso del que el jugador sea derrotado por el enemigo
    golpes_al_enemigo=0
    game_over = True
    personaje_visible = False  
    obstaculo.visible = False 
    fondo_borroso = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo_borroso.png")
    pantalla_ppal.blit(fondo_borroso, (0, 0))
    fuente_nombre = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 50)
    texto_nombre = fuente_nombre.render(f"GAME OVER", True, (ROJO))
    rect_texto_nombre = texto_nombre.get_rect(center=(600, 250))
    fuente_score_tiempo = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 25)
    texto_score = fuente_score_tiempo.render(f"Score: {score}", True, BLANCO)
    texto_tiempo = fuente_score_tiempo.render("Tiempo: {:02}:{:02}".format(int(tiempo // 60), int(tiempo % 60)), True, BLANCO)
    pantalla_ppal.blit(texto_tiempo, (530, 300))
    pantalla_ppal.blit(texto_score, (530, 320))
    pantalla_ppal.blit(texto_nombre, rect_texto_nombre)
    boton_menu_rect = pygame.Rect(ancho_pantalla // 2 - 50, alto_pantalla // 2 + 50, 100, 40)
    pygame.draw.rect(pantalla_ppal, VERDE, boton_menu_rect)
    fuente_boton = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 20)
    texto_boton = fuente_boton.render("RESTART", True, BLANCO)
    pantalla_ppal.blit(texto_boton, (ancho_pantalla // 2 - 25, alto_pantalla // 2 + 60))
    pygame.display.flip()
    esperando_input = True

    while esperando_input:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if boton_menu_rect.collidepoint(event.pos):
                    reiniciar_juego()
                    flag_jugar = False
                    musica_activada=True
                    esperando_input=False
                    while not flag_jugar:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if rect_texto.collidepoint(event.pos):
                                    flag_jugar = True
                                    nombre_jugador = pedir_nombre()
                                    pygame.display.flip()

                                distancia_verde = math.sqrt((event.pos[0] - x_boton_verde) ** 2 + (event.pos[1] - y_boton) ** 2)
                                distancia_rojo = math.sqrt((event.pos[0] - x_boton_rojo) ** 2 + (event.pos[1] - y_boton) ** 2)

                                if distancia_verde <= radio:
                                    musica_activada = not musica_activada
                                    if musica_activada:
                                        pygame.mixer.music.unpause()
                                    else:
                                        pygame.mixer.music.pause()

                        dibujar_pantalla_de_inicio()

                        if musica_activada:
                            pygame.draw.circle(pantalla_ppal, VERDE, (x_boton_verde, y_boton), radio)
                            texto_musica = fuente_musica.render("Music", True, VERDE)
                            pantalla_ppal.blit(texto_musica, (x_boton_verde - 70, y_boton - 8))
                        else:
                            pygame.draw.circle(pantalla_ppal, ROJO, (x_boton_verde, y_boton), radio)
                            texto_musica = fuente_musica.render("Music", True, ROJO)
                            pantalla_ppal.blit(texto_musica, (x_boton_verde - 70, y_boton - 8))

                        pygame.display.flip()
                        

                    pygame.mixer.music.stop()

def reiniciar_juego():

#Esta funcion se usara en el momento que el jugador gane o pierda y desee volver a jugar , la misma reestablecera sus 
#valores a 0 
    vidas_personaje = 3
    rayos_disparados = 0
    golpes_al_enemigo=0
    score=0
    pantalla_ppal.blit(fondo,(0,0))
    tiempo_ultimo_reinicio = time.time()
    game_over = False

    pos_horizontal_personaje = 400
    pos_vertical_personaje = 200
    obstaculo.rect.x = 1000
    obstaculo.rect.y = 500

    obstaculo.visible = True

def mostrar_pantalla_ganador(score, tiempo):

#Esta funcion se mostrara unicamente si el jugador logra derrotar al enemigo en los 3 escenarios disponibles
    game_over = True
    personaje_visible = False 
    obstaculo.visible = False
    fondo_borroso = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo_borroso.png")
    pantalla_ppal.blit(fondo_borroso, (0, 0))

    fuente_nombre = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 50)
    texto_nombre = fuente_nombre.render(f"¡GANASTE!", True, (ROJO))
    rect_texto_nombre = texto_nombre.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2))
    pantalla_ppal.blit(texto_nombre, rect_texto_nombre)

    fuente_score_tiempo = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 25)
    texto_score = fuente_score_tiempo.render(f"Score: {score}", True, BLANCO)
    texto_tiempo = fuente_score_tiempo.render("Tiempo: {:02}:{:02}".format(int(tiempo // 60), int(tiempo % 60)), True, BLANCO)
    pantalla_ppal.blit(texto_score, (ancho_pantalla // 2 - 70, alto_pantalla // 2 + 50))
    pantalla_ppal.blit(texto_tiempo, (ancho_pantalla // 2 - 70, alto_pantalla // 2 + 80))

    boton_menu_rect = pygame.Rect(ancho_pantalla // 2 - 50, alto_pantalla // 2 + 120, 100, 40)
    pygame.draw.rect(pantalla_ppal, VERDE, boton_menu_rect)

    fuente_boton = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 20)
    texto_boton = fuente_boton.render("RESTART", True, BLANCO)
    pantalla_ppal.blit(texto_boton, (ancho_pantalla // 2 - 25, alto_pantalla // 2 + 130))
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if boton_menu_rect.collidepoint(event.pos):
                    reiniciar_juego()
                    dibujar_pantalla_de_inicio()
                    esperando_input = False

    reiniciar_juego()
    dibujar_pantalla_de_inicio()
while not flag_jugar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_texto.collidepoint(event.pos):
                flag_jugar = True
                nombre_jugador = pedir_nombre()
                pygame.display.flip()

            distancia_verde = math.sqrt((event.pos[0] - x_boton_verde) ** 2 + (event.pos[1] - y_boton) ** 2)
            distancia_rojo = math.sqrt((event.pos[0] - x_boton_rojo) ** 2 + (event.pos[1] - y_boton) ** 2)

            if distancia_verde <= radio:
                musica_activada = not musica_activada
                if musica_activada:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

    dibujar_pantalla_de_inicio()

    if musica_activada:
        pygame.draw.circle(pantalla_ppal, VERDE, (x_boton_verde, y_boton), radio)
        texto_musica = fuente_musica.render("Music", True, VERDE)
        pantalla_ppal.blit(texto_musica, (x_boton_verde - 70, y_boton - 8))
    else:
        pygame.draw.circle(pantalla_ppal, ROJO, (x_boton_verde, y_boton), radio)
        texto_musica = fuente_musica.render("Music", True, ROJO)
        pantalla_ppal.blit(texto_musica, (x_boton_verde - 70, y_boton - 8))

    pygame.display.flip()

pygame.mixer.music.stop()

musica("Juego parcial/musica/music.mp3", 0.5, -1)
vidas_personaje=3
vidas_enemigo=3
invulnerable = False
tiempo_invulnerable = 2
golpes_al_enemigo = 0  
impacto_rayo = False
game_over=False
segundo_enemigo_visible = False
enemigo = crear(80, 80, "Juego parcial/imagenes/enemigo1.png")
fondo = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo.png")
segundo_enemigo = False
monedas=[]
vidas=[]
tiempo_ultima_generacion = pygame.time.get_ticks()
while flag_jugar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag_jugar = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            distancia_verde = math.sqrt((event.pos[0] - x_boton_verde) ** 2 + (event.pos[1] - y_boton) ** 2)
            distancia_rojo = math.sqrt((event.pos[0] - x_boton_rojo) ** 2 + (event.pos[1] - y_boton) ** 2)

            if distancia_verde <= radio:
                musica_activada = not musica_activada
                if musica_activada:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - tiempo_ultimo_rayo

                tiempo_transcurrido_reinicio = tiempo_actual - tiempo_ultimo_reinicio
                if tiempo_transcurrido_reinicio > 15:
                    rayos_disparados = 0
                    tiempo_ultimo_reinicio = tiempo_actual

                if rayos_disparados < max_rayos:

                    nuevo_poder = Poder(pos_horizontal_personaje+70, pos_vertical_personaje+70)
                    nuevo_poder.visible = True
                    poderes.append(nuevo_poder)

                    rayos_disparados += 1
                    tiempo_ultimo_rayo = tiempo_actual
    impacto_rayo = False

    lista_teclas = pygame.key.get_pressed()
    if True in lista_teclas:
        if lista_teclas[pygame.K_RIGHT]:
            pos_horizontal_personaje += 5
            if pos_horizontal_personaje > 880:
                pos_horizontal_personaje -= 5
        elif lista_teclas[pygame.K_LEFT]:
            pos_horizontal_personaje -= 5
            if pos_horizontal_personaje < 20:
                pos_horizontal_personaje += 5
        elif lista_teclas[pygame.K_UP]:
            pos_vertical_personaje -= 5
            if pos_vertical_personaje < 20:
                pos_vertical_personaje += 5
        elif lista_teclas[pygame.K_DOWN]:
            pos_vertical_personaje += 5
            if pos_vertical_personaje == 480:
                pos_vertical_personaje -= 5

    
    obstaculo.mover()
    pantalla_ppal.blit(fondo, (0, 0))
    dibujar_obstaculo(obstaculo)
    pantalla_ppal.blit(personaje, (pos_horizontal_personaje, pos_vertical_personaje))


    if musica_activada:
        pygame.draw.circle(pantalla_ppal, VERDE, (x_boton_verde, y_boton), radio)
        texto_musica = fuente_musica.render("Music", True, VERDE)
        pantalla_ppal.blit(texto_musica, (x_boton_verde - 65, y_boton - 8))
    else:
        pygame.draw.circle(pantalla_ppal, ROJO, (x_boton_verde, y_boton), radio)
        texto_musica = fuente_musica.render("Music", True, ROJO)
        pantalla_ppal.blit(texto_musica, (x_boton_verde - 65, y_boton - 8))
    rect_personaje = pygame.Rect(pos_horizontal_personaje, pos_vertical_personaje, personaje.get_width(), personaje.get_height())
    rect_obstaculo = obstaculo.rect
    
    tiempo_actual_vida = pygame.time.get_ticks()
    if len(vidas) <6:
        nueva_vida = Vida(ancho_pantalla, random.randint(50, alto_pantalla - 50))
        vidas.append(nueva_vida)

    for vida in vidas:
        if vida.visible:
            vida.mover()
            pantalla_ppal.blit(vida.image, vida.rect)
            if rect_personaje.colliderect(vida.rect):
                if vidas_personaje == 3:
                    vidas_personaje = 3
                    vida.visible = True
                elif vidas_personaje < 3:
                    vidas_personaje += 1
                    vida.visible = False

    tiempo_actual_vida = pygame.time.get_ticks()
    if tiempo_actual_vida - tiempo_ultima_generacion > 3000:
        nueva_vida = Vida(ancho_pantalla, random.randint(50, alto_pantalla - 50))
        vidas.append(nueva_vida)
        tiempo_ultima_generacion = tiempo_actual_vida


    tiempo_actual_moneda = pygame.time.get_ticks()
    if len(monedas) < 10:
        nueva_moneda = Moneda(ancho_pantalla, random.randint(50, alto_pantalla - 50))
        monedas.append(nueva_moneda)

    for moneda in monedas:
        if moneda.visible:
            moneda.mover()
            pantalla_ppal.blit(moneda.image, moneda.rect)
            if rect_personaje.colliderect(moneda.rect):
                moneda.visible = False
                score += 1
    
    tiempo_actual_moneda = pygame.time.get_ticks()
    if tiempo_actual_moneda - tiempo_ultima_generacion > 2000:
        nueva_moneda = Moneda(ancho_pantalla, random.randint(50, alto_pantalla - 50))
        monedas.append(nueva_moneda)
        tiempo_ultima_generacion = tiempo_actual_moneda

    for poder in poderes:
        if poder.visible and rect_obstaculo.colliderect(poder.rect):
            impacto_rayo = True 
            poder.visible = False
        poder.mover()
        poder.dibujar_poder()
    
    if impacto_rayo:
        golpes_al_enemigo +=1
        if golpes_al_enemigo == 20:
            fondo = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo2.png")
            explosion=crear(600,300,"Juego parcial/imagenes/explosion.png")
            obstaculo.visible=False
            obstaculo2.visble=True
            segundo_enemigo = True
            rayos_disparados = 0
            vidas_personaje=3
            vidas_enemigo=2
            tiempo_ultimo_reinicio = time.time()
        elif golpes_al_enemigo==50:
            enemigo_imagen = crear(80, 80, "Juego parcial/imagenes/enemigo2.png")
            fondo = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo3.png")
            segundo_enemigo = True
            rayos_disparados = 0
            vidas_personaje=3
            vidas_enemigo=1
            tiempo_ultimo_reinicio = time.time()
        elif golpes_al_enemigo==70:
            vidas_enemigo=0
            mostrar_pantalla_ganador(score, tiempo)
    tiempo_actual = time.time()   
    tiempo_transcurrido_rayo_enemigo = tiempo_actual - tiempo_ultimo_rayo_enemigo

    if tiempo_transcurrido_rayo_enemigo > tiempo_entre_rayos:
        nuevo_rayo_enemigo = RayoEnemigo(obstaculo.rect.x, obstaculo.rect.y)
        nuevo_rayo_enemigo.visible = True
        rayos_enemigo.append(nuevo_rayo_enemigo)

        tiempo_ultimo_rayo_enemigo = tiempo_actual

    for rayo_enemigo in rayos_enemigo:
        rect_rayo_enemigo = pygame.Rect(rayo_enemigo.rect.x, rayo_enemigo.rect.y, rayo_enemigo.image.get_width(), rayo_enemigo.image.get_height())
        if rayo_enemigo.visible and rect_personaje.colliderect(rect_rayo_enemigo):
            if not invulnerable:  
                vidas_personaje -= 1
                invulnerable = True
                tiempo_inicio_invulnerable = time.time()
                if vidas_personaje == 0 and not game_over:
                    game_over = True
                    obstaculo.visible = False 
                    obstaculo.visible = False  
                    mostrar_pantalla_fin()
                    pygame.display.flip()

        rayo_enemigo.mover()
        rayo_enemigo.dibujar_rayo_enemigo()

    if invulnerable and (time.time() - tiempo_inicio_invulnerable) > tiempo_invulnerable:
        invulnerable = False

    conteo_rayos_text = fuente_tiempo.render(f"Rayos disponibles: {max_rayos - rayos_disparados}", True, BLANCO)
    pantalla_ppal.blit(conteo_rayos_text, (10, y_boton + 20))

    tiempo += 0.1
    score_text = fuente_score.render(f"Score: {score}", True, BLANCO)
    vidas_text = fuente_vidas.render(f"Vidas del heroe: {vidas_personaje}", True, BLANCO)
    vidas2_text = fuente_vidas.render(f"Vidas del enemigo: {vidas_enemigo}", True, BLANCO)
    tiempo_text = fuente_tiempo.render("Time: {:02}:{:02}".format(int(tiempo // 60), int(tiempo % 60)), True, BLANCO)
    tiempo_rect = tiempo_text.get_rect()
    tiempo_rect.topleft = (10, y_boton - 5)
    pantalla_ppal.blit(score_text, (10, 10))
    pantalla_ppal.blit(tiempo_text, tiempo_rect)
    pantalla_ppal.blit(vidas_text,(200,10))
    pantalla_ppal.blit(vidas2_text,(1000,10))

    tiempo_transcurrido = time.time() - tiempo_ultimo_rayo
    if tiempo_transcurrido > 15:
        rayos_disparados = 0
        tiempo_ultimo_rayo = time.time()

    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()


class Consultas:

    def __init__(self, nombre_base) -> None:
        self.path = f"Juego parcial/{nombre_base}"

    def crear_tabla(self):
        with sqlite3.connect(self.path) as conexion:
            conexion.execute('''CREATE TABLE IF NOT EXISTS personas (
                                nombre TEXT  ,
                                score INTEGER
                            )''')
            conexion.commit()

    def agregar_dato(self, nombre, score):
        with sqlite3.connect(self.path) as conexion:
            try:
                conexion.execute("INSERT INTO personas(nombre, score) VALUES (?, ?)", (nombre, score))
                conexion.commit()
                print(f"se agrego el nombre: {nombre_jugador} y su score fue de {score}")
            except Exception as e:
                print("Error")
nombre_jugador = nombre_jugador
score = score
consulta_mysql = Consultas(f"base_datos_little_hero.db")
consulta_mysql.crear_tabla()
consulta_mysql.agregar_dato(nombre_jugador, score)