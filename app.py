from flask import Flask, render_template, redirect, request, url_for
from TSP import Graph

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def upload():
    matrix = [[-1, 20, 30, 10, 11], [15, -1, 16, 4, 2], [3, 5, -1, 2, 4], [19, 6, 18, -1, 3], [16, 4, 7, 16, -1]]
    another_matrix = [[-1, 2, 7, 8], [6, -1, 3, 7], [5, 8, -1, 4], [7, 6, 9, -1]]
    first_city_name: str = "C"
    
    g = Graph(first_city_name, matrix, ["A", "B", "C", "D", "E"])
    path, cost = g.BranchAndBound()
    path.append(first_city_name)

    g2 = Graph(first_city_name, another_matrix, ["A", "B", "C", "D"])
    path2, cost2 = g2.BranchAndBound()
    path2.append(first_city_name)

    print(cost, " ".join(path))
    print(cost2, " ".join(path2))

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