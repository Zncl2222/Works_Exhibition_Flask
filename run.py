from flask import Flask, request, jsonify, render_template, Response, send_file
from flask_cors import CORS

from model import qsort
from UC_SGSIM_py_controllor import SGSIM_py_controllor
import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time
import numpy as np

app = Flask(__name__)
CORS(app)

def Plot(data, ptitle,pcolor):
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot(data,linestyle='--',marker='o',color='k',markerfacecolor=pcolor,markeredgecolor='k',markersize='8')
    ax.set_title(ptitle,fontsize=20)
    ax.set_xlabel("Index",fontsize=18)
    ax.set_ylabel("Value",fontsize=18)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.route('/plot.png')
def Plot_2(data, ptitle):

    fig = Figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(data)
    ax.set_title(ptitle,fontsize=20)
    ax.set_xlabel("Index",fontsize=18)
    ax.set_ylabel("Value",fontsize=18)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    # Embed the result in the html output.
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


@app.route("/quicksort", methods=["POST"])
def quicksort():
    insertValues = request.get_json()
    arr=insertValues['array']
    x1=Plot(arr, "Before sort", 'r')
    
    arr=qsort.quicksort_func(arr)
    arr=list(arr)
    x2=Plot(arr, "After sort", 'b')
    z=[x1,x2]
    return jsonify({"FigResult":z, "Result":arr})

@app.route("/SGSIM", methods=['POST'])
def SGSIM():
    insertValues = request.get_json()
    X = insertValues['X_Grid']
    nR = insertValues['Realizations_Numbers']
    bw = insertValues['Lag_Bandwidth']
    hs = insertValues['Lag_range']
    a = insertValues['Effective_Range']
    C0 = insertValues['Sill']
    randomseed = insertValues['Randomseed']
    model = insertValues['Model']


    res = SGSIM_py_controllor(X,nR,bw,hs,a,C0,randomseed,model)
    
    p = Plot_2(res, "Results")

    return jsonify({"X_Result":p,})

@app.route("/", methods=["GET"])
def button():
    return render_template("home.html")

@app.route("/result", methods = ["POST","GET"])
def result():
    output = request.form.to_dict()
    X = int(output['model_len'])
    nR = int(output['nR'])
    bw = int(output['bw'])
    hs = int(output['hs'])
    a = float(output['range'])
    C0 = int(output['sill'])
    randomseed = int(output['randomseed'])
    model = output['model']
    kernel = output['kernel']

    start = time.time()
    res = SGSIM_py_controllor(X,nR,bw,hs,a,C0,randomseed,model,kernel)
    end = time.time()

    time_spend = np.round(end - start,4)

    rfg = Plot_2(res[0], "RandomField")

    vario = variogram_plot(res[1], res[2], res[3])
    
    return render_template("home.html", img_rfg = rfg, img_vario = vario, t = time_spend)
    #return Response(p.getvalue(), mimetype='image/png')

@app.route('/download')
def download():
    path = r'.\static\temp.png'
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)