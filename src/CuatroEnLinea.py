#! /usr/bin/env python
# -*- coding: utf-8 -*-
import math
import sys
import numpy as np
import pygame
#instalar numpy y pygame para interfaz de las matrices y la interface grafica (mediante la consola de comandos)
#     pip install numpy  y  pip install pygame

NUM_FILA = 6
NUM_COLUMNA = 7

AMARILLO = (242, 230, 12)
ROJO = (219, 33, 0)
AZUL = (4, 76, 242)
NEGRO = (51, 35, 98)

# Crea el tablero (Matriz de 6 filas x 7 columnas)
def crear_tablero():
    tablero = np.zeros((NUM_FILA,NUM_COLUMNA))
    return tablero

def insertar_ficha(tablero, fila, col, ficha):
    tablero[fila][col] = ficha

#Comprueba si esa posicion es ocupada por una ficha o no.
def validar_posicion(tablero, col):
    return tablero[NUM_FILA-1][col] == 0


def obtener_siguiente_fila(tablero, col):
    for r in range(NUM_FILA):
        if tablero[r][col] == 0:
            return r


def imprimir_tablero(tablero):
    print(np.flip(tablero,0))


def movimiento_ganador(tablero, ficha):
    
    #comprobar las posiciones HORIZONTALES para ganar la partida
    for c in range(NUM_COLUMNA -3):
        for r in range(NUM_FILA):
            if tablero[r][c] == ficha and tablero[r][c+1] == ficha and tablero[r][c+2] == ficha and tablero[r][c+3] == ficha:
                return True
     
    #comprobar las posiciones VERTICALES para ganar la partida
    for c in range(NUM_COLUMNA):
        for r in range(NUM_FILA-3):
            if tablero[r][c] == ficha and tablero[r+1][c] == ficha and tablero[r+2][c] == ficha and tablero[r+3][c] == ficha:
                return True
                
    #comprobar las posiciones Positivas de DIAGONALES para ganar la partida  
    for c in range(NUM_COLUMNA -3):
        for r in range(NUM_FILA-3):
            if tablero[r][c] == ficha and tablero[r+1][c+1] == ficha and tablero[r+2][c+2] == ficha and tablero[r+3][c+3] == ficha:
                return True
    
    #comprobar las posiciones Negativas de DIAGONALES para ganar la partida  
    for c in range(NUM_COLUMNA -3):
        for r in range(3, NUM_FILA): #ese 3 indica apartir de que fila seria posible
            if tablero[r][c] == ficha and tablero[r-1][c+1] == ficha and tablero[r-2][c+2] == ficha and tablero[r-3][c+3] == ficha:
                return True
    

def dibujar_tablero(tablero):   
    for c in range(NUM_COLUMNA):
        for r in range(NUM_FILA):
            #Dibujamos el rectangulo azul del tablero y le doy una posicion
            pygame.draw.rect(pantalla, AZUL, (c*tamanioTablero, r*tamanioTablero+tamanioTablero, tamanioTablero, tamanioTablero))
            
            #Dibjuamos los circulos en el rectangulo azul ya creado 
            pygame.draw.circle(pantalla, NEGRO,(int(c*tamanioTablero+tamanioTablero/2), int(r*tamanioTablero+tamanioTablero+tamanioTablero/2)), radio)
            
    for c in range(NUM_COLUMNA):
        for r in range(NUM_FILA):
            if tablero[r][c] == 1:
                pygame.draw.circle(pantalla, ROJO,(int(c*tamanioTablero+tamanioTablero/2), altura-int(r*tamanioTablero+tamanioTablero/2)), radio)
            elif tablero[r][c] == 2:
                pygame.draw.circle(pantalla, AMARILLO,(int(c*tamanioTablero+tamanioTablero/2), altura-int(r*tamanioTablero+tamanioTablero/2)), radio)
    pygame.display.update()


tablero = crear_tablero()
imprimir_tablero(tablero)
game_over = False
turno = 0

#Definimos el tamaño de la ventana
pygame.init()

tamanioTablero = 100

ancho = NUM_COLUMNA * tamanioTablero
altura = (NUM_FILA+1) * tamanioTablero
medidas = (ancho,altura)
radio = int(tamanioTablero/2 - 5)
pantalla = pygame.display.set_mode(medidas)
dibujar_tablero(tablero)
pygame.display.update()


fuente = pygame.font.SysFont("monospace", 75) #asignamos el estilo y tamaño la letra.

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        
        #Dibujamos las fichas segun el turno en la parte superior del tablero
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(pantalla,NEGRO, (0, 0, ancho, tamanioTablero))
            posx = event.pos[0]
            
            if turno == 0:
                pygame.draw.circle(pantalla, ROJO, (posx, int(tamanioTablero/2)), radio)
            else:
                pygame.draw.circle(pantalla, AMARILLO, (posx, int(tamanioTablero/2)), radio)
                
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(pantalla,NEGRO, (0, 0, ancho, tamanioTablero))
            #print(event.pos)
            j1 = 0
            j2 = 0
            #Preguntar por turno del jugador 1
            if turno == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/tamanioTablero)) #almacenamos en la posicion del click una ficha (en esye caso un entero)

                if validar_posicion(tablero, col):
                    fila = obtener_siguiente_fila(tablero, col)
                    insertar_ficha(tablero, fila, col, 1)

                    if movimiento_ganador(tablero, 1):
                        label = fuente.render("JUGADOR 1 GANA!!!", 1, (ROJO)) #imprimos cuando gana
                        pantalla.blit(label, (40, 10)) #posicion de donde se va a ver en la pantalla
                        game_over = True
                        
                        
            #Preguntar por turno del jugador 2
            else: 
                posx = event.pos[0]
                col = int(math.floor(posx/tamanioTablero))

                if validar_posicion(tablero, col):
                    fila = obtener_siguiente_fila(tablero, col)
                    insertar_ficha(tablero, fila, col, 2)

                    if movimiento_ganador(tablero, 2):
                        label = fuente.render("JUGADOR 2 GANA!!!", 1, (AMARILLO)) #imprimos cuando gana
                        pantalla.blit(label, (40, 10)) #posicion de donde se va a ver en la pantalla
                        game_over = True
                        
                        
            imprimir_tablero(tablero)
            dibujar_tablero(tablero)
            
            turno +=1
            turno = turno % 2  #Hacemos el mod de turno para que vaya alternando entre J1 y J2
            
pygame.time.wait(4000)           