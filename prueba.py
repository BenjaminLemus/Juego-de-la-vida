import pygame
import sys
import numpy as np
pygame.init()
#Dimensiones de ventana
alto_ventana=700
ancho_ventana=700
#colores en RGB
blanco=(250,250,250)
plomo = (125,125,125)
#creaacion de la venta maestra
ventana = pygame.display.set_mode((alto_ventana,ancho_ventana))
#llave
game_over= False
#limitar los loops
reloj=pygame.time.Clock()
#creacion de celdas
#numero de celdas alto y ancho
nxc, nyc = 55,55
#dimensiones de celda
dimCan=ancho_ventana/nxc
dimCal=alto_ventana/nyc
#LOGICA DEL JUEGO
#creamos una matriz
estado = np.zeros((nxc,nyc))
#si 0 esta muerta, si es 1 vive
pause = False
#ciclo principal
while not game_over:
	#copia de matriz de eventos
	copestado = np.copy(estado)

	ventana.fill((0,0,0))
	#registro de eventos
	for event in pygame.event.get():
		#print(event)
		#se corta el proceso al momento de precionar el QUIT de la pantalla
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			pause = not pause

		mouse = pygame.mouse.get_pressed()

		if sum(mouse)>0:
			#print(pygame.mouse.get_pos())
			posx, posy = pygame.mouse.get_pos()
			celX, celY = int(np.floor(posx/dimCan)), int(np.floor(posy/dimCal))
			print(celX,celY)
			copestado[celX, celY] = 1
	for x in range(0,nxc):
		for y in range (0,nyc):
			if not pause:
				#calculamos el numero de vecinos
				vecinos = estado[(x-1) % nxc, (y-1)%nyc] +\
					estado[(x-1) % nxc, (y)%nyc] +\
					estado[(x-1) % nxc, (y+1)%nyc] +\
					estado[(x)% nxc, (y-1)%nyc] +\
					estado[(x) % nxc, (y+1)%nyc] +\
					estado[(x+1) % nxc, (y-1)%nyc] +\
					estado[(x+1) % nxc, (y)%nyc] +\
					estado[(x+1)% nxc, (y+1)%nyc]
				#reglas:
				#1: una celula muerta con tres vecinas vivas revive
				if estado[x,y] == 0 and vecinos == 3:
					copestado[x,y] = 1
				elif estado[x,y] == 1 and (vecinos < 2 or vecinos > 3):
					copestado[x,y]=0

			#cordenadas para el dibujo de las celdas
			poly= [ (x    * dimCan, y    * dimCal),
					((x+1)* dimCan, y    * dimCal),
					((x+1)* dimCan,(y+1) * dimCal),
					(x    * dimCan,(y+1) * dimCal)
			]
			if copestado[x,y] == 0:
				pygame.draw.polygon(ventana,plomo, poly,1)
			else:
				pygame.draw.polygon(ventana,blanco,poly,0)
	#actualizamos la matriz
	estado = np.copy(copestado)
	#definimos el numero de frame a 20
	pygame.display.update()
	pygame.time.delay(100)
	reloj.tick(20)

	