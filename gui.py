
import pygame

from random import randint

square_size = 20

white = (255,255,255)

class GUI(object):
    def __init__(self, world):
        pygame.init()
        self.surface = self._pygameInit(world)
        
        self.world_width = world.width
        self.world_height = world.height
    def _pygameInit(self,world):
        width = (world.width+5)*(square_size+2) + 10
        height = world.height*(square_size+2) + 10 
        window_size = [width,height]
        return pygame.display.set_mode(window_size)

    def getRandomColor(self):
        #c = (randint(0,255),randint(0,255),randint(0,255))
        t = randint(0,100)
        c = (t,randint(100,255),t+50)
        #return (randint(0,255),randint(0,255),randint(0,255))
        return c

    def _drawSquare(self,square_x,square_y, color, offset_x = 0, offset_y = 0):
        t_x = (self.world_width-square_x-1)* (square_size + 2) 
        t_y = (self.world_height-square_y-1)* (square_size + 2)
        
        x = 5 + t_x + offset_x
        y = 5 + t_y + offset_y
        
        pygame.draw.rect(self.surface, color, (x,y,square_size,square_size))
        pygame.draw.rect(self.surface, map(lambda x: x*0.6, color), (x+2,y+2,square_size - 4,square_size - 4))
        
    def _drawBlock(self, offset_x, offset_y, b):
        for square_x, column in enumerate(b.shape):
            for square_y, active in enumerate(column):
                if active:
                    #print square_x+b.pos[0], square_y+b.pos[1]
                    self._drawSquare(b.pos[0]+square_x, b.pos[1]+square_y, (255,0,0), offset_x, offset_y)
                

    def _drawWorld(self, world):
        for square_x in range(world.width):
            for square_y in range(world.height):
                if world._getCell(square_x, square_y) == True:
                    self._drawSquare(square_x, square_y, (0,0,150), 0, 0)
                else:
                    self._drawSquare(square_x, square_y, (50,50,50), 0, 0)
                    
        self._drawBlock(0,0, world.getCurrentBlock())

    def _drawInfoLabel(self,position, space, label, value):
        font = pygame.font.Font(None,24)
        text = font.render(label, 1, white)
        self.surface.blit(text, position)   
        text = font.render(str(value), 1, white)
        self.surface.blit(text, (position[0]+ space,position[1] ))   
        
    def updateWorld(self, world):
        self.surface.fill((0,0,0))
        self._drawWorld(world)
        self._drawBlock((square_size + 2) * (self.world_width),0, world.getNextBlock())
        
        self._drawInfoLabel((20,20), 90, "Cleared:", str(world.rows_cleared))
        pygame.display.flip()

