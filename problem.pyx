
import random

from libc.stdlib cimport malloc, free


class Block:
    def __init__(self, shape, world_width):
        self.world_width = world_width
        self.pos = [world_width/2, 19]
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
        b = Block(self.shape, self.world_width)
        b.pos[1] = self.pos[1]
        b.pos[0] = self.pos[0]
        return b
    def step(self):
        self.pos[1] -= 1
    def __repr__(self):
        return str(self.pos[0]) + " " + str(self.pos[1]) + " " + str(self.shape)
    
    def get_all_orientations(self):
        b = self.copy()
        r = [b.copy()]
        for x in xrange(4):
            b.rotate_right()
            if not b in r:
                r.append(b.copy())
        return r
        
    def getMask(self):
        mask = [0]*self.height
        
        for row_index in xrange(self.height):
            mask[row_index] = 0
            for col_index in xrange(self.width):
                v = self.shape[col_index][row_index]
                if v:
                    mask[row_index]  = mask[row_index]  | 1
                mask[row_index]  = mask[row_index]  << 1
                
                
            mask[row_index]  = mask[row_index]  >> 1
        return mask
        

#    def __eq__(self, other):
#        try:
#            if len(self.shape) != len(other.shape):
#                return False
#            for col1, col2 in zip(self.shape,other.shape): 
#                if len(col1) != len(col2):
#                    return False
#                for cell1, cell2 in zip(col1, col2):
#                    if cell1 != cell2:
#                        return False
#            return True
#        except:
#            return False
            

#    def __ne__(self, other):
#        return not self.__eq__(other)
        
    def show(self):
        print "BLOCK:"
        print "Pos:", self.pos[0], self.pos[1]
        print "Shape:", self.shape
        print "W/H:", self.width,self.height

class BlockGenerator(object):
    def __init__(self, world_width):
        self.pool = []
        self.world_width = world_width
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
        index = random.randint(0,len(self.pool)-1)
        shape = self.pool.pop(index)
        return shape
    
    def get(self):
        shape = self.pool.pop(0)
        b = Block(shape, self.world_width)
        
        if len(self.pool) == 1:
            self.reinit_pool()
        return b
        
    def peak(self):
        shape = self.pool[0]
        b = Block(shape, self.world_width)
        return b
        
        
    def __getitem__(self,index):
        shape = self.pool[index]
        b = Block(shape)
        return b
    def __len__(self):
        return len(self.pool)



class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [0]*self.height
        
        
        for r in xrange(height):
            self.data[r] = 0 #2**r - 1
            
        assert width<32, "Too wide board"
        
        
        
        self.col_height = [0]*self.width
        
        self.block_generator = BlockGenerator(self.width)
        
        self.current_block = self.block_generator.get()
        
        self.rows_cleared = 0
        self.score = 0
        
    def setCurrentBlock(self, b):
        self.current_block = b
    def getCurrentBlock(self):
        return self.current_block
    def getNextBlock(self):
        return self.block_generator.peak()
    def fastForward(self):
        while not self.blockPlaced(self.current_block):
            self.current_block.step()
            
        self.placeBlock(self.current_block)
        self.current_block = self.block_generator.get()
        cleared = self._clearRows()
        self.rows_cleared += cleared
        self.score += cleared*cleared*250
        
    def placeBlock(self, block):
        mask = block.getMask()
        for i in xrange(block.height):
            self.data[i+block.pos[1]] = self.data[i+block.pos[1]] | (mask[i] << block.pos[0])

        
        
    def step(self):
        self.current_block.step()
        if self.blockPlaced(self.current_block):
            self.placeBlock()
            self.current_block = self.block_generator.get()
            
            cleared = self._clearRows()
            self.rows_cleared += cleared
            self.score += cleared*cleared*250
        print "Stepped"
            
        
    def clone(self):
        w = World(self.width, self.height)
        
        w.data[:] = self.data[:]
            
        w.current_block = self.current_block.copy()
        
        w.rows_cleared = self.rows_cleared 
        return w
        
        
    def _calcColHeight(self, col_index):
        for i in xrange(self.width):
            self.col_height[i] = -1
        mask = 1 << col_index
        
        acc = 2**self.width-1
        for r in xrange(self.height):
            acc = acc & self.data[r]
            
            if acc & mask == 0:
                return r-1
                
        return self.height-1
            
        
    def getColHeight(self, col_index):
        return self._calcColHeight(col_index)
        
    def detectCollision(self, block):  
        #Check for outside bounds rights
        if block.pos[0] + block.width >= self.width:
            return True
            
        #Check for outside bounds left
        if block.pos[0] < 0:
            return True
            
        #Check for outside bounds bottom
        if block.pos[1] < 0:
            return True
            
        mask = block.getMask()
        for i in xrange(block.height):
            if i+block.pos[1] >= self.height:
                continue
            
            if self.data[i+block.pos[1]] & (mask[i] << block.pos[0]) > 0:
                return True
        
        return False
        
    def blockPlaced(self, block):
        b = block.copy()
        b.step()
        return self.detectCollision(b)
    def gameOver(self):
        return self.detectCollision(self.current_block) 
        
    def checkFullRow(self,row_index):
        full_row = 2**self.width - 1
        return self.data[row_index] == full_row
        
    def _getCell(self, col_index, row_index):
        value = 1 << col_index
        return self.data[row_index] & value > 0
        
    def _updateRow(self, row_index, row):
        self.data[row_index] = self.data[row_index] ^ row
        
    def _setCell(self, col_index, row_index, value):
        if self._getCell == value:
            return
        
        mask = 1 << col_index
        self._updateRow(row_index, mask)
        
    def getRowPrintable(self, row_index):
        row = [False]*self.width
        for c in range(self.width):
            row[c] = self._getCell(c, row_index)
        return row
        
    def _clearRows(self):
        offset = 0
        for r in range(self.height):
            if r+ offset >= self.height:
                break
            
            if self.checkFullRow(r+offset):
                offset += 1 
                continue
                
            if offset > 0:
                self.data[r] = self.data[r+offset]
                
        return offset
                
    def __getitem__(self,row_index):
        return self.getRowPrintable(row_index)
    
    
