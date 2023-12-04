import re
import pygame
import colores

def crear(ancho:int,alto:int,imagen:str):

#Funcion utlizada para crear cualquier tipo de imagen que sirva para el juego.
    imagen_player = pygame.image.load(imagen)
    imagen_player = pygame.transform.scale(imagen_player,(ancho,alto))
    return imagen_player

ancho_pantalla = 1200
alto_pantalla = 600
pantalla_ppal = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Little Hero")



class Poder:

#Esta clase se encarga de crear y manejar el poder del personaje principal
    def __init__(self, x, y):
        self.image = crear(60, 60, "Juego parcial/imagenes/rayo.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 14
        self.visible = False 

    def mover(self):
        if self.visible:
            self.rect.x += self.velocidad

    def dibujar_poder(self):
        if self.visible:
            pantalla_ppal.blit(self.image, self.rect)

def colision_enemigo(self, enemigo):
        return self.rect.colliderect(enemigo.rect)
