
import random
import pygame

from problem import World
from gameai import AI
from gui import GUI

def run(ai = False, gui_enabled=False):
    world_size = [8,20]
    
    world = World(world_size[0], world_size[1])
    
    if gui_enabled:
        g = GUI(world)
    
    while True:
        next_block = world.getNextBlock()
        
        if gui_enabled:
            g.updateWorld(world)
        
        current_block = ai.get_position(world.clone())
        world.setCurrentBlock(current_block)
            
        world.fastForward()
        if world.gameOver():
            if  gui_enabled:
                print "Game over", world.rows_cleared
            return world.rows_cleared
            
            
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
            #elif event.type == pygame.KEYUP:
                #s=  chr(event.key)
            
                #current_block =  world.getCurrentBlock()
               
                
                #pos_x = current_block.pos[0]
                
               ##keys = event.key.get_pressed()
                #if s == "l":
                    #pos_x += 1
                    
                #if s == "k":
                    #pos_x -= 1
                
                #pos_x = max(0,min(world_size[0],pos_x))
                
                #current_block.pos[0] = pos_x
        from time import sleep
        sleep(1)
                

    

def demo():
    random.seed(2)
    ai = AI([1,0.1, None,0.01,None, 0.5])
    #blocked, compacted, future_pot, highest_row, diff, delta_rows
    #ai = AI([0.2, 0.0, 0.0, 0.0, 0.2, 0.2])
    for x in xrange(10):
        run(ai)
    #run()
                
def fitness(parameters):
    avg = 0.0
    ai = AI(parameters)
    for x in xrange(10):
        r = run(ai, True)
        avg += r
    return avg/10.0
    
if __name__=="__main__":
    demo()
            
