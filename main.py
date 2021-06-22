from flask import Flask, render_template, request
from styem.GetData import GetData
import json
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/get_data", methods=['POST'])
def get_data():
    #GetData.get_data()
    stock = request.values['stock']
    sdate = request.values['sdate']
    edate = request.values['edate']
    d1 = int(request.values['D1'])
    d2 = int(request.values['D2'])
    c1 = int(request.values['C1'])
    c2 = int(request.values['C2'])
    c3 = int(request.values['C3'])

    response = app.response_class(
        response=json.dumps(GetData.tradingtrends(stock,sdate,edate,d1,d2,c1,c2,c3)),
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)