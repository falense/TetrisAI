import random
import os
import numpy
import traceback,sys
import multiprocessing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from problem import fitness
from progress import Progress

def bootstrap(population_size):
    creator.create("Fitness", base.Fitness, weights=(1.0,))# 1.0))
    creator.create("Individual", list, fitness=creator.Fitness, step_count=None)

    toolbox = base.Toolbox()

    def initConfiguration(individ_class, weight_count):
        r = []
        
        for x in xrange(weight_count):
            weight = random.uniform(0.0,1.0)
            r.append(weight)
                
                
        return individ_class(r)
    
    toolbox.register("individual", initConfiguration, creator.Individual, 6)
  
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #pool = multiprocessing.Pool()
   # toolbox.register("map", pool.map)

    toolbox.register("evaluate", fitness)
    
    
    #def cxOnePoint(ind1, ind2):
        #size = min(len(ind1), len(ind2))
        #cxpoint = random.randint(1, size - 1)
        
        #tmp_ind1 = ind2[:cxpoint] + ind1[cxpoint:]
        #tmp_ind2 = ind1[:cxpoint] + ind2[cxpoint:]
        
        #emergency_breakout = 10000
        #while convert_ind_to_uav_count(conf,tmp_ind1) == 0 or convert_ind_to_uav_count(conf,tmp_ind2) == 0:
            #cxpoint = random.randint(1, size - 1)
            #tmp_ind1 = ind2[:cxpoint] + ind1[cxpoint:]
            #tmp_ind2 = ind1[:cxpoint] + ind2[cxpoint:]
            
            #emergency_breakout -= 1
            #if emergency_breakout == 0:
                #cxpoint = 0
                #print "Unable to find a suitable crossover"
                #break
                
        #ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
        
        #if convert_ind_to_uav_count(conf,ind1) == 0 or convert_ind_to_uav_count(conf,ind2) == 0:
            #print "Warning null uavs"
        
        #return ind1, ind2
    
    toolbox.register("mate", tools.cxOnePoint)
    
    def mutate(individual):
        index = random.randint(0,len(individual)-1)
        
        individual[index] += random.gauss(0,0.1)
    
        individual[index] = max(0.0, min(1.0, individual[index]))
        
        return individual,
    
    toolbox.register("mutate", mutate)
    
    toolbox.register("select", tools.selRoulette)



    MGA_LOGFOLDER = "mga_log"    
    pop = toolbox.population(n=population_size)

    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    return pop, toolbox, hof, stats


def main():
    population_size = 50
    lambda_size = 50
    
    pop, toolbox, hof, stats =   bootstrap(population_size)
    prog = Progress()
    
            
    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, mu=population_size, lambda_=lambda_size, 
            cxpb=0.7, mutpb=0.05, ngen=0, stats=stats, halloffame=hof)
    prog.update(0,pop,hof)
    for gen in range(1000):
        pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, mu=population_size, lambda_=lambda_size, 
                cxpb=0.7, mutpb=0.05, ngen=1, stats=stats, halloffame=hof)
        prog.update((gen+1),pop,hof)
    
    
    return pop, stats, hof
                 
if __name__ == "__main__":
    main()                 

