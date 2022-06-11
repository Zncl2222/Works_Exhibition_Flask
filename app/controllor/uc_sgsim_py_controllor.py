import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time
import numpy as np
import app.model.UC_SGSIM_py as UC


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
    elif model == "Spherical":
        Cov_model = UC.Spherical(hs, bw, a, C0)

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

def plot_empty_canvas():
    
    fig = Figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot()
    #ax.set_title("Empty Canvas",fontsize=20)
    #ax.set_xlabel("Index",fontsize=18)
    #ax.set_ylabel("Value",fontsize=18)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    FigureCanvas(fig).print_png(buf)

    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


def Plot_2(data, ptitle):

    fig = Figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data)
    ax.set_title(ptitle,fontsize=20)
    ax.set_xlabel("Index",fontsize=18)
    ax.set_ylabel("Value",fontsize=18)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    FigureCanvas(fig).print_png(buf)

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return Response(buf.getvalue(), mimetype='image/png')
    return data

def variogram_plot(variogram, theory_model, vario_mean):
    
    fig = Figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(variogram,alpha=0.3)
    a, = ax.plot(theory_model, 'o',markeredgecolor='k',markerfacecolor='w')
    b, = ax.plot(vario_mean,'--',color='r')
    ax.set_title("Variogram",fontsize=20)
    ax.set_xlabel("Lag Distance",fontsize=18)
    ax.set_ylabel("Value",fontsize=18)
    ax.legend(handles = [a, b],labels = ['Theory model', "Rf mean"],
                edgecolor = 'k')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    # Embed the result in the html output.
    FigureCanvas(fig).print_png(buf)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data