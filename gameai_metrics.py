class Metric(object):
    def get_score(self, world, prev_world):
        return 0
        
class BlockedMetric(Metric):
    def get_score(self, world, prev_world):
        blocked_squares = 0.0
        for x in xrange(world.width):
            column = world[x]
            for y in xrange(world.get_col_height(x)-1, -1, -1):
                if column[y] is None and world.get_col_height(x) > world.height-y: 
                   blocked_squares += 1.0
        blocked_squares /= world.width*world.height
        return -blocked_squares
        
class CompactedMetric(Metric):
    def get_score(self, world, prev_world):
        compacted = 0.0
        count = 0
        for y in xrange(world.height):
            for x in xrange(world.width):
                if world[x][y] is not None:
                    compacted += float(y)
                    count += 1
        if count > 0:
            compacted /= count*world.height
            
        return - compacted
        
class FuturePotentialMetric(Metric):
    def get_score(self, world, prev_world):
        
        future_potential = 0.0
        for x in xrange(world.width):
            for y in xrange(world.height-1, -1, -1):
                if world[x][y] is None and world.get_col_height(x) > world.height-y: 
                    future_potential += world.get_col_height(x)-y
        future_potential /= 1000
        
        return -future_potential
        
class HighestColMetric(Metric):
    def get_score(self,world, prev_world):
        highest_row = 0
        for x in xrange(0,world.width):
            highest_row = max(highest_row, float(world.get_col_height(x)))
            
        highest_row = (highest_row)/world.height
        
        return -highest_row
        
        
class ColumnDiffMetric(Metric):
    def get_score(self,world, prev_world):
        
        col_diff = 0.0
        last_height = world.get_col_height(0)
        for x in xrange(1,world.width):
            cur_height = world.get_col_height(x)
            col_diff += abs(last_height-cur_height)
            
        col_diff /= (world.width-1)*world.height
        return -col_diff*0.1
        
        
        
class DeltaRowsMetric(Metric):
    def get_score(self,world, prev_world):
        
        delta_rows = world.rows_cleared - prev_world.rows_cleared
        
        return delta_rows*10
