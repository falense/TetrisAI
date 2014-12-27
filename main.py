

import pygame

pygame.init()


world_size = (10,20)
square_size = 20

width = (world_size[0]+5)*(square_size+2) + 10
height = world_size[1]*(square_size+2) + 10 
window_size = [width,height]
window = pygame.display.set_mode(window_size)
from random import randint, choice

white = (255,255,255)
def get_random_color():
	c = (randint(0,255),randint(0,255),randint(0,255))
	return c

class Block(object):
	def __init__(self, shape):
		self.pos = [world_size[0]/2, 0]
		self.color = get_random_color()
		self.shape = shape
		self.update()
	def update(self):
		self.width = len(self.shape)
		self.height = len(self.shape[0])
	def rotate_left(self):
		new_shape = []
		for y in xrange(self.height):
			col = []
			for x in xrange(self.width):
				col.append(self.shape[x][y])
			new_shape.append(col)
		self.shape = new_shape
		
		self.update()
	def rotate_right(self):
		for x in xrange(3):
			self.rotate_left()
	def copy(self):
		b = Block(self.shape)
		b.pos[1] = self.pos[1]
		return b
		
	
def draw_square(surf,square_x,square_y, color, offset_x = 0, offset_y = 0):
	global square_size
	x = 5 + square_x* (square_size + 2) + offset_x
	y = 5 + square_y* (square_size + 2) + offset_y
	pygame.draw.rect(surf, color, (x,y,square_size,square_size))



	x = 5 + square_x* (square_size + 2) + offset_x + 2
	y = 5 + square_y* (square_size + 2) + offset_y + 2
	pygame.draw.rect(surf, map(lambda x: x*0.6, color), (x,y,square_size - 4,square_size - 4))

	




def draw_block(surf, offset_x, offset_y, b):
	for square_x, row in enumerate(b.shape):
		for square_y, active in enumerate(row):
			if active:
				draw_square(surf, square_x+b.pos[0], square_y+b.pos[1], b.color, offset_x, offset_y)
			
def draw_game(surf, next_block):
	width = world_size[0]*(square_size+2)
	height = world_size[1]*(square_size+2)
	#pygame.draw.rect(surf, white, (5,5,width,height))
	
	offset_x = width + 8
	offset_y = 5
	width = 5*(square_size+2)
	height = 5*(square_size+2)
	pygame.draw.rect(surf, white, (offset_x,offset_y,width,height))
	
	draw_block(surf, offset_x, offset_y, next_block)

			
def draw_world(surf, world, current_block):
	for square_x, column in enumerate(world):
		for square_y, color in enumerate(column):
			if color != None:
				draw_square(surf, square_x, square_y, color, 5, 5)
				
	draw_block(surf, 5,5, current_block)
def detect_collision(world, b):
	for square_x, column in enumerate(b.shape):
		for square_y, active in enumerate(column):
			if active == 1:
				index_x = square_x+b.pos[0]
				index_y = square_y+b.pos[1]
				if index_x >= world_size[0]:
					return True
				if index_y >= world_size[1]:
					return True
				if world[index_x][index_y] != None and active != None:
					return True
	return False
def step_world(world, b):
	b.pos[1] += 1
	if not detect_collision(world,b):
		return False
	else:
		b.pos[1] -= 1
		
		for square_x, column in enumerate(b.shape):
			for square_y, active in enumerate(column):
				if active:
					world[square_x+b.pos[0]][square_y+b.pos[1]] = b.color
		
		return True
def get_random_block():
	s = []
	s.append([[1,1,1,1]])
	s.append([[1,0],[1,1],[0,1]])
	s.append([[0,1],[1,1],[1,0]])
	s.append([[1,1],[1,1]])
	s.append([[0,1],[0,1],[1,1]])
	s.append([[1,0],[1,0],[1,1]])
	
	index = randint(0,len(s)-1)
	
	b = Block(s[index])
	return b

class Player(object):
	def get_position(world, current_block):
		pass
		
from copy import deepcopy

def copy_world(world):
	new_copy = []
	for index_x, col in enumerate(world):
		new_col = col[:]
		new_copy.append(new_col)
	return new_copy
		
			
class AI(Player):
	
	def test_position(self, orig_world, orig_current_block, x):
		world = deepcopy(orig_world)
		current_block = orig_current_block.copy()
		current_block.pos[0] = x
		while not step_world(world, current_block):
			continue
			
		#print self.score(world), self.score(orig_world)
		return world
	def score(self,world):
		blocked_squares = 0
		for y in xrange(0,world_size[1]-1):
			for x in xrange(0,world_size[0]):
				if world[x][y] is not None and world[x][y+1] is None:
					blocked_squares += 1
			
		return -blocked_squares
	def get_position(self,world, current_block):
		
		position = 0
		rotation = 0
		score = None
		
		moves = []
		
		current_block = current_block.copy()
		
		for r in xrange(3):
			current_block.rotate_left()
			for x in xrange(world_size[0]-current_block.width):
				if detect_collision(world, current_block):
					break
				
				t = self.test_position(world,current_block,x)
				s = self.score(t)
				#print x, s
				if s > score or score is None:
					moves = []
					move = (x,r)
					moves.append(move)
					score = s
				elif s == score:
					move = (x,r)
					moves.append(move)
				
		position, rotation = choice(moves)
		
				
		print position, rotation, score
		return position, rotation
		
class Human(Player):
	def get_position(world, current_block):
		pass

def detect_loss(world):
	for index_x, col in enumerate(world):
		if col[1] is not None:
			return True
	return False
for game_count in xrange(100):
	world = []
	for square_x in xrange(world_size[0]):
		column = []
		for square_y in xrange(world_size[1]):
			column.append(None)
		world.append(column)
		
	current_block = get_random_block()
	next_block = get_random_block()
	block_placed = False
	ai = AI()
	while True:
		
		pygame.display.flip()
		window.fill((0,0,0))
		draw_game(window, next_block)
		
		draw_world(window,world,current_block)
		
		
		
		
		if block_placed:
			current_block = next_block
			next_block = get_random_block()
			
		if detect_loss(world):
			print "Game over"
			break
				
				
		try:
			block_placed = step_world(world, current_block)
		except:
			print current_block.shape,  current_block.width,  current_block.height
			sleep(1000)
		
		position, rotation = ai.get_position(world,current_block)#randint(0,9)
		current_block.pos[0] = position
		for r in xrange(rotation):
			current_block.rotate_left()
		
		from time import sleep
		
		#sleep(0.11)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				pygame.quit()
			
