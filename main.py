

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
    def step(self):
        self.pos[1] += 1
    def unstep(self):
        self.pos[1] -= 1
    def __repr__(self):
        return str(self.pos) + " " + str(self.shape)
    def show(self):
        print "BLOCK:"
        print "Pos:", self.pos
        print "Shape:", self.shape
        print "W/H:", self.width,self.height
        
class BlockGenerator(object):
    def __init__(self):
        self.pool = []
        self.reinit_pool()
        
    def reinit_pool(self):
        self.pool.append([[1,1,1,1]])
        self.pool.append([[1,0],[1,1],[0,1]])
        self.pool.append([[0,1],[1,1],[1,0]])
        
        self.pool.append([[1,1],[1,1]])
        self.pool.append([[0,1],[0,1],[1,1]])
        self.pool.append([[1,0],[1,0],[1,1]])
        
        self.shuffle()
        
    def shuffle(self):
        for x in xrange(len(self.pool)):
            self.pool.append(self.get_random_shape())
            
    def get_random_shape(self):
        index = randint(0,len(self.pool)-1)
        shape = self.pool.pop(index)
        return shape
    
    def get(self):
        shape = self.pool.pop(0)
        b = Block(shape)
        
        if len(self.pool) == 1:
            self.reinit_pool()
        return b
        
    def peak(self):
        shape = self.pool[1]
        b = Block(shape)
        return b
        
        
        
        
        

	
from copy import deepcopy
    
class World(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.world = []
        for square_x in xrange(width):
            column = []
            for square_y in xrange(height):
                column.append(None)
            self.world.append(column)
            
        
        self.block_generator = BlockGenerator()
        
        
        self.current_block = self.block_generator.get()
        
        self.rows_cleared = 0
        

    def set_current_block(self, b):
        self.current_block = b
        
    def get_current_block(self):
        return self.current_block
    def get_next_block(self):
        return self.block_generator.peak()
    def fast_forward(self):
        while not self.block_placed():
            self.current_block.step()
            
        self.place_block()
        self.current_block = self.block_generator.get()
        self.rows_cleared += self.clear_rows()
    def place_block(self):
        b = self.current_block
        for square_x, column in enumerate(b.shape):
            for square_y, active in enumerate(column):
                if active:
                    self.world[square_x+b.pos[0]][square_y+b.pos[1]] = b.color
        
    def step(self):
        self.current_block.step()
        if self.block_placed():
            self.place_block()
            self.current_block = self.block_generator.get()
            self.rows_cleared += self.clear_rows()
            
            
    def clone(self):
        w = World(self.width, self.height)
        
        for index_x, col in enumerate(self.world):
            w.world[index_x] = col[:]
            
        w.current_block = self.current_block.copy()
        return w
    def detect_collision(self):
        b = self.current_block
        shape = self.current_block.shape
        for square_x, column in enumerate(shape):
            for square_y, active in enumerate(column):
                if active == 1:
                    index_x = square_x+b.pos[0]
                    index_y = square_y+b.pos[1]
                    if index_x >= self.width:
                        return True
                    if index_y >= self.height:
                        return True
                    if self.world[index_x][index_y] != None and active != None:
                        return True
        return False     
    def block_placed(self):
        self.current_block.step()
        r = self.detect_collision()
        self.current_block.unstep()
        return r
        
    def game_over(self):
        return self.detect_collision()
        
    def check_full_row(self,row):
        for x in xrange(self.width):
            if self.world[x][row] == None:
                return False
        return True
    def clear_rows(self):
        for y in xrange(self.height):
            if self.check_full_row(y):
                for v in xrange(y-1,-1,-1):
                    for x in xrange(self.width):
                        self.world[x][v+1] = self.world[x][v]
                return self.clear_rows()+1
        return 0
        
        

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


    
class Player(object):
	def get_position(world, current_block):
		pass
		
			
class AI(Player):
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
                    
        debug = True
        if debug:
            print "Score: ",-blocked_squares, compacted, - 2.0*future_potential, highest_row
        
        #print blocked_squares, compacted
        return -blocked_squares + compacted - future_potential - highest_row
    def get_position(self,world):
        
        moves = self.lookup_moves(world, world.get_current_block())
        
        best_score = None
        best_moves = []
        
        for s,b in moves:
            
            new_world = world.clone()
            new_world.fast_forward()
            new_world.set_current_block(world.get_current_block().copy())
            
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
        
        for r in xrange(4):
            
            for x in xrange(world_size[0]-b.width+1):
                cworld = world.clone()
                cblock = cworld.get_current_block()
                for i in xrange(r):
                    cblock.rotate_left()
                cblock.pos[0] = x
                
                b = cblock.copy()
                
                if cworld.detect_collision():
                    continue
                cworld.fast_forward()    
                
                delta_rows = cworld.rows_cleared - world.rows_cleared
                s = self.score(cworld.world) + delta_rows*100
                if s > score or score is None:
                    moves = []
                    move = (s, b)
                    moves.append(move)
                    score = s
                elif s == score:
                    move = (s, b)
                    moves.append(move)
        
        return moves
		
		
class Human(Player):
	def get_position(world, current_block):
		pass

	
from random import seed

seed(2)


def draw_info_label(window, position, space, label, value):

	font = pygame.font.Font(None,24)
	text = font.render(label, 1, white)
	window.blit(text, position)   
	text = font.render(str(value), 1, white)
	window.blit(text, (position[0]+ space,position[1] ))   

for game_count in xrange(100):
    ai = AI()
    world = World(world_size[0], world_size[1])
    
    while True:
        window.fill((0,0,0))
        #draw_game(window, next_block)
        draw_world(window,world)
        next_block = world.get_next_block()
        draw_block(window, (square_size+2)*(world_size[0]-next_block.pos[0]+1),(square_size+2)*2, next_block)
        
        draw_info_label(window, (20,20), 90, "Cleared:", str(world.rows_cleared))
        pygame.display.flip()
        
        current_block = ai.get_position(world)
        world.set_current_block(current_block)
            
        
        world.fast_forward()
        if world.game_over():
            print "Game over", world.rows_cleared
            break
        from time import sleep
        #sleep(0.1)
        
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
            
