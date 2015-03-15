import numpy as np

from random import choice

from gameai_metrics import *

class Player(object):
	def get_position(world, current_block):
		pass


class AI(Player):
    def __init__(self, parameters):
        self.weights = parameters
        
        self.metrics = []
        
        self.metrics.append(BlockedMetric())
        self.metrics.append(CompactedMetric())
        self.metrics.append(FuturePotentialMetric())
        self.metrics.append(HighestColMetric())
        self.metrics.append(ColumnDiffMetric())
        self.metrics.append(DeltaRowsMetric())
        
    def score(self,world, prev_world, debug = False):
        score = 0.0

        for metric, weight in zip(self.metrics, self.weights):
            score += metric.get_score(world, prev_world)*weight
        
        return score
    #def get_position(self,world):
        
        #moves = self.lookup_moves(world, world.get_current_block())
        
        #lookahead = 1
        
        #max_score = max(map(lambda x: x[0], moves))
        #first_moves = filter( lambda x: x[0] >= max_score,moves)
        
        
        #results = []
        
        #if lookahead < 2:
            #results.extend(first_moves)
        #else:
            #for s,b in first_moves:
                #new_world = world.clone()
                #new_world.set_current_block(b)
                #new_world.fast_forward()
                #new_world.set_current_block(world.get_next_block().copy())
                
                #moves = self.lookup_moves(new_world, new_world.get_current_block())
                    
                #max_score = max(map(lambda x: x[0], moves))
                #second_moves = filter( lambda x: x[0] >= max_score,moves)
                
                #if lookahead < 3:
                    #for s2,b2 in second_moves:
                        #results.append((s2,  b))
                
                #else:
                    #blocks = BlockGenerator()
                    
                    #for s2,b2 in second_moves:
                        
                        #avg_score = 0.0
                        #for i in xrange(len(blocks)):
                            #future_world = new_world.clone()
                            #future_world.set_current_block(b2.copy())
                            #future_world.fast_forward()
                            #future_world.set_current_block(blocks[i])
                            
                            #moves = self.lookup_moves(future_world, future_world.get_current_block())       
                            
                            #try:
                                #s3, b3 = moves[0]
                                
                                #avg_score += s3
                            #except:
                                #pass
                        
                        #avg_score /= len(blocks)
                        #results.append((avg_score,b))
                
                
        #try:
            
            #max_score = max(map(lambda x: x[0], results))
            #results = filter( lambda x: x[0] >= max_score,results)
            
            ##results = sorted(results, key=lambda x: x[0], reverse=True)
            #s, b = choice(results)
            #return b
        #except:
            #import traceback
            
            #print traceback.format_exc()
            #print "Returning none, this will fail"
            #return None
                
    def get_position(self,world):

        moves = self.lookup_moves(world, world.get_current_block())

        lookahead = 2

        max_score = max(map(lambda x: x[0], moves))
        first_moves = filter( lambda x: x[0] >= max_score,moves)


        results = []

        if lookahead < 2:
            results.extend(first_moves)
        else:
            for s,b in first_moves:
                new_world = world.clone()
                new_world.set_current_block(b)
                new_world.fast_forward()
                new_world.set_current_block(world.get_next_block().copy())
                
                moves = self.lookup_moves(new_world, new_world.get_current_block())
                    
                max_score = max(map(lambda x: x[0], moves))
                second_moves = filter( lambda x: x[0] >= max_score,moves)
                
                if lookahead < 3:
                    for s2,b2 in second_moves:
                        results.append((s2,  b))
                
                else:
                    blocks = BlockGenerator()
                    
                    for s2,b2 in second_moves:
                        
                        avg_score = 0.0
                        for i in xrange(len(blocks)):
                            future_world = new_world.clone()
                            future_world.set_current_block(b2.copy())
                            future_world.fast_forward()
                            future_world.set_current_block(blocks[i])
                            
                            moves = self.lookup_moves(future_world, future_world.get_current_block())       
                            
                            try:
                                s3, b3 = moves[0]
                                
                                avg_score += s3
                            except:
                                pass
                        
                        avg_score /= len(blocks)
                        results.append((avg_score,b))
                
                
        try:
            
            max_score = max(map(lambda x: x[0], results))
            results = filter( lambda x: x[0] >= max_score,results)
            
            #results = sorted(results, key=lambda x: x[0], reverse=True)
            s, b = choice(results)
            return b
        except:
            import traceback
            
            print traceback.format_exc()
            print "Returning none, this will fail"
            return None
            
                

        
    def lookup_moves(self, world, b):		
        score = None
        
        moves = []
        all_orientations =  world.get_current_block().get_all_orientations()
        for cblock in all_orientations:
            for x in xrange(world.width):
                cworld = world.clone()
                cworld.set_current_block(cblock.copy())
                cblock.pos[0] = x
                
                b = cworld.get_current_block().copy()
                
                if cworld.detect_collision():
                    continue
                cworld.fast_forward()    
                
                s = self.score(cworld, world)
                
                move = (s, b)
                moves.append(move)
                
        moves = sorted(moves, key=lambda x: x[0], reverse=True)
        
        best_score = moves[0][0]
        moves = filter(lambda x: x[0]>=best_score, moves)
        
        return moves
		
		
class Human(Player):
	def get_position(world, current_block):
		pass
