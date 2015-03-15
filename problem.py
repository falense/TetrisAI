

import numpy as np

from random import seed, randint, choice
from copy import deepcopy


from gameai import AI, Human
from gui import *
	

world_size = (12,40)



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
        b.pos[1] = 0
        b.pos[0] = self.pos[0]
        return b
    def step(self):
        self.pos[1] += 1
    def unstep(self):
        self.pos[1] -= 1
    def __repr__(self):
        return str(self.pos) + " " + str(self.shape)
    
    def get_all_orientations(self):
        b = self.copy()
        r = [b.copy()]
        for x in xrange(4):
            b.rotate_right()
            if not b in r:
                r.append(b.copy())
        return r
        

    def __eq__(self, other):
        try:
            if len(self.shape) != len(other.shape):
                return False
            for col1, col2 in zip(self.shape,other.shape): 
                if len(col1) != len(col2):
                    return False
                for cell1, cell2 in zip(col1, col2):
                    if cell1 != cell2:
                        return False
            return True
        except:
            return False
            

    def __ne__(self, other):
        return not self.__eq__(other)
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
        
        
    def __getitem__(self,index):
        shape = self.pool[index]
        b = Block(shape)
        return b
    def __len__(self):
        return len(self.pool)
        
        

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
            
        
        self.col_height = [None]*self.width
            
        
        self.block_generator = BlockGenerator()
        
        
        self.current_block = self.block_generator.get()
        
        self.rows_cleared = 0
        self.score = 0
        

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
        cleared = self.clear_rows()
        self.rows_cleared += cleared
        self.score += cleared*cleared*250
    def place_block(self):
        b = self.current_block
        for square_x, column in enumerate(b.shape):
            for square_y, active in enumerate(column):
                if active:
                    self.world[square_x+b.pos[0]][square_y+b.pos[1]] = b.color
                    self.col_height[square_x+b.pos[0]] = None
        
    def step(self):
        self.current_block.step()
        if self.block_placed():
            self.place_block()
            self.current_block = self.block_generator.get()
            
            cleared = self.clear_rows()
            self.rows_cleared += cleared
            self.score += cleared*cleared*250
            
            
    def clone(self):
        w = World(self.width, self.height)
        
        for index_x, col in enumerate(self.world):
            w.world[index_x] = col[:]
            
        w.current_block = self.current_block.copy()
        return w
    def calc_col_height(self, col):
        for y in xrange(self.height):
            if self.world[col][y] is not None:
                return self.height-y
        return 0
    def get_col_height(self, col):
        if self.col_height[col] is None:
            self.col_height[col] = self.calc_col_height(col)
        return self.col_height[col]
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
        r = False
        for x in xrange(self.width):
            r = r or (self.get_col_height(x) == self.height)
        return self.detect_collision() or r
        
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
        
        
    def __getitem__(self,index):
        return self.world[index]

    def __iter__(self):
        return self.world.__iter__()






def run(ai = False, gui_enabled=True):
    seed(2)

    from pygame.locals import *
    
    world = World(world_size[0], world_size[1])
    
    time_to_step = 1000
    
    while True:
        next_block = world.get_next_block()
        
        if gui_enabled and (time_to_step < 0 or ai != False):
            window.fill((0,0,0))
            draw_world(window,world)
            draw_block(window, (square_size+2)*(world_size[0]-next_block.pos[0]+1),(square_size+2)*2, next_block)
            
            draw_info_label(window, (20,20), 90, "Cleared:", str(world.rows_cleared))
            pygame.display.flip()
        
        if ai!=False:
            
            current_block = ai.get_position(world.clone())
            world.set_current_block(current_block)
                
            
            world.fast_forward()
            if world.game_over():
                if False and gui_enabled:
                    print "Game over", world.rows_cleared
                return world.rows_cleared,
            #raw_input()
            #raw_input()
        
        
        
        
        if time_to_step < 0:
        
            time_to_step = 1000
            world.step()
        else:
            time_to_step -= 1
            
        #print time_to_step
            
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
            elif event.type == pygame.KEYUP:
                s=  chr(event.key)
            
                current_block =  world.get_current_block()
               
                
                pos_x = current_block.pos[0]
                
               #keys = event.key.get_pressed()
                if s == "l":
                    pos_x += 1
                    
                if s == "k":
                    pos_x -= 1
                
                pos_x = max(0,min(world_size[0],pos_x))
                
                current_block.pos[0] = pos_x
                

    

def demo():
    ai = AI([1,1, 1,1,1])
    #blocked, compacted, future_pot, highest_row, diff, delta_rows
    ai = AI([0.2, 0.0, 0.0, 0.0, 0.2, 0.2])
    for x in xrange(10):
        run(ai)
    #run()
                
def fitness(parameters):
    ai = AI(parameters)
    return run(ai, True)
    
if __name__=="__main__":
    demo()
            
