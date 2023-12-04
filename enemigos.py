import pygame
import random
from componentes_generales import*
from personaje import Poder
from personaje import*

ancho_pantalla = 1200
alto_pantalla = 600
pantalla_ppal = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Little Hero")
class Obstaculo:

#Esta clase funciona con el fin de crear el enemigo y hacer funcionable
    def __init__(self):
        self.image = crear(80, 80, "Juego parcial/imagenes/enemigo1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 500
        self.velocidad = -3
        self.visible=True

    def mover(self):
        self.rect.y += self.velocidad
        if self.rect.bottom >= alto_pantalla:
            self.velocidad = -self.velocidad  
        elif self.rect.top <= 50:
            self.velocidad = abs(self.velocidad)  


def dibujar_obstaculo(obstaculo):
    pantalla_ppal.blit(obstaculo.image, obstaculo.rect)

class Obstaculo2:
    def __init__(self):
        self.image = crear(80, 80, "Juego parcial/imagenes/enemigo2.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 500
        self.velocidad = -3
        self.visible=True

    def mover(self):
        self.rect.y += self.velocidad
        if self.rect.bottom >= alto_pantalla:
            self.velocidad = -self.velocidad  
        elif self.rect.top <= 50:
            self.velocidad = abs(self.velocidad)  


    def dibujar_obstaculo(obstaculo):
        pantalla_ppal.blit(obstaculo.image, obstaculo.rect)

class Obstaculo3:
    def __init__(self):
        self.image = crear(80, 80, "Juego parcial/imagenes/enemigo3.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 500
        self.velocidad = -3
        self.visible=True

    def mover(self):
        self.rect.y += self.velocidad
        if self.rect.bottom >= alto_pantalla:
            self.velocidad = -self.velocidad  
        elif self.rect.top <= 50:
            self.velocidad = abs(self.velocidad)  


    def dibujar_obstaculo(obstaculo):
        pantalla_ppal.blit(obstaculo.image, obstaculo.rect)


class RayoEnemigo:

#Esta clase funciona con el fin de crear el fuego enemigo para atacar al personaje y hacerlo funcionable
    def __init__(self, x, y):
        self.image = crear(60, 60, "Juego parcial/imagenes/fuego.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 8
        self.visible = False 

    def mover(self):
        if self.visible:
            self.rect.x -= self.velocidad

    def dibujar_rayo_enemigo(self):
        if self.visible:
            pantalla_ppal.blit(self.image, self.rect)


def colision_personaje(self, personaje):
        if self.rect.colliderect(personaje.rect):
            self.visible = False
            return True
        return False

