import UC_SGSIM_py as UC
import numpy as np
import matplotlib.pyplot as plt
import time

def SGSIM_py_controllor(*args, **kwargs):
    
    X = args[0]
    nR = args[1]
    bw = args[2]
    hs = args[3]
    a = args[4]
    C0 = args[5]
    randomseed = args[6]
    model = args[7]
    kernel = args[8]

    X = range(X)
    hs = np.arange(0, hs, bw)

    if model == 'Gaussian':
        Cov_model = UC.Gaussian(hs, bw, a, C0)
    else:
        Cov_model = UC.Gaussian(hs, bw, a, C0)

    if kernel == "C":
        sgsim = UC.Simulation_byC(X, Cov_model, nR, randomseed) # Create simulation and input the Cov model
    
        sgsim.cpdll(randomseed) # Start compute with n CPUs
        sgsim.vario_cpdll(1)

    elif kernel == "Python":

        sgsim = UC.Simulation(X, Cov_model, nR, randomseed)
        sgsim.compute(1, randomseed)
        sgsim.variogram_compute()

    theory_model = Cov_model.Var_compute(hs)
    print("ADAD",np.shape(sgsim.Variogram))
    Vario_mean=np.zeros(len(hs))
    for i in range(len(hs)):
        Vario_mean[i]=np.mean(sgsim.Variogram[i,:])

    return [sgsim.RandomField,sgsim.Variogram, theory_model, Vario_mean]
