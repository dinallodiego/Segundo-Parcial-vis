import pygame
from enemigos import *
from personaje import *
from colores import *
from personaje import Poder
from pygame.locals import *
import sys
def toggle_musica():

#Funcion encargada de manejar la musica
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play(-1)

def musica(url:str,vol:float,play:int):

#Funcion encargada de cargar la musica iniciarla y manejar volumen
    pygame.mixer.music.load(url)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play(play)

def dibujar_pantalla_de_inicio():

#Esta funcion se utiliza apenas comienza el juego, muestra el titulo y un boton play para poder comenzar
    fondo_borroso = crear(ancho_pantalla, alto_pantalla, "Juego parcial/imagenes/fondo_borroso.png")
    pantalla_ppal.blit(fondo_borroso, (0, 0))
    fuente_titulo = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 100)
    texto = fuente_titulo.render("Play", True, GRIS)
    titulo = fuente_titulo.render("Little Hero", True, ROJO)
    rect_texto = texto.get_rect()
    rect_texto.center = (ancho_pantalla // 2, alto_pantalla // 2)
    pantalla_ppal.blit(texto, rect_texto)
    pantalla_ppal.blit(titulo, (380, 130))
    boton_menu_rect = pygame.Rect(540, 490, 100, 40)
    pygame.draw.rect(pantalla_ppal, VERDE, boton_menu_rect)
    fuente_boton = pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 30)
    texto_boton = fuente_boton.render("QUIT", True, BLANCO)
    pantalla_ppal.blit(texto_boton, (563, 500))
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if boton_menu_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    return rect_texto

def fuentes(fuente:str,dimension:int):

#Esta funcion toma como parametro fuente el cual es un str asociado al directorio en donde se encuentra la fuente
#deseada a utilizar , ademas una dimension que hace referencia al tamaño de la fuente, y luego lo retornara para su uso.
    fuente=pygame.font.Font(fuente, dimension)
    return fuente

def pedir_nombre():

#Esta funcion permite ingresar un nombre de maximo 10 caracteres y retornara el mismo.
    nombre = ""
    input_activo = True

    while input_activo:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:  
                    input_activo = False
                elif event.key == K_BACKSPACE:
                    nombre = nombre[:-1]
                elif event.unicode.isalnum() and len(nombre) < 10:
                    nombre += event.unicode
            
        fondo_borroso=crear(ancho_pantalla,alto_pantalla,"Juego parcial/imagenes/fondo_borroso.png")
        pantalla_ppal.blit(fondo_borroso, (0, 0))
        fuente_nombre =  pygame.font.Font("Juego parcial/fuentes/fuente_inicio.otf", 50)
        texto_nombre = fuente_nombre.render(f"Ingrese su nombre y presione enter: {nombre}", True, (ROJO))
        rect_texto_nombre = texto_nombre.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2))
        pantalla_ppal.blit(texto_nombre, rect_texto_nombre)

        pygame.display.flip()

    return nombre






    

