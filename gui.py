
import pygame

from problem import world_size
from random import randint

square_size = 20



pygame.init()


width = (world_size[0]+5)*(square_size+2) + 10
height = world_size[1]*(square_size+2) + 10 
window_size = [width,height]
window = pygame.display.set_mode(window_size)

white = (255,255,255)

def get_random_color():
	#c = (randint(0,255),randint(0,255),randint(0,255))
	t = randint(0,100)
	c = (t,randint(100,255),t+50)
	#return (randint(0,255),randint(0,255),randint(0,255))
	return c

def draw_square(surf,square_x,square_y, color, offset_x = 0, offset_y = 0):
	global square_size
	x = 5 + square_x* (square_size + 2) + offset_x
	y = 5 + square_y* (square_size + 2) + offset_y
	pygame.draw.rect(surf, color, (x,y,square_size,square_size))



	x = 5 + square_x* (square_size + 2) + offset_x + 2
	y = 5 + square_y* (square_size + 2) + offset_y + 2
	pygame.draw.rect(surf, map(lambda x: x*0.6, color), (x,y,square_size - 4,square_size - 4))

	
def draw_block(surf, offset_x, offset_y, b):
	for square_x, column in enumerate(b.shape):
		for square_y, active in enumerate(column):
			if active:
				#print square_x+b.pos[0], square_y+b.pos[1]
				draw_square(surf, square_x+b.pos[0], square_y+b.pos[1], b.color, offset_x, offset_y)
			

def draw_world(surf, world):
	for square_x, column in enumerate(world.world):
		for square_y, color in enumerate(column):
			if color != None:
				draw_square(surf, square_x, square_y, color, 0, 0)
			else:
				draw_square(surf, square_x, square_y, (50,50,50), 0, 0)
				
	draw_block(surf, 0,0, world.get_current_block())

def draw_info_label(window, position, space, label, value):

	font = pygame.font.Font(None,24)
	text = font.render(label, 1, white)
	window.blit(text, position)   
	text = font.render(str(value), 1, white)
	window.blit(text, (position[0]+ space,position[1] ))   
