from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from backend import *
from datetime import date

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "ThisIsHokkyss"

@app.route("/", methods=["GET"])
def fill_input():
    session.clear()
    return render_template('index.html', step=1)

@app.route("/", methods=["POST"])
def fill():
    sender:str = request.form.get("sender")
    sent_on:str = request.form.get("sent_on")
    speed:float = request.form.get("speed")

    if sent_on == "":
        sent_on = str(date.today())
    
    session["sender"] = sender
    session["sent_on"] = sent_on
    session["speed"] = speed
    return redirect(url_for('second_step'))

@app.route("/input", methods=["GET"])
def second_step():
    filled = not(session.get("sender") == None or session.get("sent_on") == None or session.get("speed") == None)
    if not(filled):
        return redirect(url_for('fill'))

    return render_template('index.html', step=2)

@app.route("/input", methods=["POST"])
def second_step_validation():
    locations = request.form.get("locations")
    
    try:
        locations = Location.convert_to_list_from_string(locations)
    except:
        return jsonify(error="No locations provided")

    session["locations"] = locations
    return redirect(url_for('third_step'))

@app.route("/file", methods=["GET"])
def second_step_file():
    filled = not(session.get("sender") == None or session.get("sent_on") == None or session.get("speed") == None)
    if not(filled):
        return redirect(url_for('fill'))
    
    return render_template('index.html', step=3)

@app.route("/file", methods=["POST"])
def second_step_file_validation():
    files = request.files.getlist("file")

    session["locations"] = []

    for file in files:
        content = file.stream.read().decode("UTF8")
        content = from_JSON(content)
        for location in content:
            loc = Location.from_dict(location)
            session["locations"].append(loc)

    return redirect(url_for('third_step'))

@app.route("/final", methods=["GET"])
def third_step():
    filled = not(session.get("sender") == None or session.get("sent_on") == None or session.get("speed") == None)
    if not(filled):
        return redirect(url_for('fill'))
    
    filled = filled and not(session.get("locations") == None)
    if not(filled):
        return redirect(url_for('second_step'))
    
    return render_template('index.html', step=4, locations=session["locations"])

@app.route("/final", methods=["POST"])
def third_step_validation():
    start = request.form.get("start")
    session["start"] = start

    locations: list = session["locations"]
    N: int = len(locations)
    matrix: list = [[-1 for j in range(N)] for i in range(N)]
    city_list: list = [city["name"] for city in locations]

    for i in range(N):
        for j in range(N):
            if (i == j):
                matrix[i][j] = -1
            else:
                matrix[i][j] = Location.haversine(locations[i], locations[j])
    
    graph = Graph(first_city_name=start, adj_matrix=matrix, city_list=city_list)
    path, cost = graph.BranchAndBound()
    path.append(start)

    temp_path = {"distance": cost, "path": [
        locations[city_list.index(city)] for city in path
    ]}

    push(sender=session.get("sender"), locations=session.get("locations"), result=temp_path, start=session.get("start"), speed=session.get("speed"), sent_on=session.get("sent_on"))

    if (session.get("start") == None):
        return redirect(url_for('third_step'))

    return redirect(url_for('result'))

@app.route("/path", methods=["GET", "POST"])
def result():
    sender = request.args.get("sender")
    sent_on = request.args.get("sent_on")

    if(sender == None):
        result = get_latest()
        (_, sender, date, locations, start, result, speed) = result
        # return jsonify(from_JSON(locations.decode("UTF8")))
        return from_JSON(result.decode("UTF8"))
    elif(sent_on == None):
        result = get_by_name_and_date(sender=sender)
    else:
        result = get_by_name_and_date(sender=sender, sent_on=sent_on)
    return render_template('result.html')

if __name__ == '__main__':
    app.run()