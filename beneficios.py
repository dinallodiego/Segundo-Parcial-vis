import pygame
import random
import time
from personaje import*
ancho_pantalla = 1200
alto_pantalla = 600

pantalla_ppal = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

class Vida(pygame.sprite.Sprite):

#Esta clase vida parte a ser un beneficio para el personaje en la cual si puede tomarlas y en caso de tener menos de 3
#vidas puede sumar una nueva vida
    def __init__(self, x, y):
        super().__init__()
        self.image =crear(40,40,"Juego parcial/imagenes/vida.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        

    def mover(self):
        self.rect.x -= 1

    def dibujar_vida(self, pantalla):
        if self.visible:
            pantalla.blit(self.image, self.rect)
class Moneda(pygame.sprite.Sprite):
#Esta clase moneda parte a ser la parte mas importante del juego para el personaje ya que al tomarlas
#incrementara su score 
    def __init__(self, x, y):
        super().__init__()
        self.image =crear(40,40,"Juego parcial/imagenes/moneda.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        

    def mover(self):
        self.rect.x -= 3

    def dibujar_moneda(self, pantalla):
        if self.visible:
            pantalla.blit(self.image, self.rect)
