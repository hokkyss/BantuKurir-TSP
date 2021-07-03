from flask import Flask, render_template, redirect, request, url_for
from TSP import Graph

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def upload():
    print(request.form)
    file = request.form.get("file")
    print(request.files)

    matrix = [[-1, 20, 30, 10, 11], [15, -1, 16, 4, 2], [3, 5, -1, 2, 4], [19, 6, 18, -1, 3], [16, 4, 7, 16, -1]]
    g = Graph('A', matrix, ["A", "B", "C", "D", "E"])
    g.BranchAndBound()

    print(file)
    return redirect(url_for('home'))
    print(request.form)
    locations = request.form["locations"]
    goal = request.form["goal"]
    date = request.form["date"]
    file = request.form["files"]
    return redirect(url_for("result", type=user))

@app.route("/res/<type>/name", methods=["GET"])
def result(type):
    return render_template('result.html')

if __name__ == '__main__':
    app.run()