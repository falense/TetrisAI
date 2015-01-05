

import pygame

pygame.init()


world_size = (10,40)
square_size = 20

width = (world_size[0]+5)*(square_size+2) + 10
height = world_size[1]*(square_size+2) + 10 
window_size = [width,height]
window = pygame.display.set_mode(window_size)
from random import randint, choice

white = (255,255,255)
def get_random_color():
	#c = (randint(0,255),randint(0,255),randint(0,255))
	t = randint(0,100)
	c = (t,randint(100,255),t+50)
	#return (randint(0,255),randint(0,255),randint(0,255))
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
				col.append(self.shape[x][self.height-y-1])
			new_shape.append(col)
		self.shape = new_shape
		
		self.update()
	def rotate_right(self):
		for x in xrange(3):
			self.rotate_left()
	def copy(self):
		b = Block(self.shape)
		b.pos[1] = self.pos[1]
		b.pos[0] = self.pos[0]
		return b
	def __repr__(self):
		return str(self.pos) + " " + str(self.shape)
	def show(self):
		print "BLOCK:"
		print "Pos:", self.pos
		print "Shape:", self.shape
		print "W/H:", self.width,self.height
		
#b = Block([[0,1],[0,0]])
#b.show()
#b.rotate_left()
#b.show()
#b.rotate_left()
#b.show()
#b.rotate_left()
#b.show()
#b.rotate_left()
#exit(1)
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
			


			
def draw_world(surf, world, current_block):
	for square_x, column in enumerate(world):
		for square_y, color in enumerate(column):
			if color != None:
				draw_square(surf, square_x, square_y, color, 0, 0)
			else:
				draw_square(surf, square_x, square_y, (50,50,50), 0, 0)
				
	draw_block(surf, 0,0, current_block)
def detect_collision(world, b):
	for square_x, column in enumerate(b.shape):
		for square_y, active in enumerate(column):
			#print "SQ: ", square_x, square_y
			if active == 1:
				index_x = square_x+b.pos[0]
				index_y = square_y+b.pos[1]
				if index_x >= world_size[0]:
					#print "Collision out of bounds x", index_x, world_size[0],
					#b.show()
					return True
				if index_y >= world_size[1]:
					#print "Collision out of bounds y", index_y, world_size[1]
					#b.show()
					return True
				if world[index_x][index_y] != None and active != None:
					#print "Collision overlapping squares", index_x, index_y
					#b.show()
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
		
random_pool = []

def init_pool():
	global random_pool
	s = []
	s.append([[1,1,1,1]])
	s.append([[1,0],[1,1],[0,1]])
	s.append([[0,1],[1,1],[1,0]])
	
	s.append([[1,1],[1,1]])
	s.append([[0,1],[0,1],[1,1]])
	s.append([[1,0],[1,0],[1,1]])
	random_pool = s
	
def get_random_block():
	global random_pool
	if len(random_pool) == 0:
		init_pool()
	#s = []
	#s.append([[1,1,1,1]])
	#s.append([[1,0],[1,1],[0,1]])
	#s.append([[0,1],[1,1],[1,0]])
	
	#s.append([[1,1],[1,1]])
	#s.append([[0,1],[0,1],[1,1]])
	#s.append([[1,0],[1,0],[1,1]])
	
	index = randint(0,len(random_pool)-1)
	
	shape = random_pool.pop(index)
	
	b = Block(shape)
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
	
	def apply_move(self, orig_world, orig_current_block):
		world = deepcopy(orig_world)
		current_block = orig_current_block.copy()
		while not step_world(world,current_block):
			pass
			
		while clear_rows(world):
			pass
			
		return world
	def score(self,world, debug = False):
		blocked_squares = 0
		for y in xrange(0,world_size[1]-1):
			for x in xrange(0,world_size[0]):
				if world[x][y] is None:
					for y2 in xrange(0,y):
						if world[x][y2] is not None:
							blocked_squares += 1
							break
		
		compacted = 0.0
		count = 0
		for y in xrange(world_size[1]):
			for x in xrange(world_size[0]):
				if world[x][y] is not None:
					compacted += float(y)
					count += 1
		if count > 0:
			compacted /= count
		
		future_potential = 0.0
		for y in xrange(0,world_size[1]-1):
			for x in xrange(0,world_size[0]):
				if world[x][y] is None:
					for y2 in xrange(0,y):
							if world[x][y2] is None:
								future_potential += 1
		future_potential /= 1000
						
		highest_row = -1
		for y in xrange(0,world_size[1]):
			for x in xrange(0,world_size[0]):
				if world[x][y] is not None:
					highest_row = float(y)
			
			if highest_row != -1:
				break
		
		highest_row = (world_size[1]-highest_row)/world_size[1]
		
		if highest_row > 0.5:
			highest_row = 50
					
		
		if debug:
			print "Score: ",-blocked_squares, compacted, - 2.0*future_potential, highest_row
		
		#print blocked_squares, compacted
		return -blocked_squares + compacted - future_potential - highest_row
	def get_position(self,world, current_block, next_block):
		
		moves = self.lookup_moves(world, current_block)
		
		best_score = None
		best_moves = []
		
		for s,b in moves:
			new_world = self.apply_move(world, b)
			#print self.score(new_world)
			
			next_moves = self.lookup_moves(new_world, next_block)
			#for s2,b2 in next_moves:
			#	print "\t", s2
			
			if len(next_moves) > 0:
				score, next_move = choice(next_moves)#s, b#
			else:
				continue
			#score, next_move = s,b
			if best_score is None or best_score < score:
				best_score = score
				best_moves = []
				best_moves.append(b)
			elif score >= best_score:
				best_moves.append(b)
				
		#print best_moves
		try:
			s, b = choice(moves)
			#print s
			#b.show()
			return b
		except:
			return None
				

		
	def lookup_moves(self, world, b):		
		score = None
		
		moves = []
		
		b = b.copy()
		
		for r in xrange(4):
			if r > 0:
				b.rotate_left()
			
			for x in xrange(world_size[0]-b.width+1):
				if detect_collision(world, b):
					continue
				
				b.pos[0] = x
				t = self.apply_move(world,b)
				s = self.score(t)
				#print x, s
				if s > score or score is None:
					moves = []
					move = (s, b.copy())
					moves.append(move)
					score = s
				elif s == score:
					move = (s, b.copy())
					moves.append(move)
		
		moves = sorted(moves, key=lambda x: x[0], reverse=True)
		
		return moves
		
		
class Human(Player):
	def get_position(world, current_block):
		pass

def detect_loss(world):
	for index_x, col in enumerate(world):
		if col[1] is not None:
			return True
	return False
	
from random import seed

def row_is_full(world,row):
	for x in xrange(world_size[0]):
		if world[x][row] == None:
			return False
	return True
def clear_rows(world):
	for y in xrange(0,world_size[1]):
		if row_is_full(world,y):
			#print "Clearing row" ,y 
			for v in xrange(y-1,-1,-1):
				for x in xrange(0,world_size[0]):
					world[x][v+1] = world[x][v]
			return True
	return False
seed(2)


def draw_info_label(window, position, space, label, value):

	font = pygame.font.Font(None,24)
	text = font.render(label, 1, white)
	window.blit(text, position)   
	text = font.render(str(value), 1, white)
	window.blit(text, (position[0]+ space,position[1] ))   

for game_count in xrange(100):
	world = []
	for square_x in xrange(world_size[0]):
		column = []
		for square_y in xrange(world_size[1]):
			column.append(None)
		world.append(column)
	ai = AI()
		
	current_block = get_random_block()
	next_block = get_random_block()
	current_block = ai.get_position(world,current_block, next_block)
	block_placed = False
	
	rows_cleared = 0
	drop = False
	while True:
		
		#print "**** DISP FLIP ****"
		window.fill((0,0,0))
		#draw_game(window, next_block)
		draw_world(window,world,current_block)
		draw_block(window, (square_size+2)*(world_size[0]-next_block.pos[0]+1),(square_size+2)*2, next_block)
		
		draw_info_label(window, (20,20), 90, "Cleared:", str(rows_cleared))
		pygame.display.flip()
		
		
			
				
		block_placed = step_world(world, current_block)
		while drop and not block_placed:
			block_placed = step_world(world, current_block)
			
		while clear_rows(world):
			#window.fill((0,0,0))
			#draw_game(window, next_block)
			#draw_world(window,world,current_block)
			#draw_block(window, (square_size+2)*(world_size[0]-next_block.pos[0]+1),(square_size+2)*2, next_block)
			
			#draw_info_label(window, (20,20), 90, "Cleared:", str(rows_cleared))
			#pygame.display.flip()
			rows_cleared += 1
			
			#sleep(0.1)
			
		
		if block_placed:
			current_block = next_block
			next_block = get_random_block()
		
			if detect_loss(world):
				print "Game over"
				break
			
			new_current_block = ai.get_position(world,current_block, next_block)#randint(0,9)
			if new_current_block is not None:
				if not detect_collision(world, new_current_block):
					current_block = new_current_block
				else:
					print "Invalid move reverting"
			else:
				print "Got None move"
				
			drop = True
		
		from time import sleep
		
		
		#sleep(0.1)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				pygame.quit()
			
