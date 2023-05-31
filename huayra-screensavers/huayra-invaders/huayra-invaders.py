#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

import pygame, sys, glob, os, types, random
from pygame import *

class Alien(object):
	def __init__(self):
		self.vida = 1
		self.escala = 1.0
		self.x, self.y = 0 , 0 # Inicia coordenadas 
		self.ani_speed_init=15
		self.ani_speed = self.ani_speed_init
		self.ani = glob.glob("/usr/share/huayra-screensavers/huayra-invaders/sprites/alien_*.png")
		self.ani.sort()
		self.cur_frame = 0
		self.last_frame = len(self.ani) - 1
		self.img = pygame.image.load(self.ani[0])
		self.w, self.h = self.img.get_size()
		self.img = pygame.transform.scale(self.img, (int(self.w * self.escala), int(self.h * self.escala)))
		self.update(0)

	def muere(self):
		global aliens_totales
		self.vida = 0

		self.ani = glob.glob("/usr/share/huayra-screensavers/huayra-invaders/sprites/bum*.png")
		self.ani.sort()
		self.cur_frame = 0
		self.last_frame = len(self.ani) - 1
		self.img = pygame.image.load(self.ani[0])
		self.update(0)

	def update(self, avance):
		if avance != 0:
			self.x+=avance
			self.ani_speed -=1 #ani_speed es un bucle de retardo para que los frames pasen más lento
			if self.ani_speed == 0:
				self.img = pygame.image.load(self.ani[self.cur_frame])
				w, h = self.img.get_size()
				self.img = pygame.transform.scale(self.img, (int(self.w * self.escala), int(self.h * self.escala)))
				self.ani_speed = self.ani_speed_init
				if self.cur_frame == self.last_frame:
					if self.vida > 0:
						self.cur_frame = 0
				else:
					self.cur_frame+=1
		pantalla.blit(self.img, (self.x, self.y))

class vaca(object):
	def __init__(self):
		self.escala = 1.0
		self.x, self.y = 0, 0
		self.ani_speed_init=30
		self.ani_speed = self.ani_speed_init
		self.ani = glob.glob("/usr/share/huayra-screensavers/huayra-invaders/sprites/vaca_*.png")
		self.ani.sort()
		self.cur_frame = 0
		self.last_frame = len(self.ani) - 1
		self.img = pygame.image.load(self.ani[0])
		self.update(0)
#		self.img = self.scale(self.escala)

	def update(self, avance):
		if avance != 0:
			self.ani_speed -=1 #ani_speed es un bucle de retardo para que los frames pasen más lento
			self.x+=avance
			if self.ani_speed == 0:
				self.img = pygame.image.load(self.ani[self.cur_frame])
				self.w, self.h = self.img.get_size()
				self.img = pygame.transform.scale(self.img, (int(self.w* self.escala), int(self.h* self.escala)))

				self.ani_speed = self.ani_speed_init
				if self.cur_frame == self.last_frame:
					self.cur_frame = 0
				else:
					self.cur_frame+=1
		pantalla.blit(self.img, (self.x, self.y))

	
def reiniciar():
	global aliens
	global vaca
	global aliens_totales
	global pos
	print ("len(POS):", len(pos))
	aliens_totales = len(pos) - 1
	aliens = [] # Borra todo
	for n in range(0, len(pos) ): # aliens_totales = filas x columnas -1, el indice va de 0 a filas x columnas - 1
		aliens.append(Alien())
		aliens[n].x, aliens[n].y = pos[n] #Restablece las coordenadas X e Y iniciales que se almacenaron
	vaca_random = random.randint(0, len(aliens) - 1)
	vaca.x = aliens[vaca_random].x # Copiamos posicion de una alien existente
	vaca.y = aliens[vaca_random].y
	aliens[vaca_random] = vaca


if __name__ == '__main__':
	ident = os.environ.get('XSCREENSAVER_WINDOW')
	os.environ['SDL_WINDOWID'] = str(ident) # Asigna la ventana del screensaver a la salida de SDL
	
	pygame.init()

	# Cuando hay multiples monitores presentes, elegimos la resolucion del que tenia la ventana activa

	display = gdk.Display.get_default()
	monitores = []
	geometrias = []
	nmons = display.get_n_monitors()
	for m in range(nmons):
		monitor = display.get_monitor(m)
		geo = monitor.get_geometry()
		
		#print "monitor %d: %d x %d" % (m,geo.width, geo.height)
		monitores.append(monitor)
		geometrias.append(geo)

	#monitor_actual = (screen.get_active_window())
	x, y, w, h = geometrias[0].x, geometrias[0].y, geometrias[0].width, geometrias[0].height
#	w = 1024 # Para test
#	h = 768	 # Para test

	pantalla = pygame.display.set_mode((geometrias[0].width, geometrias[0].height), FULLSCREEN, 32)  #Usar para screensaver
#	pantalla = pygame.display.set_mode((1024, 768)) # para tests
	max_X = w
	min_X = 0

	filas = 6
	columnas = 9
	offset = 80

	pos = []
	aliens = []
	aliens_totales = filas * columnas - 1

	clock = pygame.time.Clock()
	


	al = 0

	# Crea una matriz de filas x columnas de aliens

	for fila in range(filas):
		for columna in range (columnas):
			aliens.append(Alien())
			aliens[al].x = 1.5 * columna * aliens[al].w * aliens[al].escala
			aliens[al].y = 1.25 * fila * aliens[al].h * aliens[al].escala + offset
			pos.append((aliens[al].x, aliens[al].y)) # Guardamos la posicion como un par en una lista
			al += 1 # añade un alien

	# Pone la vaca en una posicion aleatoria de la matriz

	vaca = vaca()
	vaca_random = random.randint(0, len(aliens) - 1)
	vaca.x = aliens[vaca_random].x # Copiamos posicion de una alien existente
	vaca.y = aliens[vaca_random].y
	aliens[vaca_random] = vaca

	avance = 2

#	blanco = 255, 255, 255
#	azul = 0, 0, 255
#	fontObj = pygame.font.Font('freesansbold.ttf',20)
#	textSurfaceObj1 = fontObj.render('La pantalla es de', True, blanco, azul)
#	textSurfaceObj2 = fontObj.render(str(w) + " x ", True, blanco, azul)
#	textSurfaceObj3 = fontObj.render(str(h), True, blanco, azul)
#	textRect1 = textSurfaceObj1.get_rect()
#	textRect2 = textSurfaceObj2.get_rect()
#	textRect3 = textSurfaceObj3.get_rect()
#	textRect1.center = (0, h/2)
#	textRect2.center = (w/4, h/3)
#	textRect3.center = (w/4, h/2)


	pygame.time.set_timer(USEREVENT+1, 1000) # Establece un timer para que cada 10 segundos muera un alien

	while True:
		pantalla.fill((0,0,0))
		clock.tick(60)
#		pantalla.blit(textSurfaceObj1, textRect1)
#		pantalla.blit(textSurfaceObj2, textRect2)
#		pantalla.blit(textSurfaceObj3, textRect3)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == USEREVENT+1:
				ali = aliens[random.randint(0, len(aliens) - 1)]
				print(type(ali))
				if isinstance(ali, Alien) and ali.vida > 0 and aliens_totales > 0: # Si el elemento es de clase "alien" y está vivo
					ali.muere() # Elimina un alien al azar
					aliens_totales-=1
				if aliens_totales == 0:
					reiniciar()
		if isinstance( aliens[0], Alien):
			if aliens[0].x > (w - 1.5 * columnas * int(aliens[0].w * aliens[0].escala)) or aliens[0].x < 0 :
				avance = (-1)*avance
		else: 
			if aliens[0].x > (w - 1.5 * columnas * int(aliens[1].w * aliens[1].escala)) or aliens[0].x < 0 :
				avance = (-1)*avance

		for alien in aliens:
			alien.update(avance)


		pygame.display.update()
