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
        #self.metrics.append(CompactedMetric())
        #self.metrics.append(FuturePotentialMetric())
        #self.metrics.append(HighestColMetric())
        self.metrics.append(ColumnDiffMetric())
        self.metrics.append(DeltaRowsMetric())
        
    def score(self,world, prev_world, debug = False):
        score = 0.0
        debugging = []


        for metric, weight in zip(self.metrics, self.weights):
            n = metric.get_score(world, prev_world)*weight
            try:
                o = metric.get_score(prev_world, None)*weight
            except:
                o = 0
            score += n
            
            
            debugging.append((metric.__class__.__name__, n, o))
        return score, debugging

                
    def get_position(self,world):
        #First step lookup
        moves = self.lookup_moves(world, world.get_current_block())
        results = moves

        #Second step lookup
        new_moves = []
        results = []
        for s,b,w,d in moves:
            new_world = w.clone()
            new_world.set_current_block(b)
            new_world.fast_forward()
            new_world.set_current_block(w.get_next_block().copy())
            
            t = self.lookup_moves(new_world, new_world.get_current_block())
            for s2,b2,w2,d in t:
                results.append((s2,b,d))
            new_moves.extend(t)
        moves = new_moves
                
                
        #Picking a move
        try:
            #max_score = max(map(lambda x: x[0], moves))
            #moves = filter( lambda x: x[0] >= max_score,moves)
            
            results = sorted(results, key=lambda x: x[0], reverse=True)
            top = int(len(results)*0.1)
            
            print "Top scores:", map(lambda x: x[0], results[:top])
            s, b, d = choice(results[:2])
            for metric, new, old in d:
                print metric, new, old
            
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
                
                s, d = self.score(cworld, world)
                
                move = (s, b, world, d)
                moves.append(move)
                
        moves = sorted(moves, key=lambda x: x[0], reverse=True)
        
        #best_score = moves[0][0]
        #moves = filter(lambda x: x[0]>=best_score, moves)
        
        return moves
		
		
class Human(Player):
	def get_position(world, current_block):
		pass
