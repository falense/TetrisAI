
#import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt 
import os
import datetime
import json
import shutil

from matplotlib.patches import Rectangle, Circle, RegularPolygon, Arrow



            
class ParetoView(object):
    subfolder = "Pareto_view"
    def __init__(self, logfolder):
        plt.figure(1)
        plt.clf()
        
        self.logfolder = logfolder
        
        self.lim_axis = None
        
        self.view = plt.gcf().gca()
        self.view_ax = plt.gca()
        
    def setup_view(self):
        self.view.set_ylabel("Lines cleared")
        self.view.set_xlabel("Score")
        self.view_ax.axis([0,self.lim_axis[0],0,self.lim_axis[1]])
        self.view.grid(b=True)
        
    def update(self,gen,pop,hof):
        plt.figure(1)
        
        self.view.cla()
        
        results =  [i.fitness.values for i in hof]
        data_x = map(lambda x: x[1],results)
        data_y = map(lambda x: x[0],results)
        
        if self.lim_axis is None:
            self.lim_axis = (max(data_x)*2,max(data_y)*2)
        
        
        self.setup_view()
        
        self.view.plot(data_x, data_y)
        
        plt.draw()
        folder = os.path.join(self.logfolder, self.subfolder)
        if not os.path.exists(folder):
            os.makedirs(folder)   
        plt.savefig(os.path.join(folder,"Paretofront_%s.png"%gen))

class Progress(object):
    def __init__(self):
        plt.close("all")

        self.views = []
        self.num_pheno_views = 0
        
        
        self.logfolder = "log"
        if not os.path.exists(self.logfolder):
            os.makedirs(self.logfolder)   
            
            
        #view = ParetoView(self.logfolder)
        #self.views.append(view)
            
        self.pop_dump_folder = os.path.join(self.logfolder, "Population_dump")
        
        if not os.path.exists(self.pop_dump_folder):
            os.makedirs(self.pop_dump_folder)   
            
        #plt.ion()
        #plt.show()
    def update(self,gen,pop,hof):   
        for view in self.views:
            view.update(gen,pop,hof)
        self.dump_population(gen,pop,hof)
        
        
    def dump_population(self,gen,pop,hof):
        population_file = os.path.join(self.pop_dump_folder, "generation_%s.txt" % gen)
        paretofront_file = os.path.join(self.pop_dump_folder, "paretofront_%s.txt" % gen)
        
        f = open(population_file,"w")
        for individual in pop:
            d = json.dumps(individual)
            f.write(d + "\n")
        f.close()
        
        f = open(paretofront_file,"w")
        for individual in hof:
            d = json.dumps(individual)
            f.write(d + "\n")
        f.close()
            
        
        
            
    def hold(self):
        plt.ioff()
        plt.show()
