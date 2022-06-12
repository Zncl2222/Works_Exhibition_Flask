from app import app
from flask import request, jsonify, render_template, Response, send_file
from app.controllor import uc_sgsim_py_controllor as ucc
import time
import numpy as np

@app.route("/")
def about():
    return render_template("home.html")

@app.route("/works")
def works():
    return render_template("works.html")

@app.route("/sgsim", methods=["GET"])
def sgsim():
    empty_canvas = ucc.plot_empty_canvas()
    #return render_template("home.html",img_rfg = empty_canvas, img_vario =empty_canvas)
    return render_template("sgsim.html",img_rfg = empty_canvas, img_vario =empty_canvas)

@app.route("/author")
def author():
    return render_template("author.html")

@app.route("/acheivement")
def acheivement():
    return render_template("acheivement.html")


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

@app.route("/sgsim/results", methods = ["POST","GET"])
def sgsim_results():

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
    res = ucc.SGSIM_py_controllor(X,nR,bw,hs,a,C0,randomseed,model,kernel)
    end = time.time()

    time_spend = np.round(end - start,4)

    rfg = ucc.Plot_2(res[0], "RandomField")

    vario = ucc.variogram_plot(res[1], res[2], res[3])
    
    #return render_template("home.html", img_rfg = rfg, img_vario = vario, t = time_spend)
    return render_template("sgsim.html", img_rfg = rfg, img_vario = vario, t = time_spend)

