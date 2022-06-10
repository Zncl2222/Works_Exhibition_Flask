import app.model.UC_SGSIM_py as UC
from app.model.UC_SGSIM_py.Krige.kriging import Kriging
from app.model.UC_SGSIM_py.Plot.Plot import Visualize
import numpy as np
from ctypes import *
import time
import os

class Simulation:
    
    def __init__(self, Y, model, nR,  randomseed = 0, krige_method='SimpleKrige'):
        self.Y = Y
        self.model = model
        self.nR = nR
        self.hs=model.hs
        self.bw=model.bw
        self.randomseed = randomseed
        self.krige_method = krige_method
        self.size = len(self.Y)
        self.RandomField = np.empty([self.size, self.nR])
        self.parallel_times = 0
        self.n_process = 1

    def compute(self, randomseed = 0, parallel = False):
        
        if parallel == True:
            self.randomseed = randomseed
        else:
            self.n_process = 1

        initial_seed = self.randomseed

        if self.krige_method == 'SimpleKrige':

            self.krige = UC.SimpleKrige(self.model)

        counts = 0

        start_time = time.time()

        while counts < self.nR // self.n_process:
            
            boundary_constrained = 0 
            unsampled = np.linspace(0, self.size-1, self.size)
            
            if boundary_constrained == 0:
                y_value = np.random.normal(0,1,2).reshape(2,1)
                x_grid = np.array([0, self.size-1]).reshape(2,1)
                Z = np.zeros(self.size)
                Z[0], Z[-1] = y_value[0], y_value[1]
                unsampled = np.delete(unsampled,[0,-1])
                neigh = 0 
            else:
                y_value = np.random.normal(0,1,1).reshape(1,1)
                ridx = np.random.randint(0,self.size-1,1)
                x_grid = np.array([ridx]).reshape(1,1)
                Z = np.zeros(self.size)
                Z[ridx] = y_value[0]
                unsampled = np.delete(unsampled,[ridx])
                neigh = 1

            L = np.hstack([x_grid, y_value])

            np.random.seed(self.randomseed)
            randompath = np.random.choice(unsampled, len(unsampled), replace=False)
            
            for i in range(len(unsampled)):

                Z[int(randompath[i])] = self.krige.compute(L, randompath[i], neigh, self.randomseed)
            
                temp = np.hstack([randompath[i],Z[int(randompath[i])]])
                L = np.vstack([L,temp])
                
                if neigh<6:
                    neigh += 1
                
                self.randomseed += 1

            Z_Gap = abs(Z.max()-Z.min())

            if 2<Z_Gap<=6.5:
                self.RandomField[:,counts] = Z
                counts = counts+1
                #print('Progress = %.2f' % (counts/self.nR*100)+'%', end='\r')

            self.randomseed += 1
            
        #print('Progress = %.2f' % 100+'%\n', end='\r')
        
        end_time = time.time()
        
        #print('Time = %f'%(end_time-start_time),'s\n')
        #print("Last RandomSeed = %d" %(self.randomseed),'\n')
        #print("RandomSeed passed = %d" %(self.randomseed-initial_seed),'\n')
        #print("Theroritical Randomseed = %d" %(initial_seed+(self.end-self.start)*self.nR))
        return self.RandomField

    def variogram_compute(self, n_process = 1):
    
        model_len = self.size
        
        x=np.linspace(0,self.size-1,model_len).reshape(model_len,1)
        print(np.shape(self.RandomField))
        print(np.shape(x))
        self.Variogram = np.empty([len(self.hs), self.nR])
        
        for i in range(self.nR):
            L=np.hstack([x,self.RandomField[:,i].reshape(model_len,1)])
            self.Variogram[:,i] = self.model.Variogram(L)

        #self.Variogram = np.array(self.Variogram).T

    def MeanPlot(self,n,mean=0,std=1):
        
        m_plot = Visualize(self.model, self.RandomField)
        m_plot.MeanPlot(n, mean, std)
        
    def VarPlot(self,mean=0,std=1):
    
        s_plot = Visualize(self.model, self.RandomField)
        s_plot.Variance_Plot(mean, std)

    def Cdf_Plot(self, x_location):

        c_plot = Visualize(self.model, self.RandomField)
        c_plot.CDF_Plot(x_location)
    
    def Hist_Plot(self, x_location):

        h_plot = Visualize(self.model, self.RandomField)
        h_plot.HIST(x_location)

    def VarioPlot(self):

        v_plot = Visualize(self.model, self.RandomField)
        print(np.shape(self.Variogram))
        v_plot.Variogram_Plot(self.Variogram)

    def Save_RandomField(self, path):
                
        for i in range(self.nR):
            
            if i<10:
                number='000'+str(i)
            elif 10<=i<100:
                number='00'+str(i)
            elif 100<=i<1000:
                number='0'+str(i)
            elif i>=1000:
                number=str(i)
            
            with open(path+'Realizations'+number+'.txt', 'w') as f:

                for j in range(0, self.size):

                    print('%.2d' %(j) ,'%10.6f' %(self.RandomField[j,i]), file=f)
    
    def Save_Variogram(self, path):

        for i in range(self.nR):
                    
            if i<10:
                number='000'+str(i)
            elif 10<=i<100:
                number='00'+str(i)
            elif 100<=i<1000:
                number='0'+str(i)
            elif i>=1000:
                number=str(i)
                    
            with open(path+'Variogram'+number+'.txt', 'w') as f:

                for j in range(0, len(self.hs)):

                    print('%.2d' %(j) ,'%10.6f' %(self.RandomField[j,i]), file=f)

class Simulation_byC(Simulation):

    def __init__(self, Y, model, nR, randomseed = 0, krige_method='SimpleKrige'):
        super().__init__(Y, model, nR, randomseed, krige_method)
        self.dll = CDLL('./app/model/UC_SGSIM_py/lib/sgsim.so')
        self.sgsim = self.dll.sgsim_dll

    def cpdll(self,randomseed):
        
        #dll = CDLL('./app/model/UC_SGSIM_py/lib/sgsim.so')
        #dll = CDLL('./app/model/UC_SGSIM_py/lib/sgsim.dll')
        #sgsim = dll.sgsim_dll
        self.sgsim.argtypes = (POINTER(c_double),c_int, c_int, c_double, c_double, c_int)
        self.sgsim.restype = None 
        mlen = int(self.size)
        nR = int(self.nR//self.n_process)
        self.RandomField = np.empty([self.size, nR])
        array = (c_double * (mlen*nR))()

        self.sgsim(array, mlen, nR, 17.32, 1, randomseed)

        for i in range(nR):
            self.RandomField[:,i] = list(array)[i*mlen:(i+1)*mlen]
        return self.RandomField


    def vario_cpdll(self, cpu_number):
        
        #dll =CDLL('./app/model/UC_SGSIM_py/lib/sgsim.so')
        #dll = CDLL('./app/model/UC_SGSIM_py/lib/sgsim.dll')
        vario = self.dll.variogram
        vario.argtypes = (POINTER(c_double),POINTER(c_double), c_int, c_int, c_int)
        vario.restype = None 

        mlen = int(self.size)
        nR = int(self.nR//self.n_process)

        Variogram = np.empty([self.size, nR])
        vario_size = len(self.hs)

        vario_array = (c_double * (vario_size))()
        RandomField_array = (c_double * (mlen))()

        self.Variogram = np.empty([vario_size, nR])
       
        for i in range(nR):
            RandomField_array[:] = self.RandomField[:,i]
            vario(RandomField_array,vario_array, mlen, vario_size, 1)
            self.Variogram[:,i] = list(vario_array)

        return self.Variogram
