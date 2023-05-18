#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygame, sys, glob, os, types, random, gtk
from pygame import *

# 1. Crear vacas en posiciones aleatorias. Se sortea la direccion inicial entre cuatro posibles diagonales.
# 2. Actualizar posiciones de acuerdo a la direccion de la vaca. Si hay colision con limites se sortea nueva direccion.
# 3. En el 70% de la vida de la vaca, empezar a achicarla y hacerla transparente.
# 4. Cuando se hace alpha cero, matar la vaca
# 5. Creamos nubes de distinto tamaño para el fondo. Se debe actualizar la posicion de las nubes. Si llegan al limite derecho, deben reiniciarse a la izquierda.

direcciones = ["NO", "NE", "SO", "SE"]
CELESTE = 125, 216, 236
estados = ["creciendo", "alejando", "muriendo"] 

class Nube(object):
	def __init__(self):
		self.escala = random.uniform(0.8, 2.0)
		self.x, self.y = random.randint(0 , w), random.randint(0, h) # Inicia coordenadas aleatorias entre el 0 y el ancho de pantalla, y entre 0 y el alto de la pantalla
		self.img = pygame.image.load("/usr/share/huayra-screensavers/vaca_h6/sprites/nube.png")
		self.w, self.h = self.img.get_size()
		self.retardo = 10
		self.retardo_inicial = 10
		self.img = pygame.transform.scale(self.img, (int(self.w * self.escala), int(self.h * self.escala)))
		#print("Datos de Nube:", self.w, self.h, self.x, self.y)
		self.surf = pygame.Surface(self.img.get_size(), depth=24)

		self.key = CELESTE
		self.surf.fill(self.key, self.surf.get_rect()) #llena con color de fondo
		self.surf.set_colorkey(self.key)

		self.surf = pygame.transform.scale(self.surf, (int(self.w * self.escala), int(self.h * self.escala))) #Escalamos la superficie
		self.surf.blit(self.img, (0,0))

	def update(self):
		self.retardo -=1
		if self.retardo == 0:
			self.x += 1
			if self.x > (w + self.w):
				self.x = -self.w
				self.y = random.randint(0, h - self.h)
			self.retardo = self.retardo_inicial
			pantalla.blit(self.surf, (self.x, self.y))


class VacaVoladora(object):
	def __init__(self):
#		global direcciones
#		global CELESTE
		self.estado = "creciendo"
		self.direccion = direcciones[random.randint(0, 3)] # Sortea una de las cuatro posibles direcciones.
		self.opacidad = 0.1 #Opacidad inicial
		self.vida = 100
		self.escala = 0.1 # Escala inicial
		self.x, self.y = random.randint(0 , w), random.randint(0, h) # Inicia coordenadas aleatorias entre el 0 y el ancho de pantalla, y entre 0 y el alto de la pantalla
		self.zindex = 1000 # La profundidad inicial es tal que aparezca detrás de las nubes y de cualquier otra vaca voladora.
		self.retardo = 15
		self.ani_speed_init=10
		self.ani_speed = self.ani_speed_init
		self.ani = glob.glob("/usr/share/huayra-screensavers/vaca_h6/sprites/vuela_derecha/vaca_vuela*.png")
#		self.ani = glob.glob("sprites/vaca-volando*.png")
		self.ani.sort()
		self.cur_frame = 0
		self.last_frame = len(self.ani) - 1
		self.img = pygame.image.load(self.ani[0])
		self.w, self.h = self.img.get_size()
		self.img = pygame.transform.scale(self.img, (int(self.w * self.escala), int(self.h * self.escala)))
#		self.img = self.img.convert()
#		self.img = self.img.convert_alpha()
		self.surface = pygame.Surface(self.img.get_size(), depth=24) #Creo una superficie para tener opacidad global en el sprite
		self.key = CELESTE
		self.surface.fill(self.key, self.surface.get_rect()) #llena con color de fondo
		self.surface.set_colorkey(self.key)
		self.surface.blit(self.img, (0,0)) #Vuelca la imagen en la surface
		self.surface.set_alpha(10)
		self.update(0)

	def alejar(self):
		self.estado = "alejando"
		
	def muere(self):
		self.estado = "muriendo"
		vacas.remove(self) # Borrar de la lista el elemento en cuestion que acaba de extinguirse

	def check_limites(self):
		global w, h #Limites de la pantalla
		direcciones = []
		if self.x < 0:
			#sortear entre SE y NE
			direcciones = ["SE", "NE"]
		elif self.x > w:
			#sortear entre SO y NO
			direcciones = ["SO", "NO"]
		elif self.y < 0:
			#sortear entre NE y NO
			direcciones = ["NE", "NO"]
		elif self.y > h:
			#sortear entre SE y SO
			direcciones = ["SE", "SO"]
		else:
			direcciones = [self.direccion, self.direccion] # Si no se llegó a ningun limite forzamos la seleccion a la direccion que ya teniamos
		
		self.direccion = direcciones[random.randint(0, 1)]

	def update(self, avance):
		if avance != 0: # Actualiza frames de animacion
			# Mueve la vaca
			# Chequea la direccion de movimiento
			if self.direccion == "NO":
				self.x-=avance
				self.y+=avance

			elif self.direccion == "NE":
				self.x+=avance
				self.y+=avance

			elif self.direccion == "SE":
				self.x+=avance
				self.y-=avance

			elif self.direccion == "SO":
				self.x-=avance
				self.y-=avance

			self.check_limites() #Cambia la direccion si choca con los limites de la pantalla
		
			# Actualiza frames de animacion
			self.ani_speed -=1 #ani_speed es un bucle de retardo para que los frames pasen más lento
			if self.ani_speed == 0:
				self.img = pygame.image.load(self.ani[self.cur_frame])
				w, h = self.img.get_size()
				self.img = pygame.transform.scale(self.img, (int(self.w * self.escala), int(self.h * self.escala))) #Escalamos la imagen
				self.surface = pygame.transform.scale(self.surface, (int(self.w * self.escala), int(self.h * self.escala))) #Escalamos la superficie
				self.surface.fill(self.key, self.surface.get_rect()) #llena con color de fondo para generar una mascara
				self.surface.set_colorkey(self.key) #Crea la mascara

				self.surface.blit(self.img, (0,0)) #Vuelca la imagen en la surface
				self.ani_speed = self.ani_speed_init
				if self.cur_frame == self.last_frame:
					self.cur_frame = 0
				else:
					self.cur_frame+=1

			self.retardo -= 1
			if self.retardo == 0:
				if self.estado == "creciendo":
					if self.opacidad < 1.0:
						self.opacidad += 0.03 # Aumenta opacidad si no está al 100%
						self.surface.set_alpha(255 * self.opacidad)
					else:
						self.zindex = 10
					if self.escala < 1.0 :
						self.escala += 0.01
					else:
						self.zindex = 10

				elif self.estado == "alejando":
					if self.opacidad > 0.5:
						self.opacidad -= 0.03 # Aumenta opacidad si no está al 100%
						self.surface.set_alpha(255 * self.opacidad)
						self.zindex = 100

					if self.escala > 0.5 :
						self.escala -= 0.01

				elif self.estado == "muriendo":
					if self.opacidad > 0:
						self.opacidad -= 0.03 # Aumenta opacidad si no está al 100%
						self.surface.set_alpha(255 * self.opacidad)
					else:
						vacas.remove(self) # Si la opacidad de la vaca es 0, la borramos de la lista

					if self.escala > 0 :
						self.escala -= 0.01
					elif self.escala <= 0.1:
						vacas.remove(self) #Si la escala es menor de 10% la borramos de la lista

				self.retardo = self.ani_speed_init
			

#			if self.vida <= 70:
#				self.scale = 0.9 * self.scale #Achica un 10%

		pantalla.blit(self.surface, (self.x, self.y))


if __name__ == '__main__':
	ident = os.environ.get('XSCREENSAVER_WINDOW')
	os.environ['SDL_WINDOWID'] = str(ident) # Asigna la ventana del screensaver a la salida de SDL
	
	pygame.init()

	# Cuando hay multiples monitores presentes, elegimos la resolucion del que tenia la ventana activa

	ventana = gtk.Window()
	screen = ventana.get_screen()
	monitores = []
	nmons = screen.get_n_monitors()
	for m in range(nmons):
		mg = screen.get_monitor_geometry(m)
		#print "monitor %d: %d x %d" % (m,mg.width,mg.height)
		monitores.append(mg)

	monitor_actual = screen.get_monitor_at_window(screen.get_active_window())
	x, y, w, h = monitores[monitor_actual]
#	w = 1024 # Para test
#	h = 768	 # Para test

	pantalla = pygame.display.set_mode((w, h), FULLSCREEN, 32)  #Usar para screensaver
#	pantalla = pygame.display.set_mode((1024, 768)) # para tests
	max_X = w
	min_X = 0

	clock = pygame.time.Clock()

	vacas = [] # prepara una lista vacia de vacas
	vacas.append(VacaVoladora()) # Vaca inicial

	nubes = []
	for n in range(2, random.randint(3, 5)):
		nubes.append(Nube())


	avance = 0.75

	pygame.time.set_timer(USEREVENT+1, 9) # Cada x milisegundos actualizamos la pantalla
	pygame.time.set_timer(USEREVENT+2, 5000) # Cada X segundos creamos una nueva vaca
	pygame.time.set_timer(USEREVENT+3, 7000) # Sorteamos un estado entre las vacas
	pygame.time.set_timer(USEREVENT+4, 10) # Cada x milisegundos actualizamos la pantalla

	while True:
		pantalla.fill(CELESTE)
		clock.tick(60)
		#Mostrar nubes
		for n in nubes:
			pantalla.blit(n.surf, (n.x, n.y))


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == USEREVENT+1:
				# deberiamos actualizar
				vacas_ordenadas = sorted(vacas, key=lambda vaca: vaca.zindex, reverse= True)
				for vaca in vacas_ordenadas:
					vaca.update(avance)	# Dibuja las vacas en la pantalla ordenadas por z-index. Las que tienen
			if event.type == USEREVENT+2:
				if len(vacas) < 6:
					vacas.append(VacaVoladora())
			if event.type == USEREVENT+3:
				vacas[random.randint(0, len(vacas)-1)].estado = estados[random.randint(0,2)]
			if event.type == USEREVENT+4:
				for nube in nubes:
					nube.update() # Dibuja las nubes.

		pygame.display.update()
